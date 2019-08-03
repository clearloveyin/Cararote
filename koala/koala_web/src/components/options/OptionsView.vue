<template>
    <div class="warpper">
        <div class="container">
            <div class="menu">
                <el-breadcrumb separator-class="el-icon-arrow-right" >
                    <el-breadcrumb-item>{{title.feature_name}}</el-breadcrumb-item>
                    <el-breadcrumb-item>{{title.options_name}}</el-breadcrumb-item>
                </el-breadcrumb>
            </div>
            <div class="header border-left">
                <div class="btn">
                    <el-button  type="text" @click="submit_confirm">[ 下一步：再次确认feature ]</el-button>
                    <el-button  type="text" @click="return_prv">[ 返回 ]</el-button>
                </div>
                <el-input
                    class="inline-block input"
                    placeholder="option名称"
                    size="small"
                    type="textarea"
                    v-model="addOptionText"
                    autosize
                ></el-input>
                <el-button
                    class="inline-block margin-btn"
                    type="text"
                    @click="addOption"
                >[ 添加option]</el-button>
                <p class="border"></p>
            </div>
            <div class="middle border-left">
                <div >
                    <div class="checkbox_container" >
                        <ul>
                            <li v-for="(item,index) in options_list" :key="index">
                                <el-checkbox :label="item.id" v-model="item.checked" :disabled="item.value=='Default'">{{item.value}}</el-checkbox>
                                <i class="el-icon-delete" @click="delete_option(item,index)" v-if="item.disable_delete!=true"></i>
                            </li>
                        </ul>
    
                    </div>
                </div>
                <p class="border"></p>
            </div>
        </div>
    </div>
</template>
<script>
import {
    get_OptionCombination_list,
    update_OptionCombination_list,
    delete_OptionCombination_list
} from '@/api/content_api'
export default {
    
    data() {
        return {
            title: {
                feature_name: 'Feature分配',
                proj_name: "",
                options_name: "option填写",
                version: ''
            },
            addOptionText: '',
            quotation_id:0,
            proj_id:0,
            checkList:[],
            options_list:[],
            add_option_list:[],
            add_options_value_list:[],
            excel_table:false,
            readOnly:true
        }
    },
    mounted() {
        this.default_mounted()        
    },
    methods: {
        default_mounted(){
            // console.log(this.$route.query)
            this.quotation_id = Number(this.$route.query.quotation_id)
            this.proj_id = Number(this.$route.query.proj_id)
            get_OptionCombination_list(this.quotation_id).then(res=>{
                // console.log(res,'---------------')
                for (const item of res.data.content) {
                    if (item.value == "Default") {
                        this.checkList.push(item.id)
                    }
                }
                this.options_list = res.data.content
            })
        },
        addOption() {
            if (this.addOptionText !== '') {
                let newAddObj = {value:this.addOptionText,id:0,quotation_id:this.quotation_id,proj_id:this.proj_id,disable_delete:false,checked:true}
                this.options_list.push(newAddObj)
            }
            setTimeout(()=>{
                this.addOptionText =''
            },0)
        },
        return_prv() {
            this.$router.back(-1)
        },
        submit_confirm(){
            this.submit_post()
        },
        submit_post(){
            let data = this.options_list
            update_OptionCombination_list(data,this.quotation_id).then(res=>{
                // console.log(res,'aaaaaaa');
                if (res.data.result == 'OK') {
                    this.$message({
                        type:"success",
                        message:"成功！"
                    })
                    console.log(this.quotation_id,'this.quotation_id')
                    this.$router.push({path:'/featurePage/ConfirmFeature',query:{quotation_id:this.quotation_id,proj_id:this.proj_id}})
                } else {
                    this.$message({
                        type:"error",
                        message:res.data.error
                    })
                }
                
            })
        },
        delete_option(item,index){
            // console.log(item,index);
            if (item.id == 0) {
               this.options_list.splice(index,1) 
            } else {
                delete_OptionCombination_list(item.id).then(res=>{
                    // console.log(res,'============')
                    if (res.data.result == "NG") {
                        this.$message({
                            type:"error",
                            message:res.data.error
                        })
                    }else if(res.data.result == "OK"){
                        this.options_list.splice(index,1) 
                    }
                })
            }
        },
        review_feature(){
            this.excel_table = true;
        },
        close_review_feature(){
            this.excel_table = false;
        },
        getChildPlugData(data){
            
           
        }
        
    }
}
</script>
<style scoped lang="less">
.warpper{
    height: 100%;
}
.container {
    width: 1280px;
    height: 100%;
    margin: 0 auto;
    background: #fff;
    .input{
        width: 350px;
    }
    .border {
        border-bottom: 1px solid rgb(197, 194, 194);
        margin-top: 10px;
        // margin-right: 20px;
    }
    .border-left {
        margin-left: 15px;
        margin-right: 15px;
    }
    .checkbox_container {
        padding-left: 10px;
        background-color: rgb(242, 245, 240);
    }
}
.menu{
    padding: 10px 0 0 20px;
}
.header,
.middle,
.footer {
    line-height: 30px;
    padding: 20px 20px 0 20px;
}

.inline-block {
    display: inline-block;
    cursor: pointer;
}
.margin-btn {
    margin-left: 10px;
}
.confirm {
    margin-left: 213px;
}
.title {
    /* margin-top: 20px; */
    display: inline-block;
    width: 100px;
    font-weight: 600;
}
.el-checkbox-group {
    display: inline-block;
}
.checkbox {
    width: 745px;
    vertical-align: top;
}

.btn {
    float: right;
    padding-right: 40px;
    cursor: pointer;
}
ul li{
    list-style: none;
    width: 25%;
}
.el-icon-delete{
    float: right;
    margin: 8px 0 0 0;
    cursor: pointer;
}
.el-icon-d-arrow-left,.el-icon-d-arrow-right{
    transform:rotate(-90deg);    
}
.excel-table{
    position: absolute;
    top: 80px;
    left: 0;
    width: 100%;
    background-color: #ffffff;
    z-index: 100;
}

.color{
    color: #000000;
}
.cursor{
    cursor: pointer;    
}
.el-icon-close{
    float: right;
    margin-right: 15px;
}
</style>