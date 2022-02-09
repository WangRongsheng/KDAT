# 删除没有对应xml文件的jpg文件

import os
from tqdm import tqdm

xml_path = './sources/Annotation'       # 标注文件路径
image_path = './sources/images/'     # 数据原图路径

image_lst = os.listdir(image_path)
xml_lst = os.listdir(xml_path)

missing_index = []
for image in tqdm(image_lst):
    xml = image[:-4] + '.xml'
    if xml not in xml_lst:
        missing_index.append(xml[:-4])

for index in missing_index:
    image = index + '.jpg'
    os.remove(image_path + image)
    
