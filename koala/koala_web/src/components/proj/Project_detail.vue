<template>
    <div class="warpper">
        <div class="pro-content">
            <ul class="pro-nav">
                <div class="menu">
                    <el-breadcrumb separator-class="el-icon-arrow-right">
                        <el-breadcrumb-item>项目列表</el-breadcrumb-item>
                        <el-breadcrumb-item>项目详细</el-breadcrumb-item>
                    </el-breadcrumb>
                </div>
                <li>
                    <span @click="cancel_fun()" class="cursor">[ 返回 ]</span>
                </li>

                <li>
                    <span @click="push_quotation()" class="cursor" v-if="show_edit_flag">[ 发起报价 ]</span>
                </li>
                <li>
                    <span @click="push_system_table()" class="cursor" v-if="SALES || SGL">[ 修改体制 ]</span>
                </li>
                <li>
                    <span @click="editProj()" class="cursor" v-if="show_edit_flag">[ 编辑 ]</span>
                </li>
            </ul>
            <div style="clear:both"></div>
            <div class="msg-box">
                <div class="detail-box">
                    <span>项目名称</span>
                    <div class="detail-box-item msg-content">{{data_json.inside_i_name}}</div>
                </div>
                <div class="detail-box">
                    <span>状态</span>
                    <div class="detail-box-item msg-content">{{data_json.proj_i_state}}</div>
                </div>
                <div class="detail-box">
                    <span>项目系列</span>
                    <div class="detail-box-item msg-content">{{data_json.proj_i_type}}</div>
                </div>
                <div class="detail-box">
                    <span>负责人</span>
                    <div class="detail-box-item msg-content">{{data_json.user_name}}</div>
                </div>
                <div class="detail-box">
                    <span>PL</span>
                    <div class="detail-box-item msg-content">
                        <span
                            :key="index"
                            v-for="(observer_name,index) in data_json.observer_name_list"
                        >{{observer_name.name}}&nbsp;&nbsp;</span>
                    </div>
                </div>
                <div class="detail-box">
                    <span>创建时间</span>
                    <div class="detail-box-item msg-content">{{data_json.commit_time}}</div>
                </div>
                <div class="detail-box">
                    <span>修改时间</span>
                    <div class="detail-box-item msg-content">{{data_json.update_time}}</div>
                </div>
                <div class="detail-box">
                    <span>描述</span>
                    <div class="detail-box-item msg-content">{{data_json.describe}}</div>
                </div>
                <div class="detail-box">
                    <span>报价列表</span>
                </div>
                <el-table :data="quotations_list" style="width: 100%">
                    <el-table-column label="报价名称" prop="quotation_name"></el-table-column>
                    <el-table-column label="报价版本" prop="quotation_ver"></el-table-column>
                    <el-table-column label="报价状态" prop="status"></el-table-column>
                    <el-table-column label="描述" prop="destribe"></el-table-column>
                    <el-table-column label="创建人" prop="create_user"></el-table-column>
                    <el-table-column label="创建日期" prop="create_time"></el-table-column>
                    <el-table-column label="更新日期" prop="update_time"></el-table-column>
                    <template v-if="SALES || SGL">
                        <el-table-column
                            align="center"
                            label="待分配数"
                            prop="count_not_assign"
                            width="80"
                        >
                            <template slot-scope="scope">
                                <el-button
                                    :disabled="!scope.row.checkout_flag"
                                    @click="assignHourMan(scope.row.proj_id, scope.row.quotation_id)"
                                    type="text"
                                    v-if="scope.row.check_status_flag"
                                >{{scope.row.count_not_assign}}</el-button>
                                <el-button
                                    @click="assignHourMan(scope.row.proj_id, scope.row.quotation_id)"
                                    type="text"
                                    v-else
                                >{{scope.row.count_not_assign}}</el-button>
                            </template>
                        </el-table-column>
                    </template>
                    <template v-if="SGL">
                        <el-table-column
                            align="center"
                            label="待确认数"
                            prop="count_not_confirm"
                            width="80"
                        >
                            <template slot-scope="scope">
                                <el-button
                                    :disabled="!scope.row.checkout_flag"
                                    type="text"
                                    v-if="scope.row.check_status_flag"
                                >{{scope.row.count_not_confirm}}</el-button>
                                <a
                                    :href="'cell.html?quotationId=' + scope.row.quotation_id + '&projId=' + scope.row.proj_id"
                                    rel="noopener noreferrer"
                                    target="_blank"
                                    v-else
                                >
                                    <el-button type="text">{{scope.row.count_not_confirm}}</el-button>
                                </a>
                            </template>
                        </el-table-column>
                    </template>
                    <template v-if="GL">
                        <el-table-column
                            align="center"
                            label="待报价数"
                            prop="count_not_quotation"
                            width="80"
                        >
                            <template slot-scope="scope">
                                <el-button
                                    :disabled="!scope.row.checkout_flag"
                                    type="text"
                                    v-if="scope.row.check_status_flag"
                                >{{scope.row.count_not_quotation}}</el-button>

                                <a
                                    :href="'cell.html?quotationId=' + scope.row.quotation_id + '&projId=' + scope.row.proj_id"
                                    rel="noopener noreferrer"
                                    target="_blank"
                                    v-else
                                >
                                    <el-button type="text">{{scope.row.count_not_quotation}}</el-button>
                                </a>
                            </template>
                        </el-table-column>
                    </template>
                    <template v-if="SALES">
                        <el-table-column
                            align="center"
                            label="工数汇总"
                            prop="count_not_admit"
                            width="100"
                        >
                            <template slot-scope="scope">
                                <el-button
                                    @click="goSummaryAccount(scope.row.quotation_id)"
                                    type="text"
                                >工数汇总</el-button>
                            </template>
                        </el-table-column>
                    </template>
                    <el-table-column label="单次报价构成图">
                        <template slot-scope="scope">
                            <el-button
                                @click="look_quotation_pie(scope.row.quotation_id)"
                                type="text"
                            >查看</el-button>
                        </template>
                    </el-table-column>
                </el-table>
                <el-pagination
                    :total="total"
                    @current-change="current_change"
                    layout="prev, pager, next"
                    small
                    v-if="total!=0"
                ></el-pagination>
            </div>
        </div>
    </div>
