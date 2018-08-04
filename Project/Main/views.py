from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from Main.models import Question, Profile, Answer, Vote
from Main.forms import Update
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Create your views here.
@csrf_protect
def user_login(request):
  top = Profile.objects.all().order_by("-points")[:min(Profile.objects.count(),5)]
  if request.user.is_authenticated:
    return HttpResponseRedirect('/')
  if request.method == 'POST':
    if 'email' in request.POST:
      username = request.POST['username']
      email = request.POST['email']
      password = request.POST['password']
      conf_password = request.POST['conf_password']

      if password==conf_password:
        if User.objects.filter(email=email).exists():
          messages.error(request, "An account already exists on this email.")
          return render(request,'login.html',{})
        if User.objects.filter(username=username).exists():
          messages.error(request, "Username already in use.")
          return render(request,'login.html',{})
        user = User.objects.create_user(username, email, password)
        user.save()
        profile = Profile(user=user)
        profile.save()
        messages.success(request, "Account created.")
      else:
        messages.error(request, "Passwords do not match.")
      return render(request,'login.html',{"q":Question.objects.count(),"a":Answer.objects.count(),"u":Profile.objects.count(),"top":top})


    else:
      username = request.POST['username']
      password = request.POST['password']
      user = authenticate(username=username, password=password)
      if user is not None:
        if user.is_active:
          login(request, user)
          return HttpResponseRedirect('/')
        else:
          return HttpResponse("You're account is disabled.")
      else:
        messages.error(request, "Invalid username or password")
        return render(request,'login.html',{})
  else:
    return render(request,'login.html',{"q":Question.objects.count(),"a":Answer.objects.count(),"u":Profile.objects.count(),"top":top})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


@login_required
def Question_create(request):
  top = Profile.objects.all().order_by("-points")[:min(Profile.objects.count(),5)]
  if request.user.is_authenticated:
    profile = get_object_or_404(Profile,user=request.user)
    if profile.points < 100:
      val = str(profile.points)+" / 100"
      percent = float(profile.points)/100*100
    elif profile.points < 1000:
      val = str(profile.points)+" / 1000"
      percent = float(profile.points)/1000*100
    elif profile.points < 2000:
      val = str(profile.points)+" / 2000"
      percent = float(profile.points)/2000*100
    else:
      val = str(profile.points)
      percent = 100
  else:
    profile = get_object_or_404(Profile,id=1)
    val = ""
    percent = 100


  if request.method == 'POST':
    question = request.POST['question']
    des = request.POST['description']
    user = request.user
    instance=get_object_or_404(Profile,user=user)
    ques = Question(user=instance,question=question, description=des)
    ques.save()
    instance.points = instance.points + 2
    instance.questions = instance.questions+1
    instance.save()
    messages.success(request, "Question Submitted.")
    return HttpResponseRedirect('/')
  context={
    "value":"",
    "description":"",
    "action":"/create/",
    "profile":profile,
    "val":val,
    "percent":percent,"q":Question.objects.count(),"a":Answer.objects.count(),"u":Profile.objects.count(),"top":top
  }
  return render(request,"create.html",context)


@login_required
def Question_update(request, id):
  instance=get_object_or_404(Question,id=id)
  if request.user == instance.user.user:
    top = Profile.objects.all().order_by("-points")[:min(Profile.objects.count(),5)]
    if request.user.is_authenticated:
      profile = get_object_or_404(Profile,user=request.user)
      if profile.points < 100:
        val = str(profile.points)+" / 100"
        percent = float(profile.points)/100*100
      elif profile.points < 1000:
        val = str(profile.points)+" / 1000"
        percent = float(profile.points)/1000*100
      elif profile.points < 2000:
        val = str(profile.points)+" / 2000"
        percent = float(profile.points)/2000*100
      else:
        val = str(profile.points)
        percent = 100
    else:
      profile = get_object_or_404(Profile,id=1)
      val = ""
      percent = 100
    
    if request.method == 'POST':
      question = request.POST['question']
      des = request.POST['description']
      instance.question = question
      instance.description = des
      instance.save()
      messages.success(request, "Question Updated.")
      return HttpResponseRedirect('/')
    x="/update/" + str(id) + "/"
    context={
      "value":instance.question,
      "description":instance.description,
      "action":x,
      "profile":profile,
      "val":val,
      "percent":percent,"q":Question.objects.count(),"a":Answer.objects.count(),"u":Profile.objects.count(),"top":top
    }
    return render(request,"create.html",context)
  else:
    messages.error(request, "User unauthorized.")
    return HttpResponseRedirect('/')

