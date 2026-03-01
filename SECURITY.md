# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this repository — including prompt injection patterns, unsafe template content, or exposed secrets — please report it responsibly.

**Do not open a public GitHub Issue for security vulnerabilities.**

Instead, email the maintainer directly:

📧 **[kunalsuri](https://github.com/kunalsuri)** — open a [private security advisory](https://github.com/kunalsuri/prompt-engineering-playbook/security/advisories/new) on this repository.

### What to Include

- A clear description of the vulnerability
- Steps to reproduce the issue
- The affected file(s) or section(s)
- Suggested fix (if available)

### Response Timeline

- **Acknowledgement:** within 72 hours
- **Assessment:** within 7 days
- **Fix or mitigation:** within 30 days for confirmed issues

## Scope

This policy covers:

- Prompt template content that could enable prompt injection or jailbreaking
- Secrets, API keys, or credentials accidentally committed
- CI/CD pipeline vulnerabilities
- Dependencies with known CVEs

## Supported Versions

| Version | Supported |
|---------|-----------|
| Latest (`main`) | ✅ |
| Older releases | ❌ |

Only the latest version on the `main` branch is actively maintained.
