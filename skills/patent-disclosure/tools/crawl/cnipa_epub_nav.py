# -*- coding: utf-8 -*-
"""
公布站检索 **路径 B：整页导航提交**（``cnipa_epub_crawler.py`` 的兜底实现）。

本模块是原 ``cnipa_epub_crawler.py`` 的检索逻辑原样迁出，行为不变：
``page.fill`` 写检索框 → 对 ``#indexForm`` / ``#advForm`` 提交 → **整页导航** →
等结果页 ``<title>`` 与 ``#result`` DOM 就绪 → ``page.content()`` 取 HTML。

-------------------------------------------------------------------------------
与路径 A（``cnipa_epub_crawler.py`` 内的 fetch 快路径）的分工
-------------------------------------------------------------------------------
- **路径 A（默认）**：同一会话内用 ``fetch`` POST 表单，只取 HTML 文本。实测每词
  **0.3–0.5 秒**。
- **路径 B（本模块）**：整页导航，浏览器要额外加载结果页的 CSS/JS/图片等资源，
  实测每词 **约 20 秒**；但它走的是站点的常规交互路径，兼容性最好。

本模块因此保留为兜底：路径 A 被站点改版、``fetch`` 被拦截或返回非结果页时，
``cnipa_epub_crawler`` 会自动回退到这里，不影响既有行为。

**高级查询（分类号 + 名称）目前只走本模块**：其表单字段与提交端点未经 fetch 实测，
第二轮收口默认 1×1，一次导航的耗时可接受，不值得为此冒改版风险。

-------------------------------------------------------------------------------
本模块只提供**原子操作**，不含整轮循环
-------------------------------------------------------------------------------
整轮循环（多词、失败处理、回退选择）留在 ``cnipa_epub_crawler.search_epub_keywords``，
以便该模块的名字可被测试 patch。本模块只负责单跳的 gate / 提交 / 取 HTML。

等待参数：同目录 ``cnipa_epub_wait.yaml``（``EPUB_WAIT_YAML`` 可改路径），缺文件回退
``cnipa_epub_wait.DEFAULTS``；``EPUB_WAF_MAX_WAIT_SEC`` 若已设置则覆盖 ``gate_poll_sec``。
"""
from __future__ import annotations

import os
import sys
import time
from datetime import datetime
from pathlib import Path

from playwright.sync_api import (
    Browser,
    BrowserContext,
    Error,
    Page,
    Playwright,
    TimeoutError as PlaywrightTimeoutError,
)

_HERE = Path(__file__).resolve().parent
_TOOLS = _HERE.parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from browser import launch_chromium
from patent_type import TYPE_ALL, epub_checkbox_states
from cnipa_epub_wait import EpubNavError, load_wait_config, progress


EPUB_BASE = "http://epub.cnipa.gov.cn/"
EPUB_ADVANCED = EPUB_BASE.rstrip("/") + "/Advanced"
# 高级查询页 checkbox（与首页 #fmgb 等不同）
EPUB_ADVANCED_CHECKBOX = {
    "fmgb": "isFmgb",
    "fmsq": "isFmsq",
    "xxsq": "isXx",
    "wgsq": "isWg",
}
# 国知局 /Dxb/IndexQuery 结果页 <title>；改版时须同步单测与 _RESULT_PAGE_READY_JS
EPUB_TITLE_RESULT = "专利查询结果展示"
EPUB_TITLE_NO_HIT = "无查询结果"
# 在浏览器内判断结果页可解析：title + #result DOM（列表或零结果文案）
_RESULT_PAGE_READY_JS = """(titles) => {
    const t = document.title.trim();
    if (t === titles.noHit) return true;
    if (t !== titles.result) return false;
    const r = document.querySelector("#result");
    if (!r) return false;
    if (r.querySelector("div.item, h1.title")) return true;
    const html = r.innerHTML;
    if (
        html.includes("无查询结果") ||
        html.includes("没有找到") ||
        html.includes("未检索到") ||
        html.includes("0条")
    ) {
        return true;
    }
    return false;
}"""
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def _cfg() -> dict:
    return load_wait_config()


def _page_url(page: Page) -> str:
    try:
        return str(page.url or "")
    except Exception:
        return ""


def _nav_hint(*, advanced: bool) -> str:
    return "keep_round1" if advanced else "skip_epub"


