<template>
  <el-row class="home" :gutter="20">
    <el-col :span="8">
      <el-card shadow="hover">
        <div class="user">
          <!-- <img src="../../assets/images/user.jpg" alt="" /> -->

          <el-upload
            class="avatar-uploader"
            :action="uploadAvatar"
            :show-file-list="false"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload"
          >
            <img v-if="imageUrl" :src="imageUrl" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
          <div class="user-info">
            <p class="name">{{ userinfo.name }}</p>
            <p class="role">{{userinfo.identity}}</p>
          </div>
        </div>
        <div class="login-info">
          <p>
            本次登录时间:<span>{{ userlog.nowdate }}</span>
          </p>
          <p>
            本次登录的IP:<span>{{ userlog.ip }}</span>
          </p>
        </div>
      </el-card>
    </el-col>
    <el-col :span="8">
      <el-card shadow="hover">
        <div class="user">
          <div class="user-info">
            <p class="name">密码</p>
          </div>
        </div>
        <div class="login-info">
          <p>************</p>
          <el-button type="primary" plain @click="changepasswd">更改</el-button>
        </div>
      </el-card>
    </el-col>

    <el-col :span="8">
      <el-card shadow="hover">
        <div class="user">
          <div class="user-info">
            <p class="name">邮箱</p>
          </div>
        </div>
        <div class="login-info">
          <p>{{ UserEmail }}</p>
          <el-button v-if="UserEmail === '未绑定邮箱'" type="primary" plain @click="dialogVisibleEmail = true"
            >添加</el-button
          >
          <el-button v-else type="primary" plain @click="dialogVisibleEmail = true">修改</el-button>
        </div>
      </el-card>
    </el-col>
  </el-row>


  <el-dialog
    v-model="dialogFormVisible"
    title="修改密码"
    width="40%"
    :before-close="handleClose"
  >
    <el-form :inline="true" :model="formUser" ref="userForm" :rules="rules">
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
          <el-button type="info" @click="dialogFormVisible=false">取消</el-button>
          <el-button type="primary" @click="onSubmit">确定</el-button>
        </el-form-item>
      </el-row>
    </el-form>
  </el-dialog>


  <el-dialog
    v-model="dialogVisibleEmail"
    :title='UserEmail === "未绑定邮箱"?"添加邮箱":"修改邮箱"'
    width="500"
  >
    <el-form :inline="true" :model="formEmail" ref="reformEmail" :rules="rulesformEmail">
        <el-row>
          <el-col :span="16">
            <el-form-item label="邮箱" prop="email">
              <el-input
                type="email"
                v-model="formEmail.email"
                placeholder="输入邮箱"
                clearable
              />
              
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-button type="primary" @click="sendemail"  :loading-icon="Eleme" color="#626aef" :dark="isDark" :disabled="disablesendemail" plain :loading="sendemailstate">{{disablesendemail===false?"发送验证码":'已发送'}}</el-button>
          </el-col>
        </el-row>
        <el-row>
          <el-col>
            <el-form-item label="验证码" prop="email_msg">
              <el-input
                v-model="formEmail.email_msg"
                placeholder="输入验证码"
                clearable
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row style="justify-content: flex-end">
        <el-form-item>
          <el-button type="info" @click="dialogVisibleEmail=false">取消</el-button>
          <el-button type="primary" @click="alteremail">确定</el-button>
        </el-form-item>
      </el-row>
  </el-form>
  </el-dialog>

  
</template>



<script>
import { getCurrentInstance, onMounted, ref, reactive } from "vue";
import { ElMessage,ElMessageBox } from "element-plus";
import configs from "../../config";
import { useStore } from "vuex";

