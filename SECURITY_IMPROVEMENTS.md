# Security Improvements - Input Sanitization

## Overview
This document outlines the security improvements made to the Grimorio T20 application to protect against common web vulnerabilities.

## Changes Made

### 1. Installed Security Libraries
- **markdown**: For safe markdown-to-HTML conversion
- **bleach**: For HTML sanitization and XSS prevention

Installation command:
```bash
pip install markdown bleach
```

### 2. Added Sanitization Functions (spell/views.py)

#### sanitize_input()
A comprehensive input sanitization function that:
- **Prevents SQL Injection**: Removes common SQL injection patterns (UNION SELECT, DROP TABLE, etc.)
- **Prevents XSS Attacks**: Escapes HTML for regular fields or allows only safe HTML tags for markdown fields
- **Configurable**: Can be used with or without markdown support

Parameters:
- `text`: The text to sanitize
- `allow_markdown`: Boolean flag to allow safe HTML tags (for markdown content)

#### render_markdown()
Converts markdown text to HTML with built-in sanitization:
- Uses markdown library with 'extra' and 'nl2br' extensions
- Automatically sanitizes the output to prevent XSS
- Returns safe HTML string

### 3. Applied Sanitization to User Inputs

#### create_spell() Function
All user inputs are now sanitized before saving:
- `name`: Sanitized (no HTML)
- `execution`: Sanitized (no HTML)
- `range`: Sanitized (no HTML)
- `duration`: Sanitized (no HTML)
- `resistance`: Sanitized (no HTML)
- `description`: Sanitized (HTML escaped, ready for markdown)
- `enhancement cost`: Sanitized (no HTML)
- `enhancement effect`: Sanitized (HTML escaped)

#### edit_spell() Function
Same sanitization applied as in create_spell():
- All spell fields are sanitized before updating
- Enhancement fields are sanitized before saving

### 4. SQL Injection Protection

The sanitize_input() function removes or neutralizes:
- UNION SELECT attacks
- DROP TABLE commands
- INSERT INTO statements
- DELETE FROM statements
- UPDATE SET commands
- SQL comments (-- and ;)
- OR-based injection attempts ('OR'='')

### 5. XSS Protection

For regular text fields:
- All HTML is escaped using Django's escape()
- User cannot inject <script> tags or other dangerous HTML

For markdown-enabled fields (when implemented):
- Only safe HTML tags are allowed (p, br, strong, em, h1-h6, ul, ol, li, blockquote, code, pre, a, img, table elements)
- Dangerous attributes are stripped
- Script tags and event handlers are removed
- Uses bleach library's whitelist approach

## Security Benefits

### Before Implementation
- User inputs were stored directly in the database
- No protection against HTML/JavaScript injection
- SQL injection patterns could potentially be exploited
- XSS vulnerabilities in user-generated content

### After Implementation
- All user inputs are sanitized before storage
- HTML/JavaScript injection is prevented
- SQL injection patterns are removed
- XSS attacks are mitigated through HTML escaping
- Safe subset of HTML allowed for markdown content

## Testing Recommendations

To verify the security improvements:

1. **SQL Injection Test**:
   - Try entering: `'; DROP TABLE spell_spell; --`
   - Expected: Pattern removed, no database impact

2. **XSS Test**:
   - Try entering: `<script>alert('XSS')</script>`
   - Expected: HTML escaped, displays as text

3. **Markdown Test** (when template filter is added):
   - Try entering: `**Bold** and <script>alert('XSS')</script>`
   - Expected: Bold works, script is removed

## Future Enhancements

1. **Template Filter**: Create a custom Django template filter to render markdown safely in templates
2. **Input Validation**: Add more specific validation rules for each field
3. **Rate Limiting**: Implement rate limiting for form submissions
4. **CSRF Protection**: Ensure Django's CSRF protection is enabled (already built-in)
5. **Content Security Policy**: Add CSP headers to prevent inline scripts

## Notes

- The current implementation escapes HTML in all fields by default
- To enable markdown rendering in the frontend, you'll need to:
  1. Create a template filter using the `render_markdown()` function
  2. Update templates to use the filter with `|safe` tag
  3. Test thoroughly to ensure no XSS vulnerabilities

## Dependencies

Add to `requirements.txt`:
```
markdown==3.10.2
bleach==6.3.0