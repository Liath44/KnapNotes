const state = (() => {})()
const getters = {}
const mutations = {}
const actions = {
  async getPublicNotes (context, payload) {
    return await this.$axios
      .get('get-public', payload)
      .then((response) => {
        const publicNotes = []
        response.data.messages.forEach((message) => {
          publicNotes.push(message.text)
        })
        return publicNotes
      })
  },
  async swapPrivacyStatusOfNote (context, payload) {
    return await this.$axios
      .put('note/change-privacy', payload, { headers: { token: sessionStorage.getItem('token') } })
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
