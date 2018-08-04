from django.contrib import admin
from Main.models import Question, Profile, Answer, Vote

# Register your models here.
class Questionadmin(admin.ModelAdmin):
	list_display=["question", "user", "views", "answers"]
	list_display_links=["question", "user", "views", "answers"]
	list_filter=["timestamp"]
	search_fields=["question","description"]
	class Meta:
		model=Question


class Profileadmin(admin.ModelAdmin):
	list_display=["user"]
	list_display_links=["user"]
	search_fields=["user"]
	class Meta:
		model=Profile


class Answeradmin(admin.ModelAdmin):
	list_display=["question","answer","user","votes"]
	list_display_links=["question","answer","user","votes"]
	search_fields=["question","answer","user"]
	class Meta:
		model=Answer


class Voteadmin(admin.ModelAdmin):
	list_display=["user","answer"]
	list_display_links=["user","answer"]
	search_fields=["user","answer"]
	class Meta:
		model=Vote


admin.site.register(Question,Questionadmin)
admin.site.register(Profile,Profileadmin)
admin.site.register(Answer,Answeradmin)
admin.site.register(Vote,Voteadmin)