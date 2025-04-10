import subprocess
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QHBoxLayout,QVBoxLayout, QWidget, QMessageBox, QMenu, QAction)
from GUI.left_UI import LeftUI
from GUI.right_UI import RightUI
from Tools.log import Logger


class TranslationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.processed_img = None
        self.raw_img = None
        self.img_path = None
        # self.setupConnections()
        self.language_map={"中文":"zh","英文":"en","自动检测":None,"日文":"ja"}
        self.logger = Logger()
        # 主窗口设置
        self.setWindowTitle("图片文字翻译替换工具")
        self.setGeometry(300, 200, 1000, 800)
        # 创建主布局容器
        main_widget = QWidget()
        # main_widget.setMouseTracking(True)
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # left_layout = QVBoxLayout()
        # right_layout = QVBoxLayout()
        self.right_ui = RightUI(self)
        self.left_ui = LeftUI(self)
        main_layout.addLayout(self.left_ui)
        main_layout.addLayout(self.right_ui)
        # 美化样式[5](@ref)
        self.setStyleSheet("""
                        QWidget { font-family: 'Microsoft YaHei'; }
                        QPushButton { 
                            background: #0078D7; 
                            color: white;
                            padding: 8px 16px;
                            border-radius: 4px;
                        }
                        QProgressBar {
                            border: 2px solid #D0D0D0;
                            border-radius: 5px;
                            text-align: center;
                        }
                        QProgressBar::chunk {
                            background: #0078D7;
                        }
                    """)



    def contextMenuEvent(self, event):
        #右键上下文菜单管理器
        # 创建菜单对象
        context_menu = QMenu(self)

        # 添加菜单项
        action1 = QAction("像素锁定", self)
        action2 = QAction("选项2", self)
        action3 = QAction("选项3", self)

        # 连接菜单项的触发信号
        action1.triggered.connect(lambda: print("选择了选项1"))
        action2.triggered.connect(lambda: print("选择了选项2"))
        action3.triggered.connect(lambda: print("选择了选项3"))

        # 添加分隔线
        context_menu.addAction(action1)
        context_menu.addAction(action2)
        context_menu.addSeparator()
        context_menu.addAction(action3)

        # 显示菜单
        context_menu.exec_(event.globalPos())

    # def mouseMoveEvent(self, event):
    #     # 获取鼠标相对于image_label的位置
    #     pos = self.image_label.mapFrom(self, event.pos())
    #
    #     if 0 <= pos.x() < self.image_label.width() and 0 <= pos.y() < self.image_label.height():
    #         self.coord_label.setText(f"鼠标坐标: ({pos.x()}, {pos.y()})")
    #     else:
    #         self.coord_label.setText("鼠标坐标: (不在图片区域内)")
    #     event.ignore()
        # super().mouseMoveEvent(event)



def handle_exception(exc_type, exc_value, exc_traceback):
    """全局异常处理函数"""
    # 忽略键盘中断（Ctrl+C）
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    # 显示错误弹窗
    # error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    msg_box = QMessageBox()
    # msg_box.setIcon(QMessageBox.Critical)
    msg_box.setWindowTitle("程序异常")
    msg_box.setText("发生未捕获的异常，详情见下方信息。")
    msg_box.setDetailedText("1")
    msg_box.exec_()




if __name__ == "__main__":
    process = subprocess.Popen(
        ["libretranslate"],
        stdout=subprocess.DEVNULL,  # 丢弃标准输出
        stderr=subprocess.DEVNULL,  # 丢弃错误输出
        shell=True  # 若命令包含通配符或管道需启用
    )
    # sys.excepthook = handle_exception  # 关键：注册全局钩子
    app = QApplication(sys.argv)
    window = TranslationApp()
    window.show()
    sys.exit(app.exec_())