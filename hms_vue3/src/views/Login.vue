<template>
  <el-row class="" style="background-color: #a78bfa; height: 100%">
    <el-col :lg="16" :md="12">
      <div class="left-div">
        <div class="text-title">欢迎</div>
        <div class="text-body">
          当你心中充满阳光，整个世界都会为你点亮。愿你每天积极向上，充满希望和力量。
        </div>
      </div>
    </el-col>
    <el-col :lg="8" :md="12" style="background-color: white">
      <div class="right-div">
        <el-form
          :model="loginForm"
          class="login-container"
          ref="userForm"
          :rules="rules"
          @keyup.native.enter="login"
        >
          <h3>系统登录</h3>
          <el-form-item prop="username">
            <el-input
              type="input"
              placeholder="请输入学号"
              v-model="loginForm.username"
              clearable
            ></el-input>
          </el-form-item>
          <el-form-item prop="pwd">
            <el-input
              type="password"
              placeholder="请输入密码"
              v-model="loginForm.pwd"
              clearable
              show-password
            ></el-input>
          </el-form-item>
          <a @click="forgetpasswd">忘记密码</a>
          <el-form-item>
            <el-button type="primary" @click="login">登录</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-col>
  </el-row>

  <el-dialog
    v-model="dialogFormVisible"
    title="修改密码"
    width="40%"
    :before-close="handleClose"
  >
    <el-form
      :inline="true"
      :model="formUser"
      ref="userinfoForm"
      :rules="userrules"
    >
      <el-row>
        <el-col :span="12">
          <el-form-item label="旧密码" prop="oldpasswd">
            <el-input
              v-model="formUser.oldpasswd"
              placeholder="输入旧密码"
              clearable
              show-password
            />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12">
          <el-form-item label="新密码" prop="newpasswd">
            <el-input
              v-model="formUser.newpasswd"
              placeholder="输入新密码"
              clearable
              show-password
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="确认新密码" prop="newtwopasswd">
            <el-input
              v-model="formUser.newtwopasswd"
              placeholder="确认新密码"
              clearable
              show-password
            />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row style="justify-content: flex-end">
        <el-form-item>
          <el-button type="info" @click="dialogFormVisible = false"
            >取消</el-button
          >
          <el-button type="primary" @click="onSubmit">确定</el-button>
        </el-form-item>
      </el-row>
    </el-form>
  </el-dialog>

  <el-dialog v-model="dialogForgetpasswd" title="忘记密码" width="500">
    <el-form
      :inline="true"
      :model="forgetform"
      ref="reforgetform"
      :rules="rulesforgetform"
    >
      <el-row>
        <el-col :span="16">
          <el-form-item label="学号" prop="stuid">
            <el-input
              v-model="forgetform.stuid"
              placeholder="输入学号"
              clearable
            />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="16">
          <el-form-item label="邮箱" prop="email">
            <el-input
              type="email"
              v-model="forgetform.email"
              placeholder="输入邮箱"
              clearable
            />
          </el-form-item>
        </el-col>
        <el-col :span="4" style="margin-left: 3px">
          <el-button
            type="primary"
            @click="sendemail"
            color="#626aef"
            :disabled="disablesendemail"
            plain
            :loading="sendemailstate"
            >{{
              disablesendemail === false ? "发送验证码" : "已发送"
            }}</el-button
          >
        </el-col>
      </el-row>
      <el-row>
        <el-col>
          <el-form-item label="验证码" prop="email_reg">
            <el-input
              v-model="forgetform.email_reg"
              placeholder="输入验证码"
              clearable
              style="width: 100px"
            />
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogForgetpasswd = false">关闭</el-button>
        <el-button type="primary" @click="subforgetpasswd">
          提交
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script>
import { reactive, ref } from "vue";
import { getCurrentInstance } from "vue-demi";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import md5 from "js-md5";
import { ElMessage,ElNotification } from "element-plus";

