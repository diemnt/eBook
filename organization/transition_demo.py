# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals

# from django.db import models
# from django_fsm import FSMField, transition
# import datetime

# # Create your models here.
# class Blog(models.Model):
#     class STATE:
#         DRAFF = 'draff'
#         COMPOSER = 'composer'
#         PUBLISH = 'publish'
#         UNPUBLISH = 'unpublish'

#     name = models.CharField("Name", max_length=100)
#     status = FSMField(default=STATE.DRAFF)

#     @transition(field='status', source='draff', target='composer', conditions=[])
#     def composere(self):
#         pass

#     def can_publish(instance):
#     # No publishing after 17 hours
#         if datetime.datetime.now().hour < 17:
#             return False
#         return True

#     @transition(field='status', source='composer', target='publish', conditions=[can_publish])
#     def publish(self):
#         pass

#     @transition(field='status', source='publish', target='unpublish')
#     def ununblish(self):
#         pass
