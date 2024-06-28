"""hms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from apis import views

urlpatterns = [
    path('api/Login/',views.Login.as_view()),#登录
    path('api/LoginAlterpasswd',views.LoginAlterpasswd.as_view()),#第一次登录改密码
    path("api/getmenu/",views.getmenu.as_view()),#返回菜单
    path("api/getClasses/",views.getClasses.as_view()),#返回全部班级getZyClassesInfo
    path("api/getZyClassesInfo/",views.getZyClassesInfo.as_view()),#返回全部班级
    path('api/user/getUser/',views.StuData.as_view()),#查询学生用户信息
    path('api/user/getUserAvatar/',views.getUserAvatar.as_view()),#获取学生头像
    path('api/user/alterUserAvatar/',views.AlterUserAvatar.as_view()),#获取学生头像
    path('api/user/addUser/',views.addStuData.as_view()),#新增学生用户
    path('api/user/editUser/',views.editStuData.as_view()),#编辑学生用户
    path('api/user/loginlog/',views.UserLoginlog.as_view()),#查看本次登录的时间和ip信息
    path('api/user/deleteUser/',views.deleteStuData.as_view()),#删除学生用户
    path('api/user/getuseremail/',views.getUserEmail.as_view()),#获取用户邮箱
    path('api/email/add',views.AddEmail.as_view()),#绑定邮箱
    path('api/email/sendmsg',views.SendEmailMsg.as_view()),#邮箱发送验证码
    path('api/email/forgetsendmsg',views.SendForgetEmailMsg.as_view()),#邮箱发送忘记密码验证码
    path('api/email/alterpasswd',views.EmailToAlterpasswd.as_view()),#邮箱发送忘记密码验证码
    path("api/getzylist/",views.getZyList.as_view()),#获取作业列表
    path("api/getglzylist/",views.getGlZyList.as_view()),#管理员获取作业列表
    path("api/getzyinfo/",views.getZyInfo.as_view()),#获取作业详情
    path("api/zy/upload",views.getZyUpload.as_view()),#上传作业
    path("api/zy/delmyzy",views.getDelZy.as_view()),#删除我的作业
    path("api/zy/viewmyzy",views.getViewZy.as_view()),#浏览我的作业
    path("api/zy/getmyzy",views.getMyZy.as_view()),#下载我的作业
    path("api/home/getCharData",views.getCharData.as_view()),#获取近七天的上传作业的统计
    path("api/home/getCountData",views.getCountData.as_view()),
    path("api/getTeacher",views.getTeacher.as_view()),#获取所有教师姓名
    path("api/addzy",views.addzy.as_view()),#添加作业
    path("api/editzy",views.Editzy.as_view()),#编辑作业
    path("api/delzy",views.delzy.as_view()),#删除作业
    path("api/getzytestfile",views.GetzyTestFile.as_view()),#预览上传页面(学生能看到的页面)
    path("api/getglzyinfo",views.GetGlzyinfo.as_view()),#获取作业完成情况
    path("api/getglstuzyinfo",views.GetGlstuzyinfo.as_view()),#获取学生作业内容
    path("api/delglstuzy",views.DelGlstuzy.as_view()),#删除学生作业
    path("api/getglstuzyzip",views.GetGlstuzyZip.as_view()),#删除学生作业
    path("api/alterstupasswd",views.AlterStuPasswd.as_view()),#删除学生作业
    path('api/getuserinfo',views.UserInfo.as_view()),#获取个人信息的姓名和角色
    path('api/kebiao',views.GetKebiao.as_view()),
    path('api/shijian',views.GetShijian.as_view()),
    # path('api/test',views.test.as_view()),
]
