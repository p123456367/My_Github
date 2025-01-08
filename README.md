# My_Github
Nanodet_plus是一个十分强大的轻量级目标检测模型,但是在visual studio ncnn端部署自己定制的模型时会产生一些错误,因此做出以下修改:
(1) 使用pnnx通过onnx文件生成.param和.bin文件时,有时最后的permute算子会消失不见,导致ncnn运行模型后没有结果产生,因此需要修改Nanodet.cpp中的decode_infer函数;
(2) 修改Nanodet.cpp中的disPred2Bbox函数;
(3) 修改NanoDet.h中的相关参数,比如图像宽度和高度等等.
