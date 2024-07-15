import cv2
import os
from tqdm import tqdm

# Path to the video file
video_path = 'runt_movie.mkv'
output_dir = 'frames'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Open the video file
cap = cv2.VideoCapture(video_path)

# Get the total number of frames
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Get the frame rate of the video
fps = cap.get(cv2.CAP_PROP_FPS)
frame_interval = int(fps * 3)  # 3 seconds interval

frame_count = 0
saved_frame_count = 0

# Initialize the progress bar
with tqdm(total=total_frames, desc='Processing video', unit='frame') as pbar:
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Save a frame every 3 seconds
        if frame_count % frame_interval == 0:
            frame_filename = os.path.join(output_dir, f'frame_{saved_frame_count:04d}.jpg')
            cv2.imwrite(frame_filename, frame)
            saved_frame_count += 1
        
        frame_count += 1
        pbar.update(1)  # Update the progress bar

# Release the video capture object
cap.release()

print(f"Saved {saved_frame_count} frames to {output_dir}")
