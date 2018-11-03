from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse, JsonResponse

from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny

from .utils import parseCSVFileFromDjangoFile, isNumber, returnTestChartData
from .getInsight import parseAuthorCSVFile, getReviewScoreInfo, getAuthorInfo, getReviewInfo, getSubmissionInfo


# TODO: to be removed
@api_view(['POST'])
def check_auth(request):
    print(request.user)
    if request.user.is_authenticated:
        return JsonResponse({"status": "true"})
    else:
        return JsonResponse({"status": "false"})


@api_view(['POST'])
@permission_classes((AllowAny, ))
def register(request):
    username = request.data['username']
    email = request.data['email']
    password = request.data['password']

    # TODO: validate in serializers, and validate email and others?
    if User.objects.filter(username=username).exists():
        raise ResourceConflict("Username is already taken")
    try:
        user = User.objects.create_user(username, email, password)
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return JsonResponse(serializer.data)
        # return JsonResponse(serializer.errors, status=400)
    except Exception as e:
        raise APIException(e)


def index(request):
    return render(request, 'dataanalysis/index.html')


# Note: csr: cross site request, adding this to enable request from localhost
@csrf_exempt
def uploadCSV(request):
    print("Inside the upload function")
    if request.FILES:
        csvFile = request.FILES['file']
        fileName = str(csvFile.name)
        rowContent = ""

        if "author.csv" in fileName:
            rowContent = getAuthorInfo(csvFile)
        elif "score.csv" in fileName:
            rowContent = getReviewScoreInfo(csvFile)
        elif "review.csv" in fileName:
            rowContent = getReviewInfo(csvFile)
        elif "submission.csv" in fileName:
            rowContent = getSubmissionInfo(csvFile)
        else:
            rowContent = returnTestChartData(csvFile)

        print(type(csvFile.name))

        if request.POST:
            # current problem: request from axios not recognized as POST
            # csvFile = request.FILES['file']
            print("Now we got the csv file")

        return JsonResponse(rowContent)
    # return HttpResponse("Got the CSV file.")
    else:
        print("Not found the file!")
        return JsonResponse({"status": "Page not found for CSV"})


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class ResourceConflict(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Resource conflict.'
    default_code = 'resource_conflict'
