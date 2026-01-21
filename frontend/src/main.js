import { createApp } from 'vue'
import { FrappeUI } from 'frappe-ui'
import router from './router'
import App from './App.vue'
import './index.css'

const app = createApp(App)

app.use(FrappeUI)
app.use(router)

app.mount('#app')
