<template>
  <div class="tags">
    <el-tag
    v-for="(tag,index) in tags"
    :key="tag.name"
    :closable="tag.name!=='home'"
    :disable-transitions="false"
    :effect="$route.name===tag.name?'dark':'plain'"
    @click="changeMenu(tag)"
    @close="handClose(tag,index)"
    >{{tag.label}}</el-tag>
  </div>
</template>

<script>
import { useStore } from "vuex";
import { useRoute, useRouter } from 'vue-router';
export default {
  setup() {
    const store=useStore();
    const router=useRouter();
    const route=useRoute();
    const tags=store.state.tabsList;
    const changeMenu=(item)=>{
        router.push({name:item.name})
    }
    const handClose=(tag,index)=>{
      
      let len=tags.length-1;
      store.commit('closeTag',tag);

      // 判断当前的页面的name,如果不一样则不用处理
      if (tag.name!=route.name) {
        return;
      }
      // 判断当前的页面的name一致时，判断本页面的位置，以便做路由跳转
      if(index===len){
        router.push({
          name:tags[index-1].name
        })
      }else{
        router.push({
          name:tags[index].name
        })
      }

    }
    return {
      tags,
      changeMenu,
      handClose,
    };
  },
};
</script>

<style lang="less" scoped>
.tags{
  padding-left: 20px;
  width: 100%;
  .el-tag{
    margin-right: 15px;
    cursor:pointer;
  }
}
</style>