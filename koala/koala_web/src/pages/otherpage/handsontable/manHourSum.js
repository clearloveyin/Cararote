export function hiddenManHourCount() {
    //隐藏工数总和统计方法
    let manHourCountDom = document.getElementsByClassName('man-hour-sum')[0]
    let cssData = 'display: none;'
    manHourCountDom.style = cssData
}
export function showManHourCount(td) {
    let manHourCountDom = document.getElementsByClassName('man-hour-sum')[0]
    let leftInstance = 'left: ' + Number(td.getClientRects()[0].right) + 'px;'
    let topInstance = 'top: ' + Number(td.getClientRects()[0].top) + 'px;'
    let cssData =
        'display: inline-block;position: fixed; width: 150px; height: 70px;z-index: 2000; font-size: 12px;' +
        leftInstance +
        topInstance
    manHourCountDom.style = cssData
}
export function isShowManHourCount(manHourSum) {
    if (manHourSum != 0) {
        return true
    }
    return false
}