@login_required
def Answer_update(request, id):
  instance=get_object_or_404(Answer,id=id)
  if request.user == instance.user.user:
    top = Profile.objects.all().order_by("-points")[:min(Profile.objects.count(),5)]
    if request.user.is_authenticated:
      profile = get_object_or_404(Profile,user=request.user)
      if profile.points < 100:
        val = str(profile.points)+" / 100"
        percent = float(profile.points)/100*100
      elif profile.points < 1000:
        val = str(profile.points)+" / 1000"
        percent = float(profile.points)/1000*100
      elif profile.points < 2000:
        val = str(profile.points)+" / 2000"
        percent = float(profile.points)/2000*100
      else:
        val = str(profile.points)
        percent = 100
    else:
      profile = get_object_or_404(Profile,id=1)
      val = ""
      percent = 100
    
    if request.method == 'POST':
      answer = request.POST['answer']
      instance.answer = answer
      instance.save()
      messages.success(request, "Answer Updated.")
      return HttpResponseRedirect('/')
    x="/ansupdate/" + str(id) + "/"
    context={
      "value":instance.answer,
      "action":x,
      "profile":profile,
      "val":val,
      "percent":percent,"q":Question.objects.count(),"a":Answer.objects.count(),"u":Profile.objects.count(),"top":top
    }
    return render(request,"ans_create.html",context)
  else:
    messages.error(request, "User unauthorized.")
    return HttpResponseRedirect('/')


@login_required
def Answer_delete(request,id=None):
  instance=get_object_or_404(Answer,id=id)
  if request.user == instance.user.user:
    instance.question.answers = instance.question.answers-1
    instance.question.save()
    instance.accepted = 0
    instance.save()
    if Answer.objects.filter(question=instance.question, accepted=1).exists():
      instance.question.answered = 1
    else:
      instance.question.answered = 0
    instance.question.save()
    instance.user.answers = instance.user.answers - 1
    instance.user.save()
    instance.delete()
    messages.success(request, "Successfully deleted")
  return HttpResponseRedirect('/')


@login_required
def Answer_accept(request,id=None):
  instance=get_object_or_404(Answer,id=id)
  if request.user == instance.question.user.user:
    instance.accepted = 1
    instance.user.points = instance.user.points + 10
    instance.user.save()
    instance.save()
    instance.question.answered = 1
    instance.question.save()
    return HttpResponseRedirect('/question/'+str(instance.question.id)+'/')
  else:
    messages.error(request, "User unauthorized.")
    return HttpResponseRedirect('/question/'+str(instance.question.id)+'/')


@login_required
def vote_up(request,id=None):
  instance=get_object_or_404(Answer,id=id)
  print (instance)
  if Vote.objects.all().filter(answer=instance, user=request.user).exists():
    vote = get_object_or_404(Vote,answer=instance, user=request.user)
    if vote.vote==-1:
      instance.votes = instance.votes+2
      instance.save()
      vote.vote = 1
      vote.save()
      return HttpResponseRedirect('/question/'+str(instance.question.id)+'/')
    else:
      messages.error(request, "Already voted up")
      return HttpResponseRedirect('/question/'+str(instance.question.id)+'/')
  else:

    vote = Vote(answer=instance, user=request.user,vote=1)
    instance.votes = instance.votes+1
    instance.save()
    vote.save()
    return HttpResponseRedirect('/question/'+str(instance.question.id)+'/')


