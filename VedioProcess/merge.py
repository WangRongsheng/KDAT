import cv2
import os
import numpy as np
from PIL import Image
 
 
def frame2video(im_dir,video_dir,fps):
    im_list = os.listdir(im_dir)
    im_list.sort(key=lambda x: int(x.split('.')[0]))  #最好再看看图片顺序对不
    img = Image.open(os.path.join(im_dir,im_list[0]))
    img_size = img.size #获得图片分辨率，im_dir文件夹下的图片分辨率需要一致
 
    # fourcc = cv2.cv.CV_FOURCC('M','J','P','G') #opencv版本是2
    fourcc = cv2.VideoWriter_fourcc(*'XVID') #opencv版本是3
    videoWriter = cv2.VideoWriter(video_dir, fourcc, fps, img_size)
    # count = 1
    for i in im_list:
        im_name = os.path.join(im_dir+i)
        frame = cv2.imdecode(np.fromfile(im_name, dtype=np.uint8), -1)
        videoWriter.write(frame)
        # count+=1
        # if (count == 200):
        #     print(im_name)
        #     break
    videoWriter.release()
    print('finish')
 
if __name__ == '__main__':
    im_dir =  r'D:\project\android\demo\demo_mask/'#帧存放路径
    video_dir = r'D:\project\android\demo\demo_mask.mp4' #合成视频存放的路径
    fps = 24 #帧率，每秒钟帧数越多，所显示的动作就会越流畅
    frame2video(im_dir, video_dir, fps)
