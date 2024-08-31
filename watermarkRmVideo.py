# My own scripts
import watermarkRm as wrm

# To handle file paths
import os

# For concurrent calls
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import argparse

# Call a frame processing job
def process_frame(frame, frame_folder, output_folder, mask_folder, proxy=None):
    global processed_f
    
    # Skip if already processed
    with processed_f_lock:
        if frame in processed_f:
            print(f"Skipping {frame}")
            return True
        else:
            processed_f.add(frame)

    # Obtain the exact path to the frame
    frame_path = os.path.join(frame_folder, frame)

    # Try to process the frame
    print(f"Processing {frame}...")
    try:
        # Call the watermarkRm.py file with an execution
        isSuccessful = wrm.remove_watermark(frame_path, output_folder, mask_folder, proxy)

        # If successful, complete
        if isSuccessful:
            print(f"Completed {frame}")
            return True
        else:
            raise Exception("Successful call, but unexpected result")

    except Exception as e:
        print(f"Failed to process {frame}: {e}")
        return False


def get_processed_frames(output_folder):
    # If output directory doesn't exist, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get a list of already processed frames in the output directory
    processed = set()
    for f in os.listdir(output_folder):
        if f.startswith("frame_") and f.endswith("-t.png"):
            original_frame = f.split("-")[0] + ".png"
            processed.add(original_frame)

    return processed


def remove_watermark_video(frame_folder, output_folder, mask_folder=None, proxy=None, max_workers=20):
    global processed_f, processed_f_lock

    # Get a sorted list of all frames in the directory
    all_f = sorted([f for f in os.listdir(frame_folder) if f.startswith("frame_") and f.endswith(".png")])
    processed_f = get_processed_frames(output_folder)

    # Lock so that multiple workers don't process the same frame (race-condition)
    processed_f_lock = threading.Lock()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_frame, frame, frame_folder, output_folder, mask_folder, proxy) for frame in all_f]
        for future in as_completed(futures):
            future.result()  # To raise any exceptions that occurred during processing


def main():
    parser = argparse.ArgumentParser(description="Process video frames to remove watermark.")
    parser.add_argument("frame_folder", type=str, help="Path to the folder containing the frames.")
    parser.add_argument("output_folder", type=str, help="Path to the folder where processed frames will be saved.")
    parser.add_argument("mask_folder", type=str, help="Path to the folder containing the masks.")
    parser.add_argument("--proxy", type=str, default=None, help="Proxy settings if needed.")
    parser.add_argument("--max_workers", type=int, default=20, help="Number of concurrent tasks. Default is 20.")

    args = parser.parse_args()

    remove_watermark_video(args.frame_folder, args.output_folder, args.mask_folder, args.proxy, args.max_workers)


if __name__ == "__main__":
    main()

# Example usage:
# python3 watermarkRmVideo.py "/Users/pez/Downloads/caro videos/smile hug/frames_new" "/Users/pez/Downloads/caro videos/smile hug/frames_new_new" "/Users/pez/Downloads/caro videos/smile hug/masks" --proxy "http://proxy.example.com" --max_workers 20