def run_weekly_job() -> bool:
    """정시 트리거로 Crawler → Store → Notifier 파이프라인을 실행한다."""
    raise NotImplementedError


def retry_job(attempt: int, max_attempts: int) -> bool:
    """실행 실패·누락 감지 시 재시도를 수행한다."""
    raise NotImplementedError


if __name__ == "__main__":
    run_weekly_job()
