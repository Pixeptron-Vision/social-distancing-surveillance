
import numpy as np
import argparse
import cv2
import sys
from scipy.spatial import distance
import datetime as dt
import time
import os
from threading import Thread
# VideoCaptureAsync implements separate thread for reading stream from camera
from utils.videocaptureasync import VideoCaptureAsync
from utils.frameDisplay import FrameDisplay
from utils.distanceCalc import calculate_dist
from utils.DL_model import DetectorAPI,centre_calcualtion
from utils.process_stream import VisionSurveillance , spawn_process
import multiprocessing

from multiprocessing import shared_memory , Queue
from ui.ui_main import *
import ctypes

from utils.CSVConverter import writeToCSV, readFromCSV 

# The below model_path contains the link to frozen graph of pretrained tensorflow object detection model.
model_path = 'ssd_mobilenet_v1_coco_2018_01_28/frozen_inference_graph.pb'
# Probability of detected box to be human
detection_confidence = 0.4
# A standard shape has been fixed for all images
shape = (800,800)

# Human Detector class is responsible of initiating the object detection model
# Here the detection task is designed to run on a separate process.
class HumanDetector():
    def __init__(self):
        self.isStarted=True

    # Start function spawn the process for detection tasks and executes detector function.
    def start(self,queue,N):
        # Spawn the process and store the refernece in p
        self.p=multiprocessing.Process(target=self.detector,args=(queue,N))
        self.p.start()
        return self

    # Detector function does the detection on each image from all cams.
    # It uses a queue to receive and process the request from different cameras in a First Come First Serve basis.
    # It fetches the images of coreesponding cam from shared memory and does detection task.
    # The results of detection are the stored in a separate sahred memory container.
    def detector(self,queue,N):
        # DetectorAPI is the tensorflow Object Detection API which loads the model and performs detection
        # with help of image tensors and saved model tensors
        odapi = DetectorAPI(model_path)

        # Below the different shared memory are connected and assigned to specific numpy arrays as needed

        # The image conatiner conatins the images of all N cameras in a numpy aaray format.
        # The shape of image is fixed beforehand declared as global variable on start of this script as 'shape'
        image_container = shared_memory.SharedMemory(name='image_container')
        # Reshape the connected memory in desired numpy aaray and assign to local variable image
        images = np.ndarray((N,shape[0],shape[1],3), dtype=np.float32, buffer=image_container.buf)

        # Boxes shared stores the vertices of the rectangular boxes of all cameras given by the detectorAPI
        boxes_shared = shared_memory.SharedMemory(name='boxes_container')
        boxes = np.ndarray((N,100,4),dtype=np.float32, buffer=boxes_shared.buf)

        # Scores stores the probability of each predicted boxes
        scores_shared = shared_memory.SharedMemory(name='scores_container')
        scores = np.ndarray((N,100),dtype=np.float32, buffer=scores_shared.buf)

        # Classes stores the class index of boxes predicted by the detector
        # Note: The detector currently being used does multiclass detection
        classes_shared = shared_memory.SharedMemory(name='classes_container')
        classes = np.ndarray((N,100),dtype=np.float32, buffer=classes_shared.buf)

        # num stores the total number of objects detected in a frame.
        num_shared = shared_memory.SharedMemory(name='num_container')
        num = np.ndarray((N),dtype=np.int, buffer=num_shared.buf)

        status_flag_memory = shared_memory.SharedMemory(name='status_flag_container')
        status_flag = np.ndarray((N), dtype=bool, buffer=status_flag_memory.buf)
        # Start the while loop till user exits it and performs the detection.
        # The index of cameras who has requested for detection is fetched from queue
        # The request are adhered in First Come First Serve basis
        # print('Detection start')
        while self.isStarted :
            if not queue.empty():
                # get index or Cam ID of cam with first request from queue
                index = queue.get()
                if status_flag[index]:
                    # Fetch most recent image of indexed camera from the shared memory
                    img = images[index]
                    # processFrame does the detection on image feeded to it
                    # Store the results like boxes , scores , classes,num of the respective frame in the
                    # shared memory with the cam id as index
                    boxes[index], scores[index], classes[index], num[index] = odapi.processFrame(img)
        # print('Detection closed')
        # After exit of while loop disconnect all shared memory.
        image_container.close()
        boxes_shared.close()
        scores_shared.close()
        classes_shared.close()
        num_shared.close()
        sys.exit(0)

