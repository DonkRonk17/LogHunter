![LogHunter Title Card](branding/LogHunter%20Title.png)

# 🔍 LogHunter

**Smart Log Analysis & Pattern Finder**

A powerful command-line tool for parsing, analyzing, and extracting insights from log files. Find errors, analyze patterns, filter by time ranges, and more. Zero dependencies, cross-platform, and blazing fast.

---

## ✨ Features

- 🔍 **Smart Search** - Regex pattern matching with highlighting
- ❌ **Error Detection** - Automatically find ERROR, FATAL, CRITICAL logs
- ⚠️ **Warning Tracking** - Filter and analyze warning messages
- 📊 **Statistics** - Comprehensive log analysis and summaries
- ⏰ **Time Filtering** - Filter by timestamp ranges (absolute or relative)
- 🎯 **Log Level Filtering** - Filter by DEBUG, INFO, WARN, ERROR, etc.
- 💥 **Exception Finder** - Detect exceptions and stack traces
- 📈 **Pattern Analysis** - Find most common log patterns
- 📂 **Multi-File Support** - Analyze multiple files with glob patterns
- 🌈 **Context Display** - Show surrounding lines for better understanding
- 🎯 **Zero Dependencies** - Pure Python, works everywhere

---

## 📦 Installation

### Option 1: Quick Install

```bash
# Clone the repository
git clone https://github.com/DonkRonk17/LogHunter.git
cd LogHunter

# Make executable (Linux/Mac)
chmod +x loghunter.py
ln -s $(pwd)/loghunter.py /usr/local/bin/loghunter

# Windows: Add to PATH or use python loghunter.py
```

### Option 2: Package Install

```bash
pip install -e .
```

**Requirements:** Python 3.6+

---

## 🚀 Quick Start

```bash
# Search for errors in a log file
loghunter errors app.log

# Search for a pattern
loghunter search app.log "connection timeout"

# Show statistics
loghunter stats app.log

# Filter by log level
loghunter level app.log ERROR WARN

# Show last 50 lines
loghunter tail app.log -n 50

# Find logs from last hour
loghunter time app.log --since 1h
```

---

## 📖 Command Reference

### 🔍 search - Search with Regex

Search log files for patterns using regular expressions.

```bash
# Basic search
loghunter search app.log "error"

# Case-insensitive search
loghunter search app.log "error" -i

# Regex search
loghunter search app.log "connection.*timeout"

# Search across multiple files
loghunter search "logs/*.log" "exception"

# Show context (3 lines before/after)
loghunter search app.log "error" -c 3

# Limit results
loghunter search app.log "error" -l 10
```

**Options:**
- `-i, --ignore-case` - Case insensitive search
- `-c, --context N` - Show N lines of context around matches
- `-l, --limit N` - Limit output to N results

---

### ❌ errors - Show All Errors

Display all ERROR, FATAL, and CRITICAL level log entries.

```bash
# Show all errors
loghunter errors app.log

# Limit to first 20 errors
loghunter errors app.log -l 20

# Errors from multiple files
loghunter errors "logs/**/*.log"
```

---

### ⚠️ warnings - Show All Warnings

Display all WARN and WARNING level log entries.

```bash
# Show all warnings
loghunter warnings app.log
loghunter warn app.log  # Short alias

# Limit results
loghunter warnings app.log -l 50
```

---

### 📋 level - Filter by Log Level

Filter logs by one or more log levels.

```bash
# Show ERROR logs only
loghunter level app.log ERROR

# Show ERROR and WARN logs
loghunter level app.log ERROR WARN

# Show DEBUG and INFO
loghunter level app.log DEBUG INFO

# Limit results
loghunter level app.log ERROR -l 100
```

**Supported Levels:** TRACE, DEBUG, INFO, WARN, WARNING, ERROR, FATAL, CRITICAL

---

### 📊 stats - Show Statistics

Display comprehensive statistics about log files.

```bash
# Show statistics
loghunter stats app.log

# Stats for multiple files
loghunter stats "logs/*.log"
```

**Output includes:**
- Total lines and files
- Log level distribution
- Error, warning, and exception counts
- Time range covered

**Example output:**
```
📊 Log Statistics

Total lines:  12,543
Files:        3

Log Levels:
  INFO       8,234
  ERROR      2,156
  WARN       1,843
  DEBUG        310

⚠️  Warnings:   1,843
❌ Errors:     2,156
💥 Exceptions: 45

📅 Time Range:
  Start: 2026-01-10 08:00:00
  End:   2026-01-10 17:45:23
  Span:  9:45:23
```

---

### 📄 tail / head - Show First/Last Lines

Display the beginning or end of log files.

```bash
# Last 10 lines (default)
loghunter tail app.log

# Last 100 lines
loghunter tail app.log -n 100

# First 20 lines
loghunter head app.log -n 20
```

---

### ⏰ time - Filter by Time Range

Filter logs by timestamp (absolute or relative).

