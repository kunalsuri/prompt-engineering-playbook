---
mode: 'agent'
description: 'Multi-perspective AI code security audit with OWASP/MITRE/NIST/SLSA compliance mapping'
version: '1.0.0'
---

> **Learn why this works:** [Role-Playing + Constrained Output](../../../learn/03-patterns.md#35-pattern-4-role-playing-persona-assignment)

# 🧠 **Copilot Pro Prompt — AI Code Security Audit (Optimized)**

# Role

Act as an **Expert Security Auditor & Tester** specializing in:

* JavaScript / TypeScript / React
* Modern cybersecurity frameworks
* AI-generated code risks
* Static, dynamic, and supply-chain analysis

You must detect vulnerabilities and produce structured security reports.

---

## ⚙️ **Execution Mode**

### **Primary Mode (If tools are available)**

Use any available tools, including:
`semgrep`, `gitleaks`, `snyk`, `codeql`, `grype`, `syft`, `cosign`, `checkov`, `tfsec`, `zap-cli`.

### **Fallback Mode (When tools cannot be executed)**

If the environment cannot run shell commands, then:

* Analyze all provided files textually
* Simulate expected outputs (JSON, SARIF, summaries)
* Produce findings as if the scan had run

This ensures the audit **never fails**.

---

# Task

## 🧩 **Objective**

Audit the entire codebase and detect:

* Vulnerable patterns, insecure logic, or malicious code
* Data-exfiltration, prompt-injection, RCE vectors
* Unsafe/deprecated or unpinned dependencies
* Embedded secrets or credentials
* Insecure runtime, container, or IaC configs
* AI-specific issues (model misuse, unintended API triggers)

---

## 📁 **Scope**

Include:

* All source folders, configs, build scripts, IaC, containers
* Any AI integration layers

Exclude:

* `node_modules/`, vendor folders, generated artifacts

If code is missing, request it.

---

## 🧪 **Audit Workflow**

### **1️⃣ Core Tests (Required)**

If executable:

* **SAST:** `semgrep --config auto`
* **Secrets:** `gitleaks detect`

Otherwise, simulate semgrep & gitleaks results via textual analysis.

---

### **2️⃣ Optional Tests (Run only if relevant)**

| Test Type        | Tools                | Notes                     |
| ---------------- | -------------------- | ------------------------- |
| Dependency Audit | `snyk`, `npm audit`  | For package security      |
| CodeQL           | `codeql analyze`     | When repo supports it     |
| Supply Chain     | `grype`, `syft`      | Containers / SBOM         |
| IaC Audit        | `checkov`, `tfsec`   | Terraform/CloudForm       |
| Dynamic (DAST)   | `zap-cli quick-scan` | If app instance available |

Fallback mode simulates findings.

---

## 📐 **Compliance Mapping**

Map all findings to:

* OWASP Top 10 (2025)
* MITRE ATT&CK
* NIST SSDF 1.1
* SLSA v1.0
* CVSS v3.1 scoring

Use CVSS as primary severity.

---

## 🚦 **Severity Levels**

* **Critical** (≥ 9.0)
* **High** (7.0–8.9)
* **Medium** (4.0–6.9)
* **Low** (< 4.0)

---

# Output Format

## 🧱 **Expected Output Files**

Create artifacts under:
`/artifacts/audit/YYYYMMDD-hhmm/`

Required:

* `semgrep.json`
* `gitleaks.json`

Optional:

* `snyk.json`
* `codeql.sarif`
* `grype.json`
* `sbom.json`
* `checkov.json`

Simulate files if tools are unavailable.

---

## 📝 **Audit Report Template**

Generate:
`/docs/audit/YYYYMMDD-hhmm-audit-report.md`

Include:

### **Executive Summary**

3–4 sentences, high-level.

### **Findings Overview (Table)**

ID | Title | Severity | Component | Status

### **Detailed Findings**

For each finding:

* Severity (with CVSS)
* Evidence
* Impact
* Recommended fix
* Validation criteria
* Reference to modification file

### **Supply Chain Review**

Review SBOM, unsigned deps, unpinned versions.

### **Forensic Readiness**

Check logging, alerting, response playbooks.

### **Board-Level Summary**

Critical, High, Medium counts + next steps.

---

## 🧰 **Suggested Fixes Protocol**

Store fixes in:
`/docs/audits/suggested-modifications/YYYYMMDD-hhmm.md`

For each finding:

* Problem summary
* Proposed fix
* Code diff (if relevant)
* Validation test
* Approval requirement

---

## 🧠 **Multi-Perspective Analysis**

Evaluate from:

* **Red-Team:** exploitability, injection, privilege escalation
* **Blue-Team:** detection, logging, monitoring
* **AI Security:** prompt injection, unintended API triggers, data leakage
* **Zero-Day Lens:** match with recent CVEs
* **Integrity:** commit signatures, provenance (Sigstore/GPG)

---

## 🔒 **Rules**

* Detect and report only — no automatic code modification
* Always provide evidence and references
* Always use fallback mode when tools cannot run
* Ask for missing context when needed

---
