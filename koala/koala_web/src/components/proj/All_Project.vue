<template>
    <div class="proj-quote-list" >
        <div class="container" >
            <el-collapse v-model="activeNames" @change="handleChange" >
                <el-collapse-item title="项目列表" name="project">
                    <template slot="title">
                        <!-- <i class="el-icon-info" style="padding-left: 50px;"></i> -->
                        <h2 >项目列表
                            <i class="el-icon-plus"  @click="addProject()" style="padding-left: 10px;" ></i>&nbsp;

                            <i :class="projRefreshIcon" @click.stop="refresh('proj')"></i>
                        </h2>
                    </template>
                    <div class="table-wrapper"> 
                        <div class="table-flex">
                            <el-table :data="projList" style="width: 100%;" :row-class-name="tableRowClassName" size="medium">
                                <el-table-column prop="inside_name" label="项目名" width="180">
                                    <template slot-scope="scope">
                                        <span class="link-type" @click="goProjDetail(scope.row)">{{scope.row.inside_name}}</span>
                                    </template>
                                </el-table-column>

                                <el-table-column prop="proj_type" label="系列名" width="180">
                                </el-table-column>
                                <el-table-column prop="describe" label="描述">
                                </el-table-column>
                                <el-table-column align="center" prop="update_time" label="日期" width="180">
                                </el-table-column>
                                
                            </el-table>
                        </div>
                    </div>
                </el-collapse-item>
                <el-collapse-item title="报价列表" name="quote" v-loading="loading2">
                    <template slot="title">
                        <!-- <i class="el-icon-info" style="padding-left: 50px;"></i> -->
                        <h2>报价列表
                            <!-- <i class="el-icon-plus" style="padding-left: 10px;"></i>&nbsp; -->
                            <i :class="quoteRefreshIcon" @click.stop="refresh('quote')"></i>
                        </h2>
                    </template>
                    <div class="table-wrapper">
                        <div class="table-flex">
                            <el-table :data="quoteList" style="width: 100%;" :row-class-name="tableRowClassName" size="medium">
                                <el-table-column prop="quotation_name" label="报价名称" width="180">
                                </el-table-column>

                                <el-table-column prop="proj_name" label="项目名称" width="100">
                                </el-table-column>
                                <el-table-column prop="quotation_ver" label="报价版本" width="80">
                                </el-table-column>
                                <el-table-column prop="status.status_cn" label="报价状态" width="100">

                                </el-table-column>
                                <el-table-column prop="destribe" label="描述">
                                </el-table-column>
                                <el-table-column prop="count_issue" label="指摘" width="80">
                                </el-table-column>
                                <el-table-column align="center" prop="update_time" label="日期" width="180">
                                </el-table-column>
                                <template v-if="SALES || SGL">
                                    <el-table-column align="center" prop="count_not_assign" label="待分配数" width="80">
                                        <template slot-scope="scope">
                                            <el-button v-if="scope.row.check_status_flag" :disabled="!scope.row.checkout_flag" type='text' @click="assignHourMan(scope.row.proj_id, scope.row.quotation_id)">{{scope.row.count_not_assign}}</el-button>
                                            <el-button v-else type='text' @click="assignHourMan(scope.row.proj_id, scope.row.quotation_id)">{{scope.row.count_not_assign}}</el-button>

                                        </template>
                                    </el-table-column>
                                </template>
                                <template v-if="SGL">
                                    <el-table-column align="center" prop="count_not_confirm" label="待确认数" width="80">
                                        <template slot-scope="scope">
                                            <el-button  v-if="scope.row.check_status_flag" type='text' :disabled="!scope.row.checkout_flag">{{scope.row.count_not_confirm}}</el-button>
                                            <a v-else  :href="'cell.html?quotationId=' + scope.row.quotation_id + '&projId=' + scope.row.proj_id" target="_blank" rel="noopener noreferrer">
                                                <el-button type='text' >{{scope.row.count_not_confirm}}</el-button>
                                            </a>
                                        </template>
                                    </el-table-column>
                                </template>
                                <template v-if="GL">
                                    <el-table-column align="center" prop="count_not_quotation" label="待报价数" width="80">
                                        <template slot-scope="scope">
                                            <el-button  v-if="scope.row.check_status_flag" type='text' :disabled="!scope.row.checkout_flag">{{scope.row.count_not_quotation}}</el-button>
                                            <a v-else :href="'cell.html?quotationId=' + scope.row.quotation_id + '&projId=' + scope.row.proj_id" target="_blank" rel="noopener noreferrer">
                                                <el-button type='text'>{{scope.row.count_not_quotation}}</el-button>
                                            </a>
                                        </template>
                                    </el-table-column>
                                </template>
                                <template v-if="SALES">
                                    <el-table-column align="center" prop="" label="工数填写" width="80">
                                        <template slot-scope="scope">
                                            <a  :href="'cell.html?quotationId=' + scope.row.quotation_id + '&projId=' + scope.row.proj_id" target="_blank" rel="noopener noreferrer">
                                                <el-button type='text'>工数填写</el-button>
                                            </a>
                                        </template>
                                    </el-table-column>
                                </template>
                                <template v-if="SALES">
                                    <el-table-column align="center" prop="count_not_admit" label="工数汇总" width="100">
                                        <template slot-scope="scope">
                                            <el-button type='text' @click='goSummaryAccount(scope.row.quotation_id)'>工数汇总</el-button>
                                        </template>
                                    </el-table-column>
                                </template>
                               
                                
                            </el-table>
                            <el-pagination small layout="prev, pager, next" :total="total" @current-change="current_change" v-if="total!=0"> </el-pagination>
                        </div>
                    </div>
                </el-collapse-item>
            </el-collapse>
        </div>
    </div>
