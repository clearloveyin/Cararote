<template>
	<div class="Project-content">
		<div class="pro-tree">
			
		</div>
		<div class="pro-content">
			<router-view/>
		</div>
	</div>
</template>
<script>
	export default {
		name: 'proj_list',
		data () {
			return {
			}
		},
		mounted() {

		},
		methods: {

		}
	}
</script>
<style scoped>
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
</style>