from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import viewsets, mixins, status
from rest_framework.views import APIView
from users.serializers import UserSerializer, AuthTokenSerializer, LoginSerializer, \
    UserInfoSerializer_Safe
from users import models

from users.custom_exception import exception


class Login(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        login_serializer = LoginSerializer(data=request.data)
        login_serializer.is_valid(request.data)
        email = request.data['email']
        password = request.data['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
        elif user is None:
            return JsonResponse(
                {
                    "error": exception("Wrong username or password or you did not confirm your email!", False)
                }
                , status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(
                {
                    "error": exception("Oops! something wrong. please try later...", False)
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        user_info_serializer = UserInfoSerializer_Safe(data=user.__dict__)
        user_info_serializer.is_valid(user.__dict__)
        if user_info_serializer["is_active"] is False:
            return JsonResponse({"error": "your account is not active!"})

        return JsonResponse({'user': user_info_serializer.data, 'token': token.key})


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = {authentication.TokenAuthentication, }
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
