import videoToFrames as v2f
import framesToVideo as f2v
import watermarkRmVideo as rmwv

import argparse
import os

def main(video_path, use_mask):

    # Get base name of the video
    video_name = os.path.basename(video_path)

    # Get FPS from video
    fps = v2f.get_video_fps(video_path)

    # Set frames output folder as folder "./frames_og"
    frames_folder = os.path.join(os.path.dirname(video_path), "frames_og")
    # Get frames from video if not present already
    if not os.path.exists(frames_folder):
        v2f.extract_frames(video_path, frames_folder)

    # Set frames output folder as folder "./frames_new"
    output_folder = os.path.join(os.path.dirname(video_path), "frames_new")

    # Set mask input folder as folder "./masks"
    mask_folder = os.path.join(os.path.dirname(video_path), "masks")
    # Check if there's a mask folder and if the flag is set
    if not os.path.exists(mask_folder) or not use_mask:
        mask_folder = None

    # Use frames to remove watermark
    rmwv.remove_watermark_video(frames_folder, output_folder, mask_folder)

    # Run once more to check that no frame was skipped by mistake
    rmwv.remove_watermark_video(frames_folder, output_folder, mask_folder)
    
    # Set output video path as "./{}-output.mp4"
    output_video_name = f"{video_name.split('.')[0]}-output.mp4"
    output_video_path = os.path.join(os.path.dirname(video_path), output_video_name)

    # Get video from frames
    f2v.create_video_from_frames(output_folder, output_video_path, fps)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a video to remove watermark.")
    parser.add_argument("video_path", type=str, help="Path to the video file.")
    parser.add_argument("-m", "--mask", action="store_true", help="Use mask folder if available.")

    args = parser.parse_args()

    main(args.video_path, args.mask)

# Example usage:
# python3 main.py "/path/to/video.mp4" -m