from django.http import FileResponse
from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from ext.auth import  *
from django.db.models import Q
from apis.models import (classes,Student,Teacher,ClassTasks,ClassTasksSussess,ZyUploadTmp,EmailSerReg,TimeTables)
from ext.SendEmail import (send_mail)
from ext.pinyin import (pinyin)
from django.utils import timezone
from rest_framework import exceptions
import uuid
import hashlib
import shutil
import zipfile
import os
import random
import json


HomeWorkPath='homeworks/'
User_Avatar='User_Avatar/'

# 班级序列化器
class ClassesSerializers(serializers.ModelSerializer):
    # 班级序列化器
    class Meta:
        model=classes
        fields='__all__'
# 学生数据表序列化器
class StudataSerializers(serializers.ModelSerializer):
    # 学生数据表序列化器
    # gender=serializers.CharField(source='get_gender_display')
    classes=serializers.CharField(source='classes.name')
    lastTime=serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",source='NowTime')
    lastIP=serializers.IPAddressField(source='NowIp')
    password=serializers.SerializerMethodField()
    class Meta:
        model=Student
        # fields='__all__'
        fields=['id','gender','StuId','classes',
                'email','lastIP','lastTime','name','password']
    def get_password(self,obj):
        return "******"

# 修改学生头像序列化校验
class AlterStuAvaterSerializers(serializers.ModelSerializer):
    avatar=serializers.FileField()
    class Meta:
        model=Student
        fields=['avatar']

    def update(self, instance, validated_data):
        # instance是要修改的对象
        # validated_data是校验过后的数据
        instance.avatar = validated_data.get('file')
        # 保存修改的数据
        instance.save()
        # 返回修改后的数据
        return instance

# 添加学生信息序列化校验器
class AddStudataSerializers(serializers.ModelSerializer):
    class Meta:
        model=Student
        # fields='__all__'
        fields=['gender','StuId','classes','email'
                ,'name','password']

    def validate_email(self, value):
        try:
            if len(value)>6:
                return value
        except:
            pass
        return None
    
    def update(self, instance, validated_data):
        # instance是要修改的对象
        # validated_data是校验过后的数据
        instance.gender = validated_data.get('gender')
        instance.StuId = validated_data.get('StuId')
        instance.classes = validated_data.get('classes')
        instance.email = validated_data.get('email')
        instance.name = validated_data.get('name')
        instance.password = validated_data.get('password')
        # 保存修改的数据
        instance.save()
        # 返回修改后的数据
        return instance


# 教师数据表序列化器
class TeadataSerializers(serializers.ModelSerializer):
    # 教师数据表序列化器
    stuID=serializers.CharField(source='StuId')
    classes=ClassesSerializers()
    lastTime=serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",source='NowTime')
    lastIP=serializers.IPAddressField(source='NowIp')
    password=serializers.SerializerMethodField()
    class Meta:
        model=Teacher
        # fields='__all__'
        fields=['id','stuID','classes',
                'email','lastIP','lastTime','name','password']
        
    def get_password(self,obj):
        return "******"

# 获取教师列表序列化器id和姓名
class GetTeadataSerializers(serializers.ModelSerializer):
    # 教师数据表序列化器
    class Meta:
        model=Teacher
        # fields='__all__'
        fields=['id','name']
        

#作业状态序列化器
class ClassTaskSussessSerializers(serializers.ModelSerializer):
    PutTime=serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    State=serializers.SerializerMethodField()
    Score=serializers.SerializerMethodField()
    IsReplace=serializers.SerializerMethodField()
    filetype=serializers.SerializerMethodField()
    class Meta:
        model=ClassTasksSussess
        fields=['id',"PutTime",'PutIp','Score','State','IsReplace','ReplaceUser'
                ,'Repetition','filetype','FileUrl']
    
    def get_State(self,obj):
        return '已交' if obj.State==1 else "未交"
    def get_Score(self,obj):
        return "未评"if obj.Score==-1 else obj.Score
    def get_IsReplace(self,obj):
        return "否" if obj.IsReplace==2 else "是"
    def get_filetype(self,obj):
        filetype='file'
        filename=obj.FileUrl.split('.')[-1]
        if 'doc' in filename:
            filetype="word"
        
        for i in ['jpg','png','gif']:
            if i in filename:
                filetype='img'
                break

        return filetype


#作业详情序列化器
class ClassTaskSerializers(serializers.ModelSerializer):
    classes=ClassesSerializers(many=True)
    # xx=serializers.CharField(source="")
    Score=serializers.SerializerMethodField()
    State=serializers.SerializerMethodField()
    FileUrl=serializers.SerializerMethodField()
    StartTime=serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    StopTime=serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    Teacher=serializers.CharField(source='Teacher.name')
    class Meta:
        model=ClassTasks
        fields="__all__"

    def get_State(self,obj):
        stu_id=self.context.get("Stuid")
        tasksussess=obj.classtaskssussess_set.filter(Student=stu_id).first()
        if tasksussess:
            if tasksussess.State==1:
                return "已做"
        return "未做"
    def get_Score(self,obj):
        stu_id=self.context.get("Stuid")
        tasksussess=obj.classtaskssussess_set.filter(Student=stu_id).first()
        if tasksussess:
            if tasksussess.Score==-1 or tasksussess.Score==None:
                return "未评"
            return tasksussess.Score
        return ""
    def get_FileUrl(self,obj):
        url='/getzytestfile?token='+obj.token
        return url

# 作业列表序列化器 管理员
class ZylistSerializers(serializers.ModelSerializer):
    State=serializers.SerializerMethodField()
    FileUrl=serializers.SerializerMethodField()
    Teacher=serializers.CharField(source='Teacher.name')
    StartTime=serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    StopTime=serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    classes=serializers.SerializerMethodField()
    class Meta:
        model=ClassTasks
        # fields="__all__"
        fields=['token','title','Subheading','StartTime','StopTime',
                'Teacher','classes','FileType','FileUrl','State']

    def get_State(self,obj):
        # print(StopTime)
        if obj.StopTime<timezone.now():
             return "已过时"
        return "未过时"

    def get_classes(self,obj):
        class_list=[]
        for i in obj.classes.all():
            class_list.append(i.name)
        return ",".join(class_list)
    
    def get_FileUrl(self,obj):
        url='/getzytestfile?token='+obj.token
        return url
    
# 添加作业时的序列化器
class AddZylistSerializers(serializers.ModelSerializer):
    token=serializers.CharField()

    classes=serializers.ListField()
    FileType=serializers.CharField(required=False)
    FileUrl=serializers.FileField(required=False)
    StartTime=serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    StopTime=serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    
    class Meta:
        model=ClassTasks
        fields="__all__"
        # fields=['token','title','Subheading','StartTime','StopTime',
        #         'Teacher','classes','FileType','FileUrl']
        
    def validate_token(self,value):
        token=uuid.uuid1()
        return token

    def validate_classes(self, value):
        try:
            id=value[0].split(',')
            int_id= [int(item) for item in id]
        except:
            raise exceptions.ValidationError({'code':10014,'msg':"班级错误"})
        return int_id

# 编辑作业时的序列化器
class EditZylistSerializers(serializers.ModelSerializer):
    class Meta:
            model=ClassTasks
            fields="__all__"
    def update(self, instance, validated_data):
        # instance是要修改的对象
        # validated_data是校验过后的数据
        instance.title = validated_data.get('title')
        instance.Subheading = validated_data.get('Subheading')
        instance.StartTime = validated_data.get('StartTime')
        instance.StopTime = validated_data.get('StopTime')
        instance.Teacher = validated_data.get('Teacher')
        instance.FileType = validated_data.get('FileType')
        instance.FileUrl = validated_data.get('FileUrl')
        instance.classes = validated_data.get('classes')
        # 保存修改的数据
        instance.save()
        # 返回修改后的数据
        return instance


