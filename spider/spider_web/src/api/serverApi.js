import server from '@/plugins/axios'
import URL from '@/api/serverApiConfig'
export function login (user) {
    return server({
        url: URL.login,
        method: 'post',
        data: user
    })
}
