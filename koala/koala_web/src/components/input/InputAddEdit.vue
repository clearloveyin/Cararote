<template>
    <div class='warpper'>
        <!-- <div class="left-content-box"></div> -->
        <div class="content-box">
            <div class="menu">
                <el-breadcrumb separator-class="el-icon-arrow-right">
                    <el-breadcrumb-item >项目列表</el-breadcrumb-item>
                    <el-breadcrumb-item >项目详细</el-breadcrumb-item>
                    <el-breadcrumb-item >项目input资料列表</el-breadcrumb-item>
                    <el-breadcrumb-item>项目input资料添加</el-breadcrumb-item>
                </el-breadcrumb> 
            </div>
            <div class="content-box-header">
                <div class="content-box-header-left title"></div>
                <div class="content-box-header-right">
                    <el-button type="text" size="small"  @click="submit_fun" >[ 保存 ]</el-button>
                    <el-button type="text" size="small"  @click="cancel_fun">[ 返回 ]</el-button>
                </div>
            </div>
            <div ></div>
            <div class="content-box-content" >
                    <div class="content-box-content-children">
                        <div class="display-content">
                            <span>项目</span>
                        </div>
                        <el-select v-model="input_data.proj_id" placeholder="" @change="select_project" disabled>
                            <el-option v-for="item in project_list" :key="item.proj_id" :label="item.proj_type" :value="item.proj_id" >
                            </el-option>
                        </el-select>
                    </div>
                   
                    <div class="content-box-content-children">
                        <div class="display-content">
                            <span>版本</span>
                        </div>
                        <div class="el-select">
                            <el-input  v-model="input_data.version_id"  placeholder="请填写input版本"></el-input>
                        </div>
                    </div>
                    <div class="content-box-content-children">
                        <div class="display-content">
                            <span >选择上传类型</span>
                        </div>
                        <div class="el-select local-element">
                            <el-switch
                                style="display: block"
                                v-model="select_upload_input_type_value"
                                active-color="#00A597"
                                inactive-color="#00A597"
                                active-text="文件"
                                inactive-text="文本"
                                :disabled="select_upload_input_flag"
                                >
                            </el-switch>
                        </div>
                        
                    </div>
                    <div class="content-box-content-children local-element" v-if="select_upload_input_type_value">
                        <div class="display-content">
                            <span></span>
                        </div>
                        <div class="el-select">
                            <el-upload  ref="upload" :action="upload_api"  :data="input_data" 
                            :auto-upload="false" :on-success='up_success' :on-error="up_error" :before-upload="before_upload">
                                <el-button size="small" style="width:100%" type="primary" @click="upload_click_fun">上传</el-button>
                            </el-upload>
                        </div>
                    </div>
                    <div class="content-box-content-children local-element" v-else>
                        <div class="display-content local-span">
                            <span >文本标题</span>
                        </div>
                        <div class="el-select">
                                <el-input  v-model="input_data.title"  placeholder="请填写上传文本的标题"></el-input>
                                <el-input class="textarea-input" type="textarea" v-model="input_data.text"  :autosize="{ minRows: 4, maxRows: 30}"></el-input>
                        </div>
                    </div>
                   
            </div>
            <div class="content-box-footer">    
                <!-- <el-button type="primary" size="small"  @click="submit_fun" >[ 确定 ]</el-button>
                <el-button size="small"  plain @click="cancel_fun">[ 返回 ]</el-button> -->
            </div>
        </div>
    </div>
