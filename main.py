import os
import re
import requests
from PIL import Image, ExifTags
from io import BytesIO


def download_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        img_data = response.content
        return Image.open(BytesIO(img_data))
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error downloading image: {e}")


def open_local_image(file_path):
    try:
        return Image.open(file_path)
    except (FileNotFoundError, IsADirectoryError) as e:
        raise ValueError(f"Error opening image: {e}")


def extract_metadata(exif_data, img):
    metadata = {}

    if hasattr(img, 'size'):
        width, height = img.size
        metadata['Image Size'] = f"{width} x {height}"
    else:
        metadata['Image Size'] = 'unknown'

    if 'FNumber' in exif_data:
        f_stop = exif_data['FNumber']
        if isinstance(f_stop, tuple):
            f_stop = f_stop[0] / f_stop[1]
        metadata['F-stop'] = f_stop
    else:
        metadata['F-stop'] = 'unknown'

    if 'FocalLength' in exif_data:
        focal_length = exif_data['FocalLength']
        if isinstance(focal_length, tuple):
            focal_length = focal_length[0] / focal_length[1]
        metadata['Focal Length'] = focal_length
    else:
        metadata['Focal Length'] = 'unknown'

    if 'ExposureTime' in exif_data:
        exposure_time = exif_data['ExposureTime']
        if isinstance(exposure_time, tuple):
            exposure_time = f"{exposure_time[1]}/{exposure_time[0]}"
        else:
            exposure_time = f"1/{str(round(1/exposure_time))}"
        metadata['Shutter Speed'] = exposure_time
    else:
        metadata['Shutter Speed'] = 'unknown'

    return metadata


def get_metadata(img):
    exif_data = {}
    exif = img._getexif()
    if exif:
        for tag, value in exif.items():
            if tag in ExifTags.TAGS:
                exif_data[ExifTags.TAGS[tag]] = value

    return extract_metadata(exif_data, img)


def print_metadata(metadata):
    for key, value in metadata.items():
        print(f"{key}: {value}")


def parse_args():
    import argparse

    parser = argparse.ArgumentParser(description='Extract metadata from an image file.')
    parser.add_argument('file_path', help='Path to the image file (local file path or URL)')
    return parser.parse_args()


def main():
    args = parse_args()
    file_path = args.file_path

    if re.match(r"^(http|https)://[a-zA-Z0-9\-.]+\.[a-zA-Z]{2,}(/\S*)?$", file_path):
        try:
            image = download_image(file_path)
            metadata = get_metadata(image)
            print_metadata(metadata)
        except ValueError as e:
            print(f"Error: {e}")
    else:
        if os.path.exists(file_path):
            try:
                image = open_local_image(file_path)
                metadata = get_metadata(image)
                print_metadata(metadata)
            except ValueError as e:
                print(f"Error: {e}")
        else:
            print("File not found. Please check the file path and try again.")


if __name__ == '__main__':
    main()
