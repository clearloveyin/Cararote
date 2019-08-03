<template>
    <div id="point-container" @mousewheel.prevent @click.stop.prevent @mousedown.stop>
        <h3 class="point-title" style="margin-top: 0;margin-bottom: 5px;">指摘{{quotationId}}</h3>
        <div class="point-title">
            <span>状态</span>
            <span class="xinhao">*</span>
            <span>:</span>
            <select v-model="status">
                <option value="" disabled hidden style="color: #606266;">请选择</option>
                <option v-for="(item, index) in statusOptionsList" :key="index">{{item}}</option>
            </select>
        </div>
        <div class="point-title">
            <span>指摘内容</span>
            <span class="xinhao">*</span>
            <span>：</span>
        </div>
        <el-input type="textarea" placeholder="请输入内容" v-model="issueComment" :autosize="{ minRows: 4, maxRows: 4 }" :clearable=true>
        </el-input>
        <div class="point-btn-bar">
            <el-button type="info" size="mini" @click="hiddenPoint">取消</el-button>
            <el-button type="success" size="mini" @click="saveIssue">提交</el-button>
        </div>
        <div id="point-list" @mousewheel.prevent v-loading="issueListLoading">
            <div class="point-list-item" v-for="item of issueRecord">
                <div style="font-size: 14px;color: #24292e!important;font-weight: 600;">{{item.comment}}</div>
                <div style="font-size: 12px;color: #586069!important;
                    line-height: 1.25!important;">#{{item.issue_user}} {{item.status}} {{item.commit_time}}</div>
            </div>
        </div>
        <i class="point-arrow" :class="activePointArrow"></i>
    </div>
