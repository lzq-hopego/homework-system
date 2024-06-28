import request from "./request";

export default{
    getTableData(params){
        return request({
            url:'/home/getData',
            method:'get',
            data:params,
            mock:false
        })
    },
    getCountData(params){
        return request({
            url:'/home/getCountData',
            method:'get',
            data:params,
            mock:false
        })
    },
    getEchartsData(params){
        return request({
            url:'/home/getCharData',
            method:'get',
            data:params,
            mock:false
        })
    },
    getUserData(params){
        return request({
            url:'/user/getUser/',
            method:'get',
            data:params,
            mock:false,
        })
    },
    getClasses(params){
        return request({
            url:'/getClasses/',
            method:'get',
            data:params,
            mock:false,
        })
    },getZyClassesInfo(params){
        return request({
            url:'/getZyClassesInfo/',
            method:'get',
            data:params,
            mock:false,
        })
    },getTeacher(params){
        return request({
            url:'/getTeacher',
            method:'get',
            data:params,
            mock:false,
        })
    },
    addUser(params){
        return request({
            url:'/user/addUser/',
            method:'post',
            data:params,
            mock:false
        })
    },
    editUser(params){
        return request({
            url:'/user/editUser/',
            method:'post',
            data:params,
            mock:false
        })
    },
    deleteUser(params){
        return request({
            url:'/user/deleteUser/',
            method:'get',
            data:params,
            mock:false
        })
    },
    Login(params){
        return request({
            url:'/Login/',
            method:'post',
            data:params,
            mock:false
        })
    },
    getmenu(params){
        return request({
            url:'/getmenu/',
            method:'get',
            data:params,
            mock:false,
            
        })
    },
    getuserlog(params){
        return request({
            url:'/user/loginlog',
            method:'get',
            data:params,
            mock:false,
            
        })
    },
    getzylist(params){
        return request({
            url:'/getzylist',
            method:'get',
            data:params,
            mock:false,
            
        })
    },
    getglzylist(params){
        return request({
            url:'/getglzylist',
            method:'get',
            data:params,
            mock:false,
            
        })
    },
    getzyinfo(params){
        return request({
            url:'/getzyinfo',
            method:'get',
            data:params,
            mock:false,
            
        })
    },getUserEmail(params){
        return request({
            url:'/user/getuseremail/',
            method:'get',
            data:params,
            mock:false,
            
        })
    },
    mergeFileszyupload(params){
        return request({
            url:'/zy/upload',
            method:'get',
            data:params,
            mock:false,
            
        })
    },
    postzyupload(params){
        return request({
            url:'/zy/upload',
            method:'post',
            data:params,
            mock:false,
            
        })
    },
    deletemyzy(params){
        return request({
            url:'/zy/delmyzy',
            method:'get',
            data:params,
            mock:false,
        })
    },
    viewmyzy(params){
        return request({
            url:'/zy/viewmyzy',
            method:'get',
            data:params,
            mock:false,
        })
    },
    getmyzy(params){
        return request({
            url:'/zy/getmyzy',
            method:'get',
            data:params,
            mock:false,
        })
    },
    addzy(params){
        return request({
            url:'/addzy',
            method:'post',
            data:params,
            mock:false
        })
    },
    delzy(params){
        return request({
            url:'/delzy',
            method:'get',
            data:params,
            mock:false
        })
    },
    editzy(params){
        return request({
            url:'/editzy',
            method:'post',
            data:params,
            mock:false
        })
    },
    getglzyinfo(params){
        return request({
            url:'/getglzyinfo',
            method:'get',
            data:params,
            mock:false
        })
    },
    delstuzy(params){
        return request({
            url:'/delglstuzy',
            method:'get',
            data:params,
            mock:false
        })
    },
    getglstuzyzip(params){
        return request({
            url:'/getglstuzyzip',
            method:'get',
            data:params,
            mock:false
        })
    },
    alterstupasswd(params){
        return request({
            url:'/alterstupasswd',
            method:'post',
            data:params,
            mock:false
        })
    },
    getuserinfo(params){
        return request({
            url:'/getuserinfo',
            method:'get',
            data:params,
            mock:false
        })
    },
    SendEmailMsg(params){
        return request({
            url:'/email/sendmsg',
            method:'get',
            data:params,
            mock:false
        })
    },
    SendForgetEmailMsg(params){
        return request({
            url:'/email/forgetsendmsg',
            method:'post',
            data:params,
            mock:false
        })
    },
    AddEmail(params){
        return request({
            url:'/email/add',
            method:'post',
            data:params,
            mock:false
        })
    },
    EmailToAlterpasswd(params){
        return request({
            url:'/email/alterpasswd',
            method:'post',
            data:params,
            mock:false
        })
    },
    LoginAlterpasswd(params){
        return request({
            url:'/LoginAlterpasswd',
            method:'post',
            data:params,
            mock:false
        })
    }
}