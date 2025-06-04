import re
import os
import markdown
from pathlib import Path
from bs4 import BeautifulSoup

def read_file(file_path):
    """Read the content of a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content):
    """Write content to a file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def extract_toc(soup):
    """Extract table of contents from headings."""
    headings = soup.find_all(['h1', 'h2'])
    toc = []
    
    for heading in headings:
        level = int(heading.name[1])
        text = heading.get_text()
        # Create an ID based on the heading text
        heading_id = text.lower().replace(' ', '-').replace(':', '').replace('/', '-')
        # Add id attribute to the heading
        heading['id'] = heading_id
        
        toc.append((level, text, heading_id))
    
    return toc

def generate_toc_html(toc):
    """Generate HTML for table of contents."""
    toc_html = ['<ul class="toc-list">']
    
    prev_level = 1
    for level, text, heading_id in toc:
        if level > prev_level:
            toc_html.append('<ul class="toc-sublist">')
        elif level < prev_level:
            # Close the number of levels we've moved up
            for _ in range(prev_level - level):
                toc_html.append('</ul>')
        
        # Add TOC entry
        toc_html.append(f'<li class="toc-item toc-level-{level}"><a href="#{heading_id}">{text}</a></li>')
        
        prev_level = level
    
    # Close any remaining open lists
    for _ in range(prev_level - 1):
        toc_html.append('</ul>')
    
    toc_html.append('</ul>')
    
    return '\n'.join(toc_html)

def transform_markdown_to_html(markdown_text):
    """Transform markdown to HTML with custom processing."""
    # Convert markdown to HTML
    html = markdown.markdown(markdown_text, extensions=['tables', 'fenced_code', 'toc'])
    
    # Parse HTML for further processing
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract table of contents
    toc = extract_toc(soup)
    toc_html = generate_toc_html(toc)
    
    # Return both the processed HTML and TOC HTML
    return str(soup), toc_html

def generate_html_page(markdown_text, title="27 Personalities in Search of Being"):
    """Generate a full HTML page from markdown content."""
    # Transform markdown to HTML
    content_html, toc_html = transform_markdown_to_html(markdown_text)
    
    # Template for the full HTML page
    html_template = f"""<!DOCTYPE html>
<html lang="en" class="light-mode">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="/css/reading-experience-custom.css">
</head>
<body class="reading-experience">
    <div class="progress-container">
        <div class="progress-bar" id="readingProgress"></div>
    </div>
    
    <div class="reading-preferences">
        <button id="darkModeToggle" class="preference-button" title="Toggle Dark Mode">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
            </svg>
        </button>
    </div>
    
    <div class="container">
        <header>
            <h1 class="book-title">{title}</h1>
            <div class="book-subtitle">by Claudio Naranjo</div>
        </header>
        
        <div class="content-wrapper">
            <aside class="toc-container">
                <div class="toc-header">Table of Contents</div>
                <div class="toc-content">
                    {toc_html}
                </div>
            </aside>
            
            <main class="content">
                {content_html}
            </main>
        </div>
        
        <footer>
            <p>English translation. Original title: "27 Personajes en Busca de Ser" by Claudio Naranjo</p>
        </footer>
    </div>

    <script>
        /* JavaScript for table of contents functionality */
        document.addEventListener('DOMContentLoaded', function() {{
            /* Highlight the current section in the TOC */
            const observer = new IntersectionObserver(entries => {{
                entries.forEach(entry => {{
                    const id = entry.target.getAttribute('id');
                    if (entry.intersectionRatio > 0) {{
                        document.querySelectorAll('.toc-item a').forEach(link => {{
                            link.classList.remove('active');
                            if (link.getAttribute('href') === '#' + id) {{
                                link.classList.add('active');
                            }}
                        }});
                    }}
                }});
            }}, {{ rootMargin: '0px 0px -80% 0px' }});

            /* Track all headings */
            document.querySelectorAll('h1[id], h2[id]').forEach(heading => {{
                observer.observe(heading);
            }});
            
            /* Smooth scrolling for TOC links */
            document.querySelectorAll('.toc-item a').forEach(link => {{
                link.addEventListener('click', e => {{
                    e.preventDefault();
                    const targetId = link.getAttribute('href').substring(1);
                    const targetElement = document.getElementById(targetId);
                    
                    if (targetElement) {{
                        window.scrollTo({{
                            top: targetElement.offsetTop - 20,
                            behavior: 'smooth'
                        }});
                    }}
                }});
            }});
            
            /* Mobile TOC toggle */
            const tocToggle = document.createElement('button');
            tocToggle.classList.add('toc-toggle');
            tocToggle.textContent = 'Table of Contents';
            document.querySelector('.container').prepend(tocToggle);
            
            tocToggle.addEventListener('click', () => {{
                const tocContainer = document.querySelector('.toc-container');
                tocContainer.classList.toggle('toc-open');
                tocToggle.classList.toggle('toc-toggle-active');
            }});
            
            /* Reading Progress Bar */
            window.addEventListener('scroll', function() {{
                const windowHeight = window.innerHeight;
                const documentHeight = document.body.scrollHeight - windowHeight;
                const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
                const progress = Math.max(0, Math.min(100, (scrollTop / documentHeight) * 100));
                
                document.getElementById('readingProgress').style.width = progress + '%';
            }});
            
            /* Dark Mode Toggle */
            const darkModeToggle = document.getElementById('darkModeToggle');
            darkModeToggle.addEventListener('click', () => {{
                document.documentElement.classList.toggle('dark-mode');
                document.documentElement.classList.toggle('light-mode');
                
                // Save preference to localStorage
                const isDarkMode = document.documentElement.classList.contains('dark-mode');
                localStorage.setItem('darkMode', isDarkMode);
            }});
            
            /* Load user preferences from localStorage */
            if (localStorage.getItem('darkMode') === 'true') {{
                document.documentElement.classList.add('dark-mode');
                document.documentElement.classList.remove('light-mode');
            }}
        }});
    </script>
</body>
</html>
"""
    
    return html_template

