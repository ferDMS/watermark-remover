# Watermark Removal Toolkit

This toolkit provides scripts to remove watermarks from videos and images. It includes functionality to process video frames, apply masks, and log responses.

## [`main.py`](./main.py)

This is the main entry point for processing videos to remove watermarks.

To use it simply run the code with the following arguments:

```sh
python3 main.py "path/to/video_name/video_name.mp4" [-m]
```

- video_path: Path to the video file.
    - The folder where the video is contained, `video_name` must be the same as the video's base name (without the extension, e.g.: .mp4, .mov, etc.)

- -m, --mask: Use mask folder if available.
    - If intending to use a mask, it must be located inside the directory `/video_name/masks/`. The two files must be called `mask_base.png` and `mask_brush.png`.


## Dependencies

Python 3.x

Required Python packages (install via pip):

- argparse
- concurrent.futures
- os
- re
- json
- time

## License

This project is licensed under the MIT License.