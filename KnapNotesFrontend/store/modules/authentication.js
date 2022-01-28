const state = (() => {})()
const getters = {}
const mutations = {}
const actions = {
  async login (context, payload) {
    await this.$axios
      .post('login', payload, { headers: { 'Content-Type': 'application/json' } })
      .then((response) => {
        context.commit('setUserId', response.data.id)
        sessionStorage.setItem('token', response.headers.token)
      })
  },
  async register (context, payload) {
    await this.$axios
      .post('register', payload)
      .then((response) => {
        context.commit('setUserId', response.data.id)
        sessionStorage.setItem('token', response.headers.token)
      })
  }
}

export default {
  getters,
  state,
  mutations,
  actions
}
