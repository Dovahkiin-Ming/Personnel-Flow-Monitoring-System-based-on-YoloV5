import cv2

#为方便打包，路径引用方式改为自动获取
import os
PROJECT_DIR = os.path.dirname(__file__)
DRAW_DIR = os.path.join(PROJECT_DIR,"..\\tmp\\draw").replace('\\', '/')

def predict(dataset, model, ext):
    global img_y
    x = dataset[0].replace('\\', '/')
    file_name = dataset[1]
    print(x)
    print(file_name)
    x = cv2.imread(x)
    img_y, image_info = model.detect(x)
    cv2.imwrite(DRAW_DIR+'/{}.{}'.format(file_name, ext), img_y)
    return image_info