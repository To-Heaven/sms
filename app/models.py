from django.db import models

'''
Student

Teacher

TeacherType
    User(多对一)

BanJi
    Student(多对一)
    classAdmin(一对一)
    teacher(多对多)
'''


class Student(models.Model):
    sId = models.AutoField(primary_key=True)
    sName = models.CharField(max_length=32)
    sAge = models.CharField(max_length=6)
    sGender = models.CharField(max_length=6)
    sPhone = models.CharField(max_length=32)
    joinDate = models.DateField(verbose_name='入学时间')

    banJi = models.ForeignKey(to='BanJi', to_field='bId')

    def __str__(self):
        return self.sName


class UserType(models.Model):
    uId = models.AutoField(primary_key=True)
    role = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.role


class Teacher(models.Model):
    tId = models.AutoField(primary_key=True)
    tName = models.CharField(max_length=32)
    tAge = models.CharField(max_length=6)
    tGender = models.CharField(max_length=6)
    tPhone = models.CharField(max_length=32)
    salary = models.CharField(max_length=32)
    userName = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

    teacher2user = models.ForeignKey(to='UserType', to_field='role')

    def __str__(self):
        return self.tName


class BanJi(models.Model):
    bId = models.AutoField(primary_key=True)
    bName = models.CharField(max_length=32)

    banji2teacher = models.ManyToManyField(to='Teacher')


    def __str__(self):
        return self.bName
