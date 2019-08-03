import handsontable from 'handsontable-pro'
//工数不同状态表格样式
function noneCellRenderer(instance, td, row, col, prop, value, cellProperties) {
  handsontable.renderers.TextRenderer.apply(this, arguments)
}

function checkingCellRenderer(instance, td, row, col, prop, value, cellProperties) {
  handsontable.renderers.TextRenderer.apply(this, arguments)
  td.style.background = '#85ce61'
  td.style.color = '#fff'
  td.style['box-sizing'] = 'border-box'
}

function issueCellRenderer(instance, td, row, col, prop, value, cellProperties) {
  handsontable.renderers.TextRenderer.apply(this, arguments)
  td.style.background = '#d73a4a'
  td.style.color = '#fff'
  td.style['box-sizing'] = 'border-box'
}

function acceptCellRenderer(instance, td, row, col, prop, value, cellProperties) {
  handsontable.renderers.TextRenderer.apply(this, arguments)
  td.style.background = '#7057ff'
  td.style.color = '#fff'
  td.style['box-sizing'] = 'border-box'
}

handsontable.renderers.registerRenderer('noneCellRenderer', noneCellRenderer)
handsontable.renderers.registerRenderer('checkingCellRenderer', checkingCellRenderer)
handsontable.renderers.registerRenderer('issueCellRenderer', issueCellRenderer)
handsontable.renderers.registerRenderer('acceptCellRenderer', acceptCellRenderer)

export function customCommentRenderer(instance, td, row, col, prop, value, cellProperties) {
    const escaped = Handsontable.helper.stringify(value);
    let div = null;

    div = document.createElement('div');
    div.style="max-height: 100%;overflow-y: auto;overflow-x:hidden;text-align:left;"
    div.innerText = value;

    Handsontable.dom.empty(td);
    td.appendChild(div);

    return td;
}
// function strip_tags(input, allowed){
//     var tags = /<\/?([a-z][a-z0-9]*)\b[^>]*>/gi,
//         commentsAndPhpTags = /<!--[\s\S]*?-->|<\?(?:php)?[\s\S]*?\?>/gi

//     // making sure the allowed arg is a string containing only tags in lowercase (<a><b><c>)
//     allowed = (((allowed || '') + '').toLowerCase().match(/<[a-z][a-z0-9]*>/g) || []).join('')

//     return input.replace(commentsAndPhpTags, '').replace(tags, function($0, $1) {
//         return allowed.indexOf('<' + $1.toLowerCase() + '>') > -1 ? $0 : ''
//     })
// }
// export function customCommentRenderer(instance, td, row, col, prop, value, cellProperties) {
//     let escaped = Handsontable.helper.stringify(value);
//     escaped = strip_tags(escaped, '<b><i><u>');

//     let div = document.createElement('div');
//     div.style="max-height: 100%;overflow-y: auto;overflow-x:hidden;text-align: left;"
//     div.innerHTML = escaped;

//     Handsontable.dom.empty(td);
//     td.appendChild(div);

//     return td;
// }
export function costRenderer(instance, td, row, col, prop, value, cellProperties) {
  let data = instance.getSourceData()
  let rowData = data[row]
  const propArr = prop.split('.')
  const propArrLen = propArr.length - 1
  for (let i = 0; i < propArrLen; i++) {
    let key = propArr[i]
    rowData = rowData[key]
  }
  const issueStatus = rowData.issue_status
  handsontable.renderers.TextRenderer.apply(this, arguments);
  switch (issueStatus) {
    case '打开': //指摘+
      td.style.backgroundColor = '#d73a4a'
      break

    case '已确认': //指摘回复完了，已确认
      td.style.backgroundColor = '#85ce61'
      break

    case '关闭': //曾经被指摘
      td.style.backgroundColor = '#7057ff'
      break

    default:
      break
  }
  return td
}
export function cells(row, col) {
  let cellProperties = {}
  let data = this.instance.getSourceData()
  if (data.length == 0) {
    return cellProperties
  }
  const colProp = this.instance.colToProp(col)

  if (typeof colProp == 'number') {
    //有bug, 渲染在添加nestedHeaders之前
    return cellProperties
  }
  const splitArr = colProp.split('.')
  const splitArrLen = splitArr.length - 1
  if (splitArr[splitArrLen] == 'days') {
    let status = ''
    let value = data[row]
    for (let i = 0; i < splitArrLen; i++) {
      let key = splitArr[i]
      value = value[key]
    }
    console.log(value.issue_status, '=====')
    switch (value.issue_status) {
      case 'none': // 从来没有被指摘
        cellProperties.renderer = 'noneCellRenderer'
        break

      case '打开': //指摘
        cellProperties.renderer = 'issueCellRenderer'
        break

      case '已确认': //指摘回复完了，等待确认
        cellProperties.renderer = 'checkingCellRenderer'
        break

      case '关闭': //曾经被指摘
        cellProperties.renderer = 'acceptCellRenderer'
        break

      default:
        cellProperties.renderer = 'noneCellRenderer'
        break
    }
  }
  return cellProperties
}
var handleHotBeforeOnCellMouseDown = function(event, coords, element) {
  if (coords.row < 0) {
    //禁止表头事件
    event.stopImmediatePropagation()
  }
}
handsontable.hooks.add('beforeOnCellMouseDown', handleHotBeforeOnCellMouseDown)

export let Handsontable = handsontable
