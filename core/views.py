# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.shortcuts import render
# from core.models import Banner
# from ranged_fileresponse import RangedFileResponse
from s3.range_file_response import RangedFileResponse
import mimetypes
from s3.authenticate import S3AuthenticateJWT
from s3.minio.storage import MinioStorage
import urllib
import tempfile
from django.http import StreamingHttpResponse, HttpResponse
from django.http.response import FileResponse
import cStringIO
import uuid
import os
import psutil
# Create your views here.


def protected_video(request, filename):
    print "protected_video filename ",filename
    
    # filename = settings.MEDIA_ROOT + "/" + filename
    content_type, encoding = mimetypes.guess_type(filename)
    print "#### content_type ",filename
    print "#### Check Range Request ",request.META["HTTP_RANGE"] if "HTTP_RANGE" in request.META else None
    response = RangedFileResponse(request, open(filename, 'r'), content_type=content_type)
    # print "response ",response.start
    # print "response ",response.stop
    return response


def media_access(request):
    try:
        process = psutil.Process(os.getpid())
        print "======== Begin Memory Usage ====== ", process.memory_info()[0]

        data_encode = request.GET.get('key', None)

        if data_encode is None:
            return HttpResponse()
        
        data_payload = S3AuthenticateJWT.decoding(data_encode, 60, False)
        
        path = data_payload['path']
        content_type, encoding = mimetypes.guess_type(path)
        
        file_output = cStringIO.StringIO()
        
        storage = MinioStorage()
        object_storage = storage.get_object_by_name(str(path))

        for d in object_storage.stream(32*1024):
            file_output.write(d)

        # Sets the file current position at start
        file_output.seek(0)
        response = RangedFileResponse(request, file_output, content_type=content_type)
        response['Cache-Control'] = 'no-cache'

    except Exception, e:
        file_output.close()
        print "Error access media file : ",e
        pass
    finally:
        print "======== Finally Memory Usage ====== ", process.memory_info()[0]
        print "==== Detect file is close , ", len(file_output.getvalue())

    return response

