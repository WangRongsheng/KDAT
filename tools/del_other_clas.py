import xml.etree.cElementTree as ET
import os

path_root = ['./NEU-DEF2/Annotations']  #自己的xml路径

CLASSES = ['crazing', 'patches', 'scratches']  #要保留的类别
for anno_path in path_root:
    xml_list = os.listdir(anno_path)
    for axml in xml_list:
        path_xml = os.path.join(anno_path, axml)
        print(path_xml)
        tree = ET.parse(path_xml)
        root = tree.getroot()

        for child in root.findall('object'):
            name = child.find('name').text
            if not name in CLASSES:
                root.remove(child)
        print(axml)
        tree.write(os.path.join('./NEU-DEF2/Annotations2', axml))  #处理结束后保存的路径

