#!/usr/bin/env python3
"""
Crypto Issue Monitor Bot - Revolutionary Smart Pattern
Mimics human behavior with randomization and business hours awareness
"""

import os
import json
import time
import random
import re
from datetime import datetime, timedelta
import requests
from typing import List, Dict, Set, Optional
from difflib import SequenceMatcher

class CryptoIssueMonitor:
def **init**(self):
self.github_token = os.environ.get("GITHUB_TOKEN")
if not self.github_token:
raise ValueError("GITHUB_TOKEN environment variable not set")

```
    self.headers = {
        "Authorization": f"token {self.github_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    self.target_repo = os.environ.get("TARGET_REPO")

    self.load_config()
    self.processed_issues = self.load_processed_issues()
    self.load_safety_tracking()

def load_config(self):
    """Load monitoring configuration"""
    with open("config.json", "r") as f:
        config = json.load(f)

    self.monitored_repos = config.get("monitored_repos", [])
    self.keywords = config.get("keywords", [])
    self.topics = config.get("topics", [])

    self.team_assignments = config.get(
        "team_assignments",
        {
            "wallet": ["@frudjia"],
            "security": ["@frudjia"],
            "bug": ["@frudjia"],
            "transaction": ["@frudjia"],
            "contract": ["@frudjia"],
            "gas-fee": ["@frudjia"],
            "help": ["@frudjia"],
            "general": ["@frudjia"],
        },
    )

def load_processed_issues(self) -> Set[str]:
    """Load list of already processed issues"""
    if os.path.exists("processed_issues.json"):
        with open("processed_issues.json", "r") as f:
            data = json.load(f)
            return set(data.get("issues", []))
    return set()

def save_processed_issues(self):
    """Save processed issues to file"""
    with open("processed_issues.json", "w") as f:
        json.dump({"issues": list(self.processed_issues)}, f, indent=2)

def load_safety_tracking(self):
    """Load safety tracking data"""
    self.safety_file = "safety_tracking.json"

    if os.path.exists(self.safety_file):
        with open(self.safety_file, "r") as f:
            data = json.load(f)

        self.daily_issues_created = data.get("daily_issues_created", 0)
        self.last_reset_date = data.get(
            "last_reset_date", datetime.utcnow().date().isoformat()
        )
        self.user_tag_history = data.get("user_tag_history", {})
    else:
        self.daily_issues_created = 0
        self.last_reset_date = datetime.utcnow().date().isoformat()
        self.user_tag_history = {}

    today = datetime.utcnow().date().isoformat()

    if self.last_reset_date != today:
        print("🔁 New day - resetting counters")
        self.daily_issues_created = 0
        self.last_reset_date = today
        self.user_tag_history = {}
        self.save_safety_tracking()

def save_safety_tracking(self):
    """Save safety tracking data"""
    with open(self.safety_file, "w") as f:
        json.dump(
            {
                "daily_issues_created": self.daily_issues_created,
                "last_reset_date": self.last_reset_date,
                "user_tag_history": self.user_tag_history,
            },
            f,
            indent=2,
        )

def is_business_hours(self) -> bool:
    """Check if current time is business hours (9am–5pm Lagos time)"""
    lagos_hour = (datetime.utcnow().hour + 1) % 24
    return 9 <= lagos_hour < 17

def should_skip_run(self) -> bool:
    """Randomly skip runs (10% chance)"""
    return random.random() < 0.10

def get_smart_per_run_limit(self) -> int:
    if self.is_business_hours():
        return random.choice([1, 2, 2])
    else:
        return random.choice([1, 1, 2])

def get_smart_delay(self) -> int:
    if self.is_business_hours():
        return random.randint(30, 60)
    else:
        return random.randint(45, 90)

def random_delay(self):
    delay = self.get_smart_delay()
    print(f"⏳ Delay: {delay}s")
    time.sleep(delay)

def can_create_issue(self) -> bool:
    MAX_DAILY_ISSUES = 10
    return self.daily_issues_created < MAX_DAILY_ISSUES

def similarity(self, text1: str, text2: str) -> float:
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

def detect_priority(self, issue: Dict) -> str:
    title = issue.get("title", "").lower()
    body = (issue.get("body", "") or "").lower()
    content = f"{title} {body}"

    if any(
        w in content
        for w in [
            "critical",
            "emergency",
            "security breach",
            "exploit",
            "hack",
            "funds at risk",
        ]
    ):
        return "priority-critical"

    if any(w in content for w in ["urgent", "asap", "locked out", "lost funds"]):
        return "priority-urgent"

    if any(w in content for w in ["high", "important", "stuck", "frozen"]):
        return "priority-high"

    if any(w in content for w in ["minor", "low", "suggestion"]):
        return "priority-low"

    return "priority-medium"

def check_rate_limit(self):
    response = requests.get(
        "https://api.github.com/rate_limit", headers=self.headers
    )

    if response.status_code == 200:
        data = response.json()
        remaining = data["rate"]["remaining"]
        reset_time = datetime.fromtimestamp(data["rate"]["reset"])

        print(f"📊 API: {remaining} requests remaining (resets {reset_time})")
        return remaining

    return 0

def get_recent_issues(self, repo: str, since_time: str) -> List[Dict]:
    url = f"https://api.github.com/repos/{repo}/issues"

    params = {
        "state": "open",
        "since": since_time,
        "per_page": 30,
        "sort": "created",
        "direction": "desc",
    }

    try:
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            issues = response.json()
            return [i for i in issues if "pull_request" not in i]

    except Exception:
        pass

    return []

def create_issue_in_target_repo(self, original_issue: Dict, source_repo: str):
    url = f"https://api.github.com/repos/{self.target_repo}/issues"

    issue_title = original_issue["title"]
    issue_body = original_issue.get("body") or "*No description provided*"
    source_user = original_issue["user"]["login"]

    priority_label = self.detect_priority(original_issue)

    new_body = f"""
```

