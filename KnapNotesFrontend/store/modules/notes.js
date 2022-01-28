const state = (() => {})()
const getters = {}
const mutations = {}
const actions = {
  async getAllNotes (context) {
    await this.$axios.get('note/get-all', { headers: { token: sessionStorage.getItem('token') } })
      .then((response) => {
        const userNotes = {}
        response.data.messages.forEach((element) => {
          userNotes[element.note_id] = {
            text: element.text,
            isEncrypted: element.is_encrypted,
            isPublic: element.is_public
          }
        })
        context.commit('setUserNotes', userNotes)
      })
  },
  async saveNote (context, payload) {
    return await this.$axios.put('/note/save', payload, { headers: { token: sessionStorage.getItem('token') } })
      .then((response) => {
        return response.data
      })
  },
  async getNote (context, payload) {
    return await this.$axios.post('/note/get', payload, { headers: { token: sessionStorage.getItem('token') } })
      .then((response) => {
        return response.data.text
      })
  },
  async createNote (context, payload) {
    return await this.$axios.post('note/new', payload, { headers: { token: sessionStorage.getItem('token') } })
      .then((response) => {
        return {
          noteId: response.data.note_id,
          data: {
            text: response.data.text,
            isEncrypted: response.data.is_encrypted,
            isPublic: response.data.is_public
          }
        }
      })
  }
}

export default {
  getters,
  state,
  mutations,
  actions
}
