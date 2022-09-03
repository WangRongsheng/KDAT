'''
数据增强方法测试
1. 像素级：HSV增强、旋转、平移、缩放、剪切、透视、翻转等
2. 图片级：MixUp、Cutout、CutMix、Mosaic、Copy-Paste等
'''
import math
import os
import random
import cv2
import numpy as np


# 将图像的最长边缩放到640，短边填充到640
def fix_shape(imgs, new_shape=(640, 640), color=(114, 114, 114)):
    new_imgs = []
    for img in imgs:
        shape = img.shape[:2]  # current shape [height, width]
        # Scale ratio (new / old)
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        # Compute padding
        ratio = r, r  # width, height ratios
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
        dw /= 2  # divide padding into 2 sides
        dh /= 2
        if shape[::-1] != new_unpad:  # resize
            img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
        new_imgs.append(img)
    return new_imgs


# 将xywh形式的标签信息转化为xyxy形式
def xywhn2xyxy(x, w=640, h=640, padw=0, padh=0):
    # Convert nx4 boxes from [x, y, w, h] normalized to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
    y = np.copy(x)
    y[:, 0] = w * (x[:, 0] - x[:, 2] / 2) + padw  # top left x
    y[:, 1] = h * (x[:, 1] - x[:, 3] / 2) + padh  # top left y
    y[:, 2] = w * (x[:, 0] + x[:, 2] / 2) + padw  # bottom right x
    y[:, 3] = h * (x[:, 1] + x[:, 3] / 2) + padh  # bottom right y
    return y


# 绘制带有GT框图像
def plot_box(img, label, line_thickness=3):
    colors = [[np.random.randint(0, 255) for _ in range(3)] for _ in range(len(label))]
    for i, l in enumerate(label):
        color = colors[i % len(colors)]
        # tl = 框框的线宽  要么等于line_thickness要么根据原图im长宽信息自适应生成一个
        tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
        # c1 = (x1, y1) = 矩形框的左上角   c2 = (x2, y2) = 矩形框的右下角
        c1, c2 = (int(l[1]), int(l[2])), (int(l[3]), int(l[4]))
        # cv2.rectangle: 在im上画出框框   c1: start_point(x1, y1)  c2: end_point(x2, y2)
        # 注意: 这里的c1+c2可以是左上角+右下角  也可以是左下角+右上角都可以
        cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)


