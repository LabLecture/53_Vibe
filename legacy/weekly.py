from legacy.report import render


def build_weekly_message(papers):
    return render(papers)


def build_digest(papers, title):
    return render(papers, header=title)