def _goto(page: Page, url: str, *, advanced: bool) -> None:
    cfg = _cfg()
    timeout_ms = int(cfg["goto_timeout_ms"])
    wait_until = str(cfg["goto_wait_until"])
    progress(f"stage=goto wait_until={wait_until} timeout_ms={timeout_ms} url={url}")
    try:
        page.goto(url, wait_until=wait_until, timeout=timeout_ms)
    except (PlaywrightTimeoutError, Error) as exc:
        raise EpubNavError(
            "goto",
            hint=_nav_hint(advanced=advanced),
            message="打开公布站页面超时或失败",
            timeout_s=timeout_ms / 1000.0,
            url=url,
        ) from exc


def _wait_selector(
    page: Page,
    selector: str,
    *,
    advanced: bool,
    max_wait_sec: float | None = None,
) -> None:
    cfg = _cfg()
    limit = float(max_wait_sec) if max_wait_sec is not None else float(cfg["gate_poll_sec"])
    step = float(cfg["gate_poll_step_sec"])
    progress(f"stage=gate selector={selector} timeout_s={limit:g}")
    deadline = time.monotonic() + limit
    while True:
        try:
            if page.query_selector(selector):
                return
        except Error:
            pass
        if time.monotonic() >= deadline:
            raise EpubNavError(
                "gate",
                hint=_nav_hint(advanced=advanced),
                message=f"页面已打开但未出现 {selector}",
                timeout_s=limit,
                url=_page_url(page),
            )
        remaining = deadline - time.monotonic()
        page.wait_for_timeout(int(min(step, max(remaining, 0.05)) * 1000))


def _headed() -> bool:
    return os.environ.get("PLAYWRIGHT_HEADED", "").strip() in ("1", "true", "yes")


def default_result_html_path() -> Path:
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    return Path(__file__).resolve().parent / f"_last_result_{ts}.html"


def wait_for_epub_home_ready(page: Page, *, max_wait_sec: float | None = None) -> None:
    if page.query_selector("#searchStr"):
        return
    _goto(page, EPUB_BASE, advanced=False)
    _wait_selector(page, "#searchStr", advanced=False, max_wait_sec=max_wait_sec)


def open_epub_advanced_search(page: Page) -> None:
    """Open CNIPA's fielded search after the browser session passed the home gate."""
    _goto(page, EPUB_ADVANCED, advanced=True)
    _wait_selector(page, "#advForm #e72", advanced=True)


def _safe_page_content(page: Page, *, max_attempts: int = 10) -> str:
    last_err: Exception | None = None
    for i in range(max_attempts):
        try:
            return page.content()
        except Error as e:
            msg = str(e).lower()
            last_err = e
            if "navigating" not in msg and "changing" not in msg:
                raise
            try:
                page.wait_for_load_state("load", timeout=20_000)
            except Exception:
                pass
            page.wait_for_timeout(400 + 200 * i)
    if last_err:
        raise last_err
    raise RuntimeError("_safe_page_content: 未返回内容")


def _wait_result_page_ready(page: Page, *, advanced: bool = False) -> None:
    """等结果页 title 与 #result 列表/零结果 DOM 就绪（不等完整 load）。"""
    timeout_ms = int(_cfg()["submit_timeout_ms"])
    progress(f"stage=submit timeout_ms={timeout_ms}")
    try:
        page.wait_for_function(
            _RESULT_PAGE_READY_JS,
            arg={"result": EPUB_TITLE_RESULT, "noHit": EPUB_TITLE_NO_HIT},
            timeout=timeout_ms,
        )
    except PlaywrightTimeoutError as exc:
        raise EpubNavError(
            "submit",
            hint=_nav_hint(advanced=advanced),
            message="提交后未出现结果页（有结果或明确0条）",
            timeout_s=timeout_ms / 1000.0,
            url=_page_url(page),
        ) from exc


def apply_epub_type_filter(page: Page, patent_type: str = TYPE_ALL) -> None:
    """按类型勾选首页 #fmgb/#fmsq/#xxsq/#wgsq（与截图四类一致）。"""
    states = epub_checkbox_states(patent_type)
    for cid, want in states.items():
        box = page.query_selector(f"#{cid}")
        if not box:
            continue
        try:
            if want:
                box.check(force=True)
            else:
                box.uncheck(force=True)
        except Error:
            page.evaluate(
                """({id, checked}) => {
                    const el = document.getElementById(id);
                    if (!el) return;
                    el.checked = checked;
                    el.dispatchEvent(new Event('change', { bubbles: true }));
                    el.dispatchEvent(new Event('click', { bubbles: true }));
                }""",
                {"id": cid, "checked": want},
            )


