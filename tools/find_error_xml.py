import os
import xml.etree.ElementTree as ET
import numpy as np

# np.set_printoptions(suppress=True, threshold=np.nan)
import matplotlib
from PIL import Image


def parse_obj(xml_path, filename):
    tree = ET.parse(xml_path + filename)
    objects = []
    for obj in tree.findall('object'):
        obj_struct = {}
        obj_struct['name'] = obj.find('name').text
        bbox = obj.find('bndbox')
        obj_struct['bbox'] = [int(bbox.find('xmin').text),
                              int(bbox.find('ymin').text),
                              int(bbox.find('xmax').text),
                              int(bbox.find('ymax').text)]
        objects.append(obj_struct)
    return objects


def read_image(image_path, filename):
    im = Image.open(image_path + filename)
    W = im.size[0]
    H = im.size[1]
    area = W * H
    im_info = [W, H, area]
    return im_info


if __name__ == '__main__':
    image_path = r'../datasets/JPEGImages/'
    xml_path = r'../datasets/Annotations/'
    filenamess = os.listdir(xml_path)
    filenames = []
    for name in filenamess:
        name = name.replace('.xml', '')
        filenames.append(name)
    recs = {}
    ims_info = {}
    obs_shape = {}
    classnames = []
    num_objs = {}
    obj_avg = {}
    for i, name in enumerate(filenames):
        recs[name] = parse_obj(xml_path, name + '.xml')
        ims_info[name] = read_image(image_path, name + '.jpg')
    for name in filenames:
        im_w = ims_info[name][0]
        im_h = ims_info[name][1]
        im_area = ims_info[name][2]
        for object in recs[name]:
            if object['name'] not in num_objs.keys():
                num_objs[object['name']] = 1
            else:
                num_objs[object['name']] += 1
            ob_w = object['bbox'][2] - object['bbox'][0]
            ob_h = object['bbox'][3] - object['bbox'][1]
            ob_area = ob_w * ob_h
            if object['bbox'][3] > im_h:
                print("这个标签有问题：{}".format(name))
                print("这个目标有问题：{}".format(object['name']))
            if object['bbox'][2] > im_w:
                print("这个标签有问题：{}".format(name))
                print("这个目标有问题：{}".format(object['name']))
            if object['bbox'][1] > im_h:
                print("这个标签有问题：{}".format(name))
                print("这个目标有问题：{}".format(object['name']))
            if object['bbox'][0] > im_w:
                print("这个标签有问题：{}".format(name))
                print("这个目标有问题：{}".format(object['name']))
            ob_h = object['bbox'][3] - object['bbox'][1]
            ob_area = ob_w * ob_h
            w_rate = ob_w / im_w
            h_rate = ob_h / im_h
            area_rate = ob_area / im_area
            if not object['name'] in obs_shape.keys():
                obs_shape[object['name']] = ([[ob_w,
                                               ob_h,
                                               ob_area,
                                               w_rate,
                                               h_rate,
                                               area_rate]])
            else:
                obs_shape[object['name']].append([ob_w,
                                                  ob_h,
                                                  ob_area,
                                                  w_rate,
                                                  h_rate,
                                                  area_rate])
        if object['name'] not in classnames:
            classnames.append(object['name'])
