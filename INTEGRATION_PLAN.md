# LogHunter - Integration Plan

**Goal:** 100% Utilization & Compliance  
**Target Date:** February 2026  
**Owner:** Atlas (Team Brain)  
**Version:** 1.1.0

---

## 🎯 INTEGRATION GOALS

This document outlines how LogHunter integrates with:
1. Team Brain agents (Forge, Atlas, Clio, Nexus, Bolt)
2. Existing Team Brain tools
3. BCH (Beacon Command Hub) - if applicable
4. Logan's workflows

| Goal | Target | Metric |
|------|--------|--------|
| AI Agent Adoption | 100% | 5/5 agents using |
| Daily Usage | 10+ uses/day | Usage tracking |
| Integration with Tools | 5+ tools | Integration examples working |

---

## 📦 BCH INTEGRATION

### Overview
LogHunter can be integrated into BCH for centralized log analysis commands. This enables Logan and agents to analyze logs directly from the BCH interface.

### BCH Commands

**Pattern:** `@loghunter [command] [args]`

**Examples:**
```
User: @loghunter errors backend.log
BCH: [X] Found 23 error(s)
     backend.log:156: 2026-01-10 10:02:30 ERROR Connection failed
     backend.log:234: 2026-01-10 10:05:00 ERROR NullPointerException
     ... 21 more

User: @loghunter stats production.log
BCH: [STATS] Log Statistics
     Total lines: 12,543
     Errors: 156
     Warnings: 89
```

### API Endpoints

**Endpoint 1:** `/api/tools/loghunter/errors`
```python
@router.post("/loghunter/errors")
async def loghunter_errors(file_path: str, limit: int = 50):
    """Get errors from log file"""
    import sys
    sys.path.insert(0, "C:/Users/logan/OneDrive/Documents/AutoProjects/LogHunter")
    from loghunter import LogHunter
    
    hunter = LogHunter()
    hunter.load_file(file_path)
    errors = hunter.get_errors()
    
    return {
        "count": len(errors),
        "errors": [
            {"file": e.file_path, "line": e.line_num, "content": e.line}
            for e in errors[:limit]
        ]
    }
```

**Endpoint 2:** `/api/tools/loghunter/search`
```python
@router.post("/loghunter/search")
async def loghunter_search(file_path: str, pattern: str, limit: int = 50):
    """Search logs for pattern"""
    from loghunter import LogHunter
    
    hunter = LogHunter()
    hunter.load_file(file_path)
    results = hunter.filter_by_pattern(pattern)
    
    return {
        "count": len(results),
        "results": [
            {"file": r.file_path, "line": r.line_num, "content": r.line}
            for r in results[:limit]
        ]
    }
```

**Endpoint 3:** `/api/tools/loghunter/stats`
```python
@router.post("/loghunter/stats")
async def loghunter_stats(file_path: str):
    """Get log statistics"""
    from loghunter import LogHunter
    
    hunter = LogHunter()
    hunter.load_files(file_path)
    stats = hunter.get_statistics()
    
    return {
        "total_lines": stats['total_lines'],
        "files": stats['files'],
        "errors": stats['errors'],
        "warnings": stats['warnings'],
        "exceptions": stats['exceptions'],
        "levels": dict(stats['levels']),
        "time_range": {
            "start": str(stats.get('time_start', 'N/A')),
            "end": str(stats.get('time_end', 'N/A')),
            "span": str(stats.get('time_span', 'N/A'))
        }
    }
```

### Implementation Steps
1. Add LogHunter to BCH imports
2. Create command handlers for @mention
3. Add API endpoints to tools router
4. Test integration with sample logs
5. Update BCH documentation

---

## 🤖 AI AGENT INTEGRATION

### Integration Matrix

| Agent | Use Case | Integration Method | Priority |
|-------|----------|-------------------|----------|
| **Forge** | Review session logs, identify patterns | Python API | HIGH |
| **Atlas** | Debug tool builds, analyze test output | CLI + Python | HIGH |
| **Clio** | Ubuntu log analysis, system debugging | CLI | HIGH |
| **Nexus** | Cross-platform log analysis | Python API | MEDIUM |
| **Bolt** | Batch log processing, automated analysis | CLI | MEDIUM |

### Agent-Specific Workflows

#### Forge (Orchestrator / Reviewer)
**Primary Use Case:** Analyze agent session logs to identify issues and patterns

**Integration Steps:**
1. Import LogHunter at session start
2. Load session logs for review
3. Use pattern analysis to find recurring issues
4. Generate reports for team

