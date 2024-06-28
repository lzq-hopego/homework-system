<script setup>
// import { useRouter } from "vue-router";
// import { useStore } from "vuex";

// const store=useStore();
// const router=useRouter();
// store.commit('addMenu',router);
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'

</script>

<template>
  <el-config-provider :locale="zhCn">
    <router-view />
  </el-config-provider>

  <!-- <router-view /> -->
</template>

<style>
#app{
  height: 100vh;

}
</style>
