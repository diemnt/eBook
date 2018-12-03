# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.postgres.fields import ArrayField
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db import models
from main.models import DateTimeAuthModel, DateTimeModel
from main.models import User
from django.contrib.postgres.aggregates import StringAgg
# from django.db.models.signals import post_save
# from django.dispatch import receiver


# Create your models here.
@python_2_unicode_compatible
class Staff(DateTimeModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_staff_rel")
    email = models.CharField(_('Email'), max_length=255)
    phone = models.CharField(_('Phone'), max_length=100, null=True, blank=True)
    roles = models.ManyToManyField('Role', through='StaffRole', blank=True)

    # @receiver(post_save, sender=User)
    # def create_user_staff(sender, instance, created, **kwargs):
    #     if created:
    #         print "Signal Call create_user_staff"
    #         Staff.objects.create(user=instance)

    # @receiver(post_save, sender=User)
    # def save_user_staff(sender, instance, **kwargs):
    #     print "Signal Call save_user_staff"
    #     instance.staff.save()

    def __str__(self):
        return "%s" % (self.user.username)

    def has_role_permission(self, permission_key):
        try:
            role_objects = StaffRole.objects.filter(staff=self).aggregate(
                permissions=StringAgg("role__permission", delimiter=',', distinct=True))

            # Check role objects exist and check permission is empty
            if not role_objects or not role_objects['permissions']:
                return False

            # Convert String to List
            permission_list = role_objects['permissions'].split(',')

            """
                Case 1: If permission_key is array then check list permission_key is subarrray of permission_list
            """
            if isinstance(permission_key, list):
                is_access = set(permission_key).issubset(set(permission_list))
                if not is_access:
                    print "Permission %s Forbidden." % permission_key
                    return False
                return True

            """
                Case 1: If permission_key is string then check permission_key in permission_list
            """
            if permission_key not in permission_list:
                print "Permission %s Forbidden." % permission_key
                return False

            return True
        except Staff.DoesNotExist, e:
            print "ERROR: Staff Not Found."
            return False
        except Exception, e:
            print "ERROR: Internal Server Error.", e
            return False

    class Meta:
        verbose_name = _('Staff')


@python_2_unicode_compatible
class Role(DateTimeAuthModel):
    name = models.CharField(_('Name'), max_length=255)
    description = models.CharField(
        _('Description'), max_length=255, null=True, blank=True)
    permission = models.TextField(_('Permission'), null=True, blank=True)

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = _('Role')


@python_2_unicode_compatible
class StaffRole(DateTimeModel):
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE)
    role = models.ForeignKey('Role', on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % (self.staff.phone)

    class Meta:
        verbose_name = _('Staff Role')
        unique_together = ("staff", "role")
