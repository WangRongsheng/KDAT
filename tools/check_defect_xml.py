
# 代码描述：数据清洗第二步--- 对比数据源图（jpg）与所保存的标注的xml文件，打印缺失的xml图片序号

import os
from tqdm import tqdm

xml_path = '../datasets/Annotations'       # 标注文件路径
image_path = '../datasets/JPEGImages/'     # 数据原图路径
image_lst = os.listdir(image_path)
xml_lst = os.listdir(xml_path)
print("image list:", len(image_lst))
print("xml list:", len(xml_lst))

missing_index = []
for image in tqdm(image_lst):
    xml = image[:-4] + '.xml'
    if xml not in xml_lst:
        missing_index.append(xml[:-4])
print(len(missing_index))
print(missing_index)

