import json
from collections import Counter
from decimal import Decimal
from itertools import accumulate

from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.db import transaction, connection
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_datetime, parse_date, parse_time
from django.utils.timezone import make_aware
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound

from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny

from .models import CsvFile, Author, UserCsvFile, Submission, Review
from .utils import parseCSVFileFromDjangoFile, isNumber, returnTestChartData, parseCSVFile, sha256sum, try_int, \
    parseSubmissionTime, linspace, pairwise
from .getInsight import parseAuthorCSVFile, getReviewScoreInfo, getAuthorInfo, getReviewInfo, getSubmissionInfo


@api_view(['POST'])
def get_analyzed_data(request):
    user_file_ids = (userCsvFile.csv_file_id for userCsvFile in UserCsvFile.objects.filter(user_id=request.user.id))

    author_csv_file_id = None
    submission_csv_file_id = None
    review_csv_file_id = None
    # Each user can have more than one of the same type of the file (which allows us to support further extensions).
    # Right now we just iterate through all the files and take the newest file with the same type.
    for csvFile in CsvFile.objects.filter(id__in=user_file_ids):
        if csvFile.file_type == CsvFile.AUTHOR_FILE_TYPE:
            author_csv_file_id = csvFile.id
        elif csvFile.file_type == CsvFile.SUBMISSION_FILE_TYPE:
            submission_csv_file_id = csvFile.id
        elif csvFile.file_type == CsvFile.REVIEW_FILE_TYPE:
            review_csv_file_id = csvFile.id

    result = []
    if author_csv_file_id:
        top_authors, top_countries, top_affiliations = analyze_author_data(author_csv_file_id)

        parsed_result = {
            'topAuthors': {'labels': [ele[0] for ele in top_authors],
                           'data': [ele[1] for ele in top_authors]},
            'topCountries': {'labels': [ele[0] for ele in top_countries],
                             'data': [ele[1] for ele in top_countries]},
            'topAffiliations': {'labels': [ele[0] for ele in top_affiliations],
                                'data': [ele[1] for ele in top_affiliations]}
        }
        if submission_csv_file_id:
            top_accepted_affiliations = analyze_author_submission_data(author_csv_file_id, submission_csv_file_id)
            parsed_result['topAcceptedAffiliations'] = {'labels': [ele[0] for ele in top_accepted_affiliations],
                                                        'data': [ele[1] for ele in top_accepted_affiliations]}
        if review_csv_file_id:
            top_reviewed_authors = analyze_author_review_data(author_csv_file_id, review_csv_file_id)
            parsed_result['topReviewedAuthors'] = {'labels': [ele[0] for ele in top_reviewed_authors],
                                                   'data': [ele[1] for ele in top_reviewed_authors]}
        result.append({'infoType': 'author', 'infoData': parsed_result})
    if submission_csv_file_id:
        analyzed_data = analyze_submission_data(submission_csv_file_id)

        parsed_result = {
            'acceptanceRate': analyzed_data['acceptance_rate'],
            'timeSeries': analyzed_data['time_series'],
            'lastEditSeries': analyzed_data['last_edit_series'],
            'overallKeywordMap': analyzed_data['overall_keywords_map'],
            'overallKeywordList': analyzed_data['overall_keywords_list'],
            'acceptedKeywordMap': analyzed_data['accepted_keywords_map'],
            'acceptedKeywordList': analyzed_data['accepted_keywords_list'],
            'rejectedKeywordMap': analyzed_data['rejected_keywords_map'],
            'rejectedKeywordList': analyzed_data['rejected_keywords_list'],
            'keywordsByTrack': analyzed_data['keywords_group_by_track'],
            'acceptanceRateByTrack': analyzed_data['acceptance_rate_by_track'],
            'topAcceptedAuthors': analyzed_data['top_accepted_authors_map'],
            'topAuthorsByTrack': analyzed_data['top_authors_by_track'],
            'comparableAcceptanceRate': analyzed_data['comparable_acceptance_rate'],
        }
        result.append({'infoType': 'submission', 'infoData': parsed_result})

    if review_csv_file_id:
        analyzed_data = analyze_review_data(review_csv_file_id)

        parsed_result = {
            'IDReviewMap': analyzed_data['id_review_map'],
            'scoreList': analyzed_data['score_list'],
            'meanScore': analyzed_data['mean_score'],
            'meanRecommend': analyzed_data['mean_recommend'],
            'meanConfidence': analyzed_data['mean_confidence'],
            'recommendList': analyzed_data['recommend_list'],
            'scoreDistribution': analyzed_data['score_distribution'],
            'recommendDistribution': analyzed_data['recommend_distribution'],
        }
        result.append({'infoType': 'review', 'infoData': parsed_result})

    return JsonResponse({'data': result})


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

    # TODO: remove after adding submission and review
    rowCSV = parseCSVFile(csvFile)

    previewData = []
    for row in rowCSV[:5]:
        rowData = {}
        for idx,col in enumerate(row):
            cell = str(col)
            rowData[idx] = (cell[:12] + '...') if len(cell) > 12 else cell

        previewData.append(rowData)

    # TODO: remove data after adding submission and review
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


