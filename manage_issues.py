#!/usr/bin/env python3
"""
manage_issues.py
Automated GitHub Issue Manager for JCTA Manuscript Reviewer Comments.
Dynamically retrieves GitHub credentials via git-credential helper.
"""

import os
import json
import subprocess
import urllib.request
import urllib.error

REPO = "festomanolo/swahili-SL"
API_BASE = f"https://api.github.com/repos/{REPO}"

def get_github_token():
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    try:
        p = subprocess.Popen(["git", "credential", "fill"],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             text=True)
        out, _ = p.communicate("host=github.com\nprotocol=https\n\n")
        for line in out.splitlines():
            if line.startswith("password="):
                return line.split("=", 1)[1].strip()
    except Exception:
        pass
    return None

TOKEN = get_github_token()

HEADERS = {
    "Authorization": f"token {TOKEN}" if TOKEN else "",
    "Accept": "application/vnd.github.v3+json",
    "Content-Type": "application/json",
    "User-Agent": "SwSL-Reviewer-Automation"
}

def api_request(endpoint, data=None, method="GET"):
    url = f"{API_BASE}/{endpoint.lstrip('/')}"
    req = urllib.request.Request(url, headers=HEADERS, method=method)
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        req.data = body
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"HTTP Error {e.code} on {method} {url}: {err_msg}")
        return None

def create_issue(title, body, labels=None):
    payload = {"title": title, "body": body}
    if labels:
        payload["labels"] = labels
    return api_request("issues", payload, method="POST")

def add_comment(issue_number, comment):
    return api_request(f"issues/{issue_number}/comments", {"body": comment}, method="POST")

def close_issue(issue_number):
    return api_request(f"issues/{issue_number}", {"state": "closed"}, method="PATCH")

def get_open_issues():
    return api_request("issues?state=open") or []

def get_all_issues():
    return api_request("issues?state=all") or []

if __name__ == "__main__":
    print(f"Connecting to GitHub API for {REPO}...")
    issues = get_all_issues()
    print(f"Connected successfully. Current issues count: {len(issues)}")
