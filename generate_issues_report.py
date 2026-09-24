#!/usr/bin/env python3
"""
generate_issues_report.py
Generates a clean markdown table summarizing all 22 GitHub issues and their resolutions.
"""

import manage_issues

def main():
    issues = manage_issues.get_all_issues()
    lines = [
        "# SwSL Reviewer Response: GitHub Issues & Empirical Evidence Registry",
        "",
        "This registry records all GitHub issues created, empirically commented on, and resolved for the JCTA manuscript revision across Reviewer A and Reviewer B comments.",
        "",
        "| Issue | Status | Reviewer & Topic | Issue URL |",
        "|:---:|:---:|:---|:---:|"
    ]
    for iss in sorted(issues, key=lambda x: x["number"]):
        num = iss["number"]
        title = iss["title"].replace("|", "-")
        state = iss["state"].upper()
        url = iss["html_url"]
        lines.append(f"| **#{num}** | `{state}` | {title} | [View #{num}]({url}) |")

    with open("outputs/GITHUB_ISSUES_REPORT.md", "w") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Generated outputs/GITHUB_ISSUES_REPORT.md with {len(issues)} issues.")

if __name__ == "__main__":
    main()
