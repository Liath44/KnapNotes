<template>
  <v-container>
    <v-row align="stretch">
      <v-col
        v-for="(note, id) in userNotes"
        :key="id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
        xl="2"
        class="note-container"
      >
        <v-card v-if="note.isEncrypted" elevation="5" outlined class="pa-2 note" @click="initialisePassphrase(id)">
          <div class="center-container">
            <v-icon large>
              mdi-lock
            </v-icon>
          </div>
        </v-card>
        <v-card v-else elevation="5" outlined class="pa-2 note" @click="initialiseEditor(id, note.text)">
          {{ note.text }}
        </v-card>
      </v-col>
      <v-col
        cols="12"
        sm="6"
        md="4"
        lg="3"
        xl="2"
        class="note-container"
      >
        <v-card elevation="5" outlined class="pa=2 note" @click="noteCreator = true">
          <div class="center-container">
            <v-icon large>
              mdi-plus-thick
            </v-icon>
          </div>
        </v-card>
      </v-col>
    </v-row>
    <v-dialog
      v-model="editor"
      fullscreen
      hide-overlay
      persistent
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-toolbar>
          <v-toolbar-title>Edit</v-toolbar-title>
          <v-spacer />
          <v-btn icon @click="editor = false">
            <v-icon>
              mdi-close
            </v-icon>
          </v-btn>
        </v-toolbar>
        <v-md-editor
          v-model="currentNoteText"
          :left-toolbar="leftToolbar"
          :right-toolbar="rightToolbar"
          :toolbar="toolbar"
          height="calc(100vh - 64px)"
          @save="performSave"
          @swap-privacy="swapPrivacyStatusOfNote"
        />
      </v-card>
    </v-dialog>
    <v-dialog v-model="passphraseDialog" :width="cardWidth">
      <v-card outlined class="pa-2">
        <v-card-title>Enter passphrase</v-card-title>
        <v-text-field v-model="passphrase" type="password" />
        <div class="buttons-container">
          <v-btn @click="passphraseDialog = false">
            cancel
          </v-btn>
          <v-btn @click="fetchEncryptedNote">
            enter
          </v-btn>
        </div>
      </v-card>
    </v-dialog>
    <v-dialog v-model="noteCreator" :width="cardWidth">
      <v-card outlined class="pa-2">
        <v-card-title>Create new note</v-card-title>
        <v-radio-group v-model="isEncrypted" mandatory>
          <v-radio key="is-unencrypted" label="Unencrypted" :value="false" />
          <v-radio key="is-encrypted" :value="true">
            <template #label>
              <v-container>
                <v-row>
                  <v-col
                    xl="2"
                    lg="3"
                    sm="4"
                    cols="5"
                    align-self="center"
                    class="pa-0"
                  >
                    <div>
                      Encrypted
                    </div>
                  </v-col>
                  <v-col xl="10" lg="9" sm="8" cols="7" class="pa-0">
                    <v-text-field
                      id="passphrase"
                      v-model="newPassphrase"
                      label="passphrase"
                      prepend-icon="mdi-key"
                      type="password"
                    />
                  </v-col>
                </v-row>
              </v-container>
            </template>
          </v-radio>
        </v-radio-group>
        <div class="buttons-container">
          <v-btn @click="noteCreator = false">
            cancel
          </v-btn>
          <v-btn @click="createNote">
            create
          </v-btn>
        </div>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
export default {
  name: 'Index',
  async asyncData (context) {
    await context.store.dispatch('getAllNotes')
      .catch((error) => {
        console.log(error)
        context.redirect('/login')
      })
    return {
      userNotes: context.store.getters.userNotes
    }
  },
  data () {
    return {
      rightToolbar: 'preview toc sync-scroll',
      toolbar: {
        makePublicToolbar: {
          icon: 'v-md-icon-tip',
          title: 'Make public',
          action (editor) {
            editor.$emit('swap-privacy')
          }
        },
        makePrivateToolbar: {
          icon: 'v-md-icon-tip',
          title: 'Make private',
          action (editor) {
            editor.$emit('swap-privacy')
          }
        }
      },
      currentNoteId: undefined,
      encryptedNoteId: undefined,
      currentNoteText: undefined,
      editor: false,
      passphraseDialog: false,
      noteCreator: false,
      passphrase: '',
      newPassphrase: '',
      isEncrypted: true,
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
    },
    leftToolbar () {
      if (!this.currentNoteId || this.userNotes[this.currentNoteId].isEncrypted) {
        return 'undo redo clear | h bold italic strikethrough quote | ul ol table hr | link image code | save'
      }
      return this.userNotes[this.currentNoteId].isPublic
        ? 'undo redo clear | h bold italic strikethrough quote | ul ol table hr | link image code | makePrivateToolbar save'
        : 'undo redo clear | h bold italic strikethrough quote | ul ol table hr | link image code | makePublicToolbar save'
    }
  },
  methods: {
    initialiseEditor (noteId, noteText) {
      this.currentNoteId = noteId
      this.currentNoteText = noteText
      this.editor = true
    },
    initialisePassphrase (noteId) {
      this.encryptedNoteId = noteId
      this.passphraseDialog = true
    },
    async performSave () {
      await this.$store.dispatch('saveNote', { note_id: this.currentNoteId, text: this.currentNoteText })
        .then((data) => {
          this.userNotes[data.note_id].text = data.text
        })
        .catch((error) => {
          console.log(error)
        })
    },
    async fetchEncryptedNote () {
      const noteId = this.encryptedNoteId
      // if method fails then further action is undergone
      const noteText = await this.$store.dispatch('getNote', { note_id: noteId, passphrase: this.passphrase })
        .catch((error) => {
          console.log(error)
        })
      this.passphraseDialog = false
      this.initialiseEditor(noteId, noteText)
    },
    async createNote () {
      const payload = {
        is_encrypted: this.isEncrypted,
        passphrase: this.newPassphrase
      }
      await this.$store.dispatch('createNote', payload)
        .then((newNote) => {
          this.userNotes[newNote.noteId] = newNote.data
          this.noteCreator = false
        })
        .catch((error) => {
          console.log(error)
        })
    },
    async swapPrivacyStatusOfNote () {
      await this.$store.dispatch('swapPrivacyStatusOfNote', { note_id: this.currentNoteId })
        .then((updatedNote) => {
          this.userNotes[updatedNote.noteId] = updatedNote.data
        })
        .catch((error) => {
          console.log(error)
        })
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

.center-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.buttons-container {
  display: flex;
  justify-content: space-around;
}
</style>