# YOLOv5 4-mosaic loader. Loads 1 image + 3 random images into a 4-image mosaic
def mosaic(imgs, labels, img_size=640):
    labels4 = []
    s = img_size
    mosaic_border = [-s // 2, -s // 2]
    # 从点A（s/2, s/2）和点B（3s/2, 3s/2）限定的矩形内随机选择一点作为拼接点
    yc, xc = (int(random.uniform(-x, 2 * s + x)) for x in mosaic_border)  # mosaic center x, y
    for i in range(len(imgs)):
        img = imgs[i]
        h, w = img.shape[:2]
        # place img in img4
        if i == 0:  # top left
            # 创建马赛克图像 [1280, 1280, 3]=[h, w, c] base image with 4 tiles
            img4 = np.full((s * 2, s * 2, imgs[0].shape[2]), 114, dtype=np.uint8)
            # xmin, ymin, xmax, ymax (large image)
            # 计算马赛克图像中的坐标信息(将图像填充到马赛克图像中)
            # 马赛克图像【大图】：(x1a,y1a)左上角，(x2a,y2a)右下角
            x1a, y1a, x2a, y2a = max(xc - w, 0), max(yc - h, 0), xc, yc
            # xmin, ymin, xmax, ymax (small image)
            # 计算截取的图像区域信息(以xc,yc为第一张图像的右下角坐标填充到马赛克图像中，丢弃越界的区域)
            # 要拼接的图像【小图】：(x1b,y1b)左上角 (x2b,y2b)右下角
            x1b, y1b, x2b, y2b = w - (x2a - x1a), h - (y2a - y1a), w, h
        elif i == 1:  # top right
            x1a, y1a, x2a, y2a = xc, max(yc - h, 0), min(xc + w, s * 2), yc
            x1b, y1b, x2b, y2b = 0, h - (y2a - y1a), min(w, x2a - x1a), h
        elif i == 2:  # bottom left
            x1a, y1a, x2a, y2a = max(xc - w, 0), yc, xc, min(s * 2, yc + h)
            x1b, y1b, x2b, y2b = w - (x2a - x1a), 0, w, min(y2a - y1a, h)
        elif i == 3:  # bottom right
            x1a, y1a, x2a, y2a = xc, yc, min(xc + w, s * 2), min(s * 2, yc + h)
            x1b, y1b, x2b, y2b = 0, 0, min(w, x2a - x1a), min(y2a - y1a, h)
        # img4[ymin:ymax, xmin:xmax]
        # 将截取的图像区域填充到马赛克图像的相应位置   img4[h, w, c]
        # 将图像img的【(x1b,y1b)左上角 (x2b,y2b)右下角】区域截取出来填充到马赛克图像的【(x1a,y1a)左上角 (x2a,y2a)右下角】区域
        img4[y1a:y2a, x1a:x2a] = img[y1b:y2b, x1b:x2b]  # img4[ymin:ymax, xmin:xmax]

        # 计算小图填充到大图时所产生的偏移 用来计算mosaic数据增强后 标签框的位置
        padw = x1a - x1b
        padh = y1a - y1b

        # 处理图像的labels信息
        label = labels[i].copy()
        if label.size:
            # normalized xywh to pixel xyxy format
            label[:, 1:] = xywhn2xyxy(label[:, 1:], w, h, padw, padh)
        labels4.append(label)

    # Concat/clip labels
    # 把label4中4张小图的信息整合到一起
    labels4 = np.concatenate(labels4, 0)
    for x in (labels4[:, 1:]):
        np.clip(x, 0, 2 * s, out=x)  # clip when using random_perspective()

    return img4, labels4


# 1. 像素级：HSV增强、旋转、平移、缩放、剪切、透视、翻转等
def pix_augment(img, method):
    width = img.shape[1]
    height = img.shape[0]

    # 上下垂直翻转
    if method == 'flipud':
        img = np.flipud(img)

    # 左右水平翻转
    elif method == 'fliplr':
        img = np.fliplr(img)

    # hsv色域变换
    elif method == 'hsv':
        """hsv色域增强  处理图像hsv，不对label进行任何处理
        :param img: 待处理图片  BGR [736, 736]
        :param hgain: h通道色域参数 用于生成新的h通道
        :param sgain: h通道色域参数 用于生成新的s通道
        :param vgain: h通道色域参数 用于生成新的v通道
        :return: 返回hsv增强后的图片 img
        """
        hgain, sgain, vgain = 0.015, 0.7, 0.4
        if hgain or sgain or vgain:
            # 随机取-1到1三个实数，乘以hyp中的hsv三通道的系数  用于生成新的hsv通道
            r = np.random.uniform(-1, 1, 3) * [hgain, sgain, vgain] + 1  # random gains
            hue, sat, val = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2HSV))  # 图像的通道拆分 h s v
            dtype = img.dtype  # uint8

            # 构建查找表
            x = np.arange(0, 256, dtype=r.dtype)
            lut_hue = ((x * r[0]) % 180).astype(dtype)  # 生成新的h通道
            lut_sat = np.clip(x * r[1], 0, 255).astype(dtype)  # 生成新的s通道
            lut_val = np.clip(x * r[2], 0, 255).astype(dtype)  # 生成新的v通道

            # 图像的通道合并 img_hsv=h+s+v  随机调整hsv之后重新组合hsv通道
            # cv2.LUT(hue, lut_hue)   通道色域变换 输入变换前通道hue 和变换后通道lut_hue
            img_hsv = cv2.merge((cv2.LUT(hue, lut_hue), cv2.LUT(sat, lut_sat), cv2.LUT(val, lut_val)))
            # no return needed  dst:输出图像
            cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR, dst=img)

    # 旋转
    elif method == 'rotation':
        a = random.uniform(-45, 45)
        R = cv2.getRotationMatrix2D(angle=a, center=(width / 2, height / 2), scale=1)
        img = cv2.warpAffine(img, R, dsize=(width, height), borderValue=(114, 114, 114))

    # 缩放
    elif method == 'scale':
        img = cv2.resize(img, dsize=(640, 640))

    # 剪切
    # https://blog.csdn.net/LaoYuanPython/article/details/113856503
    elif method == 'shear':
        S = np.eye(3)
        sh = 20.0
        S[0, 1] = math.tan(random.uniform(-sh, sh) * math.pi / 180)  # x shear (deg)
        S[1, 0] = math.tan(random.uniform(-sh, sh) * math.pi / 180)  # y shear (deg)
        img = cv2.warpAffine(img, S[:2], dsize=(width, height), borderValue=(114, 114, 114))

    # 平移
    elif method == 'translation':
        T = np.eye(3)
        tr = 0.1
        T[0, 2] = random.uniform(0.5 - tr, 0.5 + tr) * width  # x translation (pixels)
        T[1, 2] = random.uniform(0.5 - tr, 0.5 + tr) * height  # y translation (pixels)
        img = cv2.warpAffine(img, T[:2], dsize=(width, height), borderValue=(114, 114, 114))

    # 透视变换
    # 透视变换原理实例代码详解：https://xiulian.blog.csdn.net/article/details/104281693
    elif method == 'perspective':
        P = np.eye(3)
        pe = 0.001
        P[2, 0] = random.uniform(-pe, pe)  # x perspective (about y)
        P[2, 1] = random.uniform(-pe, pe)  # y perspective (about x)
        img = cv2.warpPerspective(img, P, dsize=(width, height), borderValue=(114, 114, 114))

    return img


