<template>
    <div class="zy-header">
    <el-button type="primary" @click="handleAdd"
      ><el-icon><CirclePlus /></el-icon>&nbsp新增</el-button
    >
    <el-form :inline="true" :model="formInline">
      <el-form-item label="请输入">
        <el-input
          v-model="formInline.keyword"
          placeholder="请输入用户名"
          clearable
        />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="handleSearch">搜索</el-button>
      </el-form-item>
    </el-form>
    </div>


    <div class="table">
        <div class="user-header">
    <el-form :inline="true" :model="formInline">
      <el-form-item label="请输入">
        <el-input
          v-model="formInline.keyword"
          placeholder="请输入作业标题"
          clearable
        />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="handleSearch">搜索</el-button>
      </el-form-item>
    </el-form>
  </div>
  <div class="table">
    <el-table :data="list" style="width: 100%" :height="500">
      <el-table-column
        v-for="item in tableLabel"
        :key="item.prop"
        :label="item.label"
        :prop="item.prop"
        :width="item.width ? item.width : 125"
      />

      <el-table-column
        prop="State"
        label="状态"
        width="100"
        :filters="[
          { text: '已做', value: '已做' },
          { text: '未做', value: '未做' },
        ]"
        :filter-method="filterTag"
        filter-placement="bottom-end"
      >
        <template #default="scope">
          <el-tag
            :type="scope.row.State === '未做' ? 'danger' : 'success'"
            disable-transitions
            >{{ scope.row.State }}</el-tag
          >
        </template>
      </el-table-column>

      <el-table-column fixed="right" label="操作" min-width="120">
        <template #default="scope">
          <el-button
            v-if="scope.row.State === '未做'"
            type="success"
            size="small"
            @click="handleEdit(scope.row)"
            >编辑</el-button
          >
          <el-button
            v-if="scope.row.State === '已做'"
            type="primary"
            size="small"
            @click="handleView(scope.row)"
            >查看</el-button
          >
          <el-button
            v-if="scope.row.State === '已做'"
            type="danger"
            size="small"
            @click="handleDelete(scope.row)"
            >删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      small
      background
      layout="prev, pager, next"
      :total="config.total"
      :page-size="11"
      class="pager mt-4"
      @current-change="changePage"
    />
  </div>
  </div>

  <el-drawer
    v-model="table"
    title="I have a nested table inside!"
    direction="rtl"
    size="50%"
  >
    <el-table :data="gridData">
      <el-table-column property="date" label="Date" width="150" />
      <el-table-column property="name" label="Name" width="200" />
      <el-table-column property="address" label="Address" />
    </el-table>
  </el-drawer>

</template>


<script>
import { getCurrentInstance, onMounted, reactive, ref, computed } from "vue";


export default {
  setup() {
    const { proxy } = getCurrentInstance();
    const list = ref([]);
    const formInline = reactive({
      keyword: "",
    });
    const table=ref(false);
    const config = reactive({
      total: 0,
      page: 1,
      name: "",
    });
    const tableLabel = reactive([
      {
        prop: "name",
        label: "班级名",
        width: 240,
      },{
        prop: "name",
        label: "班级名",
        width: 240,
      },{
        prop: "name",
        label: "班级名",
        width: 240,
      },{
        prop: "name",
        label: "班级名",
        width: 240,
      },
    ])
    const handleAdd=()=>{

    }
    const handleSearch=()=>{

    }
    const handleView=()=>{
        // table.value=true
        // getzylist
    }
    const changePage=()=>{

    }
    const getUserData=async()=>{
        let res=await proxy.$api.getzylist(config);
        // config.total = res.count;
        list.value = res.list.map((item) => {
        return item;
      });
    }
    onMounted(() => {
      getUserData(config);
    });
    return {
      list,
      table,
      tableLabel,
      config,
      changePage,
      formInline,
      handleSearch,
    //   dialogVisible,
    //   handleClose,
    //   formUser,
    //   onSubmit,
    //   rules,
    //   handleCancel,
    //   action,
    handleView,
      handleAdd,
    //   classes,
    };
  },
};
</script>


<style lang="less">
.table {
  position: relative;
  height: 520px;
  .pager {
    position: absolute;
    right: 0;
    bottom: -20px;
  }
}

.zy-header {
  display: flex;
  justify-content: space-between;
}
</style>