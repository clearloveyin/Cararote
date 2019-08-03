<template>
    <div id="app">
        <router-view/>
    </div>
</template>

<script>
export default {
    name: 'App'
}
</script>

<style >
* {
    margin: 0;
    padding: 0;
}
#app {
    font-family: 'Microsoft YaHei', 微软雅黑, 'MicrosoftJhengHei', 华文细黑, STHeiti, MingLiu;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    width: 100%;
    height: 100%;
    position: fixed;
    min-width: 1000px;
    /* color: #5e6d82; */
    color: #303133;
}

/* 自定义更改饿了么UI局部组件样式 */
.warpper {
    font-size: 14px;
}

.warpper .el-switch__label.is-active {
    /* color: #42b983; */
    font-weight: 600;
}
.warpper .local-element .el-upload {
    width: 100%;
}
.warpper .active {
    font-size: 18px;
    font-weight: 600;
}
.warpper .cursor {
    cursor: pointer;
}
.warpper .cursor:hover {
    color: #00a597;
}
.warpper .el-dialog__header,
.warpper .el-dialog__body {
    padding: 5px 20px 10px 20px;
    padding-bottom: 10px;
    /* padding-left: 20px */
}
/* handsontable表格样式自定义 */

.warpper .handsontable th {
    background-color: rgb(253, 233, 217);
}

.handsontable .ht_clone_top_left_corner th {
    background-color: rgb(183, 222, 232);
}
.warpper .el-upload-list__item {
    width: 43%;
}
.warpper .handsontable .majorClass {
    background-color: rgb(195, 255, 203);
}
.warpper .handsontable .minorClass {
    background-color: rgb(255, 251, 189);
}

.warpper .handsontable .htAutocomplete {
    text-align: center;
}
#example-container .handsontable .ht_clone_top th {
    background-color: rgb(253, 233, 217);
}
.shadow .handsontable .ht_clone_top th {
    background-color: rgb(253, 233, 217);
}
.pl-review-container .handsontable .blueCell {
    background: rgb(253, 233, 217);
}
.pl-review-container .handsontable .redCell {
    background: rgb(183, 222, 232);
}
</style>
