'use strict'
import axios from 'axios'
import store from '@/store/store'
import { Message, Progress } from 'element-ui'
import router from '@/router/router'
import IP from '@/api/ipAddress'
// axios.defaults.baseURL = process.env.baseURL || process.env.apiUrl || '';
// axios.defaults.headers.common['Authorization'] = AUTH_TOKEN;
// axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
let config = {
    //   baseURL: process.env.baseURL || process.env.apiUrl || "",
    baseURL: IP,
    timeout: 60 * 1000, // Timeout
    withCredentials: false, // Check cross-site Access-Control
    headers: { 'X-Requested-With': 'XMLHttpRequest' },
    url: '/user',
    method: 'get',
    responseType: 'json',
    transformRequest: [function (data, headers) {
        // `transformRequest`允许在请求数据发送到服务器之前对其进行更改
        // 这只适用于请求方法'PUT'，'POST'和'PATCH'
        // 数组中的最后一个函数必须返回一个字符串，一个 ArrayBuffer或一个 Stream
        // 做任何你想要的数据转换
        // console.log('form:', data, headers)
        return JSON.stringify(data)
    }],
    transformResponse: [function (data) {
        // Do whatever you want to transform the data
        return data
    }],
    // `onUploadProgress` allows handling of progress events for uploads
    onUploadProgress: function (progressEvent) {
        // Do whatever you want with the native progress event
    },
    // `onDownloadProgress` allows handling of progress events for downloads
    onDownloadProgress: function (progressEvent) {
        // Do whatever you want with the native progress event
    },
    validateStatus: function (status) {
        return status >= 200 && status < 300 // default
    }
    // `cancelToken` specifies a cancel token that can be used to cancel the request
    // (see Cancellation section below for details)
    // cancelToken: new CancelToken(function (cancel) {
    // })
}
const server = axios.create(config)
server.interceptors.request.use(
     config => {
        // Do something before request is sent
        // var token = $cookies.get('token')
        // config.headers.Authorization = 'Token ' + token;
        // to do :mainjs中store读取token,此处更新token
        // const token = store.state.token;
        // token && (config.headers.Authorization = token);
        return config
    },
    error => {
        // Do something with request error
        // Message.error({ message: '请求超时!' });
        return Promise.reject(error)
    }
)

// Add a response interceptor
server.interceptors.response.use(
    response => {
        // Do something with response data
        console.log(response, '---------')
        if (response.data.code === 200) {
            // Message.error({ message: response.data.message })
            return response
        } else if (response.data.code === 201) {
            Message.error({ message: response.data.message })
            return Promise.reject(response)
        } else if (response.data.code === 202) {
            Message.error({ message: response.data.message })
            return Promise.reject(response)
        } else if (response.data.code === 203) {
            Message.error({ message: response.data.message })
            return Promise.reject(response)
        } else if (response.data.code === 204) {
            Message.error({ message: response.data.message })
            return Promise.reject(response)
        } else {
            Message.error({ message: response + '超出定义错误范围' })
            return Promise.reject(response)
        }
    },
    error => {
        // Do something with response error
        Message.error({ message: error, showClose: true })
        if (error) {
            router.replace({ path: '/' })
        }
        return Promise.reject(error)
    }
)

// function getProcessEnv (env){
// console.log('env:', env);
// 环境的切换
// if (env.NODE_ENV == 'development') {
//     axios.defaults.baseURL = 'https://www.baidu.com';
// }
// else if (env.NODE_ENV == 'test') {
//     axios.defaults.baseURL = 'https://www.ceshi.com';
// }
// else if (env.NODE_ENV == 'production') {
//     axios.defaults.baseURL = 'https://www.production.com';
// }
// }
// Full config:  https://github.com/axios/axios#request-config
// axios.defaults.baseURL = process.env.baseURL || process.env.apiUrl || '';
// axios.defaults.headers.common['Authorization'] = AUTH_TOKEN;
// axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'

export default server
