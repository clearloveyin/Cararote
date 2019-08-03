<template>
	<div class="Project-content warpper">
		<div class="pro-content">
			<div style="padding-top:20px;">
				<el-breadcrumb separator-class="el-icon-arrow-right">
					<el-breadcrumb-item >项目列表</el-breadcrumb-item>
					<el-breadcrumb-item >项目详细</el-breadcrumb-item>
					<el-breadcrumb-item >报价列表</el-breadcrumb-item>
					<el-breadcrumb-item>单次报价构成图</el-breadcrumb-item>
				</el-breadcrumb>
			</div>
			<span style="float:right;font-size:14px;font-weight:500;cursor:pointer;marginTop:20px;" @click='cancel_fun()'>[ 返回 ]</span>
			<ul class='pie-box'>
				<li id='GL'></li>
				<li id='SGL'></li>
				<li id='Feature'></li>
			</ul>
		</div>	
	</div>
</template>
<script>
import {get_quotation_pie} from '@/api/content_api'
	export default {
		data () {
			return {
				quotation_id:'',
				proj_id:''
			}
		},
		mounted() {
		    this.quotation_id = this.$route.params.quotation_id
		    this.proj_id = this.$route.params.pro_id
		    this.get_quotation_data()
		},
		watch: {
		    $route(to, from) {
		   		this.proj_id = this.$route.params.pro_id
		        this.quotation_id = this.$route.params.quotation_id
		    }
		},
		methods: {
			get_quotation_data(){
				let Feature = this.$echarts.init(document.getElementById('Feature'))
				let GL = this.$echarts.init(document.getElementById('GL'))
				let SGL = this.$echarts.init(document.getElementById('SGL'))

				let option_Feature = {
					title : {
					        text: '单次报价构成图-Feature',
					        subtext: '',
					        x:'center'
					    },
					    tooltip : {
					        trigger: 'item',
					        formatter: "{a} <br/>{b} : {c} ({d}%)"
					    },
					    legend: {
					        orient: 'vertical',
					        left: 'left',
					        data: []
					    },
					    series : [
					        {
					            // name: '访问来源',
					            type: 'pie',
					            radius : '55%',
					            center: ['50%', '60%'],
					            data:[
					            
					            ], // 显示数据
					            itemStyle: {
					                emphasis: {
					                    shadowBlur: 10,
					                    shadowOffsetX: 0,
					                    shadowColor: 'rgba(0, 0, 0, 0.5)'
					                }
					            }
					        }
					    ]
				}
				let option_GL = {
					title : {
					        text: '单次报价构成图-GL',
					        subtext: '',
					        x:'center'
					    },
					    tooltip : {
					        trigger: 'item',
					        formatter: "{a} <br/>{b} : {c} ({d}%)"
					    },
					    legend: {
					        orient: 'vertical',
					        left: 'left',
					        data: []
					    },
					    series : [
					        {
					            // name: '访问来源',
					            type: 'pie',
					            radius : '55%',
					            center: ['50%', '60%'],
					            data:[

					            ], // 显示数据
					            itemStyle: {
					                emphasis: {
					                    shadowBlur: 10,
					                    shadowOffsetX: 0,
					                    shadowColor: 'rgba(0, 0, 0, 0.5)'
					                }
					            }
					        }
					    ]
				}
				let option_SGL = {
					title : {
					        text: '单次报价构成图-SGL',
					        subtext: '',
					        x:'center'
					    },
					    tooltip : {
					        trigger: 'item',
					        formatter: "{a} <br/>{b} : {c} ({d}%)"
					    },
					    legend: {
					        orient: 'vertical',
					        left: 'left',
					        data: []
					    },
					    series : [
					        {
					            // name: '访问来源',
					            type: 'pie',
					            radius : '55%',
					            center: ['50%', '60%'],
					            data:[

					            ], // 显示数据
					            itemStyle: {
					                emphasis: {
					                    shadowBlur: 10,
					                    shadowOffsetX: 0,
					                    shadowColor: 'rgba(0, 0, 0, 0.5)'
					                }
					            }
					        }
					    ]
				}
				get_quotation_pie(this.quotation_id).then(res=>{
					if(res.data.result == 'OK'){
						let data_json = JSON.parse(res.data.content)
						option_Feature.series[0].data = data_json.Feature
						option_GL.series[0].data = data_json.GL
						option_SGL.series[0].data = data_json.SGL
						console.log(data_json)
						for(let item of data_json.Feature){
							option_Feature.legend.data.push(item.name)
						}

						for(let item of data_json.GL){
							option_GL.legend.data.push(item.name)
						}

						for(let item of data_json.SGL){
							option_SGL.legend.data.push(item.name)
						}
					}
					// 生成饼图
					Feature.setOption(option_Feature);
					GL.setOption(option_GL);
					SGL.setOption(option_SGL);

					// 监听屏幕缩放  图表自适应
					window.addEventListener("resize",function(){
					    Feature.resize();
					});
					window.addEventListener("resize",function(){
					    GL.resize();
					});
					window.addEventListener("resize",function(){
					    SGL.resize();
					});
				})
			},
			cancel_fun(){
				this.$router.push({ path: '/proj/pro_detail/' + this.proj_id })
			}
		}
	}
</script>
<style scoped>
	ul,li{list-style: none;}
	.Project-content{
		height: 100%;
		overflow-y:auto;
	}
	.pro-tree,.pro-content{
		height: 100%;
	}

	.pro-tree{
		width:300px;
		border-right: solid 1px #e6e6e6;
	}
	.pro-content{
		/*background: #fff;*/
		width: 1280px;
		margin: 0 auto;
	}
	.pie-box{
		width: 100%;
		overflow: hidden;
	}
	.pie-box li {
		margin: 15px;
		height: 500px;
		width: 45%;
		float: left;
		/*background:pink*/
	}
</style>
