# -*- coding: utf-8 -*-
from rest_framework import serializers
from core.models import *
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class DisplayLevelSerializer(serializers.ModelSerializer):
    count_book = serializers.SerializerMethodField()
    
    class Meta:
        model = Level
        fields = '__all__'

    # Count published book in level
    def get_count_book(self, obj):
        return Book.objects.filter( level = obj, status = 'published' ).count()
    

class LevelSerializer(serializers.ModelSerializer):
    sequence_number = serializers.IntegerField( read_only = True )

    class Meta:
        model = Level
        fields = '__all__'

    # Prevent unactive level which has published books
    def validate_is_active(self, value):
        # Check when update and is_active is false
        if self.instance and (value == False):
            has_published_book = Book.objects.filter( level = self.instance, status = 'published' ).count()
            if has_published_book:
                raise serializers.ValidationError(_("Can not unactive level."))
        return value


class DisplayBookCategorySerializer(serializers.ModelSerializer):
    count_book = serializers.SerializerMethodField()
    
    class Meta:
        model = BookCategory
        fields = '__all__'

    # Count published book in category
    def get_count_book(self, obj):
        return Book.objects.filter( category = obj, status = 'published' ).count()

    # Set serializer for nested childrens
    def get_fields(self):
        fields = super(DisplayBookCategorySerializer, self).get_fields()
        fields['children'] = DisplayBookCategorySerializer(many=True)
        return fields

class BookCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = BookCategory
        fields = '__all__'

    # Prevent unactive category which has published books
    def validate_is_draft(self, value):
        # Check when update and is_draft is false
        if self.instance and (value == True):
            has_published_book = Book.objects.filter( category = self.instance, status = 'published' ).count()
            if has_published_book:
                raise serializers.ValidationError(_("Can not unactive category."))
        return value


        