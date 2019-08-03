<template>
    <div class="container" v-loading.fullscreen.lock="fullscreeLoading" element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading" element-loading-background="rgba(0, 0, 0, 0.8)">
        <div class="title">
            <el-breadcrumb separator-class="el-icon-arrow-right" style="padding-top: 10px;font-weight: normal;">
                <el-breadcrumb-item>{{title.projName}}</el-breadcrumb-item>
                <el-breadcrumb-item>{{title.quotationName}}</el-breadcrumb-item>
                <el-breadcrumb-item>{{title.version}}</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="btn-switch">
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
            <div style="display: inline-block;margin-right: 10px;" @click.capture.stop="switchType">
                <el-switch v-model="quoteType" active-text="我的" inactive-text="全部">
                </el-switch>
            </div>
            <el-button type="success" size="mini" @click="save">保存</el-button>
        </div>

        <div id="example-container" class="handsontable-wrapper">
            <HotTable :root="root" ref="textHot" :settings="hotSettings" v-if="showTable"></HotTable>
        </div>

        <!-- 履历 -->
        <div class="shadow" @mousedown.stop>
            <i class="el-icon-d-arrow-right" @click='hide_shadow()'></i>
            <div style="position: absolute; top: 0px; bottom: 0; left: 44px; right: 0px;" v-loading="taskRecordLoading">
                <task-record :taskRecordList="taskRecordList" :taskRecordTitle="taskRecordTitle"></task-record>
            </div>

        </div>
        <!-- 指摘弹窗 -->
        <point-dialog @setDaysStatus="setDaysCellStyle" :pointVisible.sync="pointVisible" :selectedCell="selectedCell" v-show="pointVisible" :baseId="baseId" :quotationId="quotationId"></point-dialog>
        <!-- 工数统计弹窗 -->
        <man-day-dialog v-show="manDayVisible" :selectedArea="selectedArea" :dialogWidth="200" :dialogHeight="100">
            <p>
                <span>选中区域的总工数:</span>
                <span>{{manDaySum}}</span>
            </p>
            <p>
                <span>选中区域的已填写工数:</span>
                <span>{{manDayNum}}</span>
            </p>
        </man-day-dialog>
    </div>
</template>
<script>
import '../../../../node_modules/handsontable-pro/dist/handsontable.full.css'
import moment from 'moment' //handsontable plugin
import numbro from 'numbro'
import pikaday from 'pikaday' //date plugun
import Zeroclipboard from 'zeroclipboard'
import PointDialog from './pointDialog' //指摘组件
import ManDayDialog from './manDayDialog'
import TaskRecord from '../views/taskRecord' //履历组件
import { Handsontable, CustomEditor, cells, customCommentRenderer, costRenderer } from './cellStyle' //工数表格样式
import { HotTable } from '@handsontable-pro/vue'
import { Message, MessageBox } from 'element-ui' // element UI
import 'handsontable-pro/languages/zh-CN' //中文包
require('../../../assets/js/jquery-1.8.3.min.js')

import {
    reqAllQuotations,
    reqMyQuotations,
    setQuotationList,
    reqTaskHistory,
    checkDeleteTask,
    reqDetailQuote,
    reqGroupList
} from '../../../api/hansontable.js' //请求接口方法
import basicConfig from './basicConfig' //表格基础配置

