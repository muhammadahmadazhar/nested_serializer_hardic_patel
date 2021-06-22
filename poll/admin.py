from django.contrib import admin
from .models import *
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["title", "id"]

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["text", "question", "id"]
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Answer)
