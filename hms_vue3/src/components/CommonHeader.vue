<template>
  <el-header>
    <div class="l-content">
      <el-button size="small" plain @click="handleCollapse">
        <el-icon :size="20">
          <Menu />
        </el-icon>
      </el-button>
      <!-- <h3>首页</h3> -->
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item :to="current.path" v-if="current">{{
          current.label
        }}</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="r-content">
      <el-dropdown>
        <img class="user" :src="getImgSrc('user')" alt="" />

        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="handlePersonalCenter">个人中心</el-dropdown-item>
            <el-dropdown-item @click="handleLoginOut">退出</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </el-header>
</template>

<script>
import { computed } from "vue-demi";
import { useStore } from "vuex";
import { useRouter } from 'vue-router';
import configs from "../config";
export default {
  setup() {
    const store = useStore();
    const router=useRouter();
    const getImgSrc = (user) => {
      return configs.baseApi + "/user/getUserAvatar/?usertoken=" + store.state.token
      // return new URL(`../assets/images/${user}.jpg`, import.meta.url).href;
    };
    const handleCollapse = () => {
      store.commit("updateIsCollapse");
    };
    const current = computed(() => {
      return store.state.currentMune;
    });

    const handleLoginOut=()=>{
        store.commit('cleanMenu');
        store.commit('cleanToken')
        router.push({name:'login'})
    }

    const handlePersonalCenter=()=>{
      router.push({name:'PersonalCenter'})

    }

    // console.log(current);
    return {
      getImgSrc,
      handleCollapse,
      current,
      handleLoginOut,
      handlePersonalCenter,

    };
  },
};
</script>

<style lang="less" scoped>
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.r-content {
  .user {
    width: 40px;
    height: 40px;
    border-radius: 50%;
  }
}

.l-content {
  display: flex;
  align-items: center;
  .el-button {
    margin-right: 20px;
    border: none;
  }
}
</style>