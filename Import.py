import subprocess
import xml.etree.ElementTree as ET
import requests
import os

def install_required_packages():
    try:
        import requests
        import xml.etree.ElementTree as ET
        return True
    except ImportError:
        return False

# Check if required packages are installed
if not install_required_packages():
    print("Installing required packages...")
    try:
        subprocess.run(['python', '-m', 'pip', 'install', 'requests', 'xml.etree.ElementTree'], check=True)
        print("Required packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing required packages: {e}")
        exit(1)

def parse_xml(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return ET.fromstring(response.content)
    except requests.RequestException as e:
        print(f"Error retrieving XML data from {url}: {e}")
        return None

def main():
    print("Starting the Plex Script...\n")
    
    # Get Plex Media Server IP Address from the user
    plex_ip_input = input("Enter the Plex Media Server IP Address (example 192.468.1.5 or 192.468.1.5:32400): ")

    # Extract IP address and port (default to 32400 if no port is provided)
    if ':' in plex_ip_input:
        plex_ip, plex_port = plex_ip_input.split(':')
    else:
        plex_ip = plex_ip_input
        plex_port = 32400

    print(f"\nYou entered Plex Media Server IP Address: {plex_ip} and Port: {plex_port}\n")

    # Get Plex Authentication Token from the user with an example and note
    print("Enter your Plex Authentication Token (example dGwsxVcK4vNWhNxN-fgV  This is a fake token): ")
    auth_token = input()
    print(f"\nYou entered Plex Authentication Token: {auth_token}\n")

    # Build the URL using the provided format
    plex_url = f"http://{plex_ip}:{plex_port}/library/sections/?X-Plex-Token={auth_token}"

    # Ask the user for the desired location to save the HTML file with a complete file path example
    save_location = input("\nWhere do you want your Plex Media Library HTML file saved? (example: C:\\Users\\Username\\Desktop\\): ")

    # Remove quotes if present in the user's input
    save_location = save_location.strip('\"')

    # Extract the drive letter and path from the user's input
    drive_letter, path = os.path.splitdrive(save_location)

    # Build the desktop path based on the extracted drive letter and path
    desktop_path = os.path.join(drive_letter, path)

    # Check if the directory exists; if not, create it
    if not os.path.exists(desktop_path):
        os.makedirs(desktop_path)

    # Ask the user for a custom name for the HTML file
    custom_html_name = input("\nEnter a custom name for the HTML file without extension (example: plex media import): ")

    # Build the full HTML file path with the custom name
    html_file_path = os.path.join(desktop_path, f'{custom_html_name}.html')

    # Ask the user if they require a PDF file
    pdf_required = input("\nDo you require a PDF file? (Y or N): ").strip().lower()

    if pdf_required == 'y':
        print("\nPDF being created. This may take a while. :)\n")
    elif pdf_required == 'n':
        print("\nPDF creation skipped.\n")
    else:
        print("\nInvalid input. Assuming PDF creation is not required.\n")

    # Make a request to the Plex server and parse the XML response
    xml_data = parse_xml(plex_url)

    if xml_data is not None:
        # Extract data from every "Key" element within "Directory" elements
        key_values = [element.get("key") for element in xml_data.findall(".//Directory")]

        # Print the extracted key values
        if key_values:
            # Accumulate HTML content for all videos
            all_videos_html_content = ""

            # Add the "Movies" heading only once above all images
            all_videos_html_content += '<h1 class="movies-heading" style="text-align: center; font-size: x-large; text-decoration: underline;">Movies</h1>'

            for key_value in key_values:
                # Construct new URL for each key value (modify this part based on your needs)
                section_url = f"http://{plex_ip}:{plex_port}/library/sections/{key_value}/all?X-Plex-Token={auth_token}"

                try:
                    # Fetch and print data from the section URL
                    section_response = requests.get(section_url)
                    section_response.raise_for_status()

                    # Parse the XML data for all 'Video' and 'Directory' elements under 'MediaContainer'
                    media_container_element = ET.fromstring(section_response.text)
                    video_elements = media_container_element.findall(".//Video")
                    directory_elements = media_container_element.findall(".//Directory")

                    if video_elements:
                        # Accumulate HTML content for each video under "Movies"
                        videos_html_content = ""

                        for video_element in video_elements:
                            title = video_element.get("title")
                            thumb = video_element.get("thumb")

                            # Create a new URL for the title and thumbnail image
                            new_html_url = f"http://{plex_ip}:{plex_port}{thumb}?X-Plex-Token={auth_token}"

                            # Create HTML content for each video with titles below the image, smaller font, and dark grey background
                            video_html_content = f"""<div class="video-item">
    <!DOCTYPE html>
    <html>
    <head>
        <title>Plex Media Import to HTML</title>
        <style>
            body {{
                background-color: #333;  /* Dark grey background color */
                color: #fff;  /* White text color */
                font-family: Arial, sans-serif;
                margin: 20px;  /* Additional margin on both sides */
            }}
            .video-item {{
                text-align: center;
                margin: 10px;
                padding: 10px;
                border-radius: 5px;
                display: inline-block; /* Display videos in a row */
            }}
            img {{
                width: 175px;  /* Shrink the size of the images to 175px */
                margin: 5px;  /* Additional space between images */
            }}
            .title {{
                font-size: small;
            }}
            .movies-heading {{
                margin-bottom: 10px;  /* Add space between headings and videos */
            }}
        </style>
    </head>
    <body>
        <img src="{new_html_url}" alt="{title} Thumbnail">
        <h1 class="title">{title}</h1>
    </body>
    </html>
    </div>
    """

                            # Accumulate HTML content for all videos under "Movies"
                            videos_html_content += video_html_content

                        # Add CSS styling to create a grid layout for "Movies"
                        all_videos_html_content += f'<div style="text-align: center;">{videos_html_content}</div>'

                except requests.RequestException as e:
                    print(f"Error retrieving data from {section_url}: {e}")

            if directory_elements:
                # Add the "TV Shows" heading only once above all images for TV Shows
                all_videos_html_content += '<h1 class="tv-shows-heading" style="text-align: center; font-size: x-large; text-decoration: underline;">TV Shows</h1>'
                directories_html_content = ""

                for directory_element in directory_elements:
                    title = directory_element.get("title")
                    thumb = directory_element.get("thumb")

                    # Create a new URL for the title and thumbnail image
                    new_html_url = f"http://{plex_ip}:{plex_port}{thumb}?X-Plex-Token={auth_token}"

                    # Create HTML content for each directory with titles below the image, smaller font, and dark grey background
                    directory_html_content = f"""<div class="video-item">
                            <!DOCTYPE html>
                            <html>
                            <head>
                                <title>Plex Media Import to HTML</title>
                                <style>
                                    .directory-item {{
                                        text-align: center;
                                        margin: 10px;
                                        padding: 10px;
                                        border-radius: 5px;
                                        display: inline-block; /* Display directories in a row */
                                    }}
                                    .directory-item img {{
                                        width: 175px;  /* Shrink the size of the images to 175px */
                                        margin: 5px;  /* Additional space between images */
                                    }}
                                    .title {{
                                        font-size: small;
                                    }}
                                    .tv-shows-heading {{
                                        margin-bottom: 10px;  /* Add space between headings and videos */
                                    }}
                                </style>
                            </head>
                            <body>
                                <img src="{new_html_url}" alt="{title} Thumbnail">
                                <h1 class="title">{title}</h1>
                            </body>
                            </html>
                            </div>
                            """

                    # Accumulate HTML content for all directories under "TV Shows"
                    directories_html_content += directory_html_content

                # Add CSS styling to create a grid layout for "TV Shows"
                all_videos_html_content += f'<div style="text-align: center;">{directories_html_content}</div>'

        else:
            print("Failed to retrieve valid XML data from the Plex server.")

        # Save the HTML page to the desktop
        with open(html_file_path, 'w') as html_file:
            html_file.write(all_videos_html_content)

        print(f"\nHTML Page created and saved at: {html_file_path}")

        # Convert HTML to a PDF using wkhtmltopdf if requested
        if pdf_required == 'y':
            print("\nPDF being created. This may take a while. :)\n")
            pdf_file_path = os.path.join(desktop_path, f'{custom_html_name}.pdf')
            wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'  # Update this path

            command = f'"{wkhtmltopdf_path}" --page-height 1000 --page-width 400 "{html_file_path}" "{pdf_file_path}" '

            try:
                subprocess.run(command, check=True, text=True, shell=True)
                print(f"\nPDF created and saved at: {pdf_file_path}")
            except subprocess.CalledProcessError as e:
                print(f"Error converting HTML to PDF: {e}")
        else:
            print(f"\nHTML Page created and saved at: {html_file_path}")

if __name__ == "__main__":
    main()
