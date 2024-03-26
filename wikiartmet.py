import requests
from bs4 import BeautifulSoup
import time

url = "https://en.wikipedia.org/wiki/Category:Paintings_in_the_Metropolitan_Museum_of_Art"

response = requests.get(url)
page_content = response.text
soup = BeautifulSoup(page_content, 'html.parser')

# Find all 'a' tags with href attributes
links = soup.find_all('a', href=True)

article_links = [a['href'] for a in links if '/wiki/' in a['href'] and not a['href'].startswith(("/wiki/Talk:", "/wiki/Category:", "/wiki/Portal:", "/wiki/Special:", "/wiki/Help:", "/wiki/File:"))]
print(article_links)
base_url = "https://en.wikipedia.org"
normalized_links = []

# Normalize URLs
for link in article_links:
    if link.startswith("/wiki/"):
        normalized_links.append(base_url + link)
    elif link.startswith("//"):
        normalized_links.append("https:" + link)
    # Skip external or unrelated links
    elif link.startswith("https://www.wikidata.org"):
        normalized_links.append(link)
unique_links = set(normalized_links)


import csv

# Prepare for CSV writing
with open('extracted_content_met.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["URL", "Title", "Content"])  # Example CSV structure

    for full_url in unique_links:
        try:
            response = requests.get(full_url)
            if response.status_code == 200:
                # Parse the HTML content of the page
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract the title of the page
                title = soup.find('h1').text if soup.find('h1') else 'No Title Found'
                print(title)
                
                content_paragraphs = soup.find(id='bodyContent').find_all('p')
                content = ' '.join([para.text for para in content_paragraphs])
                print(content)
                
                writer.writerow([full_url, title, content[:8000]])  # Saving a snippet for brevity
                
                # Respectful delay between requests
                time.sleep(1)
            else:
                print(f"Failed to fetch {full_url}: Status code {response.status_code}")
        except requests.RequestException as e:
            print(f"Request failed for {full_url}: {str(e)}")