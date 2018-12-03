from rest_framework import serializers, status
from main.models import User
from staff.models import Staff, Role, StaffRole
from django.db import transaction
from django.utils.translation import ugettext_lazy as _

"""
    Author: TienDang (tiendangdht@gmail.com)
    Description: Serializer CRUD for Role
"""


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'


"""
    Author: TienDang (tiendangdht@gmail.com)
    Description: Serializer CRUD for User
"""


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.is_staff = True
        user.save()
        return user


"""
    Author: TienDang (tiendangdht@gmail.com)
    Description: Serializer CRUD for Staff
"""


class StaffSerializer(serializers.ModelSerializer):
    """
    A staff serializer to return the staff details
    """
    user = UserSerializer(required=False)
    roles = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Role.objects.all())

    class Meta:
        model = Staff
        fields = ("id", "user", "phone", "roles")

    @transaction.atomic
    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of staff
        :return: returns a successfully created staff record
        """
        print "validated_data ", validated_data
        # Create User Object
        user_data = validated_data.pop('user', None)
        if not user_data:
            raise serializers.ValidationError(
                {"user": _("User must be is required.")})

        user = UserSerializer.create(
            UserSerializer(), validated_data=user_data)

        # Create Staff with relation one to one User
        staff, created = Staff.objects.update_or_create(user=user,
                                                        phone=validated_data.pop('phone'))

        # Check list role ids not empty then assign role for staff

        if 'roles' in validated_data:
            lst_roles = validated_data.pop('roles')
            staff_roles = [StaffRole(staff=staff, role=role)
                           for role in lst_roles]
            StaffRole.objects.bulk_create(staff_roles)

        return staff

    @transaction.atomic
    def update(self, instance, validated_data):
        print "update"
        if 'roles' in validated_data:
            lst_roles = validated_data.pop('roles')
            # Remove Old roles of staff
            StaffRole.objects.filter(staff_id=instance.id).delete()
            # Update new roles for staff
            staff_roles = [StaffRole(staff=instance, role=role)
                           for role in lst_roles]
            StaffRole.objects.bulk_create(staff_roles)

        # Update User Object
        user_data = validated_data.pop('user', None)
        if user_data:
            user = UserSerializer.update(
                UserSerializer(), instance.user, user_data)

        return super(StaffSerializer, self).update(instance, validated_data)


"""
    Author: TienDang (tiendangdht@gmail.com)
    Description: Serializer List and Detail for Staff
"""


class DisplayStaffSerializer(serializers.ModelSerializer):
    """
    A Display Staff serializer to return the staff and role details
    """
    user = UserSerializer(required=True)
    roles = RoleSerializer(many=True)

    class Meta:
        model = Staff
        fields = '__all__'


"""
    Example Disable a method in ViewSet
"""
# The definition of ModelViewSet is:

# class ModelViewSet(mixins.CreateModelMixin,
#                    mixins.RetrieveModelMixin,
#                    mixins.UpdateModelMixin,
#                    mixins.DestroyModelMixin,
#                    mixins.ListModelMixin,
#                    GenericViewSet)
# So rather than extending ModelViewSet, why not just use whatever you
# need? So for example:

# from rest_framework import viewsets, mixins

# class SampleViewSet(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     viewsets.GenericViewSet):
#     ...
