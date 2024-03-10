import time
import cv2
import numpy as np

def compare_frame(count,target_frame, threshold=10):
    
    # Read From Device
    reference_frame = cv2.imread('reference.jpg')
    
    # Assign Frame
    if reference_frame is None:
        height, width, channels = target_frame.shape
        reference_frame = np.zeros((height, width, channels), dtype=np.uint8)
        cv2.imwrite('reference.jpg', reference_frame)
        cv2.imread('reference.jpg')
    
    # Convert -> Gray Scale
    reference_gray = cv2.cvtColor(reference_frame, cv2.COLOR_BGR2GRAY)
    target_gray = cv2.cvtColor(target_frame, cv2.COLOR_BGR2GRAY)
    
    # Calculate Absolute Difference
    frame_diff = cv2.absdiff(reference_gray, target_gray)
    
    # Calculate Mean Of Absolute Difference
    mean_diff = frame_diff.mean()
    
    # Write To Device
    cv2.imwrite('reference.jpg', target_frame)
    
    if mean_diff > threshold:
        cv2.imwrite('changes/changed'+str(count)+'.jpg', target_frame)

    
def capture_frame(video_path):
    # Start Capturing Frame
    cap = cv2.VideoCapture(video_path)
    
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
        
        # Check if Elapsed Time has passed a second
        if elapsed_time >= 0.1:                           
            print(str(elapsed_time) +" Second Passed")
            start_time = time.time()            
            # Write To Device
            cv2.imwrite('frames/frame'+str(count)+'.jpg', frame)
            count+= 1
    
    
    # Release the video capture object
    cap.release()
    
    return count

            
count = capture_frame('CCTV.mp4')
print(count)
for i in range(count):
    
    target_frame = cv2.imread('frames/frame'+str(i)+'.jpg')
    compare_frame(count=i,target_frame=target_frame)
    
    