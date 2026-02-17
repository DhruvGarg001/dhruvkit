"""
License templates for dhruvkit

Common open source licenses that can be added to projects
License templates are stored in the license_templates/ folder as .md files
"""

from datetime import datetime
from pathlib import Path

# Mapping of license names to template files
LICENSE_ALIASES = {
    'mit': 'mit',
    'apache': 'apache',
    'apache-2.0': 'apache',
    'gpl': 'gpl',
    'gpl-2.0': 'gpl',
    'bsd': 'bsd',
    'bsd-3-clause': 'bsd',
    'unlicense': 'unlicense',
    'cc': 'cc',
    'cc0': 'cc',
    'creative-commons': 'cc',
}

# Available licenses for display
AVAILABLE_LICENSES = {
    'mit': 'MIT License (default)',
    'apache': 'Apache License 2.0',
    'gpl': 'GNU General Public License v2.0',
    'bsd': 'BSD 3-Clause License',
    'unlicense': 'The Unlicense (public domain)',
    'cc': 'Creative Commons CC0 1.0 Universal',
}

def get_license(license_name: str, project_name: str = "", author: str = "") -> str:
    """
    Get license content for the specified license type
    
    Args:
        license_name: Name of the license (e.g., 'mit', 'apache', 'gpl')
        project_name: Name of the project
        author: Author name (defaults to project name if not provided)
        
    Returns:
        License text content with placeholders replaced
    """
    license_name = license_name.lower()
    year = datetime.now().year
    author = author or project_name or "Your Name"
    
    # Get the template filename
    template_name = LICENSE_ALIASES.get(license_name, 'mit')
    
    # Load template from file
    template_path = Path(__file__).parent / 'license_templates' / f'{template_name}.md'
    
    if not template_path.exists():
        # Fallback to MIT if template not found
        template_path = Path(__file__).parent / 'license_templates' / 'mit.md'
    
    try:
        license_text = template_path.read_text(encoding='utf-8')
        
        # Replace placeholders
        license_text = license_text.replace('{YEAR}', str(year))
        license_text = license_text.replace('{AUTHOR}', author)
        license_text = license_text.replace('{PROJECT_NAME}', project_name)
        
        return license_text
    except Exception as e:
        # Fallback to basic MIT license if file reading fails
        return f"""MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
