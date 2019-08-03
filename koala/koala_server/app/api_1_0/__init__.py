# -*- coding: UTF-8 -*-
from app.api_1_0.login import Login, Root
from app.api_1_0.api_project import *
from app.api_1_0.api_quotations import *
from app.api_1_0.api_resources import ApiInputUpload, ApiInputInfo
from app.api_1_0.api_resources import ApiInputDel
from app.api_1_0.api_down_up import DownFile
from app.api_1_0.api_user_group import ApiAllUser, ApiProjectGroups, ApiAllGroup
from app.api_1_0.api_user_group import ApiGroupsToTask
from app.api_1_0.api_user_group import ApiManagerGroup, ApiManagerMemeber
from app.api_1_0.api_task import ApiTask, ApiCheckTaskDelete
from app.api_1_0.api_issue import ApiIssueList, ApiReplayList
from app.api_1_0.api_cost import ApiCost, ApiTaskCostHistiry, ApiCostSummary, ExportSummary, ApiDownLoad
from app.api_1_0.api_cost import ApiCostDetail
from app.api_1_0.api_user_role import ApiUserRole, ApiProjUserRole


class Api_1_0():
    def __init__(self, api):
        # Home
        api.add_resource(Root, '/')
        # 登录
        api.add_resource(Login, '/login')
        # 项目管理
        api.add_resource(ApiProjectState, '/ProjectState')
        api.add_resource(ApiProjectInside, '/ProjectInside')
        api.add_resource(ApiProjectType, '/ProjectType')
        api.add_resource(ApiProjectNameCheck, '/Project/check/name')  # 获取当前已选择过的内部名称
        api.add_resource(ApiProjectList,
                         '/Project/List',                   # 获取项目列表所有
                         '/Project/List/<int:user_id>',     # 获取某人的项目列表
                         '/Project/add')                    # 添加项目
        api.add_resource(ApiProjectInfo,
                         '/Project/show/<int:pro_id>',      # 获取单个项目信息
                         '/Project/update/<int:pro_id>',    # 修改单个项目信息
                         '/Project/del')                    # 删除单个项目
        api.add_resource(ApiProjectManager,

                         '/manager/show/<int:proj_id>/<int:user_id>',
                         )
        api.add_resource(ApiManageList,
                         '/manager/list',                   # 项目ID和项目-体制表获取
                         )
        api.add_resource(ApiManagerImport,
                         '/manager/import')                 # 导入项目体制信息
        api.add_resource(ApiManagerGroup,
                         '/manager/group/update',
                         '/manager/group/delete/<int:proj_id>/<int:group_id>/<int:commit_user>'
                         )
        # api.add_resource(ApiManagerMemeber,
        #                  '/manager/member/update',
        #                  '/manager/member/delete/<int:proj_id>/<int:group_id>/<int:user_id>/<int:commit_user>'
        #                  )
        # 人员组别管理
        api.add_resource(ApiAllUser,
                         '/user/show'
                         )
        api.add_resource(ApiProjUserRole,
                         '/role/list/<int:user_id>/<int:proj_id>',  # 获取某人在该项目下的角色
                         '/role/list/<int:user_id>'  # 获取某人的所有角色
                         )
        api.add_resource(ApiAllGroup,
                         '/group/show')
        api.add_resource(ApiProjectGroups,
                         '/project/group/list/<int:proj_id>'
                         )
        api.add_resource(ApiGroupsToTask,
                         '/task/group/assign/<int:proj_id>')
        # Input资料管理
        api.add_resource(ApiInputUpload,
                         '/GetQuotationInput/<int:quotation_id>',                    # 获取某报价下资料列表
                         '/InputUpload')                                             # 上传资料到项目下
        api.add_resource(ApiInputInfo,
                         '/GetInputInfo/<int:proj_id>/<_type>'                       # 获取项目下某类型资料
                         )
        api.add_resource(ApiInputDel, '/DelInputInfo')  # （设置status）删除子表，没有子表则删除父表
        # api.add_resource(ApiInputInfo, '/GetInputInfo/<int:proj_id>/<string:_type>') # 获取某报价下资料列表
        # 工数
        api.add_resource(ApiCost,
                         '/cost/show/<int:quotation_id>/<int:user_id>',  # 取机能工数数据
                         '/cost/show/myself/<int:quotation_id>/<int:user_id>/<myself>',  # 取我的工数数据
                         '/cost/update')
        api.add_resource(ApiCostSummary,
                         '/cost/summary/<int:quotation_id>/<int:user_id>')
        api.add_resource(ApiCostDetail, '/cost/detail/<int:func_id>')
        # 报价管理
        api.add_resource(ApiQuotationInfo,
                         '/BaseQuotation/List/<int:pro_id>',                          # 获取项目下base报价列表
                         '/Quotation/List',                                           # 获取所有报价列表
                         '/Quotation/List/<int:page>/<int:size>',                     # 获取所有报价列表(分页)
                         '/Quotation/add',)                                           # 新增项目下报价
        api.add_resource(ApiQuotationStatue,
                         '/QuotationStatue/show/<int:quotation_id>',                  # 获取单个报价状态
                         '/QuotationStatue/update', )                                 # 修改单个报价状态
        api.add_resource(ApiQuotations,
                         '/Quotation/show/<int:quotation_id>',                        # 获取单个报价详细
                         '/Quotation/update/<int:quotation_id>'                       # 修改单个报价
                         )
        api.add_resource(ApiQuotationList,
                         # '/Quotation/List/proj/<int:pro_id>/<int:user_id>',           # 项目下报价对比列表
                         # '/Quotation/List/user/<int:user_id>',                        # 某人名下报价对比列表
                         '/Quotation/List/proj/<int:pro_id>/<int:user_id>/<int:page>/<int:size>',# 项目下报价对比列表(分页)
                         '/Quotation/List/user/<int:user_id>/<int:page>/<int:size>',   # 某人名下报价对比列表(分页)
                         )
        api.add_resource(ApiQuotationPie,
                         '/Quotation/Pie/<int:quotation_id>'                          # 报价饼图
                         )
        # Option管理
        # api.add_resource(ApiOptionInfo,
        #                  '/Option/list/<int:quotation_id>',                  # 获取单个报价下options
        #                  '/Option/update/<int:quotation_id>'                 # 修改/新增 options及options下的optionvalue
        #                  )
        # api.add_resource(ApiOptionValueInfo,
        #                  '/OptionValue/show/<int:option_id>',              # 获取单个options下的optionvalue
        #                  '/OptionValue/update/<int:option_id>'             # 修改/新增 optionvalue
        #                  )
        api.add_resource(ApiOptionCombinationInfo,
                         '/OptionCombination/list/<int:quotation_id>',       # 获取单个quotation下的Combination
                         '/OptionCombination/update/<int:quotation_id>',      # 修改/新增 Combination
                         '/OptionCombination/delete/<int:op_id>'              # 删除 Combination
                         )
        # # Feature
        api.add_resource(ApiFeatureImport,
                         '/feature/import',                                  # 上传 FeatureList 文件
                         )
        api.add_resource(ApiFeatureInfo,
                         '/feature/list/<int:quotation_id>/<int:user_id>',   # 获取单个报价下 FeatureList
                         '/feature/update/<int:quotation_id>'                # 更新 FeatureList
                         )
        api.add_resource(ApiFeatureAssign,
                         '/feature/history/<int:quotation_id>',              # 获取 FeatureList 历史
                         '/feature/assign/<int:quotation_id>'                # 分配 FeatureList
                         )

        # 指摘管理
        api.add_resource(ApiIssueList,
                         '/GetIssueList',  # 获取指摘列表
                         '/issue/cost/list/<int:base_id>',  # 获取某条工数的指摘
                         '/issue/add', )  # 添加指摘
        api.add_resource(ApiReplayList,
                         '/GetReplayList',  # 获取回复列表
                         '/AddReplayIssue')  # 添加回复

        # Task
        api.add_resource(ApiTask, '/task/update',
                         '/task/list/<quotation_id>'
                         )
        api.add_resource(ApiCheckTaskDelete,
                         '/task/delete/check/<int:quotation_id>/<int:commit_user>/<int:task_id>')
        api.add_resource(ApiTaskCostHistiry, '/task/history/<int:task_id>',)
        # 上传下载
        api.add_resource(DownFile, '/DownFile', '/DownFile/<path:path_info>')

        # @Hongcz: 临时测试使用
        # from app.api_1_0.api_test import ApiTestDsQuotation, ApiTestSumFunction
        # api.add_resource(ApiTestDsQuotation, '/test/ds/quotation/<int:quotation_id>')
        # api.add_resource(ApiTestSumFunction, '/test/summary/quotation/<int:group_id>/<int:quotation_id>')

        # ExportSummary
        api.add_resource(ExportSummary, '/exportsummary/<int:user_id>/<int:quotation_id>/<string:unit>')
        api.add_resource(ApiDownLoad, '/download/<path:path>')

        # pl角色管理
        api.add_resource(ApiUserRole, '/pl/user/show',
                         '/pl/user/update')


