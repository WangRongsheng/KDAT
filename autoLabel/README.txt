环境：
同yolov5-V6环境

使用：
0. 选择使用gpu还是cpu，在autoLabel.py的第26行，cpu模式下半精度推理
1. 自己的图片数据集到sources/images
2. 修改自己的数据集的yaml文件，sources/data.yaml
3. 修改sources/detector_classes.txt内容为要标注的类别
4. 下载模型权重或者准备自己的权重
5. 运行软件开始使用（调试情况下运行软件即为运行py，正常运行bat）
6. 安装使用labelimg软件进行标注校准

脚本：
- 制作yolo数据集：https://github.com/WangRongsheng/make-your-yolov5_dataset
