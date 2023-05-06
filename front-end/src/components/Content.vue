<!--
  # 本模块为前端核心模块，展示摄像头和处理前后图片画面，展示各种功能按钮，展示计算后的数据
  # 初步功能布局设计【已完成】2022
  # 主体功能构建【已完成】2023-3-13
  # 数据库构建【已完成】2023-3-12
  # 功能测试【已完成】2023-3-13
  # 代码优化【正在进行】
  # 最后编译时间 2023-03-13
  # 存在问题【暂无】
-->
<template>
  <div id="Content">
    <el-backtop target=".page-component__scroll .el-scrollbar__wrap" :bottom="100">
  </el-backtop>
    <el-dialog
      title="正在识别中"
      :visible.sync="dialogTableVisible"
      :show-close="false"
      :close-on-press-escape="false"
      :append-to-body="true"
      :close-on-click-modal="false"
      :center="true"
    >
      <el-progress :percentage="percentage"></el-progress>
      <span slot="footer" class="dialog-footer">请稍等哦~~~</span>
    </el-dialog>

    <div id="CT">

      <el-tabs v-model="activeName">
          <div id="CT_image">
            <el-card
              style="border-radius: 15px;"
            >
            <div class="camera_outer">
              <video id="videoCamera" :width="videoWidth" :height="videoHeight" autoplay style="border-radius: 8px;width: 456px;height: 320px;margin-bottom: -30px;margin-top: -32px;"></video>
              <canvas style="display:none;" id="canvasCamera" :width="videoWidth" :height="videoHeight" ></canvas>
              <!-- <div v-if="imgSrc" class="img_bg_camera">
                <img :src="imgSrc" alt="" class="tx_img">
              </div> -->
            </div>
              <div class="img_info_1" style="border-radius: 8px;margin-bottom: 20px;">
                <span style="color: white; letter-spacing: 8px">相机画面</span>
              </div>
              <div class="demo-image__preview1">
                <div
                  v-loading="loading"
                  element-loading-text="上传图片中"
                  element-loading-spinner="el-icon-loading"
                >
                  <el-image
                    :src="url_1"
                    class="image_1"
                    :preview-src-list="srcList"
                    style="border-radius: 8px 8px 8px 8px"
                  >
                    <div slot="error">
                      <div slot="placeholder" class="error">
                        <!-- <el-button
                          style="margin-left: 35px"
                          v-show="showbutton"
                          type="primary"
                          icon="el-icon-upload"
                          class="download_bt"
                          v-on:click="true_upload"
                        >
                          点击上传图像
                          <input
                            ref="upload"
                            style="display: none"
                            name="file"
                            type="file"
                            @change="update"
                          />
                        </el-button> -->
                      </div>
                    </div>
                  </el-image>
                </div>
                <div class="img_info_1" style="border-radius: 8px;margin-bottom: 20px;">
                  <span style="color: white; letter-spacing: 8px">原始图像</span>
                </div>
              </div>
              <div class="demo-image__preview2">
                <div
                  v-loading="loading"
                  element-loading-text="处理中,请耐心等待"
                  element-loading-spinner="el-icon-loading"
                >
                  <el-image
                    :src="url_2"
                    class="image_1"
                    :preview-src-list="srcList1"
                    style="border-radius: 8px;margin-left: -2px;width: 456px;"
                  >
                    <div slot="error">
                      <div slot="placeholder" class="error">{{ wait_return }}</div>
                    </div>
                  </el-image>
                </div>
                <div class="img_info_1" style="border-radius: 8px; margin-bottom: 20px;margin-left: -2px;">
                  <span style="color: white; letter-spacing: 8px">检测结果</span>
                </div>
              </div>
            </el-card>
            <!-- 试验了一下内嵌外部网站时钟 -->
            <!-- <div>
              <iframe height="400" style="border-radius: 18px; width: 100%; margin-top: 25px;" src="https://tools.miku.ac/screen_clock/" frameborder="0" allowfullscreen></iframe>
            </div> -->
          </div>
      </el-tabs>

      <div class="card_imginfo">
        <!-- 卡片放置表格 -->
        <el-card style="border-radius: 15px">
          <div slot="header" class="clearfix">
            <span>检测按钮：</span>
            
            <el-button
              style="border-radius: 8px;margin-left: 35px"
              type="primary"
              icon="el-icon-upload"
              class="download_bt"
              v-on:click="true_upload2"
            >
              本地上传
              <input
                ref="upload2"
                style="display: none"
                name="file"
                type="file"
                @change="update"
              />
            </el-button>
            <el-button 
            style="border-radius: 8px;margin-left: 25px"
              v-show="showbutton"
              type="primary"
              icon="el-icon-view"
              class="download_bt"
              @click="getCompetence()"
              >开启摄像头</el-button>
            <el-button 
            style="border-radius: 8px;margin-left: 25px"
              v-show="!showbutton"
              type="primary"
              icon="el-icon-error"
              class="download_bt"
              @click="stopNavigator()"
              >关闭摄像头</el-button>
            <el-button 
              style="border-radius: 8px;margin-left: 25px"
              v-show="!showbutton"
              type="primary"
              icon="el-icon-camera"
              class="download_bt"
              @click="setImage()"
              >拍照上传</el-button>
            <el-button 
              style="border-radius: 8px;margin-left: 25px"
              v-show="!showbutton"
              type="primary"
              icon="el-icon-cpu"
              class="download_bt"
              @click="setImageAuto()"
              >自动化监测</el-button>
            <el-switch
              :disabled="switchdisvalue"
              style="display: block;float: right;margin-top: 6px;"
              v-show="!showbutton"
              v-model="switchvalue"
              active-color="#13ce66"
              inactive-color="#ff4949"
              ></el-switch>

          </div>
          <el-tabs v-model="activeName">
            <div>
              <span>当前人流量：</span>
              <el-button 
              style="border-radius: 8px;margin-left: 20px;margin-right: 20px;"
              type="primary"
              icon="el-icon-user"
              class="download_bt"
              >{{person_num}}</el-button>
              <span>设定人流量峰值：</span>
              <!--<el-input-number v-model="numAlert" @change="handleChange" :min="0" :max="100" label="警报人数"></el-input-number>-->
              <el-slider
                style="margin-left: 5px;width: 50%;float: right;"
                v-model="numAlert"
                show-input
                max="300">
              </el-slider>
            </div>
          </el-tabs>
          <el-tabs v-model="activeName">
            <el-table
              :data="feature_list"
              style="width: 700px; text-align: center"
              v-loading="loading"
              element-loading-text="数据正在处理中，请耐心等待"
              element-loading-spinner="el-icon-loading"
              lazy
            >
              <el-table-column label="目标类型及编号" width="220px">
                <template slot-scope="scope">
                  <span>{{ scope.row[2] }}</span>
                </template>
              </el-table-column>
              <el-table-column label="目标大小" width="220px">
                <template slot-scope="scope">
                  <span>{{ scope.row[0] }}</span>
                </template>
              </el-table-column>
              <el-table-column label="置信度" width="220px">
                <template slot-scope="scope">
                  <span>{{ scope.row[1] }}</span>
                </template>
              </el-table-column>
            </el-table>
          </el-tabs>
          <div>
            <h3 style="float: left;">查看历史监测数据，以JSON格式输出</h3>
            <el-button 
              style="border-radius: 8px;margin-left: 25px;margin-top: 15px;"
              type="primary"
              icon="el-icon-connection"
              class="download_bt"
              @click="showDataSummarize()"
              >查看历史监测概览</el-button>
            <el-button 
              style="border-radius: 8px;margin-left: 25px;margin-top: 15px;"
              type="primary"
              icon="el-icon-coin"
              class="download_bt"
              @click="showDataDetail()"
              >查看历史监测明细</el-button>
            <json-viewer
              style="margin-top: 20px;"
              :value="jsonData"
              :expand-depth="8"
              boxed
              sort
            ></json-viewer>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { randomBytes } from "crypto";
