#-*-coding:utf-8-*-
# date:2021-05
# Author: Eric.Lee
# function: show yolo data of voc format anno

import cv2
import os
import numpy as np
import xml.etree.cElementTree as et

if __name__ == "__main__":

    path='G:/hand_detect_datasets-0/'
    path_voc_names = './cfg/hand.names'

    with open(path_voc_names, 'r') as f:
        label_map = f.readlines()
    label_dict = {}
    for i in range(len(label_map)):
        label_map[i] = label_map[i].strip()
        print(i,') ',label_map[i])
        label_dict[label_map[i]] = i

    print("label_dict : {}".format(label_dict))

    for file in os.listdir(path):
        if ".jpg" in file:
            path_img = path + file
            path_label = path_img.replace(".jpg",".xml")
            if not os.access(path_label,os.F_OK):
                continue
            img = cv2.imread(path_img)
            #
            tree=et.parse(path_label)
            root=tree.getroot()
            for Object in root.findall('object'):
                name=Object.find('name').text

                bndbox=Object.find('bndbox')
                x1= np.float32((bndbox.find('xmin').text))
                y1= np.float32((bndbox.find('ymin').text))
                x2= np.float32((bndbox.find('xmax').text))
                y2= np.float32((bndbox.find('ymax').text))

                cv2.rectangle(img, (int(x1),int(y1)), (int(x2),int(y2)), (255,100,100), 2)

                cv2.putText(img, "{}".format(name), (int(x1),int(y1)),\
                cv2.FONT_HERSHEY_PLAIN, 2.5, (0, 55, 255), 6)
                cv2.putText(img, "{}".format(name), (int(x1),int(y1)),\
                cv2.FONT_HERSHEY_PLAIN, 2.5, (0, 155, 255), 2)
            cv2.namedWindow('image',0)
            cv2.imshow('image',img)
            if cv2.waitKey(30) == 27:
                break
    cv2.destroyAllWindows()