#作业完成记录的序列化器

class ClassTaskSucSerializers(serializers.Serializer):
    token=serializers.SerializerMethodField()
    class Meta:
            fields=['token']
    

    def get_token(self,obj):
        token=obj.classtaskssussess_set.filter(classtasks_id=obj.classes_id).first().token
        if not token:
            return token
        return None


#课程表序列化器
class TimeTablesSerializers(serializers.ModelSerializer):
    class Meta:
        model=TimeTables
        fields="__all__"



# 登录校验
class Login(APIView):
    # 登录校验
    def post(self,request):
        username=request.data.get('username')
        password=request.data.get('password')

        # print(username,password)

        user_obj=Student.objects.filter(StuId=username,password=password).first()
        if user_obj:
            if user_obj.ChangePassword==2:
                return Response({'code':10000,'data':{'msg':'请修改默认密码','token':''}})
            token=str(uuid.uuid4())
            user_obj.token=token
            user_obj.NowIp=self.get_visitor_ip(request)
            user_obj.save()
            return Response({'code':10000,'data':{'token':token,'username':user_obj.name}})
    
        tea_obj=Teacher.objects.filter(StuId=username,password=password).first()
        if tea_obj:
            token=str(uuid.uuid4())
            tea_obj.token=token
            tea_obj.NowIp=self.get_visitor_ip(request)
            tea_obj.save()
            return Response({'code':10000,'data':{'token':token,'username':tea_obj.name}})
        return Response({'code':10001,'msg':'用户名或密码错误'})


    def get_visitor_ip(self, request):
        # 获取访问者ip
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class LoginAlterpasswdSerializers(serializers.Serializer):
    stuid=serializers.CharField(max_length=64)
    oldpasswd=serializers.CharField(max_length=255)
    newpasswd=serializers.CharField(max_length=255)
    newtwopasswd=serializers.SerializerMethodField()


    def get_newtwopasswd(self,obj):
        # print(obj)
        if obj.get("newpasswd")==obj.get("newtwopasswd"):
            return obj.get("newtwopasswd")
        raise exceptions.ValidationError({'code':10014,'msg':"两次密码不一致"})
# 第一次登录修改密码
class LoginAlterpasswd(APIView):
    def post(self,request):
        # 
        login_ser=LoginAlterpasswdSerializers(instance=request.data)
        # print(login_ser.data)
        stuid=login_ser.data.get("stuid")
        password=login_ser.data.get("oldpasswd")
        newpassword=login_ser.data.get("newtwopasswd")
        # print(newpassword)
        stu_obj=Student.objects.filter(StuId=stuid,password=password).first()
        if stu_obj:
            if stu_obj.ChangePassword==1:
                return Response({'code':10000,'data':{'msg':'账号初始密码已被修改'}})
            Student.objects.filter(StuId=stuid,password=password).update(password=newpassword,ChangePassword=1)
            return Response({'code':10000,'data':{'msg':'success'}})
        return Response({'code':10001,'msg':'用户名或密码错误'})

# 邮箱校验序列化器
class AddEmailSerializers(serializers.Serializer):
    email=serializers.EmailField()
    email_msg=serializers.CharField(max_length=6)


# 绑定邮箱
class AddEmail(APIView):
    authentication_classes=[TwoStudentAuthentication,TeacherAuthentication]
    def post(self,request):
        print(request.data)
        addemail_obj=AddEmailSerializers(instance=request.data)
        if not addemail_obj.data:
            return Response({'code':10010,'msg':'数据获取失败'})

        user=True   #true学生    false教师
        usertoken=Student.objects.filter(id=request.auth,name=request.user).first()
        if not usertoken:
            usertoken=Teacher.objects.filter(id=request.auth,name=request.user).first()
            user=False
        if not usertoken:
            return Response({'code':10010,'msg':"您的账户存在问题！"})
        
        email=addemail_obj.data.get('email','')
        email_reg=addemail_obj.data.get('email_msg','')
        # print(email_reg)
        email_obj=EmailSerReg.objects.filter(token=usertoken.token,email=email,regnum=email_reg).order_by('-send_time').first()

        # print(email_obj)

        if not email_obj:
            # EmailSerReg.objects.filter(token=usertoken.token,email=email,regnum=email_reg).delete()
            return Response({'code':10010,'msg':'验证码无效'})
        
        send_time=email_obj.send_time
        now_time=timezone.now()
        if (now_time-send_time).seconds>1800:
            EmailSerReg.objects.filter(token=usertoken.token,email=email,regnum=email_reg).delete()
            return Response({'code':10012,'msg':'验证码失效'})
        # print(user)

        ## 删除验证码记录
        EmailSerReg.objects.filter(token=usertoken.token,email=email,regnum=email_reg).delete()

        if user:
            stu_obj=Student.objects.filter(email=email).first()
            if stu_obj:
                return Response({'code':10012,'msg':'邮箱已被使用'})
            
            Student.objects.filter(token=usertoken.token,id=request.auth).update(email=email)
        else:
            tea_obj=Teacher.objects.filter(email=email).first()
            if tea_obj:
                return Response({'code':10012,'msg':'邮箱已被使用'})
            Teacher.objects.filter(token=usertoken.token,id=request.auth).update(email=email)

        
        return Response({'code':10000,'data':{'state':'ok'}})

# 发用邮箱验证码校验序列化器
class SendEmailMsgSerializers(serializers.Serializer):
    email=serializers.EmailField()

# 发送邮箱验证码
class SendEmailMsg(APIView):
    authentication_classes=[TwoStudentAuthentication,TeacherAuthentication]
    def get(self,request):
        email_ser=SendEmailMsgSerializers(instance=request.query_params)
        email=email_ser.data.get('email','')

        if (not email_ser) or (email==''):
            return Response({'code':10025,'msg':"邮箱格式有误"})


        usertoken=Student.objects.filter(id=request.auth,name=request.user).first()
        if not usertoken:
            usertoken=Teacher.objects.filter(id=request.auth,name=request.user).first()
        if not usertoken:
            return Response({'code':10010,'msg':"您的账户存在问题！"})


        email_obj=EmailSerReg.objects.filter(token=usertoken.token,email=email).order_by('-send_time').first()

        if email_obj:
            send_time=email_obj.send_time
            now_time=timezone.now()
            if (now_time-send_time).seconds<1800:
                return Response({'code':10000,'data':{'state':'ok'}})
            EmailSerReg.objects.filter(token=usertoken.token,email=email).delete()

        while True:
            # 保障验证码唯一
            regnum=random.randint(100000,999999)
            serreg_obj=EmailSerReg.objects.filter(regnum=regnum).all()
            if not serreg_obj:
                break


        state=send_mail(f"你的验证码是{regnum}",email,
                  "来自作业系统的验证码",request.user)
        if not state:
            return Response({'code':10025,'msg':"验证码发送失败，请联系管理员"})

        EmailSerReg.objects.create(token=usertoken.token,
                                   email=email,
                                   regnum=regnum,
                                   per_id=request.user+str(request.auth))

        

        return Response({'code':10000,'data':{'state':'ok'}})

# 发用邮箱忘记密码验证码校验序列化器
class SendForgetEmailMsgSerializers(serializers.Serializer):
    email=serializers.EmailField()
    stuid=serializers.SerializerMethodField()

    def get_stuid(self,value):
        try:
            if len(value.get('stuid'))>6:
                num=int(value.get('stuid'))
            else:
                raise NotFound('学号应是6为以上')            
        except:
            raise NotFound('学号应是数字')
        
        return num
        

