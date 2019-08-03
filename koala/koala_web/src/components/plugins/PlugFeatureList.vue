<template>
    <div class="wrapper">
        <p class="remark-title">备注：一个Feature，只能一个主担当组。（★ :主担当组；☆：关联组）</p>
        <hot-table :settings="settings" v-loading="loading" ref="hot"></hot-table>
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
    // get_project_group_list,
    get_user_delete_manage,
    get_project_group_list_children
} from "@/api/content_api";
import { HotTable } from "@handsontable-pro/vue";
import "../../../node_modules/handsontable-pro/dist/handsontable.full.css";
import '../../../node_modules/handsontable-pro/languages/zh-CN.js' //中文
export default {
    components: {
        HotTable
    },
    props:['readOnly'],
    data() {
        return {
            adaptivePageHeight: window.innerHeight - 150,
            loading: false,
            settings: {
                width: "100%",
                height: window.innerHeight - 200,
                stretchH: 'all',//根据宽度横向扩展，last:只扩展最后一列，none：默认不扩展,自动展开宽度100%，
                colHeaders: true, //显示表头
                rowHeaders: true, //显示序号
                autoWrapRow: true,//自动换行
                comments: true, //添加注释
                manualColumnResize: true,//手动更改列距
                data: [],//表格总数据
                columns: [],//表格头部prop配置
                colHeaders: [],//自定义列表头or 布尔值
                // contextMenu: {},//右键
                language: 'zh-CN', // 右键显示菜单语言类型
                fillHandle: true, //选中拖拽复制 possible values: true, false, "horizontal", "vertical"
                fixedRowsTop: 0, //固定上边列数
                customBorders: [], //添加边框
                hiddenColumns: {
                    indicators: true
                },
                afterOnCellMouseDown: () => {
                },
                afterChange: (changes, source) => {
                },
                colWidths: [],
                manualRowResize: true,//控制行的大小
                // rowHeights: [30],
                fixedColumnsLeft: null,//固定列
                observeChanges: true,
                observeDOMVisibility: true,
                cells: (row, col) => {
                },
                fillHandle: {//选中拖拽复制 possible values: true, false, "horizontal", "vertical"
                    direction: 'vertical',
                    autoInsertRow: false,
                },
                dropdownMenu: true,
                filters: true
            },
            group_options_data: [],
            parent_group_list: [],
            sub_group_list: [],
            select_string_list: ['★', '☆'],
            proj_id: null,
            quotation_id: null,
            delete_list: [],
            // 分割线
            title: {
                feature_name: 'Feature分配',
                proj_name: "",
                quotation_name: "",
                version: ''
            },
            save_btn: "[ 保存 ]",
            show_btn_flag: true,
            SGL: this.$cookies.get("role").indexOf('SGL'),
        };
    },
    mounted() {
        this.default_mounted_fun();
        this.windowResizeEvent()
    },
    methods: {
        windowResizeEvent(callback) {
            var firstFire = null;
            window.onresize =  ()=> {
                if (firstFire === null) {
                    firstFire = setTimeout( ()=>{
                        firstFire = null;
                        // this.settings.height = window.innerHeight - 150
                        this.$refs.hot.hotInstance.updateSettings({
                            // width: document.body.clientWidth,
                            height: window.innerHeight -150
                        })
                        callback();
                    }, 100);
                }
            }
        },
        default_mounted_fun() {
            this.quotation_id = this.$route.query.quotation_id
            this.proj_id = this.$route.query.proj_id
            this.promise_all()
        },
        promise_all() {
            const feature_list = get_feature_list(this.quotation_id, Number(this.$cookies.get('userId'))).then(res => {//创建 feature_list请求
                if (res.data.result == "OK") {
                    return res
                } else {
                    this.$message({ type: 'error', message: res.data.error })
                }
            });
            this.loading = true
            Promise.all([feature_list]).then(res => {//执行feature_list和group_list并发请求
                const feature = (feature_list_data) => {
                    // 配置表格数据
                    let req_data = feature_list_data
                    let feature_list = feature_list_data.feature_list
                    this.title.proj_name = "项目名：" + req_data.proj_name
                    this.title.quotation_name = "报价名：" + req_data.quotation_name
                    this.title.version = "版本：" + req_data.quotation_ver
                    if (this.$route.query.type == "") {
                        this.save_btn = "[ 发起报价 ]"
                    }
                    if (this.$route.query.btn) {
                        this.show_btn_flag = false
                    }
                    req_data.feature_list = feature_list//合并第一例相同key
                    return req_data
                }
                let table_data = feature(res[0].data.content)
                this.created_table(table_data);//创建表格数据方法
                this.loading = false
                let listenData = {
                    title: this.title,
                    show_flag: this.show_btn_flag,
                    btn_name: this.save_btn
                }
                this.$emit('listenExcelTabelEvent', listenData)
                // this.settings.fixedColumnsLeft = 7 //设置表头固定列颜色渲染列数

            })
        },
        created_table(table_all_data) {
            var that = this
            // console.log(table_all_data,'-------')
            table_all_data.columns.unshift("category_name")
            let fixedColumnsLeft = 0 // 统计 feature 列数
            let regSub = RegExp(/[sub]\d/) //匹配 sub 正则
            this.settings.columns = table_all_data.columns.map(item => {
                if (regSub.test(item) || item == 'category_name') {
                    fixedColumnsLeft ++
                    return { data: item, type: "text", readOnly: true }
                }else {
                    let read_only
                    if (this.readOnly) {
                        read_only = true
                    }
                    return {
                        data: item, type: "autocomplete", readOnly: read_only, strict: false, filter: false, trimDropdown: false, source: that.select_string_list
                    }
                }
                
            })
            // console.log('fixedColumnsLeft',fixedColumnsLeft);
            // to do查找固定列问题
            this.$nextTick(()=>{
                this.settings.fixedColumnsLeft = fixedColumnsLeft //设置表头固定列颜色渲染列数
            })
            // this.settings.fixedColumnsLeft = fixedColumnsLeft //设置表头固定列颜色渲染列数
            // console.log(this.settings.columns);
            // console.log(this.settings.columns.slice(0, -2),'=============')
            // 合并表格列相同：            
            let columns = this.settings.columns.slice(0, -2)
            for (let columns_name of columns) {
                this.clear_attributes_fun(table_all_data.feature_list, columns_name.data)//合并相同行key,并返回处理好的task_list
            };
            //设置表头渲染 key
            this.settings.colHeaders = function (index) {
                if (this.settings.columns[index].data == "category_name") {
                    return "category"
                }
                else {
                    return this.settings.columns[index].data;
                }
            };
            this.settings.contextMenu = {
                items: {
                    row_below: {},// name: '下方插入一行'
                    col_right: {},
                    hsep1: '---------', //提供分隔线
                    remove_row: {},
                    remove_col: {},//删除列
                    hsep2: '---------'
                }
            };
            // console.log(table_all_data,'table_all_data')            
            this.settings.data = table_all_data.feature_list.map(item => {//渲染table数据赋值
                this.edit_data_item_fun(item,table_all_data.group_list)//给 item添加新的属性用于分配组使用
                return item
            });
            this.settings.afterChange = (changes, source) => {
                // console.log(changes, 'changes', source)
                if (changes == null) {
                    return false
                }
                changes.forEach(([row, prop, oldValue, newValue]) => {
                    // console.log(row, prop, oldValue, newValue,'row, prop, oldValue, newValue')
                    const feature_item = table_all_data.feature_list[row]
                    newValue != oldValue ? table_all_data.feature_list[row].change = true:delete table_all_data.feature_list[row].change
                    for (const group_item of table_all_data.group_list) {
                        if (group_item !== prop && feature_item[group_item] === newValue && newValue ==='★' ) {
                            this.$message({
                                type: "warning",
                                message: "主担当组只能选一个！"
                            })
                            const asyncRead = async ()=>{
                                table_all_data.feature_list[row][prop] = null
                            }
                            this.$nextTick(()=>{
                                asyncRead()
                            })  
                        }
                    }
                    // console.log(this.settings.data)

                })
            };
            this.settings.afterOnCellMouseDown = (event, coords, TD) => {//点击表格获取相应位置方法
            
            }
            // console.log(table_all_data.my_group, 'my_group',index_arr)
            this.settings.cells = (row, col,prop) => {//设置单元格背景色高亮
                // console.log(this.settings.data,'row,covalue',prop)
                let row_background_color = {}
                const element = this.settings.data[row];
                if (element.relation!==undefined) {
                    if (element.relation == 'major') {
                    row_background_color.className = 'majorClass';
                    return row_background_color
                } else if(element.relation == 'minor'){
                    row_background_color.className = 'minorClass';
                    return row_background_color

                }else if(element.relation == 'nothing'){
                    row_background_color.className = 'nothingClass';
                    return row_background_color
                }
                }
            }
            this.settings.contextMenu.items.col_right = {// 右方插入行
                name: '添加子task',
                disabled() {
                    return true
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
                    return true
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
                    // this.hiddenRow()
                    get_user_delete_manage(that.quotation_id, Number(that.$cookies.get("userId")), that.settings.data[curRowIndex].task_id).then(res => {
                        if (delete_flag == 'OK') {
                            that.settings.data[curRowIndex].action = 'delete'
                            that.delete_list.push(that.settings.data[curRowIndex])
                            that.settings.data.splice(curRowIndex, 1)
                        }
                    })
                }
            },
            this.settings.contextMenu.items.row_below = {
                disabled() {
                    return true
                },
                //下方插入行
                callback() {
                    const curRowIndex = this.getSelectedLast()[0]
                    const curRowData = JSON.parse(JSON.stringify(that.settings.data[curRowIndex]))
                    // console.log(curRowData, 'curRowData')
                    const funcTaskList = that.funcTaskList
                    for (let key in curRowData) {
                        let value = curRowData[key]
                        if (key == 'Default') {
                            for (let itemKey in value) {
                                let sonValue = value[itemKey]
                                for (let sonItemKey in sonValue) {
                                    sonValue[sonItemKey] = null
                                }
                            }
                            continue
                        }
                        if (key == 'task_id') {
                            curRowData[key] = 0
                        }
                        for (let item of funcTaskList) {
                            if (key == item) {
                                curRowData[key] = null
                                break
                            }
                        }
                    }
                    that.settings.data.splice(curRowIndex + 1, 0, curRowData)
                }
            };
            let copyright_logo = document.getElementById('hot-display-license-info')
            copyright_logo.style = "display:none"
        },
        clear_attributes_fun(data, columns_name) {//合并相同行
            let regSub = RegExp(/[sub]\d/) //匹配 sub 正则
            if (regSub.test(columns_name) || columns_name == 'category_name') {
                let make_index_arr = [],
                    index_value = null;
                for (let i = 0; i < data.length; i++) {
                    if (i == 0) {
                        make_index_arr.push(1)
                        index_value = 0
                    } else {
                        if (data[i][columns_name] == data[i - 1][columns_name]) {
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
                    } else {
                        data[j][columns_name] = data[j][columns_name]
                    }
                }
                return data
            }
        },
        reset_table_data_fun(data) {//还原数据
            for (let j = 0; j < this.pos_arr.length; j++) {
                if (this.pos_arr[j] == 0) {
                    data[j].sub1 = data[j - 1].sub1
                } else {
                    data[j].sub1 = data[j].sub1
                }
            }
            return data
        },

        edit_data_item_fun(item,group_list) {
            // console.log(item,group_list)
            const element = item;
            for (const itemKey of group_list) {
                // console.log(itemKey,'key')
                if (element[itemKey] == "major") {
                    element[itemKey] = "★"
                } else if (element[itemKey] == "minor") {
                    element[itemKey] = "☆"
                }
            }
            return item
        },
        filter_sub_group_list_fun(group_options_data, row) {//
            let parent_group_name = this.settings.data[row].group_id[0]//获取大组的值
            for (let item of group_options_data) {
                if (item.group_name == parent_group_name) {//
                    for (let sub_item of item.sub) {
                        this.sub_group_list.push(sub_item.group_name)
                    }
                    break
                }
            }
            return this.sub_group_list
        },
        clear_sub_select_group_name(row_data, newValue) {
            row_data.group_id.length = 0
            row_data.group_id[0] = newValue
            setTimeout(() => {
                row_data.select_sub_group_name = ""
            }, 0)
            return row_data
        },
        add_table_action_key(feature_data) {
            for (let items of feature_data) {

                items.action = 'default'
            }
            return feature_data
        },
        replace_feature_list_major_value(feature_data) {
            let new_feature_data = feature_data.map(item => {
                const key_value = item;
                for (const key in key_value) {
                    if (key_value.hasOwnProperty(key)) {
                        if (key_value[key] === "★") {
                            key_value[key] = 'major'
                            // only_major++
                        } else if (key_value[key] === "☆") {
                            key_value[key] = 'minor'
                        } else if (key_value[key] === "") {
                            key_value[key] = null
                        }
                    }
                }
            })
            return new_feature_data
        },
        copy_feature_data(feature_data){
            let data = {
                proj_id: this.proj_id,
                commit_user: Number(this.$cookies.get('userId')),
                quotation_id: this.quotation_id,
                feature_list: feature_data,
            }
            return data
        },
        check_feature_list_major(feature_data){
            if (feature_data == undefined) {
                feature_data = this.settings.data
            }
            const check_major = (element,index,array)=>{
                return Object.values(element).includes('★')
            }
            let flag = feature_data.every(check_major)//对所有元素执行检测是否有主担当（★），如果有一个不满足，则整个表达式返回false，且剩余元素不再进行检测。
            return flag
        },
        save() {
            let feature_data = JSON.parse(JSON.stringify(this.settings.data)), 
            data,
            router_flag_message = false;//是否执行保存开关
            this.replace_feature_list_major_value(feature_data)
            data = this.copy_feature_data(feature_data)
            console.log(data,'data');
            
            this.loading = true
            this.post_data(data,router_flag_message)
        },
        next_option() {
            let feature_data = JSON.parse(JSON.stringify(this.settings.data)),
            check_major_flag = this.check_feature_list_major(feature_data);//若check有一个没填主担当，则返回false.,
            if (check_major_flag == false) {
                this.$message({
                    type: 'warning',
                    message: '每个feature必须选一个主担当。',
                    duration: 3000,
                })
                return false
            }
            this.replace_feature_list_major_value(feature_data)
            let data = {
                proj_id: this.proj_id,
                commit_user: Number(this.$cookies.get('userId')),
                quotation_id: this.quotation_id,
                feature_list: feature_data,
            },
            router_flag = true;
            this.loading = true
            this.post_data(data,router_flag)//保存
          
        },
        return_fun() {
            this.$router.push('/proj/projQuoteList')
        },
        post_data(data,router_flag){
            // console.log(data,'data');
            feature_list_assign(data, this.quotation_id).then(res => {
                if (res.data.result == 'OK') {
                    this.$message({
                        type: 'success',
                        message: '保存成功！',
                        duration: 3000,
                    })
                    if (router_flag) {
                        this.$router.push({ path: "/Options/OptionsView", query: { quotation_id: this.quotation_id, proj_id: this.proj_id } })
                    }else{
                        setTimeout(() => {
                            this.promise_all()
                        }, 100);
                    }
                    this.loading = false
                } else {
                    this.$message({
                        type: 'error',
                        message: "失败：" + res.data.error,
                        duration: 0,
                        showClose: true
                    })
                    this.loading = false
                }
            })
            
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
.remark-title {
    color: red;
}
</style>
<style>
.wtHolder {
    height: 650px;
}
</style>

