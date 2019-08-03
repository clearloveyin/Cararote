<template>
    <div class='warpper'>
        <!-- <div class="left-content-box"></div> -->
        <div class="content-box">
            <div class="menu">
                <el-breadcrumb separator-class="el-icon-arrow-right">
                    <el-breadcrumb-item >项目列表</el-breadcrumb-item>
                    <el-breadcrumb-item >项目详细</el-breadcrumb-item>
                    <el-breadcrumb-item>项目input资料列表</el-breadcrumb-item>
                </el-breadcrumb> 
            </div>
            <div class="content-box-header">
                <span class="project-title">项目</span>
                        <el-select v-model="proj_id" placeholder="请选择" @change="select_input" size="small" disabled>
                            <el-option v-for="item in project_list" :key="item.proj_id" :label="item.proj_type" :value="item.proj_id">
                            </el-option>
                        </el-select>
                        <span class="content-box-header-search-input" @keyup.enter="search_click(searchValue)">
                            <el-input clearable @clear="clear_click()" placeholder='搜索式样书标题' size="small"  v-model="searchValue" disabled>
                                <el-button slot="append" icon="el-icon-search" @click="search_click(searchValue)"></el-button>
                            </el-input>
                        </span>
                <span class="content-box-header-btn">
                    <span class="cursor padding-right" @click="add_input_data_fun('add')">
                        [ Input资料添加 ]
                    </span>
                    <span class="cursor" @click="cancel_fun">[ 返回 ]</span>
                </span>
            </div>
            <div class="content-box-content" >
                    <div class="label-box-text" >
                        <span v-for="(book,index) in book_data_list" :key="index" :class="{'active':index === inActive}" 
                            @click="click_book_fun(book.type,index)">[ {{book.book_name}} ]</span>
                    </div>
                    <el-table :data="tableData" border  v-loading="loading">
                        <el-table-column prop="resource_name" label="资料名称" min-width="200" align="left" header-align="center">
                        </el-table-column>
                        <el-table-column prop="ver_list" label="版本"  align="left" header-align="center" min-width="300">
                            <template slot-scope="scope">
                                <span class="go-doc-text" v-for="item in scope.row.ver_list"> 
                                    <span v-if="scope.row.type=='FILE'" class="cursor padding-right" @click="download_file(item,item.version_id,scope.row)">{{item.version_id}}</span>
                                    <span v-else @click="download_file(item,item.version_id,scope.row)"><a :href="url" target="_blank" rel="noopener noreferrer">{{item.version_id}}</a></span>
                                </span>
                            </template>
                        </el-table-column>
                        <el-table-column prop="name" label="操作" width="200" align="left" header-align="center">
                            <template slot-scope="scope">
                                <el-button size="mini" type="text" @click="add_new_book_fun('children',scope.row)">
                                    <span class="append-span" style="color:#606266;fontSize:14px;font-weight: none;"> &nbsp;[ 添加 ]</span>
                                </el-button>
                                <el-popover placement="right" trigger="click" width="200" >
                                    <el-table :data="gridData.ver_list" v-if="delete_input_flag">
                                        <el-table-column  property="version_id" label="版本号"></el-table-column>
                                        <el-table-column  property="id" label="操作">
                                            <template slot-scope="scope">
                                                <span @click="delete_input_ver(scope.$index,scope.row,'delete_ver')" style="fontSize:12px;cursor:pointer;"> &nbsp;[ 删除 ]</span>
                                            </template>
                                        </el-table-column>
                                    </el-table>
                                    
                                    <el-button slot="reference" size="mini" type="text"  @click="delete_input_fun(scope.$index,scope.row)">
                                        <span class="append-span" style="color:#606266;fontSize:14px;font-weight: none;"> &nbsp;[ 删除 ]</span>
                                    </el-button>
                                </el-popover>
                            </template>
                        </el-table-column>
                    </el-table>
            </div>
            <div class="content-box-footer">
                <!-- <el-button type="primary" size="small"  @click="submit_fun" >[ 确定 ]</el-button> -->
                <!-- <el-button size="small"  plain @click="cancel_fun">[ 返回 ]</el-button> -->
            </div>
        </div>
    </div>
