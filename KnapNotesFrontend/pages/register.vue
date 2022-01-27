<template>
  <div class="register-container">
    <v-card :style="cardWidth" elevation="5" outlined shaped class="pa-4">
      <v-card-title>Register</v-card-title>
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
      <v-text-field
        id="password2"
        v-model="password2"
        label="repeat password"
        prepend-icon="mdi-key"
        type="password"
      />
      <div class="buttons-container">
        <v-btn @click="doRegister">
          register
        </v-btn>
      </div>
    </v-card>
  </div>
</template>

<script>
export default {
  name: 'Register',
  layout: 'empty',
  data () {
    return {
      login: '',
      password: '',
      password2: '',
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
  // TODO: Add frontside password/login verification
  methods: {
    doRegister () {
      if (this.password !== this.password2) {
        console.log('Passwords do not match')
        return
      }
      this.$store
        .dispatch('register', { username: this.login.trim(), password: this.password.trim() })
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
.register-container {
  height: 100% !important;
  display: flex;
  align-content: center;
  align-items: center;
  justify-content: center;
}

.buttons-container {
  display: flex;
  justify-content: center;
}
</style>
