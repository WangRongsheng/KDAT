'''
coco instance file example:
{
    "info": { 
        "description": "COCO 2017 Dataset", # 数据集描述
        "url": "http://cocodataset.org", # 下载地址
        "version": "1.0", # 版本
        "year": 2017, # 年份
        "contributor": "COCO Consortium", # 提供者
        "date_created": "2017/09/01" # 数据创建日期
    },
    
    "licenses": [
        {
            "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
            "id": 1,
            "name": "Attribution-NonCommercial-ShareAlike License"
        },
    ],
    
    "images": [
        {
            "license": 4,
            "file_name": "000000397133.jpg", # 图片名
            "coco_url":  "http://images.cocodataset.org/val2017/000000397133.jpg",# 网路地址路径
            "height": 427, # 高
            "width": 640, # 宽
            "date_captured": "2013-11-14 17:02:52", # 数据获取日期
            "flickr_url": "http://farm7.staticflickr.com/6116/6255196340_da26cf2c9e_z.jpg",# flickr网路地址
            "id": 397133 # 图片的ID编号（每张图片ID是唯一的）
        },
    ],

    "categories": [ # 类别描述
        {
            "supercategory": "person", # 主类别
            "id": 1, # 类对应的id （0 默认为背景）
            "name": "person" # 子类别
        },
        {
            "supercategory": "vehicle", 
            "id": 2,
            "name": "bicycle"
        },
        {
            "supercategory": "vehicle",
            "id": 3,
            "name": "car"
        },
    ],

    "annotations": [
        {
            "segmentation": [ # 对象的边界点（边界多边形）
                [
                    224.24,297.18,# 第一个点 x,y坐标
                    228.29,297.18, # 第二个点 x,y坐标
                    234.91,298.29,
                    ……
                    ……
                    225.34,297.55
                ]
            ],
            "area": 1481.3806499999994, # 区域面积
            "iscrowd": 0, # 
            "image_id": 397133, # 对应的图片ID（与images中的ID对应）
            "bbox": [217.62,240.54,38.99,57.75], # 定位边框 [x,y,w,h]
            "category_id": 44, # 类别ID（与categories中的ID对应）
            "id": 82445 # 对象ID，因为每一个图像有不止一个对象，所以要对每一个对象编号（每个对象的ID是唯一的）
        },
    ]
}
'''


import sys
import os
import json
import cv2
import random
import shutil