</template>
<script>
import { get_project_info, get_quotation_list, getUserRolePL } from '@/api/content_api'
export default {
    data() {
        return {
            pro_id: '',
            userId: null,
            data_json: [],
            quotations_list: [],
            Sales_SGL: false,
            Sales: false,
            check_workers_flag: false,
            SALES: false,
            SGL: false,
            GL: false,
            total: 0,
            page: 1,
            size: 10,
            show_edit_flag: false
        }
    },
    mounted() {
        this.pro_id = this.$route.params.pro_id
        this.userId = this.$cookies.get('userId')
        this.get_data()
        this.get_quotation_list_data()
        let cookie = this.$cookies.get('role')

        this.SALES = false;
        this.SGL = false;
        this.GL = false;
        if (cookie.indexOf('SALES') > -1) {
            this.SALES = true;
        } else if (cookie.indexOf('SGL') > -1) {
            this.SGL = true
        } else {
            this.GL = true;
        }
    },
    watch: {
        $route(to, from) {
            this.pro_id = this.$route.params.pro_id
        }
    },
    methods: {
        get_data() {
            get_project_info(this.pro_id).then(res => {
                if (res.data.result == 'OK') {
                    // console.log(res.data.content, 'data_json');
                    this.data_json = res.data.content
                } else {
                    this.$message({
                        type: 'error',
                        message: res.data.content,
                        duration: 0,
                        showClose: true
                    })
                }
            })
            getUserRolePL(this.userId,this.pro_id ).then(res => {
                // console.log(res,'---------');
                let data = res.data.content
                // let cookie = this.$cookies.get('role')
                // let temp = cookie.split(',')
                this.show_edit_flag = data.some(role => {
                    return role == 'SALES' || role == 'SuperPL'
                })
                // console.log(temp,'temp',this.show_edit_flag);


            })
        },
        get_quotation_list_data() {
            get_quotation_list(this.pro_id, this.userId, this.page, this.size).then(res => {
                if (res.data.result == 'OK') {
                    // console.log(res.data, '==============');
                    this.total = res.data.content.count
                    this.quotations_list = res.data.content.quotation_list.map(item => {
                        if (item.status == '新建') {
                            item.check_workers_flag = true
                            return item
                        } else {
                            item.check_workers_flag = false
                            return item
                        }
                    })
                    
                } else {
                    this.$message({
                        type: 'error',
                        message: '服务器异常！'
                    })
                }
                this.loading = false
            })
        },
        push_quotation() {
            this.$router.push({ path: '/proj/quotation/' + this.pro_id })
        },
        input_list_fun() {
            this.$router.push({ path: '/Input/InputList', query: { proj_id: this.pro_id } })
        },
        look_quotation_fun(id) {
            this.$router.push({ path: '/featurePage/FeatureList', query: { quotation_id: id, proj_id: this.pro_id } })
        },
        cancel_fun() {
            if (sessionStorage.getItem('page_index') == 3) {
                this.$router.push('/proj/projQuoteList')
            }else{
                this.$router.push('/allProject')
            }
        },
        push_system_table() {
            this.$router.push({ path: '/system_table/system_table_view/' + this.pro_id })
        },
        look_quotation_pie(quotation_id) {
            this.$router.push({ path: '/proj/quotation_pie/' + quotation_id + '/' + this.pro_id })
        },
        goSummaryAccount(quotationId) {
            let routeData = this.$router.resolve({
                name: 'summaryAccount',
                query: { quotation_id: quotationId }
            })
            window.open(routeData.href, '_blank')
        },
        assignHourMan(projId, quoteId) {
            this.$router.push({ path: '/featurePage/FeatureList', query: { 'quotation_id': quoteId, 'proj_id': projId } })
        },
        current_change(val) {
            this.page = val
            const userId = this.$cookies.get('userId')
            this.loading = true
            this.get_quotation_list_data()
        },
        editProj() {
            this.$router.push({ path: '/proj/add_project/' + this.pro_id })
        },
    }
}
</script>
<style scoped lang='less'>
ul,
li {
    list-style: none;
}
.warpper {
    height:calc(100%);
    width: 1280px;
    margin: 0 auto;
    background: #fff;

    .pro-content {
        height: 100%;
        overflow-y: auto;
    }
    .detail-box {
        // height: 40px;
        // line-height: 40px;
        // margin:20px 0 0 20px;
        width: 100%;
        overflow: hidden;
        margin: 15px 0;
    }
    .detail-box span,
    .describe-box p {
        color: #5e6d82;
        // font-size: 14px;
        margin-right: 20px;
        font-weight: bold;
        display: block;
        float: left;
        width: 120px;
    }

    .pro-nav {
        width: 95%;
        height: 40px;
        line-height: 40px;
        padding-top: 20px;
        list-style: none;
        margin-left: 20px;
    }
    .pro-nav li {
        float: right;
        margin: 0 10px;
    }
    .msg-box {
        margin-top: 20px;
        margin-left: 20px;
    }
}
</style>
