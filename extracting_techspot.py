import os
import requests
from bs4 import BeautifulSoup

website_url = 'https://www.techspot.com/'

techspot_urls = [
	'https://www.techspot.com/review/2965-amd-ryzen-9-9950x3d/',
	'https://www.techspot.com/review/2911-intel-core-ultra-9-285k/',
	'https://www.techspot.com/products/processors/intel-core-i7-14700k.285188/',
	'https://www.techspot.com/products/processors/intel-core-i5-13600k-39ghz-socket-1700.260540/',
	'https://www.techspot.com/review/2135-amd-ryzen-5600x/'
]

i = 1

output_directory = 'techspot pages'
os.makedirs(output_directory,exist_ok=True)

print('Starting HTML page extraction')

for i, url in enumerate(techspot_urls):
    print(f"Fetching URL {i}/{len(techspot_urls)}: {url}")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }

        r = requests.get(url, headers=headers, timeout=10) # Added timeout for robustness
        r.raise_for_status()

        soup = BeautifulSoup(r.text, 'html.parser')
        s = soup.prettify() # prettify() makes the HTML readable

        file_path = os.path.join(output_directory, f"techspot_{i+1}.html")

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(s)

        print(f"Successfully saved HTML to {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred for {url}: {e}")

print("HTML page extraction complete for Techspot.")
