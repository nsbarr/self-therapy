import re
import os
from pathlib import Path

def read_file(file_path):
    """Read the content of a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content):
    """Write content to a file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def standardize_headings(text):
    """Standardize heading formats throughout the document."""
    
    # Create a copy of the original text
    standardized_text = text
    changes = []
    
    # Find all type headings with their associated HTML IDs
    type_headings = re.findall(r'^#\s+(.*?)\s+\{#.*?\}$', standardized_text, re.MULTILINE)
    
    # Find all subtype headings with their associated HTML IDs
    subtype_headings = re.findall(r'^##\s+\*\*(.*?)\*\*\s+\{#.*?\}$', standardized_text, re.MULTILINE)
    
    # 1. Standardize main type headings
    # Example: Change varied formats to "# Enneagram Type X: [Passion]"
    main_type_patterns = [
        # Various heading formats for main types
        (r'^#\s+Type (\d+): (.*?)(\s+\{#.*?\})?$', r'# Enneagram Type \1: \2\3'),
        (r'^#\s+Enneatype (\d+): (.*?)(\s+\{#.*?\})?$', r'# Enneagram Type \1: \2\3'),
        (r'^#\s+Enneatype ([IVX]+): (.*?)(\s+\{#.*?\})?$', r'# Enneagram Type \1: \2\3'),
        (r'^#\s+Type ([IVX]+): (.*?)(\s+\{#.*?\})?$', r'# Enneagram Type \1: \2\3'),
    ]
    
    # 2. Standardize subtype headings
    # Example: Change varied formats to "## [Subtype] [Number]: [Description]"
    subtype_patterns = [
        # Various heading formats for subtypes
        (r'^##\s+\*\*The (Social) (One): (.*?)\*\*(\s+\{#.*?\})?$', r'## \1 1: \3\4'),
        (r'^##\s+\*\*(Social) (Two): (.*?)\*\*(\s+\{#.*?\})?$', r'## \1 2: \3\4'),
        (r'^##\s+\*\*(Sexual) (One): (.*?)\*\*(\s+\{#.*?\})?$', r'## \1 1: \3\4'),
        (r'^##\s+\*\*(Self-Preservation) (One): (.*?)\*\*(\s+\{#.*?\})?$', r'## \1 1: \3\4'),
        (r'^##\s+\*\*(E\d+) (Social): (.*?)\*\*(\s+\{#.*?\})?$', r'## Social \1: \3\4'),
        (r'^##\s+\*\*(E\d+) (Sexual): (.*?)\*\*(\s+\{#.*?\})?$', r'## Sexual \1: \3\4'),
        (r'^##\s+\*\*(E\d+) (Conservation): (.*?)\*\*(\s+\{#.*?\})?$', r'## Self-Preservation \1: \3\4'),
        (r'^##\s+(Social) (\d+): (.*?)(\s+\{#.*?\})?$', r'## \1 \2: \3\4'),
        (r'^##\s+(Sexual) (\d+): (.*?)(\s+\{#.*?\})?$', r'## \1 \2: \3\4'),
        (r'^##\s+(Self-Preservation) (\d+): (.*?)(\s+\{#.*?\})?$', r'## \1 \2: \3\4'),
        (r'^##\s+(SO) (\d+) \- (.*?)(\s+\{#.*?\})?$', r'## Social \2: \3\4'),
        (r'^##\s+(Sexual) (\d+) \- (.*?)(\s+\{#.*?\})?$', r'## \1 \2: \3\4'),
        (r'^##\s+(E\d+) (Self-Preservation): (.*?)(\s+\{#.*?\})?$', r'## Self-Preservation \1: \3\4'),
    ]
    
    # Apply replacements
    for pattern, replacement in main_type_patterns + subtype_patterns:
        prev_text = standardized_text
        standardized_text = re.sub(pattern, replacement, standardized_text, flags=re.MULTILINE)
        if prev_text != standardized_text:
            changes.append(f'Applied heading pattern: {pattern} -> {replacement}')
    
    return standardized_text, changes

def main():
    # Paths
    input_file = '/Users/nickbarr/Desktop/ai/selftherapy/consistency/27 Personalities - Standardized.md'
    # If the standardized file doesn't exist yet, use the original
    if not os.path.exists(input_file):
        input_file = '/Users/nickbarr/Desktop/ai/selftherapy/public/27 Personalities in Search of Being.md'
        
    output_dir = '/Users/nickbarr/Desktop/ai/selftherapy/consistency'
    output_file = os.path.join(output_dir, '27 Personalities - Headings Standardized.md')
    changes_file = os.path.join(output_dir, 'heading-standardization-changes.txt')
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Read input file
    if not os.path.exists(input_file):
        print(f"Input file not found: {input_file}")
        return
    
    text = read_file(input_file)
    
    # Standardize headings
    standardized_text, changes = standardize_headings(text)
    
    # Write standardized text to output file
    write_file(output_file, standardized_text)
    
    # Write changes to changes file
    with open(changes_file, 'w', encoding='utf-8') as f:
        f.write(f"Applied {len(changes)} heading standardization changes:\n\n")
        for i, change in enumerate(changes, 1):
            f.write(f"{i}. {change}\n")
    
    print(f"Heading standardization complete.")
    print(f"- Input file: {input_file}")
    print(f"- Standardized file: {output_file}")
    print(f"- Changes log: {changes_file}")
    print(f"- Total changes applied: {len(changes)}")

if __name__ == "__main__":
    main() 