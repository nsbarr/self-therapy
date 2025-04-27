#!/bin/bash

# This script extracts content from the updated markdown file and updates the index.html file

# Paths
MARKDOWN_FILE="static/27 Personalities updated 2.md"
HTML_FILE="reading-experience/index.html"
TEMP_CONTENT_FILE="/tmp/content.html"
TEMP_MARKDOWN_FILE="/tmp/modified_markdown.tmp"

echo "Starting sync process..."

# Check if files exist
if [ ! -f "$MARKDOWN_FILE" ]; then
    echo "Error: Markdown file not found at $MARKDOWN_FILE"
    exit 1
fi

if [ ! -f "$HTML_FILE" ]; then
    echo "Error: HTML file not found at $HTML_FILE"
    exit 1
fi

# Create a backup of the original HTML file
cp "$HTML_FILE" "${HTML_FILE}.backup"
echo "Created backup at ${HTML_FILE}.backup"

# Process the markdown file to fix TOC formatting
echo "Processing markdown file to fix TOC formatting..."
cp "$MARKDOWN_FILE" "$TEMP_MARKDOWN_FILE"
sed -i '' -E 's/\[([^]]+)[[:space:]]+([0-9]+)\]/\[\1 - \2\]/g' "$TEMP_MARKDOWN_FILE"

# Extract the header and footer from the original HTML
echo "Extracting header and footer from original HTML..."
MAIN_START_LINE=$(grep -n '<main class="content">' "$HTML_FILE" | cut -d':' -f1)
MAIN_END_LINE=$(grep -n '</main>' "$HTML_FILE" | cut -d':' -f1)

# Extract the part before the main content (including the main opening tag)
head -n $MAIN_START_LINE "$HTML_FILE" > "${HTML_FILE}.header"
# Extract the part after the main content (including the main closing tag)
tail -n +$MAIN_END_LINE "$HTML_FILE" > "${HTML_FILE}.footer"

# Basic Markdown to HTML conversion for our specific use case
echo "Converting markdown to HTML..."
# Skip the first table/comment block
sed '1,/\| :---- \|/d' "$TEMP_MARKDOWN_FILE" | 
# Convert headers
sed 's/^# \(.*\)$/<h1 id="\1">\1<\/h1>/g' |
sed 's/^## \(.*\)$/<h2 id="\1">\1<\/h2>/g' |
sed 's/^### \(.*\)$/<h3 id="\1">\1<\/h3>/g' |
# Convert bold text
sed 's/\*\*\(.*\)\*\*/<strong>\1<\/strong>/g' |
# Convert italics
sed 's/\*\(.*\)\*/<em>\1<\/em>/g' |
# Convert paragraphs (lines that aren't headers or empty)
awk '{if(NF>0 && !match($0, /^<h[1-6]>/) && !match($0, /<\/h[1-6]>/)) print "<p>"$0"</p>"; else print;}' |
# Convert list items
sed 's/^- \(.*\)$/<li>\1<\/li>/g' > "$TEMP_CONTENT_FILE"

# Combine header, new content, and footer
echo "Combining parts into updated HTML..."
cat "${HTML_FILE}.header" > "$HTML_FILE.new"
cat "$TEMP_CONTENT_FILE" >> "$HTML_FILE.new"
cat "${HTML_FILE}.footer" >> "$HTML_FILE.new"

# Replace the original file with the new one
mv "$HTML_FILE.new" "$HTML_FILE"

# Clean up temporary files
rm "${HTML_FILE}.header" "${HTML_FILE}.footer" "$TEMP_CONTENT_FILE" "$TEMP_MARKDOWN_FILE"

echo "Sync complete. Updated $HTML_FILE with content from $MARKDOWN_FILE"

# Optionally, rebuild the site
if [ "$1" == "--build" ]; then
  echo "Rebuilding Hugo site..."
  hugo
  echo "Site rebuilt successfully."
fi 