# -*- coding: utf-8 -*-
import os
from aeneas.exacttiming import TimeValue
from aeneas.executetask import ExecuteTask
from aeneas.language import Language
from aeneas.syncmap import SyncMapFormat
from aeneas.task import Task
from aeneas.task import TaskConfiguration
from aeneas.textfile import TextFileFormat
import aeneas.globalconstants as gc
import tempfile
from s3.minio.storage import MinioStorage
import speech_recognition as sr


"""
    Author: Tiendang (tiendangdht@gmail.com)
    Description: Class ProcessAudio contains actions generate_timming_audio , 
"""
class ProcessAudio(object):
    recognize_language = "vi-VN"
    task_language = Language.VIE
    task_input_format = TextFileFormat.PLAIN
    task_output_format = SyncMapFormat.JSON

    def __init__(self, language=None):
        configuration = TaskConfiguration()
        configuration[gc.PPN_TASK_LANGUAGE] = language if language else self.task_language
        configuration[gc.PPN_TASK_IS_TEXT_FILE_FORMAT] = self.task_input_format
        configuration[gc.PPN_TASK_OS_FILE_FORMAT] = self.task_output_format
        self.config = configuration
        

    
    def generate_timming_audio(self, audio_path, text_audio_path):
        """
            Author: TienDang
            Description: Generate file mapping between audio file and text file, 
                        File mapping use highlight text when play an audio.
        """
        try:
            """
                step 1: init tow file temporary (audio_file_temp, text_audio_file_temp) use store data audio and text of audio from media server (s3).
                            Because aeneas library cannot support get data form url. support only OS file system
                step 2: init temporary file timing_mapping_file_temp is output timming mapping file when aeneas sync_map.
                step 3: init Aeneas Task and excute output_sync_map_file
                step 4: Upload file timming mapping to s3
            """
            
            # Begin step 1
            s3 = MinioStorage()
            # Download audio file and store into temporary file
            audio_file_temp = tempfile.NamedTemporaryFile(delete=False)

            object_audio_storage = s3.get_object_by_name(audio_path)
            for d in object_audio_storage.stream(32*1024):
                audio_file_temp.write(d)


            text_audio_file_temp = tempfile.NamedTemporaryFile(delete=False)
            
            object_text_audio_storage = s3.get_object_by_name(text_audio_path)
            with open(text_audio_file_temp.name, 'w+') as cxt:
                for data_text in object_text_audio_storage.stream(32*1024):
                    cxt.write(data_text)

            # End step 1

            # Begin step 2
            timing_mapping_file_temp = tempfile.NamedTemporaryFile(delete=False)
            # End step 2

            # Begin step 3
            task = Task()
            task.configuration = self.config
            task.audio_file_path_absolute = audio_file_temp.name
            task.text_file_path_absolute = text_audio_file_temp.name
            task.sync_map_file_path_absolute = timing_mapping_file_temp.name

            # # process Task
            ExecuteTask(task).execute()
            task.output_sync_map_file()

            # End step 3

            # Begin step 4
            content_type = "application/json"
            url_timming = s3.upload_object(timing_mapping_file_temp.name, audio_path, content_type)
            # End step 4
            
            if url_timming is None:
                raise Exception("Cannot upload timming mapping file to s3")

            return url_timming
            
        except Exception, e:
            raise Exception("Cannot Generate Timming For Audio : ",e)
        finally:
            os.unlink(text_audio_file_temp.name)
            os.unlink(audio_file_temp.name)
            os.unlink(timing_mapping_file_temp.name)

    
    def get_text_from_audio(self, audio_path, language=None):
        try:
            """
                step 1: init tow file temporary (audio_file_temp, text_audio_file_temp) use store data audio and text of audio from media server (s3).
                            Because aeneas library cannot support get data form url. support only OS file system
                step 2: use AudioFile of Recognizer library get text from audio
            """

            # Get extention of audio file
            pathname, ext = os.path.splitext(audio_path)

            # Begin step 1
            s3 = MinioStorage()
            # Download audio file and store into temporary file
            audio_file_temp = tempfile.NamedTemporaryFile(suffix=ext, delete=False)

            object_audio_storage = s3.get_object_by_name(audio_path)
            for d in object_audio_storage.stream(32*1024):
                audio_file_temp.write(d)

            r = sr.Recognizer()

            with sr.AudioFile(audio_file_temp.name) as source:
                print "Begin"
                # audio = r.listen(source)
                audio = r.record(source)
            
            if language is None:
                language = self.recognize_language
                
            text = r.recognize_google(audio, language=language)
            return text

        except Exception, e:
            raise Exception("Cannot Get Text From Audio : ",e)
        finally:
            os.unlink(audio_file_temp.name)

