<template>
  <div class="login-container">
    <v-card :style="cardWidth" elevation="5" outlined shaped class="pa-4">
      <v-card-title>Welcome to CornyNotes</v-card-title>
      <v-text-field
        id="login"
        v-model="login"
        label="e-mail"
        prepend-icon="mdi-account"
      />
      <v-text-field
        id="password"
        v-model="password"
        label="password"
        prepend-icon="mdi-key"
        type="password"
      />
      <div class="buttons-container">
        <v-btn @click="doLogin">
          log in
        </v-btn>
        <v-btn @click="$router.push('/register')">
          register
        </v-btn>
      </div>
    </v-card>
  </div>
</template>

<script>
export default {
  name: 'Login',
  layout: 'empty',
  data () {
    return {
      login: '',
      password: '',
      widthsForBreakpoints: {
        xs: 90,
        sm: 70,
        md: 50,
        lg: 40,
        xl: 40
      }
    }
  },
  computed: {
    cardWidth () {
      return {
        width: this.widthsForBreakpoints[this.$vuetify.breakpoint.name] + '%'
      }
    }
  },
  methods: {
    doLogin () {
      this.$store
        .dispatch('login', { username: this.login.trim(), password: this.password.trim() })
        .then(() => {
          this.$router.push('/')
        })
        .catch((error) => {
          console.log(error)
        })
    }
  }
}
</script>

<style scoped>
.login-container {
  height: 100% !important;
  display: flex;
  align-content: center;
  align-items: center;
  justify-content: center;
}

.buttons-container {
  display: flex;
  justify-content: space-around;
}
</style>
