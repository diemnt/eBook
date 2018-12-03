from rest_framework import serializers, status
from main.models import User
from personal.models import Package, Personal, PersonalPackage
from django.db import transaction


"""
    Author: TienDang (tiendangdht@gmail.com)
    Description: Serializer CRUD for User 
"""


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

"""
    Author: TienDang (tiendangdht@gmail.com)
    Description: Serializer Create, Update for Package (exclude field status). Update status using another action

"""


class PackageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Package
        fields = ('id', 'name', 'description', 'price',
                  'kid_limit', 'effective_time', 'is_trial', 'status')
        read_only_fields = ('status',)


"""
    Author: TienDang (tiendangdht@gmail.com)
    Description: Serializer CRUD for Personal 
"""


class PersonalSerializer(serializers.ModelSerializer):
    """
    A personal serializer to return the personal details
    """
    user = UserSerializer(required=False)

    class Meta:
        model = Personal
        fields = ("id", "user", "full_name", "email", "gender", "phone",
                  "address", "city", "personal_id", "packages", "avatar")
        read_only_fields = ('packages', "avatar",)

    @transaction.atomic
    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of personal
        :return: returns a successfully created personal record
        """
        # Create User Object
        user_data = validated_data.pop('user', None)
        if not user_data:
            raise serializers.ValidationError(
                {"user": _("User must be is required.")})

        user = UserSerializer.create(
            UserSerializer(), validated_data=user_data)
        # Create Personal with relation one to one User
        personal, created = Personal.objects.update_or_create(
            user=user, **validated_data)

        return personal

    @transaction.atomic
    def update(self, instance, validated_data):

        # Update User Object
        user_data = validated_data.pop('user', None)
        if user_data:
            user = UserSerializer.update(
                UserSerializer(), instance.user, user_data)

        return super(PersonalSerializer, self).update(instance, validated_data)

"""
    Author: TienDang (tiendangdht@gmail.com)
    Description: Serializer CRUD for Package of Personal 
"""


class PersonalPackageSerializer(serializers.ModelSerializer):
    personal = serializers.PrimaryKeyRelatedField(
        queryset=Personal.objects.all())
    packages = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Package.objects.all())

    class Meta:
        model = PersonalPackage
        fields = ('personal', 'packages', 'expiry_date')
