<template>
  <el-aside :width="$store.state.isCollapse ? '180px' : '64px'">
    <el-menu
      class="el-menu-vertical-demo"
      :collapse="!$store.state.isCollapse"
      :collapse-transition="true"
      :hide-timeout="800"
    >
      <h3 v-show="$store.state.isCollapse">作业平台</h3>
      <h3 v-show="!$store.state.isCollapse">作业<br />平台</h3>

      <el-menu-item
        :index="item.path"
        v-for="item in noChildren()"
        :key="item.path"
        @click="clickMenu(item)"
      >
        <el-icon>
          <component class="icons" :is="item.icon" />
        </el-icon>
        <span>{{ item.label }}</span>
      </el-menu-item>

      <el-sub-menu
        :index="item.label"
        v-for="item in haschildren()"
        :key="item.path"
      >
        <template #title>
          <el-icon>
            <component class="icons" :is="item.icon" />
          </el-icon>
          <span>{{ item.label }}</span>
        </template>
        <el-menu-item-group :title="item.label">
          <el-menu-item
            :index="subitem.path"
            v-for="(subitem, subindex) in item.children"
            :key="subindex"
            @click="clickMenu(subitem)"
          >
            <el-icon>
              <component class="icons" :is="subitem.icon" />
            </el-icon>
            <span>{{ subitem.name }}</span>
          </el-menu-item>
        </el-menu-item-group>
      </el-sub-menu>
    </el-menu>
  </el-aside>
</template>

<script>
import {useRouter} from 'vue-router'
import { useStore } from 'vuex';
export default {
  setup() {
    const store=useStore();
    const router=useRouter();
    const list = [
      {
        path: "/user",
        name: "user",
        label: "用户管理",
        icon: "user",
        url: "UserManage/UserManage",
      },
      {
        label: "其他",
        icon: "location",
        path: "/other",
        children: [
          {
            path: "/page1",
            name: "page1",
            label: "页面1",
            icon: "setting",
            url: "page1/page1",
          },
          {
            path: "/page2",
            name: "page2",
            label: "页面2",
            icon: "setting",
            url: "page2/page2",
          },
        ],
      },
    ];

    const asyncList=store.state.menu;

    const noChildren = () => {
      return asyncList.filter((item) => !item.children);
    };
    const haschildren = () => {
      return asyncList.filter((item) => item.children);
    };
    const clickMenu = (item) => {
        router.push({
            name:item.name,
        });
        store.commit('selectMenu',item);
    };

    return {
      noChildren,
      haschildren,
      clickMenu,
    };
  },
};
</script>


<style lang="less" scoped>
.el-menu {
  border-right: none;
  height:100%;
  h3 {
    margin-top: 30px;
    margin-bottom: 15px;
    line-height: 20px;
    text-align: center;
    font-family: 幼圆 bold;
  }
}
.el-aside{
    height: 100%;
    overflow:hidden;
}
</style>
