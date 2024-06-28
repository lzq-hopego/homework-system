<template>
  <el-row class="home" :gutter="20">
    <el-col :span="8" >
      <el-card shadow="hover">
        <div class="user">
          <img :src="imageUrl" alt="" />
          <div class="user-info">
            <p class="name">{{ userinfo.name }}</p>
            <p class="role">{{userinfo.identity}}</p>
          </div>
        </div>
        <div class="login-info">
          <p>本次登录时间:<span>{{userlog.nowdate}}</span></p>
          <p>本次登录的IP:<span>{{userlog.ip}}</span></p>
        </div>
      </el-card>

    </el-col>
    <el-col :span="16">
      <div class="num">
        <el-card
          :body-style="{ display: 'flex', padding: 0 }"
          v-for="item in countData"
          :key="item.name"
        >
          <component
            class="icons"
            :is="item.icon"
            :style="{ background: item.color }"
          />
          <div class="detail">
            <p class="num">{{ item.value }}</p>
            <p class="txt">{{ item.name }}</p>
          </div>
        </el-card>
      </div>

      <el-card style="height: 280px">
        <div ref="echart" style="height: 280px"></div>
      </el-card>
      <el-carousel indicator-position="outside">
        <el-carousel-item v-for="item in msgData" :key="item.title">
          <div class="text_msg">
            <el-card shadow="hover">
              <p class="title">{{ item.title }}</p>
              <div class="date_time">
                <span class="date_line"></span>
                <span class="time">{{ item.time }}</span>
              <span class="date_line"></span>
              </div>
              <p class="msg_body">{{ item.msg }}</p>
              <p class="msg_bottom">{{ item.manager }} </p>
            
            </el-card>
          </div>
        </el-carousel-item>
      </el-carousel>
    </el-col>
  </el-row>
</template>

<script>
import { getCurrentInstance, onMounted, ref } from "vue";
import { useStore } from "vuex";
import * as echarts from "echarts";
import configs from "../config";

export default {
  setup() {
    const store = useStore();
    const { proxy } = getCurrentInstance();
    const tableData = ref([]);
    const countData = ref([]);
    const msgData = ref([]);
    const imageUrl = ref(
      configs.baseApi + "/user/getUserAvatar/?usertoken=" + store.state.token
    );
    const userlog=ref({
      ip:'',
      nowdate:''
    })
    const userinfo=ref({
      name:'',
      identity:''
    })
    const tableLable = {
      name: "课程名",
      todayBuy: "今日购买",
      monthBuy: "本月购买",
      totalBuy: "总购买",
    };
    const option = {
      title: {
        text: "提交统计",
      },
      xAxis: {
        type: "category",
        boundaryGap: false,
        data: [],
      },
      yAxis: {
        type: "value",
      },
      series: [],
    };
    const getTableData = async () => {
      // await axios.get('https://www.fastmock.site/mock/e57abff016d8de66e9cd869e98cc05bc/api/home/getData').then((res)=>{
      //   console.log(res)
      // })
      let res = await proxy.$api.getTableData();
      tableData.value = res.tableData;
    };
    const getCountData = async () => {
      let res = await proxy.$api.getCountData();
      countData.value = res;
    };
    const getCharData = async () => {
      let res = await proxy.$api.getEchartsData();
      option.xAxis.data = res.orderData.date;
      msgData.value=res.messageData;
      let data = {
        data: res.orderData.data,
        type: "line",
        smooth: true,
      };
      option.series[0] = data;

      //   console.log(option.value.series.data);
      //在dom数中渲染
      let hEcharts = echarts.init(proxy.$refs["echart"]);
      hEcharts.setOption(option);
    };
    const getUserLog=async()=>{
      let res = await proxy.$api.getuserlog()
      userlog.value.nowdate=res.nowdatetime
      userlog.value.ip=res.nowip
      
    }
    const getUserInfo=async()=>{
      let res = await proxy.$api.getuserinfo()

      userinfo.value.name=res.name
      userinfo.value.identity=res.identity
    }
    onMounted(() => {
      // getTableData();
      getUserInfo();
      getCountData();
      getCharData();
      getUserLog();
      
    });
    return {
      tableData,
      tableLable,
      countData,
      msgData,
      userlog,
      imageUrl,
      userinfo,
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

// .el-carousel__item h3 {
//   display: flex;
//   color: #475669;
//   opacity: 0.75;
//   line-height: 300px;
//   margin: 0;
// }

// .el-carousel__item:nth-child(2n) {
//   background-color: #99a9bf;
// }

// .el-carousel__item:nth-child(2n + 1) {
//   background-color: #d3dce6;
// }
.el-carousel {
  border-radius: 5px;
  height: 256px;
}
.text_msg{
  height: 80%;
  width: 80%;
  margin:0 auto;
  margin-top: 30px;
  font-family: 幼圆;
  .title {
    font-size: 30px;
    font-weight:bold;
    text-align: center;
    margin-bottom: 10px;
  }
  
 .el-card{
  height: 80%;
 }
  .msg_body{
    margin: auto 30px;
    font-size: 15px;
    line-height: 20px;
    text-indent:2em;
  }
  .msg_bottom{
    font-weight:bold;
    text-align: right;
    position: relative;
    top:5vh;
  }
  .date_time{
    display: flex;
    justify-content: center;
  }
  .time{
    color: #999;
  }
  .date_line{
      margin: 0px 5px;
      position: relative;
      top:7px;
      height: 1px;
      width: 16px;
      background-color: #bebebe;
    }
}
</style>