import time
import cv2
import numpy as np

class Frame:
    
    def __init__(self):        
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2()
    
    def compare_frame(self, count, target_frame, threshold=8):
        # Apply background subtraction
        fg_mask = self.bg_subtractor.apply(target_frame)
        
        # Count non-zero pixels (foreground pixels)
        fg_pixel_count = np.count_nonzero(fg_mask)
        
        # Calculate percentage of foreground pixels
        total_pixels = target_frame.shape[0] * target_frame.shape[1]
        fg_percentage = (fg_pixel_count / total_pixels) * 100
        
        start_time = time.time()
        # Check if percentage of foreground pixels exceeds threshold
        if fg_percentage > threshold:
            cv2.imwrite('changes/changed' + str(count) + '.jpg', target_frame)
        
        # Print elapsed time
        elapsed_time = time.time() - start_time
        print(str(elapsed_time*1000) + " MiliSecond Passed")
    

def capture_frame(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    count = 0
    start_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        elapsed_time = time.time() - start_time
        if elapsed_time >= 0.1:
            print(str(elapsed_time) + " Second Passed")
            start_time = time.time()
            cv2.imwrite('frames/frame' + str(count) + '.jpg', frame)
            count += 1
    
    cap.release()
    return count

count = capture_frame('CCTV.mp4')
print(count)

frame = Frame()
for i in range(count):
    target_frame = cv2.imread('frames/frame' + str(i) + '.jpg')
    frame.compare_frame(count=i, target_frame=target_frame)