# MetaInjector
 MetaInjector is a tool designed to test security by injecting malicious payloads (such as XSS, SQL Injection, remote code execution, etc.) into image metadata. The tool supports image formats such as JPEG, PNG, and SVG It provides options to encrypt payloads using Base64 or URL markup to bypass some security filters.

## Features
1. Multiple Payload Injections: Supports common payloads such as XSS, SQL Injection, Command Injection, RCE, LFI, and more.
2. Image Formats Support: Supports JPEG, PNG, and SVG images.
3. Metadata Display and Analysis: Displays image metadata before and after injection to make it easy to verify changes.
4. Payload Encoding: Supports encoding payloads using Base64 and URL Encoding.

## Requirements

To run the tool, ensure you have the following:
* Python 3.6 or higher
* The following Python libraries:
     * Pillow - for image processing
     * piexif - for EXIF metadata manipulation
     * xml.etree.ElementTree - for editing SVG files
You can install the required libraries using pip:
```
pip install Pillow piexif
```

## Usage
Steps:
Run the program: Start the tool by running the following command:
```
python metainjector.py
```

* Input image path: After starting the program, you will be prompted to input the path of the image you wish to inject.
* Choose the payload: Select the type of payload you wish to inject. You can choose from the available payloads or input a custom one.
* Select payload encoding: You can choose to encode the payload using Base64 or URL Encoding or proceed with the raw payload.
* Results: After the payload is injected, the modified image will be saved, and the metadata will be displayed for verification.

## Example:
```
Enter the path to the image file (JPEG, PNG, or SVG): /path/to/image.jpg
Choose the type of payload to inject:
1. XSS
2. SQL Injection
3. Remote Code Execution
4. Command Injection
5. Local File Inclusion (LFI)
6. Remote File Inclusion (RFI)
7. Buffer Overflow
Enter the number of the payload type (1-7) or 'custom' for a custom payload: 1
Do you want to encode the payload? (y/n): y
Choose encoding method:
1. Base64 Encoding
2. URL Encoding
Enter the encoding method (1-2): 1
Payload injected and saved to modified_image.jpg
```
