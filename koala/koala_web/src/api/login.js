import request from '@/axios_config/request'
export function login(data) {
    return request({
        url: '/login',
        method: 'post',
        data
    })
}

// export function get_data(pro_id){
// 	return request({
// 	    url: '/GetBaseQuotationList/' + pro_id,
// 	    method: 'get',
// 	})
// }