<template>
	<div class="Project-content">
		<div class="pro-content">
			<h1 class='title_h1'>
				<div class="menu">
                    <el-breadcrumb separator-class="el-icon-arrow-right">
                        <el-breadcrumb-item >项目列表</el-breadcrumb-item>
                        <el-breadcrumb-item>项目详细</el-breadcrumb-item>
                        <el-breadcrumb-item>体制表</el-breadcrumb-item>
                    </el-breadcrumb> 
                </div>
				<span style="float:right;font-size:14px;font-weight:500;cursor:pointer" @click='cancel_fun()'>[ 返回 ]</span>
			</h1>
<!-- 			<div class="detail-box">
				<span>体制表模板:</span>
				<a href="http://192.168.64.172:8081/koala/template/开发体制_template_ver0.1.xlsx">点击下载</a>
			</div>
			<div class="detail-box">
				<span>体制表:</span>
				<el-upload ref="upload" :action="upload_api" :data="data_json" 
				:on-success='up_success' :on-error="up_error" :show-file-list='false'>
				    <el-button type="text">点击上传</el-button>
				</el-upload>
			</div> -->
			<ul class="project-tree-title">
				<li class="tree-table-title">
					<span class="group cl">组/组员</span>
					<span class="person cl">负责人</span>
					<!-- <span class="direct-population cl">直属人数</span> -->
					<!-- <span class="total-number cl">总人数</span> -->
					<span class="operation cl">操作</span>
				</li>
			</ul>
			<ul class="project-tree" style="max-height:650px">
				<li class="tree-node-li clearfix node-first" v-for='(node_msg,node_index) in tree_data' :key="node_index">
					<div class="bg">
						<span class="group cl tree-node" @click='node_click(node_index)'> 
							<i class="el-icon-arrow-right"></i>
							{{node_msg.proj_name}}
						</span>
						<span class="person cl"> {{node_msg.owner_user.user_name}}</span>
						<!-- <span class="direct-population cl"> 20</span> -->
						<!-- <span class="total-number cl"> 20</span> -->
						<span class="operation cl tree-node" style="text-align:center"> 
							<el-button type="text" @click='add_group(node_msg)' :disabled="node_msg.permissions.length==0">增加组</el-button>
							<!-- <el-button type="text" @click='add_group_user(node_msg)'>增加成员</el-button> -->
							<!-- <el-button type="text">退出</el-button> -->
						</span>
					</div>
					<!-- 第二层 -->
					<ul style="border:0 none;">
						<li class="tree-node-li clearfix node-second" v-for='(node_msg_cl,node_index_cl) in node_msg.sub' :key="node_index_cl">
							<div class="bg">
								<span class="group cl tree-node" @click='node_click_second(node_index,node_index_cl)'> 
									<span style="padding-left:20px;">
										<i class="el-icon-arrow-right"></i>
										{{node_msg_cl.group_name}}
									</span>
								</span>
								<span class="person cl"> {{node_msg_cl.owner_user.user_name}}</span>
								<!-- <span class="direct-population cl"> 20</span> -->
								<!-- <span class="total-number cl"> 20</span> -->
								<span class="operation cl tree-node" style="text-align:center"> 
									<el-button type="text" @click='add_group(node_msg_cl)' :disabled="node_msg_cl.permissions.length==0">增加组</el-button>
									<!-- <el-button type="text">增加成员</el-button> -->
									<el-button type="text" @click="edit_group(node_msg_cl,node_msg)" :disabled="node_msg_cl.permissions.length==0">编辑</el-button>
									<el-button type="text" @click='delete_group(node_msg,node_index_cl,node_msg_cl.group_id)' :disabled="node_msg_cl.permissions.length==0">退出</el-button>
								</span>
							</div>
							<!-- 第三层 -->
							<ul style="border:0 none;">
								<li class="tree-node-li clearfix" v-for='(last_node, last_node_index) in node_msg_cl.sub' :key="last_node_index">
									<ul style="border:0 none;"  v-if='false'>
										<li class="tree-node-li clearfix">
											<div class="bg">
												<span class="group cl tree-node"> 
													<span style="padding-left:40px;">
														name +工号
													</span>
												</span>
												<span class="person cl"> 负责人</span>
												<!-- <span class="direct-population cl"> 20</span> -->
												<!-- <span class="total-number cl"> 20</span> -->
												<span class="operation cl tree-node" style="text-align:center"> 
													<el-button type="text">退出</el-button>
												</span>
											</div>
										</li>
									</ul>
									<div class="bg">
										<span class="group cl tree-node"> 
											<span style="padding-left:40px;">
												<i class="el-icon-arrow-right"></i>
												{{last_node.group_name}}
											</span>
										</span>
										<span class="person cl"> {{last_node.owner_user.user_name}}</span>
										<!-- <span class="direct-population cl"> 20</span> -->
										<!-- <span class="total-number cl"> 20</span> -->
										<span class="operation cl tree-node" style="text-align:center">
											<!-- <el-button type="text">增加成员</el-button> -->
											<el-button type="text" @click="edit_group(last_node,node_msg_cl)" :disabled="last_node.permissions.length==0">编辑</el-button>
											<el-button type="text" @click='delete_group(node_msg_cl,last_node_index,last_node.group_id)'
                                            :disabled="node_msg_cl.permissions.length==0">退出</el-button>
										</span>
									</div>
									<!-- 第四层 -->
									<ul style="border:0 none;"  v-if='false'>
										<li class="tree-node-li clearfix">
											<div class="bg">
												<span class="group cl tree-node"> 
													<span style="padding-left:60px;">
														name +工号
													</span>
												</span>
												<span class="person cl"> 负责人</span>
												<!-- <span class="direct-population cl"> 20</span> -->
												<!-- <span class="total-number cl"> 20</span> -->
												<span class="operation cl tree-node" style="text-align:center"> 
													<el-button type="text">退出</el-button>
												</span>
											</div>
										</li>
									</ul>
								</li>
							</ul>
						</li>
					</ul>
				</li>
			</ul>
		</div>
		<!-- 增加组 -->
		<el-dialog
		  :title="dialog_title" :visible.sync="dialogVisible" :append-to-body="true" width='40%'>
		    <p>
		  	  <span>组名:</span>
		  	  <el-input v-if="dialog_title =='编辑组' " v-model="group_name" placeholder="请输入组名" class='ipt'></el-input>
		  	  <el-autocomplete v-else
		  	    popper-class="my-autocomplete"
		  	    v-model="group_name"
		  	    :fetch-suggestions="querySearch"
		  	    placeholder="请输入内容"  @select="handleSelect"
				class='ipt'
		  	    >
		  	    <i
		  	      class="el-icon-edit el-input__icon"
		  	      slot="suffix">
		  	    </i>
		  	    <template slot-scope="{ item }">
		  	      <div class="name">{{ item.group_name }}</div>
		  	    </template>
		  	  </el-autocomplete>
		    </p>
		    <p style="margin-top:10px;">
		    	<span>组长:</span>
		    	<el-select v-model="group_user" filterable placeholder="请选择">
		    	  <el-option
		    	    v-for="item in user_data"
		    	    :key="item.user_id"
		    	    :label="item.user_name"
		    	    :value="item.user_id">
					<span style="float: left">{{ item.user_name }}</span>
      				<span style="float: right; color: #8492a6; font-size: 13px">{{ "工号"+item.work_id }}</span>
		    	  </el-option>
		    	</el-select>
		    </p>
		    <span slot="footer" class="dialog-footer">
		      <el-button @click="dialogVisible = false">取 消</el-button>
		      <el-button type="primary" @click="Post_group_data()" v-if='add_flag'>确 定</el-button>
		      <el-button type="primary" @click="Edit_group_data()" v-if='edit_flag'>确 定</el-button>
		 	</span>
		</el-dialog>
		<!-- 增加组员 -->
		<el-dialog
		  title="增加组员" :visible.sync="dialogVisible_user" :append-to-body="true" width='40%'>
		    <p>
		  	  <span>组员:</span>
		  	  <el-input v-model="group_user_name" placeholder="请输入组员姓名" class='ipt'></el-input>
		    </p>
		       <span slot="footer" class="dialog-footer">
		         <el-button @click="dialogVisible_user = false">取 消</el-button>
		         <el-button type="primary" @click="dialogVisible_user = false">确 定</el-button>
		    	</span>
		</el-dialog>
	</div>
