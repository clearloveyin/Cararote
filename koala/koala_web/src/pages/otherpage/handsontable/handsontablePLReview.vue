<template>
    <div class="pl-review-container" v-loading.fullscreen.lock="fullscreeLoading" element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading" element-loading-background="rgba(0, 0, 0, 0.8)">
        <div class="title" id="title">
            <el-breadcrumb separator-class="el-icon-arrow-right" >
                <el-breadcrumb-item>{{title.projName}}</el-breadcrumb-item>
                <el-breadcrumb-item>{{title.quotationName}}</el-breadcrumb-item>
                <el-breadcrumb-item>{{title.version}}</el-breadcrumb-item>
            </el-breadcrumb>
            <div class="title-bar">
                <div style="display: inline-block;margin-right: 10px;">
                    工数单位:
                    <el-select v-model="value" placeholder="请选择" size="small" style="width: 100px;" @change="switchDaysUnit">
                        <el-option
                        v-for="item in options"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                        </el-option>
                    </el-select>
                </div>
                <el-button type="primi" size="mini" @click="export_excel">导出表格</el-button>
            </div>
        </div>           
        <div id="example-container" class="hottable-wrapper">
            <HotTable :root="root" ref="textHot" :settings="hotSettings" v-if="showTable"></HotTable>
        </div>

        <!-- 覆盖层 -->
        <div class="shadow" @mousedown.stop>
            <i class="el-icon-d-arrow-right" @click='hideHistory()'></i>
            <div style="position: absolute; top: 0px; bottom: 0; left: 44px; right: 0px;overflow: hidden;" v-loading="taskRecordLoading">
                <HotTable :root="root" ref="detailTable" :settings="detailSettings" v-if="showDetailTable"></HotTable>
            </div>
        </div>
    </div>
