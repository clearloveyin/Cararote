const user = {
    state: {
        userName: '',
        userId: '',
        token: '',
        roles: []
    },
    mutation: {
        SET_USER_NAME: (state, userName) => {
            state.userName = userName
        },   
        SET_USER_ID: (state, userId) => {
            state.userId = userId
        },
        SET_TOKEN: (state, token) => {
            state.token = token
        },

        SET_ROLES: (state, roles) => {
            state.roles = roles
        }
    },
    actions: {
        setUserName({ commit, userName}) {
            commit('SET_USER_NAME', userName)
        },
        setUserId({ commit, userId}) {
            commit('SET_USER_ID', userId)
        },
        setToken({ commit, token}) {
            commit('SET_TOKEN', token)
        },
        setRoles({ commit, roles}) {
            commit('SET_ROLES', roles)
        }
    }
}

export default user