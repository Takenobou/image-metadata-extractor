# Image Metadata Extractor

This is a Python script that extracts metadata from an image file using its EXIF data. The script can handle both local image files and remote image files downloaded from a URL.

## Requirements

To run this script, you need to have the following dependencies installed:

- Python 3.x
- requests
- Pillow

## Usage

To use this script, run the following command from the command line:

`python image-metadata-extractor.py file_path_or_url`

Replace `file_path_or_url` with the file path or URL of the image file you want to extract metadata from. The script will automatically determine whether the file path is a local file or a remote URL.

### Example

To extract metadata from a local image file, run the following command:

`python image-metadata-extractor.py my_image.jpg`

To extract metadata from a remote image file, run the following command:

`python image-metadata-extractor.py https://example.com/image.jpg`

## Output

The script outputs the following metadata for the image:

- Image Size
- F-stop
- Focal Length
- Shutter Speed

The metadata is printed to the console in the following format:

```bash
Camera Make: SONY
Camera Model: ILCE-7M2
Image Size: 3000 x 4000
F-stop: 4.0
Focal Length: 70.0
Shutter Speed: 1/640
ISO: 100
```


If an error occurs while downloading or opening the image file, an error message will be printed to the console.
