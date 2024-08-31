import cv2
import os
import argparse
import math

def get_video_fps(video_path):
    # Open the video file
    video = cv2.VideoCapture(video_path)
    
    # Check if the video was opened successfully
    if not video.isOpened():
        print(f"Error: Could not open video {video_path}")
        return None
    
    # Get the FPS
    fps = video.get(cv2.CAP_PROP_FPS)
    
    # Release the video capture object
    video.release()
    
    return fps


def extract_frames(video_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(video_path)
    
    # Get the total number of frames
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Determine the number of digits needed
    num_digits = math.ceil(math.log10(total_frames + 1))

    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_path = os.path.join(output_folder, f"frame_{frame_count:0{num_digits}d}.png")
        cv2.imwrite(frame_path, frame)
        frame_count += 1

    cap.release()
    print(f"Extracted {frame_count} frames to {output_folder}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract frames from a video.")
    parser.add_argument("video_path", type=str, help="Path to the video file.")
    parser.add_argument("output_folder", type=str, help="Path to the folder where frames will be saved.")

    args = parser.parse_args()

    extract_frames(args.video_path, args.output_folder)

    # Example usage:
    # python3 videoToFrames.py "./path/to/video.mp4" "./path/to/output_folder"