def generate_css():
    """Generate CSS for the reading experience."""
    css = """/* Base Styles */
:root {
    --text-color: #333;
    --bg-color: #fff;
    --accent-color: #6b46c1;
    --light-accent: #e9e4f0;
    --muted-color: #718096;
    --border-color: #e2e8f0;
    --toc-bg: #f8f9fa;
    --toc-width: 280px;
    --content-width: 720px;
    --heading-font: 'Georgia', serif;
    --body-font: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

/* Dark Mode */
.dark-mode {
    --text-color: #e2e8f0;
    --bg-color: #1a202c;
    --accent-color: #9f7aea;
    --light-accent: #4a5568;
    --muted-color: #a0aec0;
    --border-color: #4a5568;
    --toc-bg: #2d3748;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: var(--body-font);
    color: var(--text-color);
    line-height: 1.6;
    background-color: var(--bg-color);
    font-size: 18px;
    transition: background-color 0.3s ease, color 0.3s ease;
}

/* Font Size Preferences */
body[data-font-size="small"] {
    font-size: 16px;
}

body[data-font-size="medium"] {
    font-size: 18px;
}

body[data-font-size="large"] {
    font-size: 20px;
}

.container {
    max-width: calc(var(--content-width) + var(--toc-width) + 80px);
    margin: 0 auto;
    padding: 0 20px;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    font-family: var(--heading-font);
    margin: 2rem 0 1rem;
    line-height: 1.3;
    transition: color 0.3s ease;
}

h1 {
    font-size: 2.5rem;
    border-bottom: 2px solid var(--light-accent);
    padding-bottom: 0.5rem;
    margin-top: 3rem;
}

h2 {
    font-size: 1.8rem;
    border-bottom: 1px solid var(--light-accent);
    padding-bottom: 0.3rem;
}

a {
    color: var(--accent-color);
    text-decoration: none;
    transition: color 0.3s ease;
}

a:hover {
    text-decoration: underline;
}

p {
    margin-bottom: 1.5rem;
    transition: color 0.3s ease, opacity 0.3s ease;
}

blockquote {
    border-left: 4px solid var(--light-accent);
    padding-left: 1rem;
    font-style: italic;
    margin: 1.5rem 0;
    color: var(--muted-color);
    transition: border-color 0.3s ease, color 0.3s ease;
}

code {
    font-family: Consolas, Monaco, 'Andale Mono', monospace;
    background-color: var(--light-accent);
    padding: 0.2rem 0.4rem;
    border-radius: 3px;
    transition: background-color 0.3s ease, color 0.3s ease;
}

pre {
    padding: 1rem;
    background-color: var(--light-accent);
    border-radius: 5px;
    overflow-x: auto;
    margin: 1.5rem 0;
    transition: background-color 0.3s ease;
}

/* Header & Footer */
header {
    text-align: center;
    padding: 3rem 0;
}

.book-title {
    font-size: 3rem;
    margin: 0;
    color: var(--accent-color);
    border-bottom: none;
    transition: color 0.3s ease;
}

.book-subtitle {
    font-size: 1.4rem;
    color: var(--muted-color);
    font-style: italic;
    margin-top: 0.5rem;
    transition: color 0.3s ease;
}

footer {
    margin-top: 4rem;
    padding: 2rem 0;
    border-top: 1px solid var(--border-color);
    text-align: center;
    color: var(--muted-color);
    font-size: 0.9rem;
    transition: border-color 0.3s ease, color 0.3s ease;
}

/* Content Layout */
.content-wrapper {
    display: flex;
    gap: 40px;
    position: relative;
}

.content {
    flex: 1;
    max-width: var(--content-width);
    margin: 0 auto;
    padding-bottom: 4rem;
}

/* Table of Contents */
.toc-container {
    width: var(--toc-width);
    position: sticky;
    top: 20px;
    align-self: flex-start;
    max-height: calc(100vh - 40px);
    overflow-y: auto;
    padding: 1.5rem;
    background-color: var(--toc-bg);
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.toc-header {
    font-weight: bold;
    font-size: 1.2rem;
    margin-bottom: 1rem;
    color: var(--accent-color);
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 0.5rem;
    transition: color 0.3s ease, border-color 0.3s ease;
}

.toc-list, .toc-sublist {
    list-style: none;
}

.toc-item {
    margin-bottom: 0.5rem;
}

.toc-level-1 {
    font-weight: bold;
    margin-top: 0.8rem;
}

.toc-level-2 {
    padding-left: 1rem;
    font-size: 0.95rem;
}

.toc-item a {
    display: block;
    padding: 0.3rem 0;
    transition: background-color 0.2s, color 0.2s;
    border-radius: 4px;
}

.toc-item a:hover {
    background-color: var(--light-accent);
    text-decoration: none;
}

.toc-item a.active {
    background-color: var(--light-accent);
    color: var(--accent-color);
    font-weight: bold;
}

/* Table Styles */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.5rem 0;
    transition: border-color 0.3s ease;
}

th, td {
    padding: 0.75rem;
    border: 1px solid var(--border-color);
    transition: border-color 0.3s ease, background-color 0.3s ease;
}

th {
    background-color: var(--light-accent);
}

/* Responsive Layout */
.toc-toggle {
    display: none;
    width: 100%;
    padding: 0.8rem;
    background-color: var(--accent-color);
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-bottom: 1rem;
    font-size: 1rem;
    transition: background-color 0.3s ease;
}

/* Reading Preferences */
.reading-preferences {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 100;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.preference-button {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: none;
    background-color: var(--accent-color);
    color: white;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.3s ease, transform 0.2s ease;
}

.preference-button:hover {
    transform: scale(1.1);
}

.preference-button svg {
    width: 20px;
    height: 20px;
}

/* Reading Progress Bar */
.progress-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    z-index: 1000;
    background-color: var(--border-color);
}

.progress-bar {
    height: 4px;
    background-color: var(--accent-color);
    width: 0%;
    transition: width 0.1s ease;
}

/* Focus Mode */
.focus-mode .content p:not(:hover),
.focus-mode .content li:not(:hover) {
    opacity: 0.5;
    transition: opacity 0.3s ease;
}

.focus-mode .content p:hover,
.focus-mode .content li:hover {
    opacity: 1;
}

@media (max-width: 1100px) {
    .content-wrapper {
        flex-direction: column;
    }
    
    .toc-container {
        width: 100%;
        position: static;
        max-height: none;
        margin-bottom: 2rem;
        display: none;
    }
    
    .toc-toggle {
        display: block;
    }
    
    .toc-open {
        display: block;
    }
    
    .toc-toggle-active {
        background-color: var(--muted-color);
    }
    
    .reading-preferences {
        top: auto;
        bottom: 20px;
        right: 20px;
    }
}

@media (max-width: 768px) {
    .reading-preferences {
        flex-direction: row;
    }
}

@media (max-width: 600px) {
    :root {
        --content-width: 100%;
    }
    
    body {
        font-size: 16px;
    }
    
    .container {
        padding: 0 15px;
    }
    
    .book-title {
        font-size: 2rem;
    }
    
    .book-subtitle {
        font-size: 1.1rem;
    }
    
    h1 {
        font-size: 1.8rem;
    }
    
    h2 {
        font-size: 1.4rem;
    }
}

/* Additional Reading Enhancements */
.content p {
    text-align: justify;
    hyphens: auto;
}

.content img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 2rem auto;
    border-radius: 4px;
    transition: filter 0.3s ease;
}

.dark-mode .content img {
    filter: brightness(0.8) contrast(1.2);
}

/* Print Styles */
@media print {
    .toc-container, .toc-toggle, .progress-container, .reading-preferences {
        display: none !important;
    }
    
    .content {
        max-width: 100%;
        margin: 0;
    }
    
    body {
        font-size: 12pt;
    }
    
    a {
        text-decoration: none;
        color: black;
    }
    
    h1, h2, h3, h4, h5, h6 {
        page-break-after: avoid;
        page-break-inside: avoid;
    }
    
    table, figure {
        page-break-inside: avoid;
    }
    
    p {
        orphans: 3;
        widows: 3;
    }
}
"""
    
    return css

def main():
    # Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, '../../reading-experience')
    input_file = os.path.join(script_dir, 'content.md')
    output_file = os.path.join(output_dir, 'index.html')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Read markdown content
    markdown_text = read_file(input_file)
    
    # Generate HTML page
    html_content = generate_html_page(markdown_text)
    
    # Write HTML file
    write_file(output_file, html_content)
    
    print(f"Successfully generated {output_file}")

if __name__ == '__main__':
    main() 