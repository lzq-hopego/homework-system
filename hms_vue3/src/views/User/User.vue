<template>
  <div class="user-header">
    <el-button type="primary" @click="handleAdd"
      ><el-icon><CirclePlus /></el-icon>&nbsp新增</el-button
    >

    <el-dialog
      v-model="dialogVisible"
      :title="action=='add'?'新增用户':'编辑用户'"
      width="35%"
      :before-close="handleClose"
    >
      <el-form :inline="true" :model="formUser" ref="userForm" :rules="rules">
        <el-row>
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input
                v-model="formUser.name"
                placeholder="用户名"
                clearable
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-select
                v-model="formUser.gender"
                placeholder="选择性别"
                style="width: 100px"
              >
                <el-option label="男" value="1" />
                <el-option label="女" value="2" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="12"> 
            <el-form-item label="学号" prop="StuId">
              <el-input
                v-model="formUser.StuId"
                placeholder="请输入学号"
                clearable
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="班级" prop="classes">

              <el-select
                v-model="formUser.classes"
                placeholder="请选择班级"
                style="width: 120px"
              >
              <el-option v-for="item in classes"  :label="item.name" :value="item.id"/>
                <!-- <el-option label="网安四班" value="1" />
                <el-option label="网安三班" value="2" /> -->
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="12">
            <el-form-item label="密码" prop="password">
              <el-input
                v-model="formUser.password"
                placeholder="请输入密码"
                type="password"
                clearable
                show-password
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input
                v-model="formUser.email"
                placeholder="请输入邮箱(选填)"
                type="email"
                clearable
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row style="justify-content: flex-end;">
          <el-form-item>
          <el-button type="info" @click="handleCancel">取消</el-button>
          <el-button type="primary" @click="onSubmit">确定</el-button>
        </el-form-item>
        </el-row>

      </el-form>

    </el-dialog>

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
    
    <el-table :data="list" style="width: 100%" :height="500">
      <el-table-column
        v-for="item in tableLabel"
        :key="item.prop"
        :label="item.label"
        :prop="item.prop"
        :width="item.width ? item.width : 125"
      />

      <el-table-column fixed="right" label="操作" min-width="180">
        <template  #default="scope">
          <el-button type="success" size="small" @click="handleEdit(scope.row)">编辑</el-button>
          <el-button type="danger" size="small" @click="handleDelete(scope.row)">删除</el-button>
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
</template>


<script>
import { getCurrentInstance, onMounted, reactive, ref, computed } from "vue";
import { ElMessageBox,ElMessage } from "element-plus";
import md5 from 'js-md5'

