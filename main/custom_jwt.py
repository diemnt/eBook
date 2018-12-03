from calendar import timegm
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import exceptions
from django.utils.translation import ugettext_lazy as _
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model
from kid.models import Kid

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class CustomJSONWebTokenAuthentication(JSONWebTokenAuthentication):

    def authenticate_credentials(self, payload):
        """
            While changing password: when the user changes his password, 
            note the change password time in the user db, so when the change password time is greater than the token creation time, 
            then token is not valid. Hence the remaining session will get logged out soon.
        """
        try:
            User = get_user_model()
            username = jwt_get_username_from_payload(payload)
            print "payload ",payload
            if not username:
                msg = _('Invalid payload.')
                raise exceptions.AuthenticationFailed(msg)

            try:
                user = User.objects.get_by_natural_key(username)
            except User.DoesNotExist:
                user = Kid.objects.get(pk=payload.get('user_id'))

                # msg = _('Invalid signature.')
                # raise exceptions.AuthenticationFailed(msg)

            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.AuthenticationFailed(msg)

            # return user
            # user = super(CustomJSONWebTokenAuthentication,
            #              self).authenticate_credentials(payload)
            print "#### authenticate_credentials ",user
        except Exception, e:
            print "JWT11 authenticate_credentials ", e
            raise exceptions.AuthenticationFailed(_('Invalid token.'))
        return user
