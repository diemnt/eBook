# -*- coding: utf-8 -*-
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from kid import authentication
from kid.models import Kid

@api_view(['POST'])
@permission_classes((AllowAny,))
def authenticate_kid(request):
    try:
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        
        try:
            if not username or not password:
                return Response({"code": 500, "message": "Lỗi : tên tài khoản và mật khẩu không được bỏ trống. Vui lòng kiểm tra lại", "fields": ""}, status=400)    
                    
            result = None

            user = Kid.objects.get(username=username)
            if user.check_password(password):
                result = authentication.jwt_token(user)

        except Kid.DoesNotExist:
            result = None
            
        if result is None:
            return Response({"code": 500, "message": "Lỗi : tên tài khoản hoặc mật khẩu không chính xác. Vui lòng kiểm tra lại", "fields": ""}, status=400)    
        
        return Response(result, status=200)
    except Exception,e :
        print "## error ",e
        error = {"code": 500, "message": "ERROR : Internal Server Error .Please contact administrator.", "fields": ""}
        return Response(error, status=500)


@api_view(['GET'])
def check_authenticate(request):
    try:
        return Response({"message": "Process Request Success"}, status=200)
    except Exception,e :
        print "## error ",e
        error = {"code": 500, "message": "ERROR : Internal Server Error .Please contact administrator.", "fields": ""}
        return Response(error, status=500)




