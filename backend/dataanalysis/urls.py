from django.urls import path, include, re_path
from rest_framework_jwt.views import obtain_jwt_token

from .rest_framework_jwt_patched.views import refresh_jwt_token
from . import views, getInsight

urlpatterns = [
    path('api/register/', views.register),
    path('api/login/default/jwt/', obtain_jwt_token),
    path('api/login/', include('rest_social_auth.urls_jwt')),
    path('api/token-refresh/', refresh_jwt_token),

    path('upload/', views.uploadCSV, name='upload'),

    path('parse/', views.parseCSV, name='parse'),

    path('getAuthorInfo/', views.get_author_info, name='getAuthorInfo'),
    path('getReviewInfo/', getInsight.getReviewInfo, name='getReviewInfo'),
    path('getSubmissionInfo/', getInsight.getSubmissionInfo, name='getSubmissionInfo'),

    path('api/get_analyzed_data/', views.get_analyzed_data),

    path('', views.index, name='index'),
    re_path(r'^.*/$', views.index),  # Also redirect all other urls to the SPA
]
