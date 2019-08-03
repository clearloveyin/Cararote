<template>
    <div class="warpper">
        <header class="header">
            <div class="header-left left-fl"></div>
            <div class="header-right right-fl">
                <el-upload action="https://jsonplaceholder.typicode.com/posts/" class="padding">
                    <el-button size="mini" type="primary">上传/添加</el-button>
                </el-upload>
                <div class="padding">
                    <el-button @click="deleteFun" size="mini" type="danger">删除</el-button>
                </div>
            </div>
        </header>
        <el-table
            :data="tableData"
            @selection-change="handleSelectionChange"
            ref="multipleTable"
            style="width: 100%"
            tooltip-effect="light"
        >
            <el-table-column type="selection" width="55"></el-table-column>
            <el-table-column label="Feature" prop="feature"></el-table-column>
            <el-table-column label="Compend" prop="compend"></el-table-column>
            <el-table-column label="Remark" prop="remark"></el-table-column>
        </el-table>
    </div>
</template>
<script>
import { login } from '@/api/serverApi'

export default {
    data () {
        return {
            tableData: [],
            multipleSelection: [],
            a: null
        }
    },
    mounted () {
        this.tableData = [{
            remark: '2016-05-03',
            feature: '王小虎',
            compend: '上海市普陀区金沙江路 1518 弄',
            id: 1
        }, {
            remark: '2016-05-02',
            feature: '王小虎',
            compend: '上海市普陀区金沙江路 1518 弄',
            id: 2
        }]
    },
    methods: {
        handleSelectionChange (val) {
            this.multipleSelection = val.map(item => {
                return item.id
            })
        },
        deleteFun () {
            this.tableData = this.tableData.filter(item => {
                return this.multipleSelection.indexOf(item.id) === -1
            })
        }
    }
}
</script>
<style lang="scss">
@import '@/style/commonStyle.scss';
</style>
