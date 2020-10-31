#!/usr/bin/env python3

import cv2, os, sys, time
import numpy as np
from threading import Thread, Semaphore, Lock

frameQueue = []
grayScaleQueue = []
semaphore = Semaphore(2)
queueLimit = 10

class ExtractFrames(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.video = cv2.VideoCapture('clip.mp4')
        self.maxFrames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.count = 0

    def run(self):
        success, image = self.video.read()

        while success and self.count <= 72:
            if len(frameQueue) <= queueLimit:
                semaphore.acquire()
                frameQueue.append(image)
                semaphore.release()

                success, image = self.video.read()
                print(f'Reading frame {self.count}')
                self.count += 1

            if self.count == self.maxFrames:
                semaphore.acquire()
                frameQueue.append(-1)
                semaphore.release()
                break
        print('Frame extraction complete')

class ConvertToGrayScale(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.count = 0

    def run(self):
        while self.count <= 72:
            if frameQueue and len(grayScaleQueue) <= queueLimit:
                semaphore.acquire()
                frame = frameQueue.pop(0)
                semaphore.release()

                if type(frame) == int and frame == -1:
                    semaphore.acquire()
                    grayScaleQueue.append(-1)
                    semaphore.release()
                    break

                print(f'Converting frame {self.count}')
                grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                semaphore.acquire()
                grayScaleQueue.append(grayFrame)
                semaphore.release()
                self.count += 1

        print('Finished converting to gray scale')          

class DisplayFrames(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.delay = 42
        self.count = 0

    def run(self):
        while self.count <= 72:
            if grayScaleQueue:
                semaphore.acquire()
                frame = grayScaleQueue.pop(0)
                semaphore.release()

                if type(frame) == int and frame == -1:
                    break

                print(f'Displaying Frame {self.count}')
                cv2.imshow('Video', frame)
                self.count += 1

                if cv2.waitKey(self.delay) and 0xFF == ord('q'):
                    break
        
        print('Finished displaying all frames')
        cv2.destroyAllWindows()


#run all threads concurrently
extractFrames = ExtractFrames()
extractFrames.start()
convertToGrayScale = ConvertToGrayScale()
convertToGrayScale.start()
displayFrames = DisplayFrames()
displayFrames.start()
