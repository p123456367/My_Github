import cv2
import numpy as np
from PIL import Image
from PyQt5.QtCore import QThread, pyqtSignal
from ImageProcess.txt_recongizer import TxtRecongnizer
from ImageProcess.txt_replacer import TxtReplacer



class ProcessingThread(QThread):
    """处理线程类，用于处理整个检测+翻译+替换的功能"""
    progress_updated = pyqtSignal(int)
    log_message = pyqtSignal(str)
    img_signal = pyqtSignal(np.ndarray)

    def __init__(self,src_lang,dst_lang,img_path,right_ui):
        super().__init__()
        self.src_lang=src_lang
        self.dst_lang=dst_lang
        self.img_path=img_path
        self.right_ui=right_ui


    def run(self):
        # 模拟处理过程（替换为实际OCR和翻译逻辑）
        # for i in range(5):
        #     self.log_message.emit(f"正在处理第 {i + 1} 个文本区域")
        #     self.progress_updated.emit((i + 1) * 20)
        #     self.msleep(500)
        image=Image.open(self.img_path)
        img = cv2.imread(self.img_path, cv2.IMREAD_GRAYSCALE)
        # 使用 Otsu's method 执行阈值分割
        _, thresholded_img = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
        # # 创建结构元素, 这里使用了一个4x4的方形结构元素
        # cv2.imshow("threshold", thresholded_img)
        # cv2.waitKey(0)
        # kernel = np.ones((1, 1), np.uint8)  # 超参数
        # # # 使用cv2.dilate()进行膨胀操作
        # thresholded_img = cv2.dilate(thresholded_img*255, kernel, iterations=2)  # 超参数
        # thresholded_img[thresholded_img==255]=0
        # thresholded_img[thresholded_img ==0] = 255
        image = Image.fromarray(thresholded_img, mode='L')
        cv2.imshow("threshold", thresholded_img)
        cv2.waitKey(0)
        img = cv2.imread(self.img_path)
        txt_recognizer = TxtRecongnizer(image,self.src_lang,self.dst_lang)
        txt_recognizer.txt_recognize()
        self.progress_updated.emit(50)
        [bbox_list,txt_list,conf_list]=txt_recognizer.prediction2list()
        txt_replacer = TxtReplacer(img,bbox_list,txt_list,conf_list,self.right_ui)
        txt_replacer.txt_replace()
        self.progress_updated.emit(100)
        out_img=txt_replacer.img
        self.img_signal.emit(cv2.cvtColor(out_img,cv2.COLOR_BGR2RGB))