@login_required
def vote_down(request,id=None):
  instance=get_object_or_404(Answer,id=id)
  if Vote.objects.filter(answer=instance, user=request.user).exists():
    vote = get_object_or_404(Vote,answer=instance, user=request.user)
    if vote.vote==1:
      instance.votes = instance.votes-2
      instance.save()
      vote.vote = -1
      vote.save()
      return HttpResponseRedirect('/question/'+str(instance.question.id)+'/')
    else:
      messages.error(request, "Already voted down")
      return HttpResponseRedirect('/question/'+str(instance.question.id)+'/')
  else:
    vote = Vote(answer=instance, user=request.user,vote=-1)
    instance.votes = instance.votes-1
    instance.save()
    vote.save()
    return HttpResponseRedirect('/question/'+str(instance.question.id)+'/')


@login_required
def Answer_unaccept(request,id=None):
  instance=get_object_or_404(Answer,id=id)
  if request.user == instance.question.user.user:
    instance.accepted = 0
    instance.user.points = instance.user.points - 10
    instance.user.save()
    instance.save()
    if Answer.objects.filter(question=instance.question, accepted=1).exists():
      instance.question.answered = 1
    else:
      instance.question.answered = 0
    instance.question.save()
    return HttpResponseRedirect('/question/'+str(instance.question.id)+'/')
  else:
    messages.error(request, "User unauthorized.")
    return HttpResponseRedirect('/question/'+str(instance.question.id)+'/')

def Question_detail(request,id):
  top = Profile.objects.all().order_by("-points")[:min(Profile.objects.count(),5)]
  if request.user.is_authenticated:
    profile = get_object_or_404(Profile,user=request.user)
    if profile.points < 100:
      val = str(profile.points)+" / 100"
      percent = float(profile.points)/100*100
    elif profile.points < 1000:
      val = str(profile.points)+" / 1000"
      percent = float(profile.points)/1000*100
    elif profile.points < 2000:
      val = str(profile.points)+" / 2000"
      percent = float(profile.points)/2000*100
    else:
      val = str(profile.points)
      percent = 100
  else:
    profile = get_object_or_404(Profile,id=1)
    val = ""
    percent = 100
  instance=get_object_or_404(Question,id=id)
  instance.views = instance.views + 1
  instance.save()

  queryset_list=Answer.objects.all().filter(question=instance).order_by("-accepted","-votes","-timestamp")
  query=request.GET.get('q')
  if query:
    queryset_list=queryset_list.filter(
    Q(answer__icontains=query)|
    Q(user__user__username__icontains=query)
    ).distinct()
  paginator = Paginator(queryset_list, 10)
  page = request.GET.get('page')
  try:
    queryset = paginator.page(page)
  except PageNotAnInteger:
    queryset = paginator.page(1)
  except EmptyPage:
    queryset = paginator.page(paginator.num_pages)
  

  if request.method == 'POST':
    if request.user.is_authenticated:
      if request.POST['answer']!="":
        answer = request.POST['answer']
        question = instance
        instance=get_object_or_404(Profile,user=request.user)
        ans=Answer(answer=answer, question=question, user=instance)
        question.answers = question.answers+1
        instance.points = instance.points + 1
        instance.answers = instance.answers + 1
        instance.save()
        question.save()
        ans.save()
        return HttpResponseRedirect('/question/'+str(id)+'/')
    else:
      messages.error(request, "Please log in to answer.")
      return HttpResponseRedirect('/login/')

  context={
    "question":instance,
    "object_list":queryset,
    "page":"page",
    "profile":profile,
    "val":val,
    "percent":percent,"q":Question.objects.count(),"a":Answer.objects.count(),"u":Profile.objects.count(),"top":top
  }
  return render (request, "question.html",context)