</template>
<script>
import { reqIssue, addIssue } from '../../../api/hansontable.js'
export default {
    name: 'pointDialog',
    props: {
        pointVisible: {
            type: Boolean,
            default: false
        },
        selectedCell: {
            type: Object,
            default() {
                return {}
            }
        },
        baseId: {
            type: Number,
            default: 0
        },
        quotationId: {
            type: Number,
            default: 0
        }
    },
    model: {
        prop: 'pointVisible',
        event: 'click'
    },
    watch: {
        pointVisible(value) {
            if (value) {
                this.calculatePointPosition()
                if (this.baseId != 0) {
                    this.issueListLoading = true
                    reqIssue(this.baseId)
                        .then(res => {
                            const data = res.data.content
                            this.issueRecord = data.issue_list
                            this.statusOptionsList = data.status_list
                            this.status = ''
                            this.issueComment = ''
                            this.issueListLoading = false
                        })
                        .catch(err => {
                            this.issueListLoading = false
                        })
                }
            }
        }
    },
    data() {
        return {
            issueComment: '',
            issueListLoading: false,
            activePointArrow: '',
            issueRecord: [],
            statusOptionsList: [],
            status: ''
        }
    },
    methods: {
        hiddenPoint() {
            // this.pointVisible = false
            this.$emit('update:pointVisible', false)
        },
        saveIssue() {
            const comment = this.issueComment.trim()
            const status = this.status
            if (comment == ''|| status == '') {
                this.$message({
                    type: 'warning',
                    message: '状态、指摘内容不能为空',
                    duration: 2000
                })
                return
            }
            let data = {
                comment: comment,
                issue_user: (this.userId = this.$cookies.get('userId')),
                base_id: this.baseId,
                status: status,
                quotation_id: this.quotationId
            }
            addIssue(data).then(res => {
                if (res.data.result == 'OK') {
                    this.$emit('setDaysStatus', status)
                    this.hiddenPoint()
                    this.$message({
                        type: 'success',
                        message: '提交成功',
                        duration: 2000
                    })
                } else {
                    this.$message({
                        type: 'error',
                        message: '提交失败',
                        duration: 0,
                        showClose: true
                    })
                }
            })
        },
        calculatePointPosition() {
            const clientWidth = document.body.offsetWidth
            const clientHeight = document.body.offsetHeight
            const pointWidth = 290
            const pointHeight = 338
            const tdWidth = Number(this.selectedCell.width)
            const tdHeight = Number(this.selectedCell.height)
            const tdTop = Number(this.selectedCell.top)
            const tdLeft = Number(this.selectedCell.right)
            let leftInstance
            let topInstance
            let pointStyle
            function setLeftStyle(value) {
                return 'left: ' + value + 'px;'
            }
            function setTopStyle(value) {
                return 'top: ' + value + 'px;'
            }
            if (clientWidth >= tdLeft + pointWidth) {
                //浏览器宽度 大于 指摘+定位总宽度
                leftInstance = setLeftStyle(tdLeft + 8)
                if (clientHeight >= tdTop + pointHeight) {
                    //浏览器高度 大于 指摘+定位总高度
                    topInstance = setTopStyle(tdTop)
                    this.activePointArrow = 'point-arrow-left-top'
                } else {
                    //浏览器高度 小于 指摘+定位总高度
                    if (pointHeight >= tdTop) {
                        //指摘高度 大于 td top
                        topInstance = setTopStyle(tdTop)
                        this.activePointArrow = 'point-arrow-left-top'
                    } else {
                        topInstance = setTopStyle(tdTop - pointHeight + tdHeight)
                        this.activePointArrow = 'point-arrow-left-bottom'
                    }
                }
            } else {
                //浏览器宽度 大于 指摘+定位总宽度
                leftInstance = setLeftStyle(tdLeft - tdWidth - pointWidth)
                if (clientHeight >= tdTop + pointHeight) {
                    //浏览器高度 大于 指摘+定位总高度
                    topInstance = setTopStyle(tdTop)
                    this.activePointArrow = 'point-arrow-right-top'
                } else {
                    //浏览器高度 小于 指摘+定位总高度
                    if (pointHeight >= tdTop) {
                        //指摘高度 大于 td top
                        topInstance = setTopStyle(tdTop)
                        this.activePointArrow = 'point-arrow-right-top'
                    } else {
                        topInstance = setTopStyle(tdTop - pointHeight + tdHeight)
                        this.activePointArrow = 'point-arrow-right-bottom'
                    }
                }
            }
            let pointContentDom = document.getElementById('point-container')
            pointStyle = leftInstance + topInstance
            pointContentDom.style = pointStyle
        }
    }
}
</script>
<style scoped>
#point-container {
    position: fixed;
    left: 361px;
    top: 350px;
    width: 240px;
    height: 365px;
    background-color: #fff;
    filter: drop-shadow(0 3px 5px black);
    border: 1px solid #d1d5da;
    /* border-radius: 3px; */
    padding: 18px 20px;
    z-index: 2000;
}
.point-arrow {
    position: absolute;
    width: 0;
    height: 0;
    overflow: hidden;
    border: 7px solid transparent;
}

.point-arrow-left-top {
    left: -14px;
    top: 8px;
    border-right-color: #fff;
}
.point-arrow-left-bottom {
    left: -14px;
    top: 316px;
    border-right-color: #fff;
}
.point-arrow-right-top {
    left: 280px;
    top: 8px;
    border-left-color: #fff;
}
.point-arrow-right-bottom {
    left: 280px;
    top: 316px;
    border-left-color: #fff;
}
#point-container textarea {
    resize: none;
}
.point-title {
    text-align: left;
}
.point-btn-bar {
    text-align: right;
    margin-top: 10px;
    margin-bottom: 10px;
}
#point-list {
    height: 150px;
    overflow-x: hidden;
    overflow-y: auto;
    text-align: left;
    list-style-type: none;
    font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif, Apple Color Emoji,
        Segoe UI Emoji, Segoe UI Symbol;
}
.point-list-item {
    padding: 5px 8px;
    border-width: 0 1px 1px;
    border-style: solid;
    border-color: #e1e4e8;
}
.point-list-item {
    padding: 5px 8px;
    border-width: 0 1px 1px;
    border-style: solid;
    border-color: #e1e4e8;
}
.point-list-item:first-of-type {
    border-width: 1px;
}
.xinhao {
    color: red;
    vertical-align: sub;
}
</style>