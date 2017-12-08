from django.shortcuts import render, redirect
from django.conf import settings
from app import models

from app.forms import LoginForm
from app.forms import TeacherForm
from app.forms import StudentForm
from app.forms import BanJiForm





def authModify(func):
    def inner(request, *args, **kwargs):
        username = request.session.get(settings.LOGINAUTH)['userName']
        user = models.Teacher.objects.filter(tName=username, teacher2user__role='classAdmin')
        if not user:
            return redirect('/noAuthority/')
        return func(request, *args, **kwargs)

    return inner


def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if not form.is_valid():
            form.add_error('password', '用户名或密码错误')
            return render(request, 'login.html', {'form': form})
        else:
            request.session[settings.LOGINAUTH] = {'username': form.cleaned_data['userName']}
            return redirect('/home/')

    elif request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    # if request.method == 'POST':
    #     userName = request.POST.get('userName')
    #     password = request.POST.get('password')
    #     user = models.Teacher.objects.filter(userName=userName, password=password).first()
    #     if not user:
    #         return redirect('/login/')
    #     request.session[settings.LOGINAUTH] = {'userName': user.tName}
    #     return render(request, 'home.html', {'user': user})
    # form = LoginForm()
    # return render(request, 'login.html', {'form': form})


def home(request):
    return render(request, 'base.html')


def showStudents(request):
    students = models.Student.objects.all()
    return render(request, 'showStudents.html', {'students': students})



def addStudent(request):
    if request.method == 'POST':
        form = StudentForm(data=request.POST)
        if not form.is_valid():
            return render(request, 'addStudent.html', {'form': form})

        form.cleaned_data['banJi_id'] = form.cleaned_data['banJi']
        del form.cleaned_data['banJi']
        models.Student.objects.create(**(form.cleaned_data))
        return redirect('/showStudents/')
    form = StudentForm()
    return render(request, 'addStudent.html', {'form': form})


def noAuthority(request):
    return render(request, 'noAuthority.html')



def deleteStudent(request):
    sId = request.GET.get('id')
    stduent = models.Student.objects.get(sId=sId)
    stduent.delete()
    return redirect('/showStudents/')



def editStudent(request):
    sId = request.GET.get('id')
    if request.method == 'POST':
        form = StudentForm(data=request.POST)
        if not form.is_valid():
            return render(request, 'editStudent.html', {'form': form})

        form.cleaned_data['banJi_id'] = form.cleaned_data['banJi']
        del form.cleaned_data['banJi']
        models.Student.objects.filter(sId=sId).update(**(form.cleaned_data))
        return redirect('/showStudents/')

    if request.method == 'GET':
        student = models.Student.objects.get(sId=sId)
        form = StudentForm(initial={
            'sName': student.sName,
            'sAge': student.sAge,
            'sGender': student.sGender,
            'sPhone': student.sPhone,
            'joinDate': student.joinDate,
            'banJi': student.banJi.bId
        })
        return render(request, 'editStudent.html', {'form': form, 'id': sId})


def studentInfo(request):
    sId = request.GET.get('id')
    student = models.Student.objects.filter(sId=sId).first()
    return render(request, 'studentInfo.html', {'student': student})


def showTeachers(request):
    teachers = models.Teacher.objects.all()
    return render(request, 'showTeachers.html', {'teachers': teachers})



def addTeacher(request):
    if request.method == 'POST':
        form = TeacherForm(data=request.POST)
        if not form.is_valid():
            return render(request, 'addTeacher.html', {'form': form})
        print(
            form.cleaned_data)  # {'tName': 'alex', 'tAge': '83', 'tGender': '男', 'tPhone': '64161651', 'salary': '15000', 'teacher2user': '1'}

        form.cleaned_data['teacher2user_id'] = models.UserType.objects.get(uId=form.cleaned_data['teacher2user']).role
        del form.cleaned_data['teacher2user']

        models.Teacher.objects.create(**(form.cleaned_data))

        return redirect('/showTeachers/')

    form = TeacherForm()
    return render(request, 'addTeacher.html', {'form': form})


