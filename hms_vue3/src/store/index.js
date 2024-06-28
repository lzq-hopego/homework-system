import { createStore } from 'vuex'
import Cookie from 'js-cookie'


export default createStore({
    state: {
        isCollapse: true,
        currentMune: null,
        menu:[],
        token:'',
        username:'',
        ClassTaskToken:'',
        tabsList: [
            {
                path: '/',
                name: 'home',
                label: '首页',
                icon: 'home'

            }
        ],
    },
    mutations: {
        updateIsCollapse(state, payload) {
            state.isCollapse = !state.isCollapse
        },
        selectMenu(state, val) {

            // val.name=='home'?(state.currentMune=null):(state.currentMune=val)
            if (val.name == 'home') {
                state.currentMune = null
            } else {
                state.currentMune = val
                let result = state.tabsList.findIndex(item => item.name === val.name)
                result == -1 ? state.tabsList.push(val) : ''
            }
        },
        closeTag(state,val){
            let res=state.tabsList.findIndex(item=>item.name===val.name)
            state.tabsList.splice(res,1)
        },
        setMenu(state,val){
            state.menu=val
            localStorage.setItem('menu',JSON.stringify(val))
        },
        setUsername(state,val){
            state.username=val
        },
        addMenu(state,router){
            if(!localStorage.getItem('menu')){
                return
            }
            const menu=JSON.parse(localStorage.getItem('menu'))
            state.menu=menu

            // const menuArray=[]

            // menu.forEach(element => {
            //     if(element.children){
            //         element.children=element.children.map(element=>{
            //             let url=`../views/${element.url}.vue`
            //             element.component=()=> import(url)
            //             return element
            //         })
            //         menuArray.push(...element.children)
            //     }else{
            //         let url=`../views/${element.url}.vue`
            //         element.component=()=> import(url)
            //         menuArray.push(element)
            //     }
            // });

            // menuArray.forEach(element => {
            //     router.addRoute('house',element)
            // });
        },
        cleanMenu(state){
            state.menu=[]
            localStorage.removeItem('menu')
        },
        setToken(state,val){
            state.token=val
            Cookie.set('token',val,{ expires: 7 })
        },
        cleanToken(state){
            state.token=''
            Cookie.remove('token')
        },
        getToken(state){
            state.token=state.token||Cookie.get('token')
            
        },
        AlterClassTaskToken(state,val){
            state.ClassTaskToken=val
        }
    }
})
