import os
 
images_dir = './img/'
xml_dir = './xml/'
 

#创建列表
xmls = []
#读取xml文件名(即：标注的图片名)
for xml in os.listdir(xml_dir):
    #xmls.append(os.path.splitext(xml)[0])    #append()参数：在列表末尾添加新的对象，即将所有文件名读入列表
    xmls.append(xml.split('.')[0])#splitext和split的区别：前者('0001','.jpg'), 后者('0001','jpg') 在此可选用
print(len(xmls)) # 1072

#创建列表
imgs = []
#读取xml文件名(即：标注的图片名)
for im in os.listdir(images_dir):
    #xmls.append(os.path.splitext(xml)[0])    #append()参数：在列表末尾添加新的对象，即将所有文件名读入列表
    imgs.append(im.split('.')[0])#splitext和split的区别：前者('0001','.jpg'), 后者('0001','jpg') 在此可选用
print(len(imgs)) # 1039
 
#读取所有图片
for xml_name in os.listdir(xml_dir):
    xml_name = xml_name.split('.')[0]
    if xml_name not in imgs:
        xml_name = xml_name + '.xml'
        print(xml_name)
        os.remove(os.path.join(xml_dir,xml_name))
