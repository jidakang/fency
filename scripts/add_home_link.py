#!/usr/bin/env python3
import os
import re
import glob

def add_home_link(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # More accurate check for existing home links
    home_link_patterns = [
        r'href="[^"]*index\.html"',
        r'<a[^>]*home[^>]*>',
        r'<i[^>]*fa-home[^>]*>'
    ]
    
    for pattern in home_link_patterns:
        if re.search(pattern, content):
            print(f"🔍 Home link already exists in {file_path}")
            return False
    
    # Find the navigation section
    nav_section = None
    
    # Common navigation patterns
    nav_patterns = [
        # Pattern 1: Standard nav tag
        r'<nav[^>]*>.*?<div[^>]*>.*?<div[^>]*>',
        # Pattern 2: Navigation div
        r'<div[^>]*class="[^"]*navbar[^"]*"[^>]*>',
        # Pattern 3: Header with nav
        r'<header[^>]*>.*?<div[^>]*>',
        # Pattern 4: Any nav tag
        r'<nav[^>]*>'
    ]
    
    for pattern in nav_patterns:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            nav_section = match.group(0)
            insertion_point = match.end(0)
            break
    
    # If we found a navigation section
    if nav_section:
        # Home link HTML to insert
        home_link_html = '''
        <a href="/index.html" class="flex items-center mr-3 text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 transition-colors" title="返回首页">
            <i class="fas fa-home text-xl"></i>
        </a>
        '''
        
        # Insert the home link after the navigation opening
        modified_content = content[:insertion_point] + home_link_html + content[insertion_point:]
        
        # Write the modified content back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)
        
        print(f"✅ Added home link to {file_path}")
        return True
    else:
        # If no navigation section found, let's add one after the body tag
        body_tag = re.search(r'<body[^>]*>', content)
        if body_tag:
            body_end = body_tag.end(0)
            nav_html = '''
    <nav class="sticky top-0 z-50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-b border-gray-200 dark:border-gray-800">
        <div class="container mx-auto px-4 py-2">
            <div class="flex items-center">
                <a href="/index.html" class="flex items-center mr-3 text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 transition-colors" title="返回首页">
                    <i class="fas fa-home text-xl"></i>
                </a>
            </div>
        </div>
    </nav>
            '''
            modified_content = content[:body_end] + nav_html + content[body_end:]
            
            # Write the modified content back to the file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(modified_content)
            
            print(f"✅ Added new navigation with home link to {file_path}")
            return True
        else:
            print(f"❌ Could not add home link to {file_path} - no suitable insertion point found")
            return False

def process_all_html_files():
    html_files = glob.glob('pages/**/*.html', recursive=True)
    
    modified_count = 0
    failed_count = 0
    skipped_count = 0
    
    for file_path in html_files:
        result = add_home_link(file_path)
        if result is True:
            modified_count += 1
        elif result is False:
            skipped_count += 1
        else:
            failed_count += 1
    
    print(f"\n== Summary ==")
    print(f"📊 Processed {len(html_files)} HTML files")
    print(f"✅ Modified: {modified_count}")
    print(f"🔍 Skipped (already had home link): {skipped_count}")
    print(f"❌ Failed: {failed_count}")

if __name__ == "__main__":
    process_all_html_files() 