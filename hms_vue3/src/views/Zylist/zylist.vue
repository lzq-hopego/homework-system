<template>
  
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
        prop="Obsolete"
        label="是否过时"
        width="80"
        :filters="[
          { text: '过时', value: '过时' },
          { text: '未过时', value: '未过时' },
        ]"
        :filter-method="filterTimeTag"
        filter-placement="bottom-end"
      >
        <template #default="scope">
          <el-tag
            :type="scope.row.Obsolete === '过时' ? 'danger' : 'success'"
            disable-transitions
            >{{ scope.row.Obsolete }}</el-tag
          >
        </template>
      </el-table-column>

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

  <el-drawer
    v-model="table"
    direction="rtl"
    size="40%"
    :with-header="false"
    @close="DrawerClose()"
  >
    <div>
      <div class="title">
        <h3>{{ zyInfo.title }}</h3>
        <p></p>
        <p>
          授课教师:&nbsp&nbsp{{ zyInfo.Teacher }}&nbsp&nbsp截止时间:&nbsp&nbsp{{
            zyInfo.StopTime
          }}
        </p>
      </div>
      <div class="body">
        <p>{{ zyInfo.Subheading }}</p>
        <img :src="zyInfo.FileUrl" alt="" v-if="zyInfo.FileType==='img'" height="300px" width="500px" />
        <div v-else-if="zyInfo.FileType==='file'" class="downfile">
          <p>无法在线预览提示文件</p>
          <el-button type="success" plain @click="downloadtestfile(zyInfo.FileUrl)">
            点击下载
          </el-button>

         
      </div>
      <p v-else>无提示文件</p>


      </div>
      <div class="foot" >
        <common-upload-file v-if="zyInfo.Obsolete==='未过时'"/>

      </div>
    </div>
  </el-drawer>

  <el-dialog
    v-model="centerDialogVisible"
    :title="ViewTitle"
    :width="dialogWidth"
    align-center
    destroy-on-close
  >
  
    <!-- <span>Open the dialog from the center from the screen</span> -->
    <div>
      <!-- <img v-if="filetype==='img'" :src="fileurl" class="show-img"> -->
      <!-- <button></button> -->
      <div class="demo-image__preview" v-if="filetype === 'img'" >
        <el-image
          style="width: 100px; height: 100px"
          :src="fileurl"
          :zoom-rate="1.2"
          :max-scale="7"
          :min-scale="0.2"
          :initial-index="4"
          :preview-src-list="srcList"
          fit="cover"
        />
      </div>

      <vue-office-docx
      v-else-if="filetype === 'word'"
        :src="fileurl"
        style="width: 100%"
      />
      <div v-else class="downfile">
          <p>无法在线预览</p>
          <el-button type="success" plain @click="downloadfile()">
            点击下载
          </el-button>
          
      </div>
      <!-- <div v-if="filetype==='word'" ref="docxData" class="docxData" element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading" element-loading-background="rgba(0, 0, 0, 0.8)" style="height:550px;overflow-y:auto;"></div> -->
      <!-- <docx-preview v-if="filetype==='word'" :docx="docxData" :style="{ width: '100%', height: '400px' }"></docx-preview> -->
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="centerDialogVisible = false">关闭</el-button>
      </div>
    </template>
  </el-dialog>
</template>


<script>
import { getCurrentInstance, onMounted, reactive, ref } from "vue";
import urlConfig from "../../config";
import { useStore } from "vuex";
import { ElMessageBox, ElMessage,ElNotification } from "element-plus";
import CommonUploadFile from "../../components/CommonUploadFile.vue";
import axios from "axios";

import VueOfficeDocx from "@vue-office/docx";
import "@vue-office/docx/lib/index.css";
import configs from "../../config";

