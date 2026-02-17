# Security Policy

## Supported Versions

Currently supported versions of DhruvKit with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in DhruvKit, please report it responsibly.

### How to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Please report vulnerabilities via email:

**dhruvgarg2025@gmail.com**

Please include "SECURITY" in the subject line.


### What to Include

When reporting a vulnerability, please include:

- **Type of vulnerability** (e.g., code injection, path traversal, etc.)
- **Full paths of affected source file(s)**
- **Location of the affected source code** (tag/branch/commit or direct URL)
- **Step-by-step instructions to reproduce the issue**
- **Proof-of-concept or exploit code** (if possible)
- **Impact of the vulnerability** and potential attack scenarios

### Response Timeline

- **Initial Response**: Within 48–72 hours
- **Status Update**: Within 14 days
- **Fix Timeline**: Depends on severity (critical issues prioritized)

### What to Expect

1. **Acknowledgment**: We'll confirm receipt of your report
2. **Assessment**: We'll validate and assess the severity
3. **Fix Development**: We'll develop and test a fix
4. **Disclosure**: We'll coordinate public disclosure with you
5. **Credit**: We'll credit you in the security advisory (if desired)

## Security Best Practices for Users

When using DhruvKit-generated projects:

### 1. Environment Variables

- **Never commit `.env` files** to version control
- Use strong, unique values for secrets
- Rotate credentials regularly
- Use different credentials for dev/staging/production

### 2. Dependencies

- **Keep dependencies updated**:
  ```bash
  pip install --upgrade dhruvkit
  pip install --upgrade -r requirements.txt
  ```
- Review security advisories for dependencies
- Use `pip-audit` or similar tools to check for vulnerabilities

### 3. Firebase Security

If using Firebase add-on:

- **Never commit service account keys** (`firebase-service-account.json`)
- Add `*.json` to `.gitignore`
- Use environment-specific service accounts
- Apply principle of least privilege to service accounts
- Rotate service account keys periodically
- Enable Firebase security rules appropriately

### 4. MongoDB Security

If using MongoDB add-on:

- **Never hardcode connection strings** in source code
- Use strong passwords for database users
- Enable IP whitelisting on MongoDB Atlas
- Use separate databases for dev/staging/production
- Enable encrypted connections (SSL/TLS)
- Regularly backup your database

### 5. API Security

For FastAPI/Flask projects:

- **Use the `--secure` add-on** for production deployments
- Enable CORS only for trusted origins
- Implement rate limiting
- Use HTTPS in production
- Validate and sanitize all user inputs
- Implement proper authentication and authorization
- Keep security headers enabled

### 6. Deployment Security

- **Use environment variables** for sensitive configuration
- Enable firewall rules to restrict access
- Use a reverse proxy (nginx, Apache) in production
- Keep your OS and runtime updated
- Monitor logs for suspicious activity
- Implement proper error handling (don't expose internals)

## Security Features in DhruvKit

### Built-in Security (FastAPI `--secure` add-on)

When using `--secure` with FastAPI templates, you get:

1. **CORS Middleware** - Configured with secure defaults
2. **Trusted Host Checking** - Prevents host header attacks
3. **Security Headers** - Industry-standard security headers
4. **Environment-based Configuration** - Proper secrets management

### File Generation Security

- Templates don't include hardcoded secrets
- `.gitignore` includes sensitive file patterns
- `.env.example` provided for reference
- Service account files excluded by default

## Vulnerability Disclosure Policy

We believe in responsible disclosure. Once a security issue is fixed:

1. We'll publish a security advisory
2. We'll credit the reporter (if desired)
3. We'll document the fix in CHANGELOG.md
4. We'll release a patched version

## Security Updates

Security updates will be:
- Released as patch versions (e.g., 0.1.1)
- Announced in CHANGELOG.md
- Documented in GitHub releases
- Marked with `[SECURITY]` tag in commit messages

## Scope

This security policy covers:
- DhruvKit CLI tool and core functionality
- Template generation code
- Default configurations in generated projects

This policy does NOT cover:
- Third-party dependencies (report to their maintainers)
- User-modified code after project generation
- Infrastructure where DhruvKit is deployed

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Flask Security](https://flask.palletsprojects.com/en/latest/security/)

## Contact

For security concerns:
- Contact: [dhruvgarg2025@gmail.com](mailto:dhruvgarg2025@gmail.com)
- Project: [GitHub Repository](https://github.com/dhruvgarg001/dhruvkit)

---

Thank you for helping keep DhruvKit and its users secure! 🔒
