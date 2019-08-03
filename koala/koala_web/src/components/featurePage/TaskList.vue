<template>
  <div class="warpper">
    <div class="content-box" v-loading="loading">
      <div class="content-box-header">
        <div class="menu">
            <el-breadcrumb separator-class="el-icon-arrow-right">
                <el-breadcrumb-item >{{title.feature_name}}</el-breadcrumb-item>
                <el-breadcrumb-item >{{title.proj_name}}</el-breadcrumb-item>
                <el-breadcrumb-item >{{title.quotation_name}}</el-breadcrumb-item>
                <el-breadcrumb-item >{{title.version}}</el-breadcrumb-item>

            </el-breadcrumb> 
        </div>
        <span class="content-box-header-btn">
            
          <span class="cursor padding-right"  @click="save">[ 保存task ]</span>
          <span class="cursor"  @click="return_fun">[ 返回 ]</span>
        </span>
      </div>
      <div class="content-box-content">
          <hot-table :root="root" :settings="settings" ref="hotTable"></hot-table>
          <!-- <div class="aaaa"></div> -->
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
  get_task_list,
  get_project_group_list,
  task_list_update,
  get_user_delete_manage,
  get_project_group_list_children
} from "@/api/content_api";
import { HotTable } from "@handsontable-pro/vue";
import "../../../node_modules/handsontable-pro/dist/handsontable.full.css";
import '../../../node_modules/handsontable-pro/languages/zh-CN.js' //中文
export default {
  data() {
    return {
        loading: false,
        tableData: [],
        group_options_data: [],
        root: "test-hot",
        settings: {
            width : "100%",
            height: window.innerHeight - 200,
            manualRowResize: true,//控制行的大小
            stretchH:'all',//根据宽度横向扩展，last:只扩展最后一列，none：默认不扩展,自动展开宽度100%，
            colHeaders :true, //显示表头
            rowHeaders: true, //显示序号
            autoWrapRow :true,//自动换行
            comments: true, //添加注释
            manualColumnResize :true,//手动更改列距
            data:[],//表格总数据
            columns:[],//表格头部prop配置
            colHeaders:[],//自定义列表头or 布尔值
            contextMenu:{},//右键
            language: 'zh-CN', // 右键显示菜单语言类型
            fillHandle: true, //选中拖拽复制 possible values: true, false, "horizontal", "vertical"
            fixedColumnsLeft: 3, //固定左边列数
            fixedRowsTop: 0, //固定上边列数
            customBorders: [], //添加边框
            hiddenColumns: {
                indicators: true
            },
            afterOnCellMouseDown :()=>{
            },
            afterChange: (changes,source) => {
            },
            afterSetCellMeta:()=>{
            },
            colWidths: [100,100,300,100,100,100,100,100],
            // rowHeights: [30],
            observeChanges: true,
            observeDOMVisibility:true,
            autoColumnSize:false
        },
        parent_group_list:[],
        sub_group_list:[],
        proj_id:null,
        quoation_id:null,
        delete_list:[],
        title:{
            feature_name:'Task分配',
            proj_name:"",
            quotation_name:"",
            version:''
        },
        cp_table_data:[]
    };
  },
  components: {
    HotTable
  },
  created() {  
  },
  mounted() {
        this.default_mounted_fun();
  },
  methods: {
    default_mounted_fun() {
        this.quoation_id = this.$route.query.quoteId;
        this.proj_id = this.$route.query.projId
        this.loading = true
        this.promise_all()
    },
    promise_all(){
        const group_list = get_project_group_list_children(this.proj_id).then(res => {
            // console.log(res.data, "group");
            if (res.data.result == "OK") {
                return res
            }else{
                this.$message({type:'error',message:res.data.error})
            }
        });
        const task_list = get_task_list(this.quoation_id).then(res => {
            if (res.data.result == "OK") {
                return res
           
            }else{
                this.$message({type:'error',message:res.data.error})
            }
        });
        Promise.all([group_list,task_list]).then(res=>{//执行并发请求
            // 组
            const group = (group_list_data) =>{
                this.group_options_data = group_list_data;
                this.parent_group_list = this.group_options_data.map(item=>{//父级下拉选择框data
                    return item.group_name
                })
            }
            group(res[0].data.content)
            // table
            const task = (task_list_data)=>{
                let req_data = task_list_data
                let task_list = task_list_data.task_list
                this.title.proj_name = "项目名：" + req_data.proj_name
                this.title.quotation_name = "报价名：" + req_data.quotation_name
                this.title.version = "版本："+ req_data.quotation_ver
                return req_data
            }
            let table_data = task(res[1].data.content)
            this.created_table(table_data);//创建表格数据方法
            this.loading = false
            this.settings.fixedColumnsLeft = res[1].data.content.columns.length-2 //设置表头固定列颜色渲染列数
        })
    },
    created_table(table_all_data) {
        var that = this
        table_all_data.columns.unshift("category_name")
        table_all_data.columns.push("select_parent_group_name","select_sub_group_name")//push一个key用于分配组的
        this.settings.columns = table_all_data.columns.map(item=>{
            if (item == 'select_parent_group_name') {
                return {data:item,type: "autocomplete",  filter: false,trimDropdown: false,source:that.parent_group_list,allowInvalid: false,multiple: true}//设置下拉选择框数据
            }else if (item == 'select_sub_group_name') {
                return {
                    data:item,type: "autocomplete", strict: false, filter: false,trimDropdown: false,source:that.sub_group_list }   
            }
            else {
                if (item == 'category_name' || item == 'sub1' || item == 'sub2') {
                    return {data:item,type:"text",readOnly: true}
                } else {
                    return {data:item,type:"text"}
                }
            };
           
        })
         // 合并表格列相同：
        let columns = this.settings.columns.slice(0,-2)
        for (let columns_name of columns) {
            this.clear_attributes_fun(table_all_data.task_list,columns_name.data)//合并相同行key,并返回处理好的task_list
        };

        this.settings.colHeaders = function(index) {//设置表头渲染 key
                if (this.settings.columns[index].data == 'select_parent_group_name') {
                    return  "分配大组"                    
                }else if (this.settings.columns[index].data == 'select_sub_group_name') {
                    return  "分配小组"                    
                }
                else if(this.settings.columns[index].data == "category_name"){
                    return  "category"                    
                }
                else{
                    return  this.settings.columns[index].data;
                }
            };
        this.settings.contextMenu = {
            items: {
                row_below: {},// name: '下方插入一行'
                col_right: {},
                hsep1: '---------', //提供分隔线
                remove_row: { },
                remove_col: {},//删除列
                hsep2: '---------'
            }
        };
        this.settings.data = table_all_data.task_list.map(item=>{//渲染table数据赋值
            this.edit_data_item_fun(item)//给 item添加新的属性用于分配组使用
            if (item.group_id.length != 0) {
                for (let group_options_data_item of this.group_options_data) {//select框值拆分显示
                    if (item.group_id[0] == group_options_data_item.group_name) {
                        item.select_parent_group_name = group_options_data_item.group_name
                    }
                    if (item.group_id[1]) {
                        for (let sub_item of group_options_data_item.sub) {
                            if (item.group_id[1] == sub_item.group_name) {
                                item.select_sub_group_name = sub_item.group_name
                                break
                            }
                        }
                    }
                }
            }
            return item
        });
        this.cp_table_data = JSON.parse(JSON.stringify(this.settings.data))

        this.settings.afterChange = (changes,source)=>{
            console.log(changes,'changes',source)
            if (changes == null) {
                return false
            }
            changes.forEach(([row, prop, oldValue, newValue]) => {
                if (newValue != "") {//修改过的数据action:changs
                    this.settings.data[row].action = "change" //小组赋值
                }
                if (prop == "select_parent_group_name") {//判断选的是分配大组还是小组
                    console.log('111111111')
                    for (let item of that.group_options_data) {
                        if (newValue == item.group_name) {
                            for (let sub_item of item.sub) {
                                this.sub_group_list.push(sub_item.group_name)
                            }
                            this.clear_sub_select_group_name(this.settings.data[row],newValue)
                            break
                        }
                    }
                } else {//小组
                    if (!this.settings.data[row].group_id[0]) {//如果list-item的group_id为空array，则sub_group_list为空
                        this.sub_group_list.length = 0  
                    }else{//否则，获取大组选中的值，for循环filter出 叶子数组，并重新赋值给sub_group_list。
                        this.filter_sub_group_list_fun(this.group_options_data,row)//filter 叶子方法
                        if (changes[0][1]== "select_parent_group_name" || changes[0][1] == "select_sub_group_name") {//当点击的是分配组时候赋值
                            this.settings.data[row].group_id[1] = newValue //小组赋值
                        }
                    }
                }
            })
        };
        this.settings.afterOnCellMouseDown = (event,coords,TD)=>{//点击表格获取相应位置方法
            // console.log(event,coords,TD,'event,coords,TD')
            let row = coords.row
            let col = coords.col
            if (this.settings.columns[col].data == "select_parent_group_name") {//分配大组
                // nothing to do
               
            } else if(this.settings.columns[col].data == "select_sub_group_name"){//分配小组
                this.sub_group_list.length = 0 //sub_group_list 赋值
                this.filter_sub_group_list_fun(this.group_options_data,row)//过滤叶子组
            }
        }
        this.settings.contextMenu.items.col_right = {// 右方插入行
            name: '添加子task',
            disabled() {
                // this.getSelectedLast()获得一个数组[第几行，第几列，第几行，第几列]（都从0开始）
                // 判断那一列可以添加（根据表头list判断）
                // 当task一个都没有的时候，小分类可以右方插入一个task
                // 有task时，小分类不能添加列，task只能增加子task（右方插入列
                const curColIndex = this.getSelectedLast()[1] //获得当前列的index
                const curColProp = this.colToProp(curColIndex)
                let tableData = that.settings.data
                let colHeaderNameList = that.settings.colHeaders
                let columnsSetting = that.settings.columns
                const taskList = columnsSetting.filter(item => {
                    return item.data.indexOf('task') != -1
                })
                const subList = columnsSetting.filter(item => {
                    return item.data.search('sub') != -1 && item.data.search('_') == -1
                })
                const taskListlen = taskList.length
                const subListlen = subList.length
                const lastSubName = 'sub' + subListlen
                if (taskListlen === 0 && curColProp == lastSubName) {
                    // 确定是小分类列 && 没有task列
                    return false
                } else {
                    // 有task时，只有task最后一级能添加子task
                    if (curColProp.indexOf('task') != -1 && taskListlen == curColProp.substring(4)) {
                        return false
                    }
                }
                return true
            },
            callback() {
                const curColIndex = this.getSelectedLast()[1] //获得当前列的index
                const curColProp = this.colToProp(curColIndex)
                let tableData = that.settings.data
                let columnsSetting = that.settings.columns
                // set new colHeaders
                const taskList = columnsSetting.filter(item => {
                    return item.data.indexOf('task') != -1
                })
                const taskListLen = taskList.length
                const newColName = 'task' + (taskListLen + 1)
                    // set new columns
                const newSingleColSetting = {
                    data: newColName, //数据key值
                    editor: 'text' //是否能编辑（editor没有true这个option）
                }
                columnsSetting.splice(curColIndex + 1, 0, newSingleColSetting)
                    // set new table data
                const lenOfData = tableData.length
                for (let i = 0; i < lenOfData; i++) {
                    tableData[i][newColName] = ''
                }
            }
        },
        this.settings.contextMenu.items.remove_row = {
            disabled() {
                const selectedCell = this.getSelected()
                if (selectedCell.length > 1) {
                    return true
                }
                if (selectedCell[0][0] == selectedCell[0][2] && selectedCell[0][1] == selectedCell[0][3]) {
                    return false
                }
                return true
            },
            callback() {
                const curRowIndex = this.getSelectedLast()[0] //获得当前行的index
                get_user_delete_manage(that.quoation_id,Number(that.$cookies.get("userId")),that.settings.data[curRowIndex].task_id).then(res=>{
                    console.log(res,'aaa')
                    if (res.data.result == 'OK') {
                        that.settings.data[curRowIndex].action = 'delete'
                        that.delete_list.push(that.settings.data[curRowIndex])
                        that.settings.data.splice(curRowIndex,1)
                    }else{
                        that.$message({
                            type:"warning",
                            message:res.data.error,
                            duration:3000
                        })
                    }
                })
            }
        },
        //下方插入行
        this.settings.contextMenu.items.row_below = {
            disabled(){
                return false
            },
            callback() {
                const curRowIndex = this.getSelectedLast()[0]
                const curRowData = JSON.parse(JSON.stringify(table_all_data.task_list[curRowIndex]))
                if (table_all_data.task_list[curRowIndex].task_id == 0) {
                    return false
                }
                console.log(curRowData,'curRowData')
                // const funcTaskList = table_all_data.task_list
                for (let key in curRowData) {//插入一行，把string类型的值清空
                    if(key == 'task_id') {
                        curRowData[key] = 0
                    }
                    if (typeof(curRowData[key]) == 'string') {
                        curRowData[key] = ""
                    }else if(typeof(curRowData[key]) == 'object'){
                        if (key == 'group_id') {
                            curRowData[key].length = 0
                        }
                    }
                    
                }
                curRowData.action = "newAdd"
                that.settings.data.splice(curRowIndex + 1, 0, curRowData)
            }
        };
       
    },
    clear_attributes_fun(data,columns_name) {//合并相同行
        let make_index_arr = [],
            index_value = null;
        for (let i = 0; i < data.length; i++) {
            if (i == 0) {
                make_index_arr.push(1)
                index_value = 0
            }else{
                if (data[i][columns_name] == data[i-1][columns_name]) {
                    make_index_arr[index_value] += 1
                    make_index_arr.push(0)
                } else {
                    make_index_arr.push(1)
                    index_value = i
                }
            }
        }
        for (let j = 0; j < make_index_arr.length; j++) {
            if (make_index_arr[j] == 0) {
                data[j][columns_name] = ""
            }else{
                data[j][columns_name] = data[j][columns_name]
            }
        }
        return data
    },
    save(){
        // let feature_data = this.reset_table_data_fun(copy_table_data) //还原原生数据结构
        // this.set_group_list_value(this.settings.data)
        this.set_group_list_value(this.settings.data)
        // const task_data = JSON.parse(JSON.stringify(this.settings.data))

        // this.add_table_action_key(task_data,this.cp_table_data)
        this.filter_task_value(this.settings.data)//check 提交数据是否有空item,有则去除掉
        let data ={
            proj_id:this.proj_id,
            commit_user:Number(this.$cookies.get('userId')),
            quotation_id:this.quoation_id,
            task_list:this.settings.data,
        }
        console.log(data,'保存')
        // return
        this.loading = true
        task_list_update(data).then(res=>{
            console.log(res,'a')
            if (res.data.result=='OK') {
                this.$message({
                    type:'success',
                    message:'保存成功！',
                    duration: 3000,
                })
                setTimeout(()=>{
                    this.promise_all()
                },1000)
            }else{
                this.$message({
                    type:'error',
                    message:"失败："+res.data.error,
                    duration: 0,
                    showClose:true
                })
            }
            this.loading = false
        })
    },
    reset_table_data_fun(data) {//还原数据
        for (let j = 0; j < this.pos_arr.length; j++) {
            if (this.pos_arr[j] == 0) {
                data[j].sub1 = data[j-1].sub1
            }else{
                data[j].sub1 = data[j].sub1
            }
        }
        return data
    },
    edit_data_item_fun(item){
        item.select_parent_group_name = ""
        item.select_sub_group_name = ""
        item.parent_group_list = []
        item.parent_group_list = this.group_options_data
        item.sub_group_list = []
        return
    },
    filter_sub_group_list_fun(group_options_data,row){//
        let parent_group_name = this.settings.data[row].group_id[0]//获取大组的值
        for (let item of group_options_data) {
            if (item.group_name  == parent_group_name) {//
                for (let sub_item of item.sub) {
                    this.sub_group_list.push(sub_item.group_name)
                }
                break
            }
        }
        return this.sub_group_list
    },
    clear_sub_select_group_name(row_data,newValue){
        row_data.group_id.length = 0
        row_data.group_id[0] = newValue
        setTimeout(()=>{
            row_data.select_sub_group_name = ""
        },10)
        return row_data
    },
    add_table_action_key(task_data,cp_table_data){
        if (task_data.length  == cp_table_data.length) {//思考：当又有新增，又有修改的时候，action如何设置
            for (let i = 0; i < task_data.length; i++) {//当没有新增的时候，check数据是否有修改
                if (JSON.stringify(task_data[i]) != JSON.stringify(cp_table_data[i])) {
                    task_data[i].action = 'change'
                }else{
                    task_data[i].action = 'default'
                }
            }
        } else {
            // for (let i = 0; i < task_data.length; i++) {
            //     task_data[i].action = 'default'
            // }
        }
        
        return task_data
    },
    return_fun(){
        this.$router.push('/proj/projQuoteList')
    },
    set_group_list_value(task_data){//遍历check小组和大组，
        for (let i = 0; i < task_data.length; i++) {
            if (task_data[i].select_sub_group_name == "") {
                task_data[i].group_id.length = 1
            }
            if (task_data[i].select_parent_group_name == "") {
                task_data[i].group_id.length = 0
                task_data[i].select_sub_group_name = ""
            }
        }
        return task_data
    },
    filter_task_value(task_data){
        let key_array = []
        for (let i = 0; i < task_data.length; i++) {
            if (task_data[i].action == "newAdd") {
                for (const key in task_data[i]) {
                    // if (key.search(/task/i) == -1) {//key是否有task字符
                        if (task_data[i].task1 == '') {//task是否为空
                            // key_array.push(key)
                            task_data.splice(i,1)
                        }
                    // }
                }
            }
        }
        return task_data
    }
    
  }
};
</script>

