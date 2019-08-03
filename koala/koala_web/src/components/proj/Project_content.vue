<template>
	<div class="pro-content-box warpper">
		<div class="add-box">
            <!-- <ContentMenuPlugins></ContentMenuPlugins> -->
          
			<span class="cursor" @click='add_project()'> [ 添加项目 ] </span>
		</div>
		<div class="table-box">
			<el-table :data="tableData" border style="width: 100%">
			    <el-table-column prop="proj_type" label="项目系列">
			    </el-table-column>
			    <el-table-column prop="inside_name" label="项目内部名称">
			    	<template slot-scope="scope">
			    	    <el-button type="text" @click="go_proj_detail(scope.row)">{{scope.row.inside_name}}</el-button>
			    	</template>
			    </el-table-column>
			    <el-table-column prop="outside_name" label="项目客户名称">
			    </el-table-column>
			    <el-table-column prop="describe" label="项目描述">
			    </el-table-column>
			    <el-table-column label="操作" width='150'>
			    	<template slot-scope="scope">
			    	    <el-button type="text" @click="edit_proj(scope.row)">修改</el-button>
			    	</template>
			    </el-table-column>
			</el-table>
		</div>
	</div>
</template>
<script>
import {new_add_input,get_project_list,get_project_info,get_res_info,get_project_type,get_project_inside,add_project,change_project} from '@/api/content_api'
	export default {
        name: 'proj_list',
		data () {
			return {
				tableData: []
			}
		},
		mounted() {
			this.get_data()
		},
		methods: {
			get_data(){
                get_project_list().then(res=>{
                    if(res.data.result=="OK"){
				    	this.tableData = res.data.content
				    }
                })
				
			},
			add_project(){
				this.$router.push('/proj/add_project_c')
			},
			edit_proj(row){
				this.$router.push({path:'/proj/add_project/' + row.proj_id})
			},
			go_proj_detail(row){
				this.$router.push({ path: '/proj/pro_detail/' + row.proj_id })
			}
		}
	}
</script>
<style scoped>
    
	.pro-content-box{
		width: 95%;
	}
	.table-box,.add-box{
		width:100%;
		margin:20px 0 0 20px;
	}
	.add-box{
		/* height: 20px;
		line-height: 20px; */
	}
	.add-box span{
		float: right;
        height: 20px;
        line-height: 20px;
        padding: 0 0 10px
	}
</style>