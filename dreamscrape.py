import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import string

def clean_url(url):
    """Clean the URL by removing trailing commas and ensuring proper format."""
    return url.rstrip(',')

def get_full_entry(url):
    """Fetch the full content of a dream dictionary entry with HTML formatting."""
    try:
        clean_link = clean_url(url)
        r = requests.get(clean_link)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Find the main content div
        content_div = soup.select_one('.main-text .holder')
        if content_div:
            # Get the title
            title = content_div.find('h2')
            
            # Remove social media elements
            for social in content_div.find_all(class_='fb-like'):
                social.decompose()
            
            # Remove navigation
            nav = content_div.find('div', class_='pagging')
            if nav:
                nav.decompose()
            
            # Remove comments section
            comments = content_div.find('div', class_='comment')
            if comments:
                comments.decompose()
                
            # Get the content paragraphs
            paragraphs = content_div.find_all('p')
            content_html = ''.join(str(p) for p in paragraphs)
            content_text = ' '.join(p.get_text(strip=True) for p in paragraphs)
            
            return {
                'html': content_html,
                'text': content_text,
                'title': title.get_text(strip=True) if title else None
            }
        return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def scrape_letter(letter, max_pages=3, delay=1):
    results = []
    for page in range(1, max_pages + 1):
        url = f"https://dreamhawk.com/dream-dictionary/?letter={letter.lower()}&paged={page}"
        print(f"Scraping page {page} at {url}")
        
        try:
            r = requests.get(url)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, 'html.parser')

            # Find the table containing the entries
            table = soup.find('table', class_='alfabet-list')
            if not table:
                print(f"No entries found on page {page} for letter {letter}, moving to next letter...")
                break  # No more pages for this letter

            # Process each entry in the table
            for link in table.find_all('a'):
                term = link.find('span', class_='h3')
                definition_preview = link.find('span', class_='p')
                
                if term and definition_preview and 'href' in link.attrs:
                    term_text = term.get_text(strip=True)
                    entry_url = clean_url(link['href'])
                    
                    print(f"Fetching full entry for: {term_text} at {entry_url}")
                    full_content = get_full_entry(entry_url)
                    
                    if full_content:
                        results.append({
                            'term': term_text,
                            'definition_preview': definition_preview.get_text(strip=True).replace(' More', ''),
                            'full_definition_html': full_content['html'],
                            'full_definition_text': full_content['text'],
                            'url': entry_url,
                            'source_page': page,
                            'letter': letter.upper()
                        })
                    else:
                        print(f"Failed to fetch full content for {term_text}")
                    
                    # Add delay between requests to be polite to the server
                    time.sleep(delay)
                    
            print(f"Found {len(results)} entries so far for letter {letter}...")
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            continue
            
    return results

if __name__ == "__main__":
    print("Starting dream dictionary scraping process...")
    
    all_results = []
    for letter in string.ascii_lowercase:
        print(f"\nProcessing letter: {letter.upper()}")
        letter_results = scrape_letter(letter, max_pages=15, delay=1)
        if letter_results:
            all_results.extend(letter_results)
            print(f"Completed letter {letter.upper()} with {len(letter_results)} entries")
        else:
            print(f"No entries found for letter {letter.upper()}")
    
    print(f"\nTotal entries collected: {len(all_results)}")
    
    # Save to CSV
    df = pd.DataFrame(all_results)
    df.to_csv("dream_dictionary.csv", index=False)
    print("Saved all entries to dream_dictionary.csv")
    
    # Save to HTML
    with open("dream_dictionary.html", "w", encoding='utf-8') as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Dream Dictionary</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px;
            line-height: 1.6;
        }
        .entry { 
            margin-bottom: 30px; 
            padding: 20px; 
            border: 1px solid #ddd; 
            border-radius: 5px;
            background-color: #fff;
        }
        h1 {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 30px;
        }
        h2 { 
            color: #2c3e50;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }
        .letter-section {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 3px solid #2c3e50;
        }
        .letter-heading {
            background-color: #2c3e50;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <h1>Dream Dictionary</h1>""")
        
        # Sort entries by term
        df = df.sort_values('term')
        
        # Group by letter and create sections
        current_letter = None
        for _, entry in df.iterrows():
            letter = entry['term'][0].upper()
            if letter != current_letter:
                if current_letter is not None:
                    f.write("</div>")  # Close previous letter section
                current_letter = letter
                f.write(f'\n<div class="letter-section">')
                f.write(f'<h2 class="letter-heading">Letter {letter}</h2>')
            
            f.write(f"""
            <div class="entry">
                <h2>{entry['term']}</h2>
                {entry['full_definition_html']}
            </div>""")
        
        f.write("</div></body></html>")
    
    print("Saved all entries to dream_dictionary.html")
