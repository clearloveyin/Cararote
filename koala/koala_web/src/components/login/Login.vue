<template>
    <div class="wrapper">
        <div class="header">
            <img src="../../../static/image/kaola.jpg" alt="logo" class="logo"><h1>KoaLa</h1>
        </div>
        <div class="loginPage">
            <h1>登录</h1>
            <el-form>
                <el-form-item label="用户名">
                    <el-input type="text" id="user" v-model="formName.user" @blur="inputBlur('user',formName.user)" placeholder="OA账号"></el-input>
                    <p>{{formName.userError}}</p>
                </el-form-item>
                <el-form-item label="密码">
                    <el-input type="password" id="password" v-model="formName.password" @blur="inputBlur('password',formName.password)"></el-input>
                    <p>{{formName.passwordError}}</p>
                </el-form-item>
                <el-button type="primary" @click="submitForm('formName')" >登录</el-button>
                <el-button @click="resetForm">重置</el-button>
            </el-form>              
        </div>
    </div>

</template>
<script>
import {login} from '@/api/login'
    export default {
        name: '',
        data () {
            return {
                formName: {//表单中的参数
                    user: '',
                    userError: '',
                    password: '',
                    passwordError: '',
                    beDisabled: true
                },
                beShow: false//传值给父组件
            }           
        },
        computed:{
            username(){
                return this.formName.user
            },
            password(){
                return this.formName.password
            }
        },
        watch:{
            username(){
                //对于按钮的状态进行修改
                if (this.formName.user != '' && this.formName.password != '') {
                    this.formName.beDisabled = false;
                }else{
                    this.formName.beDisabled = true;
                }
            },
            password(){
                //对于按钮的状态进行修改
                if (this.formName.user != '' && this.formName.password != '') {
                    this.formName.beDisabled = false;
                }else{
                    this.formName.beDisabled = true;
                }
            }
        },
        methods: {
            resetForm(){
                this.formName.user = '';
                this.formName.userError = '';
                this.formName.password = '';
                this.formName.passwordError = '';
            },
            submitForm(formName){
                var submit_user_data = {
                    username : this.formName.user ,
                    password : this.formName.password
                } ;
                sessionStorage.clear()
                if (this.formName.user == '' && this.formName.password == '' ) {
                    return this.$alert("登录不能为空")
                }
                login(submit_user_data).then(res=>{
                    if (res.data.result == 'OK') {
                        //console.log(res,'=======')
                        this.$cookies.set('token',res.data.LoginToken,3600*12)//token过期时间为：12小时
                        this.$cookies.set('userId', res.data.user_id,3600*12)
                        this.$cookies.set('role', res.data.role_list,3600*12)
                        this.$cookies.set('userName', res.data.user_name,3600*12)
                        sessionStorage.setItem('login_user',res.data.user_id)
                        sessionStorage.setItem('login_user_data',JSON.stringify(res.data))
                        sessionStorage.setItem('menu_active','0')//设置menu高亮：项目
                        this.$message({
                            title: '提示',
                            type: 'success',
                            message: '登录成功!',
                            duration:3000,
                            // showClose:true
                        });
                        const redirect = decodeURIComponent(
                            this.$route.query.redirect || "/projQuoteList"
                        );
                        this.$router.replace({path: redirect});
                    }else{
                        if (res.data.result == 'NG') {
                            this.$alert('登录失败：'+res.data.error)
                            return
                        }
                        this.$message({
                            title: '提示',
                            type: 'info',
                            message: '用户名或密码错误！请重新登录！',
                            duration: 2000,
                            showClose: false
                        });
                    }
                }).catch(err=>{
                    console.log(err)
                })
                
            },
            inputBlur(errorItem,inputContent){
                if (errorItem === 'user') {
                    if (inputContent === '') {
                        this.formName.userError = '用户名不能为空'
                    }else{
                        this.formName.userError = '';
                    }
                }else if(errorItem === 'password') {
                    if (inputContent === '') {
                        this.formName.passwordError = '密码不能为空'
                    }else{
                        this.formName.passwordError = '';
                    }
                }
            }
        }
    }
</script>
<style lang="less" scoped>
    .wrapper{
        max-width: 1280px;
        min-width: 640px;
        // height: 100%;
        background: #ffffff;
        margin: 0 auto;
        .header{
            text-align: center;
            margin:60px 0 0;
            h1{
                display: inline-block;
                margin-left: 10px;
                font-size: 50px;
            }
        }
        .logo{
            width: 40px;
            height: 40px;
            border-radius: 10px;
            // background-image: url('../../../static/image/kaola.jpg');
        }
        
    }
    .loginPage{
        position: absolute;
        top: 35%;
        left: 50%;
        margin-top: -150px;
        margin-left: -175px;
        width: 350px;
        min-height: 300px;
        padding: 30px 20px 20px;
        border-radius: 8px;
        box-sizing: border-box;
        background-color: #dff4ff;
    }
    .loginPage p{
        color: #f56c6c;
        text-align: left;
        line-height: 12px;
        font-size: 12px
    }

</style>
