export function getTaskIndex(taskList, rowData) { //获得task index
    for (let i = 0; i < taskList.length; i++) {
        let taskValue = taskList[i]
        if (rowData[taskValue] != '' && rowData[taskValue] != null) {
            return i
        }
    }
}

export function getPrimedColPropList(data) { //处理数据，返回预处理的列表头数据，用来下一步计算
    let colPropList = [
        // ['sub1', 'sub2', 'task1', 'task2'],
        // ['options1', 'options2'],
        // ['guide', 'navi'],
        // ['option1', 'option2', 'option3']
    ]
    colPropList[0] = data.func_task_list.map(item => {
        return item
    })

    colPropList[1] = data.option_list
    colPropList[2] = data.group_list || []
    colPropList[3] = data.cost_list
    return colPropList //返回一个预处理过的list
}

export function getDynamicColPropList(colPropList) { //获得表头展示数据（不是固定列的部分）
    let dynamicColPropList = []
    switch (colPropList.length) {
        case 3: //工数汇总表
            for (let i = 0; i < colPropList[1].length; i++) {
                for (let j = 0; j < colPropList[2].length; j++) {
                    let item =
                        colPropList[1][i] + '.' + colPropList[2][j]
                    dynamicColPropList.push(item)
                }
            }
            break;
    
        default: //工数报价填写表
            for (let i = 0; i < colPropList[1].length; i++) {
                for (let j = 0; j < colPropList[2].length; j++) {
                    for (let k = 0; k < colPropList[3].length; k++) {
                        let item =
                            colPropList[1][i] + '.' + colPropList[2][j] + '.' + colPropList[3][k]
                        dynamicColPropList.push(item)
                    }
                }
            }
            break;
    }
    
    return dynamicColPropList
}

export function getDetailDynamicColPropList(colPropList) { // detail表格 :获得表头展示数据（不是固定列的部分）
    let dynamicColPropList = []
    for (let i = 0; i < colPropList[1].length; i++) {
        let tempArr = colPropList[2][i]
        for(let item of tempArr) {
            for (let k = 0; k < colPropList[3].length; k++) { 
                let prop = colPropList[1][i] + '.' + item + '.' + colPropList[3][k]
                // console.log(prop)
                dynamicColPropList.push(prop)

            }
        }
    }

    
    return dynamicColPropList
}

export function clearRepeatData(funcTaskLen ,quoteLen, funcTaskList, quoteList) {
    for (let i = quoteLen; i > 0; i--) { // 将数据结构整理成树状结构(重复的数据清空)
        // 合并category重复数据
        const categoryName = 'category_name'
        if (quoteList[i][categoryName] == quoteList[i - 1][categoryName]) {
            quoteList[i][categoryName] = ''
        }
        
        //合并sub task重复数据
        for (let j = 0; j < funcTaskLen; j++) {
            let param = funcTaskList[j]
            if (quoteList[i - 1][param] === null) {
                break
            }

            if (quoteList[i][param] == quoteList[i - 1][param]) {
                quoteList[i][param] = ''
            } else {
                break
            }
        }
    }
    return quoteList
}

export function getUrlHrefParams() { // 获得浏览器url中的参数
    const href = window.location.href
    const args = href.split('?')
    if (args[0] === href) {
        return ''
    }

    const arr = args[1].split('&')
    const obj = {}
    for (let item of arr) {
        const arg = item.split('=')
        obj[arg[0]] = arg[1]
    }
    return obj
}

// export function calculateFeatureManHour(quoteList, optionList ,groupList) {
//     let featureIndexList = []
//     const param = 'sub1'
//     const quoteLen = quoteList.length
//     //获得最高一级feature索引
//     for(let i = 0; i < quoteLen; i++) {
//         let featureValue = quoteList[i][param]
//         if(featureValue != '') {
//             featureIndexList.push(i)
//         }
//     }
//     const featureIndexLen = featureIndexList.length
//     for(let j = 0; j < featureIndexLen; j++) {
//         let featureIndex = featureIndexList[j]
//         let nextFeatureIndex = featureIndexList[j + 1]
//         // quoteList[featureIndex][param] = 
//         let featureHourman = 0
//         for(let k = featureIndex; k < nextFeatureIndex; k++) {
//             featureHourman += feature
//             for(let item) {

//             }
//         }
//     }
// }



export function checkNumber(val){ //检测是否符合day填写规范，因为填写时删除 值会变为''
    var regPos = /^[0-9]+$/; // 整数
    var regNeg = /^[0-9]+\.?[0-9]+?$/; // 小整数
    if(regPos.test(val) || regNeg.test(val) || val === null || val == ''){
        return true;
    }else{
        return false;
    }
}