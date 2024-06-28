import axios from "axios";
import config from "../config";
import { ElMessage } from "element-plus";
import Cookie from 'js-cookie'

const NETWORK_ERROR='网络请求错误，请稍后重试';





// 创建一个aixos请求

const service=axios.create({
    baseURL:config.baseApi
})




// 请求之前做一些事
service.interceptors.request.use((req)=>{
 
    // 可以自定义header

    // req.headers['Content-Type']='application/x-www-form-urlencoded'
      
    //获取token
    const token=Cookie.get('token')
    if (token) {
        req.headers['token'] = token
    }
    return req

}, function (error) {
    // 对请求错误做些什么
    ElMessage.error("请求失败")
    return Promise.reject(error);
})


// 请求之后做一些事

service.interceptors.response.use((res)=>{
    const {code,data,msg} =res.data;
    // console.log(res)
    if (code==10000){
        return data
    }else{
        //网络错误提示
        ElMessage.error(msg+'('+code+')'||NETWORK_ERROR)
        return Promise.reject(msg||NETWORK_ERROR)
    }
    
}, function (error) {
    if(error.code==='ERR_NETWORK'){
        ElMessage.error(NETWORK_ERROR)
    }else{
        // 对请求错误做些什么
        if (error.response.data.code){
            //处理认证失败的问题
            ElMessage.error(error.response.data.msg+"("+error.response.data.code+")请重新登录")

            if(error.response.data.code==20000){
                Cookie.remove('token')
                window.location.replace('/#/login')

            }
        }else{
            ElMessage.error("请求失败"+'('+error.request.status+')'||NETWORK_ERROR)
        }
    }
    
    return Promise.reject(error);
})


// 封装请求的核心函数
function request(options){
    options.method=options.method||'get'
    if (options.method.toLowerCase()=='get'){
        options.params=options.data
    }

    // 对mock进行处理
    let isMock=config.mock
    if(typeof options.mock !== 'undefined'){
        isMock=options.mock
    }

    // 对线上环境进行处理
    if(config.env=='prod'){
        service.defaults.baseURL=config.baseApi
    }else{
        service.defaults.baseURL=isMock ? config.mockApi : config.baseApi
    }
    return service(options)
}

export default request
