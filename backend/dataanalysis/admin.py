from django.contrib import admin

from .models import UserFile, Author, Submission, Review

admin.site.register(UserFile)
admin.site.register(Author)
admin.site.register(Submission)
admin.site.register(Review)
