#!/usr/bin/env python3
"""
LogHunter - Smart Log Analysis & Pattern Finder
Parse, analyze, and extract insights from log files. Zero dependencies!
"""

import os
import sys
import io
import re
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter, defaultdict
from typing import List, Dict, Optional, Pattern
import glob

# Fix Unicode output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# --- Common log patterns ---
LOG_LEVELS = ['TRACE', 'DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR', 'FATAL', 'CRITICAL']

# Common log formats
PATTERNS = {
    'timestamp_iso': re.compile(r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}'),
    'timestamp_common': re.compile(r'\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}'),
    'timestamp_simple': re.compile(r'\d{2}:\d{2}:\d{2}'),
    'log_level': re.compile(r'\b(' + '|'.join(LOG_LEVELS) + r')\b', re.IGNORECASE),
    'ip_address': re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'),
    'url': re.compile(r'https?://[^\s]+'),
    'exception': re.compile(r'\b(Exception|Error|Traceback)\b'),
    'stack_trace': re.compile(r'^\s+at\s+|^\s+File\s+"'),
}


class LogLine:
    """Represents a single log line with metadata"""
    
    def __init__(self, line: str, line_num: int, file_path: str):
        self.line = line.rstrip('\n\r')
        self.line_num = line_num
        self.file_path = file_path
        self.timestamp = self._extract_timestamp()
        self.level = self._extract_level()
    
    def _extract_timestamp(self) -> Optional[datetime]:
        """Extract timestamp from line"""
        # Try ISO format
        match = PATTERNS['timestamp_iso'].search(self.line)
        if match:
            ts_str = match.group().replace(' ', 'T')
            try:
                return datetime.fromisoformat(ts_str)
            except:
                pass
        return None
    
    def _extract_level(self) -> Optional[str]:
        """Extract log level from line"""
        match = PATTERNS['log_level'].search(self.line)
        if match:
            return match.group().upper()
        return None
    
    def matches_pattern(self, pattern: Pattern) -> bool:
        """Check if line matches a regex pattern"""
        return pattern.search(self.line) is not None
    
    def matches_level(self, levels: List[str]) -> bool:
        """Check if line matches any of the given log levels"""
        if not self.level:
            return False
        return self.level in [l.upper() for l in levels]
    
    def __str__(self) -> str:
        """Format for display"""
        filename = Path(self.file_path).name
        return f"{filename}:{self.line_num}: {self.line}"


class LogHunter:
    """Smart log file analyzer"""
    
    def __init__(self):
        self.lines: List[LogLine] = []
    
    def load_file(self, file_path: str, encoding: str = 'utf-8'):
        """Load a single log file"""
        try:
            with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                for line_num, line in enumerate(f, 1):
                    self.lines.append(LogLine(line, line_num, file_path))
        except Exception as e:
            print(f"⚠️  Warning: Could not read {file_path}: {e}", file=sys.stderr)
    
    def load_files(self, pattern: str, encoding: str = 'utf-8'):
        """Load multiple files matching a glob pattern"""
        files = glob.glob(pattern, recursive=True)
        if not files:
            print(f"❌ No files found matching: {pattern}")
            return
        
        print(f"📂 Loading {len(files)} file(s)...")
        for file_path in sorted(files):
            self.load_file(file_path, encoding)
        
        print(f"✅ Loaded {len(self.lines):,} lines from {len(files)} file(s)\n")
    
    def filter_by_level(self, levels: List[str]) -> List[LogLine]:
        """Filter lines by log level"""
        return [line for line in self.lines if line.matches_level(levels)]
    
    def filter_by_pattern(self, pattern: str, case_sensitive: bool = False) -> List[LogLine]:
        """Filter lines by regex pattern"""
        flags = 0 if case_sensitive else re.IGNORECASE
        regex = re.compile(pattern, flags)
        return [line for line in self.lines if line.matches_pattern(regex)]
    
    def filter_by_time_range(self, start: datetime = None, end: datetime = None) -> List[LogLine]:
        """Filter lines by timestamp range"""
        result = []
        for line in self.lines:
            if line.timestamp:
                if start and line.timestamp < start:
                    continue
                if end and line.timestamp > end:
                    continue
                result.append(line)
        return result
    
    def get_errors(self) -> List[LogLine]:
        """Get all error-level lines"""
        return self.filter_by_level(['ERROR', 'FATAL', 'CRITICAL'])
    
    def get_warnings(self) -> List[LogLine]:
        """Get all warning-level lines"""
        return self.filter_by_level(['WARN', 'WARNING'])
    
    def get_exceptions(self) -> List[LogLine]:
        """Get lines containing exceptions or stack traces"""
        return [line for line in self.lines if line.matches_pattern(PATTERNS['exception'])]
    
    def get_statistics(self) -> Dict:
        """Generate statistics about loaded logs"""
        stats = {
            'total_lines': len(self.lines),
            'files': len(set(line.file_path for line in self.lines)),
            'levels': Counter(line.level for line in self.lines if line.level),
            'errors': len(self.get_errors()),
            'warnings': len(self.get_warnings()),
            'exceptions': len(self.get_exceptions()),
        }
        
        # Timestamp range
        timestamps = [line.timestamp for line in self.lines if line.timestamp]
        if timestamps:
            stats['time_start'] = min(timestamps)
            stats['time_end'] = max(timestamps)
            stats['time_span'] = max(timestamps) - min(timestamps)
        
        return stats
    
    def get_top_patterns(self, n: int = 10) -> List[tuple]:
        """Find most common line patterns (normalized)"""
        # Normalize lines by removing numbers, timestamps, IPs
        normalized = []
        for line in self.lines:
            text = line.line
            # Remove timestamps
            text = PATTERNS['timestamp_iso'].sub('[TIMESTAMP]', text)
            text = PATTERNS['timestamp_common'].sub('[TIMESTAMP]', text)
            # Remove IPs
            text = PATTERNS['ip_address'].sub('[IP]', text)
            # Remove numbers
            text = re.sub(r'\b\d+\b', '[NUM]', text)
            normalized.append(text)
        
        return Counter(normalized).most_common(n)
    
    def tail(self, n: int = 10) -> List[LogLine]:
        """Get last N lines"""
        return self.lines[-n:] if self.lines else []
    
    def head(self, n: int = 10) -> List[LogLine]:
        """Get first N lines"""
        return self.lines[:n] if self.lines else []
    
    def context(self, line_indices: List[int], before: int = 3, after: int = 3) -> List[LogLine]:
        """Get context around specific line indices"""
        result = []
        for idx in line_indices:
            start = max(0, idx - before)
            end = min(len(self.lines), idx + after + 1)
            result.extend(self.lines[start:end])
        
        # Remove duplicates while preserving order
        seen = set()
        unique = []
        for line in result:
            key = (line.file_path, line.line_num)
            if key not in seen:
                seen.add(key)
                unique.append(line)
        
        return unique