# 发送邮箱忘记密码验证码
class SendForgetEmailMsg(APIView):
    def post(self,request):
        send_ser=SendForgetEmailMsgSerializers(instance=request.data)
        if not send_ser.data:
            return Response({'code':10000,'data':{'msg':'学号为空或邮箱不合规'}})

        stuid=send_ser.data.get('stuid')
        email=send_ser.data.get('email')

        stu_obj=Student.objects.filter(StuId=stuid,email=email).first()
        if not stu_obj:
            stu_obj=Teacher.objects.filter(StuId=stuid,email=email).first()
        if not stu_obj:
            return Response({'code':10000,'data':{'msg':'找不到与之匹配的学号和邮箱的账号'}})


        while True:
            # 保障验证码唯一
            regnum=random.randint(100000,999999)
            serreg_obj=EmailSerReg.objects.filter(regnum=regnum).all()
            if not serreg_obj:
                break
        
        state=send_mail(f"你正在操作找回密码,如不是本人操作可不必在意,你的验证码是{regnum}",email,
                  "找回密码",stu_obj.name)
        if not state:
            return Response({'code':10025,'msg':"验证码发送失败，请联系管理员"})

        EmailSerReg.objects.create(token=stu_obj.token,
                                   email=email,
                                   regnum=regnum,
                                   per_id=stuid)
        
        return Response({'code':10000,'data':{'msg':'ok'}})


# 发用邮箱忘记密码验证码校验序列化器
class EmailToAlterpasswdSerializers(serializers.Serializer):
    email=serializers.EmailField()
    stuid=serializers.SerializerMethodField()
    email_reg=serializers.SerializerMethodField()

    def get_stuid(self,value):
        try:
            if len(value.get('stuid'))>6:
                num=int(value.get('stuid'))
            else:
                raise NotFound('学号应是6为以上')            
        except:
            raise NotFound('学号应是数字')
        return num

    def get_email_reg(self,value):
        try:
            if len(value.get('email_reg'))==6:
                num=int(value.get('email_reg'))
            else:
                raise NotFound('验证码应是6为')            
        except:
            raise NotFound('学号应是数字')
        return num

# 修改密码为默认密码
class EmailToAlterpasswd(APIView):
    def post(self,request):
        send_ser=EmailToAlterpasswdSerializers(instance=request.data)
        if not send_ser.data:
            return Response({'code':10010,'msg':'数据不合规'})

        stuid=send_ser.data.get('stuid')
        email=send_ser.data.get('email')
        regnum=send_ser.data.get('email_reg')

        email_reg=EmailSerReg.objects.filter(per_id=stuid,email=email,regnum=regnum).first()

        if not email_reg:
            return Response({'code':10010,'msg':'验证码错误'})
        

        send_time=email_reg.send_time
        now_time=timezone.now()
        if (now_time-send_time).seconds>1800:
            EmailSerReg.objects.filter(per_id=stuid,email=email,regnum=email_reg).delete()
            return Response({'code':10012,'msg':'验证码失效'})


        user=True #true学生   false教师

        stu_obj=Student.objects.filter(StuId=stuid,email=email).first()
        if not stu_obj:
            user=False
            stu_obj=Teacher.objects.filter(StuId=stuid,email=email).first()
        if not stu_obj:
            return Response({'code':10030,'msg':'找不到与之匹配的学号和邮箱的账号'})


        

        name=pinyin(stu_obj.name)
        passwd=hashlib.md5((name).encode()).hexdigest()
        token=str(uuid.uuid1())
        if user:
            Student.objects.filter(StuId=stuid,email=email).update(token=token,password=passwd)

        EmailSerReg.objects.filter(per_id=stuid,email=email,regnum=regnum).delete()

        return Response({'code':10000,'data':{'msg':'ok','token':token,'username':stu_obj.name}})


#获取菜单，导航信息
class getmenu(APIView):
    authentication_classes=[TwoStudentAuthentication,TeacherAuthentication]
    def get(self,request):
        tea_obj=Teacher.objects.filter(id=request.auth,name=request.user).first()
        if tea_obj:
            return Response({'code':10000,'data':[{
                "path": "/home",
                "name": "home",
                "label": "主页",
                "icon": "house",
                "url": "home",'meta':{'title':'主页'}
            },{
                "path": "/user",
                "name": "user",
                "label": "用户管理",
                "icon": "user",
                "url": "User/User",'meta':{'title':'用户管理'}
            },{
                "path": "/glzylist",
                "name": "glzylist",
                "label": "作业管理",
                "icon": "Notebook",
                "url": "Zylist/glzylist",'meta':{'title':'作业管理'}
            },{
                "path": "/PersonalCenter",
                "name": "PersonalCenter",
                "label": "个人中心",
                "icon": "Postcard",
                "url": "User/PersonalCenter",'meta':{'title':'个人中心'}
            }]})
        return Response({'code':10000,'data':[{
        "path": "/home",
        "name": "home",
        "label": "主页",
        "icon": "house",
        "url": "home",'meta':{'title':'主页'}
      },{
          "path": "/zylist",
        "name": "zylist",
        "label": "作业列表",
        "icon": "List",
        "url": "Zylist/zylist",'meta':{'title':'作业列表'}
      },{
          "path": "/kebiao",
        "name": "kebiao",
        "label": "在线课表",
        "icon": "Tickets",
        "url": "phone/kebiao",'meta':{'title':'在线课表'}
      },{
          "path": "/PersonalCenter",
        "name": "PersonalCenter",
        "label": "个人中心",
        "icon": "Postcard",
        "url": "User/PersonalCenter",'meta':{'title':'个人中心'}
      }]})

# 获取班级列表
class getClasses(APIView):
    authentication_classes=[TwoStudentAuthentication,TeacherAuthentication]
    def get(self,request):
        classes_obj=classes.objects.filter().all()
        classes_ser=ClassesSerializers(instance=classes_obj,many=True)
        return Response({'code':10000,'data':{"list":classes_ser.data}})

#获取作业班级
class getZyClassesInfo(APIView):
    authentication_classes=[TeacherAuthentication]
    def get(self,request):
        token=request.query_params.get('token',None)
        if not token:
            return Response({"code":10021,'msg':'无法获取班级信息'})
        Classes=ClassTasks.objects.filter(token=token).first()
        # classes_id=Classes.classes_set
        # print()
        class_ser=ClassesSerializers(instance=Classes.classes.all(),many=True)
        print(class_ser.data)
        return Response({"code":10000,'data':class_ser.data})


# 获取教师列表
class getTeacher(APIView):
    authentication_classes=[TeacherAuthentication]
    def get(self,reuqest):
        tea_obj=Teacher.objects.filter().all()
        tea_ser=GetTeadataSerializers(instance=tea_obj,many=True)
        return Response({'code':10000,'data':{'list':tea_ser.data}})

#获取学生账号信息    
class StuData(APIView):
    authentication_classes=[TeacherAuthentication]
    def get(self,request):
        #获取前端发来的数据
        # print()
        username=request.query_params.get('name')
        page=request.query_params.get('page')
        try:
            page=int(page)-1
        except:
            page=0
        # 处理从那个地方开始查询和结束
        page_size=11#定义每页的长度
        page_start=page*page_size
        page_end=(page+1)*page_size

        return_data={'count':0,'list':[]}#定义返回的数据
        #准备搜索时需要用到的数据
        data_dict={}

        ter_obj=Teacher.objects.filter(id=request.auth).first()
        ids=[x.id for x in ter_obj.classes.all()]
        # print(ids)
        if username:
          data_dict["name__contains"]=username
        data_dict["classes__in"]=ids

        

        #查询时处理时间格式化的问题，并解决分页问题,和搜索问题 
        #下方注释的代码可以实现orm查询时进行时间格式化，但是此方法可能带来性能问题，后面采用序列化器解决该问题

        stu_obj=Student.objects.filter(**data_dict).all()
        



        #处理要返回的数据
        return_data['count']=stu_obj.count()
        #使用序列化器进行序列化
        stud_ser=StudataSerializers(instance=stu_obj[page_start:page_end],many=True)

        print(stud_ser.data)
        return_data['list']=stud_ser.data
          
        return Response({"code":10000,'data':return_data})


