import Mock from 'mockjs'
import homeApi from './mockData/home'
import userApi from './mockData/user'

// 拦截请求，用于无后端时开发
Mock.mock('/home/getData',homeApi.getHomeData)

//获取本地user随机生成的数据
Mock.mock("/user/getUser",userApi.getUserList)
