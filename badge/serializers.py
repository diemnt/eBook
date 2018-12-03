from rest_framework import serializers
from badge.models import *
from django.utils.translation import ugettext_lazy as _



class BadgeSerializer(serializers.ModelSerializer):
    BADGE_TYPE = (
        ('point'),
        ('time'),
        ('total')
    )
    badge_type = serializers.ChoiceField(required=True, choices = BADGE_TYPE)
    created_by = serializers.CharField(source = 'created_by.user.username', default=None, read_only=True)
    modified_by = serializers.CharField(source = 'modified_by.user.username', default=None, read_only=True)
    is_active = serializers.BooleanField(read_only = True)  # Becuase has api to active
    
    class Meta:
        model = Badge
        fields = '__all__'


