import {createRouter,createWebHashHistory} from "vue-router"


const routes=[
    {
        path:'/',
        component:()=>import("../views/main.vue"),
        name:'house',
        redirect:'/home',
        children:[
            {
                path:'/home',
                name:'home',
                component:()=>import("../views/home.vue"),
                meta:{'title':'主页'}
                
            },
            {
                path:'/user',
                name:'user',
                component:()=>import("../views/User/User.vue"),
                meta:{'title':'用户管理'}
            },
            {
                path:'/zylist',
                name:'zylist',
                component:()=>import("../views/Zylist/zylist.vue"),
                meta:{'title':'作业列表'}
            },
            {
                path:'/glzylist',
                name:'glzylist',
                component:()=>import("../views/Zylist/glzylist.vue"),
                meta:{'title':'管理作业'}
            },
            {
                path:'/PersonalCenter',
                name:'PersonalCenter',
                component:()=>import("../views/User/PersonalCenter.vue"),
                meta:{'title':'个人中心'}
            }
        ]
        // children:[],
    },

    {
        path:'/login',
        name:'login',
        component:()=>import('../views/Login.vue'),
        meta: { title: '登录页面' }
    },
    {
        path:'/kebiao',
        name:'kebiao',
        component:()=>import('../views/phone/kebiao.vue'),
        meta: { title: '在线课表' }
    }
]

const router=createRouter({
    history:createWebHashHistory(),
    routes
})

export default router