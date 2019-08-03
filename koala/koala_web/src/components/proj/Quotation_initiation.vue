<template>
	<div class="Project-content warpper" >
		<div class="pro-content" v-loading="loading">
			<ul class='pro-nav'>
                <div class="menu">
                    <el-breadcrumb separator-class="el-icon-arrow-right">
                        <el-breadcrumb-item >项目列表</el-breadcrumb-item>
                        <el-breadcrumb-item >项目详细</el-breadcrumb-item>
                        <el-breadcrumb-item>项目发起报价</el-breadcrumb-item>
                    </el-breadcrumb> 
                </div>
				<li>
					<span @click="back()">[ 返回 ]</span>
				</li>
				<li>
					<span @click="save('ruleForm')">[ 下一步：发起报价 ]</span>
				</li>
			</ul>
			<div class="msg-box" >
				<el-form :model="ruleForm" :rules="rules" ref="ruleForm"  label-width="100px" class="demo-ruleForm">
					<el-form-item label="Base版本" prop="base_vaule">
						<!-- <el-input v-model="ruleForm.base_vaule"></el-input> -->
						<el-select v-model="ruleForm.base_vaule" placeholder="请选择继承版本" @clear="clear_value" @change='select_base(ruleForm.base_vaule)' 
						clearable filterable>
							<el-option
							v-for="item in base_vaule_data"
							:key="item.quotation_id"
							:label="item.show_name"
							:value="item.quotation_id">
							</el-option>
						</el-select>
					</el-form-item>
					<el-form-item label="报价名称" prop="quotation_name">
						<el-input v-model="ruleForm.quotation_name"></el-input>
					</el-form-item>
					<el-form-item label="Feature List" prop="">
						<el-button class="left" v-show="base_version_flag" type="text" @click="go_to_feature_list(ruleForm.base_vaule)">[ Base版本的FeatureList查看 ]</el-button>
						<el-upload ref="upload" :headers="http_header" :action="upload_api" :auto-upload="true" :on-success='up_success' 
						:on-remove="on_remove" :on-error="up_error" :before-upload="before_upload" style="width:200px;display: inline-block">
							<el-button class='footer-btn' type="primary" @click="upload_click_fun" style="display：inline-block">上传新FeatureList</el-button>
                        </el-upload>

					    <a :href="template_download_address" style='margin-right:10px;'>模板下载</a>

					</el-form-item>
					<el-form-item label="描述" prop="describe">
						<el-input v-model="ruleForm.describe" type="textarea" :rows="3"></el-input>
					</el-form-item>
					
				</el-form>

			</div>
			<div class="msg-box-footer">
			</div>
		</div>
	</div>
