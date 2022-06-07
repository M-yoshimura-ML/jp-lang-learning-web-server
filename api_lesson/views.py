from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Lesson, LessonContent, User
from .serializers import LessonSerializer, LessonContentSerializer, UserSerializer
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, reverse, redirect, get_object_or_404, get_list_or_404
from rest_framework.parsers import JSONParser
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed, ValidationError
import jwt, datetime
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['isSuperuser'] = user.is_superuser
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserRegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data['email']
        user = User.objects.filter(email=email).first()
        serializer = UserSerializer(data=request.data)
        if user is None:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            raise ValidationError('Email is already registered')

        return Response(serializer.data)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            "jwt": token
        }
        return response


class UserView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        token = request.COOKIES.get('jwt')
        print(token)
        if not token:
            raise AuthenticationFailed('UnAuthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token is expired')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'logout is success'
        }
        return response


class LessonListView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (AllowAny,)


class LessonRetrieveView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (AllowAny,)


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    lookup_field = 'id'

    @action(detail=True, methods=["GET"])
    def contents(self, request, id=None):
        lesson = self.get_object()
        contents = LessonContent.objects.filter(lesson=lesson)
        serializer = LessonContentSerializer(contents, many=True)
        return Response(serializer.data, status=200)

    @action(detail=True, methods=["POST"])
    def content(self, request, id=None):
        lesson = self.get_object()
        data = request.data
        data['lesson'] = lesson.id
        serializer = LessonContentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
