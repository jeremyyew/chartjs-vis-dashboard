from django.contrib import admin

from .models import CsvFile, Author, Submission, Review

admin.site.register(CsvFile)
admin.site.register(Author)
admin.site.register(Submission)
admin.site.register(Review)
