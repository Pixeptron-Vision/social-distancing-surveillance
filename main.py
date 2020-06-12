
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
from ui_trial import *
import ctypes

model_path = 'ssd_mobilenet_v1_coco_2018_01_28/frozen_inference_graph.pb'
detection_confidence = 0.4
shape = (800,800)
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
        images = np.ndarray((N,shape[0],shape[1],3), dtype=np.float32, buffer=existing_container.buf)
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


def terminate_processes(jobs,p):
    for i in jobs:
        i.terminate()
        i.join()
    p.isStarted = False
    p.p.terminate()
    p.p.join()

def ui_thread(ui,display):
    N = ui.formLayout.count()
    while True:
        for i in range(N):
            cf = display[i]
            cf = np.round(cf)
            cf = np.uint8(cf)
            ui.updateCamera(i, cf)
            # print('Updated')
            if i == ui.selectedIndex:
                ui.setLabeltoFrame(ui.getCameraWidget(i).currentQtFrame, ui.mainDisplay)
                ui.setDescription(i)
                ui.getCameraWidget(i).setChecked(True)
                ui.getCameraWidget(i).camera.setLineWidth(5)
                ui.getCameraWidget(i).cameraBoxTag.setLineWidth(5)
                ui.getCameraWidget(i).camera.setEnabled(True)
                ui.getCameraWidget(i).cameraBoxTag.setEnabled(True)
            # print('Rog')
        cv2.waitKey(1)

if __name__ == '__main__':
    M = 3

    sources = ['../../PNNLParkingLot2.avi',
                # '../../PNNL_Parking_LOT(1).avi',
                # '../../PNNLParkingLot2.avi',
                # '../../vid_short.mp4',
                # '../../PNNL_Parking_LOT(1).avi',
                # '../../PNNLParkingLot2.avi',
                '../../vid_short.mp4']
    N = len(sources)

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    # time.sleep(20)

    for index, ip in enumerate(sources):
        ui.addCamera(index, ip)

    # N=4
    src_images = np.zeros((N,shape[0],shape[1],3),dtype=np.float32)
    boxes = np.zeros((N,100,4),dtype=np.float32)
    scores=np.zeros((N,100),dtype=np.float32)
    classes=np.zeros((N,100),dtype=np.float32)
    num = np.zeros((N),dtype=np.int)

    img_shared = shared_memory.SharedMemory(create=True,size=src_images.nbytes,name='image_container')
    images = np.ndarray((N,shape[0],shape[1],3), dtype=np.float32, buffer=img_shared.buf)

    display_shared = shared_memory.SharedMemory(create=True,size=src_images.nbytes,name='display_container')
    display = np.ndarray((N,shape[0],shape[1],3), dtype=np.float32, buffer=display_shared.buf)
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
    # time.sleep(60)
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


    # print('Process Appending Complete')
    # thread = Thread(target=ui_thread,name='ui_thread',args=(ui,display))
    # thread.daemon = True
    # thread.start()
    ui_thread(ui,display)

    time.sleep(70)
    print('Sleep Over')
    terminate_processes(jobs,p)
    img_shared.unlink()
    boxes_shared.unlink()
    scores_shared.unlink()
    classes_shared.unlink()
    num_shared.unlink()
    sys.exit(0)
