#!/usr/bin/env python3
import cv2
import numpy as np
import argparse

def loadVideo(FILE):
    capture = cv2.VideoCapture(FILE)
    while(True):
        ret, frame = capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", type=str, help="Filepath for Input Video")
    args = vars(ap.parse_args())
    loadVideo(args["video"])

if __name__ == "__main__":
    main()
