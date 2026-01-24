# LogHunter - Quick Start Guides

## 📖 ABOUT THESE GUIDES

Each Team Brain agent has a **5-minute quick-start guide** tailored to their role and workflows.

**Choose your guide:**
- [Forge (Orchestrator)](#forge-quick-start)
- [Atlas (Executor)](#atlas-quick-start)
- [Clio (Linux Agent)](#clio-quick-start)
- [Nexus (Multi-Platform)](#nexus-quick-start)
- [Bolt (Free Executor)](#bolt-quick-start)
- [Logan (Human User)](#logan-quick-start)

---

## 🔥 FORGE QUICK START

**Role:** Orchestrator / Reviewer  
**Time:** 5 minutes  
**Goal:** Learn to use LogHunter for session log review and pattern analysis

### Step 1: Installation Check
```bash
# Verify LogHunter is available
cd C:\Users\logan\OneDrive\Documents\AutoProjects\LogHunter
python loghunter.py --help

# Expected: Help message with all commands
```

### Step 2: First Use - Session Log Analysis
```python
# In your Forge session
import sys
sys.path.insert(0, "C:/Users/logan/OneDrive/Documents/AutoProjects/LogHunter")
from loghunter import LogHunter

# Load session logs
hunter = LogHunter()
hunter.load_files("D:/BEACON_HQ/MEMORY_CORE_V2/02_SESSION_LOGS/*.md")

# Get overview
stats = hunter.get_statistics()
print(f"Session logs: {stats['total_lines']} lines, {stats['errors']} errors")
```

### Step 3: Common Forge Tasks

**Task 1: Review Team Session Quality**
```python
# Find errors across all session logs
errors = hunter.get_errors()
print(f"Found {len(errors)} errors in session logs")

# Show error context
for error in errors[:3]:
    print(f"\n{error.file_path}:{error.line_num}")
    print(f"  {error.line[:80]}...")
```

**Task 2: Find Recurring Patterns**
```python
# Identify systematic issues
patterns = hunter.get_top_patterns(10)
print("Top recurring patterns:")
for i, (pattern, count) in enumerate(patterns, 1):
    print(f"  {i}. ({count}x) {pattern[:60]}")
```

**Task 3: Quick Health Check**
```bash
# CLI quick stats
loghunter stats "D:\BEACON_HQ\MEMORY_CORE_V2\02_SESSION_LOGS\*.md"
```

### Step 4: Integration with Forge Workflows
```python
# At session start - quick health check
from loghunter import LogHunter
from synapselink import quick_send

hunter = LogHunter()
hunter.load_files("logs/*.log")
stats = hunter.get_statistics()

if stats['errors'] > 50:
    quick_send("TEAM", "[ALERT] High Error Count", 
               f"Found {stats['errors']} errors - investigate!", 
               priority="HIGH")
```

### Next Steps for Forge
1. Read [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) - Forge section
2. Try [EXAMPLES.md](EXAMPLES.md) - Example 10 (Production workflow)
3. Add log health check to daily orchestration routine

---

## ⚡ ATLAS QUICK START

**Role:** Executor / Builder  
**Time:** 5 minutes  
**Goal:** Learn to use LogHunter for debugging tool builds and test failures

### Step 1: Installation Check
```bash
# Quick verification
python -c "from loghunter import LogHunter; print('[OK] LogHunter ready')"
```

### Step 2: First Use - Debug Build Errors
```python
# In your Atlas tool-building session
import sys
sys.path.insert(0, "C:/Users/logan/OneDrive/Documents/AutoProjects/LogHunter")
from loghunter import LogHunter

# Load build/test output
hunter = LogHunter()
hunter.load_file("test_output.log")

# Find failures
errors = hunter.get_errors()
print(f"Build errors: {len(errors)}")

for error in errors[:5]:
    print(f"  Line {error.line_num}: {error.line[:70]}...")
```

### Step 3: Common Atlas Tasks

**Task 1: Analyze Test Failures**
```bash
# Quick CLI check
loghunter errors test_output.log
loghunter search test_output.log "FAIL" -c 3
```

**Task 2: Find Exception Stack Traces**
```python
hunter = LogHunter()
hunter.load_file("build.log")

exceptions = hunter.get_exceptions()
print(f"Found {len(exceptions)} exception(s)")

# Get context around first exception
if exceptions:
    exc_idx = hunter.lines.index(exceptions[0])
    context = hunter.context([exc_idx], before=5, after=10)
    for line in context:
        print(line.line)
```

**Task 3: Compare Before/After**
```bash
# Errors before fix
loghunter errors old_build.log | wc -l

# Errors after fix
loghunter errors new_build.log | wc -l
```

### Step 4: Integrate into Tool Build Workflow
```python
# Add to test scripts
import subprocess
from loghunter import LogHunter

# Run tests and capture output
result = subprocess.run(
    ["python", "test_tool.py"],
    capture_output=True,
    text=True
)

# Save output
with open("test_output.log", "w") as f:
    f.write(result.stdout + result.stderr)

# Analyze
hunter = LogHunter()
hunter.load_file("test_output.log")
errors = hunter.get_errors()

if errors:
    print(f"[X] Build failed with {len(errors)} errors")
    for e in errors[:3]:
        print(f"    {e.line[:70]}")
else:
    print("[OK] All tests passed!")
```

### Next Steps for Atlas
1. Integrate into Holy Grail automation
2. Add to tool build checklist
3. Use for every new tool build

---

## 🐧 CLIO QUICK START

**Role:** Linux / Ubuntu Agent  
**Time:** 5 minutes  
**Goal:** Learn to use LogHunter for system log analysis

### Step 1: Linux Installation
```bash
# Clone from GitHub
git clone https://github.com/DonkRonk17/LogHunter.git
cd LogHunter

# Install (editable mode)
pip3 install -e .

# Verify
loghunter --help
```

### Step 2: First Use - System Log Analysis
```bash
# Analyze syslog
loghunter errors /var/log/syslog

# Auth log for failed logins
loghunter search /var/log/auth.log "Failed password"

# Quick stats
loghunter stats /var/log/syslog
```

### Step 3: Common Clio Tasks

**Task 1: Monitor Recent System Errors**
```bash
# Errors in last hour
loghunter errors /var/log/syslog --since 1h

# Errors in last 24 hours with limit
loghunter errors /var/log/syslog --since 24h -l 50
```

**Task 2: Analyze Service Logs**
```bash
# Nginx errors
loghunter errors /var/log/nginx/error.log

# Find 500 errors in access log
loghunter search /var/log/nginx/access.log " 500 "

# Apache analysis
loghunter patterns /var/log/apache2/error.log -n 20
```

**Task 3: Security Monitoring**
```bash
# Failed SSH attempts
loghunter search /var/log/auth.log "Failed" -c 1

# Sudo usage
loghunter search /var/log/auth.log "sudo" --since 24h
```

### Step 4: Automation Script
```bash
#!/bin/bash
# daily_log_check.sh

echo "=== Daily Log Health Check ==="
echo ""

echo "1. System Errors (last 24h):"
loghunter errors /var/log/syslog --since 24h | wc -l

echo ""
echo "2. Auth Failures:"
loghunter search /var/log/auth.log "Failed" --since 24h | wc -l

echo ""
echo "3. Top Error Patterns:"
loghunter patterns /var/log/syslog -n 5
```

### Next Steps for Clio
1. Add to ABIOS startup for daily checks
2. Create monitoring scripts for critical services
3. Report Linux-specific issues via Synapse

---

## 🌐 NEXUS QUICK START

**Role:** Multi-Platform Agent  
**Time:** 5 minutes  
**Goal:** Learn cross-platform log analysis with LogHunter

### Step 1: Platform Detection
```python
import platform
import sys
sys.path.insert(0, "C:/Users/logan/OneDrive/Documents/AutoProjects/LogHunter")
from loghunter import LogHunter

print(f"Platform: {platform.system()}")

# LogHunter works on any platform
hunter = LogHunter()
```

### Step 2: Cross-Platform Log Paths
```python
from pathlib import Path

# Works on Windows, Linux, macOS
if platform.system() == "Windows":
    log_path = Path.home() / "AppData" / "Local" / "Temp" / "app.log"
elif platform.system() == "Darwin":  # macOS
    log_path = Path.home() / "Library" / "Logs" / "app.log"
else:  # Linux
    log_path = Path("/var/log/app.log")

hunter = LogHunter()
if log_path.exists():
    hunter.load_file(str(log_path))
```

### Step 3: Platform-Specific Analysis

**Windows:**
```python
# Windows Event Log exports
hunter.load_file("C:/Windows/Logs/export.log")
```

**Linux:**
```python
# System logs
hunter.load_file("/var/log/syslog")
```

**macOS:**
```python
# Console logs
hunter.load_file(str(Path.home() / "Library/Logs/app.log"))
```

### Step 4: Unified Analysis Script
```python
#!/usr/bin/env python3
"""Cross-platform log analysis"""

import platform
from pathlib import Path
from loghunter import LogHunter

def analyze_platform_logs():
    hunter = LogHunter()
    system = platform.system()
    
    # Find logs based on platform
    if system == "Windows":
        logs = list(Path("C:/Logs").glob("*.log"))
    elif system == "Linux":
        logs = list(Path("/var/log").glob("*.log"))
    else:  # macOS
        logs = list((Path.home() / "Library/Logs").glob("*.log"))
    
    for log in logs[:5]:
        hunter.load_file(str(log))
    
    stats = hunter.get_statistics()
    print(f"Platform: {system}")
    print(f"Files analyzed: {stats['files']}")
    print(f"Total lines: {stats['total_lines']}")
    print(f"Errors: {stats['errors']}")

if __name__ == "__main__":
    analyze_platform_logs()
```

### Next Steps for Nexus
1. Test on all 3 platforms
2. Create platform-specific log location configs
3. Report platform-specific issues via Synapse

---

## 🆓 BOLT QUICK START

**Role:** Free Executor (Cline + Grok)  
**Time:** 5 minutes  
**Goal:** Learn to use LogHunter for batch processing without API costs

### Step 1: Verify Free Access
```bash
# No API key required!
loghunter --help

# Zero cost for any operation
loghunter stats app.log
```

### Step 2: Batch Processing
```bash
# Process all logs in directory
for log in *.log; do
    echo "=== $log ==="
    loghunter errors "$log" -l 5
done

# Save results
loghunter errors "*.log" > all_errors.txt
```

### Step 3: Automated Analysis Scripts

**Script 1: Daily Error Report**
```bash
#!/bin/bash
# generate_error_report.sh

DATE=$(date +%Y-%m-%d)
REPORT="error_report_$DATE.txt"

echo "Error Report - $DATE" > $REPORT
echo "========================" >> $REPORT
echo "" >> $REPORT

for log in logs/*.log; do
    echo "=== $log ===" >> $REPORT
    loghunter errors "$log" --since 24h >> $REPORT
    echo "" >> $REPORT
done

echo "Report saved to $REPORT"
```

**Script 2: Pattern Analysis**
```bash
#!/bin/bash
# find_patterns.sh

loghunter patterns "logs/*.log" -n 20 > patterns.txt
echo "Patterns saved to patterns.txt"
```

### Step 4: Integration with Bolt Workflows
```bash
# Bulk operations - no API costs!
loghunter search "services/**/*.log" "error" > service_errors.txt
loghunter stats "services/**/*.log" > service_stats.txt

# Time-based batch processing
loghunter time "logs/*.log" --since 1h > last_hour.txt
```

### Next Steps for Bolt
1. Add to Cline workflows
2. Create batch processing scripts for repetitive tasks
3. Use for overnight analysis jobs (free!)

---

## 👤 LOGAN QUICK START

**Role:** Human User / Project Owner  
**Time:** 5 minutes  
**Goal:** Quick log analysis from command line

### Step 1: Basic Commands
```bash
# Navigate to logs
cd path/to/your/logs

# Quick error check
loghunter errors app.log

# Search for pattern
loghunter search app.log "connection failed"

# Get statistics
loghunter stats app.log
```

### Step 2: Common Scenarios

**Debugging a Production Issue:**
```bash
# 1. What happened in the last hour?
loghunter errors production.log --since 1h

# 2. Find the pattern
loghunter search production.log "timeout" -c 3

# 3. How bad is it?
loghunter stats production.log
```

**Reviewing Service Health:**
```bash
# Stats for all services
loghunter stats "services/**/*.log"

# Find common issues
loghunter patterns "services/**/*.log" -n 10
```

**Daily Health Check:**
```bash
# One-liner health check
loghunter stats app.log && loghunter errors app.log --since 24h -l 10
```

### Step 3: Integration with BCH
```
# In BCH chat (once integrated)
@loghunter errors backend.log
@loghunter stats production.log
@loghunter search logs/*.log "error"
```

### Next Steps for Logan
1. Add to daily workflow
2. Create alias for common commands
3. Request BCH integration if useful

---

## 📚 ADDITIONAL RESOURCES

**For All Agents:**
- Full Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Integration Plan: [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)
- Integration Examples: [INTEGRATION_EXAMPLES.md](INTEGRATION_EXAMPLES.md)
- Cheat Sheet: [CHEAT_SHEET.txt](CHEAT_SHEET.txt)

**Support:**
- GitHub Issues: https://github.com/DonkRonk17/LogHunter/issues
- Synapse: Post in THE_SYNAPSE/active/
- Direct: Message Atlas for complex issues

---

**Last Updated:** January 2026  
**Maintained By:** Atlas (Team Brain)