def start_streams_process(sources,M,queue,N,save_dir):
    i=0
    jobs = []
    while i<len(sources):
        # print(i)
        if (i+M)<=len(sources):
            process = multiprocessing.Process(target=spawn_process,
                            args=(sources[i:i+M],i,queue,N,save_dir))
        else:
            process = multiprocessing.Process(target=spawn_process,
                            args=(sources[i:],i,queue,N,save_dir))

        process.start()
        jobs.append(process)
        i+=M

    return jobs


# T=terminate Process is responsible for killing all the processes initiated by this programe for different cameras
def terminate_processes(jobs,detector_process):

    for process in jobs:
        process.terminate()
        process.join()


def update_UI(ui,MainWindow,dispaly,frame_data,current_cam_count,sources):
    # Append the different cameras and their sources in the UI
    for index, src in enumerate(sources):
        ui.addCamera(index,src[0],tag=src[1])

    current_cam_count=len(sources)
    while True:
        if ui.removeStreamTrigger:
            status_flag[ui.removeStreamId]=False
            ui.removeStreamTrigger=False
            sources.pop(ui.removeStreamId)
            ui.clearWidgets()
            # Returns restart or exit
            return True

        if ui.newStreamTrigger:
            ui.newStreamTrigger=False
            sources.append([ui.newStreamDict['ip'],ui.newStreamDict['tag']])
            ui.newStreamDict.clear()
            ui.clearWidgets()
            return True

        if ui.editStreamTrigger:
            ui.editStreamTrigger=False
            sources[ui.editStreamDict['id']] = [ ui.editStreamDict['ip'], ui.editStreamDict['tag'] ]
            ui.editStreamDict.clear()
            if ui.editStreamIPTrigger:
                ui.editStreamIPTrigger = False
                ui.clearWidgets()
                return True

        for i in range(current_cam_count):
            if status_flag[i]:
                # cf = current _frame : extract current frame from sahred memory
                cf = display[i]
                cf = np.round(cf)
                cf = np.uint8(cf)
                # update the frame in respective window in UI
                ui.updateCamera(i, cf,frame_data[i][0],frame_data[i][1]
                                    ,frame_data[i][2],frame_data[i][3])

                # selectedIndex show the index of camera which is in focus in Main Window
                if i == ui.selectedIndex:
                    ui.setLabeltoFrame(ui.getCameraWidget(i).currentQtFrame, ui.mainDisplay)
                    ui.setDescription(i)
                    ui.getCameraWidget(i).setChecked(True)
                    ui.getCameraWidget(i).camera.setLineWidth(5)
                    ui.getCameraWidget(i).cameraBoxTag.setLineWidth(5)
                ui.getCameraWidget(i).camera.setEnabled(True)
                ui.getCameraWidget(i).cameraBoxTag.setEnabled(True)
                

        cv2.waitKey(1)
        if not MainWindow.isVisible():
            # print('exit')
            return False



