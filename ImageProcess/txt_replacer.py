import re

import cv2
import numpy as np

from GUI.right_UI import RightUI


class TxtReplacer:
    """文本替换器，用于文本消除和替换"""
    def __init__(self,img:np.ndarray,bbox_list:list,txt_list:list,conf_list:list,
                 right_ui:RightUI):
        """

        Args:
            img:  np.ndarray,three_channels, BGR_Format, [h,w,3]
            bbox_list: list
            txt_list: list
        """
        self.img = img
        assert(img.shape[-1]==3,"Ensure the image adheres to the BGR format specification.")
        self.bbox_list = bbox_list
        self.txt_list = txt_list
        self.conf_list = conf_list
        self.right_ui = right_ui

    def txt_replace(self):
        for bbox, txt,conf in zip(self.bbox_list, self.txt_list,self.conf_list):
            if  len(re.findall(r'\d', txt['translatedText'])) < 3:
                bbox = list(map(int, bbox))
                mask = np.zeros(self.img.shape[:2], dtype="uint8")
                img_roi = self.img[bbox[1]:bbox[3], bbox[0]:bbox[2]]
                img_roi = cv2.cvtColor(img_roi, cv2.COLOR_BGR2GRAY)
                _, mask[bbox[1]:bbox[3], bbox[0]:bbox[2]] = cv2.threshold(img_roi, 0, 255,
                                                                          cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
                # 创建结构元素, 这里使用了一个4x4的方形结构元素
                kernel = np.ones((4, 4), np.uint8)  # 超参数
                # 使用cv2.dilate()进行膨胀操作
                mask = cv2.dilate(mask, kernel, iterations=2)  # 超参数
                # 消除图像文字
                img = cv2.inpaint(self.img, mask, 3, cv2.INPAINT_TELEA)
                # 加入新文字
                self.img = self.fit_text_in_rectangle(img, (bbox[0], bbox[1], bbox[2], bbox[3]), txt['translatedText'],
                                        background_color=None,color=self.right_ui.font.font_color)

    @staticmethod
    def fit_text_in_rectangle(
            image,
            rect,
            text,
            font=cv2.FONT_HERSHEY_SIMPLEX,
            min_font_scale=0.5,
            max_font_scale=2.0,
            line_spacing=1.0,
            color=(0, 0, 0),
            background_color=(0, 0, 0),
            padding=1
    ):
        """
        在指定矩形区域内适配文本，自动调整字体大小和换行。

        Args:
            image (numpy.ndarray): 输入图像（BGR 格式）。
            rect (tuple): 矩形区域坐标 (x1, y1, x2, y2)。
            text (str): 要添加的文本内容。
            font (int): 字体类型（如 cv2.FONT_HERSHEY_SIMPLEX）。
            min_font_scale (float): 最小字体比例（防止过小）。
            max_font_scale (float): 最大字体比例（防止过大）。
            line_spacing (float): 行间距倍数（如 1.2 表示 20% 的间距）。
            color (tuple): 文本颜色（BGR）。
            background_color (tuple or None): 背景填充颜色（如黑色提高可读性）。
            padding (int): 文本与矩形边框的间距。

        Returns:
            numpy.ndarray: 处理后的图像。
        """
        x1, y1, x2, y2 = rect
        rect_width = x2 - x1 - 2 * padding
        rect_height = y2 - y1 - 2 * padding

        # 初始化参数
        font_scale = max_font_scale
        lines = [text]  # 初始为单行文本

        # 尝试减小字体比例，直到文本宽度适配矩形
        while font_scale > min_font_scale:
            # 计算当前字体下的单行文本最大宽度
            max_line_width = 0
            for line in lines:
                (w, h), _ = cv2.getTextSize(
                    line,
                    fontFace=font,
                    fontScale=font_scale,
                    thickness=1
                )
                if w > max_line_width:
                    max_line_width = w

            if max_line_width <= rect_width:
                break

            font_scale -= 0.1  # 逐步减小字体

        # 如果字体比例减到最小仍溢出，则尝试换行
        if font_scale <= min_font_scale:
            # 自动换行（按空格分割）
            words = text.split()
            lines = []
            current_line = ""
            for word in words:
                temp_line = current_line + " " + word if current_line else word
                w, h = cv2.getTextSize(
                    temp_line,
                    fontFace=font,
                    fontScale=font_scale,
                    thickness=1
                )[0]
                if w <= rect_width:
                    current_line = temp_line
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)

        # 计算多行文本的总高度
        total_text_height = 0
        for line in lines:
            _, h = cv2.getTextSize(
                line,
                fontFace=font,
                fontScale=font_scale,
                thickness=1
            )[0]
            total_text_height += h * line_spacing

        # 如果总高度超过矩形高度，进一步减小字体
        while total_text_height > rect_height and font_scale > min_font_scale:
            font_scale -= 0.1
            total_text_height = 0
            for line in lines:
                _, h = cv2.getTextSize(
                    line,
                    fontFace=font,
                    fontScale=font_scale,
                    thickness=1
                )[0]
                total_text_height += h * line_spacing

        # 确定文本的起始位置（居中对齐）
        x = x1 + padding
        y = y1 + padding + int((rect_height + total_text_height) / 2)  # 垂直居中

        # 绘制背景填充（可选）
        if background_color:
            cv2.rectangle(
                image,
                (x1, y1),
                (x2, y2),
                background_color,
                -1
            )

        # 逐行绘制文本
        for line in lines:
            (w, h), _ = cv2.getTextSize(
                line,
                fontFace=font,
                fontScale=font_scale,
                thickness=1
            )
            text_bottom_y = y
            cv2.putText(
                image,
                line,
                (x + (rect_width - w) // 2, int(text_bottom_y)),  # 水平居中
                font,
                font_scale,
                color,
                1,
                cv2.LINE_AA
            )
            y += h * line_spacing

        return image