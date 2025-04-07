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

def standardize_terminology(text):
    """Standardize terminology throughout the document."""
    
    # Create a copy of the original text
    standardized_text = text
    changes = []
    
    # 1. Standardize Enneagram type references
    type_replacements = [
        # Standardize main type references (choose ONE convention)
        (r'Enneatype (\d+)', r'Enneagram Type \1'),
        (r'Enneatype ([IVX]+)', r'Enneagram Type \1'),
        (r'\bE(\d+)\b', r'Enneagram Type \1'),
        
        # Standardize Roman numerals to Arabic
        (r'Type I\b', r'Type 1'),
        (r'Type II\b', r'Type 2'),
        (r'Type III\b', r'Type 3'),
        (r'Type IV\b', r'Type 4'),
        (r'Type V\b', r'Type 5'),
        (r'Type VI\b', r'Type 6'),
        (r'Type VII\b', r'Type 7'),
        (r'Type VIII\b', r'Type 8'),
        (r'Type IX\b', r'Type 9'),
        (r'Enneagram Type I\b', r'Enneagram Type 1'),
        (r'Enneagram Type II\b', r'Enneagram Type 2'),
        (r'Enneagram Type III\b', r'Enneagram Type 3'),
        (r'Enneagram Type IV\b', r'Enneagram Type 4'),
        (r'Enneagram Type V\b', r'Enneagram Type 5'),
        (r'Enneagram Type VI\b', r'Enneagram Type 6'),
        (r'Enneagram Type VII\b', r'Enneagram Type 7'),
        (r'Enneagram Type VIII\b', r'Enneagram Type 8'),
        (r'Enneagram Type IX\b', r'Enneagram Type 9'),
    ]
    
    # 2. Standardize subtype references
    subtype_replacements = [
        # Standardize subtype abbreviations
        (r'\bSO (\d+)', r'Social \1'),
        (r'\bSX (\d+)', r'Sexual \1'),
        (r'\bSP (\d+)', r'Self-Preservation \1'),
        
        # Standardize subtype names
        (r'Self Preservation', r'Self-Preservation'),
        (r'E(\d+) Conservation', r'Self-Preservation \1'),
        (r'Conservation (\d+)', r'Self-Preservation \1'),
        
        # Standardize E notation
        (r'E(\d+) Social', r'Social \1'),
        (r'E(\d+) Sexual', r'Sexual \1'),
        (r'E(\d+) Self-Preservation', r'Self-Preservation \1'),
    ]
    
    # Apply replacements
    for pattern, replacement in type_replacements + subtype_replacements:
        prev_text = standardized_text
        standardized_text = re.sub(pattern, replacement, standardized_text, flags=re.IGNORECASE)
        if prev_text != standardized_text:
            changes.append(f'Applied: {pattern} -> {replacement}')
    
    # 3. Standardize heading formats based on detected patterns
    
    # This would be customized based on the analysis results
    # For example, ensuring all main type headings are "# Enneagram Type X: [Passion]"
    # and all subtype headings are "## [Subtype] [Number]: [Description]"
    
    return standardized_text, changes

def main():
    # Paths
    input_file = '/Users/nickbarr/Desktop/ai/selftherapy/public/27 Personalities in Search of Being.md'
    output_dir = '/Users/nickbarr/Desktop/ai/selftherapy/consistency'
    output_file = os.path.join(output_dir, '27 Personalities - Standardized.md')
    changes_file = os.path.join(output_dir, 'standardization-changes.txt')
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Read input file
    if not os.path.exists(input_file):
        print(f"Input file not found: {input_file}")
        return
    
    text = read_file(input_file)
    
    # Standardize terminology
    standardized_text, changes = standardize_terminology(text)
    
    # Write standardized text to output file
    write_file(output_file, standardized_text)
    
    # Write changes to changes file
    with open(changes_file, 'w', encoding='utf-8') as f:
        f.write(f"Applied {len(changes)} standardization changes:\n\n")
        for i, change in enumerate(changes, 1):
            f.write(f"{i}. {change}\n")
    
    print(f"Standardization complete.")
    print(f"- Original file: {input_file}")
    print(f"- Standardized file: {output_file}")
    print(f"- Changes log: {changes_file}")
    print(f"- Total changes applied: {len(changes)}")

if __name__ == "__main__":
    main() 