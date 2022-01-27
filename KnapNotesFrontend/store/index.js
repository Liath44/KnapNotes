import Vuex from 'vuex'
import authentication from '~/store/modules/authentication'
import notes from '~/store/modules/notes'

const createStore = () => {
  return new Vuex.Store({
    state () {
      return {
        userId: -1,
        userNotes: {}
      }
    },
    getters: {
      userNotes (state) {
        return state.userNotes
      }
    },
    mutations: {
      setUserId (state, userId) {
        state.userId = userId
      },
      setUserNotes (state, userNotes) {
        state.userNotes = userNotes
      }
    },
    modules: {
      authentication,
      notes
    }
  })
}

export default createStore