@api_view(['POST'])
@permission_classes((AllowAny, ))
def get_submission_info(request):
    """
    submission.csv
    data format:
    submission ID | track ID | track name | title | authors | submit time | last update time | form fields | keywords | decision | notified | reviews sent | abstract
    File has header
    """
    if not request.body:
        print('Unable to find submission data!')
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
        submission_data = [ele for ele in parseCSVFile(csv_file)[1:] if ele]

        csv_file_id = save_submissions(submission_data, data, file_hash, user)
    elif num_csv_file_with_hash == 1:
        csv_file_id = csv_file_query_set[0].id
        if user:
            UserCsvFile.objects.get_or_create(user_id=user.id, csv_file_id=csv_file_id)
    else:
        raise APIException('Duplicate files found in database when impossible')

    analyzed_data = analyze_submission_data(csv_file_id)

    parsed_result = {
        'acceptanceRate': analyzed_data['acceptance_rate'],
        'timeSeries': analyzed_data['time_series'],
        'lastEditSeries': analyzed_data['last_edit_series'],
        'overallKeywordMap': analyzed_data['overall_keywords_map'],
        'overallKeywordList': analyzed_data['overall_keywords_list'],
        'acceptedKeywordMap': analyzed_data['accepted_keywords_map'],
        'acceptedKeywordList': analyzed_data['accepted_keywords_list'],
        'rejectedKeywordMap': analyzed_data['rejected_keywords_map'],
        'rejectedKeywordList': analyzed_data['rejected_keywords_list'],
        'keywordsByTrack': analyzed_data['keywords_group_by_track'],
        'acceptanceRateByTrack': analyzed_data['acceptance_rate_by_track'],
        'topAcceptedAuthors': analyzed_data['top_accepted_authors_map'],
        'topAuthorsByTrack': analyzed_data['top_authors_by_track'],
        'comparableAcceptanceRate': analyzed_data['comparable_acceptance_rate'],
    }

    return JsonResponse({'infoType': 'submission', 'infoData': parsed_result})


def save_submissions(submission_data, data, file_hash, user):
    with transaction.atomic():
        decision_index = data['decisionIndex']
        submission_time_index = data['submissionTimeIndex']
        last_edit_time_index = data['lastEditTimeIndex']
        track_name_index = data['trackNameIndex']
        keyword_index = data['keywordIndex']
        author_index = data['authorIndex']

        csv_file_model = CsvFile(file_type=CsvFile.SUBMISSION_FILE_TYPE, file_hash=file_hash)
        csv_file_model.save()
        csv_file_id = csv_file_model.id

        submissions = (Submission(
            submission_id=int(submission[0]),
            track_no=int(submission[1]),
            track_name=submission[track_name_index],
            title=submission[3],
            authors=submission[author_index],
            submitted=make_aware(parse_datetime(submission[submission_time_index])),
            last_updated=make_aware(parse_datetime(submission[last_edit_time_index])),
            form_fields=submission[7],
            keywords=submission[keyword_index],
            decision=submission[decision_index],
            notified=True if submission[10] == 'yes' else False,
            reviews_sent=True if submission[11] == 'yes' else False,
            abstract=submission[12],
            user_file_id=csv_file_id
        ) for submission in submission_data)
        # TODO: divide into slices
        csv_file_model.submission_set.bulk_create(submissions)

        if user:
            user_csv_file_model = UserCsvFile(user_id=user.id, csv_file_id=csv_file_id)
            user_csv_file_model.save()
    return csv_file_id


