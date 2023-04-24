"""
2020.09.18:alian
json_to_xml
"""
import os
from tqdm import tqdm

from read_json_anno import ReadAnno
from create_xml_anno import CreateAnno


def json_transform_xml(json_path, xml_path, process_mode="rectangle"):
    json_path = json_path
    json_anno = ReadAnno(json_path, process_mode=process_mode)
    width, height = json_anno.get_width_height()
    filename = json_anno.get_filename()
    coordis = json_anno.get_coordis()

    xml_anno = CreateAnno()
    xml_anno.add_filename(filename)
    xml_anno.add_pic_size(width_text_str=str(width), height_text_str=str(height), depth_text_str=str(3))
    for xmin, ymin, xmax, ymax, label in coordis:
        xml_anno.add_object(name_text_str=str(label),
                            xmin_text_str=str(int(xmin)),
                            ymin_text_str=str(int(ymin)),
                            xmax_text_str=str(int(xmax)),
                            ymax_text_str=str(int(ymax)))

    xml_anno.save_doc(xml_path)


if __name__ == "__main__":
    root_json_dir = r"./json"  # json的路径
    root_save_xml_dir = r"./xml"  # xml的保存路径
    for json_filename in tqdm(os.listdir(root_json_dir)):
        if json_filename.split('.')[-1]=='json':
            json_path = os.path.join(root_json_dir, json_filename)
            save_xml_path = os.path.join(root_save_xml_dir, json_filename.replace(".json", ".xml"))
            json_transform_xml(json_path, save_xml_path, process_mode="polygon")   # labelme原数据的标注方式(矩形rectangle和多边形polygon)