export default {
  setup() {
    const { proxy } = getCurrentInstance();
    const list = ref([]);

    const dialogVisible = ref(false); //控制模态框的显示和隐藏
    const classes=ref([])
    const config = reactive({
      total: 0,
      page: 1,
      name: "",
    });
    //添加用户信息对象
    const formUser = reactive({
      name: "",
      gender: "",
      StuId:'',
      classes:'',
      password:'',
      email:null,
    });
    const formInline = reactive({
      keyword: "",
    });
    const tableLabel = reactive([
      {
        prop: "name",
        label: "姓名",
        width: 80,
      },
      {
        prop: "gender",
        label: "性别",
        width: 80,
      },
      {
        prop: "StuId",
        label: "学号",
        width: 150,
      },
      {
        prop: "classes",
        label: "班级",
        width: 120,
      },
      {
        prop: "password",
        label: "密码",
        width: 160,
      },
      {
        prop: "email",
        label: "绑定的邮箱",
        width: 190,
      },
      {
        prop: "lastTime",
        label: "最后登录时间",
        width: 180,
      },
      {
        prop: "lastIP",
        label: "最后登录IP",
        width: 180,
      },
    ]);
    const getUserData = async (config) => {
      let res = await proxy.$api.getUserData(config);
      config.total = res.count;
      list.value = res.list.map((item) => {
        item.gender = item.gender === 2 ? "女" : "男";
        item.email = item.email === null ? "未绑定邮箱" : item.email;
        return item;
      });
    };
    const changePage = (page) => {
      // console.log(page)
      config.page = page;
      getUserData(config);
    };

    const handleSearch = () => {
      config.name = formInline.keyword;
      getUserData(config);
    };

    const handleClose = (done) => {
      ElMessageBox.confirm("确定关闭吗?")
        .then(() => {
          proxy.$refs.userForm.resetFields();
          done();
        })
        .catch(() => {
          // catch error
        });
    };

    //关闭添加的弹窗，并清除所填的内容
    const handleCancel=()=>{
        dialogVisible.value = false
        proxy.$refs.userForm.resetFields();
    }
    //添加数据
    const onSubmit=async()=>{
      proxy.$refs.userForm.validate(async (valid)=>{
        if (valid) {
          if (action.value=='add') {
            // 添加时使用的api和处理过程
            let res=await proxy.$api.addUser(formUser);
            if(res){
              dialogVisible.value = false
              proxy.$refs.userForm.resetFields();
              getUserData(config);
            }
          }else{
            // 编辑用户时使用的api和处理过程
            // console.log(formUser)
            formUser.password=md5(formUser.password)
            let res=await proxy.$api.editUser(formUser);
            if(res){
              dialogVisible.value = false
              proxy.$refs.userForm.resetFields();
              getUserData(config);
            }
          }
        }else{
          ElMessage({
            message: '请输入必填项',
            type: 'error',
          })
        }
      })

      
    }

    // 校验添加表单
    const rules = reactive({
      name: [
        { required: true, message: '请填写姓名', trigger: 'blur' },
        { min: 2, message: '字数在2以上', trigger: 'blur' },
      ],
      gender:[
      { required: true, message: '请选择性别', trigger: 'blur' },
      ],
      StuId:[
      { required: true, message: '请填写学号', trigger: 'blur' },
      // { min: 2, message: '长度为2-64', trigger: 'blur' },
      ],
      classes:[
      { required: true, message: '请选择班级', trigger: 'blur' },
      ],
      password:[
      { required: true, message: '请填写密码', trigger: 'blur' },
      { min: 6,max:64, message: '长度为6-64', trigger: 'blur' },
      ],
      email:[
      { required: false, message: '请填写邮箱', trigger: 'blur' },
      ]
    })
    //区分编辑和新增的变量
    const action=ref('add')
    //编辑用户
    const handleEdit=(row)=>{
      // console.log(row)
      action.value='edit'
      dialogVisible.value = true
      getclass();
      // row.gender
      // row.email=''
      // row.classes=''
      proxy.$nextTick(()=>{
        //浅拷贝进行数据赋值
        Object.assign(formUser,row)
        Object.assign(formUser,{classes:'',gender:row.gender==='男'?'1':'2',email:row.email==='未绑定邮箱'?'':row.email})
      })
    }

    //获取全部班级
    const getclass=async()=>{
      let res=await proxy.$api.getClasses();
      // classes.value=res
      classes.value=res.list.map((item) => {
        item.value = item.id;
        item.label = item.name;
        return item;
      })
    }
    //关闭新增用户弹窗
    const handleAdd=()=>{
      getclass()
      console.log(classes)
      action.value='add'
      dialogVisible.value = true

    }

    //删除用户
    const handleDelete=(row)=>{
      ElMessageBox.confirm('确定删除吗？','再次确认',{
      type: 'warning',
    })
        .then(async() => {
          await proxy.$api.deleteUser({id:row.id});

          ElMessage({
            message: '删除成功',
            type: 'success',
          });

          getUserData(config)

        })
        .catch(() => {
        });
    }

    onMounted(() => {
      getUserData(config);
    });
    return {
      list,
      tableLabel,
      config,
      changePage,
      formInline,
      handleSearch,
      dialogVisible,
      handleClose,
      formUser,
      onSubmit,
      rules,
      handleCancel,
      action,
      handleEdit,
      handleAdd,
      handleDelete,
      classes,
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
</style>