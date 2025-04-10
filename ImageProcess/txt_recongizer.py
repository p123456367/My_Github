import requests
from surya.recognition import RecognitionPredictor
from surya.detection import DetectionPredictor


class TxtRecongnizer:
    """文本识别器，用来进行文本翻译识别和文本检测"""
    def  __init__(self,image,src_lang,dst_lang):
        self.predictions = None
        self.img = image #该image是pil形式的image
        self.langs = src_lang
        self.dst_lang = dst_lang
        self.recognition_predictor = RecognitionPredictor()
        self.detection_predictor = DetectionPredictor()

    def txt_recognize(self):
        # langs=[[self.langs]] if self.langs is not None else [None]
        if self.langs is not None:
            self.predictions = self.recognition_predictor([self.img], [[self.langs]], self.detection_predictor)
        else:
            self.predictions=self.recognition_predictor([self.img],[None],self.detection_predictor)

    def prediction2list(self):
        """将bbox和翻译后的结果进行返回"""
        # global langs
        txt_lines = self.predictions[0].text_lines
        bbox_list = []
        txt_list = []
        conf_list = []
        for txt_line in txt_lines:
            if txt_line.confidence>0.6:
                text = txt_line.text
                print(text)
                lang = self.langs if self.langs is not None else "auto"
                result = requests.post(" http://127.0.0.1:5000/translate",
                                       json={"q": text, "source": lang, "target": self.dst_lang})
                # print(result.json())
                bbox = txt_line.bbox
                conf_list.append(txt_line.confidence)
                bbox_list.append(bbox)
                txt_list.append(result.json())
        print(bbox_list)
        # print()
        print(conf_list)
        return  [bbox_list,txt_list,conf_list]