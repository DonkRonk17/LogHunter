# LogHunter - Integration Examples

## 🎯 INTEGRATION PHILOSOPHY

LogHunter is designed to work seamlessly with other Team Brain tools. This document provides **copy-paste-ready code examples** for common integration patterns.

---

## 📚 TABLE OF CONTENTS

1. [Integration Pattern 1: LogHunter + SynapseLink](#pattern-1-loghunter--synapselink)
2. [Integration Pattern 2: LogHunter + TokenTracker](#pattern-2-loghunter--tokentracker)
3. [Integration Pattern 3: LogHunter + AgentHealth](#pattern-3-loghunter--agenthealth)
4. [Integration Pattern 4: LogHunter + SessionReplay](#pattern-4-loghunter--sessionreplay)
5. [Integration Pattern 5: LogHunter + TaskQueuePro](#pattern-5-loghunter--taskqueuepro)
6. [Integration Pattern 6: LogHunter + ConfigManager](#pattern-6-loghunter--configmanager)
7. [Integration Pattern 7: LogHunter + ContextCompressor](#pattern-7-loghunter--contextcompressor)
8. [Integration Pattern 8: LogHunter + TimeSync](#pattern-8-loghunter--timesync)
9. [Integration Pattern 9: Multi-Tool Workflow](#pattern-9-multi-tool-workflow)
10. [Integration Pattern 10: Full Team Brain Stack](#pattern-10-full-team-brain-stack)

---

## Pattern 1: LogHunter + SynapseLink

**Use Case:** Alert team when critical errors are found in logs

**Why:** Keep team informed of log issues automatically

**Code:**

```python
import sys
sys.path.insert(0, "C:/Users/logan/OneDrive/Documents/AutoProjects/LogHunter")
sys.path.insert(0, "C:/Users/logan/OneDrive/Documents/AutoProjects/SynapseLink")

from loghunter import LogHunter
from synapselink import quick_send

def check_and_notify(log_path: str, error_threshold: int = 10):
    """Check logs and notify team if errors exceed threshold"""
    
    hunter = LogHunter()
    hunter.load_file(log_path)
    
    errors = hunter.get_errors()
    stats = hunter.get_statistics()
    
    if len(errors) > error_threshold:
        # Create error summary
        error_summary = "\n".join([
            f"- {e.line[:60]}..." for e in errors[:5]
        ])
        
        quick_send(
            "FORGE,LOGAN",
            f"[ALERT] High Error Count in {log_path}",
            f"Found {len(errors)} errors (threshold: {error_threshold})\n\n"
            f"Stats:\n"
            f"- Total lines: {stats['total_lines']}\n"
            f"- Warnings: {stats['warnings']}\n"
            f"- Exceptions: {stats['exceptions']}\n\n"
            f"Latest errors:\n{error_summary}",
            priority="HIGH"
        )
        return True
    
    return False

# Example usage
if __name__ == "__main__":
    alerted = check_and_notify("production.log", error_threshold=10)
    if alerted:
        print("[!] Alert sent to team")
    else:
        print("[OK] Error count within threshold")
```

**Result:** Team receives instant notification when log errors spike

---

## Pattern 2: LogHunter + TokenTracker

**Use Case:** Track log analysis activities (zero tokens used - local tool)

**Why:** Maintain activity tracking even for free/local tools

**Code:**

```python
import sys
sys.path.insert(0, "C:/Users/logan/OneDrive/Documents/AutoProjects/LogHunter")
sys.path.insert(0, "C:/Users/logan/OneDrive/Documents/AutoProjects/TokenTracker")

from loghunter import LogHunter
from tokentracker import TokenTracker

def analyze_with_tracking(log_path: str, agent: str):
    """Analyze logs and track the activity"""
    
    tracker = TokenTracker()
    hunter = LogHunter()
    
    # Load and analyze
    hunter.load_file(log_path)
    stats = hunter.get_statistics()
    errors = hunter.get_errors()
    
    # Log the activity (0 tokens - local tool)
    tracker.log_usage(
        agent=agent,
        model="loghunter-local",
        input_tokens=0,
        output_tokens=0,
        task=f"Analyzed {stats['total_lines']} lines, found {stats['errors']} errors"
    )
    
    return {
        'stats': stats,
        'errors': errors
    }

# Example usage
result = analyze_with_tracking("app.log", "ATLAS")
print(f"Analyzed {result['stats']['total_lines']} lines")
print(f"Found {len(result['errors'])} errors")
```

**Result:** Activity tracked without consuming API budget

---

## Pattern 3: LogHunter + AgentHealth

**Use Case:** Correlate log errors with agent health monitoring

**Why:** Understand how log issues affect agent performance

**Code:**

```python
import sys
from datetime import datetime
sys.path.insert(0, "C:/Users/logan/OneDrive/Documents/AutoProjects/LogHunter")
sys.path.insert(0, "C:/Users/logan/OneDrive/Documents/AutoProjects/AgentHealth")

from loghunter import LogHunter
from agenthealth import AgentHealth

def health_monitored_analysis(agent: str, log_path: str):
    """Analyze logs with health monitoring"""
    
    health = AgentHealth()
    hunter = LogHunter()
    
    # Start health session
    session_id = f"log_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    health.start_session(agent, session_id=session_id)
    
    try:
        # Analysis
        health.heartbeat(agent, status="loading")
        hunter.load_file(log_path)
        
        health.heartbeat(agent, status="analyzing")
        errors = hunter.get_errors()
        stats = hunter.get_statistics()
        
        # Log findings
        if stats['errors'] > 50:
            health.log_warning(agent, f"High error count: {stats['errors']}")
        
        if stats['exceptions'] > 10:
            health.log_warning(agent, f"Exception count: {stats['exceptions']}")
        
        health.heartbeat(agent, status="complete")
        
        return {
            'stats': stats,
            'errors': errors,
            'session_id': session_id
        }
        
    except Exception as e:
        health.log_error(agent, str(e))
        raise
        
    finally:
        health.end_session(agent, session_id=session_id)

# Example usage
result = health_monitored_analysis("ATLAS", "app.log")
print(f"Session: {result['session_id']}")
print(f"Errors: {len(result['errors'])}")
```

**Result:** Log analysis correlated with agent health data

---

## Pattern 4: LogHunter + SessionReplay

**Use Case:** Analyze session logs for replay and debugging

**Why:** Find issues in recorded sessions for post-mortem analysis

**Code:**

```python
import sys
sys.path.insert(0, "C:/Users/logan/OneDrive/Documents/AutoProjects/LogHunter")
sys.path.insert(0, "C:/Users/logan/OneDrive/Documents/AutoProjects/SessionReplay")

from loghunter import LogHunter
from sessionreplay import SessionReplay
from pathlib import Path

def analyze_session(session_id: str):
    """Analyze a recorded session for issues"""
    
    replay = SessionReplay()
    hunter = LogHunter()
    
    # Get session log path
    session_log = Path(f"D:/BEACON_HQ/MEMORY_CORE_V2/02_SESSION_LOGS/{session_id}.md")
    
    if not session_log.exists():
        print(f"[X] Session not found: {session_id}")
        return None
    
    # Load and analyze
    hunter.load_file(str(session_log))
    
    errors = hunter.get_errors()
    patterns = hunter.get_top_patterns(5)
    stats = hunter.get_statistics()
    
    # Create analysis report
    report = {
        'session_id': session_id,
        'total_lines': stats['total_lines'],
        'errors': len(errors),
        'warnings': stats['warnings'],
        'top_patterns': patterns,
        'error_samples': [e.line[:80] for e in errors[:5]]
    }
    
    # Log analysis to session
    replay.log_event(session_id, "analysis_complete", {
        "errors_found": len(errors),
        "patterns_identified": len(patterns)
    })
    
    return report

# Example usage
report = analyze_session("SESSION_2026-01-20")
if report:
    print(f"Session: {report['session_id']}")
    print(f"Errors: {report['errors']}")
    print("Top patterns:")
    for pattern, count in report['top_patterns']:
        print(f"  ({count}x) {pattern[:50]}...")
```

**Result:** Session analysis with error identification for debugging

---

## Pattern 5: LogHunter + TaskQueuePro

**Use Case:** Queue log analysis as managed tasks

**Why:** Track and manage log analysis work across agents

**Code:**

```python
import sys
sys.path.insert(0, "C:/Users/logan/OneDrive/Documents/AutoProjects/LogHunter")
sys.path.insert(0, "C:/Users/logan/OneDrive/Documents/AutoProjects/TaskQueuePro")

from loghunter import LogHunter
from taskqueuepro import TaskQueuePro

def queue_log_analysis(log_path: str, agent: str, priority: int = 2):
    """Queue a log analysis task"""
    
    queue = TaskQueuePro()
    
    # Create task
    task_id = queue.create_task(
        title=f"Analyze logs: {log_path}",
        agent=agent,
        priority=priority,
        metadata={
            "log_path": log_path,
            "tool": "LogHunter",
            "type": "log_analysis"
        }
    )
    
    return task_id

def execute_queued_analysis(task_id: str):
    """Execute a queued log analysis task"""
    
    queue = TaskQueuePro()
    hunter = LogHunter()
    
    # Get task details
    task = queue.get_task(task_id)
    log_path = task['metadata']['log_path']
    
    # Start task
    queue.start_task(task_id)
    
    try:
        # Execute analysis
        hunter.load_file(log_path)
        stats = hunter.get_statistics()
        errors = hunter.get_errors()
        
        # Complete task with results
        queue.complete_task(task_id, result={
            "total_lines": stats['total_lines'],
            "errors": stats['errors'],
            "warnings": stats['warnings'],
            "exceptions": stats['exceptions'],
            "error_count": len(errors)
        })
        
        return stats
        
    except Exception as e:
        queue.fail_task(task_id, error=str(e))
        raise

# Example usage
task_id = queue_log_analysis("production.log", "ATLAS", priority=1)
print(f"Task queued: {task_id}")

# Later, execute
stats = execute_queued_analysis(task_id)
print(f"Analysis complete: {stats['errors']} errors found")
```

**Result:** Log analysis tracked as managed tasks

---

## Pattern 6: LogHunter + ConfigManager

**Use Case:** Centralized LogHunter configuration

**Why:** Share configuration across agents and sessions

**Code:**

```python
import sys
sys.path.insert(0, "C:/Users/logan/OneDrive/Documents/AutoProjects/LogHunter")
sys.path.insert(0, "C:/Users/logan/OneDrive/Documents/AutoProjects/ConfigManager")

from loghunter import LogHunter
from configmanager import ConfigManager

def get_configured_hunter():
    """Get LogHunter with centralized configuration"""
    
    config = ConfigManager()
    
    # Get LogHunter config with defaults
    loghunter_config = config.get("loghunter", {
        "default_limit": 50,
        "context_lines": 3,
        "encoding": "utf-8",
        "error_threshold": 10,
        "monitored_paths": [
            "D:/BEACON_HQ/logs/*.log",
            "C:/Users/logan/AppData/Local/Temp/*.log"
        ]
    })
    
    hunter = LogHunter()
    
    return hunter, loghunter_config

def monitor_configured_paths():
    """Monitor all configured log paths"""
    
    hunter, config = get_configured_hunter()
    
    total_errors = 0
    
    for path in config['monitored_paths']:
        hunter.load_files(path)
    
    stats = hunter.get_statistics()
    errors = hunter.get_errors()
    
    print(f"Monitored {stats['files']} files")
    print(f"Total lines: {stats['total_lines']}")
    print(f"Errors: {len(errors)}")
    
    if len(errors) > config['error_threshold']:
        print(f"[!] Error threshold exceeded ({config['error_threshold']})")

# Example usage
monitor_configured_paths()
```

**Result:** Consistent configuration across all LogHunter usage

---

## Pattern 7: LogHunter + ContextCompressor

**Use Case:** Compress log analysis results for AI context

**Why:** Save tokens when sharing log analysis with AI agents

**Code:**

```python
import sys
sys.path.insert(0, "C:/Users/logan/OneDrive/Documents/AutoProjects/LogHunter")
sys.path.insert(0, "C:/Users/logan/OneDrive/Documents/AutoProjects/ContextCompressor")

from loghunter import LogHunter
from contextcompressor import ContextCompressor

def get_compressed_error_report(log_path: str, max_tokens: int = 1000):
    """Get compressed error report for AI context"""
    
    hunter = LogHunter()
    compressor = ContextCompressor()
    
    # Load and analyze
    hunter.load_file(log_path)
    errors = hunter.get_errors()
    stats = hunter.get_statistics()
    
    # Create full report
    full_report = f"""Log Analysis Report: {log_path}
    
Statistics:
- Total lines: {stats['total_lines']}
- Errors: {stats['errors']}
- Warnings: {stats['warnings']}
- Exceptions: {stats['exceptions']}

Error Details:
"""
    
    for i, error in enumerate(errors[:50], 1):
        full_report += f"\n{i}. Line {error.line_num}: {error.line}"
    
    # Compress for AI context
    compressed = compressor.compress_text(
        full_report,
        query="error summary and key issues",
        method="summary"
    )
    
    print(f"Original: ~{len(full_report)//4} tokens")
    print(f"Compressed: ~{compressed.compressed_size//4} tokens")
    print(f"Savings: {compressed.estimated_token_savings} tokens")
    
    return compressed.compressed_text

# Example usage
summary = get_compressed_error_report("production.log")
print("\nCompressed Report:")
print(summary)
```

**Result:** Token-efficient log analysis summaries

---

## Pattern 8: LogHunter + TimeSync

**Use Case:** Time-aware log analysis respecting BeaconTime

**Why:** Align log analysis with Team Brain timing protocols

**Code:**

```python
import sys
from datetime import datetime, timedelta
sys.path.insert(0, "C:/Users/logan/OneDrive/Documents/AutoProjects/LogHunter")
sys.path.insert(0, "C:/Users/logan/OneDrive/Documents/AutoProjects/TimeSync")

from loghunter import LogHunter
from timesync import TimeSync

def time_aware_analysis(log_path: str):
    """Analyze logs with TimeSync awareness"""
    
    ts = TimeSync()
    hunter = LogHunter()
    
    # Get current time status
    time_info = ts.get_current_time()
    logan_status = ts.get_logan_status()
    
    print(f"Current time: {time_info}")
    print(f"Logan status: {logan_status}")
    
    # Load logs
    hunter.load_file(log_path)
    stats = hunter.get_statistics()
    
    # Analyze based on time of day
    if logan_status == "SLEEP":
        # During sleep - only check for critical errors
        critical = [e for e in hunter.get_errors() 
                   if e.level in ['FATAL', 'CRITICAL']]
        print(f"[SLEEP MODE] Critical errors only: {len(critical)}")
        return critical
    
    elif logan_status == "ACTIVE":
        # During active hours - full analysis
        errors = hunter.get_errors()
        print(f"[ACTIVE MODE] Full analysis: {len(errors)} errors")
        return errors
    
    else:
        # Wind down - summary only
        print(f"[WIND DOWN] Summary: {stats['errors']} total errors")
        return None

# Example usage
errors = time_aware_analysis("app.log")
if errors:
    for e in errors[:3]:
        print(f"  - {e.line[:60]}...")
```

**Result:** Log analysis adapted to Logan's schedule

---

## Pattern 9: Multi-Tool Workflow

**Use Case:** Complete log analysis workflow using multiple tools

**Why:** Demonstrate real production scenario

**Code:**

```python
import sys
from datetime import datetime

# Add all tool paths
TOOL_PATHS = [
    "C:/Users/logan/OneDrive/Documents/AutoProjects/LogHunter",
    "C:/Users/logan/OneDrive/Documents/AutoProjects/SynapseLink",
    "C:/Users/logan/OneDrive/Documents/AutoProjects/TokenTracker",
    "C:/Users/logan/OneDrive/Documents/AutoProjects/AgentHealth",
]
for path in TOOL_PATHS:
    sys.path.insert(0, path)

from loghunter import LogHunter
from synapselink import quick_send
from tokentracker import TokenTracker
from agenthealth import AgentHealth

def complete_log_analysis(log_path: str, agent: str = "ATLAS"):
    """Full log analysis workflow with all integrations"""
    
    # Initialize tools
    hunter = LogHunter()
    tracker = TokenTracker()
    health = AgentHealth()
    
    # Start health session
    session_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    health.start_session(agent, session_id=session_id)
    
    try:
        # Load logs
        health.heartbeat(agent, status="loading")
        hunter.load_file(log_path)
        
        # Analyze
        health.heartbeat(agent, status="analyzing")
        stats = hunter.get_statistics()
        errors = hunter.get_errors()
        patterns = hunter.get_top_patterns(5)
        
        # Log activity (no tokens used)
        tracker.log_usage(
            agent=agent,
            model="loghunter",
            input_tokens=0,
            output_tokens=0,
            task=f"Analyzed {stats['total_lines']} lines from {log_path}"
        )
        
        # Notify if issues found
        if stats['errors'] > 20:
            quick_send(
                "FORGE",
                f"[Log Analysis] Issues in {log_path}",
                f"Found {stats['errors']} errors\n"
                f"Exceptions: {stats['exceptions']}\n\n"
                f"Top patterns:\n" +
                "\n".join(f"- ({c}x) {p[:40]}..." for p, c in patterns[:3]),
                priority="NORMAL"
            )
        
        # Complete
        health.heartbeat(agent, status="complete")
        health.end_session(agent, session_id=session_id)
        
        return {
            'session_id': session_id,
            'stats': stats,
            'errors': len(errors),
            'patterns': patterns
        }
        
    except Exception as e:
        health.log_error(agent, str(e))
        health.end_session(agent, session_id=session_id, status="failed")
        raise

# Example usage
result = complete_log_analysis("production.log")
print(f"Session: {result['session_id']}")
print(f"Stats: {result['stats']['total_lines']} lines, {result['errors']} errors")
```

**Result:** Fully instrumented log analysis workflow

---

## Pattern 10: Full Team Brain Stack

**Use Case:** Ultimate integration - all tools working together

**Why:** Production-grade log monitoring and analysis

**Code:**

```python
#!/usr/bin/env python3
"""
Full Team Brain Log Monitoring System
Integrates: LogHunter, SynapseLink, TokenTracker, AgentHealth, ConfigManager
"""

import sys
from datetime import datetime
from pathlib import Path

# Tool paths
TOOLS = [
    "LogHunter", "SynapseLink", "TokenTracker", 
    "AgentHealth", "ConfigManager", "TimeSync"
]
for tool in TOOLS:
    sys.path.insert(0, f"C:/Users/logan/OneDrive/Documents/AutoProjects/{tool}")

from loghunter import LogHunter
from synapselink import quick_send
from tokentracker import TokenTracker
from agenthealth import AgentHealth
from configmanager import ConfigManager
from timesync import TimeSync

class LogMonitor:
    """Full Team Brain log monitoring system"""
    
    def __init__(self, agent: str = "ATLAS"):
        self.agent = agent
        self.config = ConfigManager()
        self.hunter = LogHunter()
        self.tracker = TokenTracker()
        self.health = AgentHealth()
        self.timesync = TimeSync()
        
        # Load configuration
        self.settings = self.config.get("log_monitor", {
            "error_threshold": 10,
            "check_interval_minutes": 15,
            "monitored_paths": ["D:/BEACON_HQ/logs/*.log"],
            "notify_agents": ["FORGE", "LOGAN"]
        })
    
    def run_check(self):
        """Run a log health check"""
        
        session_id = f"monitor_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.health.start_session(self.agent, session_id=session_id)
        
        try:
            # Check Logan's status
            logan_status = self.timesync.get_logan_status()
            
            # Load all monitored logs
            for path in self.settings['monitored_paths']:
                self.hunter.load_files(path)
            
            stats = self.hunter.get_statistics()
            errors = self.hunter.get_errors()
            
            # Log activity
            self.tracker.log_usage(
                agent=self.agent,
                model="log_monitor",
                input_tokens=0,
                output_tokens=0,
                task=f"Monitor check: {stats['files']} files, {stats['errors']} errors"
            )
            
            # Alert if needed (respect sleep hours)
            if len(errors) > self.settings['error_threshold']:
                if logan_status != "SLEEP":
                    self._send_alert(stats, errors)
            
            self.health.end_session(self.agent, session_id=session_id)
            
            return {
                'session': session_id,
                'files': stats['files'],
                'lines': stats['total_lines'],
                'errors': len(errors),
                'alerted': len(errors) > self.settings['error_threshold']
            }
            
        except Exception as e:
            self.health.log_error(self.agent, str(e))
            self.health.end_session(self.agent, session_id=session_id, status="failed")
            raise
    
    def _send_alert(self, stats, errors):
        """Send alert to team"""
        
        quick_send(
            ",".join(self.settings['notify_agents']),
            f"[Log Monitor] {stats['errors']} Errors Detected",
            f"Log Monitor Alert\n"
            f"================\n"
            f"Files checked: {stats['files']}\n"
            f"Total lines: {stats['total_lines']}\n"
            f"Errors: {stats['errors']}\n"
            f"Warnings: {stats['warnings']}\n\n"
            f"Sample errors:\n" +
            "\n".join(f"- {e.line[:50]}..." for e in errors[:5]),
            priority="HIGH"
        )

# Example usage
if __name__ == "__main__":
    monitor = LogMonitor("ATLAS")
    result = monitor.run_check()
    
    print(f"Monitor Check Complete")
    print(f"  Session: {result['session']}")
    print(f"  Files: {result['files']}")
    print(f"  Lines: {result['lines']}")
    print(f"  Errors: {result['errors']}")
    print(f"  Alerted: {result['alerted']}")
```

**Result:** Complete log monitoring system for Team Brain

---

## 📊 RECOMMENDED INTEGRATION PRIORITY

**Week 1 (Essential):**
1. ✅ SynapseLink - Team notifications
2. ✅ AgentHealth - Health correlation
3. ✅ TokenTracker - Activity tracking

**Week 2 (Productivity):**
4. ☐ TaskQueuePro - Task management
5. ☐ ConfigManager - Configuration
6. ☐ SessionReplay - Debugging

**Week 3 (Advanced):**
7. ☐ ContextCompressor - Token optimization
8. ☐ TimeSync - Schedule awareness
9. ☐ Full stack integration

---

## 🔧 TROUBLESHOOTING INTEGRATIONS

**Import Errors:**
```python
# Ensure all tools are in Python path
import sys
from pathlib import Path

AUTOPROJECTS = Path("C:/Users/logan/OneDrive/Documents/AutoProjects")
for tool in AUTOPROJECTS.iterdir():
    if tool.is_dir() and not tool.name.startswith('.'):
        sys.path.insert(0, str(tool))

# Then import
from loghunter import LogHunter
```

**Version Conflicts:**
```bash
# Check versions
cd LogHunter
git log -1 --format="%H %s"

# Update if needed
git pull origin master
```

**Configuration Issues:**
```python
# Reset to defaults
from configmanager import ConfigManager
config = ConfigManager()
config.delete("loghunter")  # Remove custom config
```

---

**Last Updated:** January 2026  
**Maintained By:** Atlas (Team Brain)