# 获取个人信息和角色
class UserInfo(APIView):
    authentication_classes=[TwoStudentAuthentication,TeacherAuthentication]
    def get(self,request):
        stu_obj= Teacher.objects.filter(name=request.user,id=request.auth).first()
        identity="教师"
        if not stu_obj:
            identity="学生"
            stu_obj= Student.objects.filter(name=request.user,id=request.auth).first()
        
        if not stu_obj:
            return Response({'code':10005,'msg':'获取个人信息失败'})


        return Response({'code':10000,'data':{'name':stu_obj.name,'identity':identity}})

# 获取学生头像
class getUserAvatar(APIView):
    authentication_classes=[TwoStudentAuthentication,TeacherAuthentication]
    def get(self,request):
        
        stu_obj= Teacher.objects.filter(name=request.user,id=request.auth).first()
        if not stu_obj:
            stu_obj= Student.objects.filter(name=request.user,id=request.auth).first()


        if stu_obj.avatar:
            return FileResponse(stu_obj.avatar.file)


        return FileResponse(open('./User_Avatar/test.jpg','rb'))
        # return Response({'code':10000,'msg':'ok'})

# 修改学生或老师头像
class AlterUserAvatar(APIView):
    authentication_classes=[TwoStudentAuthentication,TeacherAuthentication]
    def post(self,request):
        
        stu_obj= Student.objects.filter(name=request.user,id=request.auth).first()

        if not stu_obj:
            stu_obj= Teacher.objects.filter(name=request.user,id=request.auth).first()
            if not stu_obj:
                return Response({'code':10005,'msg':'修改失败'})

        # 更新文件时需要，使用save而不能使用update
        try:
            stu_obj.avatar.delete()
            stu_obj.avatar=request.data.get('file')
            stu_obj.save()
        except:
            return Response({'code':10005,'msg':'修改失败'})
        
        return Response({'code':10000,'data':{'msg':'暂时无法上传头像'}})



# 获取本次登录的时间和本次登录的ip
class UserLoginlog(APIView):
    authentication_classes=[TwoStudentAuthentication,TeacherAuthentication]
    def get(self,request):
        token=request.headers.get('token')
        #校验token是否为空，防止因为有些教师从不进行注册而发生越权的情况
        if not token:
          return Response({'code':10006,'msg':'获取个人信息失败'})
      
        stu_obj=Student.objects.filter(token=token).first()
        if stu_obj:
            stu_ser=StudataSerializers(instance=stu_obj)
            return Response({'code':10000,'data':{'nowip':stu_ser.data.get('lastIP'),'nowdatetime':stu_ser.data.get('lastTime')}})
        tea_obj=Teacher.objects.filter(token=token).first()
        if(tea_obj):
            tea_ser=TeadataSerializers(instance=tea_obj)
            return Response({'code':10000,'data':{'nowip':tea_ser.data.get('lastIP'),'nowdatetime':tea_ser.data.get('lastTime')}})

        return Response({'code':10006,'msg':'获取个人信息失败'})
#添加学生信息
class addStuData(APIView):
    authentication_classes=[TeacherAuthentication]
    def post(self,request):
        email=request.data.get("email",None)
        if email=='':
            try:
                request.data['email']=None
            except:
                pass

        addstu_obj=AddStudataSerializers(data=request.data)
        if not addstu_obj.is_valid():
            # print(addstu_obj.errors)
            msg=list(addstu_obj.errors.values())[0][0]
            return Response({'code':10008,'msg':msg})
        # 保存到数据库
        addstu_obj.save()
        return Response({'code':10000,'data':{'msg':'添加成功'}})

# 修改学生信息
class editStuData(APIView):
    authentication_classes=[TeacherAuthentication]
    def post(self,request):
        # 处理容易引起序列化器报错的字段
        email=request.data.get("email",None)
        id=request.data.get('id',None)
        if email=='':
            try:
                request.data['email']=None
            except:
                pass
        if not id:
            return Response({"code":10009,'msg':'修改失败,无用户标志信息'})
        stu_obj=Student.objects.filter(id=id).first()
        stu_ser=AddStudataSerializers(data=request.data,instance=stu_obj)
        if not stu_ser.is_valid():
            # print(addstu_obj.errors)
            msg=list(stu_ser.errors.values())[0][0]
            return Response({'code':10008,'msg':msg})
        
        stu_ser.save()
        return Response({"code":10000,'data':{'msg':'修改成功'}})
#删除学生信息
class deleteStuData(APIView):
    authentication_classes=[TeacherAuthentication]
    def get(self,request):
        id=request.query_params.get('id',None)
        if not id:
            return Response({"code":10009,'msg':'修改失败,无用户标志信息'})
        try:
            Student.objects.filter(id=id).first().delete()
        except:
            return Response({"code":10009,'msg':'用户数据有误'})
        return Response({"code":10000,'data':{'msg':'删除成功'}})

#获取作业列表
class getZyList(APIView):
    authentication_classes=[StudentAuthentication]
    def get(self,request):
        # print(request.query_params)
        title=request.query_params.get('title',"")
        page=request.query_params.get('page')
        try:
            page=int(page)-1
        except:
            page=0
        # 处理从那个地方开始查询和结束
        page_size=11#定义每页的长度
        page_start=page*page_size
        page_end=(page+1)*page_size

        return_data={'count':0,'list':[]}#定义返回的数据
        #准备搜索时需要用到的数据
        data_dict={}
        if title:
          data_dict["title__icontains"]=title
          data_dict["Subheading__icontains"]=title
        # 获取班级
        Class=Student.objects.filter(id=request.auth).first().classes
        classtask=Class.classtasks_set.filter(Q(title__icontains=title)|Q(Subheading__icontains=title)).all().order_by('-StopTime')
         #处理要返回的数据
        return_data['count']=classtask.count()
        #对数据进行分页
        classtasks=classtask[page_start:page_end]
        # #使用序列化器进行序列化
        classtask_ser=ClassTaskSerializers(instance=classtasks,many=True,context={'Stuid':request.auth})
        return_data['list']=classtask_ser.data
        return Response({"code":10000,'data':return_data})


# 管理员获取作业列表
class getGlZyList(APIView):
    authentication_classes=[TeacherAuthentication]
    def get(self,request):
        #获取前端发来的数据
        # print()
        title=request.query_params.get('title',"")
        page=request.query_params.get('page')
        try:
            page=int(page)-1
        except:
            page=0
        # 处理从那个地方开始查询和结束
        page_size=11#定义每页的长度
        page_start=page*page_size
        page_end=(page+1)*page_size

        return_data={'count':0,'list':[]}#定义返回的数据
        #准备搜索时需要用到的数据
        ter_obj=Teacher.objects.filter(id=request.auth).first()
        ids=[x.id for x in ter_obj.classes.all()]
        # print(ids)
        data_dict={}
        if title:
        #   data_dict["Subheading__icontains"]=title
          data_dict["title__contains"]=title
        data_dict["classes__in"]=ids
        
        #查询时处理时间格式化的问题，并解决分页问题,和搜索问题 
        #下方注释的代码可以实现orm查询时进行时间格式化，但是此方法可能带来性能问题，后面采用序列化器解决该问题
        #Q(title__icontains=title)|Q(Subheading__icontains=title)   多查询条件
        zy_obj=ClassTasks.objects.filter(**data_dict).distinct().all().order_by('-StopTime')
        #处理要返回的数据
        return_data['count']=zy_obj.count()
        #使用序列化器进行序列化
        zy_ser=ZylistSerializers(instance=zy_obj[page_start:page_end],many=True)



        # print(zy_ser.data)
        return_data['list']=zy_ser.data

        return Response({"code":10000,"data":return_data})