</template>
<script>
import {get_quotation_data, add_quotation_data} from '@/api/content_api'
	export default {
		data () {
			return {
				upload_api : window.g.baseURL +'/feature/import',
				props:{
					label:"show_name",
					value:"quotation_id",
				},
				base_version_flag:false,
				base_vaule_data:[],
				ruleForm:{
					"proj_id" : 0,
					"commit_user" : this.$cookies.get('userId'),
					quotation_name:'',
					quotation_id:0,
					base_vaule:'',
					base_id:0,
					describe:"",
					file_url:''
				},
				rules: {
					base_vaule: [
						 { required: false, message: '继承的base版本', trigger: 'change' }
					],
					quotation_name: [
						{ required: true, message: '报价名称', trigger: 'change' }
					],
					describe:[
						{ required: true, message: '请输入描述内容', trigger: 'blur' },
					]
				},
				loading:false,
                http_header:{},
                template_download_address:window.g.baseURL+"/static/template/FeatureList_template_ver0.1.xlsx"
			}
		},
		mounted() {
		    this.ruleForm.proj_id = Number(this.$route.params.pro_id)
		    this.get_data()
		},
		watch: {
		    $route(to, from) {
		        this.ruleForm.proj_id = Number(this.$route.params.pro_id)
		    }
		},
		methods: {
			get_data(){
				get_quotation_data(this.ruleForm.proj_id).then(res=>{
				    if(res.data.result == 'OK'){
						this.base_vaule_data = res.data.content.qu_list
				    }
				})
			},
			select_base(quotation){
				if(quotation.length == 0){
					this.base_version_flag = false 
				}else{
					this.base_version_flag = true
				}
				this.clear_value()
				for (let item of this.base_vaule_data) {
					if (item.quotation_id == quotation) {
						this.ruleForm.quotation_name = item.quotation_name
						break
					}
				}
				this.ruleForm.base_id = quotation
			},
			clear_value(){
				this.ruleForm.quotation_name = ''
				this.ruleForm.base_id = 0
			},
			up_success(response, file, fileList){
				// console.log(response, file, fileList,'=============')
			    if (response.result == 'OK') {
			        this.$message({
			            type: 'success',
			            message: 'feature上传成功!',
			            duration: 2000,
			            showClose: false,
					})
					this.ruleForm.file_url = response.content.file_url					
			    }else{
			    	this.up_error("","","",response.error)
			    }
			},
			up_error(err, file, fileList, error){
			    this.$message({
			        type: 'error',
			        message: 'feature上传失败!'+ error,
			        duration:0,
			        showClose: true,
			    })
			},
			before_upload(file){
				return true
			},
			on_remove(file, fileList){
				this.ruleForm.file_url = ''					
			},
			upload_click_fun () {
				this.$refs.upload.clearFiles()//清除上传文件列表
			    const token = this.$cookies.get("token")
			    if (token) {
			        this.http_header.Authorization = 'Token ' + token;
			    }
			},
			save(ruleForm){
				// console.log(this.ruleForm,'AAAAAAAA')
				this.$refs[ruleForm].validate((valid) => {
					if (valid) {
						// alert('submit!');
						if (this.ruleForm.file_url !='') {//
							this.ruleForm.quotation_id = 0
							this.ruleForm.base_id = 0
						}
						if (this.ruleForm.base_vaule == '' && this.ruleForm.file_url =='') {
							return this.$alert("FeatureList或者Base版本漏选")
						}
						this.loading = true
						add_quotation_data(this.ruleForm).then(res=>{
							if (res.data.result == 'OK') {
								this.$message({
									type:"success",
									message:"成功！",
                                    duration: 3000,
                                    showClose: false
								})
								let quotation_id = res.data.content
								setTimeout(()=>{
									this.$router.push({path:'/featurePage/FeatureList',query:
									{'quotation_id':quotation_id,'proj_id':this.ruleForm.proj_id,type:"assign_to"}})
								})
							}else{
								this.$message({
									message: res.data.error,
									type: 'error',
									showClose: true,
									duration: 0
								})
							}
							this.loading=false
						}).catch(error=>{
							console.log(error,"捕获error")
							this.$message({
								message: "服务器错误",
								type: 'error',
								showClose: true,
								duration: 0
							})
							this.loading=false
						})

					} else {
						return false;
					}
				});
			},
			back(){
				// this.$router.push({ path: '/proj/pro_detail/' + this.pro_id })
				this.$router.back(-1)
			},
			uploadFile(file){
				// this.formData.append('file', file.file)
			},
			
			go_to_feature_list(quotation_id){
				 const {href} = this.$router.resolve({
					name: 'FeatureList',
					path: '/featurePage/FeatureList',
					query: {'quotation_id':quotation_id,'proj_id':this.ruleForm.proj_id,btn:"none"}
				});
				window.open(href, '_blank')
				// this.$router.push({path:'/featurePage/FeatureList',query:{'quotation_id':quotation_id,'proj_id':this.ruleForm.proj_id}})
			}
		}
	}
</script>
<style scoped>
	.Project-content{
		font-size: 14px;
	}
	ul,li{list-style: none;}
	.Project-content{
		height: 100%;
	}
	.pro-tree{
		width:300px;
		border-right: solid 1px #e6e6e6;
	}
	.pro-content{
		width: 1280px;
		margin: 0 auto;
		background: #fff;
		height: 100%;
	}
	.table-box,.add-box{
		width:95%;
		margin:20px 0 0 20px;
	}
	.add-box{
		height: 20px;
		line-height: 20px;
	}
	.add-box span{
		float: right;
		cursor: pointer;
	}
	.pro-nav{
		width: 95%;
		height: 40px;
		line-height: 40px;
		padding-top: 20px;
		list-style: none;
		margin-left: 20px;
	}
	.pro-nav li {
		float: right;
		margin: 0 10px;
		cursor: pointer;
	}
	.msg-box{
		margin-top: 20px;
	}
	.msg-ul{
		width: 95%;
		margin-left: 20px;
		overflow: hidden;
	}
	.msg-ul li{
		width: 100%;
		overflow: hidden;
		margin: 20px 0;
	}
	.msg-title,.msg-content{
		float: left;
	}
	.msg-title{
		width: 150px;
		color: #5e6d82;
		font-weight: bold;
		line-height: 40px;
	}
	.msg-content{
		font-size: 14px;
		font-weight: 500;
		color: #5e6d82;
	}
	.outside_name_input{
		width: 350px;
	}
	.describe{
		width: 500px;
	}
	.left{
		float: left;
		padding-right: 155px;
	}
	.msg-box-footer{
		width: 1280px;
		margin-left: 50%
	}
	.el-input,.el-textarea{
		width: 500px
	}
	
</style>
