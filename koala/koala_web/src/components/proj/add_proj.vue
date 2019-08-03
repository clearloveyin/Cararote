<template>
    <div class="Project-content warpper">
        <div class="pro-content">
            <ul class="pro-nav">
                <div class="menu">
                    <el-breadcrumb separator-class="el-icon-arrow-right">
                        <el-breadcrumb-item>项目列表</el-breadcrumb-item>
                        <el-breadcrumb-item>项目详细</el-breadcrumb-item>
                        <el-breadcrumb-item>项目编辑</el-breadcrumb-item>
                    </el-breadcrumb>
                </div>
                <li>
                    <span @click="logout_pro()" class="cursor">[ 返回 ]</span>
                </li>
                <li>
                    <span @click="post_data()" class="cursor">[ 确认 ]</span>
                    <!-- v-if="show_edit_flag" -->
                </li>
            </ul>

            <div class="msg-box">
                <div class="detail-box">
                    <span>
                        <i class="detail-box-title">*</i>项目系列
                    </span>
                    <el-select
                        @change="change_proj_type(value_type)"
                        filterable
                        placeholder="请选择"
                        size="small"
                        v-model="value_type"
                    >
                        <el-option
                            :key="item.type_id"
                            :label="item.proj_type"
                            :value="item.proj_type"
                            v-for="item in value_type_options"
                        ></el-option>
                    </el-select>
                    <el-input
                        placeholder="手动输入"
                        size="small"
                        style="width:217px"
                        v-if="value_type_flag"
                        v-model="other_proj_type"
                    ></el-input>
                </div>
                <div class="detail-box">
                    <span>
                        <i class="detail-box-title">*</i>项目内部名称
                    </span>
                    <el-select
                        @change="change_inside_name(inside_name)"
                        filterable
                        placeholder="请选择"
                        size="small"
                        v-model="inside_name"
                    >
                        <el-option
                            :key="item.inside_id"
                            :label="item.inside_name"
                            :value="item.inside_name"
                            v-for="item in inside_name_options"
                        ></el-option>
                    </el-select>
                    <el-input
                        @blur="blur_inside_name(other_inside_name)"
                        placeholder="手动输入"
                        size="small"
                        style="width:217px"
                        v-if="inside_name_flag"
                        v-model="other_inside_name"
                    ></el-input>
                    <i style="color:red;" v-if="check_proj_flag">项目内部名称已存在</i>
                    <!-- <el-autocomplete
                        :fetch-suggestions="querySearch"
                        @select="handleSelect"
                        placeholder="请输入内容"
                        popper-class="my-autocomplete"
                        size="small"
                        v-model="inside_name"
                    >
                        <i
                            @click="handleIconClick"
                            class="el-icon-edit el-input__icon"
                            slot="suffix"
                        ></i>
                        <template slot-scope="{ item }">
                            <div class="name">{{ item.inside_name }}</div>
                        </template>
                    </el-autocomplete>-->
                </div>
                <div class="detail-box">
                    <span>
                        <i class="detail-box-title">*</i>项目客户名称
                    </span>
                    <el-input
                        class="outside_name_input"
                        placeholder="请输入项目客户名称"
                        size="small"
                        v-model="outside_name"
                    ></el-input>
                </div>

                <div class="detail-box">
                    <span>&nbsp;&nbsp;负责人</span>
                    <el-input
                        :disabled="true"
                        class="outside_name_input"
                        placeholder="请输入负责人"
                        size="small"
                        v-model="user_name"
                    ></el-input>
                </div>
                <div class="detail-box">
                    <span>&nbsp;&nbsp;PL</span>
                    <el-form
                        :model="dynamicValidateForm"
                        label-width="140px"
                        ref="dynamicValidateForm"
                    >
                        <el-form-item>
                            <el-button @click="addDomain()" size="small">新增加PL</el-button>
                            <!-- <el-button @click="resetForm('dynamicValidateForm')">重置</el-button> -->
                        </el-form-item>
                        <el-form-item
                            :key="domain.key"
                            :label="'PL-' + (index + 1)"
                            :prop="'domains.' + index + '.value'"
                            :rules="{required: false, message: '不能为空', trigger: 'blur'}"
                            v-for="(domain, index) in dynamicValidateForm.domains"
                        >
                            <el-select @change="change_insert_name(domain)"  class="form-item-title" size="small" v-model="domain.value" filterable 
                            >
                                <el-option
                                    :disabled="item.disabled"
                                    :key="item.user_id"
                                    :label="item.user_name"
                                    :value="item.user_id"
                                    v-for="item in user_list"
                                >
                                    <span style="float: left">{{ item.user_name }}</span>
                                    <span
                                        style="float: right; color: #8492a6; font-size: 13px"
                                    >{{ "工号"+item.work_id }}</span>
                                </el-option>
                            </el-select>
                            <el-button @click.prevent="removeDomain(domain)" size="small">删除</el-button>
                        </el-form-item>
                    </el-form>
                </div>

                <div class="detail-box">
                    <span>
                        <i class="detail-box-title">*</i>项目描述
                    </span>
                    <el-input
                        :rows="4"
                        class="describe_input"
                        placeholder="请输入内容"
                        type="textarea"
                        v-model="describe"
                    ></el-input>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { new_add_input, get_project_list, get_project_info, get_res_info, get_project_type, get_project_inside, add_project, change_project, get_user_data, get_project_check } from '@/api/content_api'
