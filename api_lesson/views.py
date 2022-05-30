from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Lesson, LessonContent
from .serializers import LessonSerializer, LessonContentSerializer
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, reverse, redirect, get_object_or_404, get_list_or_404
from rest_framework.parsers import JSONParser
from rest_framework.decorators import action


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
