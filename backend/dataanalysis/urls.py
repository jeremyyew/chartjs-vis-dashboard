from django.urls import path, include, re_path
from rest_framework_jwt.views import obtain_jwt_token

from .rest_framework_jwt_patched.views import refresh_jwt_token
from . import views, getInsight

urlpatterns = [
    path('api/register/', views.register),
    path('api/login/default/jwt/', obtain_jwt_token),
    path('api/login/', include('rest_social_auth.urls_jwt')),
    path('api/token-refresh/', refresh_jwt_token),

    # TODO: to be removed
    path('api/checkauth/', views.check_auth),

    path('upload/', views.uploadCSV, name='upload'),

    path('parse/', views.parseCSV, name='parse'),

	path('getAuthorInfo/', getInsight.getAuthorInfo, name='getAuthorInfo'),

    path('', views.index, name='index'),
    re_path(r'^.*/$', views.index),  # Also redirect all other urls to the SPA
]
