<!--
  # 本模块为页面头部模块，展示标题
  # 初步功能布局设计【已完成】2022-11
  # 主体功能构建【已完成】2022-11
  # 添加轮播图【已完成】2023-3-10
  # 功能测试【已完成】2023-3-10
  # 最后编译时间 2023-03-13
  # 存在问题【暂无】
-->
<template>
  <div id="Header">
    <div class="top-left-edition">
      <span style="color: #21b3b9; font-weight: bold">
        <i class="el-icon-star-off" style="font-size: 40px; float: left;">基于YoloV5的人流量监测系统</i>
      </span>
    </div>

    <el-carousel :interval="4000" type="card" height="160px" style="margin-right: 35px;margin-bottom: -20px;border-radius: 15px;margin-top: -10px;">
      <el-carousel-item v-for="item in 5" :key="item" style="margin:0px;background-size:100% 100%;background-attachment:fixed;border-radius: 15px;">
        <h3 class="medium" style="text-align:right;">[{{ item }}]&nbsp;</h3>
      </el-carousel-item>
    </el-carousel>
    
    <div id="word">
      <h1><i class="el-icon-time" style="font-size: 40px; float: left; margin-top: -90px;">{{dateFormat(date)}}</i></h1>
    </div>

    
  </div>
</template>
<script>
export default {
  name: "Header",
  data() {
    return {
      activeIndex: "1",
      date:new Date()
    };
  },
  created(){
    this.timer()
  },
  methods: {
    dateFormat(time) {
          var date=new Date(time);
          var year=date.getFullYear();
          var month= date.getMonth()+1<10 ? "0"+(date.getMonth()+1) : date.getMonth()+1;
          var day=date.getDate()<10 ? "0"+date.getDate() : date.getDate();
          var hours=date.getHours()<10 ? "0"+date.getHours() : date.getHours();
          var minutes=date.getMinutes()<10 ? "0"+date.getMinutes() : date.getMinutes();
          var seconds=date.getSeconds()<10 ? "0"+date.getSeconds() : date.getSeconds();
          return year+"-"+month+"-"+day+" "+hours+":"+minutes+":"+seconds;
      }
  },
  mounted() {
          let _this = this
          this.timer = setInterval(() => {
           _this.date = new Date(); 
           }, 1000)
       },
      beforeDestroy() {
       if (this.timer) {
        clearInterval(this.timer);
      }
      }
};
</script>
<style scoped>
#Header {
  background:#ffffffae;
  padding: 6px;
  border-radius: 5px;
  width: 88%;
  height: 146px;
  margin: 20px auto;
  padding: 30px 0 20px 40px;
}

#word {
  margin-top: -25px;
}

h1 {
  color: #21b4b9ad;
  letter-spacing: 2px;
  font-size: 40px;
}

.top-left-edition span i {
  float: left;
  margin-right: 10px;
}

i,
input,
label {
  vertical-align: middle;
}

i {
  border: 0;
  display: block;
  cursor: pointer;
}

.top-left-edition span {
  float: left;
  font-size: 16px;
  color: #999999;
  line-height: 24px;
  margin-right: 40px;
}

.el-carousel__item h3 {
    color: #ffffff;
    font-size: 18px;
    opacity: 0.75;
    line-height: 400px;
    margin: 0;
  }

/* 这里有个BUG，序列从3开始，暂未找到原因2023-3-10 */
.el-carousel__item:nth-child(3) {
  background-image: url('../../public/h3.jpg');
}
.el-carousel__item:nth-child(4) {
  background-image: url('../../public/h4.jpg');
}
.el-carousel__item:nth-child(5) {
  background-image: url('../../public/h6.jpg');
}
.el-carousel__item:nth-child(7) {
  background-image: url('../../public/h1.jpg');
}
.el-carousel__item:nth-child(6) {
  background-image: url('../../public/h2.jpg');
}
</style>


