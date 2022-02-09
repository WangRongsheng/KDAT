
# 代码描述：数据清洗第四步--- 将所有xml文件信息写入一个excel表格，后期数据分析使用
# 如果报List 超出，则可以参考：https://blog.csdn.net/Tw_light/article/details/111769657

import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '*.xml'):
        print(xml_file)
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[1][0].text),
                     int(member[1][1].text),
                     int(member[1][1].text),
                     int(member[1][3].text)
                     )
            xml_list.append(value)
    
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df

if __name__ == "__main__":
    xml_path = '../datasets/Annotations/'       # 标注文件路径
    xml_df = xml_to_csv(xml_path)
    xml_df.to_csv('dataset_Vehicle.csv', index=None)
    print('Successfully converted xml to csv.')
    
