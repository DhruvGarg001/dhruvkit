# License Templates

This folder contains license templates that can be added to projects created with DhruvKit.

## Available Licenses

- `mit.md` - MIT License (default)
- `apache.md` - Apache License 2.0
- `gpl.md` - GNU General Public License v3.0
- `bsd.md` - BSD 3-Clause License
- `unlicense.md` - The Unlicense (public domain)

## Template Format

Each license file is a Markdown file with placeholders that get replaced when the license is generated:

- `{YEAR}` - Current year
- `{AUTHOR}` - Author name (defaults to project name)
- `{PROJECT_NAME}` - Name of the project

## Adding a New License

To add a new license:

1. Create a new `.md` file in this directory with the license name (e.g., `isc.md`)
2. Add the license text with placeholders for dynamic values:

```markdown
ISC License

Copyright (c) {YEAR} {AUTHOR}

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES...
```

3. Update `licenses.py` to include the new license in the `LICENSE_ALIASES` dictionary:

```python
LICENSE_ALIASES = {
    # ... existing licenses ...
    'isc': 'isc',
}
```

4. Update `AVAILABLE_LICENSES` dictionary with a description:

```python
AVAILABLE_LICENSES = {
    # ... existing licenses ...
    'isc': 'ISC License',
}
```

The license will be automatically available as: `dhruvkit new myproject --license isc`

## Notes

- License filenames should be lowercase
- Use standard SPDX identifiers when possible (mit, apache, gpl, bsd, etc.)
- Keep the original license text intact - only add placeholders where needed
- Test your license template by creating a new project with it
