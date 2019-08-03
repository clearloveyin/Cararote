import { getTaskIndex, getDynamicColPropList, clearRepeatData } from './someMethods' //整理数据方法
export let taskRecord = { //右键履历
    name: '履历',
    disabled() {
        const selectedCell = this.getSelected()
        if(typeof selectedCell == 'undefined') { //限制表头dom事件，导致的错误
            return true
        }
        if (selectedCell.length > 1) {
            return true
        }
        if (selectedCell[0][0] == selectedCell[0][2] && selectedCell[0][1] == selectedCell[0][3]) {
            const row = selectedCell[0][0]
            const data = this.getSourceData()
            const rowData = data[row]
            const taskId = rowData['task_id']
            if (taskId == 0) {
                return true
            }
            return false
        }
        return true
    },
    callback() {}
}

export let issue = { //右键指摘
    name: '指摘',
    disabled() {
        const selectedCell = this.getSelected()
        if(typeof selectedCell == 'undefined') { //限制表头dom事件，导致的错误
            return true
        }
        if (selectedCell.length > 1) {
            return true
        }
        if (selectedCell[0][0] == selectedCell[0][2] && selectedCell[0][1] == selectedCell[0][3]) {
            const colProp = this.colToProp(selectedCell[0][1])
            const splitArr = colProp.split('.')
            const splitArrLen = splitArr.length - 1
            if (splitArr[splitArrLen] == 'days') { //只有工数可以指摘
                const row = selectedCell[0][0]
                const col = selectedCell[0][1]
                const rowData = this.getSourceData()[row]

                const colProp = this.colToProp(selectedCell[0][1])
                splitArr.splice(splitArrLen, 1)
                let value = rowData
                for (let key of splitArr) {
                    value = value[key]
                }
                const baseIdKey = 'base_id'
                const baseId = value[baseIdKey]
                if(baseId != 0) { //base_id 为0时，不能指摘
                    return false
                }
            }
        }
        return true
    },
    callback() {}
}


export let removeRow = {
    disabled() {
        //只能删除没有子级的行
        const selectedCell = this.getSelected()
        if(typeof selectedCell == 'undefined') { //限制表头dom事件，导致的错误
            return true
        }
        if (selectedCell.length > 1) {
            //选中多块区域，不能删除行
            return true
        }
        if (selectedCell[0][0] == selectedCell[0][2]) {
            //只能删除一行
            const quoteData = this.getSourceData()
            const curRowIndex = this.getSelectedLast()[0] //页面显示行数
            const curRowData = this.getSourceData()[curRowIndex] // 当前行数据
            if (curRowData['task_id'] == 0) {
                //task_id为0说明为新增的行，可以直接删除
                return false
            }

            const nextRowData = quoteData[curRowIndex + 1] || 'noLastRow'

            let columnsSetting = this.getSettings().__proto__.columns

            function assembleSub(previousValue, currentValue) {
                if (currentValue.data.indexOf('sub') != -1) {
                    previousValue.push(currentValue.data)
                }
                return previousValue
            }

            function assembleTask(previousValue, currentValue) {
                if (currentValue.data.indexOf('task') != -1) {
                    previousValue.push(currentValue.data)
                }
                return previousValue
            }

            const subList = columnsSetting.reduce(assembleSub, [])
            const taskList = columnsSetting.reduce(assembleTask, [])
            for (let item of subList) {
                if (curRowData[item] == '') {
                    continue
                } else {
                    //feature有值的情况下，不能删除
                    return true
                }
            }
            //feature没值值的情况下，再判断task有没有值
            let curRowTaskIndex = getTaskIndex(taskList, curRowData)
            if(nextRowData === 'noLastRow') { //没有下一行
                return false
            }
            let nextRowTaskIndex = getTaskIndex(taskList, nextRowData)
            if (curRowTaskIndex + 1 == nextRowTaskIndex) {
                //父子关系
                return true
            } else {
                return false
            }
        } else {
            //不能同时删除多行，除非都是新增的行
            return true
        }

        return true
    }
}

export const splitTask = { // 拆分task
    name: '拆分Task',
    disabled() {
        const selectedCell = this.getSelected()
        if(typeof selectedCell == 'undefined') { //限制表头dom事件，导致的错误
            return true
        }
        if (selectedCell.length > 1) {
            //选中多块区域，不能拆分task
            return true
        }
        if(selectedCell[0][0] === selectedCell[0][2]) {
            return false
        }
        return true
    }
}

export const lookDetail = { // 查看详细
    name: '详细',
    disabled() {
        const selectedCell = this.getSelected()
        if (typeof selectedCell == 'undefined') {
            //限制表头dom事件，导致的错误
            return true
        }
        if (selectedCell.length > 1) {
            //选中多块区域，不能拆分task
            return true
        }
        if (selectedCell[0][0] === selectedCell[0][2]) {
            return false
        }
        return true
    }
}