export default {
  setup() {
    const store = useStore();
    const { proxy } = getCurrentInstance();
    const dialogVisibleEmail=ref(false)
    const sendemailstate=ref(false);
    const disablesendemail=ref(false);
    const imageUrl = ref(
      configs.baseApi + "/user/getUserAvatar/?usertoken=" + store.state.token
    );
    const uploadAvatar = ref(
      configs.baseApi + "/user/alterUserAvatar/?usertoken=" + store.state.token
    );
    const dialogFormVisible = ref(false);
    const formUser = reactive({
      oldpasswd: "",
      newpasswd: "",
      newtwopasswd: "",
    });

    const formEmail=reactive({
      email:"",
      email_msg:''
    })

    // 邮箱校验
    const validate_email = (rule, value, callback) => {
      var emailRegExp = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/;
      var emailRegExp1 = /^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/;
      if ((!emailRegExp.test(value) && value != '') || (!emailRegExp1.test(value) && value != '')) {
        callback(new Error('请输入有效邮箱格式！'));
      } else {
        callback();
      }
    };
    
    const rulesformEmail=reactive({
      email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
          { validator: validate_email, trigger: ['blur'] }
        ],
      email_msg: [
      { required: true, message: '请输入验证码', trigger: 'blur' },
      { min: 6,max:6, message: '长度为6', trigger: 'blur' },
      ]
      },
    )


    const userinfo=ref({
      name:'',
      identity:''
    })

    const userlog = ref({
      ip: "",
      nowdate: "",
    });

    // 校验添加表单
    const rules = reactive({
      oldpasswd: [
        { required: true, message: "请填写旧密码", trigger: "blur" },
        { min: 6, message: "字数在6以上", trigger: "blur" },
      ],
      newpasswd: [
        { required: true, message: "请填写新密码", trigger: "blur" },
        { min: 6, message: "字数在6以上", trigger: "blur" },
        
      ],
      newtwopasswd: [
        { required: true, message: "请确认密码", trigger: "blur" },
        { min: 6, message: "字数在6以上", trigger: "blur" },
        {validator: (rule, value, callback) => {//自定义校验器
          if (value !== formUser.newpasswd) {
                callback(new Error('两次输入密码不一致!'))
              } else {
                callback()
              }
            }, trigger: "blur"}
      ],
    });

    

    const UserEmail = ref("");

    const getUserEmail =async () => {
      let res=await proxy.$api.getUserEmail()
      if ((res.email===null)||(res.email==="")){
        UserEmail.value='未绑定邮箱'
      }else{
        UserEmail.value=res.email
      }
    };

    const getUserLog = async () => {
      let res = await proxy.$api.getuserlog();
      userlog.value.nowdate = res.nowdatetime;
      userlog.value.ip = res.nowip;
    };

    const handleAvatarSuccess = (response, uploadFile) => {
      imageUrl.value = URL.createObjectURL(uploadFile.raw);
    };

    const beforeAvatarUpload = (rawFile) => {
      console.log(rawFile.type);
      if (rawFile.type !== "image/jpeg") {
        ElMessage.error("图片必须是jpg格式");
        return false;
      } else if (rawFile.size / 1024 / 1024 > 1) {
        ElMessage.error("头像不得大于1MB");
        return false;
      }
      return true;
    };

    const changepasswd = () => {
      dialogFormVisible.value = true;
    };

    const onSubmit = async () => {
      proxy.$refs.userForm.validate(async (valid) => {
        if (valid) {
          let res=await proxy.$api.alterstupasswd(formUser)
          if (res){
            dialogFormVisible.value=false
          }
        } 
        
      });
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

    const getUserInfo=async()=>{
      let res = await proxy.$api.getuserinfo()

      userinfo.value.name=res.name
      userinfo.value.identity=res.identity
    }


    const alteremail=async()=>{
      proxy.$refs.reformEmail.validate(async (valid) => {
        if (valid) {
          // console.log(formEmail.email)
          let res=await proxy.$api.AddEmail(formEmail)
          console.log(res)
          if (res.state==='ok'){
            dialogVisibleEmail.value=false
            ElMessage.success('邮箱修改成功')
            getUserEmail()
          }
        } 
        
      });
    }

    const sendemail=async()=>{
      let email=formEmail.email
      sendemailstate.value=true

      var verify = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/;
      if (!verify.test(email)) {
        sendemailstate.value=false
        // console.log(email)
        ElMessage.error('邮箱格式错误')
        return
      }
      let res=await proxy.$api.SendEmailMsg({email:email})

      if (res.state){
        sendemailstate.value=false
        disablesendemail.value=true
        ElMessage.success("验证码已发送")

      }
    }

    onMounted(() => {
      getUserLog();
      getUserEmail();
      getUserInfo();
    });
    return {
      userlog,
      UserEmail,
      imageUrl,
      beforeAvatarUpload,
      handleAvatarSuccess,
      uploadAvatar,
      changepasswd,
      dialogFormVisible,
      formUser,
      rules,
      onSubmit,
      handleClose,
      userinfo,
      dialogVisibleEmail,
      formEmail,
      rulesformEmail,
      alteremail,
      sendemail,
      sendemailstate,
      disablesendemail,






      
    };
  },
};
</script>




<style lang="less" scoped>
.home {
  .user {
    display: flex;
    align-items: center;
    border-bottom: 1px solid #ccc;
    margin-bottom: 20px;
    padding-bottom: 20px;
    font-family: 幼圆 blod;
    img {
      width: 150px;
      height: 150px;
      border-radius: 50%;
      margin-right: 40px;
    }
    .name {
      font-size: 38px;
      margin-bottom: 10px;
    }
    .role {
      font-size: 20px;
    }
  }
  .login-info {
    p {
      line-height: 30px;
      font-size: 14px;
      color: #999;
      span {
        color: #666;
        margin-left: 60px;
      }
    }
  }
}
.num {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  .el-card {
    width: 32%;
    margin-bottom: 20px;
  }
  .icons {
    width: 80px;
    height: 80px;
    font-size: 30px;
    text-align: center;
    line-height: 80px;
    color: white;
  }
  .detail {
    margin-left: 15px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    .num {
      margin: 0 auto;
      font-size: 35px;
      margin-bottom: 10px;
    }
    .txt {
      font-size: 14px;
      text-align: center;
      color: #999;
    }
  }
}

.el-carousel {
  border-radius: 5px;
  height: 256px;
}
.text_msg {
  height: 80%;
  width: 80%;
  margin: 0 auto;
  margin-top: 30px;
  font-family: 幼圆;
  .title {
    font-size: 30px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 10px;
  }

  .el-card {
    height: 80%;
  }
  .msg_body {
    margin: auto 30px;
    font-size: 15px;
    line-height: 20px;
    text-indent: 2em;
  }
  .msg_bottom {
    font-weight: bold;
    text-align: right;
    position: relative;
    top: 5vh;
  }
  .date_time {
    display: flex;
    justify-content: center;
  }
  .time {
    color: #999;
  }
  .date_line {
    margin: 0px 5px;
    position: relative;
    top: 7px;
    height: 1px;
    width: 16px;
    background-color: #bebebe;
  }
}

.avatar-uploader .el-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
}
</style>