**Example Workflow:**
```python
# Forge reviewing Atlas session logs
import sys
sys.path.insert(0, "C:/Users/logan/OneDrive/Documents/AutoProjects/LogHunter")
from loghunter import LogHunter

# Load session logs
hunter = LogHunter()
hunter.load_files("D:/BEACON_HQ/MEMORY_CORE_V2/02_SESSION_LOGS/*.md")

# Find errors and patterns
errors = hunter.get_errors()
patterns = hunter.get_top_patterns(10)

print(f"Session Review Summary:")
print(f"- Total log lines: {hunter.get_statistics()['total_lines']}")
print(f"- Errors found: {len(errors)}")
print(f"\nTop Patterns:")
for i, (pattern, count) in enumerate(patterns[:5], 1):
    print(f"  {i}. ({count}x) {pattern[:60]}...")
```

#### Atlas (Executor / Builder)
**Primary Use Case:** Debug tool builds, analyze test output, troubleshoot errors

**Integration Steps:**
1. Use CLI during development
2. Integrate into test scripts
3. Analyze build logs for errors

**Example Workflow:**
```python
# Atlas debugging a failed tool build
from loghunter import LogHunter

hunter = LogHunter()
hunter.load_file("build.log")

# Quick error check
errors = hunter.get_errors()
if errors:
    print(f"Build failed with {len(errors)} error(s):")
    for error in errors[:5]:
        print(f"  Line {error.line_num}: {error.line[:80]}")
    
    # Get context around first error
    error_idx = hunter.lines.index(errors[0])
    context = hunter.context([error_idx], before=5, after=3)
    print("\nContext around first error:")
    for line in context:
        print(f"  {line.line_num}: {line.line}")
```

#### Clio (Linux / Ubuntu Agent)
**Primary Use Case:** System log analysis, service debugging, syslog analysis

**Platform Considerations:**
- Use CLI interface (SSH-friendly)
- Analyze /var/log files
- Monitor service logs

**Example:**
```bash
# Clio analyzing system logs
cd /var/log
loghunter errors syslog --since 1h
loghunter search auth.log "Failed password" -c 2
loghunter patterns nginx/access.log -n 10
```

#### Nexus (Multi-Platform Agent)
**Primary Use Case:** Cross-platform log analysis, standardized debugging across Windows/Linux/macOS

**Cross-Platform Notes:**
- Use Python API for consistency
- Path handling is automatic (uses pathlib internally)
- Works with any text-based log format

**Example:**
```python
# Nexus - cross-platform analysis
from loghunter import LogHunter
from pathlib import Path

# Works on any platform
log_path = Path.home() / "logs" / "app.log"

hunter = LogHunter()
hunter.load_file(str(log_path))

stats = hunter.get_statistics()
print(f"Platform: {platform.system()}")
print(f"Log health: {stats['errors']} errors, {stats['warnings']} warnings")
```

#### Bolt (Cline / Free Executor)
**Primary Use Case:** Batch log processing, automated analysis scripts

**Cost Considerations:**
- LogHunter is free (zero API costs)
- Perfect for repetitive log analysis tasks
- Can process thousands of files without API tokens

**Example:**
```bash
# Bolt batch processing
#!/bin/bash
for log in services/*.log; do
    echo "=== $log ==="
    loghunter errors "$log" -l 5
done > error_report.txt
```

---

## 🔗 INTEGRATION WITH OTHER TEAM BRAIN TOOLS

### With SynapseLink
**Notification Use Case:** Alert team when critical errors found

**Integration Pattern:**
```python
from loghunter import LogHunter
import sys
sys.path.insert(0, "C:/Users/logan/OneDrive/Documents/AutoProjects/SynapseLink")
from synapselink import quick_send

def check_logs_and_notify(log_path: str, threshold: int = 10):
    """Check logs and notify team if errors exceed threshold"""
    hunter = LogHunter()
    hunter.load_file(log_path)
    
    errors = hunter.get_errors()
    
    if len(errors) > threshold:
        quick_send(
            "FORGE,LOGAN",
            f"[ALERT] High Error Count: {log_path}",
            f"Found {len(errors)} errors (threshold: {threshold})\n\n"
            f"Latest errors:\n" +
            "\n".join(f"- {e.line[:60]}..." for e in errors[:5]),
            priority="HIGH"
        )
        return True
    return False
```

### With TokenTracker
**Usage Tracking Use Case:** Log analysis as tracked activity

