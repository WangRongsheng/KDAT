import cv2
import os
import glob
import random
import numpy as np
from tkinter import *
from tkinter import filedialog
from xml.etree import ElementTree as ET
import natsort

class MixImg():
    def __init__(self):
        self.bg_dir = r""
        self.img_dir = r""
        self.save_dir = r""
        self.annotation_dir = r""
        self.detect_class = r""
        self.rename_dir = r""
        self.first_index = None
        self.file_tail = r""
        self.new_name = r""
        self.handle_flag = False
        self.predefined_classes = []
        self.objectList = []
        self.mix_flag = False
        self.rename_flag = False
        self.root_window = None

    def re_imsize(self, num, num1):
        if (num < num1):
            num1 = num * 0.30
        return num1

    def judge_rate(self, num, num1, rate):
        if (num / num1 != rate):
            num = num1 * rate
        return num, num1

    def create_annotation(self, xn):
        global annotation
        tree = ET.ElementTree()
        tree.parse(xn)
        annotation = tree.getroot()

    # 遍历xml里面每个object的值如果相同就不插入
    def traverse_object(self, AnotPath):
        tree = ET.ElementTree(file=AnotPath)
        root = tree.getroot()
        ObjectSet = root.findall('object')
        for Object in ObjectSet:
            ObjName = Object.find('name').text
            BndBox = Object.find('bndbox')
            x1 = int(BndBox.find('xmin').text)
            y1 = int(BndBox.find('ymin').text)
            x2 = int(BndBox.find('xmax').text)
            y2 = int(BndBox.find('ymax').text)
            self.objectList.append([x1, y1, x2, y2, ObjName])

    # 定义一个创建一级分支object的函数
    def create_object(self, root, objl):  # 参数依次，树根，xmin，ymin，xmax，ymax
        # 创建一级分支object
        _object = ET.SubElement(root, 'object')
        # 创建二级分支
        name = ET.SubElement(_object, 'name')
        # print(obj_name)
        name.text = str(objl[4])
        pose = ET.SubElement(_object, 'pose')
        pose.text = 'Unspecified'
        truncated = ET.SubElement(_object, 'truncated')
        truncated.text = '0'
        difficult = ET.SubElement(_object, 'difficult')
        difficult.text = '0'
        # 创建bndbox
        bndbox = ET.SubElement(_object, 'bndbox')
        xmin = ET.SubElement(bndbox, 'xmin')
        xmin.text = '%s' % objl[0]
        ymin = ET.SubElement(bndbox, 'ymin')
        ymin.text = '%s' % objl[1]
        xmax = ET.SubElement(bndbox, 'xmax')
        xmax.text = '%s' % objl[2]
        ymax = ET.SubElement(bndbox, 'ymax')
        ymax.text = '%s' % objl[3]

    # 创建xml文件的函数
    def create_tree(self, image_name, h, w, imgdir):
        global annotation
        # 创建树根annotation
        annotation = ET.Element('annotation')
        # 创建一级分支folder
        folder = ET.SubElement(annotation, 'folder')
        # 添加folder标签内容
        folder.text = (imgdir)

        # 创建一级分支filename
        filename = ET.SubElement(annotation, 'filename')
        filename.text = image_name

        # 创建一级分支path
        path = ET.SubElement(annotation, 'path')

        # path.text = getcwd() + '\{}\{}'.format(imgdir, image_name)  # 用于返回当前工作目录
        path.text = '{}'.format(imgdir)  # 用于返回当前工作目录

        # 创建一级分支source
        source = ET.SubElement(annotation, 'source')
        # 创建source下的二级分支database
        database = ET.SubElement(source, 'database')
        database.text = 'Unknown'

        # 创建一级分支size
        size = ET.SubElement(annotation, 'size')
        # 创建size下的二级分支图像的宽、高及depth
        width = ET.SubElement(size, 'width')
        width.text = str(w)
        height = ET.SubElement(size, 'height')
        height.text = str(h)
        depth = ET.SubElement(size, 'depth')
        depth.text = '3'

        # 创建一级分支segmented
        segmented = ET.SubElement(annotation, 'segmented')
        segmented.text = '0'

    def pretty_xml(self, element, indent, newline, level=0):  # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
        if element:  # 判断element是否有子元素
            if (element.text is None) or element.text.isspace():  # 如果element的text没有内容
                element.text = newline + indent * (level + 1)
            else:
                element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
                # else:  # 此处两行如果把注释去掉，Element的text也会另起一行
                # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
        temp = list(element)  # 将element转成list
        for subelement in temp:
            if temp.index(subelement) < (len(temp) - 1):  # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
                subelement.tail = newline + indent * (level + 1)
            else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
                subelement.tail = newline + indent * level
            self.pretty_xml(subelement, indent, newline, level=level + 1)  # 对子元素进行递归操作

    def rename(self):
        for file_name in natsort.natsorted(glob.glob(os.path.join(self.rename_dir, "*"))):
            # 设置旧文件名（就是路径+文件名）
            # print(file_name)
            oldname = file_name
            if (self.first_index == None):
                self.first_index = 0
            newname = self.rename_dir + '\\' + self.new_name + str(self.first_index) + self.file_tail
            # print(newname)
            # # 设置新文件名
            # newname = file_name.split('\\')[-1]+ str(n + 1) + '.jpg'
            #
            # # 用os模块中的rename方法对文件改名
            os.rename(oldname, newname)
            print(oldname, '======>', newname)

            self.first_index = int(self.first_index) + 1
        self.first_index = None

    def make_annotation(self, iw, igauss, irate, mixdir, n, index):
        IMAGES_LIST = os.listdir(mixdir)
        # print(IMAGES_LIST)
        for bg_filename in natsort.natsorted(IMAGES_LIST):
            n += 1
            if bg_filename.endswith(('.jpg', '.png', '.jpeg', '.bmp')):
                bg_filename=os.path.join(mixdir,bg_filename)
                save_filename = self.save_dir + '/'
                # save_annoname=cut_img_filename+"mix" + os.path.splitext(bg_filename)[0].split('\\')[-1]
                save_annoname = "mix" + str(n)
                save_filename += save_annoname
                bg = cv2.imread(bg_filename)
                bg_h, bg_w = bg.shape[:2]
                # img_h=self.re_imsize(bg_h,img_h)
                img_w = int(self.re_imsize(bg_w, iw))
                # img_h,img_w=self.judge_rate(img_h,img_w,hw_rate)
                img_h = int(img_w * irate)
                img_h = int(self.re_imsize(bg_h, img_h))
                img = cv2.resize(igauss, (img_w, img_h))
                rnd = [random.randint(0, bg_h - img_h), random.randint(0, bg_w - img_w)]
                object_information = [rnd[1], rnd[0], img.shape[1] + rnd[1], img.shape[0] + rnd[0],
                                      self.predefined_classes[index]]  # x1,y1,x2,y2,name
                xml_name = ('{}\{}.xml'.format(self.annotation_dir, save_annoname))
                if (os.path.exists(xml_name)):
                    self.create_annotation(xml_name)
                    self.traverse_object(xml_name)
                else:
                    self.create_tree(save_annoname+'.jpg', img_h, img_w, mixdir)
                if (self.objectList.count(object_information) == 0):
                    self.create_object(annotation, object_information)
                self.objectList = []
                tree = ET.ElementTree(annotation)
                root = tree.getroot()
                self.pretty_xml(root, '\t', '\n')
                tree.write(xml_name, encoding='utf-8')
                # print(iname + "标签已保存")
                img_mask = 255 * np.ones(img.shape[:2], img.dtype)
                bg[object_information[1]:object_information[3],
                object_information[0]:object_information[2]] = cv2.bitwise_and(img, img, mask=img_mask)
                cv2.imwrite(save_filename + '.jpg', bg)
                print("图片已保存到" + save_filename)
                # self.handle_flag=True
                # print(img_filename+"标签已保存")

    def mix(self):
        with open(self.detect_class, "r") as f:  # 打开文件
            for line in f.readlines():
                line = line.strip('\n')  # 去掉列表中每一个元素的换行符
                self.predefined_classes.append(line)
        self.handle_flag = False
        # for i in range(1, int(self.predefined_classes[0]) + 1):
        label_index = -1
        for img_filename in natsort.natsorted(glob.glob(os.path.join(self.img_dir, "*"))):
            label_index += 1
            bg_index = 0
            if img_filename.endswith(('.jpg', '.png', '.jpeg', '.bmp')):
                original_img = cv2.imread(img_filename)
                # cut_img_filename=os.path.splitext(img_filename)[0].split('\\')[-1]
                img_h, img_w = original_img.shape[:2]
                img_gauss = cv2.GaussianBlur(original_img, (3, 3), 0)
                hw_rate = img_h / img_w
                # file_tail = os.path.splitext(img_filename)[1]
                if (self.handle_flag):
                    self.make_annotation( img_w, img_gauss, hw_rate, self.save_dir, bg_index, label_index)
                else:
                    self.make_annotation( img_w, img_gauss, hw_rate, self.bg_dir, bg_index, label_index)
                self.handle_flag = True
        self.predefined_classes=[]

    def client(self):
        def creatWindow():
            self.root_window.destroy()
            window()

        def judge(str):
            if (str):
                text = "你已选择" + str
            else:
                text = "你还未选择文件夹，请选择"
            return text

        def test01():
            self.img_dir = r""
            self.img_dir += filedialog.askdirectory()
            creatWindow()

        def test02():
            self.bg_dir = r""
            self.bg_dir += filedialog.askdirectory()
            creatWindow()

        def test03():
            self.save_dir = r""
            self.save_dir += filedialog.askdirectory()
            creatWindow()

        def test04():
            self.annotation_dir = r""
            self.annotation_dir += filedialog.askdirectory()
            creatWindow()

        def test05():
            self.detect_class = r""
            self.detect_class += filedialog.askopenfilename()
            creatWindow()

        def test06():
            self.mix_flag = True
            self.mix()
            creatWindow()
            
        def test07():
            self.rename_dir = r""
            self.rename_dir += filedialog.askdirectory()
            creatWindow()

        def test08(t_n, t_f, t_t):
            self.new_name = t_n
            self.first_index = t_f
            self.file_tail = t_t
            self.rename_flag = True
            self.rename()
            creatWindow()

        def window():
            self.root_window = Tk()
            self.root_window.title("mixImg-数据拓展工具")
            screenWidth = self.root_window.winfo_screenwidth()  # 获取显示区域的宽度
            screenHeight = self.root_window.winfo_screenheight()  # 获取显示区域的高度
            tk_width = 500  # 设定窗口宽度
            tk_height = 400  # 设定窗口高度
            tk_left = int((screenWidth - tk_width) / 2)
            tk_top = int((screenHeight - tk_width) / 2)
            self.root_window.geometry('%dx%d+%d+%d' % (tk_width, tk_height, tk_left, tk_top))
            self.root_window.minsize(tk_width, tk_height)  # 最小尺寸
            self.root_window.maxsize(tk_width, tk_height)  # 最大尺寸
            self.root_window.resizable(width=False, height=False)
            btn_1 = Button(self.root_window, text='选择要标注的图片文件夹', command=test01,
                           height=0)
            btn_1.place(x=175, y=40, anchor='w')

            text = judge(self.img_dir)
            text_label = Label(self.root_window, text=text)
            text_label.place(x=166, y=70, anchor='w')

            btn_2 = Button(self.root_window, text='选择背景图的文件夹', command=test02,
                           height=0)
            btn_2.place(x=175, y=100, anchor='w')
            text = judge(self.bg_dir)
            text_label = Label(self.root_window, text=text)
            text_label.place(x=166, y=130, anchor='w')

            btn_3 = Button(self.root_window, text='选择保存图片的文件夹', command=test03,
                           height=0)
            btn_3.place(x=175, y=160, anchor='w')
            text = judge(self.save_dir)
            text_label = Label(self.root_window, text=text)
            text_label.place(x=166, y=190, anchor='w')

            btn_4 = Button(self.root_window, text='选择保存的xml文件夹(.xml)', command=test04,
                           height=0)
            btn_4.place(x=175, y=220, anchor='w')
            text = judge(self.annotation_dir)
            text_label = Label(self.root_window, text=text)
            text_label.place(x=166, y=250, anchor='w')

            btn_5 = Button(self.root_window, text='选择需要生成数据的类别文件(.txt)', command=test05,
                           height=0)
            btn_5.place(x=175, y=280, anchor='w')
            text = judge(self.detect_class)
            text_label = Label(self.root_window, text=text)
            text_label.place(x=166, y=310, anchor='w')


            btn_6 = Button(self.root_window, text='开始生成', command=test06,
                           height=0)
            btn_6.place(x=175, y=340, anchor='w')
            if (self.mix_flag):
                text = "生成完成"
            else:
                text = "等待生成"
            text_label = Label(self.root_window, text=text)
            text_label.place(x=166, y=370, anchor='w')

            btn_7 = Button(self.root_window, text='选择要改名的文件夹', command=test07,
                           height=0)
            btn_7.place(x=20, y=100, anchor='w')

            text_label = Label(self.root_window, text="改变后的名字")
            text_label.place(x=20, y=130, anchor='w')
            t_7_name = StringVar()
            t_7_name.set("mix")
            t_7_name = Entry(self.root_window, textvariable=t_7_name)
            t_7_name.place(x=100, y=130, width=50, anchor='w')

            text_label = Label(self.root_window, text="文件序号从何值开始")
            text_label.place(x=20, y=160, anchor='w')
            t_7_first = StringVar()
            t_7_first.set("0")
            t_7_first = Entry(self.root_window, textvariable=t_7_first)
            t_7_first.place(x=137, y=160, width=20, anchor='w')

            text_label = Label(self.root_window, text="文件名后缀")
            text_label.place(x=20, y=190, anchor='w')
            t_7_tail = StringVar()
            t_7_tail.set(".jpg")
            t_7_tail = Entry(self.root_window, textvariable=t_7_tail, width=20)
            t_7_tail.place(x=90, y=190, width=30, anchor='w')
            if (self.rename_dir):
                btn_8 = Button(self.root_window, text='开始改名(慎用)',
                               command=lambda: test08(t_7_name.get(), t_7_first.get(), t_7_tail.get()),
                               height=0)
                btn_8.place(x=40, y=220, anchor='w')

            if (self.rename_flag):
                text = "改名完成"
            else:
                text = "等待改名"
            text_label = Label(self.root_window, text=text)
            text_label.place(x=40, y=250, anchor='w')

            self.root_window.mainloop()

        window()


if __name__ == '__main__':
    mixImg = MixImg()
    mixImg.client()
