import Vue from 'vue'
import VueMarkdownEditor from '@kangc/v-md-editor'
import VMdPreview from '@kangc/v-md-editor/lib/preview'
import '@kangc/v-md-editor/lib/style/base-editor.css'
import '@kangc/v-md-editor/lib/style/preview.css'
import vuepressTheme from '@kangc/v-md-editor/lib/theme/vuepress.js'
import '@kangc/v-md-editor/lib/theme/style/vuepress.css'
import '@kangc/v-md-editor/lib/theme/style/github.css'

import enUS from '@kangc/v-md-editor/lib/lang/en-US'

// Prism
import Prism from 'prismjs'
// highlight code
import 'prismjs/components/prism-json'

VueMarkdownEditor.use(vuepressTheme, {
  Prism
})

VMdPreview.use(vuepressTheme, {
  Prism
})

VueMarkdownEditor.lang.use('en-US', enUS)
VMdPreview.lang.use('en-US', enUS)

Vue.use(VueMarkdownEditor)
Vue.use(VMdPreview)
