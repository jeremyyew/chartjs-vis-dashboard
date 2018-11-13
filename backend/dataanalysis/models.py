from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class CsvFile(models.Model):
    AUTHOR_FILE_TYPE = 1
    SUBMISSION_FILE_TYPE = 2
    REVIEW_FILE_TYPE = 3
    FILE_TYPE_CHOICES = (
        (AUTHOR_FILE_TYPE, 'Author'),
        (SUBMISSION_FILE_TYPE, 'Submission'),
        (REVIEW_FILE_TYPE, 'Review'),
    )

    # user_id = models.IntegerField() not required
    # For more flexibility normalization can be used
    file_type = models.IntegerField(choices=FILE_TYPE_CHOICES)
    file_hash = models.CharField(max_length=64, unique=True)


class UserCsvFile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    csv_file = models.ForeignKey(CsvFile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'csv_file',)


class Author(models.Model):
    submission_id = models.IntegerField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    country = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    web_page = models.CharField(max_length=255)  # null = True?, better not I suppose, URLField?
    person_id = models.IntegerField('author unique id', null=True)  # consider isolated (allow duplicate) or central
    is_corresponding = models.BooleanField()

    user_file = models.ForeignKey(CsvFile, on_delete=models.CASCADE)


class Submission(models.Model):
    TRACK_NAME_CHOICES = (
        ('Full Papers', 'Full Papers'),
        ('Short Papers', 'Short Papers'),
        ('Posters and Demos', 'Posters and Demos'),
        ('Poster/Demo 2', 'Poster/Demo 2'),
        ('Panels', 'Panels'),
        ('Doctoral Consortium', 'Doctoral Consortium'),
        ('Tutorials', 'Tutorials'),
        ('JCDL 2018 - Workshops', 'JCDL 2018 - Workshops'),
    )
    ACCEPT_DECISION = 'accept'
    REJECT_DECISION = 'reject'
    NO_DECISION = 'no decision'
    DECISION_CHOICES = (
        (ACCEPT_DECISION, 'Accept'),
        (REJECT_DECISION, 'Reject'),
        (NO_DECISION, 'No decision'),
    )

    # TODO: rename to submission_friendly_id, to prevent conflict with the actual submission_id
    submission_no = models.IntegerField()
    # TODO: verify if it works with all data
    track_no = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    # TODO: verify if it works with all data
    # We can collapse track_name and track_no into 1 by using choices. Furthermore, we can use normalization
    # for more flexibility. However, for simplicity we just map the data like how it is in CSV
    track_name = models.CharField(max_length=255, choices=TRACK_NAME_CHOICES)
    title = models.CharField(max_length=255)
    authors = models.TextField()
    submitted = models.DateTimeField()  # to ensure timezone correct
    last_updated = models.DateTimeField()
    form_fields = models.CharField(max_length=255)
    keywords = models.TextField()
    decision = models.CharField(max_length=255, choices=DECISION_CHOICES)
    notified = models.BooleanField()
    reviews_sent = models.BooleanField()
    abstract = models.TextField()

    user_file = models.ForeignKey(CsvFile, on_delete=models.CASCADE)


class Review(models.Model):
    review_no = models.IntegerField()
    submission_id = models.IntegerField()
    # better to use foreign key so we can join? But we want auto generated id for Submission for now
    # submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    review_assignment_no = models.IntegerField()
    reviewer_name = models.CharField(max_length=255)
    field_no = models.IntegerField('expertise level', validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_comments = models.TextField()
    overall_evaluation_score_formatted = models.TextField()
    overall_evaluation_score = models.IntegerField()

    # subreviewer info that we ignore but store first if we want to use next time
    subreviewer_info_col_one = models.CharField(max_length=255)
    subreviewer_info_col_two = models.CharField(max_length=255)
    subreviewer_info_col_three = models.CharField(max_length=255)
    subreviewer_info_col_four = models.CharField(max_length=255)

    submission_date = models.DateField()
    submission_time = models.TimeField()
    recommendation_for_best_paper = models.BooleanField()

    user_file = models.ForeignKey(CsvFile, on_delete=models.CASCADE)