export default {
  setup() {
    const { proxy } = getCurrentInstance();
    const store = useStore();
    const router = useRouter();
    const loginForm = reactive({
      username: "",
      pwd: "",
    });
    const sendemailstate = ref(false);
    const disablesendemail = ref(false);
    const dialogForgetpasswd = ref(false);
    const dialogFormVisible = ref(false);

    const forgetform = reactive({
      email: "",
      stuid: "",
      email_reg: "",
    });

    const formUser = reactive({
      stuid: "",
      newpasswd: "",
      newtwopasswd: "",
      oldpasswd: "",
    });
    const loginData = { username: "", pwd: "" };

    const userrules = reactive({
      oldpasswd: [
        { required: true, message: "请填写旧密码", trigger: "blur" },
        { min: 6, message: "字数在6以上", trigger: "blur" },
      ],
      newpasswd: [
        { required: true, message: "请填写密码", trigger: "blur" },
        { min: 6, max: 32, message: "长度需为6-32", trigger: "blur" },
      ],
      newtwopasswd: [
        { required: true, message: "请再次填写密码", trigger: "blur" },
        { min: 6, max: 32, message: "长度需为6-32", trigger: "blur" },
        {
          validator: (rule, value, callback) => {
            //自定义校验器
            if (value !== formUser.newpasswd) {
              callback(new Error("两次输入密码不一致!"));
            } else {
              callback();
            }
          },
          trigger: "blur",
        },
      ],
    });
    // 校验添加表单
    const rules = reactive({
      username: [
        { required: true, message: "请填写学号", trigger: "blur" },
        { min: 2, max: 32, message: "学号长度需为6-32", trigger: "blur" },
      ],
      pwd: [
        { required: true, message: "请填写密码", trigger: "blur" },
        { min: 6, max: 64, message: "长度需为6-64", trigger: "blur" },
      ],
    });

    // 邮箱校验
    const validate_email = (rule, value, callback) => {
      var emailRegExp = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/;
      var emailRegExp1 =
        /^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/;
      if (
        (!emailRegExp.test(value) && value != "") ||
        (!emailRegExp1.test(value) && value != "")
      ) {
        callback(new Error("请输入有效邮箱格式！"));
      } else {
        callback();
      }
    };

    //校验忘记密码信息
    const rulesforgetform = reactive({
      email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
          { validator: validate_email, trigger: ['blur'] }
        ],
      email_reg: [
      { required: true, message: '请输入验证码', trigger: 'blur' },
      { min: 6,max:6, message: '长度为6', trigger: 'blur' },
      ], 
      stuid: [
        { required: true, message: "请填写学号", trigger: "blur" },
        { min: 2, max: 32, message: "学号长度需为6-32", trigger: "blur" },
      ],

      },

    );

    const login = async () => {

      proxy.$refs.userForm.validate(async (valid) => {
        if (valid) {
          loginData.password = md5(loginForm.pwd);
          loginData.username = loginForm.username;
          const login_info = await proxy.$api.Login(loginData);
          // console.log(login_info)
          if (login_info.token === "") {
            ElMessage({
              showClose: true,
              message: login_info.msg,
              type: "error",
            });
            dialogFormVisible.value = true;
            formUser.stuid = loginForm.username;
          } else {
            store.commit("setToken", login_info.token);
            store.commit("setUsername", login_info.username);

            if (login_info.token != "") {
              let menu;
              if (_isMobile()){
                menu = await proxy.$api.getmenu({phone:true});
              }else{
                menu = await proxy.$api.getmenu({phone:false});
              }
              store.commit("setMenu", menu);
              store.commit("addMenu", router);
              router.push({ name: "home" });
            }
          }
        }
      });
      // console.log(loginForm)
    };

    const handleClose = () => {
      ElMessageBox.confirm("确定关闭吗?")
        .then(() => {
          proxy.$refs.userinfoForm.resetFields();
          dialogFormVisible.value = false;
          done();
        })
        .catch(() => {
          // catch error
        });
    };
    const onSubmit = async () => {
      
      proxy.$refs.userinfoForm.validate(async (valid) => {
        if (valid) {
          const res = await proxy.$api.LoginAlterpasswd({
            stuid: formUser.stuid,
            oldpasswd: md5(formUser.oldpasswd),
            newpasswd: md5(formUser.newpasswd),
            newtwopasswd: md5(formUser.newtwopasswd),
          });
          if (res.msg === "success") {
            ElMessage({
              message: "修改成功，请使用新密码登录",
              type: "success",
              showClose: true,
            });
          }
          dialogFormVisible.value = false;
          proxy.$refs.userForm.resetFields();
        }
      });
    };

    const forgetpasswd = async () => {
      dialogForgetpasswd.value = true;
    };

    const sendemail = async () => {
      let email=forgetform.email
      let stuid=forgetform.stuid
      sendemailstate.value=true
      var verify = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/;
      if (!verify.test(email)) {
      sendemailstate.value=false
        // console.log(email)
        ElMessage.error('邮箱格式错误')
        return
      }
      if (stuid===''){
        sendemailstate.value=false
        ElMessage.error('请填写学号')
        return
      }
      let res=await proxy.$api.SendForgetEmailMsg({email:email,stuid:stuid})
      if (res.msg==='ok'){
        sendemailstate.value=false
        disablesendemail.value=true
        ElMessage.success("验证码已发送")
      }else{
        sendemailstate.value=false
        disablesendemail.value=false
            ElNotification({
              title: '⚠警告',
              message: res.msg,
              type: 'error',
            })
          }
    };

    const _isMobile=()=> {
      let flag = navigator.userAgent.match(/(phone|pad|pod|iPhone|iPod|ios|iPad|Android|Mobile|BlackBerry|IEMobile|MQQBrowser|JUC|Fennec|wOSBrowser|BrowserNG|WebOS|Symbian|Windows Phone)/i)
      if (flag!=null){
        return true;
      }
      return false;
    }

    const subforgetpasswd=async()=>{
      // dialogForgetpasswd = false

      
      proxy.$refs.reforgetform.validate(async (valid) => {
        if (valid) {
          let res=await proxy.$api.EmailToAlterpasswd(forgetform)
          if(res.msg==="ok"){
            ElMessage.success('密码初始化成功')
            ElNotification({
              title: '密码初始化成功',
              message: '默认密码为你的名字的拼音',
              type: 'success',
            })

            if (res.token != "") {
              store.commit("setToken", res.token);
              store.commit("setUsername", res.username);
              const menu = await proxy.$api.getmenu();
              store.commit("setMenu", menu);
              store.commit("addMenu", router);
              router.push({ name: "home" });
            }

          }       

        }
      
      })
    }

    return {
      loginForm,
      login,
      rules,
      formUser,
      userrules,
      dialogFormVisible,
      handleClose,
      onSubmit,
      forgetpasswd,
      dialogForgetpasswd,
      forgetform,
      sendemail,
      sendemailstate,
      disablesendemail,
      rulesforgetform,
      subforgetpasswd,

    };
  },
  // mounted() {
  //     document.title = '登录页面';
  // }
};
</script>

<style lang="less" scoped>
.right-div {
  margin: 0 auto;
  margin-top: 40%;
  width: 50%;
  position: relative;
  h3 {
    font-size: 25px;
    margin-bottom: 30px;
    text-align: center;
  }
  .el-button {
    margin-top: 10px;
  }
  a {
    font-size: 14px;
    color: rgb(113, 114, 114);
    text-decoration: underline;
    // margin-right:0px;
    // right:0px;
    float: right;
  }
  a:hover {
    color: black;
    cursor: pointer;
  }
}
.left-div {
  margin-left: 30px;
  font-family: 幼圆;
  font-weight: bold;
}
.text-title {
  font-size: 30px;
  margin-top: 30%;
}
.text-body {
  margin-top: 10px;
  font-size: 18px;
}
</style>