**Integration Pattern:**
```python
from loghunter import LogHunter
import sys
sys.path.insert(0, "C:/Users/logan/OneDrive/Documents/AutoProjects/TokenTracker")
from tokentracker import TokenTracker

def analyze_with_tracking(log_path: str, agent: str):
    """Analyze logs with usage tracking"""
    tracker = TokenTracker()
    hunter = LogHunter()
    
    hunter.load_file(log_path)
    stats = hunter.get_statistics()
    
    # Log the analysis activity (no tokens used - local tool)
    tracker.log_usage(
        agent=agent,
        model="loghunter",
        input_tokens=0,
        output_tokens=0,
        task=f"Analyzed {stats['total_lines']} lines, found {stats['errors']} errors"
    )
    
    return stats
```

### With AgentHealth
**Health Monitoring Use Case:** Correlate log errors with agent health

**Integration Pattern:**
```python
from loghunter import LogHunter
import sys
sys.path.insert(0, "C:/Users/logan/OneDrive/Documents/AutoProjects/AgentHealth")
from agenthealth import AgentHealth

def health_check_with_logs(agent: str, log_path: str):
    """Combine agent health with log analysis"""
    health = AgentHealth()
    hunter = LogHunter()
    
    # Start health session
    session_id = f"log_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    health.start_session(agent, session_id=session_id)
    
    try:
        hunter.load_file(log_path)
        errors = hunter.get_errors()
        
        health.heartbeat(agent, status="analyzing")
        
        if len(errors) > 50:
            health.log_warning(agent, f"High error count: {len(errors)}")
        
        return errors
        
    except Exception as e:
        health.log_error(agent, str(e))
        raise
    finally:
        health.end_session(agent, session_id=session_id)
```

### With SessionReplay
**Debugging Use Case:** Analyze session logs for replay

**Integration Pattern:**
```python
from loghunter import LogHunter
import sys
sys.path.insert(0, "C:/Users/logan/OneDrive/Documents/AutoProjects/SessionReplay")
from sessionreplay import SessionReplay

def analyze_session_log(session_id: str):
    """Analyze a session log for debugging"""
    replay = SessionReplay()
    hunter = LogHunter()
    
    # Find session log
    session_log = replay.get_session_path(session_id)
    
    hunter.load_file(str(session_log))
    
    # Find errors in session
    errors = hunter.get_errors()
    
    # Log findings to session
    for error in errors:
        replay.log_event(session_id, "error_found", {
            "line": error.line_num,
            "content": error.line[:100]
        })
    
    return errors
```

### With TaskQueuePro
**Task Management Use Case:** Log analysis as queued task

**Integration Pattern:**
```python
from loghunter import LogHunter
import sys
sys.path.insert(0, "C:/Users/logan/OneDrive/Documents/AutoProjects/TaskQueuePro")
from taskqueuepro import TaskQueuePro

def queue_log_analysis(log_path: str, agent: str):
    """Queue log analysis as a task"""
    queue = TaskQueuePro()
    
    task_id = queue.create_task(
        title=f"Analyze logs: {log_path}",
        agent=agent,
        priority=2,
        metadata={"log_path": log_path, "tool": "LogHunter"}
    )
    
    queue.start_task(task_id)
    
    try:
        hunter = LogHunter()
        hunter.load_file(log_path)
        stats = hunter.get_statistics()
        
        queue.complete_task(task_id, result={
            "total_lines": stats['total_lines'],
            "errors": stats['errors'],
            "warnings": stats['warnings']
        })
        
    except Exception as e:
        queue.fail_task(task_id, error=str(e))
```

### With ConfigManager
**Configuration Use Case:** Centralized LogHunter settings

**Integration Pattern:**
```python
import sys
sys.path.insert(0, "C:/Users/logan/OneDrive/Documents/AutoProjects/ConfigManager")
from configmanager import ConfigManager

# Load LogHunter configuration
config = ConfigManager()
loghunter_config = config.get("loghunter", {
    "default_limit": 50,
    "context_lines": 3,
    "encoding": "utf-8",
    "monitored_paths": [
        "D:/BEACON_HQ/logs/*.log",
        "C:/Users/logan/AppData/Local/Temp/*.log"
    ]
})

# Use in LogHunter
from loghunter import LogHunter
hunter = LogHunter()

for path in loghunter_config['monitored_paths']:
    hunter.load_files(path)
```

### With ContextCompressor
**Token Optimization Use Case:** Compress log analysis results for AI sharing