def print_lines(lines: List[LogLine], limit: Optional[int] = None, highlight: Optional[Pattern] = None):
    """Pretty print log lines"""
    if not lines:
        print("No results found.")
        return
    
    display_lines = lines[:limit] if limit else lines
    
    for line in display_lines:
        line_str = str(line)
        
        # Highlight pattern if provided
        if highlight:
            line_str = highlight.sub(lambda m: f"\033[1;31m{m.group()}\033[0m", line_str)
        
        print(line_str)
    
    if limit and len(lines) > limit:
        print(f"\n... {len(lines) - limit} more results (use --limit to see more)")


def print_statistics(stats: Dict):
    """Pretty print statistics"""
    print("📊 Log Statistics\n")
    print(f"Total lines:  {stats['total_lines']:,}")
    print(f"Files:        {stats['files']}")
    
    if stats['levels']:
        print(f"\nLog Levels:")
        for level, count in sorted(stats['levels'].items(), key=lambda x: -x[1]):
            print(f"  {level:10} {count:,}")
    
    print(f"\n⚠️  Warnings:   {stats['warnings']:,}")
    print(f"❌ Errors:     {stats['errors']:,}")
    print(f"💥 Exceptions: {stats['exceptions']:,}")
    
    if 'time_start' in stats:
        print(f"\n📅 Time Range:")
        print(f"  Start: {stats['time_start']}")
        print(f"  End:   {stats['time_end']}")
        print(f"  Span:  {stats['time_span']}")


