import request from '@/axios_config/request'

// input
export function new_add_input(data) {
    return request({
        url: '/InputUpload',
        method: 'post',
        data
    })
}

export function delete_input(data) {
    return request({
        url: '/DelInputInfo',
        method: 'post',
        data
    })
}

export function get_input_info(project_id, type) {
    return request({
        url: '/GetInputInfo/' + project_id + "/" + type,
        method: 'get'
    })
}

export function get_project_list() {
    return request({
        url: '/Project/List',
        method: 'get'
    })
}

export function get_project_info(project_id) {
    return request({
        url: '/Project/show/' + project_id,
        method: 'get'
    })
}
export function get_project_type() {
    return request({
        url: '/ProjectType',
        method: 'get'
    })
}

export function get_project_inside() {
    return request({
        url: '/ProjectInside',
        method: 'get'
    })
}

export function add_project(data) {
    return request({
        url: '/Project/add',
        method: 'post',
        data
    })
}
export function change_project(project_id, data) {
    return request({
        url: '/Project/update/' + project_id,
        method: 'put',
        data
    })
}
// 获取BaseQuotationList
export function get_quotation_data(pro_id) {
    return request({
        url: '/BaseQuotation/List/' + pro_id,
        method: 'get',
    })
}


// 提交QuotationList
export function add_quotation_data(data) {
    return request({
        url: '/Quotation/add',
        method: 'post',
        data
    })
}

// 报价查看
export function get_quotation_input(daquotation_id) {
    return request({
        url: '/GetQuotationInput/' + daquotation_id,
        method: 'get',
    })
}

// 单个报价查看
export function get_quotation_one(quotation_id) {
    return request({
        url: '/Quotation/show/' + quotation_id,
        method: 'get',
    })
}
// 获取单个报价状态
export function get_quotation_status(quotation_id){
    return request({
        url: '/QuotationStatue/show/' + quotation_id,
        method: 'get',
    })
}
export function update_quotation_status(data) {
    return request({
        url: '/QuotationStatue/update',
        method: 'post',
        data:data
    })
}

// 获取项目体制接口
export function get_manager_show(proj_id, user_id) {
    return request({
        url: '/manager/show/' + proj_id + '/' + user_id,
        method: 'get',
    })
}

//获取全体人员名单接口
export function get_user_data() {
    return request({
        url: '/user/show',
        method: 'get'
    })
}
// 项目体制组更新
export function post_manager_group(data) {
    return request({
        url: '/manager/group/update',
        method: 'post',
        data
    })
}
// 项目体制删除组
export function delete_manager_group(proj_id, group_id, user_id) {
    return request({
        url: '/manager/group/delete/' + proj_id + '/' + group_id + '/' + user_id,
        method: 'delete',
    })
}
// 报价对比
export function get_quotation_list(projId, userId,page,size) {
    return request({
        url: `/Quotation/List/proj/${projId}/${userId}/${page}/${size}`,
        method: 'get'
    })
} 
// 单次报价构成图
export function get_quotation_pie(proj_id) {
    return request({
        url:'/Quotation/Pie/' + proj_id,
        method:'get'
    })
} 
// feature列表接口
export function get_feature_list(daquotation_id,user_id) {
    return request({
        url: '/feature/list/' + daquotation_id + '/' + user_id,
        method: 'get',
    })
}
// feature列表分配组接口
export function feature_list_assign(data,quotation_id) {
    return request({
        url: '/feature/assign/'+ quotation_id,
        method: 'post',
        data
    })
}
// task列表接口
export function get_task_list(quotation_id) {
    return request({
        url: '/task/list/' + quotation_id,
        method: 'get',
    })
}
// 获取项目组列表接口
export function get_project_group_list(project_id) {
    return request({
        url: '/task/group/assign/'+ project_id,
        method: 'get',
    })
}
// 获取项目组列表接口
export function get_project_group_list_children(project_id) {
    return request({
        url: '/project/group/list/'+ project_id,
        method: 'get',
    })
}
// task更新接口
export function task_list_update(data) {
    return request({
        url: '/task/update',
        method: 'post',
        data
    })
}

export function getProjList(userId) { // 获得报价列表
    return request({
        url: `/Project/List/${userId}`,
        method: 'get'
    })
}
export function getAllList() { // 获得报价列表
    return request({
        url: `/Project/List`,
        method: 'get'
    })
}

export function getQuoteList(userId,page,size) { // 获得报价列表
    return request({
        url: '/Quotation/List/user/' + userId+'/'+ page + "/" + size,
        method: 'get'
    })
}  
export function getAllQuoteList( page, size) { // 获得报价列表
    return request({
        url: '/Quotation/List/' + page + "/" + size,
        method: 'get'
    })
}  

export function getAllUser() { // 获得报价列表
    return request({
        url: '/user/show',
        method: 'get'
    })
}
export function addPL(user) { // 获得报价列表
    return request({
        url: '/user/show',
        method: 'post'
    })
}   

export function getPL() { // 获得报价列表
    return request({
        url: '/pl/user/show',
        method: 'get'
    })
} 

 // 获得报价列表
export function get_manager_list() {
    return request({
        url: '/manager/list',
        method: 'get'
    })
}    

// 获取删除权限
export function get_user_delete_manage(quotation_id,commit_user,task_id) {
    return request({
        url: '/task/delete/check/' + quotation_id +'/' + commit_user + '/'+ task_id,
        method: 'get'
    })
}

// 检查项目内部名称是否重复
export function get_project_check() {
    return request({
        url: '/Project/check/name',
        method: 'get'
    })
}  
// 体制表添加组 可搜索
export function get_group_show() {
    return request({
        url: '/group/show',
        method: 'get'
    })
}  

// 获取单个报价下options
export function get_options_list(quotation_id) {
    return request({
      url:'/Option/list/' + quotation_id,
      method:'get'
    })
}

// 修改/新增 options及options下的optionvalue
export function update_options_list(quotation_id,data) {
    return request({
      url:'/Option/update/' + quotation_id,
      method:'post',
      data
    })
}

// 获取单个quotation下的Combination
export function get_OptionCombination_list(quotation_id) {
    return request({
      url:'/OptionCombination/list/' + quotation_id,
      method:'get'
    })
}

// 修改/新增 Combination
export function update_OptionCombination_list(data,quotation_id) {
    return request({
      url:'/OptionCombination/update/' + quotation_id,
      method:'post',
      data
    })
}

//删除
export function delete_OptionCombination_list(quotation_id) {
    return request({
        url: '/OptionCombination/delete/' + quotation_id,
        method: 'delete',
    
    })
}

export function getUserRolePL(userId,projId,) {
    return request({
        url: '/role/list/' + userId + '/' + projId,
        method: 'get',

    })
}

export function getUserRolePL_2(userId) {
    return request({
        url: '/role/list/' + userId,
        method: 'get',
    })
}

export function updateUserPL(data) {
    return request({
        url: '/pl/user/update',
        method: 'post',
        data
    })
}