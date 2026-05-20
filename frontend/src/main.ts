import { createApp } from "vue";
import { createPinia } from "pinia";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import ElementPlus from "element-plus";
import App from "./App.vue";
import { setupRouter } from "@/router";
import { setupElIcons } from "@/plugins/icons";

import "element-plus/theme-chalk/dark/css-vars.css";
import "element-plus/dist/index.css";
import "./styles/index.scss";

const app = createApp(App);

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);
app.use(pinia);
app.use(ElementPlus);
setupElIcons(app);

app.directive("hasPerm", { mounted() {} });

setupRouter(app);
app.mount("#app");