# 2. 图片级：MixUp、Cutout、CutMix、Mosaic、Copy-Paste等
def img_augment(imgs, labels, method):
    if method == 'mixup':
        # 填充到相同大小 640 × 640
        imgs[:2] = fix_shape(imgs[:2])
        img1 = imgs[0]
        img2 = imgs[1]
        # 显示原图
        htitch = np.hstack((img1, img2))
        cv2.imshow("origin images", htitch)
        cv2.waitKey(0)
        cv2.imwrite('outputs/mixup_origin.jpg', htitch)
        # mixup ratio, alpha=beta=32.0
        r = np.random.beta(32.0, 32.0)
        imgs = (img1 * r + img2 * (1 - r)).astype(np.uint8)
        return imgs

    elif method == 'cutout':
        img = imgs[0]
        cv2.imshow("origin images", img)
        cv2.waitKey(0)
        height, width = img.shape[:2]
        # image size fraction
        scales = [0.5] * 1 + \
                 [0.25] * 2 + \
                 [0.125] * 4 + \
                 [0.0625] * 8 + \
                 [0.03125] * 16
        # create random masks
        for s in scales:
            # mask box shape
            mask_h = random.randint(1, int(height * s))
            mask_w = random.randint(1, int(width * s))

            # mask box coordinate
            xmin = max(0, random.randint(0, width) - mask_w // 2)  # 左上角 x坐标
            ymin = max(0, random.randint(0, height) - mask_h // 2)  # 左上角 y坐标
            xmax = min(width, xmin + mask_w)  # 右下角 x坐标
            ymax = min(height, ymin + mask_h)  # 右下角 y坐标

            # apply random color mask
            color = [random.randint(64, 191) for _ in range(3)]
            # color = [0, 0, 0]
            img[ymin:ymax, xmin:xmax] = color
        return img

    elif method == 'cutmix':
        # 这里未做fix_shape处理 两张图片大小不一样
        img1, img2 = imgs[0], imgs[1]
        h1, h2 = img1.shape[0], img2.shape[0]
        w1, w2 = img1.shape[1], img2.shape[1]
        # 设定lamda的值，服从beta分布
        alpha = 1.0
        lam = np.random.beta(alpha, alpha)
        cut_rat = np.sqrt(1. - lam)
        # 裁剪第二张图片
        cut_w = int(w2 * cut_rat)  # 要裁剪的图片宽度
        cut_h = int(h2 * cut_rat)  # 要裁剪的图片高度
        # uniform
        cx = np.random.randint(w2)  # 随机裁剪位置
        cy = np.random.randint(h2)

        # 限制裁剪的坐标区域不超过2张图片大小的最小值
        xmin = np.clip(cx - cut_w // 2, 0, min(w1, w2))  # 左上角x
        ymin = np.clip(cy - cut_h // 2, 0, min(h1, h2))  # 左上角y
        xmax = np.clip(cx + cut_w // 2, 0, min(w1, w2))  # 右下角x
        ymax = np.clip(cy + cut_h // 2, 0, min(h1, h2))  # 右下角y

        # 裁剪区域混合
        img1[ymin:ymax, xmin:xmax] = img2[ymin:ymax, xmin:xmax]
        return img1

    elif method == 'mosaic':
        imgs4, labels4 = mosaic(imgs, labels)
        return imgs4, labels4


# 1. 像素级数据增强 只需要载入1张图片
def pix_main():
    PATH = 'images/3.jpg'
    ori_img = cv2.imread(filename=PATH)
    cv2.imshow("test_image", ori_img)
    cv2.waitKey(0)
    # 进行数据增强
    out_img = pix_augment(ori_img, method='perspective')
    cv2.imshow("test_image", out_img)
    cv2.waitKey(0)
    cv2.imwrite('outputs/perspective.jpg', out_img)


# 2. 图片级数据增强 需要载入2张以上的图片
def img_main():
    IMAGE_PATH = 'images/'
    LABEL_PATH = 'labels/'

    # 读取文件夹中的图片
    ori_imgs = []
    for filename in os.listdir(IMAGE_PATH):
        filename = IMAGE_PATH + filename
        img = cv2.imread(filename)
        ori_imgs.append(img)  # 将所有图片存入list集合中

    # 读取文件夹中的标签信息
    ori_labels = []
    for filename in os.listdir(LABEL_PATH):
        with open(LABEL_PATH + filename) as f:
            label = np.array([x.split() for x in f.read().strip().splitlines()], dtype=np.float32)  # labels
        ori_labels.append(label)  # 将所有标签信息存入list集合中

    # mixup、cutout、cutmix数据增强
    out_img = img_augment(ori_imgs, None, method='cutmix')
    # Mosaic数据增强
    # out_img, out_labels = img_augment(ori_imgs, ori_labels, method='mixup')
    # 绘图
    cv2.imshow("output image", out_img)
    cv2.waitKey(0)
    cv2.imwrite('outputs/cutmix.jpg', out_img)

    # mosaic绘制标签
    # plot_box(out_img, out_labels)
    # cv2.imshow("output image", out_img)
    # cv2.waitKey(0)
    # cv2.imwrite('outputs/mosaic_with_label.jpg', out_img)


if __name__ == '__main__':
    # pix_main()  # 像素级数据增强
    img_main()  # 图片级数据增强
