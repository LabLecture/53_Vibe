"""커밋 게이트 — 커밋 직전에 tests/legacy 를 돌리고, 빨간불이면 막는다.

Claude Code 의 PreToolUse(Bash) 훅으로 붙인다. stdin 으로 도구 호출 JSON 이 들어온다.
종료 코드 2 = "차단" (사유는 stderr 로 에이전트에게 전달된다).

셸 문법을 쓰지 않으므로 PowerShell·Git Bash·cmd 어디서 실행돼도 같게 동작한다.
"""
import json
import subprocess
import sys

# PowerShell 파이프는 UTF-8 BOM 을 붙인다 — lstrip 으로 견딘다
data = json.loads(sys.stdin.read().lstrip("﻿"))
command = data.get("tool_input", {}).get("command", "")

# 실제로 실행될 명령만 본다 — 파일 내용이나 주석에 섞인 문자열에는 걸리지 않는다
if not command.strip().startswith(("git commit", "git ci")):
    sys.exit(0)

result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/legacy", "-q"],
    capture_output=True,
    text=True,
    encoding="utf-8",      # Windows 기본은 cp949 — pytest 출력에 한글이 있으면 깨진다
    errors="replace",
)
if result.returncode != 0:
    last = (result.stdout.strip().splitlines() or ["(출력 없음)"])[-1]
    print("[차단] 테스트가 빨간불이다. 커밋 전에 고쳐라.", file=sys.stderr)
    print(last, file=sys.stderr)
    sys.exit(2)

sys.exit(0)
