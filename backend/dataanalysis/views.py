import json
from collections import Counter

from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.db import transaction, connection
from django.db.models import Count
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound

from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny

from .models import CsvFile, Author, UserCsvFile
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
def get_author_info(request):
    """
    author.csv: header row, author names with affiliations, countries, emails
    data format:
    submission ID | f name | s name | email | country | affiliation | page | person ID | corresponding?
    """

    if not request.body:
        print('Unable to find author data!')
        return HttpResponseNotFound('Page not found for CSV')

    data = json.loads(request.body)

    session_id = data['sessionId']
    session = SessionStore(session_key=session_id)

    csv_file = session['file']

    file_hash = sha256sum(csv_file)
    csv_file.seek(0)

    csv_file_query_set = CsvFile.objects.filter(file_hash=file_hash)
    num_csv_file_with_hash = csv_file_query_set.count()

    user = request.user if request.user.is_authenticated else None
    if num_csv_file_with_hash == 0:
        author_data = [ele for ele in parseCSVFile(csv_file)[1:] if ele]

        csv_file_id = save_authors(author_data, data, file_hash, user)
    elif num_csv_file_with_hash == 1:
        csv_file_id = csv_file_query_set[0].id
        if user:
            UserCsvFile.objects.get_or_create(user_id=user.id, csv_file_id=csv_file_id)
    else:
        raise APIException('Duplicate files found in database when impossible')

    top_authors, top_countries, top_affiliations = analyze_author_data(csv_file_id)

    parsed_result = {
        'topAuthors': {'labels': [ele[0] for ele in top_authors],
                       'data': [ele[1] for ele in top_authors]},
        'topCountries': {'labels': [ele[0] for ele in top_countries],
                         'data': [ele[1] for ele in top_countries]},
        'topAffiliations': {'labels': [ele[0] for ele in top_affiliations],
                            'data': [ele[1] for ele in top_affiliations]}
    }

    return JsonResponse({'infoType': 'author', 'infoData': parsed_result})


def save_authors(author_data, data, file_hash, user):
    with transaction.atomic():
        first_name_index = data['firstNameIndex']
        last_name_index = data['lastNameIndex']
        country_index = data['countryIndex']
        affiliation_index = data['affiliationIndex']

        csv_file_model = CsvFile(file_type=CsvFile.AUTHOR_FILE_TYPE, file_hash=file_hash)
        csv_file_model.save()
        csv_file_id = csv_file_model.id

        authors = (Author(
            submission_id=int(authorInfo[0]),
            first_name=authorInfo[first_name_index],
            last_name=authorInfo[last_name_index],
            email=authorInfo[3],
            country=authorInfo[country_index],
            organization=authorInfo[affiliation_index],
            web_page=authorInfo[6],
            person_id=try_int(authorInfo[7]),
            is_corresponding=True if authorInfo[8] == 'yes' else False,
            user_file_id=csv_file_id
        ) for authorInfo in author_data)
        # TODO: divide into slices
        csv_file_model.author_set.bulk_create(authors)

        if user:
            user_csv_file_model = UserCsvFile(user_id=user.id, csv_file_id=csv_file_id)
            user_csv_file_model.save()
    return csv_file_id


def analyze_author_data(csv_file_id):
    with connection.cursor() as cursor:
        cursor.execute('''SELECT CONCAT(first_name, ' ', last_name) AS full_name,
                                 COUNT(concat(first_name, ' ', last_name)) AS full_name_count 
                                 FROM dataanalysis_author
                                 WHERE user_file_id = %s
                                 GROUP BY full_name
                                 ORDER BY full_name_count DESC
                                 LIMIT 10''', [csv_file_id])
        top_authors = cursor.fetchall()

    top_countries = [(author['country'], author['country_count'])
                     for author in
                     Author.objects.filter(user_file_id=csv_file_id)
                     .values('country')
                     .annotate(country_count=Count('country'))
                     .order_by('-country_count')[:10]]

    top_affiliations = [(author['organization'], author['organization_count'])
                        for author in
                        Author.objects.filter(user_file_id=csv_file_id)
                        .values('organization')
                        .annotate(organization_count=Count('organization'))
                        .order_by('-organization_count')[:10]]
    return top_authors, top_countries, top_affiliations


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class ResourceConflict(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Resource conflict.'
    default_code = 'resource_conflict'
