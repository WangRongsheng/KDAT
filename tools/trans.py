import os

input_dir_path = './input'              # 原来存放mask.txt文件的目录
#os.mkdir('./output')                 # 创建修改后存放的txt目录
output_dir_path = './output'         # 修改后存放的txt目录

def CreateNewMaskTxt(input_filename):
    with open(input_dir_path+'/'+input_filename, 'r',encoding='utf-8') as inputfile:
        with open(output_dir_path+'/'+input_filename, 'a',encoding='utf-8') as outputfile:
            for line in inputfile:
                list1 = line.rstrip('\n').split(' ')
                print(list1)
                label = 'shoot'
                conf = list1[1]
                x1 = list1[2]
                y1 = list1[3]
                x2 = list1[4]
                y2 = list1[5]
                list2 = [label, conf, x1, y1, x2, y2]
                print(list2)
                outputfile.write( str(label) + " " + str(conf) + " " + str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2) + '\n')
            outputfile.close()
        inputfile.close()
    return outputfile

for input_filename in os.listdir(input_dir_path): 
    print(input_filename)
    CreateNewMaskTxt(input_filename)
