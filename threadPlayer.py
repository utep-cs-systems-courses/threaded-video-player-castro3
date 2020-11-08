#!/usr/bin/env python3

#Oscar Castro
#Producer Consumer Lab

import cv2, os, sys, time
import numpy as np
from threading import Thread, Semaphore, Lock

class ThreadQ():
    def __init__(self, qCapacity):
        self.queue = []
        self.full = Semaphore(0)
        self.empty = Semaphore(24)
        self.lock = Lock()
        self.qCapacity = qCapacity
        
    def putFrame(self, frame):
        self.empty.acquire()
        self.lock.acquire()
        self.queue.append(frame)
        self.lock.release()
        self.full.release()
        
    def getFrame(self):
        self.full.acquire()
        self.lock.acquire()
        frame = self.queue.pop(0)
        self.lock.release()
        self.empty.release()
        return frame

class ExtractFrames(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.video = cv2.VideoCapture('clip.mp4')
        self.maxFrames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.count = 0

    def run(self):
        success, image = self.video.read()

        while True:
            if success and len(frameQueue.queue) <= frameQueue.qCapacity:
                frameQueue.putFrame(image)

                success, image = self.video.read()
                print(f'Reading Frame {self.count}')
                self.count += 1
                
            if self.count == self.maxFrames:
                frameQueue.putFrame(-1)
                break
                
        print('Frame extraction complete')

class ConvertToGrayScale(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.count = 0

    def run(self):
        while True:
            if frameQueue.queue and len(grayScaleQueue.queue) <= grayScaleQueue.qCapacity:
                frame = frameQueue.getFrame()
                
                if type(frame) == int and frame == -1:
                    grayScaleQueue.putFrame(-1)
                    break

                print(f'Converting Frame {self.count}')
                grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                grayScaleQueue.putFrame(grayFrame)
                self.count += 1

        print('Finished converting to gray scale')          

class DisplayFrames(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.delay = 42
        self.count = 0

    def run(self):
        while True:
            if grayScaleQueue.queue:
                frame = grayScaleQueue.getFrame()
                
                if type(frame) == int and frame == -1:
                    break

                print(f'Displaying Frame {self.count}')
                cv2.imshow('Video', frame)
                self.count += 1

                if cv2.waitKey(self.delay) and 0xFF == ord('q'):
                    break
        
        print('Finished displaying all frames')
        cv2.destroyAllWindows()
        
#set up thread queues
frameQueue = ThreadQ(9)
grayScaleQueue = ThreadQ(9)

#run all threads concurrently
extractFrames = ExtractFrames()
extractFrames.start()
convertToGrayScale = ConvertToGrayScale()
convertToGrayScale.start()
displayFrames = DisplayFrames()
displayFrames.start()