def teacherInfo(request):
    tId = request.GET.get('id')
    teacher = models.Teacher.objects.get(tId=tId)
    return render(request, 'teacherInfo.html', {'teacher': teacher})



def delTeacher(request):
    tId = request.GET.get('id')
    teacher = models.Teacher.objects.get(tId=tId)
    teacher.delete()
    return redirect('/showTeachers/')


def editTeacher(request):
    tId = request.GET.get('id')
    if request.method == 'POST':
        form = TeacherForm(data=request.POST)
        if not form.is_valid():
            return render(request, 'editTeacher.html', {'form': form})
        print(
            form.cleaned_data)  # {'tName': 'egon', 'tAge': '73', 'tGender': 'male', 'tPhone': '123456789', 'salary': '100000', 'teacher2user': '2'}
        form.cleaned_data['teacher2user_id'] = models.UserType.objects.get(uId=form.cleaned_data['teacher2user']).role
        del form.cleaned_data['teacher2user']

        models.Teacher.objects.filter(tId=tId).update(**(form.cleaned_data))
        return redirect('/showTeachers/')
    else:
        teacher = models.Teacher.objects.get(tId=tId)
        form = TeacherForm(
            initial={
                'tName': teacher.tName,
                'tAge': teacher.tAge,
                'tGender': teacher.tGender,
                'tPhone': teacher.tPhone,
                'teacher2user': teacher.teacher2user.role,
                'salary': teacher.salary
            }
        )
        return render(request, 'editTeacher.html', {'form': form, 'tId': tId})


def showBanJis(request):
    banJis = models.BanJi.objects.all()
    return render(request, 'showBanJis.html', {'banJis': banJis})


def delBanJi(request):
    bId = request.GET.get('id')
    banJi = models.BanJi.objects.get(bId=bId)
    banJi.delete()
    return redirect('/showBanJis/')


def addBanJi(request):
    bId = request.GET.get('id')

    if request.method == 'POST':
        form = BanJiForm(data=request.POST)
        if not form.is_valid():
            return render(request, 'addBanJi.html', {'form': form})

        teachers = models.Teacher.objects.filter(tId__in=form.cleaned_data['banji2teacher'])
        banZhuRen = models.Teacher.objects.get(tId=form.cleaned_data['banZhuRen'])
        newBanJi = models.BanJi.objects.create(bName=form.cleaned_data['bName'])
        teachersList = [i for i in teachers]
        print(teachersList)
        newBanJi.banji2teacher.add(*teachersList, banZhuRen)
        return redirect('/showBanJis/')

    form = BanJiForm()
    return render(request, 'addBanJi.html', {'form': form})


def editBanJi(request):
    bId = request.GET.get('id')

    if request.method == 'POST':
        form = BanJiForm(data=request.POST)
        if not form.is_valid():
            return render(request, 'editBanJi.html', {'form': form})

        teachers = models.Teacher.objects.filter(tId__in=form.cleaned_data['banji2teacher'])
        banZhuRen = models.Teacher.objects.get(tId=form.cleaned_data['banZhuRen'])

        banJi = models.BanJi.objects.filter(bName=form.cleaned_data['bName']).first()

        models.BanJi.objects.filter(bName=form.cleaned_data['bName']).update(bName=form.cleaned_data['bName'])
        teacher_list = [i for i in teachers]

        banJi.banji2teacher.add(*teacher_list, banZhuRen)
        return redirect('/showBanJis/')

    banJi = models.BanJi.objects.get(bId=bId)
    form = BanJiForm(initial={
        'bName': banJi.bName,
        'banji2teacher': banJi.banji2teacher.values_list('tId', 'tName')  # 要指定字段
    })

    # print(form.banji2teacher)
    return render(request, 'editBanJi.html', {'form': form, 'bId': 'bId'})


def banJiInfo(request):
    bId = request.GET.get('id')
    banJi = models.BanJi.objects.get(bId=bId)
    return render(request, 'banJiInfo.html', {'banJi': banJi})