def apply_epub_advanced_type_filter(page: Page, patent_type: str = TYPE_ALL) -> None:
    """高级查询页勾选 #isFmgb / #isFmsq / #isXx / #isWg。"""
    states = epub_checkbox_states(patent_type)
    for home_id, want in states.items():
        cid = EPUB_ADVANCED_CHECKBOX.get(home_id)
        if not cid:
            continue
        box = page.query_selector(f"#{cid}")
        if not box:
            continue
        try:
            if want:
                box.check(force=True)
            else:
                box.uncheck(force=True)
        except Error:
            page.evaluate(
                """({id, checked}) => {
                    const el = document.getElementById(id);
                    if (!el) return;
                    el.checked = checked;
                    el.dispatchEvent(new Event('change', { bubbles: true }));
                    el.dispatchEvent(new Event('click', { bubbles: true }));
                }""",
                {"id": cid, "checked": want},
            )


def wait_for_epub_advanced_ready(page: Page, *, max_wait_sec: float | None = None) -> None:
    """打开 /Advanced，等到分类号框 #e51。框已在则不重新 goto。"""
    if page.query_selector("#e51"):
        return
    _goto(page, EPUB_ADVANCED, advanced=True)
    _wait_selector(page, "#e51", advanced=True, max_wait_sec=max_wait_sec)


def submit_advanced_search(
    page: Page,
    keyword: str,
    *,
    class_code: str,
    patent_type: str = TYPE_ALL,
) -> None:
    """高级查询：分类号 #e51 + 名称 #ti，类型勾选后提交。等结果标题，不死等 AdvancedQuery+load。"""
    apply_epub_advanced_type_filter(page, patent_type)
    page.fill("#e51", class_code)
    if page.query_selector("#ti"):
        page.fill("#ti", keyword or "")
    form = page.query_selector("#advForm")
    if form is None:
        raise RuntimeError("高级查询未找到 #advForm")
    btn = form.query_selector("button")
    if btn is None:
        raise RuntimeError("高级查询未找到提交按钮")
    btn.click()
    _wait_result_page_ready(page, advanced=True)


def submit_index_search(
    page: Page,
    keyword: str,
    *,
    patent_type: str = TYPE_ALL,
) -> None:
    apply_epub_type_filter(page, patent_type)
    page.fill("#searchStr", keyword)
    timeout_ms = int(_cfg()["submit_timeout_ms"])
    try:
        with page.expect_navigation(timeout=timeout_ms, wait_until="commit"):
            form = page.query_selector("#indexForm")
            if form:
                form.evaluate("el => el.submit()")
            else:
                page.evaluate(
                    """() => {
                    const f = document.getElementById('indexForm');
                    if (f) f.submit();
                }"""
                )
    except (PlaywrightTimeoutError, Error) as exc:
        raise EpubNavError(
            "submit",
            hint=_nav_hint(advanced=False),
            message="首页提交后导航超时",
            timeout_s=timeout_ms / 1000.0,
            url=_page_url(page),
        ) from exc
    _wait_result_page_ready(page, advanced=False)


def _launch_browser(p: Playwright) -> Browser:
    browser, _label = launch_chromium(p, headless=not _headed())
    return browser


def _new_context(browser: Browser) -> BrowserContext:
    """桌面 Chrome UA + zh-CN + 固定视口。

    **UA 必须覆盖**：默认无头 UA 含 ``HeadlessChrome``，实测会被站点防护直接拒绝
    （首页 DOM 仅 39 字节、``#searchStr`` 永不出现）。详见 ``cnipa_epub_crawler`` 文件头。
    """
    if sys.platform == "darwin":
        platform_token = "Macintosh; Intel Mac OS X 10_15_7"
    elif sys.platform.startswith("linux"):
        platform_token = "X11; Linux x86_64"
    else:
        platform_token = "Windows NT 10.0; Win64; x64"
    user_agent = DEFAULT_USER_AGENT.format(version=browser.version).replace(
        "Windows NT 10.0; Win64; x64", platform_token
    )
    return browser.new_context(
        user_agent=user_agent,
        locale="zh-CN",
        viewport={"width": 1280, "height": 900},
    )