</template>
<script>
require('../../assets/js/jquery-1.8.3.min.js')
import {get_manager_show, get_user_data,post_manager_group,delete_manager_group,get_group_show} from '@/api/content_api'
	export default {
		data () {
			return {
				proj_id:"",
				user_id:"",
				tree_data:[],
				upload_api:window.g.baseURL + '/manager/import',
				data_json:{
					proj_id:''
				},
				user_data:[],
				dialogVisible:false,
				group_name:"",
				group_user:"",
				dialogVisible_user:false,
				group_user_name:'',
				group_data_row:[],
				group_post_data:{},
				add_flag:false,
				edit_flag:false,
				restaurants:[],
                dialog_title:''
			}
		},
		mounted() {
		    this.proj_id = this.$route.params.pro_id
		    this.user_id = this.$cookies.get('userId')
		    this.data_json.proj_id = this.$route.params.pro_id
			this.get_manager_data()
			this.get_user()
			this.get_group_name_data()
		},
		watch: {
		    $route(to, from) {
		    	this.data_json.proj_id = this.$route.params.pro_id
		    	this.proj_id = this.$route.params.pro_id
		    }
		},
		methods: {
			get_group_name_data(){
				get_group_show().then(res=>{
					if(res.data.result == 'OK'){
						this.restaurants = res.data.content
					}
				})
			},
			get_manager_data(){
				get_manager_show(this.proj_id, this.user_id).then(res=>{
					if(res.data.result == "OK"){
						this.tree_data.push(res.data.content)
					}
				})
			},
			get_user(){
				get_user_data().then(res=>{
					if(res.data.result == 'OK'){
						this.user_data = res.data.content
					}
				})
			},
			node_click(node_index){
				$('.node-first').eq(node_index).children('ul').toggle(500)
			},
			node_click_second(node_index,node_index_cl){
				$('.node-first').eq(node_index).find('.node-second').eq(node_index_cl).children('ul').toggle(500)
			},
			up_success(response, file, fileList){
			    if (response.result == 'OK') {
			    	this.tree_data = []
			    	this.get_manager_data()
			        this.$message({
			            type: 'success',
			            message: '添加成功!',
			            duration: 2000,
			            showClose: false,
			        })
			    }else{
			    	this.up_error("","","",response.error)
			    }
			},
			up_error(err, file, fileList, error){
			    this.$message({
			        type: 'error',
			        message: '添加失败!'+ error,
			        duration:0,
			        showClose: true,
			    })
			},
			add_group(row){
                console.log(row);
                
				this.add_flag = true
				this.edit_flag = false
				this.group_post_data = {}
				this.group_name = ""
				this.group_user = ""
                this.dialog_title = "增加组"
				this.dialogVisible = true
				this.group_data_row = row
				let data_json = {
					proj_id : this.proj_id,
					group_id : 0,
					group_name: this.group_name,
					owner_user : this.group_user,
					parent_group_id : this.group_data_row.group_id,
					commit_user : this.user_id
				}
				this.group_post_data = data_json
			},
			Post_group_data(){
				this.group_post_data.group_name =  this.group_name
				this.group_post_data.owner_user = this.group_user
				let label = ''
				for(let item of this.user_data){
					if(item.user_id == this.group_user){
						label = item.user_name
					}
				}
				if(this.group_name!=""&&this.group_user!=""){
					post_manager_group(this.group_post_data).then(res=>{
						if(res.data.result == "OK"){
							this.dialogVisible = false
							this.tree_data = []
							this.get_manager_data()
							// this.group_data_row.sub.push({
							// 	group_name:this.group_name,
							// 	members:[],
							// 	owner_user:{
							// 		user_name:label
							// 	}
							// }) 
							this.$message({
							    type: 'success',
							    message: '添加成功!',
							    duration: 2000,
							    showClose: false,
							})
						}else{
							this.$message({
							    type: 'error',
							    message: '添加失败!'+ res.data.error,
							    duration:0,
							    showClose: true,
							})
						}
					})
				}else{
					this.$message({
					    message: '组名和组长不可为空!',
					    duration:0,
					    showClose: true,
					})
				}
			},
			Edit_group_data(){
				this.group_post_data.group_name =  this.group_name
				this.group_post_data.owner_user = this.group_user
				let label = ''
				for(let item of this.user_data){
					if(item.user_id == this.group_user){
						label = item.user_name
					}
				}
				if(this.group_name!=""&&this.group_user!=""){
					post_manager_group(this.group_post_data).then(res=>{
						if(res.data.result == "OK"){
							this.dialogVisible = false
							this.group_data_row.group_name = this.group_name
							this.group_data_row.owner_user.user_id = this.group_user
							this.group_data_row.owner_user.user_name = label
							this.$message({
							    type: 'success',
							    message: '修改成功!',
							    duration: 2000,
							    showClose: false,
							})
						}else{
							this.$message({
							    type: 'error',
							    message: '修改失败!'+ res.data.error,
							    duration:0,
							    showClose: true,
							})
						}
					})
				}else{
					this.$message({
					    message: '组名和组长不可为空!',
					    duration:0,
					    showClose: true,
					})
				}
			},
			edit_group(row,parent_row){
                this.dialog_title = '编辑组'
				this.add_flag = false
				this.edit_flag = true
				this.group_post_data = {}
				this.group_data_row = row
				this.group_name = row.group_name
				this.group_user = row.owner_user.user_id
				let data_json = {
					proj_id : this.proj_id,
					group_id : row.group_id,
					group_name: this.group_name,
					owner_user : this.group_user,
					parent_group_id : parent_row.group_id,
					commit_user : this.user_id
				}
				this.group_post_data = data_json
				this.dialogVisible = true
			},
			add_group_user(){
				this.group_user_name = ""
				this.dialogVisible_user = true
			},
			delete_group(row,index,group_id){
				this.$confirm('此操作将永久删除该组, 是否继续?', '提示', {
					confirmButtonText: '确定',
					cancelButtonText: '取消',
					type: 'warning'
				}).then(() => {
					delete_manager_group(this.proj_id, group_id, this.user_id).then(res=>{
						if(res.data.result == "OK"){
							row.sub.splice(index,1)
							this.$message({
								type: 'success',
                                message: '删除成功!',
                                duration: 2000,
                                showClose: false
							})
						}else{
							this.$message({
							    type: 'error',
							    message: '删除失败!'+ res.data.error,
							    duration:0,
							    showClose: true,
							})
						}
					})
					
				}).catch(() => {
					this.$message({
						type: 'info',
                        message: '已取消删除',
                        duration: 2000,
                        showClose: false,
					})          
				})
				
			},
			cancel_fun(){
				this.$router.push({ path: '/proj/pro_detail/' + this.proj_id })
			},
			querySearch(queryString, cb) {
				var restaurants = this.restaurants;
				var results = queryString ? restaurants.filter(this.createFilter(queryString)) : restaurants;
				// 调用 callback 返回建议列表的数据
				cb(results);
			},
			createFilter(queryString) {
				return (restaurant) => {
					console.log(restaurant)
					return (restaurant.group_name.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
				};
			},
			handleSelect(item) {
				this.group_name = item.group_name
			},
		}
	}
</script>
<style scoped>
	ul,li{list-style: none;}
	.clearfix:after {
	    content: ".";
	    display: block;
	    clear: both;
	    visibility: hidden;
	    line-height: 0;
	    height: 0;
	}
	.clearfix {
	 	zoom: 1;
    }
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
		background: #fff 
	}
	.title_h1{
		font-size: 20px;
		width: 95%;
		padding:20px 0 20px 20px;
		color: rgb(94,109,130);
		font-weight: 500;
	}
	.project-tree,.project-tree-title{
		width: 95%;
		padding-left: 20px;
		margin-left: 20px;
	}
	.project-tree-title{
		border:1px solid rgb(235,238,245);
		border-bottom:2px solid rgb(36,41,46);
	}
	.project-tree{
		border:1px solid rgb(235,238,245);
		border-top: 0 none;
		overflow-y: auto
	}
/*树表格头*/
	.tree-table-title{
		height: 45px;
		line-height: 40px;
	}
	.tree-table-title .cl,.tree-node-li .cl{
		float: left;
		text-align: center;
		cursor: pointer;
	}
	.tree-table-title .xl,.tree-node-li .cl{
		float: left;
	}
	.tree-node-li .cl{
		line-height: 40px;
	}
	.tree-node-li{
		/*overflow: hidden;*/
	}
	.group{
		width: 45%;
	}
	.person{
		width: 20%;
	}
	/*.direct-population {
		width: 10%;
	}
	.total-number{
		width: 10%;
	}*/
	.operation{
		width: 35%;
	}
	.tree-node-li .tree-node{
		text-align:left;
	}
	.bg{
		overflow: hidden;
		transition:1s;
		border-radius: 5px;
	}
	.bg:hover{
		background: rgba(255,255,255,.3);
		box-shadow:  5px 10px 20px 6px rgba(0,0,0,.2);
	}
	.detail-box{
		height: 40px;
		line-height: 40px;
		margin:0 0 0 20px;
	}
	.ipt{
		width: 65%;
	}
</style>