def parse_time_arg(time_str: str) -> datetime:
    """Parse time argument (ISO format or relative like '1h', '30m')"""
    # Relative time
    match = re.match(r'^(\d+)([smhd])$', time_str)
    if match:
        value = int(match.group(1))
        unit = match.group(2)
        
        now = datetime.now()
        if unit == 's':
            return now - timedelta(seconds=value)
        elif unit == 'm':
            return now - timedelta(minutes=value)
        elif unit == 'h':
            return now - timedelta(hours=value)
        elif unit == 'd':
            return now - timedelta(days=value)
    
    # Absolute time (ISO format)
    try:
        return datetime.fromisoformat(time_str)
    except:
        raise ValueError(f"Invalid time format: {time_str}")


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="LogHunter - Smart Log Analysis & Pattern Finder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  loghunter search app.log "error"              # Search for "error"
  loghunter search *.log "connection.*timeout"  # Regex search across files
  loghunter errors app.log                      # Show all errors
  loghunter stats app.log                       # Show statistics
  loghunter tail app.log -n 50                  # Last 50 lines
  loghunter level app.log ERROR WARN            # Filter by log level
  loghunter time app.log --since 1h             # Last hour
  loghunter patterns app.log                    # Find common patterns
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search logs with regex')
    search_parser.add_argument('files', help='Log file(s) or pattern (e.g., *.log)')
    search_parser.add_argument('pattern', help='Regex pattern to search for')
    search_parser.add_argument('-i', '--ignore-case', action='store_true', help='Case insensitive')
    search_parser.add_argument('-c', '--context', type=int, default=0, help='Lines of context')
    search_parser.add_argument('-l', '--limit', type=int, help='Limit results')
    
    # Errors command
    errors_parser = subparsers.add_parser('errors', help='Show all errors')
    errors_parser.add_argument('files', help='Log file(s) or pattern')
    errors_parser.add_argument('-l', '--limit', type=int, help='Limit results')
    
    # Warnings command
    warn_parser = subparsers.add_parser('warnings', aliases=['warn'], help='Show all warnings')
    warn_parser.add_argument('files', help='Log file(s) or pattern')
    warn_parser.add_argument('-l', '--limit', type=int, help='Limit results')
    
    # Level command
    level_parser = subparsers.add_parser('level', help='Filter by log level')
    level_parser.add_argument('files', help='Log file(s) or pattern')
    level_parser.add_argument('levels', nargs='+', help='Log levels to show')
    level_parser.add_argument('-l', '--limit', type=int, help='Limit results')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show log statistics')
    stats_parser.add_argument('files', help='Log file(s) or pattern')
    
    # Tail command
    tail_parser = subparsers.add_parser('tail', help='Show last N lines')
    tail_parser.add_argument('files', help='Log file(s) or pattern')
    tail_parser.add_argument('-n', '--lines', type=int, default=10, help='Number of lines')
    
    # Head command
    head_parser = subparsers.add_parser('head', help='Show first N lines')
    head_parser.add_argument('files', help='Log file(s) or pattern')
    head_parser.add_argument('-n', '--lines', type=int, default=10, help='Number of lines')
    
    # Time range command
    time_parser = subparsers.add_parser('time', help='Filter by time range')
    time_parser.add_argument('files', help='Log file(s) or pattern')
    time_parser.add_argument('--since', help='Start time (ISO or relative: 1h, 30m)')
    time_parser.add_argument('--until', help='End time (ISO or relative)')
    time_parser.add_argument('-l', '--limit', type=int, help='Limit results')
    
    # Patterns command
    patterns_parser = subparsers.add_parser('patterns', help='Find common log patterns')
    patterns_parser.add_argument('files', help='Log file(s) or pattern')
    patterns_parser.add_argument('-n', '--top', type=int, default=10, help='Top N patterns')
    
    # Exceptions command
    exc_parser = subparsers.add_parser('exceptions', aliases=['exc'], help='Show exceptions and stack traces')
    exc_parser.add_argument('files', help='Log file(s) or pattern')
    exc_parser.add_argument('-l', '--limit', type=int, help='Limit results')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Create LogHunter and load files
    hunter = LogHunter()
    hunter.load_files(args.files)
    
    if not hunter.lines:
        print("❌ No log data loaded")
        return
    
    # Execute command
    if args.command == 'search':
        results = hunter.filter_by_pattern(args.pattern, case_sensitive=not args.ignore_case)
        
        # Add context if requested
        if args.context > 0:
            indices = [hunter.lines.index(line) for line in results]
            results = hunter.context(indices, before=args.context, after=args.context)
        
        print(f"🔍 Found {len(results)} result(s)\n")
        
        # Highlight pattern
        flags = 0 if not args.ignore_case else re.IGNORECASE
        highlight = re.compile(args.pattern, flags)
        
        print_lines(results, limit=args.limit, highlight=highlight)
    
    elif args.command == 'errors':
        results = hunter.get_errors()
        print(f"❌ Found {len(results)} error(s)\n")
        print_lines(results, limit=args.limit)
    
    elif args.command in ['warnings', 'warn']:
        results = hunter.get_warnings()
        print(f"⚠️  Found {len(results)} warning(s)\n")
        print_lines(results, limit=args.limit)
    
    elif args.command == 'level':
        results = hunter.filter_by_level(args.levels)
        print(f"📋 Found {len(results)} line(s) with level(s): {', '.join(args.levels)}\n")
        print_lines(results, limit=args.limit)
    
    elif args.command == 'stats':
        stats = hunter.get_statistics()
        print_statistics(stats)
    
    elif args.command == 'tail':
        results = hunter.tail(args.lines)
        print(f"📄 Last {len(results)} line(s)\n")
        print_lines(results)
    
    elif args.command == 'head':
        results = hunter.head(args.lines)
        print(f"📄 First {len(results)} line(s)\n")
        print_lines(results)
    
    elif args.command == 'time':
        start_time = parse_time_arg(args.since) if args.since else None
        end_time = parse_time_arg(args.until) if args.until else None
        
        results = hunter.filter_by_time_range(start=start_time, end=end_time)
        print(f"📅 Found {len(results)} line(s) in time range\n")
        print_lines(results, limit=args.limit)
    
    elif args.command == 'patterns':
        patterns = hunter.get_top_patterns(args.top)
        print(f"🔍 Top {len(patterns)} Common Patterns\n")
        
        for i, (pattern, count) in enumerate(patterns, 1):
            print(f"{i}. ({count:,}×) {pattern[:100]}")
    
    elif args.command in ['exceptions', 'exc']:
        results = hunter.get_exceptions()
        print(f"💥 Found {len(results)} exception(s)\n")
        print_lines(results, limit=args.limit)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 LogHunter closed")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
