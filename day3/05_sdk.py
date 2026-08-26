# day3/05_sdk.py  (Python 3.10+) — 교안 5.5
# 관통 프로젝트 Summarizer — SDK 임베드 버전
import asyncio, os
from claude_agent_sdk import query, ClaudeAgentOptions

print("ANTHROPIC_API_KEY 설정 여부:", bool(os.getenv("ANTHROPIC_API_KEY")))

async def summarize_sdk(items):
    opts = ClaudeAgentOptions(
        system_prompt="너는 우리 파이프라인의 요약 담당이다. 사실만, 3문장.",
        allowed_tools=["Read", "Grep"],     # 최소 권한(Day 1 5교시 원칙을 코드로)
        permission_mode="default",
    )
    async for message in query(prompt="\n".join("- " + i for i in items), options=opts):
        if hasattr(message, "result"):      # 마지막 ResultMessage 가 최종 답
            return message.result
    return ""

if __name__ == "__main__":
    print(asyncio.run(summarize_sdk(
        ["MCP 표준이 확산 중", "에이전트 병렬 워크플로가 늘어남", "프롬프트 인젝션 관심 증가"])))
