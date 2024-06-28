<template>
  <div class="user-header">
    <el-button type="primary" @click="handleAdd"
      ><el-icon><CirclePlus /></el-icon>&nbsp新增</el-button
    >
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
          { text: '已过时', value: '已过时' },
          { text: '未过时', value: '未过时' },
        ]"
        :filter-method="filterTag"
        filter-placement="bottom-end"
      >
        <template #default="scope">
          <el-tag
            :type="scope.row.State === '已过时' ? 'danger' : 'success'"
            disable-transitions
            >{{ scope.row.State }}</el-tag
          >
        </template>
      </el-table-column>

      <el-table-column fixed="right" label="操作" min-width="120">
        <template #default="scope">
          <el-button type="success" size="small" @click="handleEdit(scope.row)"
            >编辑</el-button
          >
          <el-button
            type="primary"
            size="small"
            @click="handleViewZyinfo(scope.row)"
            >查看</el-button
          >
          <el-button type="info" size="small" @click="handleView(scope.row)"
            >预览</el-button
          >
          <el-button type="danger" size="small" @click="handleDelete(scope.row)"
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
    v-model="viewzypage"
    direction="rtl"
    size="40%"
    :with-header="false"
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
        <img
          :src="zyInfo.FileUrl"
          alt=""
          v-if="zyInfo.FileType === 'img'"
          height="300px"
          width="500px"
        />
        <div v-else-if="zyInfo.FileType === 'file'" class="downfile">
          <p>无法在线预览提示文件</p>
          <el-button type="success" plain @click="downloadtestfile(zyInfo.FileUrl)">
            点击下载
          </el-button>
        </div>
        <div v-else class="downfile">
          <p>无提示文件</p>
        </div>
      </div>
    </div>
  </el-drawer>

  <el-dialog
    v-model="dialogVisible"
    :title="action == 'add' ? '新增作业' : '编辑作业'"
    width="35%"
    :before-close="handleClose"
    class="addzy"
  >
    <el-form :inline="true" :model="formZy" ref="formZydata" :rules="rules">
      <el-row>
        <!-- <el-col :span="12"> -->
        <el-form-item label="标题" prop="title">
          <el-input
            v-model="formZy.title"
            placeholder="标题"
            maxlength="30"
            show-word-limit
            clearable
          />
        </el-form-item>
      </el-row>

      <!-- </el-col>
          <el-col :span="12"> -->
      <el-row>
        <el-form-item label="小标题" prop="Subheading">
          <el-input
            v-model="formZy.Subheading"
            placeholder="小标题"
            maxlength="400"
            show-word-limit
            type="textarea"
            clearable
          />
        </el-form-item>
        <!-- </el-col> -->
      </el-row>

      <el-row>
        <el-col :span="12">
          <el-form-item label="开始时间" prop="StartTime">
            <!-- <el-input
                v-model="formZy.StartTime"
                placeholder="开始时间"
                clearable
              /> -->
            <el-date-picker
              v-model="formZy.StartTime"
              type="datetime"
              placeholder="选择开始时间"
              format="YYYY-MM-DD HH:mm:ss"
              date-format="MMM DD, YYYY"
              time-format="HH:mm"
              value-format="YYYY-MM-DD HH:mm:ss"
            />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12">
          <el-form-item label="结束时间" prop="StopTime">
            <!-- <el-input
                v-model="formZy.StopTime"
                placeholder="结束时间"
                clearable
              /> -->
            <el-date-picker
              v-model="formZy.StopTime"
              type="datetime"
              placeholder="选择结束时间"
              format="YYYY-MM-DD HH:mm:ss"
              date-format="MMM DD, YYYY"
              value-format="YYYY-MM-DD HH:mm:ss"
              time-format="HH:mm"
            />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-form-item label="提示文件类型" prop="FileType">
          <el-select
            v-model="formZy.FileType"
            placeholder="请选择类型"
            style="width: 120px"
          >
            <el-option label="图片" value="img" />
            <el-option label="文件" value="file" />
          </el-select>
        </el-form-item>
      </el-row>

      <el-row>
        <el-form-item label="提示文件" prop="FileUrl">
          <!-- <el-input type="file"  v-model="formZy.FileUrl" ></el-input> -->
          <el-upload
            action="none"
            :auto-upload="false"
            :multiple="false"
            :limit="1"
            :headers="{ 'Content-Type': 'multipart/form-data' }"
            :on-change="handleChange"
          >
            <el-button size="small" type="primary">点击上传</el-button>
          </el-upload>
        </el-form-item>
      </el-row>

      <el-row>
        <el-col :span="12">
          <el-form-item label="班级" prop="classes">
            <el-select-v2
              v-model="formZy.classes"
              :options="options"
              placeholder="选择班级"
              style="width: 200px"
              multiple
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="教师" prop="Teacher">
            <el-select
              v-model="formZy.Teacher"
              placeholder="请选择教师"
              style="width: 120px"
            >
              <el-option
                v-for="item in teachers"
                :label="item.name"
                :value="item.id"
              />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row style="justify-content: flex-end">
        <el-form-item>
          <el-button type="info" @click="handleCancel">取消</el-button>
          <el-button type="primary" @click="onSubmit">确定</el-button>
        </el-form-item>
      </el-row>
    </el-form>
  </el-dialog>

  <el-drawer v-model="table" title="完成情况统计" direction="rtl" size="50%">
    <el-table :data="zyinfolist" style="width: 100%" :height="500">
      <el-table-column
        v-for="item in zyinfoLable"
        :key="item.prop"
        :label="item.label"
        :prop="item.prop"
        :width="item.width ? item.width : 125"
      />

      <el-table-column fixed="right" label="操作" min-width="120">
        <template #default="scope">
          <el-button
            type="success"
            size="small"
            @click="handleViewZylistinfo(scope.row)"
            >查看</el-button
          >
        </template>
      </el-table-column>
    </el-table>
  </el-drawer>

  <el-dialog
    v-model="dialogTableVisible"
    :title="zyclassinfotitle"
    width="1200"
  >
    <!-- handleZipZylistinfo(scope.row) -->
    <!-- <el-button
    type="success"
    size="small"
    @click=""
    >
    
      打包下载
    </el-button> -->
    <el-button type="primary" :loading="zipdownloadstate" @click="DownzipAllzy()">
      <template #loading>
        <div class="custom-loading">
          <svg class="circular" viewBox="-10, -10, 50, 50">
            <path
              class="path"
              d="
            M 30 15
            L 28 17
            M 25.61 25.61
            A 15 15, 0, 0, 1, 15 30
            A 15 15, 0, 1, 1, 27.99 7.5
            L 15 15
          "
              style="stroke-width: 4px; fill: rgba(0, 0, 0, 0)"
            />
          </svg>
        </div>
      </template>
      {{downloadfile_zip_msg}}
    </el-button>

    <el-table :data="gridData" :height="470">
      <el-table-column
        v-for="item in zyclassinfoLable"
        :key="item.prop"
        :label="item.label"
        :prop="item.prop"
        :width="item.width ? item.width : 125"
      />

      <el-table-column
        prop="IsReplace"
        label="代交"
        width="100"
        :filters="[
          { text: '是', value: '是' },
          { text: '否', value: '否' },
        ]"
        :filter-method="filterIsReplace"
        filter-placement="bottom-end"
      >
        <template #default="scope">
          <el-tag
            :type="scope.row.IsReplace === '是' ? 'danger' : 'success'"
            disable-transitions
            >{{ scope.row.IsReplace }}</el-tag
          >
        </template>
      </el-table-column>

      <el-table-column
        prop="State"
        label="状态"
        width="100"
        :filters="[
          { text: '未交', value: '未交' },
          { text: '已交', value: '已交' },
        ]"
        :filter-method="filterTag"
        filter-placement="bottom-end"
      >
        <template #default="scope">
          <el-tag
            :type="scope.row.State === '未交' ? 'danger' : 'success'"
            disable-transitions
            >{{ scope.row.State }}</el-tag
          >
        </template>
      </el-table-column>

      <el-table-column fixed="right" label="操作" min-width="120">
        <template #default="scope">
          <el-button
            v-if="scope.row.State === '已交'"
            type="primary"
            size="small"
            @click="downloadfile(scope.row)"
            >下载</el-button
          >
          <el-button
            v-if="scope.row.State === '已交'"
            type="info"
            size="small"
            @click="Viewzyinfo(scope.row)"
            >预览</el-button
          >
          <el-button
            v-if="scope.row.State === '已交'"
            type="danger"
            size="small"
            @click="DeleteStuzy(scope.row)"
            >删除</el-button
          >

          <el-button
            v-if="scope.row.State === '未交'"
            type="success"
            size="small"
            @click=""
            >代交</el-button
          >
        </template>
      </el-table-column>
    </el-table>
  </el-dialog>

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
      <div class="demo-image__preview" v-if="filetype === 'img'">
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
        <el-button type="success" plain> 请返回到列表进行下载 </el-button>
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
//   import urlConfig from "../../config";
import { useStore } from "vuex";
import { ElMessageBox, ElMessage } from "element-plus";
import configs from "../../config";
import VueOfficeDocx from "@vue-office/docx";
import axios from "axios";