# 管理员查看作业详情
class getGlZyInfo(APIView):
    authentication_classes=[TeacherAuthentication]
    def get(self,request):

        return Response({"code":10000,"data":"ok"})
    

#获取作业详情
class getZyInfo(APIView):
    authentication_classes=[TwoStudentAuthentication,TeacherAuthentication]
    def get(self,request):
        
        token=request.query_params.get('token',None)
        if not token:
            return Response({'code':10010,'msg':'作业详细信息获取错误！'})

        zy_obj=ClassTasks.objects.filter(token=token).first()
        # print(zy_obj)
        zy_ser=ClassTaskSerializers(instance=zy_obj)
        if zy_ser.data:
            return Response({'code':10000,'data':zy_ser.data})
        return Response({'code':10010,'msg':'作业详细信息获取错误！'})


# 获取用户邮箱
class getUserEmail(APIView):
    authentication_classes=[TwoStudentAuthentication,TeacherAuthentication]
    def get(self,request):
        per_obj=Student.objects.filter(name=request.user,id=request.auth).first()
        if not per_obj:
            per_obj=Teacher.objects.filter(name=request.user,id=request.auth).first()
        if not per_obj:
            return Response({'code':10010,'msg':'邮箱获取错误！'})
        email=per_obj.email
        return Response({'code':10000,'data':{'email':email}})


# 上传文件的校验序列化器
class ZyuploadSerializers(serializers.ModelSerializer):    
    class Meta:
        model=ZyUploadTmp
        fields='__all__'


class ZymergeSerializers(serializers.Serializer):
    chunkTotal=serializers.CharField()
    fileName=serializers.CharField()
    FileHash=serializers.CharField()
    ClassTaskToken=serializers.CharField()
    randomNum=serializers.CharField()

# 上传文件
class getZyUpload(APIView):
    authentication_classes=[StudentAuthentication]
    def get(self,request):
        # 合并用户上传的分片数据
        zy_ser=ZymergeSerializers(data=request.query_params)
        if not zy_ser.is_valid():
            raise NotFound({'code':20000,'msg':'文件合并失败,无法读取您上传的东西！！！'})
        fileName=zy_ser.data.get("fileName")
        filehash=zy_ser.data.get("FileHash")
        chunkTotal=zy_ser.data.get('chunkTotal')
        ClassTaskToken=zy_ser.data.get('ClassTaskToken')
        randomNum=zy_ser.data.get('randomNum')
        hash=hashlib.md5((ClassTaskToken+request.user+randomNum).encode()).hexdigest()
        zy_tmp_obj=ZyUploadTmp.objects.filter(FileHash=hash).all()
        # print(zy_tmp_obj,hash,randomNum)
        if not zy_tmp_obj:
            raise NotFound({'code':20000,'msg':'文件合并失败,因为没有找到你上传的文件,请尝试重新上传'})
        
        if zy_tmp_obj.count()!=int(chunkTotal):
            raise NotFound({'code':20000,'msg':'文件合并失败,因为上传时丢失了部分文件'})

        classtask=ClassTasks.objects.filter(token=ClassTaskToken).first()
        ip=self.get_visitor_ip(request)

        stoptime=classtask.StopTime
        if stoptime<timezone.now():
            for i in zy_tmp_obj:
                i.file.delete()
            zy_tmp_obj.delete()
            raise NotFound({'code':20000,'msg':'提交失败,已经过了提交时间'})
        StuId=Student.objects.filter(id=request.auth).first().StuId
        fileName=HomeWorkPath+f"{classtask.id}/"+StuId+request.user+"."+fileName.split('.')[-1]
        
        if os.path.exists(fileName):
            os.remove(fileName)
        
        for i in zy_tmp_obj:
            try:
                shutil.copyfileobj(i.file,open(fileName,"ab"))
            except:
                raise NotFound({'code':20000,'msg':'合并数据时出错,请联系管理员'})
            i.file.delete()
        zy_tmp_obj.delete()
        

        # 判断合并后的数据的正确性
        with open(fileName,'rb') as f:
            end_hash=hashlib.md5(f.read()).hexdigest()
        if filehash!=end_hash:
            raise NotFound({'code':20000,'msg':'提交失败,文件完整性校验失败'})

        # 在数据库中存储已完成作业记录
        classstate_obj=ClassTasksSussess.objects.create(classtasks_id=classtask.id,
                                         PutIp=ip,
                                         State=1,
                                         FileUrl=fileName)
        classstate_obj.Student.set([request.auth])



        return Response({'code':10000,'msg':'上传成功'})

    def post(self,request):
        # 检验用户上传的东西
        zy_ser=ZyuploadSerializers(data=request.data)
        if not zy_ser.is_valid():
            raise NotFound({'code':20000,'msg':'无法读取您上传的东西！！！'})
        zy_ser.save()
        # 从序列化器中拿到目标字段的值
        chunkNumber=zy_ser.data.get('chunkNumber')
        chunkTotal=zy_ser.data.get('chunkTotal')

        try:
            already_sum='{:.2f}%'.format(int(chunkNumber)/int(chunkTotal)*100)
        except:
            already_sum='100%'
        return Response({'code':10000,'data':{'progress':already_sum}})
    
    def get_visitor_ip(self, request):
        # 获取访问者ip
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


# 删除已做作业
class getDelZy(APIView):
    authentication_classes=[StudentAuthentication]
    def get(self,request):
        # 获取需要删除的作业token
        taskToken=request.query_params.get('token',None)
        if not taskToken:
            return Response({'code':20000,'msg':'获取作业token失败'})
        # 获取需要删除的作业的那条具体条目
        Task_obj=ClassTasks.objects.filter(token=taskToken).first()

        if not Task_obj:
            return Response({'code':20000,'msg':'未找到本条作业信息'})
        
        # 获取用户上传作业的记录信息
        classtasksu=Task_obj.classtaskssussess_set.filter(Student=request.auth).first()

        if not classtasksu:
            return Response({'code':20000,'msg':'未找到本条作业信息'})

        # 获取当前路径并和并数据库的路径，再调用os的删除模块进行数据删除，如果删除中报错则返回错误状态码
        filename=os.getcwd()+"/"+classtasksu.FileUrl
        try:
            os.remove(filename)
            classtasksu.delete()
        except:
            return Response({'code':20000,'msg':'删除失败,请及时联系管理员进行删除'})
        return Response({'code':10000,'data':{"msg":'删除成功'}})
    