import JsonViewer from "vue-json-viewer";
/* import CameraVue from './Camera.vue';测试用，废弃
 */
export default {
  name: "Content",
  components: {
    JsonViewer,
  },
  data() {
    return {
      numAlert: 20,
      person_num: 0,
      //静态图片上传下载所需参数
      server_url: "http://127.0.0.1:5003",
      activeName: "first",
      active: 0,
      centerDialogVisible: true,
      url_1: "",
      url_2: "",
      textarea: "",
      srcList: [],
      srcList1: [],
      feature_list: [],
      feature_list_1: [],
      feat_list: [],
      jsonData: {}, // 定义一个空对象
      url: "",
      visible: false,
      wait_return: "等待上传",
      wait_upload: "等待上传",
      loading: false,
      table: false,
      isNav: false,
      showbutton: true,
      percentage: 0,
      fullscreenLoading: false,
      opacitys: {
        opacity: 0,
      },
      dialogTableVisible: false,

      //摄像头截取所需参数
      videoWidth: 1280,
      videoHeight: 720,
      imgSrc: '',
      thisCancas: null,
      thisContext: null,
      thisVideo: null,

      camerafilename : "",

      //设置开关默认参数
      switchvalue: false,
      switchdisvalue: true,

      //设置自动模式定时器
      intervalId: null, // 定时器变量
      intervalTime: 5000, // 每隔30秒执行一次

      setImageAutoBoolean: true,
    };
  },
  created: function () {
    document.title = "基于YoloV5的人流量监测系统";
  },
  methods: {
    true_upload() {
      this.$refs.upload.click();
    },
    true_upload2() {
      this.$refs.upload2.click();
    },
    next() {
      this.active++;
    },
    handleChange(value) {
        console.log(value);
    },

    // 获得目标文件
    getObjectURL(file) {
      var url = null;
      if (window.createObjcectURL != undefined) {
        url = window.createOjcectURL(file);
      } else if (window.URL != undefined) {
        url = window.URL.createObjectURL(file);
      } else if (window.webkitURL != undefined) {
        url = window.webkitURL.createObjectURL(file);
      }
      return url;
    },
    // 上传文件
    update(e) {
      //初始化值
      this.percentage = 0;
      this.dialogTableVisible = true;
      this.url_1 = "";
      this.url_2 = "";
      this.srcList = [];
      this.srcList1 = [];
      this.wait_return = "";
      this.wait_upload = "";
      this.feature_list = [];
      this.feat_list = [];
      this.fullscreenLoading = true;
      this.loading = true;
      //this.showbutton = false;
      this.person_num = 0;

      let file = e.target.files[0];
      this.url_1 = this.$options.methods.getObjectURL(file);
      let param = new FormData(); //创建form对象
      param.append("file", file, file.name); //通过append向form对象添加数据
      var timer = setInterval(() => {
        this.myFunc();
      }, 30);
      let config = {
        headers: { "Content-Type": "multipart/form-data" },
      }; //添加请求头
      axios
        .post(this.server_url + "/upload", param, config)
        .then((response) => {
          this.percentage = 100;
          clearInterval(timer);
          this.url_1 = response.data.image_url;
          this.srcList.push(this.url_1);
          this.url_2 = response.data.draw_url;
          this.srcList1.push(this.url_2);
          this.fullscreenLoading = false;
          this.loading = false;

          this.feat_list = Object.keys(response.data.image_info);

          for (var i = 0; i < this.feat_list.length; i++) {
            response.data.image_info[this.feat_list[i]][2] = this.feat_list[i];
            this.feature_list.push(response.data.image_info[this.feat_list[i]]);
            this.person_num++;//人数加一
          }

          if (this.person_num < this.numAlert) {
            this.noticeSafe();
          } else {
            this.noticeAlert();
          }

          this.feature_list.push(response.data.image_info);
          this.feature_list_1 = this.feature_list[0];
          this.dialogTableVisible = false;
          this.percentage = 0;
          this.notice1();
        });
    },
    myFunc() {
      if (this.percentage + 33 < 99) {
        this.percentage = this.percentage + 33;
      } else {
        this.percentage = 99;
      }
    },
    drawChart() {},
    notice1() {
      const h = this.$createElement;
      this.$notify({
        title: "检测完成",
        message: "点击图片可以查看大图",
        position: 'bottom-right',
        duration: 3000, //毫秒，消失时间
        type: "success",
      });
    },
    noticeAlert() {
      this.$confirm('人流量已超越峰值，请立即处理', '警告', {
          confirmButtonText: '确定',
          cancelButtonText: '稍后',
          type: 'warning',
          showClose: false,
          closeOnClickModal: false,
          center: true
        }).then(() => {
          this.$message({
            type: 'success',
            center: true,
            message: '处理完毕，请继续监测!'
          });
        }).catch(() => {
          this.$message({
            type: 'error',
            center: true,
            showClose: true,
            duration: 0,
            message: '事态紧急，请尽快处理！'
          });
        });
    },
    noticeSafe() {
      const h = this.$createElement;
      this.$notify({
        title: "人数正常",
        message: h('i', { style: 'color: green'},"人数正常，您不用在意"),
        duration: 2000, //毫秒，消失时间
        type: "success",
      });
    },

    getCompetence () {
        this.showbutton = false;
        var _this = this
        this.thisCancas = document.getElementById('canvasCamera')
        this.thisContext = this.thisCancas.getContext('2d')
        this.thisVideo = document.getElementById('videoCamera')
        // this.switchdisvalue = !this.switchdisvalue //必须开启摄像头才可以调整自动模式【功能更新，开关仅作为示意】
        // 旧版本浏览器可能根本不支持mediaDevices，我们首先设置一个空对象
        if (navigator.mediaDevices === undefined) {
          navigator.mediaDevices = {}
        }
        // 一些浏览器实现了部分mediaDevices，我们不能只分配一个对象
        // 使用getUserMedia，因为它会覆盖现有的属性。
        // 这里，如果缺少getUserMedia属性，就添加它。
        if (navigator.mediaDevices.getUserMedia === undefined) {
          navigator.mediaDevices.getUserMedia = function (constraints) {
            // 首先获取现存的getUserMedia(如果存在)
            var getUserMedia = navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.getUserMedia
            // 有些浏览器不支持，会返回错误信息
            // 保持接口一致
            if (!getUserMedia) {
              return Promise.reject(new Error('getUserMedia is not implemented in this browser'))
            }
            // 否则，使用Promise将调用包装到旧的navigator.getUserMedia
            return new Promise(function (resolve, reject) {
              getUserMedia.call(navigator, constraints, resolve, reject)
            })
          }
        }
        var constraints = { audio: false, video: { width: this.videoWidth, height: this.videoHeight, transform: 'scaleX(-1)' } }
        navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
          // 旧的浏览器可能没有srcObject
          if ('srcObject' in _this.thisVideo) {
            _this.thisVideo.srcObject = stream
          } else {
            // 避免在新的浏览器中使用它，因为它正在被弃用。
            _this.thisVideo.src = window.URL.createObjectURL(stream)
          }
          _this.thisVideo.onloadedmetadata = function (e) {
            _this.thisVideo.play()
          }
        }).catch(err => {
          console.log(err)
        })
      },
      //  绘制图片（拍照功能）
      setImage () {

        var _this = this
        // 点击，canvas画图
        _this.thisContext.drawImage(_this.thisVideo, 0, 0, _this.videoWidth, _this.videoHeight)
        // 获取图片base64链接
        var image = this.thisCancas.toDataURL('image/png')
        _this.imgSrc = image
        this.$emit('refreshDataList', this.imgSrc)

        this.percentage = 0;
        this.dialogTableVisible = true;
        this.url_1 = "";
        this.url_2 = "";
        this.srcList = [];
        this.srcList1 = [];
        this.wait_return = "";
        this.wait_upload = "";
        this.feature_list = [];
        this.feat_list = [];
        this.fullscreenLoading = true;
        this.loading = true;
        //this.showbutton = false;
        this.person_num = 0;

        this.camerafilename = this.getCurrentDateTime();

        let file = this.dataURLtoFile(this.imgSrc, "camerafile"+ this.camerafilename +".jpg");//存储文件时，重命名打上时间戳留档
        this.url_1 = this.$options.methods.getObjectURL(file);
        let param = new FormData(); //创建form对象
        param.append("file", file, file.name); //通过append向form对象添加数据
        var timer = setInterval(() => {
          this.myFunc();
        }, 30);
        let config = {
          headers: { "Content-Type": "multipart/form-data" },
        }; //添加请求头
        axios
          .post(this.server_url + "/upload", param, config)
          .then((response) => {
          this.percentage = 100;
          clearInterval(timer);
          this.url_1 = response.data.image_url;
          this.srcList.push(this.url_1);
          this.url_2 = response.data.draw_url;
          this.srcList1.push(this.url_2);
          this.fullscreenLoading = false;
          this.loading = false;

          this.feat_list = Object.keys(response.data.image_info);

          for (var i = 0; i < this.feat_list.length; i++) {
            response.data.image_info[this.feat_list[i]][2] = this.feat_list[i];
            this.feature_list.push(response.data.image_info[this.feat_list[i]]);
          this.person_num++;//人数加一
          }

          if (this.person_num < this.numAlert) {
            this.noticeSafe();
          } else {
            this.noticeAlert();
          }

          this.feature_list.push(response.data.image_info);
          this.feature_list_1 = this.feature_list[0];
          this.dialogTableVisible = false;
          this.percentage = 0;
          this.notice1();
        });

      },

      //使用JavaScript的Date对象获取当前日期和时间。
      //使用new Date()语句来创建一个Date对象，然后使用Date对象的各种方法来获取当前日期和时间的各个部分，如年、月、日、时、分、秒等。
      //将获取到的日期和时间部分拼接成一个纯数字的字符串。
      //使用字符串的拼接操作符（+）来将各个部分拼接在一起，并使用字符串的padStart()方法来在数字前添加0，以确保每个部分都是两位数。
      getCurrentDateTime() {
        const now = new Date()
        const year = now.getFullYear().toString()
        const month = (now.getMonth() + 1).toString().padStart(2, '0')
        const date = now.getDate().toString().padStart(2, '0')
        const hour = now.getHours().toString().padStart(2, '0')
        const minute = now.getMinutes().toString().padStart(2, '0')
        const second = now.getSeconds().toString().padStart(2, '0')
        return year + month + date + hour + minute + second
      },

      // 自动化监测模块2023-3-13,已使用ChatGPT丰富注释
      // 定义一个名为setImageAuto的函数
      setImageAuto() {
        this.intervalTime = 10000 // 设置定时器间隔时间为10秒
        if (this.setImageAutoBoolean) { // 如果设置自动轮播的开关为true
          this.switchvalue = !this.switchvalue // 切换轮播状态
          this.setImageAutoBoolean = !this.setImageAutoBoolean // 切换自动轮播的开关
          if (this.switchvalue) { // 如果轮播状态为true
            this.intervalId = setInterval(this.setImage, this.intervalTime) // 设置定时器，每隔10秒调用一次setImage函数
          }
        }
        else { // 如果设置自动轮播的开关为false
          this.switchvalue = !this.switchvalue // 切换轮播状态
          this.setImageAutoBoolean = !this.setImageAutoBoolean // 切换自动轮播的开关
          clearInterval(this.intervalId) // 清除定时器
        }
      },

      // base64转文件
      dataURLtoFile (dataurl, filename) {
        var arr = dataurl.split(',')
        var mime = arr[0].match(/:(.*?);/)[1]
        var bstr = atob(arr[1])
        var n = bstr.length
        var u8arr = new Uint8Array(n)
        while (n--) {
          u8arr[n] = bstr.charCodeAt(n)
        }
        return new File([u8arr], filename, { type: mime })
      },
      // 关闭摄像头
      stopNavigator () {
        this.showbutton = true;
        this.thisVideo.srcObject.getTracks()[0].stop()
        // this.switchdisvalue = !this.switchdisvalue //关闭摄像头自动禁用模式切换开关【功能更新，开关仅作为示意】
        this.switchvalue = false //并将开关切换到手动模式
      },
      
      // 对接flask数据库查看模块，读取数据【明细记录】
      showDataDetail() {
        this.fullscreenLoading = true;
        this.loading = true;
        this.jsonData = {};

        let config = {
          headers: { "Content-Type": "multipart/form-data" },
        }; //添加请求头
        axios
          .get(this.server_url + "/testdb", config)
          .then((response) => {
          this.fullscreenLoading = false;
          this.loading = false;
          
          let arr = response.data.historical_data;
          let jsonObj = JSON.parse(JSON.stringify(arr));
          this.jsonData = jsonObj; // 将jsonObj赋值给jsonData属性
          console.log(jsonObj); // 输出JSON格式的对象
        });
      },

      // 对接flask数据库查看模块，读取数据【概览记录】
      showDataSummarize() {
        this.fullscreenLoading = true;
        this.loading = true;
        this.jsonData = {};

        let config = {
          headers: { "Content-Type": "multipart/form-data" },
        }; //添加请求头
        axios
          .get(this.server_url + "/testdbow", config)
          .then((response) => {
          this.fullscreenLoading = false;
          this.loading = false;
          
          let arr = response.data.testoverview;
          let jsonObj = JSON.parse(JSON.stringify(arr));
          this.jsonData = jsonObj; // 将jsonObj赋值给jsonData属性
          console.log(jsonObj); // 输出JSON格式的对象
        });
      },
  },
  mounted() {
    this.drawChart();
  },
};
</script>


<style>
#Content {
  background:#00000054;
  padding: 6px;
  border-radius: 5px;
  width: 90%;
  margin: 20px auto;
  margin-top: 40px;
}

#CT {
  display: flex;
  width: 100%;
  flex-wrap: wrap;
  justify-content: center;
}

/* 图像对比框 */
#CT_image {
  width: 500px;
  margin: 40px 0 20px 40px;
  border-radius: 15px;
}

.img_info_1 {
  height: 30px;
  width: 456px;
  text-align: center;
  background-color: #21b3b9;
  line-height: 30px;
}

.demo-image__preview1 {
  width: 456px;
  float: left;
}

.demo-image__preview2 {
  width: 456px;
  float: right;
}

/* 结果输出表格 */
.card_imginfo{
  width: 750px;
  margin: 50px auto;
  border-radius: 15px;
}

.error {
  height: 240px;
  margin: 30px;
  text-align: center;
}

div {
  display: block;
}

.download_bt {
  padding: 10px 16px !important;
}

.tx_img {
    max-width: 100%;
  }
</style>
