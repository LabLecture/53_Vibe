import os
import datetime

_CACHE = {}
_LOG = os.path.join(os.path.dirname(__file__), "report.log")


def _w(msg):
    with open(_LOG, "a", encoding="utf-8") as f:
        f.write("%s %s\n" % (datetime.datetime.now().isoformat(timespec="seconds"), msg))

_MAX_LEN = 2000

def fmt(items, w=80):
    k = (w, tuple((it.get("title", ""), it.get("url")) for it in items))
    if k in _CACHE:
        _w("hit %s" % len(items))
        return _CACHE[k]
    out = []
    for i, it in enumerate(items, 1):
        t = it.get("title", "").strip()
        if len(t) > w:
            t = t[: w - 3] + "..."
        out.append("%2d. %s" % (i, t))
        u = it.get("url")
        if u:
            out.append("    %s" % u)
    s = "\n".join(out)
    _CACHE[k] = s
    _w("miss %s" % len(items))
    return s


def render(items, header=None):
    items = [it for it in items if it.get("title", "").strip()]
    body = fmt(items)
    if not body:
        return "새 논문 없음"
    h = header or ("주간 리포트 (%d건)" % len(items))
    rule = "-" * len(h)
    s = "%s\n%s\n%s" % (h, rule, body)
    if len(s) <= _MAX_LEN:
        return s
    n = len(items)
    while n > 0:
        n -= 1
        omitted = len(items) - n
        trimmed = fmt(items[:n])
        parts = [h, rule]
        if trimmed:
            parts.append(trimmed)
        parts.append("외 %d건" % omitted)
        s = "\n".join(parts)
        if len(s) <= _MAX_LEN:
            return s
    return s