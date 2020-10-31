#!/usr/bin/env python3

import cv2, os, sys, time
import numpy as np
from threading import Thread, Semaphore, Lock

global frameQueue = []
global grayScaleQueue = []
global semaphore = Semaphore(2)
global queueLimit = 10

class extractFrames(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.video = cv2.VideoCapture('clip.mp4')
        self.maxFrames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.count = 0

    def run(self):
        success, image = video.read()

        while success and count < 72:
            if len(frameQueue) <= queueLimit:
                semaphore.acquire()
                frameQueue.append(image)
                semaphore.release()

                success, image = video.read()
                print(f'Reading frame {count}')
                count += 1

            if count == maxFrames:
                semaphore.acquire()
                frameQueue.append(-1)
                semaphore.release()
                break
        return

class convertToGrayScale(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.count = 0

    def run(self):
        while True:
            if frameQueue and len(grayScaleQueue) <= queueLimit:
                semaphore.acquire()
                frame = queue1.pop(0)
                semaphore.release()

                if type(frame) == int and frame == -1:
                    semaphore.acquire()
                    grayScaleQueue.append(-1)
                    semaphore.release()
                    break

                print(f'Converting frame {count}')
                grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                semaphore.acquire()
                grayScaleQueue.append(grayFrame)
                semaphore.release()
                count += 1
        return

class displayFrames(Thread):
