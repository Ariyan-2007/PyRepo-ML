import cv2
import time

def background_subtraction_threshold(video_path, threshold):
    cap = cv2.VideoCapture(video_path)

    # Create background subtractor object
    bg_subtractor = cv2.createBackgroundSubtractorMOG2()

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

        # Apply background subtraction
        fg_mask = bg_subtractor.apply(prev_frame)

        # Calculate percentage of foreground pixels
        fg_percent = (cv2.countNonZero(fg_mask) / (fg_mask.shape[0] * fg_mask.shape[1])) * 100
        print(fg_percent)
        elapsed_time = time.time() - start_time
        # If one second has elapsed, check if the foreground percentage exceeds the threshold
        if elapsed_time >= 1:
            print(str(elapsed_time) + " Second Passed")
            start_time = time.time()
            if fg_percent > threshold:
                return prev_frame, next_frame
            prev_frame = next_frame  # Update the previous frame
        
    # Release the video capture object
    cap.release()

    # If no significant difference found, return None
    return None, None

# Example usage
video_path = 'CCTV.mp4'
threshold = 5  # Adjust threshold as needed

prev_frame, next_frame = background_subtraction_threshold(video_path, threshold)

# Do something with the frames if a significant difference is found
if prev_frame is not None and next_frame is not None:
    cv2.imshow('Previous Frame', prev_frame)
    cv2.imshow('Next Frame', next_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No significant difference found.")