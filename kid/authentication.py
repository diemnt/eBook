from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


"""
    author: TienDang
    Description: Generate json web token (jwt) using library rest_framework_jwt
"""
def jwt_token(user):
    try:
        # New Payload from user object
        payload = jwt_payload_handler(user)
        # Generate token using jwt
        token = jwt_encode_handler(payload)

        return {"token":token}
    except Exception,e :
        raise Exception(e)