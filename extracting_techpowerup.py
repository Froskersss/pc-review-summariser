import csv
import requests
from bs4 import BeautifulSoup as bs
import random
from time import sleep





rand_time = random.randrange(500)
website_url = 'https://www.techpowerup.com/'

header = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'}


def makesoup(url,headers=header,timeout=rand_time):
    try:
        r = requests.get(str(url),headers=headers,timeout=timeout)
        r.raise_for_status()
        bad_soup = bs(r.text,'html.parser')
        return bad_soup

    except Exception as e:
        print(f'Error fetching {url}\n returned the following error\n{e}')
        return None

techpowerup_urls = {
    'Ryzen 9 9950X3D':'https://www.techpowerup.com/review/amd-ryzen-9-9950x3d/',
    'INTEL 9 285K':'https://www.techpowerup.com/review/intel-core-ultra-9-285k/',
    'INTEL i7 14700k':'https://www.techpowerup.com/review/intel-core-i7-14700k/',
    'Ryzen 7 7700x': 'https://www.techpowerup.com/review/amd-ryzen-7-7700x/',
    'INTEL i5 13600k':'https://www.techpowerup.com/review/intel-core-i5-13600k/',
    'Ryzen 5 5600x':'https://www.techpowerup.com/review/amd-ryzen-5-5600x/'
    }

output_file = 'techpowerup reviews.csv'

with open(output_file,'w',newline = '',encoding = 'utf-8') as csvfile:
    fieldnames=['CPU','CPU review']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()


    print('Start HTML scraping and CSV writing')
    
    for cpu, urls in techpowerup_urls.items():
        print(f'Processing CPU: {cpu}\n')
        curr_url = urls.strip()
        soup =makesoup(url = curr_url) 
        
        if not soup:
            writer.writerow({'CPU': cpu, 'CPU review': 'Error: Failed to fetch initial page.'})
            continue


        all_review_texts=[]
        while True:
            info_element = soup.find('div',class_='text p')
            if info_element:
                all_review_texts.append(info_element.get_text(separator=' ',strip=True))
        
            next_page_link = soup.find('a',class_='button inverted nextpage-bottom')
            if next_page_link and next_page_link.get('href'):
                next_page_href = next_page_link.get('href')
                next_page_url = website_url + next_page_href
                
                # Check if the next page URL is still within the review section
                if '/review/' in next_page_url:
                    print(f'Scanning the next page: {next_page_url}')
                    
                    # Introduce a random delay to avoid being blocked
                    sleep(random.uniform(1, 3)) 
                    
                    soup = makesoup(url=next_page_url)
                    if not soup:
                        print(f"DEBUG: makesoup returned None for {next_page_url}. Breaking.")
                        break
                    current_page_url_for_debug = next_page_url # Update for next iteration's debug print
                else:
                    # If the next link is not a review page, break the loop
                    print(f'Next link is not a review page: {next_page_url}. Ending review for {cpu}.')
                    break 
 
            print(f'\n\nEnded the review for {cpu}\n\n.')
        print(f'Scraping is finished')
        
        
        #adding to csv
        if all_review_texts:
            combined_review_text = ' '.join(all_review_texts)
            try:
                writer.writerow({'CPU': cpu, 'CPU review': combined_review_text})
                print(f"Successfully scraped and added review for {cpu}")
            except Exception as e:
                print(f'An exception occurred while processing {cpu}: {e}')
                writer.writerow({'CPU': cpu, 'CPU review': f'Error: Failed to process content ({e})'})
        else:
            print(f'Content ("div", class_="text p") not found for {cpu}.')
            writer.writerow({'CPU': cpu, 'CPU review': 'Error: Main content not found'})



print(f"HTML scraping and CSV writing complete. Data saved to {output_file}.")