# 查看作业
class getViewZy(APIView):
    authentication_classes=[StudentAuthentication]
    def get(self,request):
        # 获取需要删除的作业token
        taskToken=request.query_params.get('token',None)
        if not taskToken:
            return Response({'code':20000,'msg':'获取作业token失败'})
        # 获取需要删除的作业的那条具体条目
        Task_obj=ClassTasks.objects.filter(token=taskToken).first()

        if not Task_obj:
            return Response({'code':20000,'msg':'未找到本条作业信息'})
        
        # 获取用户上传作业的记录信息
        classtasksu=Task_obj.classtaskssussess_set.filter(Student=request.auth).first()

        if not classtasksu:
            return Response({'code':20000,'msg':'未找到本条作业信息'})

        # 获取当前路径并和并数据库的路径，再调用os的删除模块进行数据删除，如果删除中报错则返回错误状态码
        filename=os.getcwd()+"/"+classtasksu.FileUrl
        if not os.path.isfile(filename):
            return Response({'code':20000,'msg':'作业原始文件被删除'})

        filetype='file'
        if '.doc' in filename:
            filetype="word"
        
        for i in ['.jpg','.png','.gif']:
            if i in filename:
                filetype='img'
                break

        return Response({'code':10000,'data':{"msg":'浏览成功','filetype':filetype}})

# 下载作业
class getMyZy(APIView):
    authentication_classes=[StudentAuthentication]

    def get(self,request):
        # 获取需要删除的作业token
        taskToken=request.query_params.get('token',None)
        if not taskToken:
            return Response({'code':20000,'msg':'获取作业token失败'})
        # 获取需要删除的作业的那条具体条目
        Task_obj=ClassTasks.objects.filter(token=taskToken).first()
        if not Task_obj:
            return Response({'code':20000,'msg':'未找到本条作业信息'})
        # 获取用户上传作业的记录信息
        classtasksu=Task_obj.classtaskssussess_set.filter(Student=request.auth).first()
        if not classtasksu:
            return Response({'code':20000,'msg':'未找到本条作业信息'})
        # 获取当前路径并和并数据库的路径，再调用os的删除模块进行数据删除，如果删除中报错则返回错误状态码
        filename="./"+classtasksu.FileUrl
        print(filename)

        return FileResponse(open(filename,'rb'))
    

# 添加作业  老师
class addzy(APIView):
    authentication_classes=[TeacherAuthentication]
    def post(self,request):
        # 把数据丢进序列化器中
        addzy_ser=AddZylistSerializers(data=request.data)
        
        if not addzy_ser.is_valid():
            # 验证失败则返回错误
            return Response({'code':10013,'msg':'添加失败,请检查提交的数据'})

        
        # 数据验证成功则添加到数据库中
        token=addzy_ser.validated_data.get('token')
        addzy_ser.save()
        # 创建作业存档
        id=ClassTasks.objects.filter(token=token).first().id
        if id:
            os.mkdir('./homeworks/'+str(id))
        return Response({'code':10000,'data':{'msg':'添加成功'}})

        

#删除作业  老师
class delzy(APIView):
    authentication_classes=[TeacherAuthentication]
    def get(self,request):
        token=request.query_params.get('token')
        # print(token)
        zydata_obj=ClassTasks.objects.filter(token=token).first()
        if zydata_obj:
            zydata_obj.delete()
            return Response({'code':10000,'data':{'msg':'删除成功'}})
        return Response({'code':10013,'msg':'删除失败'})
    

# 返回作业示例文件  老师
class GetzyTestFile(APIView):
    authentication_classes=[TwoStudentAuthentication,TeacherAuthentication]
    def get(self,request):
        token=request.query_params.get('token')
        print(token)
        zy_obj=ClassTasks.objects.filter(token=token).first()
        print(zy_obj)
        if zy_obj:
        # return exceptions.NotFound()
            return FileResponse(zy_obj.FileUrl)
        return Response({'code':10001,'msg':'无法返回'})   

# 编辑作业(管理员)
class Editzy(APIView):
    authentication_classes=[TeacherAuthentication]
    def post(self,request):
        token=request.data.get('token',None)
        if not token:
            return Response({'code':10008,'msg':'无法修改'})
        zy_obj=ClassTasks.objects.filter(token=token).first()
        zy_ser=AddZylistSerializers(data=request.data,instance=zy_obj)
        if not zy_ser.is_valid():
            print(zy_ser.errors)
            msg=list(zy_ser.errors.values())[0][0]
            return Response({'code':10008,'msg':msg})
        zy_ser.save()
        return Response({'code':10000,'data':{'msg':'ok'}})

# 获取班级所有成员的作业状态,包括没有提交的学生   
class GetGlzyinfo(APIView):
    authentication_classes=[TeacherAuthentication]
    def get(self,request):
        # print(request.query_params)
        token=request.query_params.get('token',None)
        class_id=request.query_params.get('id',None)

        if (not token) or (not class_id):
            return Response({'code':10017,'msg':'无法获取数据'})

        stu_obj=Student.objects.filter(classes_id=class_id).all()
        task_id=ClassTasks.objects.filter(token=token).first().id
        # print(dir(stu_obj[0]))
        # classtaskssussess_set
        if not task_id:
            return Response({'code':10017,'msg':'无法获取数据'})

        data_list=[]

        # print(stu_obj.count())
        for i in stu_obj:
            stu_ser=ClassTaskSussessSerializers(instance=i.classtaskssussess_set.filter(classtasks_id=task_id).first())
            # print(stu_ser.data)
            tis_data=stu_ser.data
            tis_data['name']=i.name
            tis_data['stu_id']=i.id
            if not tis_data.get('State',None):
                tis_data['State']="未交"
            data_list.append(tis_data)
            # print(tis_data)
        # data=[]
        # zy_obj=ClassTasks.objects.filter(token=token).first()
        # zy_id,zy_classes=zy_obj.id,zy_obj.classes
        # print(dir(zy_obj))
        # suc_sum=zy_obj.classtaskssussess_set.all()
        # zy_sus=ClassTasksSussess.objects(classtasks=zy_id).all().count()
        # stu_sum=Student.objects(classes=zy_classes).all().count()
        # print(suc_sum)
        # data=[{'classes':zy_classes,
        #        'count':zy_sus,
        #        'success':stu_sum}]
        # for i in zy_obj:
        #     print(i.classes)

        return Response({'code':10000,'data':data_list})


class GetGlstuzyinfo(APIView):
    authentication_classes=[TeacherAuthentication]
    def get(self,request):
        id=request.query_params.get('id',None)
        if not id:
            return Response({'code':10017,'msg':'无法获取数据'})

        stu_obj=ClassTasksSussess.objects.filter(id=id).first()

        if stu_obj.FileUrl:
            filename='./'+stu_obj.FileUrl
        
        return FileResponse(open(filename,'rb'))

        # return Response({'code':10000,'data':{'msg':'ok'}})

class DelGlstuzy(APIView):
    authentication_classes=[TeacherAuthentication]
    def get(self,request):
        id=request.query_params.get('id',None)
        if not id:
            return Response({'code':10017,'msg':'无法获取数据'})

        stu_obj=ClassTasksSussess.objects.filter(id=id).first()

        if stu_obj:
            stu_obj.delete()
            return Response({'code':10000,'data':{'msg':'ok'}})
        return Response({'code':100017,'msg':'删除失败'})


