from legacy.weekly import build_weekly_message

week1 = [
    {"title": "Attention Is All You Need", "url": "http://arxiv.org/abs/1706.03762"},
    {"title": "Denoising Diffusion Probabilistic Models", "url": "http://arxiv.org/abs/2006.11239"},
]
week2 = [
    {"title": "Mamba: Linear-Time Sequence Modeling", "url": "http://arxiv.org/abs/2312.00752"},
    {"title": "Direct Preference Optimization", "url": "http://arxiv.org/abs/2305.18290"},
]
print("=== 1주차 ===")
print(build_weekly_message(week1))
print("=== 2주차 ===")
print(build_weekly_message(week2))
