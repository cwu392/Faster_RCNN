import cv2
import sys
import os
if len(sys.argv) != 2:
	print("Usage: crop_images.py <path of mp4 file>")
else:
	#input /home/ubuntu/25videos/2018-01-26_10-44-52-264_cam.mp4
	mp4_path = sys.argv[1]
	img_folder = sys.argv[1].replace('.mp4', '') + '/'
	if not os.path.exists(img_folder):
	    os.makedirs(img_folder)
	vidcap = cv2.VideoCapture(mp4_path)
	success, image = vidcap.read()
	count = 1
	while success:
	  cv2.imwrite(img_folder + "%07d.jpg" % count, image)     # save frame as JPEG file      
	  success, image = vidcap.read()
	  print('Read a new frame: ', success)
	  count += 1
