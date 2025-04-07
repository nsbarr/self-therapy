import re
import os
import collections
from pathlib import Path

def read_file(file_path):
    """Read the content of a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_enneagram_references(text):
    """Extract different ways enneagram types are referred to in the text."""
    # Pattern matches for different type references
    patterns = [
        r'(Type|Enneatype|Enneagram Type|E)\s*(\d+)',  # Type 1, Enneatype 3, E5, etc.
        r'(Type|Enneatype|Enneagram Type|E)\s*([IVX]+)', # Type I, Enneatype III
        r'(Social|Sexual|Self-Preservation|SO|SP|SX|Self Preservation|E\d+\s*Social|E\d+\s*Sexual|E\d+\s*Conservation|E\d+\s*Self-Preservation)\s*(\d+)', # Social 5, Sexual 6, etc.
    ]
    
    results = []
    
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            results.append(match.group(0))
    
    return results

def analyze_subtype_references(text):
    """Analyze how subtypes are referred to (Social, Sexual, Self-Preservation)."""
    subtype_patterns = [
        r'(Social|SO)',
        r'(Sexual|SX)',
        r'(Self-Preservation|Self Preservation|Conservation|SP)'
    ]
    
    subtype_counts = {
        'Social': collections.Counter(),
        'Sexual': collections.Counter(),
        'Self-Preservation': collections.Counter()
    }
    
    for i, pattern in enumerate(subtype_patterns):
        matches = re.finditer(pattern, text, re.IGNORECASE)
        category = list(subtype_counts.keys())[i]
        
        for match in matches:
            term = match.group(0)
            subtype_counts[category][term] += 1
    
    return subtype_counts

def detect_heading_format_inconsistencies(text):
    """Detect inconsistencies in heading formats."""
    # Find all headings
    heading_patterns = [
        r'^#\s+(.+?)$',  # # Heading
        r'^##\s+(.+?)$', # ## Heading
        r'^###\s+(.+?)$' # ### Heading
    ]
    
    headings = []
    
    for pattern in heading_patterns:
        matches = re.finditer(pattern, text, re.MULTILINE)
        for match in matches:
            headings.append(match.group(0))
    
    # Analyze heading styles
    type_headings = [h for h in headings if re.search(r'Type|Enneatype', h, re.IGNORECASE)]
    subtype_headings = [h for h in headings if re.search(r'Social|Sexual|Self-Preservation', h, re.IGNORECASE)]
    
    return {
        'type_heading_examples': type_headings[:5],
        'subtype_heading_examples': subtype_headings[:5]
    }

def main():
    file_path = '/Users/nickbarr/Desktop/ai/selftherapy/public/27 Personalities in Search of Being.md'
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    text = read_file(file_path)
    
    # 1. Analyze enneagram type references
    enneagram_refs = extract_enneagram_references(text)
    ref_counter = collections.Counter(enneagram_refs)
    
    # 2. Analyze subtype references
    subtype_counts = analyze_subtype_references(text)
    
    # 3. Analyze heading formats
    heading_inconsistencies = detect_heading_format_inconsistencies(text)
    
    # Output results
    print("=== Enneagram Type Reference Analysis ===")
    print("Most common references:")
    for ref, count in ref_counter.most_common(20):
        print(f"  {ref}: {count}")
    
    print("\n=== Subtype Reference Analysis ===")
    for subtype, counts in subtype_counts.items():
        print(f"\n{subtype} references:")
        for term, count in counts.most_common():
            print(f"  {term}: {count}")
    
    print("\n=== Heading Format Analysis ===")
    print("Type heading examples:")
    for heading in heading_inconsistencies['type_heading_examples']:
        print(f"  {heading}")
    
    print("\nSubtype heading examples:")
    for heading in heading_inconsistencies['subtype_heading_examples']:
        print(f"  {heading}")

    # Write results to file
    output_path = Path('/Users/nickbarr/Desktop/ai/selftherapy/consistency/terminology-analysis.txt')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=== Enneagram Type Reference Analysis ===\n")
        f.write("Most common references:\n")
        for ref, count in ref_counter.most_common():
            f.write(f"  {ref}: {count}\n")
        
        f.write("\n=== Subtype Reference Analysis ===\n")
        for subtype, counts in subtype_counts.items():
            f.write(f"\n{subtype} references:\n")
            for term, count in counts.most_common():
                f.write(f"  {term}: {count}\n")
        
        f.write("\n=== Heading Format Analysis ===\n")
        f.write("Type heading examples:\n")
        for heading in heading_inconsistencies['type_heading_examples']:
            f.write(f"  {heading}\n")
        
        f.write("\nSubtype heading examples:\n")
        for heading in heading_inconsistencies['subtype_heading_examples']:
            f.write(f"  {heading}\n")
    
    print(f"\nAnalysis complete. Results written to {output_path}")

if __name__ == "__main__":
    main() 