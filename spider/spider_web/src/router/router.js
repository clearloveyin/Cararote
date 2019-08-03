import Vue from 'vue'
import Router from 'vue-router'
import store from '@/store/store'
import { Message } from 'element-ui'
import VueCookies from 'vue-cookies'

Vue.use(Router)
const Login = () => import('@/views/login/Login.vue')
const Home = () => import('@/views/homePage/Home.vue')
const Spec = () => import('@/views/specPage/Spec')
const Rfq = () => import('@/views/rfqPage/RfqManage')

const routerUrl = new Router({
    routes: [
        {
            path: '/',
            name: 'login',
            component: Login,
            meta: {
                isLogin: false
            }
        },
        {
            path: '/home',
            name: 'home',
            component: Home,
            children: [
                {
                    path: '/home/spec',
                    name: 'spec',
                    component: Spec,
                    meta: {
                        isLogin: true
                    }
                },
                {
                    path: '/home/rfq',
                    name: 'rfq',
                    component: Rfq,
                    meta: {
                        isLogin: true
                    }
                }
            ],
            meta: {
                isLogin: true
            }
        }
  ]
})

routerUrl.beforeEach((to, from, next) => {
    // 获取用户登录成功后的登录标志，
    // let getFlag = cookies.get('Flag')
    // 判断登录标志存在且为 isLogin,即用户已登录
    // 设置vuex登录状态为true， store.state.isLogin = true
    // 如果已登录状态，用户又想进入登录页面，则定向回首页，提示用户必须先退出用户
    // ！to.meta.isLogin , Message.error({message:'请先退出登录'}),next({path:'/home'})
    // 如果登录标志不存在，即未登录，
    // 用户想进入页面必须登录，所以重定向回登录页面,
    // to.meta.isLogin, next({path:'/'})
    // 友好提示
    let getFlag = VueCookies.get('Flag')
    console.log(getFlag)
    if (getFlag === 'isLogin') {
        store.state.isLogin = true
        next()
        if (!to.meta.isLogin) {
            Message.error({ message: '请先退出登录!' })
            next({ path: '/home' })
        }
    } else {
        if (to.meta.isLogin) {
            next({ path: '/' })
            Message.error({ message: '请先登录!' })
        } else {
            next()
        }
    }
})
routerUrl.afterEach(transition => {
    window.scroll(0, 0)
})

export default routerUrl
