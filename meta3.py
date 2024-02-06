import subprocess
import json
import argparse
import os
import sys

def extract_binary_data(metadata, key, output_path):
    """
    Extracts binary data for a given key from the metadata and saves it to a specified output path.
    This function assumes that the binary data is provided by ExifTool directly in a readable format.
    For actual binary extraction, additional logic might be needed based on the metadata structure.
    """
    # This is a placeholder for extracting binary data.
    # Actual implementation will depend on the structure of the binary data in the metadata.
    print(f"Extracting binary data for {key} to {output_path}")
    # In a real scenario, you would extract and save the binary data here.

def read_c2pa_metadata(image_path, extract_binary=False):
    exiftool_path = 'exiftool'  # Adjust this if needed
    cmd = [exiftool_path, '-json', image_path]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = process.communicate()

    try:
        metadata = json.loads(out)[0]
    except json.JSONDecodeError as e:
        print("Error decoding JSON from ExifTool output:", e)
        sys.exit(1)

    if extract_binary:
        # Assuming there could be specific keys for binary data in C2PA metadata. This part needs adjustment.
        for key in metadata:
            if 'BinaryData' in key:  # This condition is hypothetical and should be adjusted.
                output_path = image_path + f"_{key}.bin"
                extract_binary_data(metadata, key, output_path)

    return metadata

def remove_metadata(image_path):
    exiftool_path = 'exiftool'  # Adjust this if needed
    file_root, file_ext = os.path.splitext(image_path)
    output_path = f"{file_root}_no_meta{file_ext}"

    cmd = [exiftool_path, '-all=', '-o', output_path, image_path]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = process.communicate()

    if process.returncode == 0:
        print(f"Metadata removed. New file saved as: {output_path}")
    else:
        print("Error removing metadata:", err)

def main():
    parser = argparse.ArgumentParser(description='Read and manipulate C2PA metadata from an image.')
    parser.add_argument('image_path', type=str, help='Path to the image file')
    parser.add_argument('--extract-binary', action='store_true', help='Extract binary data if available')
    parser.add_argument('--remove', action='store_true', help='Remove all metadata from the image and save as a new file')
    args = parser.parse_args()

    if args.remove:
        remove_metadata(args.image_path)
    else:
        c2pa_metadata = read_c2pa_metadata(args.image_path, args.extract_binary)
        print("C2PA Metadata:", json.dumps(c2pa_metadata, indent=4))

if __name__ == "__main__":
    main()

