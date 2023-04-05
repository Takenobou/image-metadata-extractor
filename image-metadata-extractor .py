import os
import re
import requests
from PIL import Image, ExifTags
from io import BytesIO


def get_image(file_path):
    """
    Retrieves an image from a local file path or a remote URL.
    :param str file_path: The file path or URL of the image to retrieve.
    :return: A PIL Image object representing the retrieved image.
    :raises ValueError: If an error occurs while retrieving the image.
    """
    if re.match(r"^(http|https)://[a-zA-Z0-9\-.]+\.[a-zA-Z]{2,}(/\S*)?$", file_path):
        print("Retrieving image from URL...")
        return download_image(file_path)
    else:
        if os.path.exists(file_path):
            return open_local_image(file_path)
        else:
            raise ValueError("File not found. Please check the file path and try again.")


def download_image(url):
    """
    Downloads an image from a given URL and returns it as a PIL Image object.
    :param str url: The URL of the image to download.
    :return: A PIL Image object representing the downloaded image.
    :raises ValueError: If an error occurs while downloading the image.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        img_data = response.content
        return Image.open(BytesIO(img_data))
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error downloading image: {e}")


def open_local_image(file_path):
    """
    Opens an image file from the local file system and returns it as a PIL Image object.
    :param str file_path: The file path of the image to open.
    :return: A PIL Image object representing the opened image.
    :raises ValueError: If the file cannot be found or is not an image file.
    """
    try:
        return Image.open(file_path)
    except (FileNotFoundError, IsADirectoryError) as e:
        raise ValueError(f"Error opening image: {e}")


def extract_metadata(exif_data, img):
    """
    Extracts metadata from a PIL Image object using its EXIF data.
    :param dict exif_data: A dictionary containing the EXIF data of the image.
    :param Image img: A PIL Image object.
    :return dict: A dictionary containing the extracted metadata.
    """
    metadata = {}

    # Extract camera make and model
    if 'Make' in exif_data:
        metadata['Camera Make'] = exif_data['Make']
    else:
        metadata['Camera Make'] = 'unknown'

    if 'Model' in exif_data:
        metadata['Camera Model'] = exif_data['Model']
    else:
        metadata['Camera Model'] = 'unknown'

    # Extract image size
    if hasattr(img, 'size'):
        width, height = img.size
        metadata['Image Size'] = f"{width} x {height}"
    else:
        metadata['Image Size'] = 'unknown'

    # Extract f-stop
    if 'FNumber' in exif_data:
        f_stop = exif_data['FNumber']
        if isinstance(f_stop, tuple):
            f_stop = f_stop[0] / f_stop[1]
        metadata['F-stop'] = str(f_stop)
    else:
        metadata['F-stop'] = 'unknown'

    # Extract focal length
    if 'FocalLength' in exif_data:
        focal_length = exif_data['FocalLength']
        if isinstance(focal_length, tuple):
            focal_length = focal_length[0] / focal_length[1]
        metadata['Focal Length'] = str(focal_length)
    else:
        metadata['Focal Length'] = 'unknown'

    # Extract shutter speed
    if 'ExposureTime' in exif_data:
        exposure_time = exif_data['ExposureTime']
        if isinstance(exposure_time, tuple):
            exposure_time = f"{exposure_time[1]}/{exposure_time[0]}"
        else:
            exposure_time = f"1/{str(round(1 / exposure_time))}"
        metadata['Shutter Speed'] = exposure_time
    else:
        metadata['Shutter Speed'] = 'unknown'

    # Extract ISO
    if 'ISOSpeedRatings' in exif_data:
        metadata['ISO'] = str(exif_data['ISOSpeedRatings'])
    else:
        metadata['ISO'] = 'unknown'

    return metadata


def get_metadata(img):
    """
    Retrieves metadata from a PIL Image object.
    :param Image img: A PIL Image object.
    :return dict: A dictionary containing the extracted metadata.
    """
    exif_data = {}
    exif = img._getexif()
    if exif:
        for tag, value in exif.items():
            if tag in ExifTags.TAGS:
                exif_data[ExifTags.TAGS[tag]] = value

    return extract_metadata(exif_data, img)


def print_metadata(metadata):
    """
        Prints metadata to the console.
        :param dict metadata: A dictionary containing the metadata to be printed.
    """
    for key, value in metadata.items():
        print(f"{key}: {value}")


def export_metadata(metadata):
    """
    Exports the metadata as a JSON file.
    :param dict metadata: A dictionary containing the metadata to be exported.
    """
    import json

    with open('metadata.json', 'w') as outfile:
        json.dump(metadata, outfile, indent=4)
    print("Metadata exported as JSON to metadata.json")


def parse_args():
    """
    Parses command-line arguments passed to the script using the argparse module.
    :return: An argparse Namespace object containing the parsed arguments.
    """
    import argparse

    parser = argparse.ArgumentParser(description='Extract metadata from an image file.')
    parser.add_argument('file_path', help='Path to the image file (local file path or URL)')
    parser.add_argument('-j', '--json', action='store_true', help='Export metadata as JSON')
    return parser.parse_args()


def main():
    """
    The main entry point of the program. Retrieves the file path or URL of the image to extract metadata from,
    calls `get_image` to retrieve the image, extracts the metadata from the image using `get_metadata`,
    and prints the metadata to the console using `print_metadata`.
    """
    args = parse_args()
    file_path = args.file_path

    try:
        image = get_image(file_path)
        metadata = get_metadata(image)
        if args.json:
            export_metadata(metadata)
        else:
            print_metadata(metadata)
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
