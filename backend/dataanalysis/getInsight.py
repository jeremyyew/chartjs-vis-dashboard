import csv
import codecs
import json
from collections import Counter

from django.http import HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .utils import parseCSVFile, testCSVFileFormatMatching, isNumber, parseSubmissionTime

def parseAuthorCSVFile(inputFile):

	csvFile = inputFile
	dialect = csv.Sniffer().sniff(codecs.EncodedFile(csvFile, "utf-8").read(1024))
	csvFile.open()
	# reader = csv.reader(codecs.EncodedFile(csvFile, "utf-8"), delimiter=',', dialect=dialect)
	reader = csv.reader(codecs.EncodedFile(csvFile, "utf-8"), delimiter=',', dialect='excel')

	rowResults = []
	for index, row in enumerate(reader):
		rowResults.append(row)
		print(row)
		print(type(row))
		if index == 5:
			break

	parsedResult = {}

	return parsedResult

@csrf_exempt
def getAuthorInfo(request):
	"""
	author.csv: header row, author names with affiliations, countries, emails
	data format:
	submission ID | f name | s name | email | country | affiliation | page | person ID | corresponding?
	"""
	
	if request.body:
		data = json.loads(request.body)
		authorData = data['authorData'][1:]
		authorData = [ele for ele in authorData if ele]
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

		authors = [ele['name'] for ele in authorList if ele] # adding in the if ele in case of empty strings; same applies below
		topAuthors = Counter(authors).most_common(10)
		parsedResult['topAuthors'] = {'labels': [ele[0] for ele in topAuthors], 'data': [ele[1] for ele in topAuthors]}

		countries = [ele['country'] for ele in authorList if ele]
		topCountries = Counter(countries).most_common(10)
		parsedResult['topCountries'] = {'labels': [ele[0] for ele in topCountries], 'data': [ele[1] for ele in topCountries]}

		affiliations = [ele['affiliation'] for ele in authorList if ele]
		topAffiliations = Counter(affiliations).most_common(10)
		parsedResult['topAffiliations'] = {'labels': [ele[0] for ele in topAffiliations], 'data': [ele[1] for ele in topAffiliations]}

		return JsonResponse({'infoType': 'author', 'infoData': parsedResult})

	else:
		print('Unable to find author data!')
		return HttpResponseNotFound('Page not found for CSV')

def getReviewScoreInfo(inputFile):
	"""
	review_score.csv
	data format:
	review ID | field ID | score
	File has header

	e.g. 1,1,3 - score (can be negative)
	     1,2,5 - confidence
	     1,3,no - recommended
	"""
	parsedResult = {}
	lines = parseCSVFile(inputFile)[1:]
	lines = [ele for ele in lines if ele]
	scores = []
	confidences = []
	isRecommended = []

	scores = [int(line[2]) for line in lines if int(line[1]) == 1]
	confidences = [int(line[2]) for line in lines if int(line[1]) == 2]
	isRecommended = [str(line[2]).replace("\r", "") for line in lines if int(line[1]) == 3]

	parsedResult['yesPercentage'] = float(isRecommended.count('yes')) / len(isRecommended)
	parsedResult['meanScore'] = sum(scores) / float(len(scores))
	parsedResult['meanConfidence'] = sum(confidences) / float(len(confidences))
	parsedResult['totalReview'] = len(confidences)

	return {'infoType': 'reviewScore', 'infoData': parsedResult}


