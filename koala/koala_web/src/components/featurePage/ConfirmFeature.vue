<template>
    <div class="warpper">
        <div class="content-box" v-loading="loading">
            <div class="content-box-header">
                <div class="menu">
                    <el-breadcrumb separator-class="el-icon-arrow-right">
                        <el-breadcrumb-item>{{title.feature_name}}</el-breadcrumb-item>
                        <el-breadcrumb-item>{{title.proj_name}}</el-breadcrumb-item>
                        <el-breadcrumb-item>{{title.quotation_name}}</el-breadcrumb-item>
                        <el-breadcrumb-item>{{title.version}}</el-breadcrumb-item>
                    </el-breadcrumb>
                </div>
                <span class="content-box-header-btn" v-show="show_btn_flag">
                    <el-button type=text v-if="SGL" @click="confirm" class="cursor padding-right" :disabled="confirm_flag">[ 确认发布 ]</el-button>
                    <!-- <span @click="save" class="cursor padding-right">{{save_btn}}</span> -->
                    <span @click="return_fun" class="cursor">[ 返回 ]</span>
                </span>
            </div>
            <div class="color">
                <ExcelTabel ref="excel" :readOnly="readOnly" @listenExcelTabelEvent="getChildPlugData"></ExcelTabel>
            </div>
        </div>
    </div>
</template>
<script>

import {
    new_add_input,
    get_project_list,
    get_project_info,
    get_input_info,
    delete_input,
    get_feature_list,
    feature_list_assign,
    get_project_group_list,
    get_user_delete_manage,
    get_project_group_list_children,
    update_quotation_status,
    get_quotation_status
} from "@/api/content_api";
import ExcelTabel from "../plugins/PlugFeatureList";
export default {
    components:{
        'ExcelTabel':ExcelTabel
    },
    data() {
        return {
            adaptivePageHeight: window.innerHeight - 200,
            loading: false,
            proj_id: null,
            quotation_id: null,
            title: {
                feature_name: 'Feature分配',
                proj_name: "",
                quotation_name: "",
                version: ''
            },
            // 分割线
            save_btn: "[ 保存 ]",
            show_btn_flag: true,
            SGL:this.$cookies.get("role").indexOf('SGL'),
            readOnly:true,
            confirm_flag:false

        };
    },
    mounted() {
        this.quotation_id = this.$route.query.quotation_id
        this.default_mounted()
    },
    methods: {
        default_mounted(){
            get_quotation_status(this.quotation_id).then(res=>{
                if (res.data.result == "OK") {
                    if (res.data.content == '2') {
                        this.confirm_flag = true
                    }
                }
            })
        },
        confirm() {
            // this.$refs.excel.status()
            console.log(this.quotation_id)
            let data ={
                quotation_id:this.quotation_id
            }
            update_quotation_status(data).then(res=>{
                if (res.data.result =='OK') {
                    this.$message({
                        type:"success",
                        message:"发布成功"
                    })
                    this.$router.push("/projQuoteList")
                } else {
                    this.$message({
                        type:"error",
                        message:res.data.error
                    }) 
                }
            })
        },
        next_option() {
            this.$refs.excel.next_option()
        },
        return_fun() {
            this.$router.push('/proj/projQuoteList')
        },
        getChildPlugData(data){
            this.save_btn = data.btn_name
            this.title = data.title
            this.show_btn_flag = data.show_flag
        }
    }
};
</script>

<style lang="less" scoped>
// 通用大模块样式
.warpper {
    width: 100%;
    height: 100%;
    font-size: 14px;
    background: #fff;
    position: absolute;
    top: 82px;
}
.content-box {
    width: 100%;
    // margin: 0 20px 0 20px;
}
// 具体小模块样式
.content-box-header {
    width: 100%;
    height: 25px;
    line-height: 25px;
    margin: 20px 0 20px 0;
}

.content-box-header-btn {
    float: right;
    padding-right: 50px;
}
.content-box-content {
    width: 100%;
    height: 95%;
}

.padding-right {
    padding-right: 20px;
}
.warpper a {
    color: #5e6d82;
    text-decoration: none;
}
.warpper .e-dialog {
    background-color: rgb(255, 255, 255, 0.6);
    border: 1px solid #333;
    height: 160px;
}
.warpper > .el-dialog__header,
.el-dialog__body {
    padding: 0;
    padding-bottom: 0px;
}

.dialog-content {
    font-size: 14px;
    // cursor: pointer;
}
.warpper .el-table .cell {
    padding-left: 0;
    padding-right: 0;
}
.warpper .el-select {
    width: 100%;
}
.menu {
    padding-left: 20px;
}
.color{
    color: #000000;

}

</style>
<style>
.wtHolder {
    height: 650px;
}
</style>

