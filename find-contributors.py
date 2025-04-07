#!/usr/bin/env python3

import re
import sys

def find_contributors(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match various forms of contributor mentions
    patterns = [
        # Match "Transformation of the X" patterns with variations
        r'(?:The )?[Tt]ransformation (?:of|in|on) the (?:Social|Sexual|Self-Preservation|Conservation) (?:One|Two|Three|Four|Five|Six|Seven|Eight|Nine|[1-9])(?: -|:| by|\n) ([A-Za-z ]+)',
        
        # Match section headers with author attribution
        r'<h[12][^>]*>(?:The )?(?:Social|Sexual|Self-Preservation|Conservation) (?:One|Two|Three|Four|Five|Six|Seven|Eight|Nine|[1-9]).*?(?:by|-).*?([A-Za-z ]+)</h[12]>',
        
        # Match "By X" patterns in various formats
        r'<strong>By ([A-Za-z ]+)</strong>',
        r'(?<!>)By ([A-Za-z ]+)</p>',
        
        # Match specific section patterns
        r'The (?:Social|Sexual|Self-Preservation|Conservation) (?:One|Two|Three|Four|Five|Six|Seven|Eight|Nine|[1-9])[^<]*?by ([A-Za-z ]+)',
        r'(?:Social|Sexual|Self-Preservation|Conservation) (?:One|Two|Three|Four|Five|Six|Seven|Eight|Nine|[1-9])[^<]*?- ([A-Za-z ]+)',
        
        # Match author bylines
        r'<p class="author">([A-Za-z ]+)</p>',
        r'<div class="author">([A-Za-z ]+)</div>'
    ]
    
    # Words that indicate a section title rather than a name
    non_names = {
        'A', 'The', 'In', 'On', 'Through', 'What', 'How', 'Our', 'My',
        'True', 'New', 'Other', 'Setting', 'Breaking', 'Emerging',
        'Reclaiming', 'Reconnecting', 'Seeing', 'Daring', 'Contact',
        'Sexuality', 'Thought', 'Parents', 'Testimonies', 'Recommendations',
        'Meditation', 'Personality', 'Hatred', 'Tenacity'
    }
    
    contributors = set()
    for pattern in patterns:
        for match in re.finditer(pattern, content, re.MULTILINE | re.DOTALL):
            contributor = match.group(1).strip()
            # Clean up the contributor name
            contributor = re.sub(r'\s+', ' ', contributor)  # normalize whitespace
            contributor = contributor.strip('.,:-')  # remove punctuation
            
            # Only add if it meets our criteria
            if (contributor and 
                contributor != "Claudio Naranjo" and 
                not any(contributor.startswith(word) for word in non_names) and
                len(contributor.split()) <= 3 and  # Most names are 1-3 words
                not contributor.isupper()):  # Skip all-caps text
                contributors.add(contributor)
    
    return sorted(contributors)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python find-contributors.py <path-to-index.html>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    contributors = find_contributors(file_path)
    
    print(f"Found {len(contributors)} contributors:")
    for contributor in contributors:
        print(f"- {contributor}")
    
    if len(contributors) < 27:
        print(f"\nWarning: Found only {len(contributors)} contributors out of expected 27.") 