<style lang="less" scoped>
// 通用大模块样式
    .warpper{
        width: 100%;
        height: 100%;
        font-size: 14px;
        background: #fff;
        position: absolute;
        top: 82px;
    }
    .content-box{
        width: 100%;
        // margin: 0 20px 0 20px;
    }
    // 具体小模块样式
    .content-box-header{
        width: 100%;
        height: 25px;
        line-height: 25px;
        margin: 20px 0 20px 0       
    }

    .content-box-header-btn{
        float:right;
        padding-right: 50px;

    }
    .content-box-content{
        width: 100%;
        height: 95%;
    }
 
    .padding-right{
        padding-right: 20px;
    }
    .warpper a{
        color: #5e6d82;
        text-decoration: none;
    }
    .warpper .e-dialog{
        background-color:rgb(255,255,255,.6);
        border: 1px solid #333;
        height: 160px;

    }
    .warpper>.el-dialog__header,.el-dialog__body{
        padding: 0;
        padding-bottom:0px;
    }
    
    .dialog-content{
        font-size: 14px;
        // cursor: pointer;
    }
    .warpper .el-table .cell{
        padding-left: 0;
        padding-right: 0
    }
    .warpper .el-select{
        width: 100%
    }
    .menu{
        padding-left: 20px
    }
    
    
</style>
