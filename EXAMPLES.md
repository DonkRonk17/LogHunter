# LogHunter - Usage Examples

Comprehensive examples demonstrating all LogHunter features with real-world scenarios.

**Quick Navigation:**
- [Example 1: Basic Error Search](#example-1-basic-error-search)
- [Example 2: Pattern Search with Context](#example-2-pattern-search-with-context)
- [Example 3: Time-Based Filtering](#example-3-time-based-filtering)
- [Example 4: Multi-File Analysis](#example-4-multi-file-analysis)
- [Example 5: Log Statistics](#example-5-log-statistics)
- [Example 6: Finding Exceptions](#example-6-finding-exceptions)
- [Example 7: Log Level Filtering](#example-7-log-level-filtering)
- [Example 8: Pattern Analysis](#example-8-pattern-analysis)
- [Example 9: Integration with Shell Tools](#example-9-integration-with-shell-tools)
- [Example 10: Production Debugging Workflow](#example-10-production-debugging-workflow)

---

## Example 1: Basic Error Search

**Scenario:** You need to quickly find all errors in an application log.

**Steps:**
```bash
# Show all ERROR, FATAL, and CRITICAL level entries
loghunter errors app.log
```

**Expected Output:**
```
[LOAD] Loading 1 file(s)...
[OK] Loaded 1,542 lines from 1 file(s)

[X] Found 23 error(s)

app.log:156: 2026-01-10 10:02:30 ERROR Connection to database failed
app.log:157: 2026-01-10 10:02:31 ERROR Retry attempt 1 failed
app.log:234: 2026-01-10 10:05:00 ERROR NullPointerException in handler
app.log:456: 2026-01-10 10:15:01 ERROR Emergency shutdown initiated
... 19 more results (use --limit to see more)
```

**What You Learned:**
- `errors` command finds ERROR, FATAL, and CRITICAL levels
- Results show filename:line_number: content
- Use `-l` flag to limit results

---

## Example 2: Pattern Search with Context

**Scenario:** Find "timeout" errors and see what happened before/after.

**Steps:**
```bash
# Search for timeout patterns with 3 lines of context
loghunter search app.log "timeout" -c 3

# Case-insensitive search
loghunter search app.log "timeout" -i -c 3
```

**Expected Output:**
```
[LOAD] Loading 1 file(s)...
[OK] Loaded 1,542 lines from 1 file(s)

[SEARCH] Found 5 result(s)

app.log:152: 2026-01-10 10:02:27 INFO Attempting database connection
app.log:153: 2026-01-10 10:02:28 DEBUG Connection parameters loaded
app.log:154: 2026-01-10 10:02:29 WARN Connection taking longer than expected
app.log:155: 2026-01-10 10:02:30 ERROR Connection timeout after 30s
app.log:156: 2026-01-10 10:02:31 INFO Initiating retry logic
app.log:157: 2026-01-10 10:02:32 DEBUG Retry attempt 1
app.log:158: 2026-01-10 10:02:33 INFO Connection established
```

**What You Learned:**
- `-c 3` shows 3 lines before and after each match
- `-i` makes search case-insensitive
- Context helps understand the flow around errors

---

## Example 3: Time-Based Filtering

**Scenario:** Find all logs from the last hour for debugging a recent issue.

**Steps:**
```bash
# Logs from last hour
loghunter time app.log --since 1h

# Logs from last 30 minutes
loghunter time app.log --since 30m

# Specific time range (ISO format)
loghunter time app.log --since 2026-01-10T10:00:00 --until 2026-01-10T12:00:00

# Last 2 days with result limit
loghunter time app.log --since 2d -l 100
```

**Expected Output:**
```
[LOAD] Loading 1 file(s)...
[OK] Loaded 1,542 lines from 1 file(s)

[TIME] Found 234 line(s) in time range

app.log:1423: 2026-01-10 14:30:00 INFO Request received from 192.168.1.100
app.log:1424: 2026-01-10 14:30:01 DEBUG Processing request ID: abc123
app.log:1425: 2026-01-10 14:30:02 INFO Request completed in 45ms
...
```

**What You Learned:**
- Relative time: `1h` (hour), `30m` (minutes), `2d` (days), `5s` (seconds)
- Absolute time uses ISO format: `YYYY-MM-DDTHH:MM:SS`
- Combine `--since` and `--until` for specific ranges

---

## Example 4: Multi-File Analysis

**Scenario:** Analyze logs across multiple services or log rotations.

**Steps:**
```bash
# All .log files in current directory
loghunter errors "*.log"

# Recursive search in logs directory
loghunter errors "logs/**/*.log"

# Specific date pattern
loghunter search "app-2026-01-*.log" "error"

# All service logs
loghunter stats "services/**/*.log"
```

**Expected Output:**
```
[LOAD] Loading 5 file(s)...
[OK] Loaded 8,234 lines from 5 file(s)

[X] Found 156 error(s)

app.log:156: 2026-01-10 10:02:30 ERROR Connection to database failed
service-a.log:89: 2026-01-10 10:03:15 ERROR Request timeout
service-b.log:234: 2026-01-10 10:05:00 ERROR Memory limit exceeded
...
```

**What You Learned:**
- Use glob patterns to match multiple files
- `**` means recursive directory search
- Results show which file each line came from

---

## Example 5: Log Statistics

**Scenario:** Get an overview of log content before diving into details.

**Steps:**
```bash
# Statistics for a single file
loghunter stats app.log

# Statistics across multiple files
loghunter stats "logs/*.log"
```

**Expected Output:**
```
[LOAD] Loading 3 file(s)...
[OK] Loaded 12,543 lines from 3 file(s)

[STATS] Log Statistics

Total lines:  12,543
Files:        3

Log Levels:
  INFO       8,234
  ERROR      2,156
  WARN       1,843
  DEBUG        310

[!] Warnings:   1,843
[X] Errors:     2,156
[!!] Exceptions: 45

[TIME] Time Range:
  Start: 2026-01-10 08:00:00
  End:   2026-01-10 17:45:23
  Span:  9:45:23
```

**What You Learned:**
- `stats` gives a quick health check of log files
- See distribution of log levels
- Understand time span covered by logs

---

## Example 6: Finding Exceptions

**Scenario:** Find all exception messages and stack traces.

**Steps:**
```bash
# Find all exceptions
loghunter exceptions app.log

# Short alias
loghunter exc app.log

# With limit
loghunter exc app.log -l 20
```

**Expected Output:**
```
[LOAD] Loading 1 file(s)...
[OK] Loaded 1,542 lines from 1 file(s)

[EXC] Found 12 exception(s)

app.log:234: 2026-01-10 10:05:00 ERROR NullPointerException in handler
app.log:235: 2026-01-10 10:05:01 ERROR     at com.example.Handler.process()
app.log:236: 2026-01-10 10:05:02 ERROR     at com.example.Main.run()
app.log:567: 2026-01-10 10:12:00 ERROR IndexOutOfBoundsException: Index 5 out of bounds
...
```

**What You Learned:**
- `exceptions` finds Exception, Error, and Traceback patterns
- Also catches stack trace lines (starting with "at" or "File")
- Use `-l` to limit output

---

## Example 7: Log Level Filtering

**Scenario:** Focus on specific log levels for targeted debugging.

**Steps:**
```bash
# ERROR level only
loghunter level app.log ERROR

# Multiple levels
loghunter level app.log ERROR WARN

# Debug and Info for flow tracing
loghunter level app.log DEBUG INFO -l 50
```

**Expected Output:**
```
[LOAD] Loading 1 file(s)...
[OK] Loaded 1,542 lines from 1 file(s)

[LEVEL] Found 89 line(s) with level(s): ERROR, WARN

app.log:154: 2026-01-10 10:02:29 WARN Connection taking longer than expected
app.log:156: 2026-01-10 10:02:30 ERROR Connection to database failed
app.log:157: 2026-01-10 10:02:31 ERROR Retry attempt 1 failed
...
```

**What You Learned:**
- Filter by one or more log levels
- Supported levels: TRACE, DEBUG, INFO, WARN, WARNING, ERROR, FATAL, CRITICAL
- Level detection is case-insensitive

---

## Example 8: Pattern Analysis

**Scenario:** Find recurring patterns to identify systematic issues.

**Steps:**
```bash
# Top 10 common patterns (default)
loghunter patterns app.log

# Top 20 patterns
loghunter patterns app.log -n 20
```

**Expected Output:**
```
[LOAD] Loading 1 file(s)...
[OK] Loaded 1,542 lines from 1 file(s)

[PATTERNS] Top 10 Common Patterns

1. (234x) [TIMESTAMP] INFO Request from [IP] processed in [NUM]ms
2. (156x) [TIMESTAMP] DEBUG Loading configuration from [NUM]
3. (89x) [TIMESTAMP] WARN High memory usage: [NUM]%
4. (45x) [TIMESTAMP] ERROR Connection timeout after [NUM]s
5. (34x) [TIMESTAMP] INFO User [NUM] logged in
...
```

**What You Learned:**
- Patterns are normalized (timestamps, IPs, numbers replaced)
- Find recurring issues across thousands of lines
- Count shows frequency of each pattern

---

## Example 9: Integration with Shell Tools

**Scenario:** Combine LogHunter with other Unix tools for advanced analysis.

**Steps:**
```bash
# Count total errors
loghunter errors app.log 2>/dev/null | wc -l

# Save errors to file
loghunter errors app.log > errors.txt

# Further filter with grep
loghunter search app.log "user" | grep "user_123"

# Sort unique error messages
loghunter errors app.log | cut -d: -f3- | sort | uniq -c | sort -rn

# Watch for new errors (Linux)
watch -n 5 'loghunter errors app.log --since 5m'
```

**Expected Output:**
```
# Count output
156

# Grep filter output
app.log:234: 2026-01-10 10:05:00 INFO User user_123 logged in
app.log:567: 2026-01-10 10:15:00 ERROR User user_123 session expired
```

**What You Learned:**
- LogHunter output is pipe-friendly
- Combine with grep, sort, uniq, wc for advanced analysis
- Use `watch` for real-time monitoring

---

## Example 10: Production Debugging Workflow

**Scenario:** Complete workflow for debugging a production incident.

**Steps:**
```bash
# Step 1: Get overview
loghunter stats production.log

# Step 2: Check recent errors
loghunter errors production.log --since 1h

# Step 3: Find the spike
loghunter time production.log --since 2h --until 1h | grep ERROR | wc -l

# Step 4: Search for specific error pattern
loghunter search production.log "NullPointerException" -c 5

# Step 5: Trace the issue across services
loghunter search "services/**/*.log" "request_id=abc123"

# Step 6: Find common patterns during incident
loghunter time production.log --since 2h -l 1000 | loghunter patterns -n 5
```

**Expected Output:**
```
# Step 1: Stats show 89 errors in last hour (normally ~5)
# Step 2: All recent errors point to database module
# Step 3: Error spike started 1.5 hours ago
# Step 4: NullPointerException with stack trace identified
# Step 5: Request traced through all services
# Step 6: Pattern shows repeated "Connection pool exhausted"
```

**What You Learned:**
- Start broad (stats) then narrow down
- Use time filtering to identify when issues started
- Context (`-c`) reveals the flow around errors
- Patterns help identify systematic issues

---

## Python API Examples

### Example A: Programmatic Log Analysis

```python
from loghunter import LogHunter

# Create instance and load files
hunter = LogHunter()
hunter.load_files("logs/*.log")

# Get all errors
errors = hunter.get_errors()
print(f"Found {len(errors)} errors")

# Filter by pattern
timeouts = hunter.filter_by_pattern("timeout")
for line in timeouts[:5]:
    print(f"{line.file_path}:{line.line_num}: {line.line}")

# Get statistics
stats = hunter.get_statistics()
print(f"Total lines: {stats['total_lines']}")
print(f"Errors: {stats['errors']}")
print(f"Warnings: {stats['warnings']}")
```

### Example B: Time-Based Analysis

```python
from loghunter import LogHunter
from datetime import datetime, timedelta

hunter = LogHunter()
hunter.load_file("app.log")

# Last hour
one_hour_ago = datetime.now() - timedelta(hours=1)
recent = hunter.filter_by_time_range(start=one_hour_ago)
print(f"Logs in last hour: {len(recent)}")

# Specific time range
start = datetime(2026, 1, 10, 10, 0, 0)
end = datetime(2026, 1, 10, 12, 0, 0)
window = hunter.filter_by_time_range(start=start, end=end)
print(f"Logs in time window: {len(window)}")
```

### Example C: Custom Analysis Script

```python
#!/usr/bin/env python3
"""Daily log health check script"""

from loghunter import LogHunter
from datetime import datetime, timedelta

def daily_report(log_path):
    hunter = LogHunter()
    hunter.load_files(log_path)
    
    stats = hunter.get_statistics()
    
    print("=" * 50)
    print(f"Log Health Report - {datetime.now().date()}")
    print("=" * 50)
    print(f"Total Lines: {stats['total_lines']:,}")
    print(f"Files: {stats['files']}")
    print(f"Errors: {stats['errors']}")
    print(f"Warnings: {stats['warnings']}")
    print(f"Exceptions: {stats['exceptions']}")
    
    if stats['errors'] > 100:
        print("\n[!] HIGH ERROR COUNT - Investigation recommended!")
        
    # Top error patterns
    patterns = hunter.get_top_patterns(5)
    print("\nTop Patterns:")
    for i, (pattern, count) in enumerate(patterns, 1):
        print(f"  {i}. ({count}x) {pattern[:60]}...")

if __name__ == "__main__":
    daily_report("logs/**/*.log")
```

---

## Tips and Tricks

1. **Quick health check**: `loghunter stats app.log`
2. **Recent errors only**: `loghunter errors app.log --since 1h`
3. **Context is key**: Always use `-c 3` to see what happened around errors
4. **Patterns reveal trends**: `loghunter patterns app.log` finds systematic issues
5. **Multi-file for microservices**: `loghunter search "services/**/*.log" "trace_id"`

---

**Last Updated:** January 2026  
**Maintained By:** Atlas (Team Brain)