</template>
<script>
import '../../../../node_modules/handsontable-pro/dist/handsontable.full.css'
import TaskRecord from '../views/taskRecord' //履历组件
import Handsontable from 'handsontable-pro'
import { HotTable } from '@handsontable-pro/vue'
import 'handsontable-pro/languages/zh-CN' //中文包
require('../../../assets/js/jquery-1.8.3.min.js')
import { reqSummaryAccount, reqTaskHistory, reqDetailQuote, reqDetail,export_excel } from '../../../api/hansontable.js' //请求接口方法
import basicConfig from './basicConfig' //表格基础配置
import { getTaskIndex, getPrimedColPropList, getDynamicColPropList, clearRepeatData, getDetailDynamicColPropList, checkNumber } from './someMethods' //整理数据方法
import { lookDetail } from './contextMenu.js'
export default {
    name: 'SummaryAccount',
    components: {
        HotTable,
        TaskRecord
    },
    data: function() {
        return {
            fullscreeLoading: false,
            taskRecordLoading: false,
            quotationId: '',
            showTable: false,
            showDetailTable: false,
            root: 'preview-hot',
            rootDetail: 'detail-table',
            hotSettings: {},
            detailSettings: {
                data: [], //表格总数据
                startRows: 100, //行列范围
                startCols: 100,
                minRows: 0, //最小行列
                minCols: 0,
                maxRows: 10000, //最大行列
                maxCols: 10000,
                rowHeaders: true, //行表头
                colHeaders: [], //自定义列表头or 布尔值
                minSpareCols: 0, //列留白
                minSpareRows: 0, //行留白
                currentRowClassName: 'currentRow', //为选中行添加类名，可以更改样式
                currentColClassName: 'currentCol', //为选中列添加类名
                autoWrapRow: true, //自动换行
                // rowHeights: 100,
                autoRowSize: {
                    syncLimit: 500,
                    allowSampleDuplicates: true
                },
                autoColumnSize: {
                    syncLimit: 500,
                    allowSampleDuplicates: true
                },
                // autoColumnSize: true,
                language: 'zh-CN', // 右键显示菜单语言类型
                collapsibleColumns: true,
                className: 'htLeft',
                contextMenu: false, //右键效果
                fillHandle: {//选中拖拽复制 possible values: true, false, "horizontal", "vertical"
                    direction: 'vertical',
                    autoInsertRow: false,
                },
                fixedColumnsLeft: 2, //固定左边列数
                // fixedRowsTop: 0, //固定上边列数
                columns: [], //表格头部prop配置
                nestedHeaders: [],
                manualColumnFreeze: true, //手动固定列
                manualColumnMove: false, //手动移动列
                manualRowMove: false, //手动移动行
                manualColumnResize: true, //手工更改列距
                manualRowResize: true, //手动更改行距
                comments: true, //添加注释
                // cell: [{ row: 1, col: 1, comment: { value: 'this is test' } }],
                customBorders: [], //添加边框
                columnSorting: false, //排序
                stretchH: 'all', //根据宽度横向扩展，last:只扩展最后一列，none：默认不扩展
                hiddenColumns: {
                    indicators: true
                },
                trimRows: []
            },
            funcTaskList: [],
            costList: [],
            groupList: [],
            optionList: [],
            detailGroupList: [],
            detailOptionList: [],
            taskRecordList: [],
            title: {
                projName: '',
                quotationName: '',
                version: ''
            },
            firstDetail: true,
            ip_address: window.g.baseURL,
            options: [
                {
                    value: 'day',
                    label: '人/日'
                },
                {
                    value: 'month',
                    label: '人/月'
                }
            ],
            value: 'month',
            detailFlag: false
        }
    },
    created() {
        let that = this
        this.userId = this.$cookies.get('userId')
        this.quotationId = location.href.split('?')[1].split('=')[1]
        this.fullscreeLoading = true
        // this.detailSettings = JSON.parse(JSON.stringify(basicConfig))
        // basicConfig.fixedRowsBottom = 1
        this.hotSettings = JSON.parse(JSON.stringify(basicConfig)) //excel基本配置
        this.hotSettings.beforeKeyDown = function(e) {
            // 在最后一行，阻止 ↓ 按键事件
            const rows = this.countRows();
            const selection = this.getSelectedLast()
            const currentRow = selection[0]
            
            if(currentRow + 1 === rows  && e.keyCode === 40) {
                e.stopImmediatePropagation()
            }

            if(currentRow === 0  && e.keyCode === 38) {
                e.stopImmediatePropagation()
            }
        }
        this.hotSettings.fillHandle = false
        this.hotSettings.contextMenu.items.lookDetail = lookDetail
        this.hotSettings.contextMenu.items.lookDetail.callback = function() {
            const selectedCell = this.getSelected()
            const row = selectedCell[0][0]
            const col = selectedCell[0][1]
            const rowData = this.getSourceData()[row]
            const funcId = rowData.func_id
            that.showHistory(funcId)
        }
        this.getSummaryAccount()
    },
    mounted() {},
    methods: {
        getDetail(funcId) {
            reqDetail(funcId).then(res => {
                if(res.data.content.data_list.length === 0) {
                    this.showDetailTable = false
                    this.firstDetail = true
                } else {
                    this.getDetailDynamicBasicConfig(res)
                } 
                this.taskRecordLoading = false
            })
        },
        getDetailDynamicBasicConfig(res) {
            let settingsColumns = []
            let settingsData = []
            let nestedHeaders = [[], [], []]
            let settingFiexedLeftNum = 0

            let data = res.data.content
            /**
             * 表格列配置
             */
            let colPropList = getPrimedColPropList(data) //处理数据，返回预处理的列表头数据，用来下一步计算
            let dynamicColPropList = getDetailDynamicColPropList(colPropList) ////获得表头列columns（不是固定列的部分）
            settingFiexedLeftNum = colPropList[0].length//固定列数
            colPropList[0].map(item => {
                //固定的前几列: task、sub
                let singleColSetting = {
                    data: item,
                    readOnly: true
                }
                settingsColumns.push(singleColSetting)
            })
            
            dynamicColPropList.map((item, index) => {
                // options
                let optionProp = item.split('.')[2]
                let singleColSetting = {
                    data: item,
                    readOnly: true
                }
                settingsColumns.push(singleColSetting)
            })
            
            let funcTaskList = res.data.content.func_task_list
            let funcTaskLen = res.data.content.func_task_list.length
            let quoteList = res.data.content.data_list
            let quoteLen = res.data.content.data_list.length - 1
            this.detailGroupList = res.data.content.group_list
            this.detailOptionList = res.data.content.option_list
            if (quoteList.length != 0) {
                settingsData = clearRepeatData(funcTaskLen, quoteLen, funcTaskList, quoteList) //清理固定列重复数据
                for (let item of settingsData) {
                    item.superGroup = typeof item.group_name_list[0] == 'undefined' ? '' : item.group_name_list[0]
                    item.group = typeof item.group_name_list[1] == 'undefined' ? '' : item.group_name_list[1]
                }
            }


            /**
             * ================================================================================================
             * 合并表头list
             */
            let groupSum = 0
            for(let item of colPropList[2]) {
                groupSum += item.length
            }
            const numOfOptions = groupSum
            // 获得表头第三列数据
            nestedHeaders[2] = nestedHeaders[2].concat(colPropList[0])
            const tempArr = JSON.parse(JSON.stringify(colPropList[3]))
            tempArr[0] = 'cost'
            for (let i = 0; i < numOfOptions; i++) {
                nestedHeaders[2] = nestedHeaders[2].concat(tempArr)
            }
           
            // 获得表头第二列数据
            const numOfFixed = colPropList[0].length
            for (let i = 0; i < numOfFixed; i++) {
                nestedHeaders[1].push('')
            }
            // for (let i = 0; i < colPropList[1].length; i++) {
            for (let j = 0; j < colPropList[2].length; j++) {
                for(let item of colPropList[2][j]) {
                    nestedHeaders[1].push({
                        label: item,
                        colspan: 4
                    })
                }
            }
           
            // }
            // 获得表头第一列数据
            for (let i = 0; i < numOfFixed; i++) {
                nestedHeaders[0].push('')
            }
            for (let i = 0; i < colPropList[1].length; i++) {
                nestedHeaders[0].push({
                    label: colPropList[1][i],
                    colspan: colPropList[2][i].length * colPropList[3].length
                })
            }

            // 请求数据默认为 '人日'，页面显示默认为 '人月'，转换一下
            
            const DAYKEY = 'days'
            if(this.value == 'month') {
                const multiple = 0.05
                this.transDetailsDay(settingsData, multiple, this.detailOptionList, this.detailGroupList, DAYKEY)
            }
            
            if (this.firstDetail === true) {
                //第一次进入，获取不到this.$refs.textHot.hotInstance
                this.detailSettings.fixedColumnsLeft = settingFiexedLeftNum //固定列数
                this.detailSettings.columns = settingsColumns
                this.detailSettings.data = settingsData
                this.detailSettings.nestedHeaders = nestedHeaders
                this.firstDetail = false
                let copyright_logo = document.getElementById('hot-display-license-info')
                copyright_logo.style = 'display:none'
            } else {
                this.detailSettings.fixedColumnsLeft = settingFiexedLeftNum //固定列数
                this.detailSettings.columns = settingsColumns
                this.detailSettings.data = settingsData
                this.detailSettings.nestedHeaders = nestedHeaders
                let copyright_logo = document.getElementById('hot-display-license-info')
                copyright_logo.style = 'display:none'
            }
            this.showDetailTable = true
        },
        getDynamicBasicConfig(res) {
            let settingsColumns = []
            let settingsData = []
            let nestedHeaders = [[], ['category']]
            let settingFiexedLeftNum = 0

            let data = res.data.content
            this.funcTaskList = data.func_task_list //sub、task
            this.groupList = data.group_list //组名
            this.costList = data.cost_list //组下面的选项（days，precondition，comment，status）
            this.optionList = data.option_list //option

            /**
             * 表格列配置
             */
            let colPropList = getPrimedColPropList(data).filter(item => {
                return item.length != 0
            }) //处理数据，返回预处理的列表头数据，用来下一步计算
            let dynamicColPropList = getDynamicColPropList(colPropList) ////获得表头列columns（不是固定列的部分）
            settingFiexedLeftNum = colPropList[0].length + 1 //固定列数
            settingsColumns.push({
                //手动添加category列，这里可以改进合并进下面代码
                data: 'category_name',
                readOnly: true,
                width: 100
            })
            colPropList[0].map(item => {
                //固定的前几列: task、sub
                let singleColSetting = {
                    data: item,
                    readOnly: true,
                    width: 100
                }
                settingsColumns.push(singleColSetting)
            })
            dynamicColPropList.map((item, index) => {
                // options
                let optionProp = item.split('.')[2]
                let singleColSetting = {
                    data: item,
                    readOnly: true
                }
                settingsColumns.push(singleColSetting)
            })
            let that = this
            function detailCellStyle(instance, td, row, col, prop, value, cellProperties) {
                if(row + 1 === instance.countRows()) {
                    td.style.background = 'rgb(253, 233, 217)'
                    return td
                }
                const escaped = Handsontable.helper.stringify(value)
                let btn = null
                let btnValue = document.createTextNode('详细')
                btn = document.createElement('BUTTON')
                btn.appendChild(btnValue)

                Handsontable.dom.addEvent(btn, 'mousedown', function(event) {
                    const rowData = instance.getSourceData()[row]
                    const funcId = rowData.func_id
                    
                    that.showHistory(funcId)
                    event.preventDefault()
                })

                Handsontable.dom.empty(td)
                td.appendChild(btn)
                return td
            }
            settingsColumns.push({
                data: 'detainBtn',
                readOnly: true,
                renderer: detailCellStyle
            }) //后期额外增加一列（用来存放详细按钮）
            let funcTaskList = res.data.content.func_task_list
            let funcTaskLen = res.data.content.func_task_list.length
            let quoteList = res.data.content.data_list
            let quoteLen = res.data.content.data_list.length - 1
            if (quoteList.length != 0) {
                settingsData = clearRepeatData(funcTaskLen, quoteLen, funcTaskList, quoteList) //合并重复数据
            }

            // 获得表头第二列数据
            const numOfFixed = colPropList[0].length + 1
            for (let item of colPropList[0]) {
                nestedHeaders[1].push(item)
            }
            for (let i = 0; i < colPropList[1].length; i++) {
                for (let j = 0; j < colPropList[2].length; j++) {
                    if(colPropList[2][j] == 'days') {
                        nestedHeaders[1].push('cost')
                    } else {
                        nestedHeaders[1].push(colPropList[2][j])
                    }
                    
                }
            }
            nestedHeaders[1].push('') //后期额外增加一列（用来存放详细按钮）
            //获得表头第一列数据
            nestedHeaders[0].push('Item and Scope')
            for (let i = 1; i < numOfFixed; i++) {
                nestedHeaders[0].push('')
            }
            for (let i = 0; i < colPropList[1].length; i++) {
                nestedHeaders[0].push({
                    label: colPropList[1][i],
                    colspan: 4
                })
            }
            nestedHeaders[0].push('详细') //后期额外增加一列（用来存放详细按钮）
            this.hotSettings.fixedColumnsLeft = settingFiexedLeftNum //固定列数
            this.hotSettings.columns = settingsColumns
            // 请求数据默认为 '人日'，页面显示默认为 '人月'，转换一下
            const multiple = 0.05
            const dayKey = 'days'
            this.transDay(settingsData, multiple, data.option_list , dayKey)
            this.hotSettings.data = settingsData
            this.hotSettings.nestedHeaders = nestedHeaders
        },
        getSummaryAccount() {
            reqSummaryAccount(this.quotationId, this.userId)
                .then(res => {
                    if (res.data.result == 'OK') {
                        const data = res.data.content
                        this.title.projName = '项目名：' + data.proj_name
                        this.title.quotationName = '报价名：' + data.quotation_name
                        this.title.version = '版本：' + data.quotation_ver
                        this.getDynamicBasicConfig(res)
                        this.showTable = true
                        this.fullscreeLoading = false
                    } else {
                        reject()
                    }
                }).then(() => {
                    let hot = this.$refs.textHot.hotInstance
                    
                    let rows=hot.countRows();  // get the count of the rows in the table
                    let cols=hot.countCols();  // get the count of the columns in the table.
                    for(let col=0; col<cols; col++){  // go through each column of the row
                        if(col < 2) {
                            hot.setCellMeta(rows - 1, col, 'className', 'redCell');
                        } else {
                            hot.setCellMeta(rows - 1, col, 'className', 'blueCell');
                        }
                    }
                    hot.render();
                })
                .catch(() => {
                    this.fullscreeLoading = false
                })
        },
        showHistory(funcId) {
            let that = this
            this.detailFlag = true
            this.taskRecordLoading = true
            $('.shadow').animate({ right: '1px'}, 1000, function() {
                that.getDetail(funcId)
                that.taskRecordLoading = false
            })
        },
        hideHistory() {
            this.detailFlag = false
            $('.shadow').animate({ right: '-55%' }, 1000)
        },
        export_excel(){
            export_excel(this.userId,this.quotationId, this.value).then(res=>{
                if (res.data.result == 'OK') {
                    window.open(this.ip_address  + '/download/' + res.data.content)
                }else{
                    alert('请求失败')
                }
            }).catch(err=>{

            })
            
        },
        switchDaysUnit(value) {
            const groupList = this.groupList
            const optionList = this.optionList
            const data = this.$refs.textHot.hotInstance.getSourceData()
            
            const dayKey = 'days'
            const detailGroupList = this.detailGroupList
            const detailOptionList = this.detailOptionList
            let multiple = 0
            if(value === 'day') {
                multiple = 20
            } else {
                multiple = 0.05
            }
            if(this.detailFlag) {
                let detailsData = this.detailSettings.data
                this.transDetailsDay(detailsData, multiple, detailOptionList, detailGroupList, dayKey)
            }
            this.transDay(data, multiple, optionList , dayKey)
        },
        transDay(data, multiple, optionList, dayKey) {
            for(let dataItem of data) {
                for(let optionKey of optionList) {
                    if(checkNumber(dataItem[optionKey][dayKey])) {
                        if(dataItem[optionKey][dayKey] == '' || dataItem[optionKey][dayKey] === null) { //为什么还要检测 值 === '',因为单元格删除数字时，值会变为''
                            dataItem[optionKey][dayKey] = null
                        } else {
                            dataItem[optionKey][dayKey] = dataItem[optionKey][dayKey] * multiple
                            dataItem[optionKey][dayKey] = Math.round(dataItem[optionKey][dayKey] * 100)/100
                        }
                    } else {
                        dataItem[optionKey][dayKey] = null
                    }
                }
            }
        },
        transDetailsDay(data, multiple, optionList, groupList, dayKey) {
            for(let dataItem of data) {
                for(let i = 0; i < optionList.length;i++ ) {
                    const optionKey = optionList[i]
                    for(let groupKey of groupList[i]) {
                        if(checkNumber(dataItem[optionKey][groupKey][dayKey])) {
                            if(dataItem[optionKey][groupKey][dayKey] == '' || dataItem[optionKey][groupKey][dayKey] === null) { //为什么还要检测 值 === '',因为单元格删除数字时，值会变为''
                                dataItem[optionKey][groupKey][dayKey] = null
                            } else {
                                dataItem[optionKey][groupKey][dayKey] = dataItem[optionKey][groupKey][dayKey] * multiple
                                dataItem[optionKey][groupKey][dayKey] = Math.round(dataItem[optionKey][groupKey][dayKey] * 100)/100
                            }
                        } else {
                            dataItem[optionKey][groupKey][dayKey] = null
                        }
                    }
                }
            }
        },
    }
}
</script>

<style scoped>
@import './handsontable.css';
.pl-review-container {
    width: 100%;
    height: 100%;
}
.title{
    /* display: flex; */
    height: 50px;
    line-height: 50px;
   
}
.title-bar{
    position: absolute;
    top: 0px;
    right: 30px;
}
.el-breadcrumb{
    padding:0 10px 0 10px;
    font-weight: normal;
    height: 50px;
    line-height: 50px

}
.btn-switch {
    float: right;
    padding: 10px 15px 0 0;
}
.hottable-wrapper {
    position: absolute;
    left: 0;
    right: 0;
    top: 50px;
    bottom: 0;
    overflow: hidden;
}
#test-hot {
    width: 100%;
    height: 800px;
    overflow: hidden;
}
.shadow {
    width: 55%;
    height: calc(100% - 48px);
    position: fixed;
    background: rgba(255, 254, 255);
    top: 48px;
    right: -55%;
    z-index: 666;
    text-align: left;
    border-radius: 5px;
    filter: drop-shadow(0 3px 5px black);
}
.el-icon-d-arrow-right {
    font-size: 24px;
    padding: 10px;
}
</style>