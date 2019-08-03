<template>
    <div class="homepage">
        <!--头部组件-->
        <div class="header font-color background-color">
            <div class="header-nav">
                <el-menu :default-active="nav_active_index" class="el-menu-demo" mode="horizontal" background-color="#24292e" text-color="#fff" active-text-color="#ffd04b">
                    <el-menu-item index="1" @click="goAll()" v-if="show_btn_flag">所有项目/报价</el-menu-item>
                    <el-menu-item index="2" @click="goManager()" v-if="show_btn_flag">PL管理</el-menu-item>
                    <el-menu-item index="3" @click="goMyPage()">我的</el-menu-item>
                    <el-submenu index="4">
                        <template slot="title">{{userName}}</template>
                        <el-menu-item index="4-1" @click='logOut'>退出</el-menu-item>
                    </el-submenu>
                </el-menu>
            </div>
            
            <div class="header-left">
                <img class="header-left-logo" src="" alt="">
                <span class="header-left-title" @click="homePage">· {{titleName}}</span>
            </div>

        </div>
        <div class="homepage-view">
            <router-view/>
        </div>
    </div>
</template>

<script>
import {getUserRolePL_2} from '@/api/content_api'
export default {
    data() {
        return {
            titleName: 'Koala',
            inActive: -1,
            login_user_name: '',
            user_leve: '',
            operations: [
                { menu_name: '我的', id: 1 },
                {menu_name:'项目',id:2},
                {menu_name:'管理',id:3},
                { menu_name: '履历', id: 4 }
            ],
            nav_active_index: '',
            userName: '',
            show_btn_flag:false
        }
    },
    destroyed() {
        window.sessionStorage.removeItem("page_index")
    },
    created() {
        this.userName = this.$cookies.get('userName')
        if (!window.sessionStorage.getItem("page_index")) {
            this.nav_active_index = '3'
            window.sessionStorage.setItem("page_index",this.nav_active_index)
        }else{
            this.nav_active_index = window.sessionStorage.getItem("page_index")
        }
        this.promise_all()
        
    },
    methods: {
        promise_all(){
            getUserRolePL_2(Number(this.$cookies.get('userId'))).then(res=>{
            // console.log(res,'============homepage',Number(this.$cookies.get('userId')));
                if (res.data.result =='OK') {
                    let data = res.data.content
                    // data.push("SuperPL")
                    this.$cookies.set('role', res.data.content,3600*12)
                    this.show_btn_flag = data.some(role=>{
                        // console.log(role);
                        return role === 'SuperPL'
                    })
                }
                
            })
        },
        goMyPage() {
            this.$router.push('/projQuoteList')
            this.nav_active_index = '3'
            window.sessionStorage.setItem("page_index",this.nav_active_index)
        },
        logOut() {
            this.$cookies.remove('token')
            this.$router.push('/')
            window.sessionStorage.clear()
        },
        homePage(){
            this.$router.push("/projQuoteList")
            
        },
        goAll(){
            this.$router.push("/allProject")
            this.nav_active_index = '1'
            window.sessionStorage.setItem("page_index",this.nav_active_index)

        },
        goManager(){
            this.$router.push("/managerUser")
            this.nav_active_index = '2'
            window.sessionStorage.setItem("page_index",this.nav_active_index)

        }
    }
}
</script>

<style scoped lang="less">
.homepage {
    width: 100%;
    height: 100%;
    overflow: hidden;
}
.header-nav {
    position: absolute;
    right: 10px;
    top: 0;
    height: 50px;
}
.font-color {
    //new add
    color: #ffffff;
}
.background-color {
    //new add
    background-color: #00a597;
}
.header {
    width: 100%;
    height: 60px;
    box-shadow: 0 0 1px rgba(0, 0, 0, 0.25);
    background-color: #24292e;
    // 新加的：
    padding: 0 20px 0 20px;
    box-sizing: border-box;
    -ms-flex-negative: 0;
    flex-shrink: 0;
    .header-left {
        float: left;
        width: 300px;
        height: 60px;
        line-height: 60px;
        vertical-align: middle;
    }
    .header-left-logo {
        display: inline-block;
        vertical-align: middle;
    }
    .header-left-title {
        font-size: 24px;
        font-weight: 600;
        cursor: pointer;
    }
    .header-right-operations {
        //new add
        display: inline-block;
        float: right;
        padding-right: 100px;
        height: 100%;
    }
    .header-right-operations li {
        //new add
        display: inline-block;
        line-height: 80px;
        padding: 0 10px 0 10px;
        margin: 0 10px 0 10px;
        vertical-align: middle;
        cursor: pointer;
    }
    .header-right-operations li:hover,
    .active {
        font-weight: 600;
        font-size: 18px;
    }
    ul {
        //new add
        list-style-type: none;
        // margin-block-start: 1em;
        // margin-block-end: 1em;
        margin-inline-start: 0px;
        margin-inline-end: 0px;
        padding-inline-start: 40px;
    }
    .el-menu-item {
        padding: 0 20px 0 20px;
    }
    .login-out {
        position: fixed;
        top: 0px;
        right: 0px;
        width: 100px;
        height: 80px;
        line-height: 80px;
        z-index: 10;
        font-size: 14px;
        cursor: pointer;
    }
    .login-out-color {
        display: block;
        width: 40px;
    }
    .dropdown {
        position: relative;
        display: inline-block;
        cursor: pointer;
        z-index: 10;
    }
    .dropdown-content {
        display: none;
        position: absolute;
        min-width: 100px;
        box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.45);
        padding: 0px 0px 0 10px;
        color: #5e6d82;
        height: 50px;
        line-height: 50px;
    }
    .dropdown:hover .dropdown-content {
        display: block;
        // font-size: 14px;
        background-color: #ffffff;
    }
    .el-icon-arrow-down {
        padding-left: 5px;
    }

    .cursor:hover {
        color: #f56c6c;
    }
}
.homepage-view {
    height: calc(100% - 60px);
    width: 100%;
    clear: both;
    overflow: hidden;
    background: #f0f0f0;
}
</style>
