import { beforeClick, zTreeOnClick } from './treeFunction'
let setting = {
    view: {
        // showLine: false,
        // showIcon: false,
        selectedMulti: false,
        dblClickExpand: false,
        txtSelectedEnable: false,
        fontCss: { color: '', background: '' }
    },
    check: {
        // 打开checkBox框配置
        enable: false,
        nocheckInherit: false,
        chkboxType: { Y: 'p', N: 's' }
    },
    data: {
        // 配置渲染data的类型，simpleData：简单平铺开的json格式，标准格式则是默认模式
        key: {
            name: 'name' // 配置要显示的key参数
            },
        // simpleData: {
        //     enable: true,
        //     idKey: 'model_id',
        //     pIdKey: 'parent_id',
        //     rootPid: null
        // }
    },
    callback: {
        beforeClick: beforeClick,
        onClick: zTreeOnClick
    }
}
export default setting
