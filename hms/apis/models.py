from django.db import models
from django.utils import timezone

# Create your models here.


class classes(models.Model):
    # 班级表
    name=models.CharField(verbose_name="标题",max_length=32,unique=True)
    # token=models.CharField()
    # manager=models.ForeignKey
    
    # teachers=models.ManyToManyField("Teacher",null=True)



class Student(models.Model):
    # 学生表
    name=models.CharField("学生姓名",max_length=64)
    gender=models.SmallIntegerField(verbose_name="性别",choices=((1,"男"),(2,"女")))
    StuId=models.CharField("学号",max_length=64)
    password=models.CharField("密码",max_length=255)
    email=models.EmailField("邮箱",null=True)
    token=models.CharField("token",null=True,max_length=255)
    avatar=models.ImageField("头像",upload_to='User_Avatar',null=True)
    NowTime=models.DateTimeField("本次登录时间",null=True,auto_now=True)
    NowIp=models.GenericIPAddressField("本次登录ip",null=True)
    classes=models.ForeignKey("classes",on_delete=models.CASCADE,verbose_name="所属班级")
    ChangePassword=models.SmallIntegerField(verbose_name="是否已更改密码",choices=((1,"是"),(2,"否")),default=2)

class Teacher(models.Model):
    # 教师表
    name=models.CharField("教师姓名",max_length=64)
    StuId=models.CharField("学号",max_length=64)
    password=models.CharField("密码",max_length=255)
    email=models.EmailField("邮箱",null=True)
    token=models.UUIDField("token",null=True)
    avatar=models.ImageField("头像",upload_to='User_Avatar',null=True)
    NowTime=models.DateTimeField("本次登录时间",null=True,auto_now=True)
    NowIp=models.GenericIPAddressField("本次登录ip",null=True)
    classes=models.ManyToManyField("classes",verbose_name="任教的班级")

class ClassTasks(models.Model):
    #作业表
    token=models.CharField("作业uuid",max_length=255)
    title=models.CharField("作业标题",max_length=255)
    Subheading=models.TextField("小标题")
    StartTime=models.DateTimeField("开始时间",default=timezone.now)
    StopTime=models.DateTimeField("结束时间",default=timezone.now)
    Teacher=models.ForeignKey("Teacher",on_delete=models.CASCADE,verbose_name="任课教师")
    FileType=models.CharField("提示文件类型",null=True,max_length=64)
    FileUrl=models.FileField('提示文件',upload_to='homework_prompt',null=True)
    classes=models.ManyToManyField('classes',verbose_name="作业所属班级")


class ClassTasksSussess(models.Model):
    classtasks=models.ForeignKey('ClassTasks',on_delete=models.CASCADE,verbose_name='标记是哪个作业')
    Student=models.ManyToManyField('student',verbose_name="提交的学生")
    State=models.SmallIntegerField(verbose_name="标记作业状态",choices=((1,"已做"),(2,"未做")),default=2)
    PutTime=models.DateTimeField("提交时间",default=timezone.now)
    PutIp=models.GenericIPAddressField("提交时的ip",null=True)
    FileUrl=models.TextField("提交后的文件地址",null=True)
    Score=models.FloatField("成绩",max_length=255,default=-1,null=True)
    IsReplace=models.SmallIntegerField(verbose_name="是否有人代交",choices=((1,"是"),(2,"否")),null=True,default=2)
    ReplaceUser=models.CharField('代交人',null=True,max_length=32)
    Repetition=models.FloatField("重复率",max_length=255,null=True)

class ZyUploadTmp(models.Model):
    chunkNumber=models.CharField("第几片",max_length=255)
    chunkTotal=models.CharField("总片数",max_length=255)
    fileName=models.CharField("文件名",max_length=255)
    FileHash=models.CharField("文件hash",max_length=255)
    file=models.FileField("存储分片文件",upload_to='tmp',null=True)
    createtime=models.DateTimeField("上传时间",default=timezone.now)
# class Admin(models.Model):
#     # 管理员表


class EmailSerReg(models.Model):
    # 邮箱验证
    token=models.CharField("token",null=True,max_length=255)
    email=models.EmailField(verbose_name="邮箱")
    regnum=models.CharField("验证码",max_length=6,unique=True)
    send_time=models.DateTimeField(verbose_name="发送时间",default=timezone.now)
    per_id=models.CharField('用户id',max_length=255)


class TimeTables(models.Model):
    # 课程表
    classes=models.ForeignKey('classes',on_delete=models.CASCADE,verbose_name='所属班级')
    Student=models.ManyToManyField('student',verbose_name="所属学生")
    TimeList=models.JSONField(verbose_name="上课时间")
    StartData=models.DateField(verbose_name="学期开始时间")
    TimeTable=models.JSONField(verbose_name="课程数据")
