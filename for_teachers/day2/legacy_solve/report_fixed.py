import os
import datetime

_CACHE = {}
_LOG = os.path.join(os.path.dirname(__file__), "report.log")


def _w(msg):
    with open(_LOG, "a", encoding="utf-8") as f:
        f.write("%s %s\n" % (datetime.datetime.now().isoformat(timespec="seconds"), msg))


def fmt(items, w=80):
    k = (w,) + tuple((it.get("title", ""), it.get("url")) for it in items)
    if k in _CACHE:
        _w("hit %s" % (k,))
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
    _w("miss %s" % (k,))
    return s


def render(items, header=None):
    body = fmt(items)
    if not body:
        return "새 논문 없음"
    h = header or ("주간 리포트 (%d건)" % len(items))
    return "%s\n%s\n%s" % (h, "-" * len(h), body)
