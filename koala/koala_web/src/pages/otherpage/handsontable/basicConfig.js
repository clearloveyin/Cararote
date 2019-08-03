let basicHotSettings = {
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
    contextMenu: {
        //自定义右键菜单，可汉化，默认布尔值
        items: {
            // row_below: {
            //     // name: '下方插入一行'
            // },
            // col_right: {
            //     // name: '添加子task',
            // },
            // hsep1: '---------', //提供分隔线
            // remove_row: {
            //     // name: '删除行'
            // },
            // remove_col: {},
            // make_read_only: {
            // name: '只读'
            // },
            // borders: {
            // name: '表格线'
            // },
            // commentsAddEdit: {
            //     // name: '添加备注'
            // },
            // commentsRemove: {
            //     // name: '取消备注'
            // },
        }
    }, //右键效果
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
    trimRows: [],
    exportFile: true,
    // dropdownMenu: true,
    // filters: true
}

export default basicHotSettings