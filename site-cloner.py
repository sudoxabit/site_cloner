import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse
import logging
import platform

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ANSI escape codes for colors
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def clear_terminal():
    """Clear the terminal screen based on the operating system."""
    os_name = platform.system()
    if os_name == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def create_directory(directory):
    """Create a directory if it does not exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f'Created directory: {directory}')

def save_file(url, content, directory):
    """Save content to a file with a path derived from the URL."""
    parsed_url = urlparse(url)
    path = parsed_url.path.lstrip('/')
    if not path:
        path = 'index.html'  # Default file if path is empty
    filepath = os.path.join(directory, path)

    # Ensure directory structure exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Save file content
    with open(filepath, 'wb') as file:
        file.write(content)
        logging.info(f'Saved file: {filepath}')

def fetch_and_save_resource(url, resource_url, directory):
    """Fetch a resource and save it to the specified directory."""
    try:
        resource_response = requests.get(resource_url)
        if resource_response.status_code == 200:
            save_file(resource_url, resource_response.content, directory)
        else:
            logging.warning(f'Failed to download: {resource_url}')
    except requests.exceptions.RequestException as e:
        logging.error(f'Error downloading {resource_url}: {e}')

def download_website(url, directory):
    """Download a website's HTML and its resources (CSS, JS, images)."""
    try:
        response = requests.get(url)
        if response.status_code != 200:
            logging.error(f'Failed to retrieve {url}')
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        # Save the HTML page
        save_file(url, response.content, directory)

        # Download all linked resources (CSS, JS, images)
        resources = set()  # Avoid duplicate downloads
        for tag in soup.find_all(['link', 'script', 'img']):
            src = tag.get('href') or tag.get('src')
            if src:
                resource_url = urljoin(url, src)
                if resource_url not in resources:
                    resources.add(resource_url)
                    fetch_and_save_resource(url, resource_url, directory)

    except requests.exceptions.RequestException as e:
        logging.error(f'Error downloading website {url}: {e}')

def print_banner():
    """Print the banner with green styling."""
    banner = """
██╗  ██╗     ██████╗ ██╗   ██╗████████╗███████╗
╚██╗██╔╝     ██╔══██╗╚██╗ ██╔╝╚══██╔══╝██╔════╝
 ╚███╔╝█████╗██████╔╝ ╚████╔╝    ██║   █████╗  
 ██╔██╗╚════╝██╔══██╗  ╚██╔╝     ██║   ██╔══╝  
██╔╝ ██╗     ██████╔╝   ██║      ██║   ███████╗
╚═╝  ╚═╝     ╚═════╝    ╚═╝      ╚═╝   ╚══════╝
    """
    print(f"{GREEN}{banner}{RESET}")

def print_author_info():
    """Print author information in yellow color."""
    author_info = """
Author: x4bi7
GitHub: https://github.com/sudoxabit/
Instagram: @x_byt3
Telegram: https://t.me/scorpionisready
    """
    print(f"{YELLOW}{author_info}{RESET}")

if __name__ == '__main__':
    clear_terminal()  # Clear the terminal before running the script
    print_banner()
    print_author_info()
    
    target_url = input('Enter the URL of the website to clone: ')
    output_directory = 'cloned_website'

    create_directory(output_directory)
    download_website(target_url, output_directory)
    logging.info(f'Website cloned to: {output_directory}')

