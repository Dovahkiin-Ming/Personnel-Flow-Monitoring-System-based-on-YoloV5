# 0. 一些建议：

可以使用Anaconda来管理Python虚拟环境及包

安装包时一定要注意版本对应关系！！！包列表会在下文列出【待补充】

更新显卡驱动
查看本机GPU信息：nvidia-smi

安装gpu版本pytorch，注意CUDA版本[Release Notes :: CUDA Toolkit Documentation (nvidia.com)](https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html)

首先是各种版本的DUDA的下载链接  
[CUDA Toolkit Archive | NVIDIA Developer](https://developer.nvidia.com/cuda-toolkit-archive)

查看CUDA是否安装：nvcc -V

本人的安装命令，仅供参考：

```shell
conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia
```

https://download.pytorch.org/whl/torch_stable.html

版本对应超级重要！！！目前都是cu117版本，可以使用conda list检查
当前构建版本CUDA 11.7

```python
import torch #导入torch包
torch.cuda.device_count() #查看GPU数
torch.cuda.is_available() #验证GPU是否已激活
```

# 1. 效果：

视频链接：

[哔哩哔哩](https://www.bilibili.com/video/BV18g4y137oR/)

展示效果：

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

【待补充】

# 4. Flask 部署：

【待补充】

# 5. VUE前端：

【待补充】

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

然后在浏览器打开[localhost](http://localhost:8080/)即可：

# 关注我的哔哩哔哩：

感兴趣的同学关注我的哔哩哔哩：

[哔哩哔哩](https://space.bilibili.com/355272176)
