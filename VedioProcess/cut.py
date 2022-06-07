import cv2
import numpy as np
 
def video2frame(videos_path,frames_save_path,time_interval):
  '''
  :param videos_path: 视频的存放路径
  :param frames_save_path: 视频切分成帧之后图片的保存路径
  :param time_interval: 保存间隔
  :return:
  '''
  vidcap = cv2.VideoCapture(videos_path)
  success, image = vidcap.read()
  count = 0
  while success:
    success, image = vidcap.read()
    image_rot = cv2.rotate(image,  cv2.cv2.ROTATE_90_CLOCKWISE)
    count += 1
    print('第{}帧分割完成'.format(count))
    if count % time_interval == 0:
        cv2.imencode('.jpg', image_rot)[1].tofile(frames_save_path + "/%d.jpg" % count)
    # if count == 20:
    #   break
  print(count)
 
if __name__ == '__main__':
   videos_path = r'./demo.mp4'
   frames_save_path = r'./VideoToImage'
   time_interval = 1#隔一帧保存一次
   video2frame(videos_path, frames_save_path, time_interval)
