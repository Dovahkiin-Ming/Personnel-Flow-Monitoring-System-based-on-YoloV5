# 0. 一些建议：

使用Anaconda来管理Python虚拟环境及包

安装包时一定要注意版本对应关系！！！[包列表](#article_button)会在页尾列出

查看本机GPU信息：
```shell
nvidia-smi
```
安装gpu版本[Pytorch](https://download.pytorch.org/whl/torch_stable.html)，注意CUDA版本[Release Notes :: CUDA Toolkit Documentation (nvidia.com)](https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html)

首先是[各种版本的DUDA的下载链接](https://developer.nvidia.com/cuda-toolkit-archive)

查看CUDA是否安装：
```shell
nvcc -V
```

本人的安装命令，仅供参考：

```shell
conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia
```

版本对应超级重要！！！目前都是cu117版本，可以使用conda list检查
当前构建版本CUDA 11.7

```python
import torch #导入torch包
torch.cuda.device_count() #查看GPU数，需要大于0
torch.cuda.is_available() #验证GPU是否已激活，需要是true
```

# 1. 效果：
[展示视频](https://www.bilibili.com/video/BV18g4y137oR/)

![主界面](https://github.com/Dovahkiin-Ming/Personnel-Flow-Monitoring-System-based-on-YoloV5/blob/master/main.png)

# 2. YOLOv5模型训练：

[YoloV5官方](https://github.com/ultralytics/yolov5)的参考训练命令：

```shell
python train.py --data coco.yaml --epochs 300 --weights '' --cfg yolov5n.yaml  --batch-size 128
```

这里演示的话我就用官方训练好的 yolov5m.pt 模型。

这里我自己的训练命令：

```shell
python train.py --data coco.yaml --epochs 10 --weights yolov5m.pt --batch-size 8
```

这里需要注意的参数是epochs训练轮数，weights预训练模型，以及batch-size每次输入大小
各项参数并非越高越好，需要多次验证，选择最适合的参数

# 3. YOLOv5模型预测：

【[AIDetector_pytorch.py](https://github.com/Dovahkiin-Ming/Personnel-Flow-Monitoring-System-based-on-YoloV5/blob/beta/back-end/processor/AIDetector_pytorch.py)】

这里因为我只做人流量监测，所以做了筛选，删除即可正常检测80种类别
```python
def detect(self, im):
        im0, img = self.preprocess(im)
        pred = self.m(img, augment=False)[0]
        pred = pred.float()
        pred = non_max_suppression(pred, self.threshold, 0.3)
        pred_boxes = []
        image_info = {}
        count = 0
        for det in pred:
            if det is not None and len(det):
                det[:, :4] = scale_coords(
                    img.shape[2:], det[:, :4], im0.shape).round()
                for *x, conf, cls_id in det:
                    lbl = self.names[int(cls_id)] #用个中间参来保存人物类型名称
                    x1, y1 = int(x[0]), int(x[1])
                    x2, y2 = int(x[2]), int(x[3])
                    pred_boxes.append(
                        (x1, y1, x2, y2, lbl, conf))
                    # count += 1
                    key = ""
                    if lbl == "person" : #只输出【人】
                        count += 1
                        key = '{}-{:02}'.format(lbl, count) #输出类型和编号
                        image_info[key] = ['{}×{}'.format(
                            x2-x1, y2-y1), np.round(float(conf), 3)] #输出大小和置信度
                        #数据库操作模块
                        db = SQLManager()
                        keydb = '\'' + key + '\''#目标代号
                        image_info01db = '\'' + '{}×{}'.format(x2-x1, y2-y1) + '\''#图像大小
                        image_info02db =  '\'' + str(np.round(float(conf), 3)) + '\''#置信度
                        datatimenow = '\'' + str(datetime.datetime.now().replace(microsecond=0)) + '\''#时间戳
                        sql = 'INSERT INTO imginfo VALUES(' + keydb + ' ,' + image_info01db + ' ,' + image_info02db + ' ,' + datatimenow + ');'
                        db.moddify(sql)
                        db.close()
```

# 4. 后端部署（开发）：

【[app.py](https://github.com/Dovahkiin-Ming/Personnel-Flow-Monitoring-System-based-on-YoloV5/blob/beta/back-end/app.py)】

路由示例
```python
@app.route('/')
def hello_world():
    return redirect(url_for('static', filename='./index.html'))
```

数据库操作示例
```python
@app.route('/testdb', methods=['GET', 'POST'])
def testdb():
    db = SQLManager()
    show_data_db = db.get_list('select * from imginfo ')
    db.close()
    return jsonify({'status': 1,
                    'historical_data': show_data_db})
```

# 5. 前端部署（开发）：

【[Content.vue](https://github.com/Dovahkiin-Ming/Personnel-Flow-Monitoring-System-based-on-YoloV5/blob/beta/front-end/src/components/Content.vue)】

摄像头模块
```javascript
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
```

拍照上传模块，文件手动上传与其类似
```javascript
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
```

# 6. 启动项目：

在 Flask 后端项目下启动后端代码：

```bash
python app.py
```

在 VUE 前端项目下，先安装依赖：

```bash
npm install
```

然后运行前端：

```bash
npm run serve
```

如果遇到opensslError，可以使用：

```bash
set NODE_OPTIONS=--openssl-legacy-provider
```

然后在浏览器打开[localhost](https://space.bilibili.com/355272176)即可：

# 7. 更新纪录：

-V1.0 初始化项目，基础功能构建

-V1.1 修改路径引用方式，支持生成独立部署版本，可大幅度减轻客户机配置压力

前端生成命令
```bash
npm run build #先使用npm构建
pkg -t win package.json #再使用pkg打包
```
后端生成命令
```bash
pyinstaller app.spec #app.spec文件可以使用pyinstaller -F app.py命令自动生成，主要需要修改datas和hiddenimports字段
```
# 8. 本人所用包列表：<a id="article_button"></a>

```text
Python 3.10.6

absl-py                   1.3.0                     <pip>
asttokens                 2.1.0                     <pip>
backcall                  0.2.0                     <pip>
bzip2                     1.0.8                he774522_0    http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
ca-certificates           2022.10.11           haa95532_0    http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
cachetools                5.2.0                     <pip>
certifi                   2022.9.24       py310haa95532_0    http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
charset-normalizer        2.1.1                     <pip>
click                     8.1.3                     <pip>
colorama                  0.4.6                     <pip>
contourpy                 1.0.6                     <pip>
cycler                    0.11.0                    <pip>
decorator                 5.1.1                     <pip>
easydict                  1.10                      <pip>
executing                 1.2.0                     <pip>
Flask                     2.2.2                     <pip>
Flask-Cors                3.0.10                    <pip>
Flask-SQLAlchemy          3.0.3                     <pip>
fonttools                 4.38.0                    <pip>
google-auth               2.14.1                    <pip>
google-auth-oauthlib      0.4.6                     <pip>
greenlet                  2.0.2                     <pip>
grpcio                    1.50.0                    <pip>
idna                      3.4                       <pip>
ipython                   8.6.0                     <pip>
itsdangerous              2.1.2                     <pip>
jedi                      0.18.1                    <pip>
Jinja2                    3.1.2                     <pip>
kiwisolver                1.4.4                     <pip>
libffi                    3.4.2                hd77b12b_4    http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
Markdown                  3.4.1                     <pip>
MarkupSafe                2.1.1                     <pip>
matplotlib                3.6.2                     <pip>
matplotlib-inline         0.1.6                     <pip>
numpy                     1.23.4                    <pip>
oauthlib                  3.2.2                     <pip>
opencv-python             4.5.4.60                  <pip>
openssl                   1.1.1s               h2bbff1b_0    http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
packaging                 21.3                      <pip>
pandas                    1.5.1                     <pip>
parso                     0.8.3                     <pip>
pickleshare               0.7.5                     <pip>
Pillow                    9.3.0                     <pip>
pip                       22.2.2          py310haa95532_0    http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
prompt-toolkit            3.0.32                    <pip>
protobuf                  3.20.1                    <pip>
psutil                    5.9.4                     <pip>
pure-eval                 0.2.2                     <pip>
pyasn1                    0.4.8                     <pip>
pyasn1-modules            0.2.8                     <pip>
Pygments                  2.13.0                    <pip>
PyMySQL                   1.0.2                     <pip>
pyparsing                 3.0.9                     <pip>
python                    3.10.6               hbb2ffb3_1    http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
python-dateutil           2.8.2                     <pip>
pytz                      2022.6                    <pip>
PyYAML                    6.0                       <pip>
requests                  2.28.1                    <pip>
requests-oauthlib         1.3.1                     <pip>
rsa                       4.9                       <pip>
scipy                     1.9.3                     <pip>
seaborn                   0.12.1                    <pip>
setuptools                65.5.0          py310haa95532_0    http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
six                       1.16.0                    <pip>
SQLAlchemy                2.0.5.post1               <pip>
sqlite                    3.39.3               h2bbff1b_0    http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
stack-data                0.6.1                     <pip>
tensorboard               2.11.0                    <pip>
tensorboard-data-server   0.6.1                     <pip>
tensorboard-plugin-wit    1.8.1                     <pip>
thop-0.1.1                2209072238                <pip>
tk                        8.6.12               h2bbff1b_0    http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
torch                     1.13.0+cu117              <pip>
torchaudio                0.13.0+cu117              <pip>
torchvision               0.14.0+cu117              <pip>
tqdm                      4.64.1                    <pip>
traitlets                 5.5.0                     <pip>
typing_extensions         4.4.0                     <pip>
tzdata                    2022f                h04d1e81_0    http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
urllib3                   1.26.12                   <pip>
vc                        14.2                 h21ff451_1    http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
vs2015_runtime            14.27.29016          h5e58377_2    http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
wcwidth                   0.2.5                     <pip>
Werkzeug                  2.2.2                     <pip>
wheel                     0.37.1             pyhd3eb1b0_0    http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
wincertstore              0.2             py310haa95532_2    http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
xz                        5.2.6                h8cc25b3_0    http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
zlib                      1.2.13               h8cc25b3_0    http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
```

# 特别鸣谢✨项目参考：

🤞[YOLOv5 🚀 in PyTorch > ONNX > CoreML > TFLite](https://github.com/ultralytics/yolov5)

🤞[基于Flask开发后端、VUE开发前端框架，在WEB端部署YOLOv5目标检测模型](https://github.com/liuxiaoxiao666/Yolov5-Flask-VUE)

🤞[Person and Car Detector](https://github.com/KananVyas/person_car_detection_yolov5)