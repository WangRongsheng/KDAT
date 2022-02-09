# 清理一下jpeg和xml不匹配问题
import os,shutil

jpeg = '../datasets/JPEGImages'
jpeg_list = os.listdir(jpeg)

anno = '../datasets/Annotations'
anno_list = os.listdir(anno)

for pic in jpeg_list:
    name = pic.split('.')[0]
    anno_name = name + '.xml'
    #print(anno_name)
    if anno_name not in anno_list:
        os.remove(os.path.join(jpeg,pic))

print('清除比对后，文件数量为：')
for dirpath, dirnames, filenames in os.walk(jpeg):
    file_count = 0
    for file in filenames:
        file_count = file_count + 1
    print(dirpath,file_count)

for dirpath, dirnames, filenames in os.walk(anno):
    file_count = 0
    for file in filenames:
        file_count = file_count + 1
    print(dirpath,file_count)