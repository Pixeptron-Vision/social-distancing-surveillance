
import numpy as np
import argparse
import cv2
import sys
from scipy.spatial import distance
import datetime as dt
import time
from threading import Thread
# VideoCaptureAsync implements separate thread for reading stream from camera
from utils.videocaptureasync import VideoCaptureAsync
from utils.frameDisplay import FrameDisplay
from utils.distanceCalc import calculate_dist
from utils.DL_model import DetectorAPI,centre_calcualtion
from utils.process_stream import VisionSurveillance , spawn_process
import multiprocessing

from multiprocessing import shared_memory , Queue

import ctypes

model_path = 'ssd_mobilenet_v1_coco_2018_01_28/frozen_inference_graph.pb'
detection_confidence = 0.4

class DetectionProcess():
    def __init__(self):
        self.isStarted=True

    def start(self,queue,N):
        self.p=multiprocessing.Process(target=self.detector,args=(queue,N))
        self.p.start()
        return self

    def detector(self,queue,N):
        odapi = DetectorAPI(model_path)
        existing_container = shared_memory.SharedMemory(name='image_container')
        images = np.ndarray((N,300,300,3), dtype=np.float32, buffer=existing_container.buf)
        # #
        boxes_shared = shared_memory.SharedMemory(name='boxes_container')
        boxes = np.ndarray((N,100,4),dtype=np.float32, buffer=boxes_shared.buf)

        scores_shared = shared_memory.SharedMemory(name='scores_container')
        scores = np.ndarray((N,100),dtype=np.float32, buffer=scores_shared.buf)

        classes_shared = shared_memory.SharedMemory(name='classes_container')
        classes = np.ndarray((N,100),dtype=np.float32, buffer=classes_shared.buf)

        num_shared = shared_memory.SharedMemory(name='num_container')
        num = np.ndarray((N),dtype=np.int, buffer=num_shared.buf)
        # count =0
        print('Detection start')
        while self.isStarted :
            if not queue.empty():
                index = queue.get()
                # if index=='Die':
                #     print('Die')
                #     break
                # else:
                img = images[index]
                boxes[index], scores[index], classes[index], num[index] = odapi.processFrame(img)
        print('Detection closed')
        existing_container.close()
        boxes_shared.close()
        scores_shared.close()
        classes_shared.close()
        num_shared.close()
        sys.exit(0)

if __name__ == '__main__':
    M = 4

    sources = ['../../PNNLParkingLot2.avi',
                '../../PNNL_Parking_LOT(1).avi',
                '../../PNNLParkingLot2.avi',
                '../../vid_short.mp4',
                '../../PNNL_Parking_LOT(1).avi',
                '../../PNNLParkingLot2.avi',
                '../../vid_short.mp4']
    N = len(sources)
    # N=4
    src_images = np.zeros((N,300,300,3),dtype=np.float32)
    boxes = np.zeros((N,100,4),dtype=np.float32)
    scores=np.zeros((N,100),dtype=np.float32)
    classes=np.zeros((N,100),dtype=np.float32)
    num = np.zeros((N),dtype=np.int)

    img_shared = shared_memory.SharedMemory(create=True,size=src_images.nbytes,name='image_container')
    images = np.ndarray((N,300,300,3), dtype=np.float32, buffer=img_shared.buf)
    #
    boxes_shared = shared_memory.SharedMemory(create=True,size=boxes.nbytes,name='boxes_container')
    boxes = np.ndarray((N,100,4),dtype=np.float32, buffer=boxes_shared.buf)

    scores_shared = shared_memory.SharedMemory(create=True,size=scores.nbytes,name='scores_container')
    scores = np.ndarray((N,100),dtype=np.float32, buffer=scores_shared.buf)

    classes_shared = shared_memory.SharedMemory(create=True,size=classes.nbytes,name='classes_container')
    classes = np.ndarray((N,100),dtype=np.float32, buffer=classes_shared.buf)

    num_shared = shared_memory.SharedMemory(create=True,size=num.nbytes,name='num_container')
    num = np.ndarray((N),dtype=np.int, buffer=num_shared.buf)

    queue = Queue()

    p = DetectionProcess().start(queue,N)
    # sources = np.array(sources)
    i=0
    jobs = []
    while i<len(sources):
        # print(i)
        if (i+M)<=len(sources):
            process = multiprocessing.Process(target=spawn_process,
                            args=(sources[i:i+M],i,queue,N))
        else:
            process = multiprocessing.Process(target=spawn_process,
                            args=(sources[i:],i,queue,N))

        process.start()
        jobs.append(process)
        i+=M

    print('Process Appending Complete')
    for i in jobs:
        i.join()
    # process = multiprocessing.Process(target=spawn_process,
    #                      args=(sources,0,queue,N))
    # process.start()
    # for i in jobs:
    #     i.terminate()
    #     i.join()
    # print('All process closed')
    p.isStarted = False
    # p.p.terminate()
    p.p.join()
    img_shared.unlink()
    boxes_shared.unlink()
    scores_shared.unlink()
    classes_shared.unlink()
    num_shared.unlink()
    sys.exit(0)
