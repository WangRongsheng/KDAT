@echo off
REM 声明采用UTF-8编码
chcp 65001
echo 开始执行数据格式转化...
echo ===============================================
echo 1. 数据不对应清除...
python clear_xml_img.py
echo 清除完成
echo ===============================================
echo 2. 数据转化...
python voc_to_yolo.py
echo 转化完成
echo ===============================================
echo 3. 数据划分...
python split_trainTestVal.py
echo 划分完成
echo ===============================================
echo 3. 数据移动...
python remove_all_data.py
echo 移动完成
echo ===============================================
echo ★请前往 datasets 文件夹下复制 data 文件夹去训练模型★
echo ===============================================

pause