def analyze_submission_data(csv_file_id):
    submissions = Submission.objects.filter(user_file_id=csv_file_id)
    accepted_submissions = submissions.filter(decision=Submission.ACCEPT_DECISION)
    rejected_submissions = submissions.filter(decision=Submission.REJECT_DECISION)

    acceptance_rate = accepted_submissions.count() / submissions.count()

    submitted_times = ({'x': submission['date'].strftime('%Y-%m-%d'), 'y': submission['count']}
                       for submission in submissions
                       .annotate(date=TruncDate('submitted'))
                       .values('date')
                       .annotate(count=Count('id'))
                       .values('date', 'count')
                       .order_by('date')
                       )
    submitted_time_series = accumulate(submitted_times,
                                       lambda prev, current: {'x': current['x'], 'y': current['y'] + prev['y']})

    last_edit_times = ({'x': submission['date'].strftime('%Y-%m-%d'), 'y': submission['count']}
                       for submission in submissions
                       .annotate(date=TruncDate('last_updated'))
                       .values('date')
                       .annotate(count=Count('id'))
                       .values('date', 'count')
                       .order_by('date')
                       )
    last_edit_time_series = accumulate(last_edit_times,
                                       lambda prev, current: {'x': current['x'], 'y': current['y'] + prev['y']})

    accepted_keywords_per_submission = (submission.keywords.lower().splitlines() for submission in accepted_submissions)
    accepted_keywords = [keyword for keywords in accepted_keywords_per_submission for keyword in keywords]
    accepted_keywords_map = {key: value for key, value in Counter(accepted_keywords).items()}
    accepted_keywords_list = [[key, value] for key, value in Counter(accepted_keywords).most_common(20)]

    rejected_keywords_per_submission = (submission.keywords.lower().splitlines() for submission in rejected_submissions)
    rejected_keywords = [keyword for keywords in rejected_keywords_per_submission for keyword in keywords]
    rejected_keywords_map = {key: value for key, value in Counter(rejected_keywords).items()}
    rejected_keywords_list = [[key, value] for key, value in Counter(rejected_keywords).most_common(20)]

    all_keywords_per_submission = (submission.keywords.lower().splitlines() for submission in submissions)
    all_keywords = [keyword for keywords in all_keywords_per_submission for keyword in keywords]
    all_keywords_map = {key: value for key, value in Counter(all_keywords).items()}
    all_keywords_list = [[key, value] for key, value in Counter(all_keywords).most_common(20)]

    tracks = [submission.track_name for submission in submissions.distinct('track_name')]
    submissions_grouped_by_track = {track: submissions.filter(track_name=track) for track in tracks}

    keywords_group_by_track = {}
    acceptance_rate_by_track = {}
    comparable_acceptance_rate = {}
    top_authors_by_track = {}

    # Obtained from the JCDL.org website: past conferences
    comparable_acceptance_rate['year'] = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
    comparable_acceptance_rate['Full Papers'] = [0.29, 0.28, 0.27, 0.29, 0.29, 0.30, 0.29, 0.30]
    comparable_acceptance_rate['Short Papers'] = [0.29, 0.37, 0.31, 0.31, 0.32, 0.50, 0.35, 0.32]

    for track, track_submissions in submissions_grouped_by_track.items():
        track_keywords_per_submission = (submission.keywords.lower().splitlines() for submission in track_submissions)
        track_keywords = [keyword for keywords in track_keywords_per_submission for keyword in keywords]
        # track_keywords_map = {key: value for key, value in Counter(track_keywords).items()}
        track_keywords_list = [[key, value] for key, value in Counter(track_keywords).most_common(20)]
        keywords_group_by_track[track] = track_keywords_list

        accepted_papers_per_track = track_submissions.filter(decision=Submission.ACCEPT_DECISION)
        acceptance_rate_by_track[track] = accepted_papers_per_track.count() / track_submissions.count()

        track_accepted_authors_per_submission = [submission.authors.replace(' and ', ', ').split(', ') for submission in
                                           accepted_papers_per_track]
        track_accepted_authors = [author for authors in track_accepted_authors_per_submission for author in authors]
        track_top_accepted_authors = Counter(track_accepted_authors).most_common(10)
        top_authors_by_track[track] = {'names': [ele[0] for ele in track_top_accepted_authors],
                                       'counts': [ele[1] for ele in track_top_accepted_authors]}

        if track == "Full Papers" or track == "Short Papers":
            comparable_acceptance_rate[track].append(accepted_papers_per_track.count() / track_submissions.count())

    accepted_authors_per_submission = [submission.authors.replace(' and ', ', ').split(', ') for submission in
                                       accepted_submissions]
    accepted_authors = [author for authors in accepted_authors_per_submission for author in authors]
    top_accepted_authors = Counter(accepted_authors).most_common(10)
    top_accepted_authors_map = {'names': [ele[0] for ele in top_accepted_authors],
                                'counts': [ele[1] for ele in top_accepted_authors]}

    return {
        'acceptance_rate': acceptance_rate,
        'time_series': list(submitted_time_series),
        'last_edit_series': list(last_edit_time_series),
        'overall_keywords_map': all_keywords_map,
        'overall_keywords_list': all_keywords_list,
        'accepted_keywords_map': accepted_keywords_map,
        'accepted_keywords_list': accepted_keywords_list,
        'rejected_keywords_map': rejected_keywords_map,
        'rejected_keywords_list': rejected_keywords_list,
        'keywords_group_by_track': keywords_group_by_track,
        'acceptance_rate_by_track': acceptance_rate_by_track,
        'top_accepted_authors_map': top_accepted_authors_map,
        'top_authors_by_track':  top_authors_by_track,
        'comparable_acceptance_rate': comparable_acceptance_rate,
    }


