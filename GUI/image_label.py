from PyQt5.QtWidgets import QLabel


class ImageLabel(QLabel):
    def __init__(self,parent,coord_label):
        super().__init__(parent)
        self.y = None
        self.x = None
        self.coord_label=coord_label
        self.setMouseTracking(True)  # 启用鼠标跟踪

    def mouseMoveEvent(self, event):
        self.x = event.x()
        self.y = event.y()
        pos = self.mapFrom(self, event.pos())

        if 0 <= pos.x() < self.width() and 0 <= pos.y() < self.height():
            self.coord_label.setText(f"({pos.x()}, {pos.y()})")
        else:
            self.coord_label.setText("鼠标坐标: (不在图片区域内)")
        # print(f"实时坐标：({self.x}, {self.y})")