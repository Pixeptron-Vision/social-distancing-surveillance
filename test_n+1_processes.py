
import numpy as np
import argparse
import cv2
import sys
from scipy.spatial import distance
import datetime as dt
import time
from threading import Thread
# VideoCaptureAsync implements separate thread for reading stream from camera
from visionObjects.videocaptureasync import VideoCaptureAsync
from visionObjects.frameDisplay import FrameDisplay
from visionObjects.distanceCalc import calculate_dist

from human_detector import DetectorAPI
from human_detector import centre_calcualtion

import multiprocessing
from multiprocessing import shared_memory , Queue
import ctypes

import functools

model_path = 'ssd_mobilenet_v1_coco_2018_01_28/frozen_inference_graph.pb'
detection_confidence = 0.4
N=6
class VisionSurveillance:

    def __init__(self,src=0):
        self.src = src;
        self.threshold_dist = 75

    def spawn_detection(self,index_count,queue):
        self.started=True
        self.process = multiprocessing.Process(target=self.detection,args=(index_count,queue))
        self.process.start()
#
    def detection(self,index_count,queue):
        self.display_obj = FrameDisplay().start()
        self.display_obj.index=index_count
        self.cap = VideoCaptureAsync(src=self.src).start()
        # images = np.frombuffer(images,np.float32).reshape((N,300,300,3))

        existing_container = shared_memory.SharedMemory(name='image_container')
        images = np.ndarray((N,300,300,3), dtype=np.float32, buffer=existing_container.buf)

        boxes_shared = shared_memory.SharedMemory(name='boxes_container')
        boxes = np.ndarray((N,100,4),dtype=np.float32, buffer=boxes_shared.buf)

        scores_shared = shared_memory.SharedMemory(name='scores_container')
        scores = np.ndarray((N,100),dtype=np.float32, buffer=scores_shared.buf)

        classes_shared = shared_memory.SharedMemory(name='classes_container')
        classes = np.ndarray((N,100),dtype=np.float32, buffer=classes_shared.buf)

        num_shared = shared_memory.SharedMemory(name='num_container')
        num = np.ndarray((N),dtype=np.int, buffer=num_shared.buf)

        while True:
            ret, current_frame = self.cap.read()
            if not ret or current_frame is None:
                user_exit = self.display_obj.display_error()

            else:
                current_frame = cv2.resize(current_frame, (300, 300))
                images[index_count] = current_frame.copy()
                queue.put(index_count)
                # print(images[index_count])
                # print(num[index_count])
                centres,current_frame =centre_calcualtion(boxes[index_count]
                                        ,scores[index_count],classes[index_count],num[index_count],
                                        current_frame,detection_confidence)
                # #
                # # # Returns id of pairs violating the norms
                # pairs = calculate_dist(
                #     current_frame, centres, self.threshold_dist)

                user_exit = self.display_obj.update(current_frame)

            if user_exit == True:
                self.started=False
                self.cap.stop()
                self.display_obj.stop()
                existing_container.close()
                boxes_shared.close()
                scores_shared.close()
                classes_shared.close()
                num_shared.close()
                # self.process.terminate()

    def __exit__(self):
        self.cap.stop()
        self.display_obj.stop()
        existing_container.unlink()
        boxes_shared.unlink()
        scores_shared.unlink()
        classes_shared.unlink()
        num_shared.unlink()


def detector(queue):
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
    odapi = DetectorAPI(model_path)
    # count =0
    while not queue.empty():
        index = queue.get()
        img = images[index]
        # print(img)
        # print(index)
        # print(images)
        boxes[index], scores[index], classes[index], num[index] = odapi.processFrame(img)
        # print("num of detection = ",num[index],index)
        # time.sleep(1)
        # del index
        # del img
        # count+=1

    existing_container.close()
    boxes_shared.close()
    scores_shared.close()
    classes_shared.close()
    num_shared.close()


if __name__ == '__main__':
    #Note: index is passed in spawn function as indexing is important
    #       at the time of frame display...as windows are named with index
    #       to avoid mixing and overriding of frames during display.

    sources = ['../../PNNLParkingLot2.avi',
                '../../vid_short.mp4',
                '../../PNNL_Parking_LOT(1).avi',
                '../../PNNLParkingLot2.avi',
                # '../../vid_short.mp4',
                # '../../PNNL_Parking_LOT(1).avi',
                '../../PNNLParkingLot2.avi',
                '../../vid_short.mp4']
    # The below objects are the instance of VisionSurveillance visionObjects
    # and each object det is for each different cameras
    N = len(sources)
    src_images = np.zeros((N,300,300,3),dtype=np.float32)
    boxes = np.zeros((N,100,4),dtype=np.float32)
    scores=np.zeros((N,100),dtype=np.float32)
    classes=np.zeros((N,100),dtype=np.float32)
    num = np.zeros((N),dtype=np.int)

    img_shared = shared_memory.SharedMemory(create=True,size=src_images.nbytes,name='image_container')
    images = np.ndarray((N,300,300,3), dtype=np.float32, buffer=img_shared.buf)
    #
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



    stream_objects = []
    for i in sources:
        det = VisionSurveillance(src=i)
        stream_objects.append(det)


    for count,det in enumerate(stream_objects):
        det.spawn_detection(count,queue)

    # detector(queue,images,boxes,scores,classes,num)
    p=multiprocessing.Process(target=detector,args=(queue,))
    # p.daemon=True
    p.start()
    # p.join()
    # img_shared.close()
    # img_shared.unlink()
    # boxes_shared.unlink()
    # scores_shared.unlink()
    # classes_shared.unlink()
    # num_shared.unlink()
