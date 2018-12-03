# -*- coding: utf-8 -*-
import mimetypes
import os

from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from minio import Minio
from minio.error import InvalidXMLError, InvalidEndpointError,  NoSuchKey, NoSuchBucket, ResponseError
from urllib3.exceptions import MaxRetryError
import tempfile

# from django.core.files.base import File


def setting(name, default=None):
    """
    Helper function to get a Django setting by name or (optionally) return
    a default (or else ``None``).
    """
    return getattr(settings, name, default)


@deconstructible
class MinioStorage(Storage):
    # TODO: Log errors caused by exceptions
    server = setting('MINIO_SERVER')
    access_key = setting('MINIO_ACCESSKEY')
    secret_key = setting('MINIO_SECRET')
    bucket = setting('MINIO_BUCKET')
    secure = setting('MINIO_SECURE')
    default_content_type = 'application/octet-stream'

    def __init__(self, *args, **kwargs):
        super(MinioStorage, self).__init__(*args, **kwargs)
        self._connection = None

        if not self.server or not self.access_key or not self.secret_key or not self.bucket:
            raise ValueError(
                "Please provider settings parameters for connect mino s3 : MINIO_SERVER, MINIO_ACCESSKEY, MINIO_SECRET, MINIO_BUCKET")

        if "http:" in self.server:
            raise ValueError(
                "MINIO_SERVER : Hostname cannot have a scheme http")

    @property
    def connection(self):
        if not self._connection:
            try:
                self._connection = Minio(
                    self.server, self.access_key, self.secret_key, self.secure)
            except InvalidEndpointError:
                self._connection = None
        return self._connection

    def _open(self, name, mode='rb'):
        try:
            if self.connection:
                data = self.connection.get_object(self.bucket, name)

                # Using Temporary File Store Object
                with tempfile.TemporaryFile() as fp:
                    for d in data.stream(32 * 1024):
                        fp.write(d)

        except Exception as err:
            fp.close()
            raise err  # Let it bubble up if it was some other error
        return fp

    def _save(self, name, content):
        """
            Parameter content is instance of Django File
        """
        # Buid path and hash filename
        pathname, ext = os.path.splitext(str(name.encode('utf-8')))
        dir_path, file_name = os.path.split(pathname)
        hashed_name = "{0}/{1}{2}".format(dir_path, hash(content), ext)

        # get content type of file
        _type, encoding = mimetypes.guess_type(name)
        content_type = getattr(content, 'content_type', None)
        content_type = content_type or _type or self.default_content_type

        # get size of file
        content_size = content.size if hasattr(
            content, 'size') else len(content)

        if self.connection:
            if not self.connection.bucket_exists(self.bucket):
                self.connection.make_bucket(self.bucket)
            try:
                self.connection.put_object(
                    self.bucket, hashed_name, content, content_size, content_type=content_type
                )
            except InvalidXMLError:
                pass
            except MaxRetryError:
                pass
        return hashed_name  # TODO: Do not return name if saving was unsuccessful

    def query_string_remove(self, url):
        return url[:url.find('?')]

    def url(self, name):
        if self.connection:
            try:
                if self.connection.bucket_exists(self.bucket):

                    url = self.connection.presigned_get_object(
                        self.bucket, name.encode('utf-8'))

                    return self.query_string_remove(url)
                else:
                    return "image_not_found"  # TODO: Find a better way of returning errors
            except MaxRetryError:
                return "image_not_found"
        return "could_not_establish_connection"

    def exists(self, name):
        try:
            self.connection.stat_object(self.bucket, name.encode('utf-8'))
            return True
        except (NoSuchKey, NoSuchBucket):
            return False
        except Exception as err:
            raise IOError("Could not stat file {0} {1}".format(name, err))

    def size(self, name):
        info = self.connection.stat_object(self.bucket, name.encode('utf-8'))
        return info.size

    def get_object_by_name(self, name):
        try:
            if self.connection:
                data = self.connection.get_object(self.bucket, name)
        except Exception as err:
            raise err
        return data

    def get_object_streaming(self, name, http_range, meta):
        try:
            if self.connection:
                size_object = self.size(name)

                start, stop = self.parse_range_header(
                    http_range, size_object)[0]
                data = self.connection.get_partial_object(
                    self.bucket, name, start, stop, None)
        except Exception as err:
            raise err
        return data

    def upload_object(self, file_temp_path, audio_path, content_type):
        """
            Function upload object to media server
        """
        if self.connection:
            if not self.connection.bucket_exists(self.bucket):
                self.connection.make_bucket(self.bucket)
            try:
                pathname, ext = os.path.splitext(audio_path)
                dir_path, file_name = os.path.split(pathname)

                with open(file_temp_path, 'rb') as file_data:
                    file_stat = os.stat(file_temp_path)
                    if file_stat.st_size == 0:
                        raise Exception("File is empty.")

                    hashed_name = "{0}/{1}{2}".format(
                        dir_path, hash(file_data), ".json")
                    self.connection.put_object(self.bucket, hashed_name,
                                               file_data, file_stat.st_size)
            except InvalidXMLError:
                hashed_name = None
                pass
            except MaxRetryError:
                hashed_name = None
                pass
            except ResponseError, e:
                print "ResponseError ", e
                hashed_name = None

        return hashed_name

    def url_encode(self):
        return self.filename

    def parse_range_header(self, header, resource_size):
        """
        Parses a range header into a list of two-tuples (start, stop) where
        `start` is the starting byte of the range (inclusive) and
        `stop` is the ending byte position of the range (exclusive).
        Args:
            header (str): The HTTP_RANGE request header.
            resource_size (int): The size of the file in bytes.
        Returns:
            None if the value of the header is not syntatically valid.
        """
        if not header or '=' not in header:
            return None

        ranges = []
        units, range_ = header.split('=', 1)
        units = units.strip().lower()

        if units != 'bytes':
            return None

        for val in range_.split(','):
            val = val.strip()
            if '-' not in val:
                return None

            if val.startswith('-'):
                # suffix-byte-range-spec: this form specifies the last N bytes
                # of an entity-body.
                start = resource_size + int(val)
                if start < 0:
                    start = 0
                stop = resource_size
            else:
                # byte-range-spec: first-byte-pos "-" [last-byte-pos].
                start, stop = val.split('-', 1)
                start = int(start)
                # The +1 is here since we want the stopping point to be
                # exclusive, whereas in the HTTP spec, the last-byte-pos
                # is inclusive.
                stop = int(stop) + 1 if stop else resource_size
                if start >= stop:
                    return None

            ranges.append((start, stop))

        return ranges
