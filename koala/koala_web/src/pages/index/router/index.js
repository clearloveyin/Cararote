import Vue from 'vue';
import Router from 'vue-router';
import cookies from 'vue-cookies'

Vue.use(Router)
const router = new Router({
    routes: [
        {
            path: '*',
            redirect: {
                name: 'login'
            }
        },
        {
            path: '/login',
            component: resolve => require(['@/components/login/Login'], resolve),
            name: 'login'
        },
        {
            path: '/summaryAccount',
            component: resolve => require(['@/pages/otherpage/handsontable/handsontablePLReview'], resolve),
            name: 'summaryAccount',
            meta: {
                requiresAuth: true
            }
        },
        {
            path: '/HomeContent',
            component: resolve => require(['@/components/header/HomeContent'], resolve),
            name: '首页'
        },
        {
            path: '/HomePage',
            component: resolve => require(['@/components/header/HomePage'], resolve),
            name: 'header',
            // 项目
            children: [
                {
                    path: '/featurePage/TaskList',
                    component: resolve => require(['@/components/featurePage/TaskList'], resolve),
                    name: 'TaskList',
                    meta: {
                        requiresAuth: true
                    }
                },
                {
                    path: '/featurePage/FeatureList',
                    component: resolve => require(['@/components/featurePage/FeatureList'], resolve),
                    name: 'FeatureList',
                    meta: {
                        requiresAuth: true
                    }
                },
                {
                    path: '/featurePage/ConfirmFeature',
                    component: resolve => require(['@/components/featurePage/ConfirmFeature'], resolve),
                    name: 'ConfirmFeature',
                    meta: {
                        requiresAuth: true
                    }
                },
                {
                   
                    path: '/Input/InputList',
                    component: resolve => require(['@/components/input/InputList'], resolve),
                    name: 'inputList',
                    meta: {
                        requiresAuth: true
                    }
                },
                {
                    path: '/Input/InputAddEdit',
                    component: resolve => require(['@/components/input/InputAddEdit'], resolve),
                    name: 'InputAddEdit',
                    meta: {
                        requiresAuth: true //配子路由时候务必加上该字段：requiresAuth: true（true为验证打开，false为关闭）
                    }
                },
                {
                    path: '/Options/OptionsView',
                    component: resolve => require(['@/components/options/OptionsView'], resolve),
                    name:'OptionsView',
                    meta: {
                        requiresAuth: true
                    }
                },
                {
                    path: '/proj/proj_list',
                    component: resolve => require(['@/components/proj/Project_list'], resolve),
                    name: 'proj_list',
                    children: [{
                        path: '/proj/proj_content',
                        component: resolve => require(['@/components/proj/Project_content'], resolve),
                        name: 'Project_content',
                        meta: {
                            requiresAuth: true
                        }
                    }]
                },
                {
                    path: '/proj/add_project/:pro_id',
                    component: resolve => require(['@/components/proj/add_proj'], resolve),
                    name: 'add_proj',
                    meta: {
                        requiresAuth: true
                    }
                },
                {
                    path: '/proj/add_project_c',
                    component: resolve => require(['@/components/proj/add_proj_c'], resolve),
                    name: 'add_project_c',
                    meta: {
                        requiresAuth: true
                    }
                },
                {
                    path: '/proj/pro_detail/:pro_id',
                    component: resolve => require(['@/components/proj/Project_detail'], resolve),
                    name: 'Project_detail',
                    meta: {
                        requiresAuth: true
                    }
                },
                {
                    path: '/proj/quotation/:pro_id',
                    component: resolve => require(['@/components/proj/Quotation_initiation'], resolve),
                    name: 'Quotation_initiation',
                    meta: {
                        requiresAuth: true
                    }
                },
                {
                    path: '/proj/proj_quote',
                    component: resolve => require(['@/components/proj/Proj_quote'], resolve),
                    name: 'Proj_quote',
                    meta: {
                        requiresAuth: true
                    }
                },
                {
                    path: '/projQuoteList',
                    component: resolve => require(['@/components/proj/proj_quote_list'], resolve),
                    name: 'projQuoteList',
                    meta: {
                        requiresAuth: true
                    }
                },
                {
                    path: '/proj/quotation_pie/:quotation_id/:pro_id',
                    component: resolve => require(['@/components/proj/Quotation_pie'], resolve),
                    name: 'Quotation_pie',
                    meta: {
                        requiresAuth: true
                    }
                },
                {
                    path: '/system_table/system_table_view/:pro_id',
                    component: resolve => require(['@/components/system_table/system_table_view'], resolve),
                    name: 'system_table',
                    meta: {
                        requiresAuth: true
                    }
                },
                {
                    path: '/allProject',
                    component: resolve => require(['@/components/proj/All_Project'], resolve),
                    name: 'all_list',
                    meta: {
                        requiresAuth: true
                    }
                },
                {
                    path: '/managerUser',
                    component: resolve => require(['@/components/manager/managerUser'], resolve),
                    name: 'managerUser',
                    meta: {
                        requiresAuth: true
                    }
                },
            ]
        },
    ]
})

const whiteList = ['/login']// no redirect whitelist
router.beforeEach((to, from, next) => {
    if(cookies.get('token')) {
        if(to.path === '/login') {
            next('/projQuoteList')
        } else {
            next()
        }
    } else {
        if (whiteList.indexOf(to.path) !== -1) { // 在免登录白名单，直接进入
            next()
        } else {
            next('/login') // 否则全部重定向到登录页
        }
    }
})

export default router;

