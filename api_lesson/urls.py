from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView


router = routers.DefaultRouter()
router.register('lesson', views.LessonViewSet)

urlpatterns = [
    path('register', views.UserRegisterView().as_view(), name='user-register'),
    path('login', views.LoginView().as_view(), name='login'),
    path('logout', views.LogoutView().as_view(), name='logout'),
    path('user', views.UserView().as_view(), name='user'),
    path('lesson-list/', views.LessonListView().as_view(), name='lesson-list'),
    path('lesson-detail/<str:pk>/', views.LessonRetrieveView().as_view(), name='lesson-detail'),
    path('auth/', include('djoser.urls.jwt')),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