if __name__ == '__main__':
    #Code to support multiprocessing module for application packaging using pyinstaller
    multiprocessing.freeze_support()

    # M show the max number of cam we are willing to run in one process
    M = 4
    # N will show the max no. of cameras the program is able to handle i.e. upper threshold of no. of cams
    N = 50

    # Sets directory for saving the vilation images
    name = os.getcwd()
    save_dir = os.path.join(name,'captures')
    try:
        os.mkdir(save_dir)  
    except OSError as error:  
        pass 

    CameraIPData = 'CameraIPData'
    '''
    sources = [['../Dataset/PNNLParkingLot2.avi','t1'],
                ['../Dataset/PNNL_Parking_LOT(1).avi','t2'],
                ['../Dataset/PNNLParkingLot2.avi','t3'],
                ['../Dataset/walking.avi',''],
                ['../Dataset/PNNL_Parking_LOT(1).avi',''],
                ['../Dataset/PNNLParkingLot2.avi','']]
    '''
    sources = readFromCSV(filename = CameraIPData)

    # N = total number of streams to process
    current_cam_count = len(sources)

    # The below commands initiate some memories in the volatile spaces ehich can be shared and accesses from
    # all the different processes

    # First we make some standard variable which will decide the size of shared memory containers.

    images = np.zeros((N,shape[0],shape[1],3),dtype=np.float32)
    boxes = np.zeros((N,100,4),dtype=np.float32)
    scores=np.zeros((N,100),dtype=np.float32)
    classes=np.zeros((N,100),dtype=np.float32)
    num = np.zeros((N),dtype=np.int)
    frame_data = np.zeros((N,4),dtype=np.int)
    status_flag = np.zeros((N),dtype=bool)

    # The image conatiner conatins the images of all N cameras in a numpy aaray format.
    # The shape of image is fixed beforehand declared as global variable on start of this script as 'shape'
    try:
        img_shared = shared_memory.SharedMemory(create=True,size=images.nbytes,name='image_container')
    except FileExistsError:
        img_shared = shared_memory.SharedMemory(name='image_container')
    images = np.ndarray((N,shape[0],shape[1],3), dtype=np.float32, buffer=img_shared.buf)

    try:
        display_shared = shared_memory.SharedMemory(create=True,size=images.nbytes,name='display_container')
    except FileExistsError:
        display_shared = shared_memory.SharedMemory(name='display_container')
    display = np.ndarray((N,shape[0],shape[1],3), dtype=np.float32, buffer=display_shared.buf)

    try:
        boxes_shared = shared_memory.SharedMemory(create=True,size=boxes.nbytes,name='boxes_container')
    except FileExistsError:
        boxes_shared = shared_memory.SharedMemory(name='boxes_container')
    boxes = np.ndarray((N,100,4),dtype=np.float32, buffer=boxes_shared.buf)

    try:
        scores_shared = shared_memory.SharedMemory(create=True,size=scores.nbytes,name='scores_container')
    except FileExistsError:
        scores_shared = shared_memory.SharedMemory(name='scores_container')
    scores = np.ndarray((N,100),dtype=np.float32, buffer=scores_shared.buf)

    try:
        classes_shared = shared_memory.SharedMemory(create=True,size=classes.nbytes,name='classes_container')
    except FileExistsError:
        classes_shared = shared_memory.SharedMemory(name='classes_container')
    classes = np.ndarray((N,100),dtype=np.float32, buffer=classes_shared.buf)
    try:
        num_shared = shared_memory.SharedMemory(create=True,size=num.nbytes,name='num_container')
    except FileExistsError:
        num_shared = shared_memory.SharedMemory(name='num_container')
    num = np.ndarray((N),dtype=np.int, buffer=num_shared.buf)

    try:
        status_flag_memory = shared_memory.SharedMemory(create=True,size=status_flag.nbytes,name='status_flag_container')
    except FileExistsError:
        status_flag_memory = shared_memory.SharedMemory(name='status_flag_container')
    status_flag = np.ndarray((N),dtype=bool, buffer=status_flag_memory.buf)

    # Frame data will store all the data and parameters like no. of humans , no. of safe and unsafe humans
    # of processed frame in the shared memory which can be accessed by the UI
    try:
        frame_data_memory = shared_memory.SharedMemory(create=True,size=frame_data.nbytes,name='frame_data_container')
    except FileExistsError:
        frame_data_memory = shared_memory.SharedMemory(name='frame_data_container')
    frame_data = np.ndarray((N,4), dtype=np.float32, buffer=frame_data_memory.buf)

    queue = Queue()


    detector_process = HumanDetector().start(queue,N)

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
# ////////////////////////////////////////////////////////////////////////////////////

    while True:
        jobs = start_streams_process(sources,M,queue,N,save_dir)

        rest = update_UI(ui,MainWindow,display,frame_data,current_cam_count,sources)

        terminate_processes(jobs,detector_process)

        if not rest:
            break

    # print('Saving sources to CSV')
    writeToCSV(CameraIPData, sources)
    
    # print('Clear Garbage')
    terminate_processes(jobs,detector_process)
    # close the detector process i.e. HumanDetection class
    detector_process.isStarted = False
    detector_process.p.terminate()
    detector_process.p.join()
    # Erase all the reserved memory
    img_shared.unlink()
    display_shared.unlink()
    boxes_shared.unlink()
    scores_shared.unlink()
    classes_shared.unlink()
    num_shared.unlink()
    status_flag_memory.unlink()
    frame_data_memory.unlink()
    sys.exit(0)
