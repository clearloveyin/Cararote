<template>
	<div class="Project-content warpper">
		<div class="pro-tree">
			
		</div>
		<div class="pro-content">
			<ul class='pro-nav'>
                <div class="menu">
                    <el-breadcrumb separator-class="el-icon-arrow-right">
                        <el-breadcrumb-item >项目列表</el-breadcrumb-item>
                        <el-breadcrumb-item>项目详细</el-breadcrumb-item>
                        <el-breadcrumb-item>报价版本</el-breadcrumb-item>
                    </el-breadcrumb> 
                </div>
                <li>
					<span @click="cancel_fun()">[ 返回 ]</span>
				</li>
				<li>
					<span @click="go_to_table_fun()"><a :href="url" target="_blank" rel="noopener noreferrer">[ 报价 ]</a> </span>
				</li>
                
			</ul>
			<div class="msg-box">
				<ul class="msg-ul">
					<li>
						<p class="msg-title">报价版本</p>
						<p class="msg-content">
							{{data.quotation_name}}
						</p>
					</li>
					<li>
						<p class="msg-title">描述</p>
						<p class="msg-content">
							{{data.destribe}}
						</p>
					</li>
					<li>
						<p class="msg-title">状态</p>
						<p class="msg-content">
							{{data.status}}
						</p>
					</li>
					<li>
						<p class="msg-title">Base版本</p>
						<p class="msg-content">
							{{data.parent_quotation_name}}
						</p>
					</li>
                    <li>
						<p class="msg-title">创建人</p>
						<p class="msg-content">
							{{data.create_user}}
						</p>
					</li>
                    <li>
						<p class="msg-title">创建时间</p>
						<p class="msg-content">
							{{data.create_time}}
						</p>
					</li>
                    <li>
						<p class="msg-title">修改人</p>
						<p class="msg-content">
							{{data.update_user}}
						</p>
					</li>
                    <li>
						<p class="msg-title">修改时间</p>
						<p class="msg-content">
							{{data.update_time}}
						</p>
					</li>
                    <li>
						<p class="msg-title">Input列表</p>
					</li>
					<li>
						<el-table :data="data.input_resource" border style="width: 100%" >
						    <el-table-column prop="name" label="名称">
						    </el-table-column>
						    <el-table-column prop="ver" label="版本">
						    </el-table-column>
						</el-table>
					</li>
				</ul>

			</div>
		</div>
	</div>
</template>
<script>
import {new_add_input,get_project_list,get_project_info,get_quotation_input,get_quotation_one} from '@/api/content_api'
	export default {
		data () {
			return {
                url:'',
                proj_id:'',
                data:{
                    input_name:'',
                    type:'',
                    version:'',
                    url:''
                }
			}
		},
		mounted() {
		   this.default_mounted()
		},
		methods: {
            default_mounted(){
                let quotation_id = Number(this.$route.query.id)
                this.proj_id = Number(this.$route.query.proj_id)
                this.url = 'cell.html?proj_id='+ this.proj_id +"?quotation_id="+ quotation_id;//传输proj_id给table页
                get_quotation_one(quotation_id).then(res=>{
                    console.log(res,'res')
                    if (res.data.result =='OK') {
                        this.data = res.data.content
                    }
                })

            },
			go_to_table_fun(){
               //not to do
            },
            cancel_fun(){
                this.$router.push({path:'/proj/pro_detail/'+ this.proj_id})
            }
		}
	}
</script>
<style scoped lang="less">
	ul,li{list-style: none;}
	.Project-content{
		height: 100%;
	}
	.pro-tree,.pro-content{
		float: left;
		height: 100%;
	}

	.pro-tree{
		width:300px;
		border-right: solid 1px #e6e6e6;
	}
	.pro-content{
		width: -moz-calc(100% - 302px); 
	    width: -webkit-calc(100% - 302px); 
	    width: calc(100% - 302px); 
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
		margin-top: 20px;
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
	}
	.msg-content{
		font-size: 14px;
		font-weight: 500;
		color: #5e6d82;
    }
    .warpper a{
        color: #5e6d82;
        text-decoration: none;
    }

</style>