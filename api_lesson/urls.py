from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView


router = routers.DefaultRouter()
router.register('lesson', views.LessonViewSet)

urlpatterns = [
    path('lesson-list/', views.LessonListView().as_view(), name='lesson-list'),
    path('lesson-detail/<str:pk>/', views.LessonRetrieveView().as_view(), name='lesson-detail'),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
]
