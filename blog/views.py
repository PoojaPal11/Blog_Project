from django.shortcuts import render, get_object_or_404

from blog import forms, models
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
import random
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.views.generic import (CreateView, ListView,
                                  UpdateView, DeleteView,
                                  DetailView)
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger


def index(request):
    return render(request, 'base.html', {})


user = 0


def otp_verify(request):
    otp = request.POST.get('otp')
    uotp = request.POST.get('eotp')

    if otp == uotp:
        user.save()
        return HttpResponse("<h1> Registraion Successful </h1>")
        return render(request, 'base.html', {})
    else:
        return HttpResponse("<h1>OTP Verification Failed </h1>")


def register(request):
    if request.method == 'POST':
        global user
        user = forms.UserModelForm(request.POST)
        otp = random.randint(1111, 9999999)
        if user.is_valid():
            mail = request.POST.get('email')
            pwd = request.POST.get('password')
            user = user.save(commit=False)
            user.set_password(pwd)
            send_mail(
                'OTP',
                f'Here is the otp to complete the registration {otp}.',
                settings.EMAIL_HOST_USER,
                [mail],
                fail_silently=False, )

            return render(request, 'register/otp.html', {'otp': otp})
    else:
        form = forms.UserModelForm()
        return render(request, 'register/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('userpwd')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['username'] = username
                request.session['usr_login'] = True

                return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponse("<h1>Login Again</h1>")
    else:
        return render(request, 'register/login.html')


def user_logout(request):
    del request.session['usr_login']
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def add_user_profile(request):
    if request.method == 'POST':
        form = forms.UserProfileModelForm(request.POST, request.FILES)
        if form.is_valid():
            form_obj = form.save(commit=False)
            usr = request.session['username']
            user = models.User.objects.get(username=usr)
            form_obj.user = user

            if 'prof_pic' in request.FILES:
                form_obj.prof_pic = request.FILES['prof_pic']

            form_obj.save()

            return HttpResponse('Profile Added')
    else:
        form = forms.UserProfileModelForm()
        return render(request, 'register/add_profile.html', {'form': form})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = models.Post
    login_url = '/login/'
    fields = ('author', 'title', 'text')

    def form_valid(self, form):
        instance = form.save(commit=False)
        username = self.request.session['username']

        if instance.author.username == username:
            return super().form_valid(form)
        else:
            return HttpResponse("Invalid Form")


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Post
    login_url = '/login/'
    fields = ('title', 'text')


class PostListView(ListView):
    model = models.Post
    paginate_by = 2

    def get_queryset(self):
        return self.model.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        list_exam = self.model.objects.all()  # get all model objects
        paginator = Paginator(list_exam, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)

        context['list_exams'] = file_exams
        context['Pagination'] = "This is A Context"
        return context


class PostDraftListView(LoginRequiredMixin, ListView):
    model = models.Post
    login_url = '/login/'
    paginate_by = 2

    def get_queryset(self):
        usr = self.request.session['username']
        user = models.User.objects.get(username=usr)
        return self.model.objects.filter(author=user, published_date__isnull=True).order_by('created_date')

    def get_context_data(self, **kwargs):
        context = super(PostDraftListView, self).get_context_data(**kwargs)
        list_exam = self.model.objects.all()  # get all model objects
        paginator = Paginator(list_exam, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)

        context['list_exams'] = file_exams
        context['Pagination'] = "This is A Context"
        return context


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Post
    success_url = reverse_lazy('app:list_post')


class PostDetailView(DetailView):
    model = models.Post


def post_publish(request, pk):
    post = get_object_or_404(models.Post, pk=pk)

    post.publish()

    return HttpResponseRedirect(reverse('app:list_post'))


def add_comment(request, pk):

    if request.method == "POST":
        form = forms.CommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = get_object_or_404(models.Post, pk=pk)
            comment.save()

            return HttpResponseRedirect(reverse('app:list_post'))
        else:
            print(form.errors)
            return HttpResponse("Invalid form")

    else:
        form = forms.CommentModelForm()
        return render(request, 'blog/comments.html', {'form': form, 'id': pk})
