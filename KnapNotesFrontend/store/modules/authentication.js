const state = (() => {})()
const getters = {}
const mutations = {}
const actions = {
  async login (context, payload) {
    const response = await this.$axios
      .$post('login', payload, { headers: { 'Content-Type': 'application/json' } })
    console.log(response)
  }
}

export default {
  getters,
  state,
  mutations,
  actions
}
