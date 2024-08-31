import cv2
import os
import re
import argparse

def create_video_from_frames(frames_folder, output_video_path, fps=25):
    # Get list of all frame files
    frame_files = [f for f in os.listdir(frames_folder) if re.match(r'frame_\d+.*\.png', f)]
    
    # Sort frame files by frame number
    frame_files.sort(key=lambda f: int(re.search(r'frame_(\d+)', f).group(1)))

    # Print number of frames found
    print(f"Found {len(frame_files)} frames")

    # Read the first frame to get the frame size
    first_frame = cv2.imread(os.path.join(frames_folder, frame_files[0]))
    height, width, layers = first_frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can use other codecs like 'XVID'
    video = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    # Write each frame to the video
    for frame_file in frame_files:
        frame_path = os.path.join(frames_folder, frame_file)
        frame = cv2.imread(frame_path)
        video.write(frame)

    # Release the video writer
    video.release()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a video from frames.")
    parser.add_argument("frames_folder", type=str, help="Path to the folder containing the frames.")
    parser.add_argument("output_video_path", type=str, help="Path to the output video file.")
    parser.add_argument("--fps", type=int, default=25, help="Frames per second for the output video. Default is 25.")

    args = parser.parse_args()

    create_video_from_frames(args.frames_folder, args.output_video_path, args.fps)

    # Example usage:
    # python3 videoFromFrames.py "./smile hug/frames_new" "./smile hug/output_video.mp4" --fps 30

# Example usage:
# create_video_from_frames("./piggy/frames_new", "./piggy/output_video.mp4")