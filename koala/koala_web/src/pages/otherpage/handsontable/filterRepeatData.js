
export function filterRepeatData(data) {
    let cellArr = []
    for(let item of data) {
        const minRow = Math.min(item[0], item[2])
        const maxRow = Math.max(item[0], item[2])
        const minCol = Math.min(item[1], item[3])
        const maxCol = Math.max(item[1], item[3])
        for(let i = minRow; i <= maxRow; i++) {
            for(let j = minCol; j <= maxCol; j++ ) {
                cellArr.push(i + ',' + j)
            }
        }
    }
    
    const arrAfterFilter = [...new Set(cellArr)]
    return arrAfterFilter
}
// export function getRepeatArea(data) {
//     let areaData = data
//     // [
//     //     // [left, top, right, bottom]
//     //     [0, 2, 5, 3],
//     //     [4, 5, 0, 3]
//     // ]
//     let len = areaData.length
//     let repeatArea = []

//     console.log(areaData, 'areaData')


//     for(let i = 0;  i < len - 1; i++) {
//         for(let j = i + 1; j < len; j++) {
            
//             // 判断是否重叠
//             // 不重叠的情况
//             let p1 = getCorrectAreaData(areaData[i])
//             let p2 = getCorrectAreaData(areaData[j])
//             function getCorrectAreaData(areaData) {
//                 if(areaData[0] >= areaData[2]) {
//                     let tempNum = 0
//                     tempNum = areaData[0]
//                     areaData[0] = areaData[2]
//                     areaData[2] = tempNum
//                     tempNum = areaData[1]
//                     areaData[1] = areaData[3]
//                     areaData[3] = tempNum
//                 }
//                 return areaData
//             }
//             /**
//              * 第一种判断重叠的情况
//              *  p1[3] <= p2[1] || p1[1] >= p2[3] || p1[3] <= p2[1] || p1[1] >= p2[3]  逆向思维，判断是否不重叠
//              */
//             /**
//              * 第二种判断重叠的情况
//              * 如果不相交， Math.max(p1[0], p2[0]) > Math.min(p1[2], p2[2]) 或者Math.min(p1[2], p2[2]) > Math.min(p1[3], p2[3])
//              * 
//              * 
//              */
//             if(
//                 (p1[3] < p2[1] || p1[1] > p2[3] || p1[3] < p2[1] || p1[1] > p2[3]) 
//                 // || 
//                 // (p2[3] <= p1[1] || p2[1] >= p1[3] || p2[3] <= p1[1] || p2[1] >= p1[3])
//             )  { //不重叠的情况
//                 // do nothing
//             } else { //重叠的情况
//                 // 获得重叠区域的坐标
//                 console.log(i, 'i', j, 'j')
//                 let tempRepeatArr = [
//                     Math.max(p1[0], p2[0]),
//                     Math.max(p1[1], p2[1]),
//                     Math.min(p1[2], p2[2]),
//                     Math.min(p1[3], p2[3])
//                 ]
//                 repeatArea.push(tempRepeatArr)
//             }
//         }
//     }
//     return repeatArea
// }