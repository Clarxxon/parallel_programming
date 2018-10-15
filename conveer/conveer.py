from __future__ import print_function
from PIL import Image
from PIL import ImageFilter
from collections import deque
import os
import pprint
import datetime

time_start=datetime.datetime.now()
# queue -----------------------
read_queue =list()
blur_queue = list()

#read all----------------------
dir=os.listdir("/home/alexei/work/python/conveer/big_images")
print(dir)

for f in dir:
    im=Image.open("/home/alexei/work/python/conveer/big_images/"+f)
    read_queue.insert(0,im)

pprint.pprint(read_queue)


#blur--------------------------

def blur(blur_q,read_q):
    
    if(len(read_q)>0):
        normal_image=read_q.pop()
        blured_image=normal_image.filter(ImageFilter.GaussianBlur(2))
        blur_q.insert(0,blured_image)
        return(1)
    else: return(0)

while(True):
    if(blur(blur_queue,read_queue)==0):
        break

pprint.pprint(blur_queue)

""" for image in blur_queue:                   
    image.show() """


#compress----------------------
width = 200
height = 120

def resize(blur_q):
    if(len(blur_q)>0):
        normal_image=blur_q.pop()
        small_image=normal_image.resize((width, height), Image.NEAREST)
        #small_image.show()
        return(1)
    else: return(0)

while(True):
    if(resize(blur_queue)==0):
        break

time_end=datetime.datetime.now()
    
print ("time is",(time_end-time_start))