import { filterRepeatData } from './filterRepeatData' //剔除重复表格数据
import { taskRecord, issue, removeRow, splitTask } from './contextMenu' //右键功能方法
import { getPrimedColPropList, getDynamicColPropList, clearRepeatData, getUrlHrefParams, checkNumber} from './someMethods' //整理数据方法
export default {
    name: 'QuoteTable',
    components: {
        HotTable,
        PointDialog,
        TaskRecord,
        ManDayDialog
    },
    data: function() {
        return {
            showMessageFlag: false,
            fullscreeLoading: false,
            taskRecordLoading: false,
            projId: '',
            quotationId: '',
            showTable: false,
            selectOptionsData: {},
            headersData: [],
            root: 'test-hot',
            hotSettings: {
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
                autoRowSize: {
                    syncLimit: 500,
                    allowSampleDuplicates: true
                },
                autoColumnSize: {
                    syncLimit: 500,
                    allowSampleDuplicates: true
                },
                language: 'zh-CN', // 右键显示菜单语言类型
                collapsibleColumns: true,
                className: 'htLeft',
                contextMenu: {
                    //自定义右键菜单，可汉化，默认布尔值
                    items: {
                        // 'row_below': {
                        //     name: '拆分Task'
                        // }
                    }
                }, //右键效果
                fillHandle: {//选中拖拽复制 possible values: true, false, "horizontal", "vertical"
                    direction: 'vertical',
                    autoInsertRow: false,
                },
                fixedColumnsLeft: 2, //固定左边列数
                columns: [], //表格头部prop配置
                nestedHeaders: [],
                manualColumnFreeze: true, //手动固定列
                manualColumnMove: false, //手动移动列
                manualRowMove: false, //手动移动行
                manualColumnResize: true, //手工更改列距
                manualRowResize: true, //手动更改行距
                comments: true, //添加注释
                customBorders: [], //添加边框
                columnSorting: false, //排序
                stretchH: 'all', //根据宽度横向扩展，last:只扩展最后一列，none：默认不扩展
                hiddenColumns: {
                    indicators: true
                },
                trimRows: []
            },
            manDaySum: 0,
            manDayNum: 0,
            funcTaskList: [],
            costList: [],
            groupList: [],
            optionList: [],

            pointVisible: false,
            manDayVisible: false,
            baseId: 0,
            row: null,
            col: null,
            activePointArrow: '',
            selectedCell: {
                width: null,
                height: null,
                top: null,
                left: null
            },
            selectedArea: {
                width: null,
                height: null,
                top: null,
                left: null
            },
            colProp: [],

            //task履历
            taskRecordList: [],
            taskRecordTitle: '',
            pointList: [],

            deleteList: [],
            title: {
                projName: '',
                quotationName: '',
                version: ''
            },

            quoteType: true, //我的:true 全部:false,
            switchNum: 0,
            tempColumns: [],

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
            value: 'month'
        }
    },
    watch: {},
    created() {
        
        let that = this
        this.userId = this.$cookies.get('userId')
        const params = getUrlHrefParams()
        this.quotationId = Number(params.quotationId)
        this.projId = params.projId
        this.fullscreeLoading = true

        this.hotSettings.afterDeselect = function() {
            that.hiddenDialog()
        }

        this.hotSettings.beforeOnCellMouseDown = function(event, coords, td, controller) {
            const row = coords.row
            const col = coords.col
            const colProp = this.colToProp(col)
            const superGroupValue = this.getDataAtCell(row, col - 1)
            const superGroupList = that.superGroupList
            if (colProp == 'group') {
                for (let item of superGroupList) {
                    if (item.group_name == superGroupValue) {
                        const groupSource = item.sub.map(groupItem => {
                            return groupItem.group_name
                        })
                        this.setCellMeta(row, col, 'source', groupSource)
                        break
                    }
                }
            }
        }
        this.hotSettings.beforeChange = function(arr, source) {
            for (let item of arr) {
                const row = item[0]
                const colProp = item[1]
                const oldValue = item[2]
                const newValue = item[3]
                let quoteData = this.getSourceData()
                const groupCol = this.propToCol(colProp)
                let subGroup = []
                const superGroupList = that.superGroupList
                const superGroup = quoteData[row].superGroup
                if (newValue != oldValue && colProp === 'group' && newValue != '') {
                    //如果旧值和新值不一样，更新该行数据action
                    for (let item of superGroupList) {
                        if (item.group_name == superGroup) {
                            subGroup = item.sub
                            break
                        }
                    }
                    if (subGroup.length != 0) {
                        for (let item of subGroup) {
                            if (item.group_name == newValue) {
                                return
                            }
                        }
                    }
                    item[3] = ''
                }
            }
        }

        this.hotSettings.afterChange = function(arr, source) {
            if (arr == null) {
                // 防止在loadData的时候报错
            } else {
                for (let item of arr) {
                    const row = item[0]
                    const colProp = item[1]
                    const oldValue = item[2]
                    const newValue = item[3]
                    let quoteData = this.getSourceData()
                    if (newValue != oldValue) {
                        //如果旧值和新值不一样，更新该行数据action
                        quoteData[row].action = 'change'
                        const colPropArr = colProp.split('.') //固定列的prop 不同于 后面列的prop
                        let prop = null
                        if (colPropArr.length === 1) {
                            //固定列的prop
                            prop = colProp.split('.')[0]
                            if (prop == 'superGroup') {
                                const groupCol = this.propToCol(colProp) + 1 // '小组'列的列数
                                if (newValue == '') {
                                    //大组删除时，小组也删除
                                    this.setDataAtCell(row, groupCol, '') //设置小组值为空
                                } else {
                                    //在大组值变化后，判断小组值是否属于该大组
                                    let subGroup = []
                                    const superGroupList = that.superGroupList
                                    for (let item of superGroupList) {
                                        if (item.group_name == newValue) {
                                            subGroup = item.sub
                                            break
                                        }
                                    }
                                    const groupValue = quoteData[row].group
                                    for (let item of subGroup) {
                                        if (item.group_name == groupValue) {
                                            return
                                        }
                                    }
                                    this.setDataAtCell(row, groupCol, '') //设置小组值为空
                                }
                            }
                        } else {
                            //后面不固定列的prop
                            prop = colProp.split('.')[2]
                            if (prop == 'precondition') {
                                if (newValue == '') {
                                    return //新值为空，就不能为precondition增加选项
                                }
                                //筛选是否有相同的选项
                                const hasDiffArr = that.selectOptionsData[prop].filter(item => {
                                    return item === newValue
                                })
                                if (hasDiffArr.length == 0) {
                                    //'前提'元格:可以自己手动增加下拉选项
                                    that.selectOptionsData[prop].push(newValue)
                                }
                            }
                        }
                    }
                }
            }
        }
        /**
         * 右键菜单操作方法
         */
        this.hotSettings.contextMenu.items.remove_row = removeRow //移除行
        this.hotSettings.contextMenu.items.remove_row.callback = function() {
            const curRowIndex = this.getSelectedLast()[0] //获得当前行的index
            that.$confirm('确认移除改行？', '确认信息', {
                distinguishCancelAndClose: true,
                confirmButtonText: '确认',
                cancelButtonText: '取消'
            })
            .then(() => {
                let quoteData = this.getSourceData()
                const curRowData = quoteData[curRowIndex]
                const taskId = curRowData['task_id']
                if (taskId == 0) {
                    quoteData.splice(curRowIndex, 1)
                    this.updateSettings({
                        data: quoteData
                    })
                    return
                }
                checkDeleteTask(that.quotationId, that.userId, taskId).then(res => {
                    if (res.data.result == 'OK') {
                        that.deleteList.push(quoteData[curRowIndex])
                        quoteData.splice(curRowIndex, 1)
                        this.updateSettings({
                            data: quoteData
                        })
                    } else {
                        Message({
                            message: res.data.error,
                            type: 'warning',
                            showClose: false,
                            duration: 2000
                        })
                    }
                })
            })
            .catch(action => {});
        }

        this.hotSettings.contextMenu.items.taskRecord = taskRecord
        this.hotSettings.contextMenu.items.taskRecord.callback = function() {
            const selectedCell = this.getSelected()
            const row = selectedCell[0][0]
            const data = this.getSourceData()
            const rowData = data[row]
            const taskId = rowData['task_id']
            let taskRecordTitle = ''
            const taskRecordKey = ['category_name', 'sub1', 'sub2', 'task1']
            for(let key of taskRecordKey) {
                if(rowData[key]) {
                    taskRecordTitle += rowData[key] + ' / '
                }
            }
            that.showHistory(taskRecordTitle)
            reqTaskHistory(taskId).then(res => {
                that.taskRecordList = []
                that.taskRecordList = res.data.content
                that.taskRecordLoading = false
            })
        }

        this.hotSettings.contextMenu.items.splitTask = splitTask //拆分Task
        this.hotSettings.contextMenu.items.splitTask.callback = function(key, selection, clickEvent) {
            // 添加下一行
            const curRowIndex = this.getSelectedLast()[0]
            let quoteData = this.getSourceData()
            const curRowDataIndex = curRowIndex
            const curRowData = JSON.parse(JSON.stringify(quoteData[curRowDataIndex]))
            const funcTaskList = that.funcTaskList
            for (let key in curRowData) {
                // 将上一行的整理（复制处理过的数据，生成新的一行）
                let value = curRowData[key]
                const optionList = that.optionList
                for (let item of optionList) {
                    // 小组key都变为null
                    if (key == item) {
                        for (let itemKey in value) {
                            let sonValue = value[itemKey]
                            for (let sonItemKey in sonValue) {
                                sonValue[sonItemKey] = null
                            }
                        }
                        continue
                    }
                }
                switch (key) {
                    case 'superGroup':
                        curRowData[key] = ''
                        break
                    case 'group':
                        curRowData[key] = ''
                        break
                    case 'group_name_list':
                        curRowData[key] = []
                        break
                    case 'action':
                        curRowData[key] = ''
                        break
                    case 'task_id':
                        curRowData[key] = 0
                        break
                    case 'category_name':
                        curRowData[key] = ''
                        break
                    default:
                        break
                }
                for (let item of funcTaskList) {
                    // 固定列都变为null
                    if (key == item) {
                        curRowData[key] = null
                        break
                    }
                }
            }
           quoteData.splice(curRowDataIndex + 1, 0, curRowData)
            // 添加task
            let setting = this.getSettings().__proto__
            let nestedHeadersList = JSON.parse(JSON.stringify(setting.nestedHeaders))
            let columnsSetting = setting.columns
            
            // set new colHeaders
            const taskList = columnsSetting.filter(item => {
                return item.data.indexOf('task') != -1
            })
            if (taskList.length === 1) {
                // Task限制: 只能有一层task
                this.updateSettings({
                    data: quoteData
                })
                return
            }
            
            const subList = columnsSetting.filter(item => {
                return item.data.indexOf('sub') != -1
            })
            const taskListLen = taskList.length
            const subListLen = subList.length
            const newColName = 'task' + (taskListLen + 1)
            // 修改表头显示数据（合并表头）
            nestedHeadersList[0].splice(taskListLen + subListLen + 1, 0, '')
            nestedHeadersList[1].splice(taskListLen + subListLen + 1, 0, '')
            nestedHeadersList[2].splice(subListLen + 1, 0, newColName) //表头第三行数据
            // set new columns
            const newSingleColSetting = {
                data: newColName //数据key值
            }
            columnsSetting.splice(subListLen + 1, 0, newSingleColSetting)
            
            that.funcTaskList.push(newColName)
            // set new table data
            const lenOfData = quoteData.length
            for (let i = 0; i < lenOfData; i++) {
                quoteData[i][newColName] = ''
            }
            let fixColumnsLeft = Number(setting.fixedColumnsLeft) + 1
            
            this.updateSettings({
                fixedColumnsLeft: fixColumnsLeft,
                nestedHeaders: nestedHeadersList,
                columns: columnsSetting,
                data: quoteData
            })
            
        }

        this.hotSettings.contextMenu.items.issue = issue //添加指摘
        this.hotSettings.contextMenu.items.issue.callback = function(key, selection, clickEvent) {
            const selectedCell = this.getSelected()
            const row = selectedCell[0][0]
            const col = selectedCell[0][1]
            const quotaData = this.getSourceData()
            const rowData = quotaData[row]
            that.row = row
            that.col = col
            const td = this.getCell(row, col)
            const colProp = this.colToProp(selectedCell[0][1])
            const splitArr = colProp.split('.')
            that.colProp = colProp
            const splitArrLen = splitArr.length - 1
            splitArr.splice(splitArrLen, 1)
            let value = rowData
            for (let key of splitArr) {
                value = value[key]
            }
            const baseIdKey = 'base_id'
            const baseId = value[baseIdKey]

            that.baseId = Number(baseId)
            that.pointVisible = true

            that.selectedCell = Object.assign({}, that.selectedCell, {
                width: Number(td.getClientRects()[0].width),
                height: Number(td.getClientRects()[0].height),
                top: Number(td.getClientRects()[0].top),
                right: Number(td.getClientRects()[0].right)
            })
        }
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
        this.hotSettings.afterScrollHorizontally = function() {
            that.hiddenDialog()
        }
        this.hotSettings.afterScrollVertically = function() {
            that.hiddenDialog()
        }

        this.hotSettings.afterSelectionEnd = function(row, column, row2, column2, selectionLayerLevel) {
            that.hiddenDialog()
            const colNum = this.getColHeader().length
            if(column2 - column + 1 === colNum) {
                // 默认禁止点击行头事件
                return
            }
            if (row == row2 && column == column2) {
                // case:只选中一个单元格的情况
                that.hiddenDialog()
                return
            }
            // case:多选单元格
            const selectedRowsNum = Math.abs(row2 - row) + 1
            const selectedColumnsNum = Math.abs(column2 - column) + 1
            const settings = this.getSettings().__proto__
            const fixColumnsNum = settings.fixedColumnsLeft
            /**
             * 统计选中区域的工数总和、已填写的工数数量
             */
            let selected = this.getSelected()
            let arrAfterFilter = filterRepeatData(selected)

            let manDaySum = 0
            let manDayFilledNum = 0
            manDaySum = arrAfterFilter.reduce((prev, cur) => {
                const curArr = cur.split(',')
                const curRow = curArr[0]
                const curCol = curArr[1]
                const curValue = this.getDataAtCell(curRow, curCol)
                if (typeof curValue == 'number') {
                    manDayFilledNum++
                    return prev + curValue
                }
                return prev
            }, 0)
            if (manDaySum == 0) {
                return
            }
            that.manDaySum = manDaySum
            that.manDayNum = manDayFilledNum
            let td = null
            //判断选择cell是从左向右，还是从右向左
            if (column2 > column) {
                //从左向右
                if (column2 < fixColumnsNum) {
                    //判断最后选择cell是否在固定列中
                    return
                }
                //计算工数
                td = this.getCell(row2, column2)
                that.showManDayDialog(td)
            } else if (column2 < column) {
                //从右向左
                if (column < fixColumnsNum) {
                    //判断最后选择cell是否在固定列中
                    return
                }
                //计算工数
                td = this.getCell(row, column)
                that.showManDayDialog(td)
            } else {
                //只选中一列
                if (column < fixColumnsNum) {
                    //判断最后选择cell是否在固定列中
                    return
                }
                if (this.getSelected()[0].length > 1) {
                    //选择行大于一行时，开始计算
                    if (row > row2) {
                        td = this.getCell(row, column)
                        that.showManDayDialog(td)
                    } else {
                        td = this.getCell(row2, column)
                        that.showManDayDialog(td)
                    }
                }
            }
        }
        this.getMyQuotation()
    },
    mounted() {
        
    },

    methods: {
        showManDayDialog(td) {
            this.manDayVisible = true
            this.selectedArea = Object.assign({}, this.selectedArea, {
                width: Number(td.getClientRects()[0].width),
                height: Number(td.getClientRects()[0].height),
                top: Number(td.getClientRects()[0].top),
                right: Number(td.getClientRects()[0].right)
            })
        },
        setBasicConfig(res) {
            // this.hotSettings.cells = cells //设置单元格样式(必须在请求数据之后才能设置,因为cellStyle中的this.instance没有)
            let settingsColumns = []
            let settingsData = []
            let nestedHeaders = [[], [], ['category']]
            let settingFiexedLeftNum = 0

            this.selectOptionsData = res.data.content.select_data //两个下拉框的选项
            let data = res.data.content

            this.funcTaskList = data.func_task_list //sub、task
            this.groupList = data.group_list //组名
            this.costList = data.cost_list //组下面的选项（days，precondition，comment，status）
            this.optionList = data.option_list //option
            /**
             * 表格列配置
             */
            let colPropList = getPrimedColPropList(data) //处理数据，返回预处理的列表头数据，用来下一步计算
            let dynamicColPropList = getDynamicColPropList(colPropList) ////获得表头列columns（不是固定列的部分）
            settingFiexedLeftNum = colPropList[0].length + 1 //固定列数
            settingsColumns.unshift({
                //手动添加category列，这里可以改进合并进下面代码
                data: 'category_name',
                readOnly: true,
                width: 100
            })
            colPropList[0].map(item => {
                //固定的前几列: task、sub
                let singleColSetting
                switch (item) {
                    case '分配大组':
                        singleColSetting = {
                            data: 'superGroup',
                            type: 'dropdown',
                            source: this.superGroupList.map(item => {
                                return item.group_name
                            }),
                            visibleRows: 10,
                            trimDropdown: true,
                            strict: true,
                            allowInvalid: false,
                            width: 100
                        }
                        break
                    case '分配小组':
                        singleColSetting = {
                            data: 'group',
                            type: 'dropdown',
                            source: this.superGroupList.reduce((prev, cur) => {
                                return prev.concat(
                                    cur.sub.map(item => {
                                        return item.group_name
                                    })
                                )
                            }, []),
                            visibleRows: 10,
                            trimDropdown: true,
                            strict: true,
                            allowInvalid: false,
                            width: 100
                        }
                        break
                    default:
                        singleColSetting = {
                            data: item,
                            editor: item.indexOf('task') != -1 ? 'text' : false,
                            readOnly: item.indexOf('task') != -1 ? false : true,
                            width: 100
                        }
                        break
                }
                settingsColumns.push(singleColSetting)
            })

            dynamicColPropList.map((item, index) => {
                // options
                let optionProp = item.split('.')[2]
                let singleColSetting = {
                    data: item
                }
                switch (optionProp) {
                    case 'days':
                        singleColSetting.type = 'numeric'
                        // singleColSetting.editor = CustomEditor
                        singleColSetting.renderer = costRenderer
                        break
                    case 'precondition':
                        singleColSetting.type = 'autocomplete'
                        singleColSetting.source = this.selectOptionsData[optionProp]
                        singleColSetting.visibleRows = 10
                        singleColSetting.trimDropdown = true
                        break
                    case 'status':
                        singleColSetting.type = 'dropdown'
                        singleColSetting.source = this.selectOptionsData[optionProp]
                        singleColSetting.visibleRows = 10
                        singleColSetting.trimDropdown = true
                        singleColSetting.strict = true
                        singleColSetting.allowInvalid = false
                        break
                    case 'comment':
                        singleColSetting.renderer =  customCommentRenderer
                        break
                    default:
                        break
                }
                settingsColumns.push(singleColSetting)
            })

            let funcTaskList = res.data.content.func_task_list
            let funcTaskLen = res.data.content.func_task_list.length - 2 // '大组' '小组'列重复不用清理
            let quoteList = res.data.content.data_list
            let quoteLen = res.data.content.data_list.length - 1
            if (quoteList.length != 0) {
                settingsData = clearRepeatData(funcTaskLen, quoteLen, funcTaskList, quoteList) //清理固定列重复数据
                for (let item of settingsData) {
                    item.superGroup = typeof item.group_name_list[0] == 'undefined' ? '' : item.group_name_list[0]
                    item.group = typeof item.group_name_list[1] == 'undefined' ? '' : item.group_name_list[1]
                }
            }

            /**
             * 合并表头list
             */
            const numOfOptions = colPropList[1].length * colPropList[2].length
            // 获得表头第三列数据
            nestedHeaders[2] = nestedHeaders[2].concat(colPropList[0])
            const tempArr = JSON.parse(JSON.stringify(colPropList[3]))
            tempArr[0] = 'cost'
            for (let i = 0; i < numOfOptions; i++) {
                nestedHeaders[2] = nestedHeaders[2].concat(tempArr)
            }

            // 获得表头第二列数据
            const numOfFixed = colPropList[0].length + 1
            nestedHeaders[1].push('Item and Scope')
            for (let i = 1; i < numOfFixed; i++) {
                nestedHeaders[1].push('')
            }
            for (let i = 0; i < colPropList[1].length; i++) {
                for (let j = 0; j < colPropList[2].length; j++) {
                    nestedHeaders[1].push({
                        label: colPropList[2][j],
                        colspan: 4
                    })
                }
            }
            // 获得表头第一列数据
            for (let i = 0; i < numOfFixed; i++) {
                nestedHeaders[0].push('')
            }
            for (let i = 0; i < colPropList[1].length; i++) {
                nestedHeaders[0].push({
                    label: colPropList[1][i],
                    colspan: colPropList[2].length * colPropList[3].length
                })
            }
            const groupList = this.groupList
            const optionList = this.optionList
            const dayKey = 'days'
            if(this.value == 'month') {
                const multiple = 0.05
                this.transDayForSave(settingsData, multiple, optionList, groupList, dayKey)
            }
            
            if (this.switchNum == 0) {
                //第一次进入，获取不到this.$refs.textHot.hotInstance
                this.hotSettings.fixedColumnsLeft = settingFiexedLeftNum //固定列数
                this.hotSettings.columns = settingsColumns
                this.hotSettings.data = settingsData
                this.hotSettings.nestedHeaders = nestedHeaders
            } else {
                // this.hotSettings.fixedColumnsLeft = settingFiexedLeftNum //固定列数
                // this.hotSettings.columns = settingsColumns
                // this.hotSettings.data = settingsData
                // this.hotSettings.nestedHeaders = nestedHeaders
                this.$refs.textHot.hotInstance.updateSettings({
                    fixedColumnsLeft: settingFiexedLeftNum, //固定列数
                    columns: settingsColumns,
                    data: settingsData,
                    nestedHeaders: nestedHeaders
                })
            }
        },
        getMyQuotation() {
            const promiseForGetMyQuotations = new Promise((resolve, reject) => {
                reqMyQuotations(this.userId, this.quotationId).then(res => {
                    if (res.data.result == 'OK') {
                        this.setQuotationDetail(res)
                        resolve(res)
                    } else {
                        reject()
                    }
                })
            })

            const promiseForGetGroup = new Promise((resolve, reject) => {
                reqGroupList(this.projId).then(res => {
                    if (res.data.result == 'OK') {
                        resolve(res.data.content)
                    } else {
                        reject()
                    }
                })
            })

            Promise.all([promiseForGetMyQuotations, promiseForGetGroup])
                .then(res => {
                    this.superGroupList = res[1]
                    this.setBasicConfig(res[0])
                    this.quoteType = true
                    this.showTable = true
                }).then(() => {
                    let copyright_logo = document.getElementById('hot-display-license-info')
                    copyright_logo.style = 'display:none'
                    this.fullscreeLoading = false
                    if(this.showMessageFlag) {
                        Message({
                            message: '保存成功',
                            type: 'success',
                            showClose: false,
                            duration: 1000
                        })
                        this.showMessageFlag = false
                    }
                })
                .catch(() => {
                    this.fullscreeLoading = false
                })
        },
        getAllQuotation() {
            const promiseForGetAllQuotations = new Promise((resolve, reject) => {
                reqAllQuotations(this.userId, this.quotationId)
                    .then(res => {
                        if (res.data.result == 'OK') {
                            this.setQuotationDetail(res)
                            resolve(res)
                        } else {
                            reject()
                        }
                    }).then(() => {
                        this.fullscreeLoading = false
                        if(this.showMessageFlag) {
                            Message({
                                message: '保存成功',
                                type: 'success',
                                showClose: false,
                                duration: 1000
                            })
                            this.showMessageFlag = false
                        }
                    })
                    .catch(err => {
                        this.fullscreeLoading = false
                    })
            })

            const promiseForGetGroup = new Promise((resolve, reject) => {
                reqGroupList(this.projId).then(res => {
                    if (res.data.result == 'OK') {
                        resolve(res.data.content)
                    } else {
                        reject()
                    }
                })
            })

            Promise.all([promiseForGetAllQuotations, promiseForGetGroup])
                .then(res => {
                    this.superGroupList = res[1]
                    this.setBasicConfig(res[0])
                    this.quoteType = false
                }).then(() => {
                    let copyright_logo = document.getElementById('hot-display-license-info')
                    copyright_logo.style = 'display:none'
                    this.fullscreeLoading = false
                })
                .catch(() => {
                    this.fullscreeLoading = false
                })
        },
        switchType() {
            MessageBox.confirm('此操作将会失去填写数据, 是否继续?', '提示', {
                cancelButtonClass: 'btn-custom-cancel',
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.fullscreeLoading = true
                this.getDiffTypeData()
            })
            .catch(() => {
                // do nothing
            })
        },
        getDiffTypeData() {
            if (this.switchNum == 0) {
                this.switchNum = 1
            }
            if (this.quoteType) {
                this.getAllQuotation() //请求报价工数（全部）
            } else {
                this.getMyQuotation() //请求报价工数（我的）
            }
        },
        hiddenDialog() {
            //隐藏弹窗
            this.pointVisible = false
            this.manDayVisible = false
        },
        setDaysCellStyle(status) {
            //设置工数单元格样式
            const row = this.row
            const col = this.col
            const quotaData = this.$refs.textHot.hotInstance.getSourceData()
            const rowData = quotaData[row]
            const colProp = this.colProp
            const splitArr = colProp.split('.')
            const splitArrLen = splitArr.length - 1
            splitArr.splice(splitArrLen, 1)
            let value = rowData
            for (let key of splitArr) {
                value = value[key]
            }    
            value.issue_status = status
            this.$refs.textHot.hotInstance.updateSettings({
                data: quotaData
            })
        },
        save() {
            this.showMessageFlag = true
            this.fullscreeLoading = true
            let dataList = JSON.parse(JSON.stringify(this.$refs.textHot.hotInstance.getSourceData())).map(item => {
                //处理大小组数据
                item.group_name_list = []
                if (item.superGroup != '') {
                    item.group_name_list[0] = item.superGroup
                    if (item.group != '') {
                        item.group_name_list[1] = item.group
                    }
                }
                return item
            })
            
            const tempArr  = this.transDayAfterSave(dataList, this.value)
            if(!tempArr) {
                this.fullscreeLoading = false
                Message({
                    message: '填写不规范,请修改!',
                    type: 'warning',
                    showClose: false,
                    duration: 3000
                })
                return
            }
            let data = {
                quotation_id: this.quotationId,
                commit_user: this.userId,
                select_data: this.selectOptionsData,
                data_list: tempArr,
                func_task_list: this.funcTaskList,
                group_list: this.groupList,
                cost_list: this.costList,
                option_list: this.optionList,
                delete_list: this.deleteList
            }
            setQuotationList(data)
                .then(res => {
                    if (res.data.result == 'OK') {
                        this.getNewDataAfterSave()
                        this.switchNum = 1
                    } else if (res.data.result == 'NG') {
                        Message({
                            message: res.data.error,
                            type: 'error',
                            showClose: true
                        })
                    }
                }).catch(err => {
                    this.fullscreeLoading = false
                })
        },
        getNewDataAfterSave() {
            if (this.quoteType) {
                this.getMyQuotation()
            } else {
                this.getAllQuotation()
            }
        },
        showHistory(title) {
            $('.shadow').animate({ right: '1px' }, 1000)
            this.taskRecordTitle = title
            this.taskRecordLoading = true
        },
        hide_shadow() {
            $('.shadow').animate({ right: '-2000px' }, 1000)
        },
        setQuotationDetail(res) {
            const data = res.data.content
            this.title.projName = '项目名：' + data.proj_name
            this.title.quotationName = '报价名：' + data.quotation_name
            this.title.version = '版本：' + data.quotation_ver
        },
        switchDaysUnit(value) {
            const groupList = this.groupList
            const optionList = this.optionList
            const data = this.$refs.textHot.hotInstance.getSourceData()
            const dayKey = 'days'
            if(value === 'day') {
                const multiple = 20
                this.transDay(data, multiple, optionList, groupList, dayKey)
            } else {
                const multiple = 0.05
                this.transDay(data, multiple, optionList, groupList, dayKey)
            }
        },
        transDay(data, multiple, optionList, groupList, dayKey) {
            for(let dataItem of data) {
                for(let optionKey of optionList) {
                    for(let groupKey of groupList) {
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
        transDayAfterSave(data, type) {
            const groupList = this.groupList
            const optionList = this.optionList
            const dayKey = 'days'
            let multiple = 0
            if(type == 'month') {
                multiple = 20
            } else {
                multiple = 1
            }
            return this.transDayForSave(data, multiple, optionList, groupList, dayKey)
        },
        transDayForSave(data, multiple, optionList, groupList, dayKey) {
            for(let dataItem of data) {
                for(let optionKey of optionList) {
                    for(let groupKey of groupList) {
                        if(checkNumber(dataItem[optionKey][groupKey][dayKey])) {
                            if(dataItem[optionKey][groupKey][dayKey] == '' || dataItem[optionKey][groupKey][dayKey] === null) { //为什么还要检测 值 === '',因为单元格删除数字时，值会变为''
                                dataItem[optionKey][groupKey][dayKey] = null
                            } else {
                                dataItem[optionKey][groupKey][dayKey] = dataItem[optionKey][groupKey][dayKey] * multiple
                                dataItem[optionKey][groupKey][dayKey] = Math.round(dataItem[optionKey][groupKey][dayKey] * 100)/100
                            }
                        } else {
                            dataItem[optionKey][groupKey][dayKey] = null
                            return false
                        }
                    }
                }
            }
            return data
        },
    }
}
</script>
<style>
@import './handsontable.css';
.container {
  width: 100%;
  height: 100%;
}
.title {
  float: left;
  font-size: 30px;
  font-weight: 600;
  margin-top: 10px;
  margin-left: 10px;
}
button {
  margin: 0;
}
.handsontable-wrapper {
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
  width: 1280px;
  height: calc(100% - 48px);
  position: fixed;
  background: rgba(255, 254, 255);
  top: 48px;
  right: -2000px;
  z-index: 666;
  text-align: left;
  border-radius: 5px;
  filter: drop-shadow(0 3px 5px black);
}
.el-icon-d-arrow-right {
  font-size: 24px;
  padding: 10px;
  cursor: pointer;
}
.btn-custom-cancel {
  float: right;
  margin-left: 10px;
}
.btn-switch {
  float: right;
  padding: 10px 15px 0 0;
}
</style>