@csrf_exempt
def getReviewInfo(request):
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

	if request.body:
		data = json.loads(request.body)
		reviewData = data['reviewData']
		reviewData = [ele for ele in reviewData if ele]
		submissionIDIndex = data['submissionIDIndex']
		evaluationIndex = data['evaluationIndex']

		parsedResult = {};
		submissionIDs = set([str(line[1]) for line in reviewData])

		scoreList = []
		recommendList = []
		confidenceList = []

		submissionIDReviewMap = {}

		# Idea: from -3 to 3 (min to max scores possible), every 0.25 will be a gap
		scoreDistributionCounts = [0] * int((3 + 3) / 0.25)
		recommendDistributionCounts = [0] * int((1 - 0) / 0.1)

		scoreDistributionLabels = [" ~ "] * len(scoreDistributionCounts)
		recommendDistributionLabels = [" ~ "] * len(recommendDistributionCounts)

		for index, col in enumerate(scoreDistributionCounts):
			scoreDistributionLabels[index] = str(-3 + 0.25 * index) + " ~ " + str(-3 + 0.25 * index + 0.25)

		for index, col in enumerate(recommendDistributionCounts):
			recommendDistributionLabels[index] = str(0 + 0.1 * index) + " ~ " + str(0 + 0.1 * index + 0.1)

		for submissionID in submissionIDs:
			reviews = [str(line[evaluationIndex]).replace("\r", "") for line in reviewData if str(line[submissionIDIndex]) == submissionID]
			# print reviews
			confidences = [float(review.split("\n")[1].split(": ")[1]) for review in reviews]
			scores = [float(review.split("\n")[0].split(": ")[1]) for review in reviews]

			confidenceList.append(sum(confidences) / len(confidences))
			try:
				recommends = [1.0 if review.split("\n")[2].split(": ")[1] == "yes" else 0.0 for review in reviews]
			except:
				recommends = [0.0 for n in range(len(reviews))]
			weightedScore = sum(x * y for x, y in list(zip(scores, confidences))) / sum(confidences)
			weightedRecommend = sum(x * y for x, y in list(zip(recommends, confidences))) / sum(confidences)

			scoreIndexumn = min(int((weightedScore + 3) / 0.25), 23)
			recommendIndexumn = min(int((weightedRecommend) / 0.1), 9)
			scoreDistributionCounts[scoreIndexumn] += 1
			recommendDistributionCounts[recommendIndexumn] += 1
			submissionIDReviewMap[submissionID] = {'score': weightedScore, 'recommend': weightedRecommend}
			scoreList.append(weightedScore)
			recommendList.append(weightedRecommend)


		parsedResult['IDReviewMap'] = submissionIDReviewMap
		parsedResult['scoreList'] = scoreList
		parsedResult['meanScore'] = sum(scoreList) / len(scoreList)
		parsedResult['meanRecommend'] = sum(recommendList) / len(recommendList)
		parsedResult['meanConfidence'] = sum(confidenceList) / len(confidenceList)
		parsedResult['recommendList'] = recommendList
		parsedResult['scoreDistribution'] = {'labels': scoreDistributionLabels, 'counts': scoreDistributionCounts}
		parsedResult['recommendDistribution'] = {'labels': recommendDistributionLabels, 'counts': recommendDistributionCounts}

		return JsonResponse({'infoType': 'review', 'infoData': parsedResult})

	else:
		print('Unable to find getReviewInfo data!')
		return HttpResponseNotFound('Page not found for CSV')

