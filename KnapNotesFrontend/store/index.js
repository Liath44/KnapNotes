import Vuex from 'vuex'
import authentication from '~/store/modules/authentication'

const createStore = () => {
  return new Vuex.Store({
    modules: {
      authentication
    }
  })
}

export default createStore
