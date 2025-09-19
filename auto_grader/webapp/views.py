from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "home.html")
def student_login(request):
    return render(request, "student/login.html")
def teacher_login(request):
    return render(request, "teacher/login.html")
def hod_login(request):
    return render(request, "hod/login.html")