def Question_list(request):
  top = Profile.objects.all().order_by("-points")[:min(Profile.objects.count(),5)]
  if request.user.is_authenticated:
    profile = get_object_or_404(Profile,user=request.user)
    if profile.points < 100:
      val = str(profile.points)+" / 100"
      percent = float(profile.points)/100*100
    elif profile.points < 1000:
      val = str(profile.points)+" / 1000"
      percent = float(profile.points)/1000*100
    elif profile.points < 2000:
      val = str(profile.points)+" / 2000"
      percent = float(profile.points)/2000*100
    else:
      val = str(profile.points)
      percent = 100
  else:
    profile = get_object_or_404(Profile,id=1)
    val = ""
    percent = 100


  queryset_list=Question.objects.all().order_by("-timestamp")
  query=request.GET.get('q')
  if query:
    queryset_list=queryset_list.filter(
    Q(question__icontains=query)|
    Q(description__icontains=query)|
    Q(user__user__username__icontains=query)
    ).distinct()
  paginator = Paginator(queryset_list, 10)
  page = request.GET.get('page')
  username='Login'
  if User.is_active:
    username = User.username
  try:
    queryset = paginator.page(page)
  except PageNotAnInteger:
    queryset = paginator.page(1)
  except EmptyPage:
    queryset = paginator.page(paginator.num_pages)
  context={
    "object_list":queryset,
    "page":"page",
    "username":username,
    "home":"active",
    "home_views":"blank",
    "profile":profile,
    "val":val,
    "percent":percent,"q":Question.objects.count(),"a":Answer.objects.count(),"u":Profile.objects.count(),"top":top
  }
  return render(request,"index.html",context)


def Question_list_views(request):
  top = Profile.objects.all().order_by("-points")[:min(Profile.objects.count(),5)]
  if request.user.is_authenticated:
    profile = get_object_or_404(Profile,user=request.user)
    if profile.points < 100:
      val = str(profile.points)+" / 100"
      percent = float(profile.points)/100*100
    elif profile.points < 1000:
      val = str(profile.points)+" / 1000"
      percent = float(profile.points)/1000*100
    elif profile.points < 2000:
      val = str(profile.points)+" / 2000"
      percent = float(profile.points)/2000*100
    else:
      val = str(profile.points)
      percent = 100
  else:
    profile = get_object_or_404(Profile,id=1)
    val = ""
    percent = 100
  queryset_list=Question.objects.all().order_by("-views")
  query=request.GET.get('q')
  if query:
    queryset_list=queryset_list.filter(
    Q(question__icontains=query)|
    Q(description__icontains=query)|
    Q(user__user__username__icontains=query)
    ).distinct()
  paginator = Paginator(queryset_list, 10)
  page = request.GET.get('page')
  username='Login'
  if User.is_active:
    username = User.username
  try:
    queryset = paginator.page(page)
  except PageNotAnInteger:
    queryset = paginator.page(1)
  except EmptyPage:
    queryset = paginator.page(paginator.num_pages)
  context={
    "object_list":queryset,
    "page":"page",
    "username":username,
    "home":"blank",
    "home_views":"active",
    "profile":profile,
    "val":val,
    "percent":percent,"q":Question.objects.count(),"a":Answer.objects.count(),"u":Profile.objects.count(),"top":top
  }
  return render(request,"index.html",context)


@login_required
def Question_delete(request,id=None):
  instance=get_object_or_404(Question,id=id)
  if request.user == instance.user.user:
    instance.user.questions = instance.user.questions-1
    instance.user.save()
    instance.delete()
    messages.success(request, "Successfully deleted")
  return HttpResponseRedirect('/')


