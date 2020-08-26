from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path('signup', views.CreateUserView.as_view(), name='signup'),
    path('token', views.CreateTokenView.as_view(), name='token'),
]
