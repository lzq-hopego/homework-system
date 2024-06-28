<template>
    <div class="common-layout">
      <el-container>
        <common-aside :md="0"/>
        <el-container class="r-container">
            
        <common-header/>
        <common-tag />

          <el-main>

                <router-view/>

          </el-main>
        </el-container>
      </el-container>
    </div>
  </template>
  

<script>
import {defineComponent} from 'vue'
import CommonHeader from '../components/CommonHeader.vue';
import CommonAside from '../components/CommonAside.vue';
import CommonTag from '../components/CommonTag.vue';

export default defineComponent({
  components: { CommonHeader, CommonAside, CommonTag },
})
</script>

<style lang="less" scoped>

.r-container{
    flex-wrap: wrap;
    align-items: flex-start;
    height: 100%;
}
.common-layout{
    height: 100%;
    & > .el-container{
        height: 100%;
        align-items: flex-start;
    }
    & > .el-aside{
        height: 100%;    
    }
    .el-main{
      height: calc(100% - 124px) !important;;
    }

    
}

</style>