from django.contrib import admin
from.models import Question, Answer, Comment, Category

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Comment)
admin.site.register(Category)

# Register your models here.
