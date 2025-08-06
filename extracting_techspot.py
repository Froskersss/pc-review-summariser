
import csv
import requests
from bs4 import BeautifulSoup

def makesoup(url,headers,timeout = 15):
    try:
        r = requests.get(url,headers=headers,timeout=timeout)
        r.raise_for_status()
        soup = BeautifulSoup(r.text,'html.parser')
        return soup
    except Exception as e:
        print(f'Error fetching {url}\n returned the following error\n{e}')
        return None



cpu_list = ['ryzen 9 9950x3d','core ultra 9 285k','i7 14700k','ryzen 7 7700x','i5 13600k','ryzen 5 5600x']
techspot_urls = [
        'https://www.techspot.com/review/2965-amd-ryzen-9-9950x3d/',
        'https://www.techspot.com/review/2911-intel-core-ultra-9-285k/',
        'https://www.techspot.com/products/processors/intel-core-i7-14700k.285188/',
        'https://www.techspot.com/review/2537-amd-ryzen-7700x/',
        'https://www.techspot.com/products/processors/intel-core-i5-13600k-39ghz-socket-1700.260540/',
        'https://www.techspot.com/review/2135-amd-ryzen-5600x/'
        ]
header = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'}

output_file = 'techspot_reviews.csv'
with open (output_file,'w',newline = '',encoding = 'utf-8') as csvfile:
    fieldnames = ['CPU','CPU review']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader() 

    print("Starting HTML scraping and CSV writing.")

    for cpu, url in zip(cpu_list, techspot_urls):
        print(f"Processing CPU: {cpu}, URL: {url}")

        soup = makesoup(url, header)

        if soup is None: # Handle cases where makesoup failed to get content
            print(f"Skipping {cpu} due to an error fetching the page.")
            writer.writerow({'CPU': cpu, 'CPU review': 'Error: Could not fetch page'}) # Log the error in CSV
            continue

        # Try to find content in 'feature' ID first, then 'articleBody' as fallback

        info_element = soup.find('div', {'id': 'feature'})
        if not info_element:
            info_element = soup.find('div', {'class': 'articleBody'})

        if info_element:
            try:
                review_content = info_element.get_text(separator=' ', strip=True) # For plain text

                writer.writerow({'CPU': cpu, 'CPU review': review_content})
                print(f"Successfully scraped and added review for {cpu}")

            except Exception as e:
                print(f'An exception occurred while processing {cpu}: {e}')
                writer.writerow({'CPU': cpu, 'CPU review': f'Error: Failed to process content ({e})'})
        else:
            print(f'Content div (id="feature" or class="articleBody") not found for {cpu}.')
            writer.writerow({'CPU': cpu, 'CPU review': 'Error: Main content not found'})

print(f"HTML scraping and CSV writing complete. Data saved to {output_file}.")
