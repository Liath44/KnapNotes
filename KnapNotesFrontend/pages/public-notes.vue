<template>
  <v-container>
    <v-row align="stretch">
      <v-col
        v-for="(note, id) in notes"
        :key="id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
        xl="2"
        class="note-container"
      >
        <v-card elevation="5" outlined class="pa-2 note" @click="initialisePreview(note)">
          {{ note }}
        </v-card>
      </v-col>
    </v-row>
    <v-dialog v-model="preview" :width="cardWidth">
      <v-card outlined class="pa-2">
        <div class="note-preview">
          {{ currentNoteText }}
        </div>
        <div class="buttons-container">
          <v-btn @click="preview = false">
            exit
          </v-btn>
        </div>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
export default {
  name: 'PublicNotes',
  async asyncData (context) {
    const notes = await context.store.dispatch('getPublicNotes')
      .catch((error) => {
        console.log(error)
        context.redirect('/')
      })
    return { notes }
  },
  data () {
    return {
      preview: false,
      currentNoteText: '',
      widthsForBreakpoints: {
        xs: 70,
        sm: 50,
        md: 40,
        lg: 30,
        xl: 30
      }
    }
  },
  computed: {
    cardWidth () {
      return this.widthsForBreakpoints[this.$vuetify.breakpoint.name] + '%'
    }
  },
  methods: {
    initialisePreview (text) {
      this.currentNoteText = text
      this.preview = true
    }
  }
}
</script>

<style scoped>
.note-container {
  height: 150px;
}

.note {
  height: 100%;
  overflow: hidden;
}

.buttons-container {
  display: flex;
  justify-content: flex-end;
}

.note-preview {
  height: 275px;
}
</style>
