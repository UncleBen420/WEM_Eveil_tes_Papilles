import { createApp } from 'vue'
import App from './App.vue'
import './assets/index.css'
import Axios from 'axios';
import VariablesService from "./services/variables.service";
import BackendService from "./services/backend.service";

Axios.get('/variables.json').then(({data}) => {
    VariablesService.init(data);
    BackendService.init(VariablesService.BACKEND_URL);

    createApp(App).mount('#app');
});
