import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QPushButton, QTextEdit, QProgressBar, \
    QFileDialog
from GUI.image_label import ImageLabel
from ImageProcess.process_thread import ProcessingThread
from Tools.log import Logger
from Tools.utils import array_to_qimage


class LeftUI(QVBoxLayout):
    def __init__(self,QMainWindow):
        super().__init__()
        self.QMainWindow=QMainWindow
        self.right_ui=self.QMainWindow.right_ui
        self.processed_img = None
        self.raw_img = None
        self.img_path = None
        self.language_map = {"中文": "zh", "英文": "en", "自动检测": None, "日文": "ja"}
        self.logger = Logger()


        # 图片显示区域
        self.coord_label = QLabel("鼠标坐标: (x, y)")
        self.coord_label.setAlignment(Qt.AlignCenter)
        self.image_label = ImageLabel("点击加载图片", self.coord_label)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(600, 200)
        self.image_label.setStyleSheet("background: #F0F0F0; border: 2px dashed #999;")
        self.image_label.setMouseTracking(True)
        self.addWidget(self.image_label)

        # 语言选择区
        lang_layout = QHBoxLayout()
        self.src_lang_combo = QComboBox()
        self.src_lang_combo.addItems(["自动检测", "中文", "英文", "日文"])
        self.target_lang_combo = QComboBox()
        self.target_lang_combo.addItems(["中文", "英文", "日文"])

        lang_layout.addWidget(self.coord_label)
        lang_layout.addWidget(self.src_lang_combo)
        lang_layout.addWidget(QLabel("→"))
        lang_layout.addWidget(self.target_lang_combo)
        lang_layout.addStretch()

        self.start_btn = QPushButton("开始进行翻译替换")
        self.select_img = QPushButton("选择图片")
        self.cmp_img = QPushButton("比较")
        lang_layout.addWidget(self.cmp_img)
        lang_layout.addStretch()
        lang_layout.addWidget(self.select_img)
        lang_layout.addWidget(self.start_btn)
        self.addLayout(lang_layout)

        # 日志和进度条
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        self.addWidget(self.log_text)
        self.addWidget(self.progress_bar)
        self.setupConnections()

    def setupConnections(self):
        self.start_btn.clicked.connect(self.start_processing)
        self.select_img.clicked.connect(self.select_img_path)
        self.cmp_img.pressed.connect(self.cmp_pressed)
        self.cmp_img.released.connect(self.cmp_released)

    def start_processing(self):
        if self.img_path is None:
            self.log_text.append(self.logger("图像路径为空，请选择图像路径！"))
            return
        # 初始化进度条和日志
        self.progress_bar.setValue(0)
        self.log_text.append(self.logger(f"开始处理图片{self.img_path}..."))

        # 创建并启动工作线程
        src_lang = self.src_lang_combo.currentText()
        src_lang = self.language_map.get(src_lang)
        dst_lang = self.target_lang_combo.currentText()
        dst_lang = self.language_map.get(dst_lang)

        self.worker = ProcessingThread(src_lang, dst_lang, self.img_path,self.right_ui)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.log_message.connect(self.log_text.append)
        self.worker.img_signal.connect(self.start_replace)
        self.worker.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    # 开始进行翻译替换的槽函数
    def start_replace(self, array):
        self.processed_img = array
        self.array2Qlabel(array)
        self.log_text.append(self.logger("图片处理成功！！"))

    def array2Qlabel(self, array):
        qimage = array_to_qimage(array)
        pixmap = QPixmap.fromImage(qimage).scaled(
            self.image_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.image_label.setPixmap(pixmap)

    def select_img_path(self):
        options = QFileDialog.Options()
        path, _ = QFileDialog.getOpenFileName(
            self.QMainWindow, "选择图像", "",
            "JPEG Images (*.jpg);;PNG Images (*.png);;All Files (*)",
            options=options
        )
        if path:
            self.img_path = path
            self.log_text.append(self.logger(f"图片添加成功{self.img_path.split('/')[-1]}"))
            self.raw_img = cv2.imread(self.img_path)
            self.raw_img = cv2.cvtColor(self.raw_img, cv2.COLOR_BGR2RGB)
            self.array2Qlabel(self.raw_img)


    #通过鼠标按压/释放比较变化前和变化后的图像
    def cmp_pressed(self):
        if self.raw_img is not None:
            self.array2Qlabel(self.raw_img)
        else:
            self.log_text.append(self.logger("没有选择图像"))

    def cmp_released(self):
        if self.processed_img is not None:
            self.array2Qlabel(self.processed_img)