@login_required
def profile(request, id):
  top = Profile.objects.all().order_by("-points")[:min(Profile.objects.count(),5)]
  if request.user.is_authenticated:
    profile = get_object_or_404(Profile,id=id)
    if profile.points < 100:
      color = "#3498db"
      rank = "Amateur"
    elif profile.points < 1000:
      color = "#1abc9c"
      rank = "Trainee"
    elif profile.points < 2000:
      color = "gold"
      rank = "Professor"
    else:
      color = "red"
      rank = "Legend"
  else:
    profile = get_object_or_404(Profile,id=1)
    val = ""
    percent = 100

  queryset_list=Question.objects.all().filter(user=profile).order_by("-timestamp")
  paginator = Paginator(queryset_list, 10)
  page = request.GET.get('page')
  username='Login'
  if User.is_active:
    username = User.username
  try:
    queryset = paginator.page(page)
  except PageNotAnInteger:
    queryset = paginator.page(1)
  except EmptyPage:
    queryset = paginator.page(paginator.num_pages)


  queryset_list1=Answer.objects.all().filter(user=profile).order_by("-timestamp")
  paginator1 = Paginator(queryset_list1, 10)
  page1 = request.GET.get('page1')
  username='Login'
  if User.is_active:
    username = User.username
  try:
    queryset1 = paginator1.page(page1)
  except PageNotAnInteger:
    queryset1 = paginator1.page(1)
  except EmptyPage:
    queryset1 = paginator1.page(paginator1.num_pages)


  context={
    "profile":profile,
    "color":color,
    "rank": rank,
    "object_list":queryset,
    "page":"page",
    "object_list1":queryset1,
    "page1":"page1","q":Question.objects.count(),"a":Answer.objects.count(),"u":Profile.objects.count(),"top":top
  }
  return render(request,"profile.html",context)

@login_required
def Update_pro(request, id):
  top = Profile.objects.all().order_by("-points")[:min(Profile.objects.count(),5)]
  profile = get_object_or_404(Profile,id=id)
  instance=get_object_or_404(Profile,id=id)
  if request.user == instance.user:
    form = Update(request.POST or None, request.FILES or None,instance=instance)
    if form.is_valid():
      instance=form.save(commit=False)
      instance.save()
      messages.success(request, "Saved")
      return HttpResponseRedirect('/')
    context={
      "instance":instance,
      "form":form,"q":Question.objects.count(),"a":Answer.objects.count(),"u":Profile.objects.count(),"top":top,
      "profile":profile
    }
    return render(request,"update.html",context)
  else:
    messages.error(request, "User unauthorized.")
    return HttpResponseRedirect('/')


def User_list(request):
  top = Profile.objects.all().order_by("-points")[:min(Profile.objects.count(),5)]
  if request.user.is_authenticated:
    profile = get_object_or_404(Profile,user=request.user)
    if profile.points < 100:
      val = str(profile.points)+" / 100"
      percent = float(profile.points)/100*100
    elif profile.points < 1000:
      val = str(profile.points)+" / 1000"
      percent = float(profile.points)/1000*100
    elif profile.points < 2000:
      val = str(profile.points)+" / 2000"
      percent = float(profile.points)/2000*100
    else:
      val = str(profile.points)
      percent = 100
  else:
    profile = get_object_or_404(Profile,id=1)
    val = ""
    percent = 100


  queryset_list=Profile.objects.all().order_by("user__username")
  query=request.GET.get('q')
  if query:
    queryset_list=queryset_list.filter(
    Q(location__icontains=query)|
    Q(user__username__icontains=query)
    ).distinct()
  paginator = Paginator(queryset_list, 10)
  page = request.GET.get('page')
  username='Login'
  if User.is_active:
    username = User.username
  try:
    queryset = paginator.page(page)
  except PageNotAnInteger:
    queryset = paginator.page(1)
  except EmptyPage:
    queryset = paginator.page(paginator.num_pages)
  context={
    "object_list":queryset,
    "page":"page",
    "username":username,
    "profile":profile,
    "val":val,
    "percent":percent,"q":Question.objects.count(),"a":Answer.objects.count(),"u":Profile.objects.count(),"top":top
  }
  return render(request,"user.html",context)