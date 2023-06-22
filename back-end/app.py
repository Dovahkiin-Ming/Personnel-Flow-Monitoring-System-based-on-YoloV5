# 本模块为flask核心模块，设置各种路由功能
# 上传文件【已完成】2022
# --自动删除uploads文件夹缓存文件【已完成】2022
# --原图和分析后的图片会留档至tmp文件夹
# 展示图片【已完成】2022
# 操作数据库【已完成】2023-3-10
# --增加config.py文件，将对数据库的操作做封装【已完成】2023-3-10
# 代码优化【正在进行】
# 最后编译时间 2023-05-09
# 存在问题【暂无】

import datetime
import logging as rel_log
import os
import shutil
from datetime import timedelta
from flask import *
from processor.AIDetector_pytorch import Detector

import core.main

#引用config.py文件
from config import *
import math

#为方便打包，路径引用方式改为自动获取
import os
import sys
PROJECT_DIR = os.path.dirname(__file__)
if getattr(sys, 'frozen', False):
    # 如果是 PyInstaller 打包的应用程序，则获取静态文件夹的路径
    UPLOAD_FOLDER = os.path.join(sys._MEIPASS, "uploads")
else:
    # 否则，在开发模式下使用相对路径
    UPLOAD_FOLDER = r'./uploads'

ALLOWED_EXTENSIONS = set(['png', 'jpg'])

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'secret!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#werkzeug_logger = rel_log.getLogger('werkzeug')
#werkzeug_logger.setLevel(rel_log.ERROR)

# 解决缓存刷新问题
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)


# 添加header解决跨域
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    return response


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    return redirect(url_for('static', filename='index.html'))


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    file = request.files['file']
    print(datetime.datetime.now(), file.filename)
    if file and allowed_file(file.filename):
        src_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(src_path)
        shutil.copy(src_path, PROJECT_DIR+'/tmp/original')
        image_path = os.path.join(PROJECT_DIR+'/tmp/original', file.filename)
        pid, image_info = core.main.c_main(
            image_path, current_app.model, file.filename.rsplit('.', 1)[1])
        delete_file(file.filename)#调用删除文件上传缓存接口，避免文件多次存储导致浪费资源
        return jsonify({'status': 1,
                        'image_url': 'http://127.0.0.1:5003/tmp/original/' + pid,
                        'draw_url': 'http://127.0.0.1:5003/tmp/draw/' + pid,
                        'image_info': image_info})

    return jsonify({'status': 0})


# 下载预留接口
# @app.route("/download", methods=['GET'])
# def download_file():
#     # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
#     return send_from_directory('./tmp/original', FILE_NAME, as_attachment=True)


# 删除文件上传缓存接口【已启用】2023-1-1
# 避免文件多次存储导致浪费资源
def delete_file(filename):
    os.remove(app.config['UPLOAD_FOLDER']+'/'+filename)

# 测试数据库存储/展示功能【已验证】2023-3-10
# 修改新功能，展示之前监测数据，接口已开启，2023-3-12
# 本模块以Json格式展示数据，测试功能移入testdb1()，2023-3-13
@app.route('/testdb', methods=['GET', 'POST'])
def testdb():
    db = SQLManager()
    show_data_db = db.get_list('select * from imginfo ')
    db.close()
    return jsonify({'status': 1,
                    'historical_data': show_data_db})

# 获取testoverview数据
@app.route('/testdbow', methods=['GET', 'POST'])
def testdbow():
    db = SQLManager()
    show_data_ow_db = db.get_list('select * from testoverview ')
    db.close()
    return jsonify({'status': 1,
                    'testoverview': show_data_ow_db})

# 早期测试功能移入testdb1()，已启用2023-3-13
@app.route('/testdb1', methods=['GET', 'POST'])
def testdb1():
    db = SQLManager()
    show_data_db1 = db.get_list('select * from imginfo ')
    db.close()
    return render_template('testdb.html', show_data_db1=show_data_db1)

#把字典数据重整为字符串【未完成废弃，直接采用原始数据】
def convertdata(image_info):
    str = image_info
    return str

# 原始图片和检测结果图片展示
@app.route('/tmp/<path:file>', methods=['GET'])
def show_photo(file):
    if request.method == 'GET':
        if not file is None:
            image_data = open(PROJECT_DIR+f'/tmp/{file}', "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response


if __name__ == '__main__':
    with app.app_context():
        current_app.model = Detector()
    app.run(host='127.0.0.1', port=5003, debug=True)