**Integration Pattern:**
```python
from loghunter import LogHunter
import sys
sys.path.insert(0, "C:/Users/logan/OneDrive/Documents/AutoProjects/ContextCompressor")
from contextcompressor import ContextCompressor

def get_compressed_error_report(log_path: str):
    """Get compressed error report for AI context"""
    hunter = LogHunter()
    compressor = ContextCompressor()
    
    hunter.load_file(log_path)
    errors = hunter.get_errors()
    
    # Create full report
    report = "\n".join(str(e) for e in errors)
    
    # Compress for AI context
    compressed = compressor.compress_text(
        report,
        query="error summary",
        method="summary"
    )
    
    return compressed.compressed_text
```

---

## 🚀 ADOPTION ROADMAP

### Phase 1: Core Adoption (Week 1)
**Goal:** All agents aware and can use basic features

**Steps:**
1. [x] Tool deployed to GitHub
2. [ ] Quick-start guides sent via Synapse
3. [ ] Each agent tests basic workflow (errors, search, stats)
4. [ ] Feedback collected

**Success Criteria:**
- All 5 agents have used tool at least once
- No blocking issues reported

### Phase 2: Integration (Week 2-3)
**Goal:** Integrated into daily workflows

**Steps:**
1. [ ] Add to agent startup routines (log health check)
2. [ ] Create integration examples with existing tools
3. [ ] Update agent-specific workflows
4. [ ] Monitor usage patterns

**Success Criteria:**
- Used daily by at least 3 agents
- Integration examples tested and working

### Phase 3: Optimization (Week 4+)
**Goal:** Optimized and fully adopted

**Steps:**
1. [ ] Collect efficiency metrics (time saved)
2. [ ] Implement v1.2 improvements based on feedback
3. [ ] Create advanced workflow examples
4. [ ] Full Team Brain ecosystem integration

**Success Criteria:**
- Measurable time savings per debugging session
- Positive feedback from all agents
- v1.2 improvements identified

---

## 📊 SUCCESS METRICS

**Adoption Metrics:**
- Number of agents using tool: Track via Synapse reports
- Daily usage count: Manual reporting
- Integration with other tools: 5+ integrations documented

**Efficiency Metrics:**
- Time saved per debugging session: Target 30+ minutes
- Error discovery time: Target 5 minutes vs 30 minutes manual
- Pattern identification: Automatic vs manual review

**Quality Metrics:**
- Bug reports: Track via GitHub issues
- Feature requests: Track and prioritize
- User satisfaction: Qualitative feedback

---

## 🛠️ TECHNICAL INTEGRATION DETAILS

### Import Paths
```python
# Standard import
import sys
sys.path.insert(0, "C:/Users/logan/OneDrive/Documents/AutoProjects/LogHunter")
from loghunter import LogHunter, LogLine, parse_time_arg

# Or with pip install
from loghunter import LogHunter
```

### Configuration Integration
**Config File:** `~/.loghunterrc` (optional)

```json
{
  "default_limit": 50,
  "context_lines": 3,
  "encoding": "utf-8",
  "highlight_errors": true
}
```

### Error Handling Integration
**Exit Codes:**
- 0: Success
- 1: General error
- 2: File not found

### Logging Integration
LogHunter uses print statements for output (designed for CLI use).
For programmatic use, capture stdout or use API methods directly.

---

## 🔧 MAINTENANCE & SUPPORT

### Update Strategy
- Minor updates (v1.x): As needed for bug fixes
- Major updates (v2.0+): Quarterly review
- Security patches: Immediate

### Support Channels
- GitHub Issues: Bug reports and feature requests
- Synapse: Team Brain discussions
- Direct: Atlas for complex issues

### Known Limitations
- Log format detection works best with ISO timestamps
- Very large files (>1GB) may be slow - use time filtering
- Custom log formats may need manual regex patterns

### Planned Improvements (v1.2)
- [ ] Configuration file support
- [ ] Custom timestamp format definitions
- [ ] Output format options (JSON, CSV)
- [ ] Watch mode for real-time monitoring

---

## 📚 ADDITIONAL RESOURCES

- Main Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Quick Start Guides: [QUICK_START_GUIDES.md](QUICK_START_GUIDES.md)
- Integration Examples: [INTEGRATION_EXAMPLES.md](INTEGRATION_EXAMPLES.md)
- Cheat Sheet: [CHEAT_SHEET.txt](CHEAT_SHEET.txt)
- GitHub: https://github.com/DonkRonk17/LogHunter

---

**Last Updated:** January 2026  
**Maintained By:** Atlas (Team Brain)  
**For:** Logan Smith / Metaphy LLC
