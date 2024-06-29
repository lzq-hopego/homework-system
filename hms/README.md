## 修改配置

- 修改数据库

  ```
  vim ./hms/settings.py
  ```

  找到第72行进行修改数据库的连接密码啥的

  ```
   72 DATABASES = {
   73     'default': {
   74     'ENGINE': 'django.db.backends.mysql',
   75     'NAME':'hms',
   76     'USER': 'hms',
   77     'PASSWORD': 'password',
   78     'HOST': '127.0.0.1',
   79     'PORT': '3306',
   80     }
   81 }
  ```

- 修改邮件服务器的配置

  ```
  vim ./ext/SendEmail.py
  ```

  修改第7，8行的邮箱内容

  ```
  my_sender='user@126.com'    # 发件人邮箱账号
  my_pass = 'password'              # 发件人邮箱服务器的授权码
  ```

  修改第13行的发件人昵称

  ```
  msg['From']=formataddr(["user_src",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
  ```

  - 如果需要更换邮件服务商，请修改第17行的邮件服务商的域名

    ```
    server=smtplib.SMTP_SSL("smtp.126.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465(ssl)
    ```

    
## 准备

- pip安装所需依赖

  ```
  pip install -r requirements.txt
  ```

  

- 需要开启的端口

  ```
  firewall-cmd --add-port=465/tcp --per #465端口用于发送邮件
  firewall-cmd --reload
  ```
  
- mysql 创建数据库

  ```
  CREATE DATABASE `hms` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
  ```

- django

  > 此步骤为每次升级或降级时必须先使用的命令

  ```
  python ./manage.py makemigrations   #检测数据库
  python ./manage.py migrate          #	创建数据表
  ```

  

## 测试



- 本地测试时

  ```
  python ./manage.py runserver 0.0.0.0:80
  ```

  - 支持IPv6的运行

    ```
    python ./manage.py runserver [::]:80
    ```

    

## 上线

- UWSGI

  ```
  yum install uwsgi   
  ```

  > 推荐使用uwsgi并非测试时django自带的服务器
  >
  > 使用uwsgi需要uwsgi配置文件

  uwsgi.ini

  > 全部配置文件都是使用绝对路径进行编写的

  ```
  #下列是uwsgi.ini文件的内容，第一行的[uwsgi]必须写
  [uwsgi]
  # 使用http访问，0表示任何IP，8001表示端口号，要求同上
  # http=0:9000
  # 绑定服务器的unix/tcp套接字
  socket=/www/hms/hms.sock
  # 项目的绝对路径
  chdir=/www/hms
  # 项目的wsgi.py文件，如果你怕写乱，此处建议写绝对路径
  wsgi-file=/www/hms/hms/wsgi.py
  # 允许主线程存在
  master=true
  # 开启进程的数量
  processes=1
  # 开启多线程
  enable-threads=false
  # 当服务器退出的时候自动清理环境，删除socket文件和pid文件
  vacuum=true
  # 使进程在后台运行，并将日志打到指定的日志文件
  daemonize=uwsgi.log
  # 指定pid文件的位置，记录主进程的pid号，主要用于关闭服务
  pidfile=uwsgi.pid
  #指定上传文件最大带宽
  buffer-size = 10485760
  ```

- nginx配置文件

  ```
  upstream hms {
    server unix:/www/wwwroot/hms/hms.sock;
  }
  
  server
  {
      listen 443;#监听端口
      server_name domain;#域名
      index index.html;
      root /www/hms;
      
      location / {
        include /etc/nginx/conf/uwsgi_params;
        uwsgi_pass hms;
      }
      #禁止访问的文件或目录
      location ~ ^/(\.user.ini|\.htaccess|\.git|\.env|\.svn|\.project|LICENSE|README.md)
      {
          return 404;
      }
      location ~ .*\.(gif|jpg|jpeg|png|bmp|swf)$
      {
          expires      30d;
          error_log /dev/null;
          access_log /dev/null;
      }
  
      location ~ .*\.(js|css)?$
      {
          expires      12h;
          error_log /dev/null;
          access_log /dev/null;
      }
      access_log  /var/log/domain.log;
      error_log  /var/log/domain.error.log;
  }
  ```

  