class COCOCreater:

    def __init__(self, src_dir, dst_dir):
        self.train_map = {
            "info": { 
                "description": "COCO 2017 Dataset", # 数据集描述
                "url": "http://cocodataset.org", # 下载地址
                "version": "1.0", # 版本
                "year": 2017, # 年份
                "contributor": "COCO Consortium", # 提供者
                "date_created": "2017/09/01" # 数据创建日期
            },
            
            "licenses": [
                {
                    "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
                    "id": 1,
                    "name": "Attribution-NonCommercial-ShareAlike License"
                },
            ],
            
            "images": [
            
            ],

            "categories": [ # 类别描述
            
            ],

            "annotations": [
            
            ]
        }
        
        self.val_map = {
            "info": { 
                "description": "COCO 2017 Dataset", # 数据集描述
                "url": "http://cocodataset.org", # 下载地址
                "version": "1.0", # 版本
                "year": 2017, # 年份
                "contributor": "COCO Consortium", # 提供者
                "date_created": "2017/09/01" # 数据创建日期
            },
            
            "licenses": [
                {
                    "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
                    "id": 1,
                    "name": "Attribution-NonCommercial-ShareAlike License"
                },
            ],
            
            "images": [
            
            ],

            "categories": [ # 类别描述
            
            ],

            "annotations": [
            
            ]
        }
        
        self.support_formats=['jpg', 'JPG', 'png', 'PNG']
        self.src_dir = src_dir
        self.dst_dir = dst_dir
        self.src_label_file = self.src_dir + '/label.txt'
        self._create_dst_struct()
        
    def read_ori_labels(self):
        print("trans to coco: start read ori labels")
        labels = []
        with open(self.src_label_file, 'r') as f:
            for line in f.readlines():
                labels.append(line.strip('\r\n'))
        random.shuffle(labels)        
        self.ori_train_labels = labels[0: int(len(labels) * 0.8)]
        self.ori_val_labels = labels[int(len(labels) * 0.8):]
        #print(self.ori_train_labels)
        #print(self.ori_val_labels)
        
    
    def create_train_map(self):
        print("trans to coco: start create train dataset for coco")
        self._create_coco_map(self.ori_train_labels, self.train_map, self.dst_dir_train2017)
        with open(self.instances_train2017, "w") as f:
            json.dump(self.train_map, f)
        
        
    def create_val_map(self):
        print("trans to coco: start create val data set for coco")
        self._create_coco_map(self.ori_val_labels, self.val_map, self.dst_dir_val2017)
        with open(self.instances_val2017, "w") as f:
            json.dump(self.val_map, f)
    
    def _create_coco_map(self, ori_labels, coco_map, img_dst_dir):
        self.max_cls = -1
        self.img_id = 0
        self.box_id = 0
     
        for i, line in enumerate(ori_labels):
            print('trans to coco: %d/%d'%(i+1, len(ori_labels)))
            self._create_by_line(line.strip('\r\n'), coco_map, img_dst_dir)
        print('trans to coco: success')
        #print(self.train_map)
        #print(json.dumps(self.train_map))
        
        
    def _create_by_line(self, line, coco_map, img_dst_dir):
        fileds = line.split(' ')
        img_name=fileds[0]
        assert '.' in img_name, 'img_name do not has . '
        assert img_name.split('.')[-1] in self.support_formats, 'img_name format is not illagle: (%s)'%img_name
                
        img_path = os.path.join(self.src_dir, img_name)
        img = cv2.imread(img_path)
        assert img is not None, 'img is none, img path is:%s'%img_path
        h, w, c = img.shape
        shutil.copy(img_path, img_dst_dir)
                
        #add image
        self._add_image(img_name, h, w, coco_map)
        
        #img box
        if(len(fileds) > 4):
            boxes = fileds[1:]
            assert(len(boxes) % 5 == 0)
            box_count = int(len(boxes) / 5)
            for i in range(box_count):
                box = boxes[i*5:i*5+5]
                x0 = float(box[0])
                y0 = float(box[1])
                x1 = float(box[2])
                y1 = float(box[3])
                cls = int(float(box[4]))
                self._add_cls(cls, coco_map)
                self._add_box(x0,y0,x1,y1,cls, coco_map)
                self.box_id += 1
                
        self.img_id += 1  
        
        
    
    def _add_cls(self, cls, coco_map):
        if cls > self.max_cls:
            self.max_cls = cls
            coco_map["categories"].append({"supercategory": "type_%d"%cls, 
                                                 "id": self.max_cls,
                                                 "name": "type_%d"%cls})
    def _add_image(self, img_name, h, w, coco_map):
        coco_map["images"].append({"license": 1,
                                         "file_name": "%s"%img_name,
                                         "coco_url":  "http://images.cocodataset.org/val2017/000000397133.jpg",
                                         "height": h,
                                         "width": w,
                                         "date_captured": "2013-11-14 17:02:52",
                                         "flickr_url": "http://farm7.staticflickr.com/6116/6255196340_da26cf2c9e_z.jpg",
                                         "id": self.img_id
                                         })

    def _add_box(self, x0,y0,x1,y1,cls, coco_map):
        box_area = (x1-x0)*(y1-y0)
        coco_map["annotations"].append({"segmentation": [[x0, y0, x0, y1, x1,y1, x1, y0, x0, y0]],
                                             "area": box_area,
                                             "iscrowd": 0,
                                             "image_id": self.img_id,
                                             "bbox": [ x0, y0, x1-x0, y1-y0],
                                             "category_id": cls,
                                             "id": self.box_id
                                             })
        
        
    def _create_dst_struct(self):
        assert(os.path.exists(self.dst_dir))
        self.dst_dir_train2017 = os.path.join(self.dst_dir, 'train2017')
        self.dst_dir_val2017 = os.path.join(self.dst_dir, 'val2017')
        self.dst_dir_annotations = os.path.join(self.dst_dir, 'annotations')
        self.instances_train2017 = os.path.join(self.dst_dir_annotations, 'instances_train2017.json')
        self.instances_val2017 = os.path.join(self.dst_dir_annotations, 'instances_val2017.json')
        
        if not os.path.exists(self.dst_dir_train2017):
            os.mkdir(self.dst_dir_train2017)
        if not os.path.exists(self.dst_dir_val2017):
            os.mkdir(self.dst_dir_val2017)
        if not os.path.exists(self.dst_dir_annotations):
            os.mkdir(self.dst_dir_annotations)
    
        
        
if __name__ == '__main__':
    coco = COCOCreater('./third_bridge_0', '../ttt')
    coco.read_ori_labels()
    coco.create_train_map()
    coco.create_val_map()




