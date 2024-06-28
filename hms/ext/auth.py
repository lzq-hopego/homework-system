from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from apis.models import (classes,Student,Teacher)

# 做用户认证的逻辑处理功能
# 1、传入token
# 2、校验合法性
# 3、返回值   返回值有三种      
    # 3.1、(request.user,request.auth)认证成功
    # 3.2、抛出异常，认证失败
    # 3.3、返回None，有多个认证类   如果返回None则去找下一个认证类

class StudentAuthentication(BaseAuthentication):
    # 学生认证类
    def authenticate(self,request):
        token=request.headers.get('token') 
        usertoken=request.query_params.get('usertoken')
        token=token if token else usertoken
        if not token:
            # token=usertoken
            raise AuthenticationFailed({'code':20000,'msg':'认证失败'}) 
        user_obj=Student.objects.filter(token=token).first()
        if user_obj:
            if user_obj.ChangePassword==2:
                raise AuthenticationFailed({'code':20000,'msg':'未更改密码'})
        if user_obj:
            return user_obj.name,user_obj.id
        raise AuthenticationFailed({'code':20000,'msg':'认证失败'}) 

    
class TwoStudentAuthentication(BaseAuthentication):
    # 连用两个认证类的学生类  学生认证类
    def authenticate(self,request):
        token=request.headers.get('token') 
        usertoken=request.query_params.get('usertoken')
        token=token if token else usertoken
        
        if (not token) or token=='undefined':
            # token=usertoken
            raise AuthenticationFailed({'code':20000,'msg':'认证失败'}) 
        try:
            user_obj=Student.objects.filter(token=token).first()
        except:
            return 
        if user_obj:
            if user_obj.ChangePassword==2:
                raise AuthenticationFailed({'code':20000,'msg':'未更改密码'})
        if user_obj:
            return user_obj.name,user_obj.id

        



class TeacherAuthentication(BaseAuthentication):
    # 教师认证类
    def authenticate(self,request):
        token=request.headers.get('token') 
        usertoken=request.query_params.get('usertoken')
        token=token if token else usertoken
        if (not token) or token=='undefined':
            raise AuthenticationFailed({'code':20000,'msg':'认证失败'}) 
        try:
            user_obj=Teacher.objects.filter(token=token).first()
        except:
            raise AuthenticationFailed({'code':20000,'msg':'认证失败'}) 
        if user_obj:
            return user_obj.name,user_obj.id
        raise AuthenticationFailed({'code':20000,'msg':'认证失败'}) 





       