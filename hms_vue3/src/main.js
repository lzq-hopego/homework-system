import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import router from './router'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import './assets/less/index.less'
import store from './store'
// import './api/mock'
import api from './api/api'

const app=createApp(App)

// 注册图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
  }

app.config.globalProperties.$api=api

//注册动态路由
store.commit('addMenu',router);


//匹配现有路由和访问的路由是否一致
function checkRouter(path) {
  let hasCheck=router.getRoutes().filter(route=>route.path==path).length
  if(hasCheck){
    return true
  }else{
    return false
  }
}

//路由守卫
router.beforeEach((to,from,next)=>{
  store.commit('getToken')
  const token=store.state.token

  document.title = to.meta.title;

  if (!token&&to.name!=='login') {
    next({name:'login'})
  }else if(!checkRouter(to.path)){
    next({name:'home'})
  }else{
    next()
  }
})

app.use(ElementPlus)
app.use(router)
app.use(store)
app.mount('#app')
