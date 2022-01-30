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
    <v-dialog
      v-model="preview"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-toolbar>
          <v-toolbar-title>Preview</v-toolbar-title>
          <v-spacer />
          <v-btn icon @click="preview = false">
            <v-icon>
              mdi-close
            </v-icon>
          </v-btn>
        </v-toolbar>
        <v-md-preview
          :text="currentNoteText"
        />
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
      currentNoteText: ''
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
</style>