@api_view(['POST'])
@permission_classes((AllowAny, ))
def get_review_info(request):
    """
    review.csv
    data format:
    review ID | paper ID? | reviewer ID | reviewer name | unknown | text | scores | overall score | unknown | unknown | unknown | unknown | date | time | recommend?
    File has NO header

    score calculation principles:
    Weighted Average of the scores, using reviewer's confidence as the weights

    recommended principles:
    Yes: 1; No: 0; weighted average of the 1 and 0's, also using reviewer's confidence as the weights
    """
    if not request.body:
        print('Unable to find getReviewInfo data!')
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
        review_data = [ele for ele in parseCSVFile(csv_file) if ele]

        csv_file_id = save_reviews(review_data, data, file_hash, user)
    elif num_csv_file_with_hash == 1:
        csv_file_id = csv_file_query_set[0].id
        if user:
            UserCsvFile.objects.get_or_create(user_id=user.id, csv_file_id=csv_file_id)
    else:
        raise APIException('Duplicate files found in database when impossible')

    analyzed_data = analyze_review_data(csv_file_id)

    parsed_result = {
        'IDReviewMap': analyzed_data['id_review_map'],
        'scoreList': analyzed_data['score_list'],
        'meanScore': analyzed_data['mean_score'],
        'meanRecommend': analyzed_data['mean_recommend'],
        'meanConfidence': analyzed_data['mean_confidence'],
        'recommendList': analyzed_data['recommend_list'],
        'scoreDistribution': analyzed_data['score_distribution'],
        'recommendDistribution': analyzed_data['recommend_distribution'],
    }

    return JsonResponse({'infoType': 'review', 'infoData': parsed_result})


def save_reviews(review_data, data, file_hash, user):
    with transaction.atomic():
        submission_id_index = data['submissionIDIndex']
        evaluation_index = data['evaluationIndex']

        csv_file_model = CsvFile(file_type=CsvFile.REVIEW_FILE_TYPE, file_hash=file_hash)
        csv_file_model.save()
        csv_file_id = csv_file_model.id

        reviews = (Review(
            review_no=int(review[0]),
            submission_id=int(review[submission_id_index]),
            review_assignment_no=int(review[2]),
            reviewer_name=review[3],
            field_no=int(review[4]),
            review_comments=review[5],
            overall_evaluation_score_formatted=review[evaluation_index],
            overall_evaluation_score=int(review[7]),
            subreviewer_info_col_one=review[8],
            subreviewer_info_col_two=review[9],
            subreviewer_info_col_three=review[10],
            subreviewer_info_col_four=review[11],
            submission_date=parse_date(review[12]),
            submission_time=parse_time(review[13]),
            recommendation_for_best_paper=True if review[14] == 'yes' else False,
            user_file_id=csv_file_id
        ) for review in review_data)
        # TODO: divide into slices
        csv_file_model.review_set.bulk_create(reviews)

        if user:
            user_csv_file_model = UserCsvFile(user_id=user.id, csv_file_id=csv_file_id)
            user_csv_file_model.save()
    return csv_file_id


