<!--
  # 本模块为页面底部模块，展示诗句
  # 初步功能布局设计【已完成】2022
  # 主体功能构建【已完成】2022
  # 修改功能，随机展示诗句【已完成】2023-3-9
  # 功能测试【已完成】2023-3-9
  # 最后编译时间 2023-03-9
  # 存在问题【暂无】
-->
<template>
  <div id="Footer" @click="changeMood" @mouseleave="changeMood">
    <p>{{ msg }}</p>
  </div>
</template>
<script>
export default {
  name: "Footer",
  data() {
    return {
      msg: "蓦然回首，那人却在，灯火阑珊处。",
    };
  },
  methods:{
    changeMood(){
        const arr = ['蓦然回首，那人却在，灯火阑珊处','去年今日此门中，人面桃花相映红','乱石穿空，惊涛拍岸，卷起千堆雪','会当凌绝顶，一览众山小','青山隐隐水迢迢，秋尽江南草未凋']
        this.msg = arr[Math.floor(Math.random()*5)]
    }
  },
};
</script>
<style scoped>
#Footer {
  background:#ffffffae;
  padding: 6px;
  border-radius: 5px;
  width: 90%;
  height: 80px;
  margin: 20px auto;
  margin-top: 40px;
}

p {
  color: #186b6d;
  text-align: center;
  margin: 10px auto;
  letter-spacing: 2px;
  font-size: 40px;
}
</style>


