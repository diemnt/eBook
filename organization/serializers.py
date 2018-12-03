from rest_framework import serializers, status
from main.models import User
from organization.models import Package, Organization, OrganizationPackage
from django.db import transaction
import uuid
from payment_gateway.models import OrganizationTransactionTrack

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
                  'kid_limit_default', 'teacher_limit_default', 'effective_time', 'is_trial', 'status')
        read_only_fields = ('status',)


"""
    Author: TienDang (tiendangdht@gmail.com)
    Description: Serializer CRUD for Organization 
"""


class OrganizationSerializer(serializers.ModelSerializer):
    """
    A Organization serializer
    """
    user = UserSerializer(required=False)
    packages = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Package.objects.all(), required=False)

    class Meta:
        model = Organization
        fields = ("id", "user", "full_name", "email", "phone",
                  "address", "city", "tax_code", "kid_limit", "teacher_limit", "packages", "avatar")
        read_only_fields = ("avatar",)


    @transaction.atomic
    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of organization
        :return: returns a successfully created organization record
        """
        # Create User Object
        user_data = validated_data.pop('user')
        if not user_data:
            raise serializers.ValidationError(
                {"user": _("User must be is required.")})

        user = UserSerializer.create(
            UserSerializer(), validated_data=user_data)
        # Create Organization with relation one to one User
        organization, created = Organization.objects.update_or_create(
            user=user, **validated_data)

        # Check list packages ids not empty then add packages for organization

        if 'packages' in validated_data:
            lst_packages = validated_data.pop('packages')
            order_id = uuid.uuid4()
            organization_packages = []
            tranasction_history = []
            # Add packages for Organization and store transaction 
            for package in lst_packages:
                organization_packages.append(OrganizationPackage(organization=organization, package=package, order_id=order_id))
                tranasction_history.append(OrganizationTransactionTrack(organization=organization, package=package, order_id=order_id, amount=package.price, status='done'))

            OrganizationPackage.objects.bulk_create(organization_packages)
            OrganizationTransactionTrack.objects.bulk_create(tranasction_history)

        return organization


    @transaction.atomic
    def update(self, instance, validated_data):
        # Update User Object
        validated_data.pop('packages', None)
        user_data = validated_data.pop('user', None)
        if user_data:
            user = UserSerializer.update(
                UserSerializer(), instance.user, user_data)

        return super(StaffSerializer, self).update(instance, validated_data)


"""
    Author: TienDang (tiendangdht@gmail.com)
    Description: Serializer CRUD for Package of Organization 
"""


class OrganizationPackageSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all())
    package = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Package.objects.all())

    class Meta:
        model = OrganizationPackage
        fields = ('organization', 'package', 'expiry_date')
