
# 代码描述：数据清洗第一步--- 检查所标注的xml文件中是否有命名不合规范的存在

import os
from tqdm import tqdm

xml_path = '../datasets/Annotations'       # 标注文件路径
image_path = '../datasets/JPEGImages/'     # 数据原图路径
image_lst = os.listdir(image_path)
xml_lst = os.listdir(xml_path)
print("image list:", len(image_lst))
print("xml list:", len(xml_lst))

for xml in xml_lst:
    if len(xml) != 10:
        print(xml)