export default {
  components: { VueOfficeDocx },
  setup() {
    const { proxy } = getCurrentInstance();
    const list = ref([]);
    const table = ref(false);
    const zyInfo = ref();
    const viewzypage = ref(false);
    const store = useStore();
    const dialogVisible = ref(false);
    // const classes=ref([]);
    const teachers = ref([]);
    const options = ref([]);
    const mutipartFile = new FormData();
    const action = ref("add");
    const zyinfolist = ref([]);
    const dialogTableVisible = ref(false);
    const zyclassinfotitle = ref();
    const gridData = ref([]);
    const centerDialogVisible = ref(false);
    const filetype = ref();
    const fileurl = ref();
    const ViewTitle = ref();
    const srcList = ref([]);
    const dialogWidth = ref(500);
    const zipdownloadstate = ref(false);
    const classid=ref();
    const Tasktoken=ref();
    const ZyTitle=ref();
    const downloadfile_zip_msg=ref("点击压缩并下载"); //下载压缩包的提示信息

    //添加作业信息对象
    const formZy = reactive({
      title: "",
      Subheading: "",
      StartTime: "",
      StopTime: "",
      classes: "",
      Teacher: "",
      FileType: "",
      FileUrl: "",
    });

    const handleChange = (file) => {
      mutipartFile.set("Filename", file.name);
      mutipartFile.set("FileUrl", file.raw);
      // console.log(formZy.title)
    };

    // 请求全部数据时，使用的配置
    const config = reactive({
      total: 0,
      page: 1,
      title: "",
    });
    // 表格筛选
    const filterTag = (value, row) => {
      // console.log(row.State, value);
      return row.State === value;
    };
    const filterIsReplace = (value, row) => {
      return row.IsReplace === value;
    };

    const zyclassinfoLable = reactive([
      {
        prop: "name",
        label: "姓名",
        width: 80,
      },
      {
        prop: "PutTime",
        label: "提交时间",
        width: 180,
      },
      {
        prop: "Score",
        label: "成绩",
        width: 60,
      },
      {
        prop: "ReplaceUser",
        label: "代交人",
        width: 80,
      },
      {
        prop: "PutIp",
        label: "提交时ip",
        width: 180,
      },
      {
        prop: "Repetiton",
        label: "查重率",
        width: 80,
      },
    ]);
    const zyinfoLable = reactive([
      {
        prop: "classes",
        label: "班级",
        width: 400,
      },
    ]);

    const tableLabel = reactive([
      {
        prop: "title",
        label: "标题",
        width: 180,
      },
      {
        prop: "Subheading",
        label: "简介",
        width: 260,
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
        width: 80,
      },
      {
        prop: "classes",
        label: "班级",
        width: 80,
      },
    ]);
    const formInline = reactive({
      keyword: "",
    });
    // 添加作业时信息过滤规则
    const rules = reactive({
      title: [
        { required: true, message: "请填写标题", trigger: "blur" },
        { min: 2, message: "字数在2以上", trigger: "blur" },
        { max: 30, message: "字数在30字以内", trigger: "blur" },
      ],
      Subheading: [
        { required: true, message: "请选择填写小标题", trigger: "blur" },
        { min: 2, message: "字数在2以上", trigger: "blur" },
        { max: 400, message: "字数在400字以内", trigger: "blur" },
      ],
      StartTime: [
        { required: true, message: "请选择作业开始时间", trigger: "blur" },
      ],
      classes: [{ required: true, message: "请选择班级", trigger: "blur" }],
      StopTime: [
        { required: true, message: "请选择作业结束时间", trigger: "blur" },
      ],
      Teacher: [{ required: true, message: "请选择任课老师", trigger: "blur" }],
    });
    const getzyDataList = async () => {
      let res = await proxy.$api.getglzylist(config);
      config.total = res.count;
      list.value = res.list.map((item) => {
        item.Subheading =
          item.Subheading.length > 20
            ? item.Subheading.substring(0, 20) + "..."
            : item.Subheading;
        item.title =
          item.title.length > 20
            ? item.title.substring(0, 20) + "..."
            : item.title;
        item.FileUrl = configs.baseApi + item.FileUrl+"&usertoken="+store.state.token;

        return item;
      });
    };

    //获取全部班级
    const getclass = async () => {
      let res = await proxy.$api.getClasses();
      options.value = res.list.map((item) => {
        item.value = item.id;
        item.label = item.name;
        return item;
      });
      // classes.value=res.list.map((item) => {
      //   return item;
      // })
    };
    //获取全部班级
    const getteacher = async () => {
      let res = await proxy.$api.getTeacher();
      teachers.value = res.list.map((item) => {
        return item;
      });
    };

    const handleEdit = async (row) => {
      action.value = "edit";
      dialogVisible.value = true;
      getclass();
      getteacher();

      let res=await proxy.$api.getzyinfo({token:row.token});

      
      res.classes = "";
      res.Teacher = "";
      if (res.FileType==="null"){
        res.FileType="file"
      }
      proxy.$nextTick(() => {
        //浅拷贝进行数据赋值
        Object.assign(formZy, res);
      });
    };
    const handleView = async(row) => {
      let res=await proxy.$api.getzyinfo({token:row.token});
      zyInfo.value = res;

      // console.log(res)
      zyInfo.value.FileUrl = configs.baseApi + res.FileUrl+"&usertoken="+store.state.token;
      viewzypage.value = true;
    };

    // 删除作业
    const handleDelete = async (row) => {
      ElMessageBox.confirm("确定删除吗？", "再次确认", {
        type: "warning",
      })
        .then(async () => {
          await proxy.$api.delzy({ token: row.token });
          ElMessage({
            message: "删除成功",
            type: "success",
          });
          getzyDataList(config);
        })
        .catch(() => {});
    };
    const handleSearch = () => {
      config.title = formInline.keyword;
      getzyDataList();
    };

    const changePage = (page) => {
      // console.log(page)
      config.page = page;
      getzyDataList(config);
    };

    const handleViewZyinfo = async (row) => {
      table.value = true;
      let res = await proxy.$api.getZyClassesInfo({token:row.token});
      zyinfolist.value = res.map((item) => {
        item.classes = item.name;
        item.token = row.token;
        return item;
      });
      ZyTitle.value=row.title
      // console.log(res)

      // let res=proxy.$api.getglzyinfo({'token':row.token})
      // console.log(res);
    };


    const getgridData=async()=>{
      let res = await proxy.$api.getglzyinfo({ id: classid.value, token: Tasktoken.value });
      gridData.value = res.map((item) => {
        item.IsReplace = item.IsReplace ? item.IsReplace : "否";
        return item;
      });
    }


    const handleViewZylistinfo = async (row) => {
      dialogTableVisible.value = true;
      zyclassinfotitle.value = row.classes + "的作业提交情况";


      classid.value=row.id
      Tasktoken.value=row.token

      getgridData()
      // console.log( res.PromiseResult)
    };



    const handleAdd = () => {
      action.value = "add";
      dialogVisible.value = true;
      getclass();
      getteacher();

      // console.log(options.value)
    };

    //关闭添加的弹窗，并清除所填的内容
    const handleCancel = () => {
      dialogVisible.value = false;
      proxy.$refs.formZydata.resetFields();
      mutipartFile.set("Filename", "");
      mutipartFile.set("FileUrl", "");
    };

    const onSubmit = () => {
      // console.log(formZy)
      proxy.$refs.formZydata.validate(async (valid) => {
        if (valid) {
          let res;
          if (action.value == "add") {
            mutipartFile.set("title", formZy.title);
            mutipartFile.set("Subheading", formZy.Subheading);
            mutipartFile.set("StartTime", formZy.StartTime);
            mutipartFile.set("StopTime", formZy.StopTime);
            mutipartFile.set("classes", formZy.classes);
            mutipartFile.set("Teacher", formZy.Teacher);
            mutipartFile.set("FileType", formZy.FileType);
            mutipartFile.set("token", "aaa");
            res = await proxy.$api.addzy(mutipartFile);
          } else {
            // mutipartFile.set('classes',formZy.classes)
            // console.log(formZy.token,formZy.classes)
            mutipartFile.set("title", formZy.title);
            mutipartFile.set("Subheading", formZy.Subheading);
            mutipartFile.set("StartTime", formZy.StartTime);
            mutipartFile.set("StopTime", formZy.StopTime);
            mutipartFile.set("classes", formZy.classes);
            mutipartFile.set("Teacher", formZy.Teacher);
            mutipartFile.set("FileType", formZy.FileType);
            mutipartFile.set("token", formZy.token);
            // res=11
            res = await proxy.$api.editzy(mutipartFile);
          }

          if (res != null) {
            handleCancel();
            getzyDataList();
          }
        }
      });
    };

    const handleClose = (done) => {
      ElMessageBox.confirm("确定关闭吗?")
        .then(() => {
          done();
        })
        .catch(() => {
          // catch error
        });
    };

    const Viewzyinfo = async (row) => {
      centerDialogVisible.value = true;
      filetype.value = row.filetype;
      fileurl.value = configs.baseApi + "/getglstuzyinfo?id=" + row.id+"&usertoken="+store.state.token;
      ViewTitle.value = row.name + "的作业";

      console.log(row);

      if (filetype.value === "word") {
        // console.log(fileurl.value);
        dialogWidth.value = 800;
        // await axios.get(fileurl.value, {
        //   responseType: 'arraybuffer' // 告诉 axios 我们想要一个 ArrayBuffer 响应
        // }).then((res)=>{
        //   renderAsync(res.data, proxy.$refs.docxData);
        // })
      } else if (filetype.value === "img") {
        srcList.value.pop();
        srcList.value.push(fileurl.value);
      } else {
        dialogWidth.value = 500;
      }
    };

    const downloadfile = async (row) => {
      let file_url = configs.baseApi + "/getglstuzyinfo?id=" + row.id+"&usertoken="+store.state.token;

      const result = await axios.get(file_url, { responseType: "blob" });
      // 创建一个 Blob 对象
      const blob = new Blob([result.data], {
        type: result.headers["content-type"],
      });
      // 创建一个指向 Blob 的 URL
      const url = window.URL.createObjectURL(blob);
      // 创建一个隐藏的 <a> 标签
      const link = document.createElement("a");
      link.href = url;
      link.download = row.name; // 设置下载的文件名
      link.style.display = "none";
      // 将 <a> 标签添加到 DOM 中
      document.body.appendChild(link);
      // 模拟点击 <a> 标签来触发下载
      link.click();
      // 下载完成后，从 DOM 中移除 <a> 标签并释放 URL
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    };

     // 删除作业
     const DeleteStuzy = async (row) => {
      ElMessageBox.confirm("确定删除吗？", "再次确认", {
        type: "warning",
      })
        .then(async () => {
          await proxy.$api.delstuzy({ id: row.id });
          ElMessage({
            message: "删除成功",
            type: "success",
          });
          getgridData()
        })
        .catch(() => {});
    };

    const DownzipAllzy=async()=>{
      downloadfile_zip_msg.value="正在下载"
      ElMessage({
            message: "正在下载由于服务器带宽过小，可能需要一些时间，请耐心等待",
            type: "success",
          });

      zipdownloadstate.value=true
      // console.log(classid.value,Tasktoken.value)
      const res=await axios.get(configs.baseApi + "/getglstuzyzip?id="+classid.value+"&"+"Tasktoken="+Tasktoken.value+"&usertoken="+store.state.token, { responseType: "blob" })

      // 创建一个 Blob 对象
      const blob = new Blob([res.data], {
        type: res.headers["content-type"],
      });
      // 创建一个指向 Blob 的 URL
      const url = window.URL.createObjectURL(blob);
      // 创建一个隐藏的 <a> 标签
      const link = document.createElement("a");
      link.href = url;
      link.download = ZyTitle.value; // 设置下载的文件名
      link.style.display = "none";
      // 将 <a> 标签添加到 DOM 中
      document.body.appendChild(link);
      // 模拟点击 <a> 标签来触发下载
      link.click();
      // 下载完成后，从 DOM 中移除 <a> 标签并释放 URL
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);


      zipdownloadstate.value=false
      downloadfile_zip_msg.value="点击压缩并下载"
    }

    const downloadtestfile=async(fileurl)=>{
      
      // console.log(fileurl)
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
      handleEdit,
      table,
      zyInfo,
      handleView,
      handleSearch,
      changePage,
      handleDelete,
      handleAdd,
      viewzypage,
      handleViewZyinfo,
      dialogVisible,
      formZy,
      handleCancel,
      onSubmit,
      handleClose,
      rules,
      // classes,
      teachers,
      options,
      handleChange,
      action,
      zyinfoLable,
      zyinfolist,
      handleViewZylistinfo,
      dialogTableVisible,
      zyclassinfotitle,
      gridData,
      zyclassinfoLable,
      filterIsReplace,
      centerDialogVisible,
      Viewzyinfo,
      filetype,
      fileurl,
      ViewTitle,
      dialogWidth,
      srcList,
      downloadfile,
      zipdownloadstate,
      DownzipAllzy,
      DeleteStuzy,
      downloadtestfile,
      downloadfile_zip_msg,
    };
  },
};
</script>
  
  
  
  
  <style lang="less">
.el-button .custom-loading .circular {
  margin-right: 6px;
  width: 18px;
  height: 18px;
  animation: loading-rotate 2s linear infinite;
}
.el-button .custom-loading .circular .path {
  animation: loading-dash 1.5s ease-in-out infinite;
  stroke-dasharray: 90, 150;
  stroke-dashoffset: 0;
  stroke-width: 2;
  stroke: var(--el-button-text-color);
  stroke-linecap: round;
}
.table {
  position: relative;
  height: 520px;
  .pager {
    position: absolute;
    right: 0;
    bottom: -20px;
  }
}
.addzy {
  .el-input {
    width: 400px;
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
.downfile {
  width: 80%;
  border: 1px solid #dadada;
  border-radius: 5px;
  height: 40px;
  margin: 0 auto;
  .el-button {
    // justify-content: right;
    float: right;
    margin-top: 4px;
    margin-right: 5px;
  }
  // background-color: black;
  p {
    font-size: 20px;
    color: #c1c1c1;
    margin-top: 8px;
    margin-left: 10px;
    float: left;
  }
}
</style>