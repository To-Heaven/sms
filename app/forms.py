from django.forms import Form
from django.forms import fields
from django.forms import widgets
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app import models

class LoginForm(Form):
    userName = fields.CharField(required=True,
                                error_messages={'required': '姓名不能为空'},
                                widget=widgets.TextInput(attrs={'placeholder': "username",
                                                                'class': "form-control"}))

    password = fields.CharField(required=True,
                                error_messages={'required': '密码不能为空',
                                                'invalid': '密码格式错误'},
                                widget=widgets.TextInput(attrs=({'placeholder': "password",
                                                                 'class': 'form-control'})),
                                validators=[RegexValidator(regex='[a-zA-Z0-9]+',
                                                           message='密码只能有数字和大小写字母组成',
                                                           code='invalid')])

    # def clean_username(self):
    #     userName = self.cleaned_data['userName']
    #     user = models.Teacher.objects.filter(userName=userName)
    #     if not user:
    #         raise ValidationError('用户不存在')


class StudentForm(Form):
    sName = fields.CharField(max_length=32,
                             required=True,
                             error_messages={'required': '学生姓名不能为空'},
                             widget=widgets.TextInput(attrs={'placeholder': '学生姓名',
                                                             'class': 'form-control'}))

    sAge = fields.CharField(max_length=32,
                            required=True,
                            error_messages={'required': '学生年龄不能为空'},
                            widget=widgets.TextInput(attrs={'placeholder': '学生年龄',
                                                            'class': 'form-control'}))

    sGender = fields.CharField(max_length=32,
                               required=True,
                               error_messages={'required': '学生性别不能为空'},
                               widget=widgets.TextInput(attrs={'placeholder': '学生性别',
                                                               'class': 'form-control'}))
    sPhone = fields.CharField(max_length=32,
                              required=True,
                              error_messages={'required': '学生手机号不能为空'},
                              widget=widgets.TextInput(attrs={'placeholder': '学生手机号',
                                                              'class': 'form-control'}))

    joinDate = fields.DateField(required=True,
                                error_messages={'required': '学生入学日期不能为空',
                                                'invalid': '正确日期格式: xxxx-xx-xx'},
                                widget=widgets.DateInput(format='%Y-%d-%m',
                                                         attrs={'placeholder': 'xxxx-xx-xx',
                                                                'class': 'form-control'}))

    banJi = fields.ChoiceField(choices=models.BanJi.objects.values_list('bId', 'bName'),
                               required=True,
                               error_messages={'required': '班级'},
                               widget=widgets.Select(attrs={'class': 'form-control'}))


class TeacherForm(Form):
    tName = fields.CharField(required=True,
                             error_messages={'required': '姓名不能为空'},
                             widget=widgets.TextInput(attrs={'placeholder': '姓名',
                                                             'class': 'form-control'}))

    tAge = fields.CharField(required=True,
                            error_messages={'required': '年龄不能为空'},
                            widget=widgets.TextInput(attrs={'placeholder': '年龄',
                                                            'class': 'form-control'}))

    tGender = fields.CharField(required=True,
                               error_messages={'required': '性别不能为空'},
                               widget=widgets.TextInput(attrs={'placeholder': '性别',
                                                               'class': 'form-control'}))

    tPhone = fields.CharField(required=True,
                              error_messages={'required': '手机号不能为空'},
                              widget=widgets.TextInput(attrs={'placeholder': '手机号',
                                                              'class': 'form-control'}))

    salary = fields.CharField(required=True,
                              error_messages={'required': '薪资不能为空'},
                              widget=widgets.TextInput(attrs={'placeholder': '薪资',
                                                              'class': 'form-control'}))

    teacher2user = fields.ChoiceField(required=True,
                                      error_messages={'required': '角色不能为空'},
                                      widget=widgets.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher2user'].choices = models.UserType.objects.values_list('uId', 'role')


class BanJiForm(Form):
    bName = fields.CharField(required=True,
                             error_messages={'required': '班级名不能为空'},
                             widget=widgets.TextInput(attrs={'placeholder': '班级名',
                                                             'class': 'form-control'}))

    banji2teacher = fields.MultipleChoiceField(required=True,
                                               error_messages={'required': '至少有一名老师'},
                                               widget=widgets.SelectMultiple(attrs={'class': 'form-control'}))

    banZhuRen = fields.ChoiceField(required=True,
                                   error_messages={'required': '必须有一名班主任'},
                                   widget=widgets.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['banZhuRen'].choices = models.Teacher.objects.filter(teacher2user__role='classAdmin').values_list(
            'tId', 'tName')
        self.fields['banji2teacher'].choices = models.Teacher.objects.filter(
            teacher2user__role='teacher').values_list('tId', 'tName')