class GetGlstuzyZip(APIView):
    authentication_classes=[TeacherAuthentication]
    def get(self,request):
        classid=request.query_params.get('id',None)
        Tasktoken=request.query_params.get('Tasktoken',None)
        # print(classid,Tasktoken)
        if (not Tasktoken) or (not classid):
            return Response({'code':10017,'msg':'无法获取数据'})

        # print(classid,Tasktoken)
        # class_obj=ClassTasks.objects.filter(token=Tasktoken).first()
        # zydata_obj=class_obj.classtaskssussess_set.filter(classtasks=classid).all()
        stu_obj=Student.objects.filter(classes_id=classid).all()
        task=ClassTasks.objects.filter(token=Tasktoken).first()
        task_id,task_name=task.id,task.title
        if not task_id:
            return Response({'code':10017,'msg':'无法获取数据'})
        if not stu_obj:
            return Response({'code':10017,'msg':'无法获取数据'})

        ls=[]
        for i in stu_obj:
            file_ser=ClassTaskSussessSerializers(instance=i.classtaskssussess_set.filter(classtasks_id=task_id).first())
            # if not file_ser:
            file_url=file_ser.data.get('FileUrl',None)
            if file_url:
                ls.append(file_url)

        zip_path_name="./zyzip/"+str(task_name)+".zip"
        if os.path.exists(zip_path_name):
            os.remove(zip_path_name)
        
        for i in ls:
            with zipfile.ZipFile(zip_path_name,'a') as f:
                    f.write(i,i.split('/')[-1])

        # print(ls)
        # for i in zydata_obj:


        return FileResponse(open(zip_path_name,'rb'))
        # return Response({'code':10000,'data':{'msg':'ok'}})


class AlterStuPasswdSerializers(serializers.ModelSerializer):
    class Meta:
        model=Student

    def update(self, instance, validated_data):
        # instance是要修改的对象
        # validated_data是校验过后的数据
        instance.password = validated_data.get('newpassword')
        # 保存修改的数据
        instance.save()
        # 返回修改后的数据
        return instance
# 学生修改自己的密码
class AlterStuPasswd(APIView):
    authentication_classes=[StudentAuthentication]
    def post(self,request):
        print(request.user,request.auth)
        oldpasswd=request.data.get('oldpasswd',None)
        newpasswd=request.data.get('newpasswd',None)
        newtwopasswd=request.data.get('newtwopasswd',None)
        stu_obj=Student.objects.filter(id=request.auth).first()
        if stu_obj.password==hashlib.md5(oldpasswd.encode()).hexdigest():
            if (newpasswd==newtwopasswd) and len(newtwopasswd)>=6:
                Student.objects.filter(id=request.auth).update(password=hashlib.md5(newtwopasswd.encode()).hexdigest())
                return Response({'code':10000,'data':{'msg':'success'}})
        return Response({'code':10020,'msg':'更改失败'})



#作业状态序列化器
class CTSSerializers(serializers.ModelSerializer):
    PutTime=serializers.DateTimeField(format="%Y-%m-%d")
    class Meta:
        model=ClassTasksSussess
        fields=["PutTime"]

# 获取折线统计图的数据
class getCharData(APIView):
    authentication_classes=[TwoStudentAuthentication,TeacherAuthentication]
    def get(self,request):
        tea_obj=Teacher.objects.filter(id=request.auth,name=request.user).first()
        if tea_obj:
            return Response({  "code":10000,  "data":{    "orderData":{    "date":["2024-1-1","2024-1-1","2024-1-1","2024-1-1","2024-1-1","2024-1-1","2024-1-1"],    "data":[0,0,0,0,0,0,0]},    "messageData":[    {'title':'告全体用户书','time':'2024/6/20','msg':'感谢对本系统的支持,送你们最后一件礼物(本系统的源代码),源代码还未推送至开源社区请谨记该链接(https://github.com/lzq-hopego/homework-system),将在不久后可以下载,愿你们在未来的道路上，勇往直前，无惧风雨，始终怀揣着对生活的热爱和对梦想的执着，勇敢地闯荡人生的江湖。再见！','manager':'李展旗'},{'title':'增加在线课程表','time':'2024/5/14 23:30','msg':'此次更新修复了一些bug提高稳定性,新增了在线课表功能',"manager":'管理员-李展旗'},{'title':'作业系统更新','time':'2024/4/9 18:20','msg':'此次更新增加了绑定邮箱功能，和登录页面密码找回功能，找回后会重置密码至初始密码，初始密码为名字的拼音',"manager":'管理员-李展旗'},{"title":"关于作业系统更新为新版本的通知","time":'2024/3/18 11:09',"msg":'旧版本作业系统依旧保留，随时等待开源，旧版本因为不支持前后端分离，性能大打折扣，因此启用新版本，望周知',"manager":'管理员-李展旗'    },     ],  "userData":[{  "date":'周一',  "new":5,  "active":200},{  "date":'周二',  "new":5,  "active":200},{  "date":'周三',  "new":5,  "active":200},{  "date":'周四',  "new":5,  "active":200},{  "date":'周五',  "new":5,  "active":200},{  "date":'周六',  "new":5,  "active":200},{  "date":'周日',  "new":5,  "active":200},]}  })
    
        stu_obj=Student.objects.filter(id=request.auth).first()
        class_task_obj=stu_obj.classtaskssussess_set.filter().all()
        # print(class_task_obj)
        class_task_ser=CTSSerializers(instance=class_task_obj,many=True)
        date=[]
        date_sum=[]

        if not class_task_ser.data:
            return Response({  "code":10000,  "data":{    "orderData":{    "date":date,
                                                                       "data":date_sum},    "messageData":[   {'title':'告全体用户书','time':'2024/6/20','msg':'感谢对本系统的支持,送你们最后一件礼物(本系统的源代码),源代码还未推送至开源社区请谨记该链接(https://github.com/lzq-hopego/homework-system),将在不久后可以下载,愿你们在未来的道路上，勇往直前，无惧风雨，始终怀揣着对生活的热爱和对梦想的执着，勇敢地闯荡人生的江湖。再见！','manager':'李展旗'},{'title':'增加在线课程表','time':'2024/5/14 23:30','msg':'此次更新修复了一些bug提高稳定性,新增了在线课表功能',"manager":'管理员-李展旗'},{'title':'作业系统更新','time':'2024/4/9 18:20','msg':'此次更新增加了绑定邮箱功能，和登录页面密码找回功能，找回后会重置密码至初始密码，初始密码为名字的拼音',"manager":'管理员-李展旗'}, {"title":"关于作业系统更新为新版本的通知","time":'2024/3/18 11:09',"msg":'旧版本作业系统依旧保留，随时等待开源，旧版本因为不支持前后端分离，性能大打折扣，因此启用新版本，望周知',"manager":'管理员-李展旗'    },     ],  "userData":[{  "date":'周一',  "new":5,  "active":200},{  "date":'周二',  "new":5,  "active":200},{  "date":'周三',  "new":5,  "active":200},{  "date":'周四',  "new":5,  "active":200},{  "date":'周五',  "new":5,  "active":200},{  "date":'周六',  "new":5,  "active":200},{  "date":'周日',  "new":5,  "active":200},]}  })


        for i in class_task_ser.data:
            date.append(i.get('PutTime',None))
            if i.get('PutTime',None):
                date_sum.append(1)
                continue

            date_sum.append(1)

        return Response({  "code":10000,  "data":{    "orderData":{    "date":date,
                                                                       "data":date_sum},    "messageData":[   {'title':'告全体用户书','time':'2024/6/20','msg':'感谢对本系统的支持,送你们最后一件礼物(本系统的源代码),源代码还未推送至开源社区请谨记该链接(https://github.com/lzq-hopego/homework-system),将在不久后可以下载,愿你们在未来的道路上，勇往直前，无惧风雨，始终怀揣着对生活的热爱和对梦想的执着，勇敢地闯荡人生的江湖。再见！','manager':'李展旗'},
                                                                                                            {'title':'增加在线课程表','time':'2024/5/14 23:30','msg':'此次更新修复了一些bug提高稳定性,新增了在线课表功能',"manager":'管理员-李展旗'},
                                                                                                            {'title':'作业系统更新','time':'2024/4/9 18:20','msg':'此次更新增加了绑定邮箱功能，和登录页面密码找回功能，找回后会重置密码至初始密码，初始密码为名字的拼音',"manager":'管理员-李展旗'}, {"title":"关于作业系统更新为新版本的通知","time":'2024/3/18 11:09',"msg":'旧版本作业系统依旧保留，随时等待开源，旧版本因为不支持前后端分离，性能大打折扣，因此启用新版本，望周知',"manager":'管理员-李展旗'    },     ],  "userData":[{  "date":'周一',  "new":5,  "active":200},{  "date":'周二',  "new":5,  "active":200},{  "date":'周三',  "new":5,  "active":200},{  "date":'周四',  "new":5,  "active":200},{  "date":'周五',  "new":5,  "active":200},{  "date":'周六',  "new":5,  "active":200},{  "date":'周日',  "new":5,  "active":200},]}  })

