import numpy as np
from PyQt5.QtGui import QImage


def array_to_qimage(array):
    """将numpy数组转换为QImage对象[5](@ref)"""
    if array.dtype != np.uint8:
        array = (array - array.min()) / (array.max() - array.min()) * 255
        print(1)
        array = array.astype(np.uint8)
    height, width = array.shape[:2]
    if len(array.shape) == 2:  # 灰度图
        bytes_per_line = width
        return QImage(array.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
    elif len(array.shape) == 3:  # RGB
        bytes_per_line = 3 * width
        return QImage(array.data, width, height, bytes_per_line, QImage.Format_RGB888)

if __name__ == '__main__':
    try:
        array_to_qimage(None)
    except Exception as e:
        print(e)