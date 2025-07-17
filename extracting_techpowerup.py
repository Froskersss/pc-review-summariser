import os
import requests
from bs4 import BeautifulSoup

website_url = 'https://www.techpowerup.com/'

techpowerup_urls = [
		'https://www.techpowerup.com/review/amd-ryzen-9-9950x3d/',
		'https://www.techpowerup.com/review/intel-core-ultra-9-285k/',
		'https://www.techpowerup.com/review/intel-core-i7-14700k/',
		'https://www.techpowerup.com/review/amd-ryzen-7-7700x/',
		'https://www.techpowerup.com/review/intel-core-i5-13600k/',
		'https://www.techpowerup.com/review/amd-ryzen-5-5600x/'
	]

i = 1

output_directory = 'techpowerup pages'
os.makedirs(output_directory,exist_ok=True)

print('Starting HTML page extraction')

for i, url in enumerate(techpowerup_urls):
    print(f"Fetching URL {i}/{len(techpowerup_urls)}: {url}")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }
        
        r = requests.get(url, headers=headers, timeout=10) # Added timeout for robustness
        r.raise_for_status()

        soup = BeautifulSoup(r.text, 'html.parser') 
        s = soup.prettify() # prettify() makes the HTML readable

        file_path = os.path.join(output_directory, f"techpowerup_{i+1}.html")
        
        with open(file_path, 'w', encoding='utf-8') as file: 
            file.write(s)
        
        print(f"Successfully saved HTML to {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred for {url}: {e}")

print("HTML page extraction complete for TechPowerUp.")