</template>
<script>
import {new_add_input,get_project_list,get_project_info,get_input_info,delete_input} from '@/api/content_api'
export default {
    data () {
        return {
            book_data_list:[
                {'book_name':"文件",id:0,type:'FILE'},
                {'book_name':"文本",id:1,type:'TEXT'},
            ],
            inActive:0,
            searchValue:"",
            tableData:[],
            adaptivePageHeight: window.innerHeight - 300,
            project_list:[],
            proj_id:'',
            book_type:'FUNC',
            gridData:[],
            delete_input_flag:true,
            visible:false,
            loading:false,
            tableData:[],
            tableflag:false,
            url:'cell.html?input'
            // this.url = 'cell.html?proj_id='+ ;//传输proj_id给table页

        }

    },
    mounted () {
        this.default_mounted_fun()
    },
    methods: {
        default_mounted_fun(){
            this.proj_id = Number(this.$route.query.proj_id)
            this.get_project_list()
        },
        add_input_data_fun(type) {
            this.$router.push({path:'/Input/InputAddEdit',query:{proj_id:this.proj_id}})
        },
        get_project_list () {
            get_project_list().then(res=>{
                // console.log(res,'aaa')
                this.project_list = res.data.content
                this.click_book_fun('FILE',0)
            })
        },
        click_book_fun(type,num){
            this.inActive = Number(num)
            if (this.proj_id == '') {
                return this.$message({
                    type:'warning',
                    message:"请选择项目",
                    duration: 2000,
                    showClose: false
                })
            }
            this.loading = true
            get_input_info(this.proj_id,type).then(res=>{
                // console.log(res,'info')
                if (res.data.result == 'OK') {
                    this.tableData = res.data.content
                }
                this.loading = false
            })
        },
        search_click(val){
            
        },
        download_file(val,index,data){
            if (data.type == 'FILE') {
                window.open(val.url)
            } else {
                val.name = data.resource_name
                sessionStorage.setItem('input_version_data',JSON.stringify(val))
            }
        },
        clear_click () {
        },
        select_input () {
           return
        },
        add_new_book_fun(val,data){
            this.$router.push({path:'/Input/InputAddEdit',query:{'proj_id':this.proj_id,'resource_id':data.resource_id,type:data.type}})
        },
        delete_input_fun(index,data){
            // console.log(index,data)
            if (data.ver_list.length == 0) {//删除整本式样书
                this.delete_input_flag = false
                this.delete_input_ver(index,data,'delete')
                let delete_data={
                    resource_id: data.resource_id,
                    resource_data_id:''
                }
                delete_input(delete_data).then(res=>{
                    if (res.data.result == 'OK') {
                        this.$message({
                            type: 'success',
                            message:res.data.content,
                            duration: 2000,
                            showClose: false
                        })
                        this.tableData.splice(index, 1)
                    }
                    
                })     
            }else{//删除某版本式样书
                this.gridData = data
                this.delete_input_flag = true
            }
        },
        delete_input_ver(index,data,submit){//删除某版本式样书的方法
            let delete_data ={
                resource_id: this.gridData.resource_id,
                resource_data_id:data.id
            }
            delete_input(delete_data).then(res=>{
                if (res.data.result == 'OK') {
                    this.$message({
                        type: 'success',
                        message:res.data.content,
                        duration: 2000,
                        showClose: false
                    })
                    this.gridData.ver_list.splice(index, 1)
                }
                
            }) 
        },
        submit_fun(){
            
        },
        cancel_fun(){
			this.$router.push({ path: '/proj/pro_detail/' + this.proj_id })
        }
    }
}
</script>

<style lang="less" scoped>
// 通用大模块样式
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
    // 具体小模块样式
    .content-box-header{
        padding: 0 0 10px 0;
       
    }
    .project-title{
        margin-right: 20px;
    }
    .content-box-header-btn{
        float:right;
        margin-top:6px;
    }
    .content-box-header-search-input{
        display: inline-block
    }
    .content-box-content{
        padding: 10px 0 0 0;
    }
    .label-box-text{
        padding: 0px 0 20px 0;
        span{
            margin-right: 20px;
            cursor: pointer;
        }
    }
    .btn-color-active{

    }
    .active{
        font-size: 14px;
        color: #00a597;
    }
    .menu{
        padding: 0 0 20px 0
    }
    .content-box-footer{
        position: fixed;
        bottom: 100px;
        right: 100px;
    }
    .padding-right{
        padding-right: 20px;
    }
    .warpper a{
        color: #5e6d82;
        text-decoration: none;
    }
    
</style>
