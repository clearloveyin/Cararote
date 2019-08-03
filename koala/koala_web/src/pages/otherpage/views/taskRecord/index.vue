<template>
    <div class="task-record">
        <div class="task-record-container">
            <div class="task-record-header">
                <h1>
                    <svg class="octicon" viewBox="0 0 12 16" version="1.1" width="12" height="16" aria-hidden="true">
                        <path fill-rule="evenodd" d="M4 9H3V8h1v1zm0-3H3v1h1V6zm0-2H3v1h1V4zm0-2H3v1h1V2zm8-1v12c0 .55-.45 1-1 1H6v2l-1.5-1.5L3 16v-2H1c-.55 0-1-.45-1-1V1c0-.55.45-1 1-1h10c.55 0 1 .45 1 1zm-1 10H1v2h2v-1h3v1h5v-2zm0-10H2v9h9V1z"></path>
                    </svg>
                    履历:{{taskRecordTitle}}
                </h1>
            </div>

            <el-table :data="taskRecordList" stripe style="width: 100%" size="medium" border
                :header-cell-style="{background:'#f0f0f0'}">
                <el-table-column prop="group_name" label="组">
                </el-table-column>
                <el-table-column prop="option" label="option">
                </el-table-column>
                <el-table-column prop="days" label="工数(人/日)">
                </el-table-column>
                <el-table-column prop="precondition" label="前提">
                </el-table-column>
                <el-table-column prop="comment" label="注释">
                </el-table-column>
                <el-table-column prop="update_user" label="修改人">
                </el-table-column>
                <el-table-column prop="update_time" label="时间">
                </el-table-column>
            </el-table>
        </div>
    </div>
</template>
<script>
export default {
    name: 'taskRecord',
    props: ['taskRecordList', 'taskRecordTitle'],
    watch: {
        taskRecordList(value) {
            console.log(value)
        }
    },
    data() {
        return {}
    }
}
</script>
<style scoped>
.task-record {
    width: 100%;
    height: 100%;
    overflow-x: hidden;
    overflow-y: auto;
    /* background: #f0f0f0; */
}
.task-record-container {
    width: 100%;
    height: 100%;
    margin-left: auto;
    margin-right: auto;
    background: #ffffff;
}
.task-record-header {
    margin-bottom: 20px;
    /* padding-top: 20px; */
}
.task-record h1 {
    color: #586069;
    /* float: left; */
    font-size: 18px;
    line-height: 26px;
    max-width: 635px;
    padding-left: 18px;
    position: relative;
    font-weight: 400;
    color: #0366d6;
    /* margin-bottom: 0; */
}
.octicon {
    color: #959da5;
    left: 0;
    margin-top: 5px;
    position: absolute;
    top: 0;
    vertical-align: text-bottom;
    fill: currentColor;
}
</style>