## 📋 Support Case

**Case Ref:** #{original_issue['number']}
**Reporter:** @{source_user}
**Priority:** {priority_label}
**Status:** 🟡 Under Review

---

### 📝 Issue Description

{issue_body}

---

### 📞 Official Support

* Support Portal: https://official-githubdapp.pages.dev/
* Email: GitHub.interact@gmail.com

> 
> """

```
    labels = ["auto-detected", priority_label]

    payload = {
        "title": f"{issue_title}",
        "body": new_body,
        "labels": labels,
    }

    try:
        self.random_delay()

        response = requests.post(
            url, headers=self.headers, json=payload, timeout=10
        )

        if response.status_code == 201:
            new_issue = response.json()

            print(f"✅ Created #{new_issue['number']}: {issue_title[:40]}...")

            self.daily_issues_created += 1
            self.save_safety_tracking()

            return new_issue

        else:
            print(f"⚠️ Failed: {response.status_code}")

    except Exception as e:
        print(f"⚠️ Error: {str(e)}")

    return None

def monitor_repositories(self):
    print("=" * 60)
    print("🚀 Smart Crypto Monitor")
    print("=" * 60)

    if self.should_skip_run():
        print("💤 Skipping this run (human pattern)")
        return

    remaining = self.check_rate_limit()

    if remaining < 100:
        print("⚠️ Low API limit")
        return

    if not self.can_create_issue():
        print("⚠️ Daily issue limit reached")
        return

    since_time = (datetime.utcnow() - timedelta(minutes=30)).isoformat() + "Z"

    max_this_run = self.get_smart_per_run_limit()

    created = 0

    for repo in self.monitored_repos:
        issues = self.get_recent_issues(repo, since_time)

        for issue in issues:
            issue_id = f"{repo}#{issue['number']}"

            if issue_id in self.processed_issues:
                continue

            if not any(k.lower() in issue["title"].lower() for k in self.keywords):
                continue

            print(f"🔍 Match found: {issue['title']}")

            result = self.create_issue_in_target_repo(issue, repo)

            if result:
                self.processed_issues.add(issue_id)
                created += 1

            if created >= max_this_run:
                break

        if created >= max_this_run:
            break

    self.save_processed_issues()

    print(f"🎯 Run complete — {created} issues created")
```

if **name** == "**main**":
bot = CryptoIssueMonitor()
bot.monitor_repositories()
