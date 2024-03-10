import time
import cv2
import numpy as np

class Frame:
    
    def __init__(self):        
        self.reference_frame = np.zeros((100, 100, 3), dtype=np.uint8)
        self.last_output_time = time.time()
    def compare_frame(self, target_frame, threshold=8):
        
        if(self.reference_frame.shape != target_frame.shape):
            height, width, channels = target_frame.shape
            self.reference_frame = np.zeros((height,width,channels), dtype=np.uint8)
            
        # Convert -> Gray Scale
        reference_gray = cv2.cvtColor(self.reference_frame, cv2.COLOR_BGR2GRAY)
        target_gray = cv2.cvtColor(target_frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate Absolute Difference
        frame_diff = cv2.absdiff(reference_gray, target_gray)
        
        # Calculate Mean Of Absolute Difference
        mean_diff = frame_diff.mean()
        
        current_time = time.time()
        elapsed_time = current_time - self.last_output_time
        print(elapsed_time)
        if mean_diff > threshold or elapsed_time >=60:
            self.last_output_time = current_time
            self.reference_frame = target_frame
            return True

        return None

    
def capture_frame(video_path):
    # Start Capturing Frame
    cap = cv2.VideoCapture('rtsp://admin:admin@192.168.1.105:554/1/h264major')
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    count=0
    # Start Timer
    start_time = time.time()
    while True:
        
        # Capture Frame
        ret, frame = cap.read()
        
        # If unable to read the frame, break the loop
        if not ret:
            break
        # Caculate Elapsed Time
        elapsed_time = time.time() - start_time    
        # count+=1
        # Check if Elapsed Time has passed a second
        if elapsed_time >= 0.1:                           
            print(str(elapsed_time) +" Second Passed")
            # print(elapsed_time, count, fps)
            start_time = time.time()  
            # count=0          
            # Write To Device
            cv2.imwrite('frames/frame'+str(count)+'.jpg', frame)
            count+= 1

    # elapsed_time = time.time() - start_time
    # print(elapsed_time, count, fps)
    # # Release the video capture object
    cap.release()
    
    return count

            
count= capture_frame('CCTV.mp4')
# count = capture_frame('rtsp://admin:admin@192.168.1.106:554/1/h264major')
print(count)
frame = Frame()
for i in range(count):
    
    target_frame = cv2.imread('frames/frame'+str(i)+'.jpg')
    acquired_frame = frame.compare_frame(target_frame=target_frame) 
    if acquired_frame:
        print("Call API & Pass Acquired Frame")
        cv2.imwrite('changes/frame'+str(count)+'.jpg', target_frame)        
    else:
        print("Null")
    