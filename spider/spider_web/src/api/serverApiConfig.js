
// 统一定义接口，有利于维护
import IP from '@/api/ipAddress'
const URL = {
    // 登录接口
    login: IP + '/login',
    projectAdd: IP + '/project/add', // 添加
    projectEdit: IP + '/project/edit/', // 编辑
    projectDelete: IP + '/project/delete/', // 删除
    project: IP + '/project/', // 获取单个项目的信息
    projectList: IP + '/project/list/', // 获取项目列表
    carList: IP + '/car/dest/', // 获取仕向地和车种
    carEdit: IP + '/car/dest/', // 编辑仕向地和车种
    rfq: IP + '/rfq/', // 获取RFQ详细信息。
    rfqAdd: IP + '/rfq/add/', // 添加
    rfqEdit: IP + '/rfq/edit/', // 编辑
    rfqDelete: IP + '/rfq/delete/',
    feature: IP + '/feature/list/',
    featureMaster: IP + '/feature/list/master',
    featureEdit: IP + '/feature/list/', // 编辑
    featureRfq: IP + '/feature/rfq/',
    featureAssign: IP + '/feature/func/assign',
    featureExpand: IP + '/feature/expand/apply/',
    featureIssue: IP + '/feature/issue/',
    featureMergeExpand: IP + '/feature/merge/expand',
    featureDiff: IP + '/feature/diff/',
    permission: IP + '/permission',
    rolePermission: IP + '/role/permission/',
    rolePermissionEdit: IP + '/role/permission/',
    catalogList: IP + '/catalog/list/',
    catalog: IP + '/catalog/',
    catalogAdd: IP + '/catalog/add/',
    catalogEdit: IP + '/catalog/edit/',
    catalogDiff: IP + '/catalog/diff/',
    catalogReview: IP + '/catalog/review/',
    catalogFeatureConfirm: IP + '/catalog/feature/confirm/',
    catalogMergeExpand: IP + '/catalog/merge/expand/',
    funcList: IP + '/func/list/',
    funcFeatureConfirm: IP + '/func/feature/confirm/',
    func: IP + '/func/',
    funcMergeExpand: IP + '/func/merge/expand/',
    exportFeature: IP + '/export/feature/',
    exportFuncSpec: IP + '/export/funcspec/'
}

export default URL
