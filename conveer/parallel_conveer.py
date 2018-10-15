from __future__ import print_function
from PIL import Image
from PIL import ImageFilter
from collections import deque
import os
import datetime
import multiprocessing
import pprint
from multiprocessing import Pool
from multiprocessing import Process, Queue,Value, Array,Manager

import scipy
import base64
# queue -----------------------

width = 200
height = 120


#read all----------------------
def read(q,lock):
   
    dir_=os.listdir("/home/alexei/work/python/conveer/big_images")
    print(dir_)

    for f in dir_:
        im=Image.open("/home/alexei/work/python/conveer/big_images/"+f)
        q.df.appendleft(im)
    
    q.df.appendleft('READ_DONE')
    return(0)


#blur--------------------------

def async_blur_worker(original_list,blur_list,lock):
    #lock.acquire()
 
    while(True):
        
        if(len(original_list)>0):
            im=(original_list.pop())
            if(im=='READ_DONE'):
                blur_list.insert(0,'BLUR_DONE')
                break
            print("blur...")
            blur_list.insert(0,im.filter(ImageFilter.GaussianBlur(2)))
        
    #print("blur done!")
    #lock.release()





#compress----------------------

def async_resize_worker(original_list,resize_list,lock):

    #lock.acquire()
 
    while(True):
        
        if(len(original_list)>0):
            im=(original_list.pop())
            if(im=='BLUR_DONE'):
                break
            width = 200
            height = 120
            print("resize...")
            small_image=im.resize((width, height), Image.NEAREST)
            #small_image.show()
            
        
    #print("blur done!")
    #lock.release()




if __name__ == '__main__':
    time_start=datetime.datetime.now()
    lock = ''

    mgr = Manager()
    l_read=mgr.list()
    l_blur=mgr.list()
    l_resize=mgr.list()

    #read-------------
    dir_=os.listdir("/home/alexei/work/python/conveer/big_images")
    for f in dir_:
        im=Image.open("/home/alexei/work/python/conveer/big_images/"+f)
        l_read.insert(0,im)
    
    l_read.insert(0,'READ_DONE')
    

    #workers----------
    p2 = Process(target=async_blur_worker, args=(l_read,l_blur,lock,))
    p2.start()
    
    p3 = Process(target=async_resize_worker, args=(l_blur,l_resize,lock,))
    p3.start()

    p2.join()
    p3.join() 
    
    time_end=datetime.datetime.now()
    
    print ("time is",(time_end-time_start))