export default {
    name: 'proj_list',
    data() {
        return {
            value_type_options: [],
            inside_name_options: [],
            value_type: '',
            inside_name: "",
            outside_name: "",
            describe: "",
            proj_id: '',
            post_flag: true,
            new_inside_name: "",
            state3: '',
            user_list: [],
            temp_user_list: [],
            dynamicValidateForm: {
                domains: [{
                    value: '',
                    key: 0
                }],
                observer_value: ""
            },
            user_name: '',
            value_type_flag: false,
            inside_name_flag: false,
            check_proj_flag: false,
            other_inside_name: '',
            check_proj_data: [],
            other_proj_type: '',
        }
    },
    created() {
        // this.get_inside_name()
        this.proj_id = this.$route.params.pro_id
        this.promise_all()
    },
    mounted() {
        // this.get_value_type()
        // this.get_user_list()
        // this.get_data()
        // this.get_check_project()
    },
    watch: {
        $route(to, from) {
            this.proj_id = this.$route.params.pro_id
        }
    },
    methods: {
        promise_all(){
            const checkProject = new Promise((resolve,reject)=>{
                get_project_check().then(res => {
                    if (res.data.result == 'OK') {
                        // this.check_proj_data = res.data.content
                        resolve(res.data.content)
                    } else {
                        this.$message({
                            type: 'error',
                            message: res.data.error,
                        })
                    }
                })  
            }),
            get_project_info_func = new Promise((resolve,reject)=>{
                get_project_info(this.proj_id).then(res => {
                    resolve(res.data.content)
                })
            }),
            get_project_type_func = new Promise((resolve,reject)=>{
                get_project_type().then(res => {
                    if (res.data.result == "OK") {
                        resolve(res.data.content)
                    }
                })
            }),
            get_project_inside_func = new Promise((resolve,reject)=>{
                get_project_inside().then(res => {
                    if (res.data.result == "OK") {
                        resolve(res.data.content)
                    }
                })
            }),
            get_user_data_func = new Promise((resolve,reject)=>{
                get_user_data().then(res => {
                    if (res.data.result == 'OK') {
                        resolve(res.data.content)
                    }
                })
            })
            Promise.all([checkProject,get_project_info_func,get_project_type_func,get_project_inside_func,get_user_data_func]).then(data=>{
                console.log('data:',data);
                this.implement_data(data)
            })
        },
        implement_data(data){
            let implement_project_data = ()=>{
                this.post_flag = false
                this.check_proj_data = data[0]
            },
            implement_info = ()=>{
                this.outside_name = data[1].outside_name
                this.value_type = data[1].proj_i_type
                this.describe = data[1].describe
                this.user_name = data[1].user_name
                this.inside_name = data[1].inside_i_name
                this.dynamicValidateForm.domains = data[1].observer_list.map(item=>{
                    if (item.value == null) {
                        data[1].observer_list.pop(item)
                    }
                    return item
                })
            },
            implement_type = ()=>{
                let item = { 'proj_type': '其他', 'type_id': 0 }
                this.value_type_options = data[2]
                this.value_type_options.length !== 0 ? this.value_type_options.push(item) : this.value_type_options.length = 0
            },
            implement_inside = ()=>{
                let item = { 'inside_name': '其他', 'inside_id': 0 }
                this.inside_name_options = data[3]
                this.inside_name_options.length !== 0 ? this.inside_name_options.push(item) : this.inside_name_options.length = 0
            },
            implement_user_data = ()=>{
                this.user_list = this.check_select_user_list_data(data[4],this.dynamicValidateForm.domains)
                this.temp_user_list = JSON.parse(JSON.stringify(this.user_list))
            }
            implement_project_data()
            implement_info()
            implement_type()
            implement_inside()
            implement_user_data()
        },
        check_select_user_list_data(data,select_user_id_list){
            let login_user_id = Number(this.$cookies.get('userId'))
            let temp_user_id_list = select_user_id_list.map(id=>{//获取选择框已选过的userid集合
                    if (id.value !== '') {
                        return  id.value
                    }
                })
            let user_list = data.map(item=>{
                if (item.user_id == login_user_id || temp_user_id_list.indexOf(item.user_id) !==-1) {
                    item.disabled = true
                }else{
                    item.disabled = false
                }
                return item
            })
            return user_list
        },
        change_insert_name(val) {
            this.user_list = this.check_select_user_list_data(this.temp_user_list,this.dynamicValidateForm.domains)
        },
        removeDomain(item) {
            var index = this.dynamicValidateForm.domains.indexOf(item)
            if (index !== -1) {
                this.dynamicValidateForm.domains.splice(index, 1)
            }
            this.user_list = this.check_select_user_list_data(this.temp_user_list,this.dynamicValidateForm.domains)
        },
        resetForm(formName) {
            this.$refs[formName].resetFields();
        },
        addDomain() {
            this.dynamicValidateForm.domains.push(
                {
                    value: '',
                    key: Date.now()
                });

        },

        post_data() {
            let data = {
                "outside_name": this.outside_name,
                "proj_type": this.value_type == '其他' ? this.other_proj_type : this.value_type,
                "inside_name": this.inside_name == '其他' ? this.other_inside_name : this.inside_name,
                "describe": this.describe,
                "commit_user": this.$cookies.get('userId'),
                // 'new_inside_name': this.new_inside_name,
                'observer_list': this.dynamicValidateForm.domains,
                "user_name": this.user_name
            }
            const check_post_data = () => {
                for (const key in data) {
                    if (data.hasOwnProperty(key)) {
                        const element = data[key];
                        if (typeof (element) === 'string' && element.length === 0) {
                            switch (key) {
                                case 'outside_name':

                                    return false
                                case 'proj_type':

                                    return false
                                case 'describe':

                                    return false

                                case 'inside_name':

                                    return false
                                    break;
                                default:
                                    break;
                            }

                        }
                    }
                }
                return true
            }
            let flag = check_post_data(data)
            if (flag === false) {
                return this.$message({
                    type: "warning",
                    message: "有必填项未填！"
                })
            }
            change_project(this.proj_id, data).then(res => {
                if (res.data.result == "OK") {
                    this.$router.go(-1)
                    this.$message({
                        type: 'success',
                        message: '修改成功!',
                        duration: 2000,
                        showClose: false
                    })
                } else {
                    this.$message({
                        type: 'error',
                        message: res.data.error
                    })
                }
            })

        },
        logout_pro() {
            this.$confirm('是否退出?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.$router.go(-1)
                // window.sessionStorage.removeItem('proj_id')
            }).catch(() => {

            })
        },
        querySearch(queryString, cb) {
            var restaurants = this.inside_name_options;
            var results = queryString ? restaurants.filter(this.createFilter(queryString)) : restaurants;
            // 调用 callback 返回建议列表的数据
            cb(results);
        },
        createFilter(queryString) {
            return (restaurant) => {
                return (restaurant.inside_name.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
            };
        },
        handleSelect(item) {
            this.inside_name = item.inside_name
        },
        handleIconClick(ev) {
            console.log(ev, 'aaa');
        },
        
        change_proj_type(type) {
            if (type == '其他') {
                this.other_proj_type = ''
                this.value_type_flag = true
            } else {
                this.value_type_flag = false
            }
        },
        change_inside_name(type) {
            this.other_inside_name = ''
            this.check_proj_flag = false
            if (type == '其他') {
                this.inside_name_flag = true
            } else {
                this.inside_name_flag = false
                for (let item of this.check_proj_data) {
                    if (item.inside_name == type) {
                        this.check_proj_flag = true
                    }
                }
            }
        },
        blur_inside_name(val) {
            for (let item of this.check_proj_data) {
                if (val == item.inside_name) {
                    this.check_proj_flag = true
                } else {
                    this.check_proj_flag = false
                }
            }
        },
    }
}
</script>
<style scoped lang='less'>
.Project-content {
    width: 1280px;
    margin: 0 auto;
    height: 100%;
    overflow-y: scroll;
    color: #000000;
    font-size: 14px;
    .pro-content {
        /*float: left;*/
        height: 100%;
        background: #fff;
    }
    .pro-nav {
        width: 95%;
        height: 40px;
        line-height: 40px;
        padding-top: 20px;
        list-style: none;
        margin-left: 20px;
        .menu {
            // padding-left: 20px;
            width: 20%;
        }
    }
    .pro-nav li {
        float: right;
        margin: 0 10px;
        // font-size: 14px;
    }
    .msg-box {
        width: 800px;
        height: 70%;
        min-height: 540px;
        /*border:1px solid #ebebeb;*/
        border-radius: 3px;
        // margin: 30px 0 0 20px;
        padding-left: 20px;
        transition: 0.2s;
    }
    .detail-box {
        // height: 40px;
        // line-height: 40px;
        // margin:20px 0 0 20px;
        width: 100%;
        overflow: hidden;
        margin: 15px 0;
    }
    .detail-box span,
    .describe-box p {
        color: #5e6d82;
        // font-size: 14px;
        margin-right: 20px;
        font-weight: bold;
        display: block;
        float: left;
        width: 120px;
    }
    .outside_name_input {
        width: 400px;
    }
    .describe_input {
        width: 400px;
        // margin:0px 0 0 116px;
    }
    .describe-box {
        margin: 30px 0 0 20px;
    }
    .form-item-title {
        padding-left: 0px;
        margin-right: 10px;
    }
    .detail-box-title {
        color: red;
        margin-right: 2px;
    }
}
</style>