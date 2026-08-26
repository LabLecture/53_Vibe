import json, re, sys

DANGER = [r"\brm\s+-[a-z]*r", r"\bDROP\s+TABLE\b", r"\bDELETE\s+FROM\b",
          r"\bTRUNCATE\b", r"git\s+push\s+.*--force"]

data = json.loads(sys.stdin.read().lstrip("\ufeff"))   # PS 파이프 BOM 방어
cmd = data.get("tool_input", {}).get("command", "")

for pat in DANGER:
    if re.search(pat, cmd, re.IGNORECASE):
        print("[차단] 파괴적 명령이다: %s\n사람이 직접 실행해라." % pat, file=sys.stderr)
        sys.exit(2)          # 2 = 차단
sys.exit(0)