from django.contrib import admin

from .models import CsvFile, Author, Submission, Review, UserCsvFile

admin.site.register(CsvFile)
admin.site.register(UserCsvFile)
admin.site.register(Author)
admin.site.register(Submission)
admin.site.register(Review)
