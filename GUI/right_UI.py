from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QGridLayout, QGroupBox, QPushButton, QFontComboBox, QSpinBox, QButtonGroup, QRadioButton, \
    QVBoxLayout, QTextEdit, QColorDialog

from Settings.font_setting import FontSetter


class RightUI(QGridLayout):
    def __init__(self,QMainWindow):
        super().__init__()
        # self.color = None
        self.initUI()
        self.ui=QMainWindow
        self.font = FontSetter(10,(0,0,0))

    def initUI(self):
        # 主网格布局
        # 字体设置容器
        font_group = QGroupBox("字体设置")
        font_layout = self.create_font_settings()
        font_group.setLayout(font_layout)

        # 更多设置容器
        advanced_group = QGroupBox("更多设置")
        advanced_layout = self.create_advanced_settings()
        advanced_group.setLayout(advanced_layout)

        # 网格布局分配
        self.addWidget(font_group, 0, 0, 1, 1)  # 占前两行
        self.addWidget(advanced_group, 1, 0, 1, 1)

        # self.setLayout(main_grid)
        # self.setWindowTitle('文档设置面板')
        # self.resize(800, 400)

    def create_font_settings(self):
        layout = QGridLayout()

        # 字体颜色按钮 [1](@ref)
        self.color_btn = QPushButton("字体颜色")
        self.color_btn.clicked.connect(self.choose_font_color)

        # 字体类型选择 [3,11](@ref)
        self.font_combo = QFontComboBox()

        # 字号设置 [3](@ref)
        self.size_spin = QSpinBox()
        self.size_spin.setRange(8, 72)
        self.size_spin.setValue(12)
        # self.font.font_size =self.size_spin.value()

        # 对齐方式按钮组 [3](@ref)
        align_group = QButtonGroup()
        self.align_left = QRadioButton("左对齐")
        self.align_center = QRadioButton("居中")
        self.align_right = QRadioButton("右对齐")
        align_group.addButton(self.align_left)
        align_group.addButton(self.align_center)
        align_group.addButton(self.align_right)

        # 背景颜色按钮 [1](@ref)
        self.bg_color_btn = QPushButton("背景颜色")
        self.bg_color_btn.clicked.connect(self.choose_bg_color)

        # 布局排列
        layout.addWidget(self.color_btn, 0, 0)
        layout.addWidget(self.font_combo, 0, 1)
        layout.addWidget(self.size_spin, 0, 2)
        layout.addWidget(self.align_left, 1, 0)
        layout.addWidget(self.align_center, 1, 1)
        layout.addWidget(self.align_right, 1, 2)
        layout.addWidget(self.bg_color_btn, 2, 0, 1, 3)

        return layout

    def create_advanced_settings(self):
        layout = QVBoxLayout()

        # ROI选择按钮 [8](@ref)
        self.roi_btn = QPushButton("选择ROI区域")
        self.roi_btn.clicked.connect(self.select_roi)

        # 文字消除输入框 [3,12](@ref)
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("输入待处理文本...")

        # 功能按钮组
        btn_layout = QGridLayout()
        self.clear_btn = QPushButton("执行消除")
        self.reset_btn = QPushButton("重置设置")

        btn_layout.addWidget(self.clear_btn, 0, 0)
        btn_layout.addWidget(self.reset_btn, 0, 1)

        layout.addWidget(self.roi_btn)
        layout.addWidget(self.text_edit)
        layout.addLayout(btn_layout)

        return layout

    def choose_font_color(self):
        color = QColorDialog.getColor()  # [1](@ref)

        if color.isValid():
            self.text_edit.setTextColor(color)
            print(color.rgb())
            self.font.font_color=(color.blue(),color.green(),color.red())

    def choose_bg_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            palette = self.text_edit.palette()
            palette.setColor(QPalette.Base, color)  # [1](@ref)
            self.text_edit.setPalette(palette)

    def select_roi(self):
        # 需结合OpenCV或QGraphicsView实现区域选择
        # 此处为伪代码示例
        print("调用ROI选择功能，获取坐标信息")

    # 其他信号槽连接
    def connect_signals(self):
        self.font_combo.currentFontChanged.connect(self.update_font)
        self.size_spin.valueChanged.connect(self.update_font_size)
        self.align_left.toggled.connect(lambda: self.update_alignment(Qt.AlignLeft))
        self.clear_btn.clicked.connect(self.process_text_elimination)

    def update_font(self):
        self.text_edit.setCurrentFont(self.font_combo.currentFont())

    def update_font_size(self, size):
        self.text_edit.setFontPointSize(size)

    def update_alignment(self, align):
        self.text_edit.setAlignment(align)

    def process_text_elimination(self):
        # 结合ROI坐标进行文字消除处理
        print("执行文字消除操作")