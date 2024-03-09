import cv2
import time
def frame_difference_threshold(video_path, threshold):
    cap = cv2.VideoCapture(video_path)
    
    frame = 0
    # Read the first frame
    ret, prev_frame = cap.read()
    start_time = time.time()
    while True:
        # Read the next frame
        frame= frame+1
        print("Rendering Frame: "+str(frame))
        ret, next_frame = cap.read()

        # If unable to read the frame, break the loop
        if not ret:
            break

        # Convert frames to grayscale for faster processing
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        next_gray = cv2.cvtColor(next_frame, cv2.COLOR_BGR2GRAY)

        # Calculate absolute difference between frames
        frame_diff = cv2.absdiff(prev_gray, next_gray)
        
        # Calculate the mean of the absolute difference
        mean_diff = frame_diff.mean()
        print(mean_diff)
        
        elapsed_time = time.time() - start_time
        # If the mean difference exceeds the threshold, return
        if elapsed_time >= 1:
            print(str(elapsed_time) +" Second Passed")
            start_time = time.time()
            if mean_diff > threshold:
                end_time = time.time()
                print(end_time - start_time)
                return prev_frame, next_frame
            prev_frame = next_frame 
            # Update the previous frame
            
        
        
        

    # Release the video capture object
    cap.release()
    
    # If no significant difference found, return None
    return None, None

# Example usage
video_path = 'CCTV.mp4'
threshold = 10 # Adjust threshold as needed

prev_frame, next_frame = frame_difference_threshold(video_path, threshold)

# Do something with the frames if a significant difference is found
if prev_frame is not None and next_frame is not None:
    cv2.imshow('Previous Frame', prev_frame)
    cv2.imshow('Next Frame', next_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No significant difference found.")