</template>
<script>
import {new_add_input,get_project_list,get_project_info} from '@/api/content_api'
export default {
    data () {
        return {
            input_title_name:'Input 资料添加',
            project_list:[],
            input_data:{
                'proj_id':'',
                'version_id':'',
                'type':'',
                'resource_id':0,
                'commit_user':'',
                'text':'',
                title:''
            },
            select_upload_input_type_value: true,//true是文件，false是文本
            select_upload_input_flag:false,
            upload_api : window.g.baseURL + "/InputUpload",
        }
    },
    mounted() {
        this.default_mounted()
    },
    methods: {
        default_mounted(){
            get_project_list().then(res=>{
                this.project_list = res.data.content
            })
            this.input_data.proj_id = Number(this.$route.query.proj_id)
            if (this.$route.query.resource_id) {
                this.input_data.resource_id = Number(this.$route.query.resource_id)
                if (this.$route.query.type == 'FILE') {
                    this.select_upload_input_flag = true//当添加子的时候，滑块开关始终是默认禁止操作状态
                    this.select_upload_input_type_value = true
                }else if(this.$route.query.type == 'TEXT'){
                    this.select_upload_input_flag = true//当添加子的时候，滑块开关始终是默认禁止操作状态
                    this.select_upload_input_type_value = false
                }
            }
        },
        select_project(){

        },
        upload_file_headers_fun(file){
            this.form_data.append('file', file.file);
        },
        upload_click_fun () {
            this.$refs.upload.clearFiles()//清除上传文件列表
            const token = window.sessionStorage.getItem('token')
            return//暂时屏蔽token
            if (token) {
                this.http_header.token = token
                this.http_header.Authorization = 'Token ' + token;
            }
        },
        before_upload(file){
            // console.log(file,'aaaaasssss')
            if (!file) {
                this.$alert('上传文件为空')
                return false
            }
        },
        up_success(response, file, fileList){
            if (response.result == 'OK') {
                this.$message({
                    type: 'success',
                    message: '上传成功!',
                    duration: 2000,
                    showClose: false,
                })
            }
        },
        up_error(err, file, fileList){
            this.$message({
                type: 'error',
                message: '上传失败!'+ err.data.error,
                duration:0,
                showClose: true,
            })
        },
        submit_fun(){
            this.input_data.commit_user = Number(this.$cookies.get('userId'))
            if (this.select_upload_input_type_value) {
                this.input_data.type = "FILE"
                this.$refs.upload.submit();//文件提交
            } else {
                this.input_data.type = "TEXT"
                console.log(this.input_data,'--')
                new_add_input(this.input_data).then(res=>{//文本提交
                    console.log(res,'ssssss')
                    if (res.data.result == 'OK') {
                        this.$message({
                            type: 'success',
                            message: '上传成功!',
                            duration: 2000,
                            showClose: false,
                        })
                    }else{
                        this.$message({
                            type: 'success',
                            message: '失败!'+ res.data.error,
                            duration:0,
                            showClose: true,

                        })
                    }
                }).catch(err=>{

                })   
            }
        },
        cancel_fun(){
            this.$router.push({path:'/Input/InputList',query:{proj_id:this.input_data.proj_id}})
        }
    }
}
</script>

<style lang="less" scoped>
    .warpper{
        display:flex;
        width: 98%;
        height: 100%;
        font-size: 14px
    }
    // .left-content-box,.content-box{
    //     float: left;
    //     height: 100%;
    // }
    // .left-content-box{
    //     width: 300px;
	// 	border-right: solid 1px #e6e6e6;
    // }
    .content-box{
        width: 1280px; 
        margin: 0 auto;
        padding: 20px 20px 0 20px;
    }
    .content-box-header{
        padding: 0 0 20px 0;
        .content-box-header-left{
            float: left;
        }
        .content-box-header-right{
            float: right;
        }
        .el-button + .el-button{
            margin-left: 20px
        }
    }
    .content-box-content{
        width: 100%;
        padding: 10px 0 0 0;
        clear: both;
        .display-content{
            display: inline-flex;
            width: 150px;
            span{
                margin-right: 20px;
            }
            
        }
        
        .local-span{
            height: 50px;
            line-height: 35px;
            vertical-align: top
        }
        .el-select{
            width: 40%;
        }

        .content-box-content-children{
            margin: 0 0 20px 0px;
            
        }
    }
    .content-box-footer{
        position: fixed;
        bottom: 100px;
        right: 100px;
    }
    .menu{
        padding: 0 0 20px 0
    }
    .textarea-input{
        margin-top: 20px
    }
    .title{
        font-size: 18px;
        font-weight: 600
    }
</style>
