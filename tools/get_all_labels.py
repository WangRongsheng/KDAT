import xml.dom.minidom as xmldom
import os

#voc数据集获取所有标签的所有类别数"
annotation_path=r'../datasets/Annotations/'

annotation_names=[os.path.join(annotation_path,i) for i in os.listdir(annotation_path)]

labels = list()
for names in annotation_names:
    xmlfilepath = names
    domobj = xmldom.parse(xmlfilepath)
    # 得到元素对象
    elementobj = domobj.documentElement
    #获得子标签
    subElementObj = elementobj.getElementsByTagName("object")
    for s in subElementObj:
        label=s.getElementsByTagName("name")[0].firstChild.data
        #print(label)
        if label not in labels:
            labels.append(label)
print(labels)

