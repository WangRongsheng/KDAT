# 清理一下jpeg和xml不匹配问题
import os,shutil

jpeg = './sources/images/'
jpeg_list = os.listdir(jpeg)

anno = './sources/Annotation'
anno_list = os.listdir(anno)

# 清除img
for pic in jpeg_list:
    name = pic.split('.')[0]
    anno_name = name + '.xml'
    #print(anno_name)
    if anno_name not in anno_list:
        os.remove(os.path.join(jpeg,pic))