@csrf_exempt
def getSubmissionInfo(request):
	"""
	submission.csv
	data format: 
	submission ID | track ID | track name | title | authors | submit time | last update time | form fields | keywords | decision | notified | reviews sent | abstract
	File has header
	"""
	if request.body:
		data = json.loads(request.body)
		submissionData = data['submissionData'][1:]
		submissionData = [ele for ele in submissionData if ele]
		acceptanceIndex = data['acceptanceIndex']
		submissionTimeIndex = data['submissionTimeIndex']
		lastEditTimeIndex = data['lastEditTimeIndex']
		trackIndex = data['trackIndex']
		keywordIndex = data['keywordIndex']
		authorIndex = data['authorIndex']

		parsedResult = {}
		acceptedSubmission = [line for line in submissionData if str(line[acceptanceIndex]) == 'accept']
		rejectedSubmission = [line for line in submissionData if str(line[acceptanceIndex]) == 'reject']

		acceptanceRate = float(len(acceptedSubmission)) / len(submissionData)

		submissionTimes = [parseSubmissionTime(str(ele[submissionTimeIndex])) for ele in submissionData]
		lastEditTimes = [parseSubmissionTime(str(ele[lastEditTimeIndex])) for ele in submissionData]
		submissionTimes = Counter(submissionTimes)
		lastEditTimes = Counter(lastEditTimes)
		timeStamps = sorted([k for k in submissionTimes])
		lastEditStamps = sorted([k for k in lastEditTimes])
		submittedNumber = [0 for n in range(len(timeStamps))]
		lastEditNumber = [0 for n in range(len(lastEditStamps))]
		timeSeries = []
		lastEditSeries = []
		for index, timeStamp in enumerate(timeStamps):
			if index == 0:
				submittedNumber[index] = submissionTimes[timeStamp]
			else:
				submittedNumber[index] = submissionTimes[timeStamp] + submittedNumber[index - 1]

			timeSeries.append({'x': timeStamp, 'y': submittedNumber[index]})

		for index, lastEditStamp in enumerate(lastEditStamps):
			if index == 0:
				lastEditNumber[index] = lastEditTimes[lastEditStamp]
			else:
				lastEditNumber[index] = lastEditTimes[lastEditStamp] + lastEditNumber[index - 1]

			lastEditSeries.append({'x': lastEditStamp, 'y': lastEditNumber[index]})

		# timeSeries = {'time': timeStamps, 'number': submittedNumber}
		# lastEditSeries = {'time': lastEditStamps, 'number': lastEditNumber}

		acceptedKeywords = [str(ele[keywordIndex]).lower().replace("\r", "").split("\n") for ele in acceptedSubmission]
		acceptedKeywords = [ele for item in acceptedKeywords for ele in item]
		acceptedKeywordMap = {k : v for k, v in iter(Counter(acceptedKeywords).items())}
		acceptedKeywordList = [[ele[0], ele[1]] for ele in Counter(acceptedKeywords).most_common(20)]

		rejectedKeywords = [str(ele[keywordIndex]).lower().replace("\r", "").split("\n") for ele in rejectedSubmission]
		rejectedKeywords = [ele for item in rejectedKeywords for ele in item]
		rejectedKeywordMap = {k : v for k, v in iter(Counter(rejectedKeywords).items())}
		rejectedKeywordList = [[ele[0], ele[1]] for ele in Counter(rejectedKeywords).most_common(20)]

		allKeywords = [str(ele[keywordIndex]).lower().replace("\r", "").split("\n") for ele in submissionData]
		allKeywords = [ele for item in allKeywords for ele in item]
		allKeywordMap = {k : v for k, v in iter(Counter(allKeywords).items())}
		allKeywordList = [[ele[0], ele[1]] for ele in Counter(allKeywords).most_common(20)]

		tracks = set([str(ele[trackIndex]) for ele in submissionData])
		paperGroupsByTrack = {track : [line for line in submissionData if str(line[trackIndex]) == track] for track in tracks}
		keywordsGroupByTrack = {}
		acceptanceRateByTrack = {}
		comparableAcceptanceRate = {}
		topAuthorsByTrack = {}

		# Obtained from the JCDL.org website: past conferences
		comparableAcceptanceRate['year'] = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
		comparableAcceptanceRate['Full Papers'] = [0.29, 0.28, 0.27, 0.29, 0.29, 0.30, 0.29, 0.30]
		comparableAcceptanceRate['Short Papers'] = [0.29, 0.37, 0.31, 0.31, 0.32, 0.50, 0.35, 0.32]
		for track, papers in paperGroupsByTrack.items():
			keywords = [str(ele[keywordIndex]).lower().replace("\r", "").split("\n") for ele in papers]
			keywords = [ele for item in keywords for ele in item]
			# keywordMap = {k : v for k, v in Counter(keywords).iteritems()}
			keywordMap = [[ele[0], ele[1]] for ele in Counter(keywords).most_common(20)]
			keywordsGroupByTrack[track] = keywordMap

			acceptedPapersPerTrack = [ele for ele in papers if str(ele[acceptanceIndex]) == 'accept']
			acceptanceRateByTrack[track] = float(len(acceptedPapersPerTrack)) / len(papers)

			acceptedPapersThisTrack = [paper for paper in papers if str(paper[acceptanceIndex]) == 'accept']
			acceptedAuthorsThisTrack = [str(ele[authorIndex]).replace(" and ", ", ").split(", ") for ele in acceptedPapersThisTrack]
			acceptedAuthorsThisTrack = [ele for item in acceptedAuthorsThisTrack for ele in item]
			topAcceptedAuthorsThisTrack = Counter(acceptedAuthorsThisTrack).most_common(10)
			topAuthorsByTrack[track] = {'names': [ele[0] for ele in topAcceptedAuthorsThisTrack], 'counts': [ele[1] for ele in topAcceptedAuthorsThisTrack]}

			if track == "Full Papers" or track == "Short Papers":
				comparableAcceptanceRate[track].append(float(len(acceptedPapersPerTrack)) / len(papers))

		acceptedAuthors = [str(ele[authorIndex]).replace(" and ", ", ").split(", ") for ele in acceptedSubmission]
		acceptedAuthors = [ele for item in acceptedAuthors for ele in item]
		topAcceptedAuthors = Counter(acceptedAuthors).most_common(10)
		topAcceptedAuthorsMap = {'names': [ele[0] for ele in topAcceptedAuthors], 'counts': [ele[1] for ele in topAcceptedAuthors]}
		# topAcceptedAuthors = {ele[0] : ele[1] for ele in Counter(acceptedAuthors).most_common(10)}

		parsedResult['acceptanceRate'] = acceptanceRate
		parsedResult['overallKeywordMap'] = allKeywordMap
		parsedResult['overallKeywordList'] = allKeywordList
		parsedResult['acceptedKeywordMap'] = acceptedKeywordMap
		parsedResult['acceptedKeywordList'] = acceptedKeywordList
		parsedResult['rejectedKeywordMap'] = rejectedKeywordMap
		parsedResult['rejectedKeywordList'] = rejectedKeywordList
		parsedResult['keywordsByTrack'] = keywordsGroupByTrack
		parsedResult['acceptanceRateByTrack'] = acceptanceRateByTrack
		parsedResult['topAcceptedAuthors'] = topAcceptedAuthorsMap
		parsedResult['topAuthorsByTrack'] = topAuthorsByTrack
		parsedResult['timeSeries'] = timeSeries
		parsedResult['lastEditSeries'] = lastEditSeries
		parsedResult['comparableAcceptanceRate'] = comparableAcceptanceRate

		return JsonResponse({'infoType': 'submission', 'infoData': parsedResult})

	else:
		print('Unable to find submission data!')
		return HttpResponseNotFound('Page not found for CSV')

if __name__ == "__main__":
	parseCSVFile(fileName)