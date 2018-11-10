import json
from collections import Counter

from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.db import transaction, connection
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound

from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny

from .models import CsvFile, Author
from .utils import parseCSVFileFromDjangoFile, isNumber, returnTestChartData, parseCSVFile, sha256sum, try_int
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

@csrf_exempt
def parseCSV(request):
    s = SessionStore()
    csvFile = request.FILES['file']
    s['file'] = csvFile
    s.create()

    rowCSV = parseCSVFile(csvFile)

    previewData = []
    for row in rowCSV[:5]:
        rowData = {}
        for idx,col in enumerate(row):
            cell = str(col)
            rowData[idx] = (cell[:12] + '...') if len(cell) > 12 else cell

        previewData.append(rowData)

    return JsonResponse({'data' : rowCSV, 'previewData': previewData, 'sessionId': s.session_key})


@api_view(['POST'])
@permission_classes((AllowAny, ))
def getAuthorInfo(request):
    """
    author.csv: header row, author names with affiliations, countries, emails
    data format:
    submission ID | f name | s name | email | country | affiliation | page | person ID | corresponding?
    """

    if not request.body:
        print('Unable to find author data!')
        return HttpResponseNotFound('Page not found for CSV')

    data = json.loads(request.body)
    sessionId = data['sessionId']
    session = SessionStore(session_key=sessionId)

    csvFile = session['file']

    if request.user.is_authenticated:
        fileHash = sha256sum(csvFile)
        print(fileHash)
        csvFile.seek(0)

        csvFileQuerySet = CsvFile.objects.filter(file_hash=fileHash)
        numCsvFileWithHash = csvFileQuerySet.count()
        if numCsvFileWithHash == 0:
            with transaction.atomic():
                authorData = parseCSVFile(csvFile)[1:]
                authorData = [ele for ele in authorData if ele]
                firstNameIndex = data['firstNameIndex']
                lastNameIndex = data['lastNameIndex']
                countryIndex = data['countryIndex']
                affiliationIndex = data['affiliationIndex']

                csvFileModel = CsvFile(file_type=CsvFile.AUTHOR_FILE_TYPE, file_hash=fileHash)
                csvFileModel.save()

                # Author.objects.bulk_create([])
                authors = (Author(
                    submission_no=int(authorInfo[0]),
                    first_name=authorInfo[firstNameIndex],
                    last_name=authorInfo[lastNameIndex],
                    email=authorInfo[3],
                    country=authorInfo[countryIndex],
                    organization=authorInfo[affiliationIndex], # affiliation?
                    web_page=authorInfo[6],
                    person_id=try_int(authorInfo[7]),
                    user_file_id=csvFileModel.id
                ) for authorInfo in authorData)
                # TODO: divide into slices
                csvFileModel.author_set.bulk_create(authors)

                # do counting
        elif numCsvFileWithHash == 1:
            print(csvFileQuerySet[0].id)
            # TODO: use author_set
            # TODO: where user_file_id=fileHash
            with connection.cursor() as cursor:
                cursor.execute('''SELECT CONCAT(first_name, ' ', last_name) AS full_name,
                                             COUNT(concat(first_name, ' ', last_name)) AS value_occurrence
                                             FROM     dataanalysis_author
                                             WHERE user_file_id = %s
                                             GROUP BY full_name
                                             ORDER BY value_occurrence DESC
                                             LIMIT 10''', [csvFileQuerySet[0].id])
                authorsTest = cursor.fetchall()
            for authors in authorsTest:
                print(authors)
            # do counting
        else:
            raise APIException('Duplicate files found in database when impossible')

    # TODO: if authenticated hash csvFile, if database contains this then skip to calculation immediately

    authorData = parseCSVFile(csvFile)[1:]
    authorData = [ele for ele in authorData if ele]
    # authorData = data['data'][1:]
    # authorData = [ele for ele in authorData if ele]
    firstNameIndex = data['firstNameIndex']
    lastNameIndex = data['lastNameIndex']
    countryIndex = data['countryIndex']
    affiliationIndex = data['affiliationIndex']


    authorList = []
    for authorInfo in authorData:
        authorList.append({'name': authorInfo[firstNameIndex] + " " + authorInfo[lastNameIndex],
                           'country': authorInfo[countryIndex],
                           'affiliation': authorInfo[affiliationIndex]})

    parsedResult = {};

    authors = [ele['name'] for ele in authorList if
               ele]  # adding in the if ele in case of empty strings; same applies below
    topAuthors = Counter(authors).most_common(10)
    parsedResult['topAuthors'] = {'labels': [ele[0] for ele in topAuthors], 'data': [ele[1] for ele in topAuthors]}

    countries = [ele['country'] for ele in authorList if ele]
    topCountries = Counter(countries).most_common(10)
    parsedResult['topCountries'] = {'labels': [ele[0] for ele in topCountries],
                                    'data': [ele[1] for ele in topCountries]}

    affiliations = [ele['affiliation'] for ele in authorList if ele]
    topAffiliations = Counter(affiliations).most_common(10)
    parsedResult['topAffiliations'] = {'labels': [ele[0] for ele in topAffiliations],
                                       'data': [ele[1] for ele in topAffiliations]}

    return JsonResponse({'infoType': 'author', 'infoData': parsedResult})


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class ResourceConflict(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Resource conflict.'
    default_code = 'resource_conflict'