export default {
  components: { CommonUploadFile, VueOfficeDocx },
  setup() {
    const { proxy } = getCurrentInstance();
    const list = ref([]);
    const table = ref(false);
    const zyInfo = ref();
    const store = useStore();
    const centerDialogVisible = ref(false);
    const ViewTitle = ref(null);
    const fileurl = ref(null);
    const filetype = ref(null);
    const srcList = ref([]);
    const dialogWidth = ref(500);

    // 请求全部数据时，使用的配置
    const config = reactive({
      total: 0,
      page: 1,
      title: "",
    });
    // 表格筛选
    const filterTag = (value, row) => {
      console.log(row.State, value);
      return row.State === value;
    };
    // 表格筛选
    const filterTimeTag = (value, row) => {
      console.log(row.Obsolete, value);
      return row.Obsolete === value;
    };
    const tableLabel = reactive([
      {
        prop: "title",
        label: "标题",
        width: 180,
      },
      {
        prop: "Subheading",
        label: "简介",
        width: 180,
      },
      {
        prop: "StartTime",
        label: "开始时间",
        width: 180,
      },
      {
        prop: "StopTime",
        label: "截止时间",
        width: 180,
      },
      {
        prop: "Teacher",
        label: "任课教师",
        width: 120,
      },
      {
        prop: "Score",
        label: "得分",
        width: 100,
      },
    ]);
    const formInline = reactive({
      keyword: "",
    });
    const compareTime = (gettime) => {
        var today = new Date()  //获取当前时间
        // gettime = gettime.replace(/-/g, '/');
        //转化成时间戳作比较
        var endTime = new Date(gettime) //自己的时间

        if (today < endTime) {
        //当前时间大于我的时间
          return "未过时"
        } else {
        //当前时间小于我的时间
          return "过时"
        }
      }
    const getzyDataList = async () => {
      let res = await proxy.$api.getzylist(config);
      config.total = res.count;
      list.value = res.list.map((item) => {
        item.title =
          item.title.length > 13
            ? item.title.substring(0, 13) + "..."
            : item.title;
        item.Subheading =
          item.Subheading.length > 13
            ? item.Subheading.substring(0, 13) + "..."
            : item.Subheading;
        item.FileUrl=configs.baseApi+item.FileUrl;
        item.Obsolete=compareTime(item.StopTime);
        return item;
      });

      console.log(list.value)
    };
    const handleEdit = async (row) => {
      store.commit("AlterClassTaskToken", row.token);

      let res = await proxy.$api.getzyinfo({ token: row.token });
      zyInfo.value = res;
      zyInfo.value.FileUrl=row.FileUrl+"&usertoken="+store.state.token
      zyInfo.value.Teacher = row.Teacher;
      zyInfo.value.Obsolete=row.Obsolete
      table.value = table.value === false ? true : false;
      if (row.Obsolete==='过时'){
        // 已过提交时间无法提交
        // ElMessageBox
        ElNotification({
          title: '错误',
          message: '已过提交时间无法提交',
          type: 'error',
          position: 'bottom-right',
        })
      }
    };
    const handleView = async (row) => {
      ViewTitle.value = row.title;
      centerDialogVisible.value = true;
      let res = await proxy.$api.viewmyzy({ token: row.token });
      // let ress=await proxy.$api.getmyzy({token:row.token})
      // console.log(res)

      filetype.value = res.filetype;

      fileurl.value =
        urlConfig.baseApi +
        "/zy/getmyzy?token=" +
        row.token +
        "&usertoken=" +
        store.state.token;
      
      

      if (filetype.value === "word") {
        console.log(fileurl.value);
        dialogWidth.value = 800;
        // await axios.get(fileurl.value, {
        //   responseType: 'arraybuffer' // 告诉 axios 我们想要一个 ArrayBuffer 响应
        // }).then((res)=>{
        //   renderAsync(res.data, proxy.$refs.docxData);
        // })
      }else if(filetype.value==='img'){
        srcList.value.pop();
        srcList.value.push(fileurl.value);
      } else {
        dialogWidth.value = 500;
      }
    };
    const handleDelete = async (row) => {
      ElMessageBox.confirm("确定删除吗？", "再次确认", {
        confirmButtonText: "确定",
        cancelButtonText: "不确定",
        type: "warning",
      })
        .then(async () => {
          let res = await proxy.$api.deletemyzy({ token: row.token });
          ElMessage.success(res.msg);
          getzyDataList();
        })
        .catch(() => {});
    };
    const handleSearch = () => {
      config.title = formInline.keyword;
      getzyDataList();
    };
    const DrawerClose = () => {
      getzyDataList();
      // table.value = table.value === true ? false : true;
      // console.log(1111)
    };
    const changePage = (page) => {
      // console.log(page)
      config.page = page;
      getzyDataList(config);
    };
    const downloadfile=async()=>{
      const result = await axios.get(fileurl.value,{responseType: 'blob'});
       // 创建一个 Blob 对象  
       const blob = new Blob([result.data], { type: result.headers['content-type'] });  
      // 创建一个指向 Blob 的 URL  
      const url = window.URL.createObjectURL(blob);  
        // 创建一个隐藏的 <a> 标签  
        const link = document.createElement('a');  
        link.href = url;  
        link.download = ''; // 设置下载的文件名  
        link.style.display = 'none';  
        // 将 <a> 标签添加到 DOM 中  
        document.body.appendChild(link);  
        // 模拟点击 <a> 标签来触发下载  
        link.click();  
        // 下载完成后，从 DOM 中移除 <a> 标签并释放 URL  
        document.body.removeChild(link);  
        window.URL.revokeObjectURL(url); 
    }


    const downloadtestfile=async(fileurl)=>{
      // console.log(zyInfo)
      const result = await axios.get(fileurl,{responseType: 'blob'});
       // 创建一个 Blob 对象  
       const blob = new Blob([result.data], { type: result.headers['content-type'] });  
      // 创建一个指向 Blob 的 URL  
      const url = window.URL.createObjectURL(blob);  
        // 创建一个隐藏的 <a> 标签  
        const link = document.createElement('a');  
        link.href = url;  
        link.download = zyInfo.value.title; // 设置下载的文件名  
        link.style.display = 'none';  
        // 将 <a> 标签添加到 DOM 中  
        document.body.appendChild(link);  
        // 模拟点击 <a> 标签来触发下载  
        link.click();  
        // 下载完成后，从 DOM 中移除 <a> 标签并释放 URL  
        document.body.removeChild(link);  
        window.URL.revokeObjectURL(url); 
    }


    onMounted(() => {
      getzyDataList();
    });

    return {
      formInline,
      list,
      config,
      tableLabel,
      filterTag,
      filterTimeTag,
      handleEdit,
      table,
      zyInfo,
      handleView,
      handleSearch,
      DrawerClose,
      changePage,
      handleDelete,
      centerDialogVisible,
      ViewTitle,
      fileurl,
      filetype,
      srcList,
      dialogWidth,
      downloadfile,
      downloadtestfile,


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

.user-header {
  display: flex;
  justify-content: space-between;
}

.el-drawer {
  text-align: center;
  width: 100%;
}
.title {
  h3 {
    font-size: 30px;
  }
  p {
    color: #c1c1c1;
    margin: 5px auto;
  }
}
.body {
  p {
    text-align: left;
    text-indent: 2em;
    font-size: 23px;
    word-wrap: break-word; /* 旧版本浏览器支持 */
    overflow-wrap: break-word; /* 标准属性 */
  }
  img {
    margin-top: 5px;
    margin-bottom: 3px;
  }
}
.docx-wrapper {
  background-color: white;
  margin-top: 0;
  padding-top: 0;
}
.downfile{
  width: 80%;
  border: 1px solid #dadada;
  border-radius: 5px;
  height: 40px;
  margin: 0 auto;
  margin-top: 20px;
  margin-bottom: 20px;
  .el-button{
    // justify-content: right;
    float: right;
    margin-top:4px;
    margin-right: 5px;
  }
  // background-color: black;
  p{
    font-size: 20px;
    color: #c1c1c1;
    margin-top: 8px;
    margin-left: 10px;
    float: left;
  }
}
</style>