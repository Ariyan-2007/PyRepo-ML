import cv2
import time

def histogram_difference_threshold(video_path, threshold):
    cap = cv2.VideoCapture(video_path)

    frame = 0
    # Read the first frame
    ret, prev_frame = cap.read()
    start_time = time.time()
    while True:
        # Read the next frame
        frame += 1
        print("Rendering Frame:", frame)
        ret, next_frame = cap.read()

        # If unable to read the frame, break the loop
        if not ret:
            break

        # Convert frames to grayscale for faster processing
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        next_gray = cv2.cvtColor(next_frame, cv2.COLOR_BGR2GRAY)

        # Calculate histograms
        hist_prev = cv2.calcHist([prev_gray], [0], None, [256], [0, 256])
        hist_next = cv2.calcHist([next_gray], [0], None, [256], [0, 256])

        # Calculate histogram intersection
        hist_intersection = cv2.compareHist(hist_prev, hist_next, cv2.HISTCMP_INTERSECT)/100000
        print(hist_intersection)
        elapsed_time = time.time() - start_time
        # If one second has elapsed, check if the histogram intersection exceeds the threshold
        if elapsed_time >= 1:
            print(str(elapsed_time) + " Second Passed")
            start_time = time.time()
            
            if hist_intersection > threshold:
                return prev_frame, next_frame
            prev_frame = next_frame  # Update the previous frame
        
    # Release the video capture object
    cap.release()

    # If no significant difference found, return None
    return None, None

# Example usage
video_path = 'rtsp://admin:admin@192.168.1.106:554/1/h264major'
threshold = 25 # Adjust threshold as needed

prev_frame, next_frame = histogram_difference_threshold(video_path, threshold)

# Do something with the frames if a significant difference is found
if prev_frame is not None and next_frame is not None:
    cv2.imshow('Previous Frame', prev_frame)
    cv2.imshow('Next Frame', next_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No significant difference found.")