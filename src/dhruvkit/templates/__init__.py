"""
Template loader for dhruvkit

This module dynamically loads all templates and their add-ons from the templates directory.
"""

import importlib
import pkgutil
from pathlib import Path

def load_templates():
    """Dynamically load all templates from the templates directory"""
    templates = {}
    addons = {}
    
    # Get the current package path
    package_path = Path(__file__).parent
    
    # Iterate through all Python modules in the templates directory
    for _, module_name, _ in pkgutil.iter_modules([str(package_path)]):
        if module_name.startswith('_'):  # Skip __init__ and other private modules
            continue
        
        # Import the module
        module = importlib.import_module(f'.{module_name}', package='dhruvkit.templates')
        
        # Get the TEMPLATE dictionary from the module
        if hasattr(module, 'TEMPLATE'):
            templates[module_name] = module.TEMPLATE
        
        # Get the ADDONS dictionary from the module
        if hasattr(module, 'ADDONS'):
            addons[module_name] = module.ADDONS
    
    return templates, addons

# Load all templates and addons when this module is imported
TEMPLATES, TEMPLATE_ADDONS = load_templates()
