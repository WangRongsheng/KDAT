# 后期修改标注好的xml文件中的标签名字

# code
def changeName(xml_fold, origin_name, new_name):
    '''
    xml_fold: xml存放文件夹
    origin_name: 原始名字，比如弄错的名字，原先要cow,不小心打成cwo
    new_name: 需要改成的正确的名字，在上个例子中就是cow
    '''
    files = os.listdir(xml_fold)
    cnt = 0 
    for xmlFile in files:
        file_path = os.path.join(xml_fold, xmlFile)
        dom = parse(file_path)
        root = dom.getroot()
        for obj in root.iter('object'):#获取object节点中的name子节点
            tmp_name = obj.find('name').text
            if tmp_name == origin_name: # 修改
                obj.find('name').text = new_name
                print("change %s to %s." % (origin_name, new_name))
                cnt += 1
        dom.write(file_path, xml_declaration=True)#保存到指定文件
    print("有%d个文件被成功修改。" % cnt)


'''
# 实战案例：
import os
import os.path
from xml.etree.ElementTree import parse, Element

def changeName(xml_fold):
    # xml_fold: xml存放文件夹
    files = os.listdir(xml_fold)
    cnt = 0 
    for xmlFile in files:
        file_path = os.path.join(xml_fold, xmlFile)
        dom = parse(file_path)
        root = dom.getroot()
        for obj in root.iter('object'):#获取object节点中的name子节点
            tmp_name = obj.find('name').text
            if tmp_name == "bao": # 修改
                obj.find('name').text = "bag"
                print("change bao to bag.")
                cnt += 1
            if tmp_name == "shouji": # 修改
                obj.find('name').text = "phone"
                print("change shouji to phone.")
                cnt += 1
            if tmp_name == "qianbao": # 修改
                obj.find('name').text = "wallet"
                print("change qianbao to wallet.")
                cnt += 1
            if tmp_name == "yaoshi": # 修改
                obj.find('name').text = "key"
                print("change yaoshi to key.")
                cnt += 1
            if tmp_name == "shuibei": # 修改
                obj.find('name').text = "cup"
                print("change shuibei to cup.")
                cnt += 1
        dom.write(file_path, xml_declaration=True)#保存到指定文件
    print("有%d个文件被成功修改。" % cnt)

changeName('./Annotations')
'''