def analyze_review_data(csv_file_id):
    reviews = Review.objects.filter(user_file_id=csv_file_id)

    submission_ids = (review.submission_id for review in reviews.distinct('submission_id').order_by('submission_id'))

    score_list = []
    recommend_list = []
    confidence_list = []

    submission_id_review_map = {}

    # Idea: from -3 to 3 (min to max scores possible), every 0.25 will be a gap
    num_scores_in_distribution = int(Decimal(3 + 3) / Decimal('0.25')) + 1
    num_recommend_in_distribution = int(Decimal(1 - 0) / Decimal('0.1')) + 1

    scores_spaced = linspace(-3, 3, num_scores_in_distribution)
    recommend_spaced = linspace(0, 1, num_recommend_in_distribution)

    # Minus 1 because each score/recommend is paired
    score_distribution_counts = [0] * (num_scores_in_distribution - 1)
    recommend_distribution_counts = [0] * (num_recommend_in_distribution - 1)

    score_distribution_labels = [str(x) + " ~ " + str(y) for x, y in pairwise(scores_spaced)]
    recommend_distribution_labels = [str(x) + " ~ " + str(y) for x, y in pairwise(recommend_spaced)]

    def is_recommended(overall_evaluation_score_formatted):
        evaluation_score_info = overall_evaluation_score_formatted.splitlines()
        if len(evaluation_score_info) < 3:
            print(overall_evaluation_score_formatted)
        else:
            return evaluation_score_info[2].split(': ')[1] == 'yes'

    for submission_id in submission_ids:
        reviews_scores_per_submission = [review.overall_evaluation_score_formatted for review in
                                         reviews.filter(submission_id=submission_id)]
        confidences = [float(review.splitlines()[1].split(": ")[1]) for review in reviews_scores_per_submission]
        scores = [float(review.splitlines()[0].split(": ")[1]) for review in reviews_scores_per_submission]

        confidence_list.append(sum(confidences) / len(confidences))
        recommends = [1.0 if is_recommended(overall_evaluation_score_formatted) else 0.0
                      for overall_evaluation_score_formatted in reviews_scores_per_submission]
        weighted_score = sum(x * y for x, y in list(zip(scores, confidences))) / sum(confidences)
        weighted_recommend = sum(x * y for x, y in list(zip(recommends, confidences))) / sum(confidences)

        score_indexumn = min(int((weighted_score + 3) / 0.25), 23)
        recommend_indexumn = min(int(weighted_recommend / 0.1), 9)
        score_distribution_counts[score_indexumn] += 1
        recommend_distribution_counts[recommend_indexumn] += 1
        submission_id_review_map[submission_id] = {'score': weighted_score, 'recommend': weighted_recommend}
        score_list.append(weighted_score)
        recommend_list.append(weighted_recommend)

    return {
        'id_review_map': submission_id_review_map,
        'score_list': score_list,
        'mean_score': sum(score_list) / len(score_list),
        'mean_recommend': sum(recommend_list) / len(recommend_list),
        'mean_confidence': sum(confidence_list) / len(confidence_list),
        'recommend_list': recommend_list,
        'score_distribution': {'labels': score_distribution_labels, 'counts': score_distribution_counts},
        'recommend_distribution': {'labels': recommend_distribution_labels,
                                   'counts': recommend_distribution_counts}
    }


def analyze_author_submission_data(author_csv_file_id, submission_csv_file_id):
    with connection.cursor() as cursor:
        # SELECT organization, count(DISTINCT submission_Id) if we want to count only a single author per submission
        cursor.execute('''SELECT organization, count(organization)
                          FROM dataanalysis_author
                          INNER JOIN dataanalysis_submission
                                   ON dataanalysis_author.submission_id=dataanalysis_submission.submission_id AND
                                      dataanalysis_author.user_file_id=%s AND dataanalysis_submission.user_file_id=%s
                          WHERE decision='accept'
                          GROUP by organization
                          ORDER by count DESC
                          LIMIT 10''', [author_csv_file_id, submission_csv_file_id])
        top_accepted_affiliations = cursor.fetchall()

    return top_accepted_affiliations


def analyze_author_review_data(author_csv_file_id, review_csv_file_id):
    with connection.cursor() as cursor:
        cursor.execute('''SELECT CONCAT(first_name, ' ', last_name), COUNT(*)
                          FROM dataanalysis_author
                          INNER JOIN dataanalysis_review
                                   ON dataanalysis_author.submission_id=dataanalysis_review.submission_id AND
                                      dataanalysis_author.user_file_id=%s AND dataanalysis_review.user_file_id=%s
                          GROUP by first_name, last_name
                          ORDER BY count DESC
                          LIMIT 10''', [author_csv_file_id, review_csv_file_id])
        top_reviewed_authors = cursor.fetchall()

    return top_reviewed_authors


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class ResourceConflict(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Resource conflict.'
    default_code = 'resource_conflict'
