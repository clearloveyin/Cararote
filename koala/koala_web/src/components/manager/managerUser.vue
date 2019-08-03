<template>
    <div class="proj-quote-list warpper">
        <div class="container">
            <div class="header">
                <div class="left"><h2>PL管理</h2></div>
                <div class="right">
                    <span @click="add_PL" class="cursor">[&nbsp;&nbsp;增加&nbsp;&nbsp;]</span>
                    <span @click="post_data" class="cursor">[&nbsp;&nbsp;保存&nbsp;&nbsp;]</span>
                </div> 
            </div>
            <div class="content">
                <el-table :data="tableData" style="width: 80%;">
                    <el-table-column label="用户名" prop="user_name"></el-table-column>
                    <el-table-column label="超级PL" prop="super_pl">
                        <template slot-scope="scope">
                            <div>
                                <el-checkbox v-model="scope.row.super_pl" :disabled='scope.row.disabled'></el-checkbox>
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column label="PL" prop="pl">
                        <template slot-scope="scope">
                            <div>
                                <el-checkbox v-model="scope.row.pl" :disabled='scope.row.disabled'></el-checkbox>
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column align="center" label="删除" prop width="180">
                        <template slot-scope="scope">
                            <div>
                                <i @click="delete_row(scope.row)" class="el-icon-delete cursor"></i>
                            </div>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
            <el-dialog
                :modal="false"
                :title="dialog_title"
                :visible.sync="dialogVisible"
                width="25%"
            >
                <div>
                    <el-select filterable placeholder="请选择新用户" size="small" v-model="newUser">
                        <el-option
                            :key="user.user_id"
                            :label="user.user_name"
                            :value="user.user_id"
                            v-for="user in userOptions"
                        ></el-option>
                    </el-select>
                </div>
                <span class="dialog-footer" slot="footer">
                    <el-button @click="dialogVisible = false" size="small">取 消</el-button>
                    <el-button @click="handleClose()" size="small" type="primary">确 定</el-button>
                </span>
            </el-dialog>
        </div>
    </div>
</template>
<script>
import { getAllUser, getPL, addPL, updateUserPL } from '@/api/content_api'
export default {
    name: '',
    data() {
        return {
            tableData: [],
            dialogVisible: false,
            dialog_title: "增加新用户",
            dialog_data: "",
            newUser: "",
            userOptions: []
        }
    },
    mounted() {
        let cookie = this.$cookies.get('role')
        this.reqProjQuote()
    },
    methods: {
        reqProjQuote() {
            getAllUser().then(res => {
                // console.log(res.data, '-----------');
                if (res.data.result == 'OK') {
                    this.userOptions = res.data.content
                } else {
                }
            })
            getPL().then(res => {
                // window.sessionStorage.setItem("tempData",JSON.stringify(res.data.content))
                if (res.data.result == 'OK') {
                    this.tableData = res.data.content.map(item=>{
                            item.disabled = false
                        if (item.user_id == Number(this.$cookies.get('userId'))) {
                            item.disabled = true
                        }
                        return item
                    })

                } else {
                }
                // console.log(res.data, '=====', );
            })
        },
        delete_row(row) {
            this.$confirm('是否删除' + row.user_name + '?', '提示', {
                distinguishCancelAndClose: true,
                confirmButtonText: '确认',
                cancelButtonText: '取消'
            }).then(()=>{
                delete_func.call(this)
                this.post_data()
            }).catch(action => {
                return
          });
            function delete_func(){
                this.tableData = this.tableData.filter(user => {
                    return user.user_id !== row.user_id
                })
            }
            
        },
        add_PL() {
            this.dialogVisible = true
        },
        post_data() {
            let message = (type, msg) => {
                this.$message({
                    type: type,
                    message: msg
                })
            }
            updateUserPL(this.tableData).then(res => {
                if (res.data.result == 'OK') {
                    message('success', '成功')
                    this.reqProjQuote()
                } else {
                    message('error', '失败：' + res.data.error)

                }
            })

        },
        edit_su_pl(row) {
            this.dialog_data = row
            this.dialog_title = '超级PL:' + row.user_name
            this.dialogVisible = true
        },
        handleClose() {
            function check_user() {
                let flag = this.tableData.some(user => {
                    return user.user_id == Number(this.newUser)
                })
                return flag
            }
            const checkFlag = check_user.call(this)
            if (checkFlag == true) {
                this.$message({
                    type: 'warning',
                    message: '该用户已存在!'
                })
                this.newUser = ''
                return
            } else {
                let newUser = this.userOptions.filter(user => {
                    return user.user_id == this.newUser
                })
                let newUserData = {
                    pl: false,
                    super_pl: false,
                    user_id: newUser[0].user_id,
                    user_name: newUser[0].user_name,
                }
                // console.log(newUser);
                this.tableData.push(newUserData)
                this.newUser = ''
                this.dialogVisible = false
            }
        }

    }
}
</script>
<style scoped>
ul,
li {
    list-style: none;
}
.proj-quote-list {
    width: 100%;
    height: 100%;
    overflow-x: hidden;
    overflow-y: scroll;
    background: #f0f0f0;
    color: #303133;
    font-size: 14px;
}
.container {
    width: 1280px;
    height: 100%;
    margin-left: auto;
    margin-right: auto;
    background: #fff;
}
.content {
    width: 100%;
    padding-left: 10%;
}
.i {
    cursor: pointer;
}
.i :hover {
    color: #5e6d82;
}
.header {
    height: 40px;
    line-height: 40px;
    padding-left: 10%;
    padding-right: 10%;
}
.left {
    float: left;
}
.bold{
    font-weight: bold
}
.right {
    float: right;
}
.right span:first-child {
    margin: 0 40px;
}
@media screen and (max-width: 1280px) {
    .container {
        width: 100%;
    }
}
</style>