# 获取提交数据
class getCountData(APIView):
    authentication_classes=[TwoStudentAuthentication,TeacherAuthentication]

    def get(self,request):
        tea_obj=Teacher.objects.filter(id=request.auth,name=request.user).first()
        if tea_obj:
            return Response({  'code':10000,  "data":[{"name":'总计作业数',"value":0,"icon":'Discount',"color":'#ffb980'},{"name":'已完成作业数',"value":0,"icon":'SuccessFilled',"color":'#5ab1ef'},{"name":'未完成作业数',"value":0,"icon":'WarnTriangleFilled',"color":'#fc3d49'}]  })
        

        Class=Student.objects.filter(id=request.auth).first().classes
        classtask=Class.classtasks_set.filter().all()
         #处理要返回的数据
        count=classtask.count()

        stu_obj=Student.objects.filter(id=request.auth).first()
        classtasksuccess=stu_obj.classtaskssussess_set.filter().all()

        count_success=classtasksuccess.count()
        
        return Response({'code':10000,"data":[{"name":'总计作业数',"value":count
                                               ,"icon":'Discount',"color":'#ffb980'}
                                               ,{"name":'已完成作业数',"value":count_success
                                                 ,"icon":'SuccessFilled',"color":'#5ab1ef'}
                                                 ,{"name":'未完成作业数',"value":(count-count_success),"icon":'WarnTriangleFilled',"color":'#fc3d49'}] })


## 获取课程表信息
class GetKebiao(APIView):
    authentication_classes=[StudentAuthentication,]
    def get(self,request):
        TimeTables_obj=TimeTables.objects.filter(Student=request.auth).first()
        # print(a.StartData)
        TimeTables_ser=TimeTablesSerializers(instance=TimeTables_obj)
        if not TimeTables_ser.data:
            return Response()
        
        return Response({'start-learn-time':TimeTables_ser.data.get('StartData')
                         ,'data':TimeTables_ser.data.get('TimeTable')})
    
## 获取时间表信息
class GetShijian(APIView):
    authentication_classes=[StudentAuthentication,]
    def get(self,request):
        TimeTables_obj=TimeTables.objects.filter(Student=request.auth).first()
        # print(a.StartData)
        TimeTables_ser=TimeTablesSerializers(instance=TimeTables_obj)
        if not TimeTables_ser.data:
            return Response()
        return Response({'data':TimeTables_ser.data.get('TimeList')})





class test(APIView):
    def get(self,request):
        
#         stu=Student.objects.filter(classes_id=2).all()
#         lt=[x.id for x in stu]
#         ls=[
#   { 's': '08:20', 'e': '09:05' }, { 's': '09:15', 'e': '10:00' },
#   { 's': '10:20', 'e': '11:05' }, { 's': '11:15', 'e': '12:00' },
#   { 's': '14:00', 'e': '14:45' }, { 's': '14:55', 'e': '15:40' },
#   { 's': '16:00', 'e': '16:45' }, { 's': '16:55', 'e': '17:40' },
#   { 's': '19:00', 'e': '19:45' }, { 's': '19:55', 'e': '20:40' },
# ]
#         ls1=[{'title': '信息安全技术与实施', 'location': '41517(多媒体)', 'teacher': '王宪凡', 'week': 1, 'start': 1, 'duration': 2, 'weeks': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]}, {'title': '信息安全技术与实施', 'location': '51405(机房)', 'teacher': '王宪凡', 'week': 1, 'start': 3, 'duration': 2, 'weeks': [13, 14, 15]}, {'title': '信息安全技术与实施', 'location': '41517(多媒体)', 'teacher': '王宪凡', 'week': 3, 'start': 3, 'duration': 2, 'weeks': [13, 14, 15]}, {'title': '信息安全技术与实施', 'location': '41517(多媒体)', 'teacher': '王宪凡', 'week': 5, 'start': 1, 'duration': 2, 'weeks': [13, 14, 15]}, {'title': '职业素养（二）', 'location': '41519(多媒体)', 'teacher': '王琳', 'week': 2, 'start': 5, 'duration': 2, 'weeks': [1, 2, 3, 4, 5, 6, 7, 8]}, {'title': '网络安全应急响应', 'location': '41508(多媒体)', 'teacher': '李熠芳', 'week': 5, 'start': 3, 'duration': 2, 'weeks': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]}, {'title': 'WEB安全技术', 'location': '41525(多媒体)', 'teacher': '冯金涛', 'week': 2, 'start': 1, 'duration': 2, 'weeks': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]}, {'title': 'WEB安全技术', 'location': '41412(多媒体)', 'teacher': '冯金涛', 'week': 3, 'start': 7, 'duration': 2, 'weeks': [1, 2, 3, 4, 5, 6, 7, 8, 9]}, {'title': 'Kali Linux技术', 'location': '41412(多媒体)', 'teacher': '冯金涛', 'week': 1, 'start': 5, 'duration': 2, 'weeks': [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]}, {'title': 'Kali Linux技术', 'location': '41412(多媒体)', 'teacher': '冯金涛', 'week': 1, 'start': 7, 'duration': 2, 'weeks': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]}, {'title': 'Kali Linux技术', 'location': '51405(机房)', 'teacher': '冯金涛', 'week': 3, 'start': 1, 'duration': 2, 'weeks': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]}, {'title': 'MSF渗透测试', 'location': '41315(多媒体)', 'teacher': '冯金涛', 'week': 1, 'start': 7, 'duration': 2, 'weeks': [15]}, {'title': 'MSF渗透测试', 'location': '41525(多媒体)', 'teacher': '冯金涛', 'week': 2, 'start': 3, 'duration': 2, 'weeks': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]}, {'title': 'Linux系统运维管理', 'location': '41513(多媒体)', 'teacher': '曹兵', 'week': 3, 'start': 3, 'duration': 2, 'weeks': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]}, {'title': 'Linux系统运维管理', 'location': '51506(机房)', 'teacher': '曹兵', 'week': 5, 'start': 1, 'duration': 2, 'weeks': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]}, {'title': '四史教育', 'location': '41303(多媒体)', 'teacher': '姚宏章', 'week': 3, 'start': 7, 'duration': 2, 'weeks': [10, 11, 12, 13, 14, 15, 16, 17]}, {'title': '高职体育(四)', 'location': '体育任选', 'teacher': '体育任选', 'week': 5, 'start': 5, 'duration': 2, 'weeks': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]}, {'title': '形势与政策(四)', 'location': '41312(多媒体)', 'teacher': '乔浩然', 'week': 2, 'start': 5, 'duration': 2, 'weeks': [14, 15, 16, 17]}]
#         test=TimeTablesSerializers(data={'classes':1,
#                                          'StartData':'2024-03-04',
#                                         'TimeList':ls,
#                                          'TimeTable':ls1 ,
#                                          'Student':lt})
#         if not test.is_valid():
#             print(test.errors)
#             # test.save()addzy_ser
#         test.save()
        return Response('ok')