from django.db import models
from django.conf import settings

# Create your models here.
def upload_location(instance, filename):
	return "%s/%s" %(instance.user.username, filename)


class Profile(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	image=models.ImageField(upload_to=upload_location,null=True,blank=True,)
	location=models.TextField(default="Not mentioned")
	points=models.IntegerField(default=0)
	questions=models.IntegerField(default=0)
	answers=models.IntegerField(default=0)

	def __str__(self):
		return self.user.username


class Question(models.Model):
	user=models.ForeignKey(Profile,on_delete=models.CASCADE)
	question=models.TextField()
	description=models.TextField(null=True, blank=True)
	views=models.IntegerField(default=0)
	answers=models.IntegerField(default=0)
	answered=models.IntegerField(default=0)
	timestamp=models.DateTimeField(auto_now=False, auto_now_add=True)

	def __str__(self):
		return self.question


class Answer(models.Model):
	question = models.ForeignKey(Question,on_delete=models.CASCADE)
	user=models.ForeignKey(Profile,on_delete=models.CASCADE)
	answer=models.TextField()
	votes=models.IntegerField(default=0)
	accepted=models.IntegerField(default=0)
	timestamp=models.DateTimeField(auto_now=False, auto_now_add=True)

	def __str__(self):
		return self.question.question


class Vote(models.Model):
	answer = models.ForeignKey(Answer,on_delete=models.CASCADE)
	user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	vote=models.IntegerField(default=0)
	def __str__(self):
		return self.answer