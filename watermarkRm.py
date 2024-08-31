import requests
import json
import time
import base64
import re
import os
import sys
import argparse


# Function to save the edited image from the API response
def bytes_to_image(bytes, frame, output_path):
    # Construct image output path
    image_name = frame.split('.')[0].split('-')[0] + '-t.png'
    image_path = os.path.join(output_path, image_name)
    print(image_path)
    # Save the image to a file
    with open(image_path, 'wb') as f:
        f.write(base64.b64decode(bytes))


# Function to log response details to a file
def log_response(response, log_file):
    with open(log_file, 'a') as f:
        f.write(f"Timestamp: {time.ctime()}\n")
        f.write(f"Status Code: {response.status_code}\n")
        f.write("Headers:\n")
        for key, value in response.headers.items():
            f.write(f"  {key}: {value}\n")
        f.write("Content:\n")
        try:
            json_content = response.json()
            f.write(json.dumps(json_content, indent=2))
        except ValueError:
            f.write(response.text)
        f.write("\n\n" + "-"*80 + "\n\n")  # Separator for readability


# Function to obtain the latest "Content: {}" from the responses log
def get_latest_response_bytes(log_file):

    with open(log_file, 'r') as f:
        content = f.read()
        # Regex pattern to match the bytes
        pattern = re.compile(r'\"image\": \"(.*?)\"', re.DOTALL)
        matches = pattern.findall(content)
        try:
            print("Retrieved image bytes")
            return matches[-1]  # Return last bytes obtained
        except Exception as e:
            print(f"No valid image bytes found")
            return None


# Function to call the API endpoint to remove a watermark from an image
def remove_watermark_auto(input_path, output_path, proxy=None):
    # URL for the API endpoint
    url = "https://api.dewatermark.ai/api/object_removal/v5/erase_watermark?smth=%0a"

    # Headers for the request
    headers = {
        "accept": "application/json",
        "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpZ25vcmUiLCJwbGF0Zm9ybSI6IndlYiIsImlzX3BybyI6ZmFsc2UsImV4cCI6MTcyNDY5MTc3NX0.1RUCtthY0LW1xY4qs9elZjGKsbYkIfLkBXjT_C__zKU",  # Replace with your actual token
        "origin": "https://dewatermark.ai",
        "referer": "https://dewatermark.ai/",
        "sec-ch-ua": "\"Not;A=Brand\";v=\"24\", \"Chromium\";v=\"128\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "x-api-mode": "AUTO",  # This changes if we pass a mask or not
        "x-service": "REMOVE_WATERMARK"
    }

    # Define proxies
    if proxy is not None:
        proxies = {
            'http': proxy,
            'https': proxy
        }
    else:
        proxies = None

    # Log file path
    log_file = 'api_responses.log'  # The file where all responses will be logged

    # Extract frame name from input path
    frame = os.path.basename(input_path)

    # Confirm that file to be sent exists
    if not os.path.exists(input_path):
        print(f"File {frame} does not exist at path provided.")

    # Creating the multipart form data
    files = {
        # Set image as path joined path and frame name using os
        'original_preview_image': ('blob', open(input_path, 'rb'), 'image/jpeg')
    }

    # Sending the POST request
    response = requests.post(url, headers=headers, files=files, proxies=proxies)

    # If succesful, turn the bytes into an image
    if response.status_code == 200:
        bytes = response.json()['edited_image']['image']
        bytes_to_image(bytes, frame, output_path)

    # Log the first response
    # log_response(response, log_file)

    return response


