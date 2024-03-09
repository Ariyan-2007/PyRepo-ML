import cv2

def background_subtraction(video_path, learning_rate=0.001):
    cap = cv2.VideoCapture(video_path)

    # Create background subtractor object
    bg_subtractor = cv2.createBackgroundSubtractorMOG2()

    while True:
        # Read a frame from the video
        ret, frame = cap.read()

        # If unable to read the frame, break the loop
        if not ret:
            break

        # Apply background subtraction
        fg_mask = bg_subtractor.apply(frame, learningRate=learning_rate)

        # Show the original frame and the foreground mask
        cv2.imshow('Original Frame', frame)
        cv2.imshow('Foreground Mask', fg_mask)

        # Wait for a key press; press 'q' to exit
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()

# Example usage
video_path = 'CCTV.mp4'
background_subtraction(video_path)