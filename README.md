# homework-system
这是一个以vue和python开发的前后端分离的课后作业收集系统
graph LR
C((整体构架))
C -->|vue3+element-plus| D[主前端页面]
C -->|vue3+uniapp| E[ 下属的在线课表 ]
C -->|django+drf| F[ 后端 ]