</template>
<script>
import { getAllList, getAllQuoteList } from '@/api/content_api'
// import IP from '../../../static/config'
export default {
    name: 'proj_quote_list',
    data() {
        return {
            SALES: false,
            SGL: false,
            GL: false,
            activeNames: ['project', 'quote'],
            projRefreshIcon: 'el-icon-refresh', //el-icon-loading
            quoteRefreshIcon: 'el-icon-refresh', //el-icon-loading
            projList: [],
            quoteList: [],
            loading:false,
            total:0,
            page:1,
            size:10,
            loading2:false
        }
    },
    mounted() {
        let cookie = this.$cookies.get('role')
        this.SALES = false;
        this.SGL = false;
        this.GL = false;
        if (cookie.indexOf('SALES') > -1){
            this.SALES = true;
        }else if (cookie.indexOf('SGL') > -1){
            this.SGL = true
        }else{
            this.GL = true;
        }
        this.reqProjQuote()
        
    },
    methods: {
        reqProjQuote() {
            this.loading = true
            const userId = this.$cookies.get('userId')
            const getProjListPromise = new Promise((resolve, reject) => {
                getAllList().then(project_list_data => {
                    if (project_list_data.data.result == 'NG') {
                        throw new Error(res.data.error+'NG')
                    }
                    this.projList = project_list_data.data.content
                    resolve()
                })
            })
            const getQuotationPromise = new Promise((resolve, reject) => {
                getAllQuoteList(this.page,this.size).then(quotation_list_data => {
                    console.log(quotation_list_data,'quotation_list_data')
                    if (quotation_list_data.data.result == 'NG') {
                        throw new Error(res.data.error+'NG')                    
                    }
                    this.quoteList = quotation_list_data.data.content.quotation_list
                    this.total = quotation_list_data.data.content.count
                    let leng = this.quoteList.length
                    for (let i = 0; i < leng; i++) {
                        this.quoteList[i].check_status_flag = false
                        if (this.quoteList[i].status.status_cn == "新建" ) {
                            if (this.$cookies.get("role").indexOf("SALES")==-1) {
                                this.quoteList[i].check_status_flag = true //如果是新建状态，并且当前登录人不是SALES的话，禁止点击
                            }else{
                                this.quoteList[i].check_status_flag = false
                            }
                        }
                    }
                    resolve()
                })
            })

            Promise.all([getProjListPromise, getQuotationPromise]).then(() => {
                this.loading = false
            })

        },
        get_quotation_fun(userId,page,size){
            getAllQuoteList(page,size).then(quotation_list_data => {
                    if (quotation_list_data.data.result == 'NG') {
                        throw new Error(res.data.error+'NG')                    
                    }
                    this.quoteList = quotation_list_data.data.content.quotation_list
                    this.total = quotation_list_data.data.content.count
                    let leng = this.quoteList.length
                    for (let i = 0; i < leng; i++) {
                        this.quoteList[i].check_status_flag = false
                        if (this.quoteList[i].status.status_cn == "新建" ) {
                            if (this.$cookies.get("role").indexOf("SALES")==-1) {
                                this.quoteList[i].check_status_flag = true //如果是新建状态，并且当前登录人不是SALES的话，禁止点击
                            }else{
                                this.quoteList[i].check_status_flag = false
                            }
                        }
                    }
                    this.loading2 = false
                })
        },
        reqProjList() {
            this.projRefreshIcon = 'el-icon-loading'
            const userId = this.$cookies.get('userId')
            getProjList(userId).then(res => {
                this.projList = res.data.content
                this.projRefreshIcon = 'el-icon-refresh'
            })
        },
        reqQuoteList() {
            this.quoteRefreshIcon = 'el-icon-loading'
            const userId = this.$cookies.get('userId')
            this.loading2 = true
            getAllQuoteList(this.page,this.size).then(res => {
                this.quoteList = res.data.content.quotation_list
                this.total = res.data.content.count
                this.loading2 = false
                this.quoteRefreshIcon = 'el-icon-refresh'
            })
        },
        handleChange(val) {
        },
        refresh(type) {
            if (type == 'proj') {
                this.reqProjList()
            } else {
                this.reqQuoteList()
            }
        },
        tableRowClassName({ row, rowIndex }) {
            
            return 'row-type'
        },
        goProjDetail(row) {
            this.$router.push({ path: '/proj/pro_detail/' + row.proj_id })
        },
        editProj(row) {
            this.$router.push({ path: '/proj/add_project/' + row.proj_id })
        },
        
        goSummaryAccount(quotationId) {
            let routeData = this.$router.resolve({
                name: 'summaryAccount',
                query: { quotation_id: quotationId }
            })
            window.open(routeData.href, '_blank')
        },
        addProject() {
            this.$router.push('/proj/add_project_c')
        },
        assignHourMan(projId, quoteId) {
		    this.$router.push({path:'/featurePage/FeatureList',query:{'quotation_id':quoteId,'proj_id':projId}})
        },
        current_change(val){
            const userId = this.$cookies.get('userId')
            this.page = val
            this.loading2 = true
            this.get_quotation_fun(userId,this.page,this.size)
        }
    }
}
</script>
<style scoped>
.proj-quote-list {
  /* width: 100%; */
  height: 100%;
  overflow-x: hidden;
  /* background: #f0f0f0; */
  overflow-y: scroll;

}
.container {
  width: 1280px;
  height: 100%;
  margin-left: auto;
  margin-right: auto;
  background: #fff;
}

i {
  cursor: pointer;
}
.link-type:hover {
  color: #337ab7;
  cursor: pointer;
}
.link-type {
  font-weight: bold;
  color: rgb(32, 160, 255);
}
.proj-tag {
  color: #ffffff;
  border-radius: 2px;
  box-shadow: inset 0 -1px 0 rgba(27, 31, 35, 0.12);
  font-size: 12px;
  font-weight: 600;
  height: 20px;
  line-height: 15px;
  padding: 0.15em 4px;
  text-decoration: none;
}
.proj-tag-unreviewed {
  background-color: #7057ff;
}

.proj-tag-submitted {
  background-color: #008672;
}

.proj-tag-point {
  background-color: #d73a4a;
}
.proj-tag-span {
  position: relative;
  line-height: 1.5 !important;
}
h2 {
  padding-left: 20px;
}
.table-wrapper {
  display: flex;
  position: relative;
}
.table-flex {
  flex: 1;
  overflow-x: hidden;
  padding-left: 20px;
}
@media screen and (max-width: 1280px) {
  .container {
    width: 100%;
  }
}
</style>