```bash
# Last hour
loghunter time app.log --since 1h

# Last 30 minutes
loghunter time app.log --since 30m

# Last 2 days
loghunter time app.log --since 2d

# Specific time range (ISO format)
loghunter time app.log --since 2026-01-10T08:00:00 --until 2026-01-10T12:00:00

# Limit results
loghunter time app.log --since 1h -l 50
```

**Time Formats:**
- **Relative:** `1s` (second), `5m` (minutes), `2h` (hours), `7d` (days)
- **Absolute:** ISO format like `2026-01-10T14:30:00`

---

### 🔍 patterns - Find Common Patterns

Analyze and display the most frequently occurring log patterns.

```bash
# Top 10 patterns (default)
loghunter patterns app.log

# Top 20 patterns
loghunter patterns app.log -n 20
```

This normalizes log lines (removes timestamps, IPs, numbers) to identify recurring patterns.

---

### 💥 exceptions - Find Exceptions

Display all lines containing exceptions or stack traces.

```bash
# Show all exceptions
loghunter exceptions app.log
loghunter exc app.log  # Short alias

# Limit results
loghunter exceptions app.log -l 10
```

---

## 🎯 Real-World Examples

### Example 1: Debugging Production Error

```bash
# 1. Check how many errors in last hour
loghunter errors production.log --since 1h | wc -l

# 2. Find specific error pattern
loghunter search production.log "NullPointerException" -c 5

# 3. Get statistics
loghunter stats production.log
```

### Example 2: Monitoring Application

```bash
# Find all connection timeouts today
loghunter search app.log "connection.*timeout" --since 24h

# Check warning trends
loghunter warnings app.log -l 100

# Analyze common issues
loghunter patterns app.log -n 20
```

### Example 3: Analyzing Multiple Services

```bash
# Errors across all microservices
loghunter errors "services/**/*.log"

# Find specific user's activity
loghunter search "services/**/*.log" "user_id=12345"

# Time-based analysis
loghunter time "services/**/*.log" --since 2h
```

### Example 4: Finding Root Cause

```bash
# 1. Find exceptions
loghunter exceptions app.log

# 2. Get context around first exception
loghunter search app.log "Exception" -c 10 -l 1

# 3. Check what happened before errors started
loghunter time app.log --since 2h --until 1h
```

---

## 🎨 Output Format

LogHunter displays results in an easy-to-read format:

```
app.log:142: 2026-01-10 14:23:45 ERROR Connection timeout after 30s
app.log:143: 2026-01-10 14:23:46 ERROR Retrying connection...
service.log:89: 2026-01-10 14:23:47 WARN High memory usage detected
```

**Format:** `filename:line_number: log_content`

---

## 🔧 Advanced Usage

### Multi-File Glob Patterns

```bash
# All .log files in directory
loghunter search "*.log" "error"

# Recursive search
loghunter search "**/*.log" "error"

# Specific patterns
loghunter search "app-2026-01-*.log" "error"
```

### Combining with Shell Tools

```bash
# Count errors
loghunter errors app.log | wc -l

# Save errors to file
loghunter errors app.log > errors.txt

# Pipe to grep for further filtering
loghunter search app.log "user" | grep "user_123"
```

### Case-Insensitive Search

```bash
# Find "error" regardless of case
loghunter search app.log "error" -i

# Matches: error, ERROR, Error, ErRoR
```

---

## 🎓 Log Format Support

LogHunter automatically detects common log formats:

**Timestamp Formats:**
- ISO 8601: `2026-01-10T14:30:00` or `2026-01-10 14:30:00`
- Common Log: `10/Jan/2026:14:30:00`
- Simple: `14:30:00`

**Log Levels:** TRACE, DEBUG, INFO, WARN, WARNING, ERROR, FATAL, CRITICAL

**Patterns Detected:**
- IP addresses
- URLs
- Exception names
- Stack traces

---

## 💡 Tips & Tricks

1. **Fast error checking:** `loghunter errors app.log -l 10` shows first 10 errors
2. **Recent issues:** `loghunter time app.log --since 1h` for last hour
3. **Pattern discovery:** `loghunter patterns app.log` reveals recurring issues
4. **Context is key:** Use `-c 5` to see what happened around errors
5. **Multiple files:** Use globs like `logs/**/*.log` for comprehensive analysis

---

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

## 🏆 Why LogHunter?

**Simple yet powerful:**
- No bloated GUI
- Works over SSH
- Fast regex engine
- Zero dependencies

**Designed for developers:**
- CLI-first interface
- Pipe-friendly output
- Regex power
- Cross-platform

**Actually solves problems:**
- Find errors fast
- Analyze patterns
- Time-based debugging
- Multi-file support

---

## 📚 Resources

- [Regular Expressions Tutorial](https://regexone.com/)
- [Log Best Practices](https://www.loggly.com/ultimate-guide/python-logging-basics/)

---

**Built for developers who live in the terminal**

Start hunting logs: `loghunter errors app.log`