# Function to call the API endpoint to remove a watermark from an image using a manual mask
def remove_watermark_manual(input_path, output_path, mask_path, proxy=None):
    # URL for the API endpoint
    url = "https://api.dewatermark.ai/api/object_removal/v5/erase_watermark?smth=%0a"

    # Headers for the request
    headers = {
        "accept": "application/json",
        "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpZ25vcmUiLCJwbGF0Zm9ybSI6IndlYiIsImlzX3BybyI6ZmFsc2UsImV4cCI6MTcyNDc4MjEzNX0.AFWIfVYlNvpLZYGtVcuNU7RJZZPbZOovKCjGjytD3MQ",  # Replace with your actual token
        "origin": "https://dewatermark.ai",
        "referer": "https://dewatermark.ai/",
        "sec-ch-ua": "\"Not;A=Brand\";v=\"24\", \"Chromium\";v=\"128\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "x-api-mode": "MANUAL",  # This changes if we pass a mask or not
        "x-service": "REMOVE_WATERMARK"
    }

    # Define proxies
    if proxy is not None:
        proxies = {
            'http': proxy,
            'https': proxy
        }
    else:
        proxies = None

    # Log file path
    log_file = 'api_responses.log'  # The file where all responses will be logged

    # Extract frame name from input path
    frame = os.path.basename(input_path)

    # Construct mask_base and mask_brush from path using os
    mask_base = os.path.join(mask_path, 'mask_base.png')
    mask_brush = os.path.join(mask_path, 'mask_brush.png')

    # Confirm that input file exists
    if not os.path.exists(input_path):
        print(f"File {frame} does not exist at path provided.")

    # Confirm that mask_base and mask_brush exists
    if not os.path.exists(mask_path):
        print("Mask file does not exist at path provided.")

    # Creating the multipart form data
    files = {
        'original_preview_image': ('blob', open(input_path, 'rb'), 'image/jpeg'),
        'mask_base': ('blob', open(mask_base, 'rb'), 'image/png'),
        'mask_brush': ('blob', open(mask_brush, 'rb'), 'image/png')
    }

    # Sending the POST request
    response = requests.post(url, headers=headers, files=files, proxies=proxies)

    # If succesful, turn the bytes into an image
    if response.status_code == 200:
        bytes = response.json()['edited_image']['image']
        bytes_to_image(bytes, frame, output_path)

    # Log the first response
    # log_response(response, log_file)

    return response


def remove_watermark_auto_n_manual(input_path, output_path, mask_path, proxy=None):
    
    # Remove watermark auto first
    auto_response = remove_watermark_auto(input_path, output_path, proxy=proxy)

    if auto_response.status_code == 200:

        print("First call successful.")

        new_input_path = os.path.join(output_path, os.path.basename(input_path).split('.')[0].split('-')[0] + '-t.png')

        # Wait for 5 seconds so that server works
        print("Waiting to make second call...")
        time.sleep(7)

        manual_response = remove_watermark_manual(new_input_path, output_path, mask_path, proxy=proxy)

        if manual_response.status_code == 200:
            print("Watermark removed successfully.")
            return True
        else:
            print("Error in removing watermark manually.")

    else:
        print("Error in removing watermark automatically.")

    return False


def remove_watermark(input_path, output_path, mask_path=None, proxy=None):
    # Check that mask path has 2 files of name 'mask_base.png' and 'mask_brush.png'
    if mask_path: 
        isSuccessful = remove_watermark_manual(input_path, output_path, mask_path, proxy=proxy)
    else:
        isSuccessful = remove_watermark_auto(input_path, output_path, proxy=proxy)

    return isSuccessful


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Remove watermark from video.')
    parser.add_argument('input_path', type=str, help='Path to the input video file')
    parser.add_argument('-o', '--output_path', type=str, required=True, help='Path to the output video file')
    parser.add_argument('-m', '--mask_path', type=str, help='Path to the mask file')
    parser.add_argument('-p', '--proxy', type=str, help='Proxy to use for network requests')

    args = parser.parse_args()

    input_path = args.input_path
    output_path = args.output_path
    mask_path = args.mask_path
    proxy = args.proxy

    remove_watermark(input_path, output_path, mask_path, proxy)


"""
python3 watermarkRm.py -o "./smile hug/frames_new" "./smile hug/frames_og/frame_0003.png"
"""

# Get the latest
# bytes = get_latest_response_bytes('api_responses.log')

# if bytes is None:
#     print("No response found in the log file.")
# else:
#     bytes_to_image(bytes, 'latest_image.png', output_path)

