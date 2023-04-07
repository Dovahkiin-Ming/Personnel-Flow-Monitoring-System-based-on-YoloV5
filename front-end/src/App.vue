<!--
  # 最后编译时间 2023-03-06
-->
<template>
  <div id="app">
    <app-header></app-header>
    <app-content></app-content>
    <app-camera></app-camera>
    <app-footer></app-footer>
  </div>
</template>

<script>
import Header from "./components/Header";
import Footer from "./components/Footer";
import Content from "./components/Content";
import Camera from "./components/Camera";
export default {
  name: "专治近视眼",
  data() {
    return {};
  },
  components: {
    "app-header": Header,
    "app-footer": Footer,
    "app-content": Content,
    //"app-camera": Camera, //仅作技术验证，2023-3-6废弃
  },
  methods: {},
};
</script>

<style scope="this api replaced by slot-scope in 2.5.0+">
</style>
