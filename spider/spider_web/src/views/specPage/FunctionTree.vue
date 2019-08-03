<template>
    <div class="tree">
        <p>测试树组件</p>
        <ul class="ztree" id="ztree-demo"></ul>
    </div>
</template>
<script>
import $ from 'jquery'
import '@/assets/ztree_v3/js/jquery.ztree.core.min.js'
/*
文档介绍：
zTree API : http://www.treejs.cn/v3/api.php
*/
import treeSetting from '@/js/functionTree/functionTreeSetting'
import data from '@/assets/js/data.json'
export default {
    name: 'zTree',
    data () {
        return {
            setting: treeSetting,
            zNodes: data,
            model_id: 0,
            project_list: [],
            proj_id: 0
        }
    },
    created () {
    },
    mounted () {
        this.create_tree_fun()
    },
    methods: {
        create_tree_fun () {
                    // this.zNodes.length = 0
                    // this.zNodes = res.data.content
                    // this.zNodes.unshift({model_name:"Overview",model_abs_id:1,model_parent_abs_id:0})
                    // 获取节点进行树渲染
                    console.log(this.zNodes)
                    $.fn.zTree.init($('#ztree-demo'), this.setting, this.zNodes).expandAll(false)
                    // let Tree_Menu_Height_fun = $.fn.zTree.getZTreeObj("ztree-demo"),
                    // treeObj = $("#treeDemo"),                  
                    // height_menu = Tree_Menu_Height_fun.getNodes()[0],
                    // set_border_style_list = Tree_Menu_Height_fun.getNodes()
                    // Tree_Menu_Height_fun.selectNode(height_menu)
                    // set_style()
                    // function set_style(){
                    //     for (const item of set_border_style_list) {
                    //         let dom_id = item.tId,
                    //         set_solid = document.getElementById(dom_id)
                    //         set_solid.style.borderBottom="1px solid #ddd"
                    //     }
                    // }
        }
    }
}
</script>
<style scoped>
#ztree-demo border-bottom {
    border-bottom: 1px solid #ddd;
}
@import '../../assets/ztree_v3/css/awesomeStyle/awesome.css';
</style>
