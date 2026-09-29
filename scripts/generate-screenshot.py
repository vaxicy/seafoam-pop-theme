"""Seafoam Pop Theme - 1280x800 store screenshot (headless browser render).

The mock-up faithfully follows the user's real Chrome screenshot (1080x645 with
this theme installed): same layout, same proportions (scaled to 1280x800) and
the same colours. Theme-controlled surfaces come from manifest.json; the
browser-owned bits are the values sampled from that real screenshot:

  Google NTP wordmark   #665BFF   (ntp_logo_alternate: 1 -> tinted wordmark)
  toolbar icons         #5B7C77   (theme's toolbar_button_icon tints them)
  customise pill text   #202124
  placeholder text      #70757A
  Lens icon             #4285F4

All copy is English (store assets must be English).

Run from the project root:  python3 scripts/generate-screenshot.py
Output: store-assets/screenshots/screenshot-1-browser.png
"""

import json
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = Path("store-assets") / "screenshots" / "screenshot-1-browser.png"
W, H = 1280, 800

# browser-owned colours sampled from the user's real screenshot
WORDMARK = "#665BFF"
PLACEHOLDER = "#70757A"
PILL_TEXT = "#202124"
ICON_GRAY = "#5F6368"
LENS_BLUE = "#4285F4"
LABEL = "#3C4043"


def hexof(c):
    return "#%02X%02X%02X" % tuple(c)


def build_html(c):
    frame = hexof(c["frame"])
    active = hexof(c["toolbar"])
    inactive = hexof(c["background_tab"])
    toolbar_icon = hexof(c["toolbar_button_icon"])
    ink = hexof(c["tab_text"])
    inactive_text = hexof(c["tab_background_text"])
    omnibox = hexof(c["omnibox_background"])
    ntp = hexof(c["ntp_background"])

    def tab(title, icon_bg, is_active=False):
        bg = active if is_active else inactive
        col = ink if is_active else inactive_text
        return f"""
      <div class="tab{' active' if is_active else ''}" style="background:{bg};color:{col}">
        <span class="favicon" style="background:{icon_bg}"></span>
        <span class="tab-title">{title}</span>
        <svg class="close" viewBox="0 0 16 16" width="12" height="12"
             stroke="{col}" stroke-width="1.6" stroke-linecap="round">
          <path d="M5 5l6 6M11 5l-6 6"/>
        </svg>
      </div>"""

    def tool(d):
        return f"""<svg viewBox="0 0 24 24" width="22" height="22" fill="none"
           stroke="{toolbar_icon}" stroke-width="1.8" stroke-linecap="round"
           stroke-linejoin="round">{d}</svg>"""

    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ width:{W}px; height:{H}px; overflow:hidden;
         font-family:'Segoe UI', Arial, sans-serif; background:{ntp}; }}
  .frame {{ position:absolute; inset:0; background:{frame}; }}
  .tabstrip {{ position:absolute; left:0; right:0; top:0; height:35px; background:{frame};
              display:flex; align-items:flex-end; padding-left:8px; }}
  .tab {{ height:29px; width:186px; margin-right:2px; border-radius:8px 8px 0 0;
         display:flex; align-items:center; gap:8px; padding:0 10px; font-size:12.5px;
         position:relative; }}
  .tab.active {{ height:33px; }}
  .favicon {{ width:14px; height:14px; border-radius:4px; flex:none; }}
  .tab-title {{ flex:1; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
                opacity:.92; }}
  .close {{ flex:none; opacity:.55; }}
  .newtab {{ width:26px; height:26px; margin:0 6px 4px; display:flex; align-items:center;
            justify-content:center; }}
  .controls {{ position:absolute; right:0; top:0; height:35px; display:flex;
              align-items:center; gap:22px; padding-right:16px; }}
  .controls span {{ display:block; background:{ink}; opacity:.72; }}
  .toolbar {{ position:absolute; left:0; right:0; top:35px; height:50px; background:{active};
             display:flex; align-items:center; padding:0 14px; gap:6px; }}
  .omnibox {{ flex:1; height:32px; margin:0 10px; border-radius:16px; background:{omnibox};
             display:flex; align-items:center; gap:10px; padding:0 12px; }}
  .omni-icons {{ margin-left:auto; display:flex; align-items:center; gap:10px; }}
  .ntp {{ position:absolute; left:0; right:0; top:85px; bottom:0; background:{ntp}; }}
  .wordmark {{ position:absolute; left:0; right:0; top:220px; text-align:center;
              font-size:76px; font-weight:700; letter-spacing:-1px;
              color:{WORDMARK}; font-family:Arial, sans-serif; }}
  .searchbox {{ position:absolute; left:327px; top:352px; width:626px; height:46px;
               border-radius:23px; background:#FFFFFF; box-shadow:0 1px 6px rgba(32,33,36,.18);
               display:flex; align-items:center; gap:12px; padding:0 16px; }}
  .placeholder {{ flex:1; font-size:14.5px; color:{PLACEHOLDER}; }}
  .shortcuts {{ position:absolute; left:0; right:0; top:432px; display:flex;
               justify-content:center; gap:66px; }}
  .shortcut {{ width:96px; text-align:center; }}
  .sicon {{ width:48px; height:48px; margin:0 auto 12px; border-radius:50%;
           display:flex; align-items:center; justify-content:center; }}
  .slabel {{ font-size:12.5px; color:{LABEL}; white-space:nowrap; }}
  .pill {{ position:absolute; right:14px; bottom:14px; height:34px; border-radius:17px;
          background:#FFFFFF; box-shadow:0 1px 4px rgba(32,33,36,.24); display:flex;
          align-items:center; gap:8px; padding:0 14px; font-size:13px; color:{PILL_TEXT}; }}
</style></head><body>
  <div class="frame"></div>
  <div class="tabstrip">
    {tab("Quarterly report.xlsx", "#1E7145", True)}
    {tab("Extensions", "#4285F4")}
    {tab("Inbox (12)", "#EA4335")}
    {tab("Theme shop", "#7B61FF")}
    {tab("New tab", "#34A853")}
    <div class="newtab">{tool('<path d="M12 6v12M6 12h12"/>')}</div>
    <div class="controls">
      <span style="width:11px;height:1px"></span>
      <span style="width:10px;height:10px;border:1px solid {ink};background:none;opacity:.72"></span>
      <svg viewBox="0 0 12 12" width="11" height="11" stroke="{ink}" stroke-width="1.4"
           stroke-linecap="round" style="opacity:.72"><path d="M2 2l8 8M10 2l-8 8"/></svg>
    </div>
  </div>
  <div class="toolbar">
    {tool('<path d="M15 5l-7 7 7 7"/>')}
    {tool('<path d="M9 5l7 7-7 7"/>')}
    {tool('<path d="M20 12a8 8 0 1 1-2.3-5.6"/><path d="M20 4v4h-4"/>')}
    <div class="omnibox">
      <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="{toolbar_icon}"
           stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="6"/>
        <path d="M16 16l4 4"/></svg>
      <div class="omni-icons">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="{ICON_GRAY}">
          <path d="M12 15a3 3 0 0 0 3-3V6a3 3 0 0 0-6 0v6a3 3 0 0 0 3 3z"/>
          <path d="M18 12a6 6 0 0 1-12 0" fill="none" stroke="{ICON_GRAY}" stroke-width="1.8"/>
          <path d="M12 18v3" fill="none" stroke="{ICON_GRAY}" stroke-width="1.8"/></svg>
        <svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="{LENS_BLUE}"
             stroke-width="1.9"><circle cx="11" cy="11" r="6.2"/><path d="M16 16l4.5 4.5"/>
        </svg>
      </div>
    </div>
    {tool('<path d="M12 4l2.6 5.6 6 .8-4.4 4.2 1.1 6-5.3-3-5.3 3 1.1-6L3.4 10.4l6-.8z"/>')}
    {tool('<path d="M10 5h4v3a2 2 0 1 0 2 2h3v4h-3a2 2 0 1 0-2 2v3h-4v-3a2 2 0 1 0-2-2H5v-4h3a2 2 0 1 0 2-2z"/>')}
    <div style="width:26px;height:26px;border-radius:50%;background:#7B61FF;color:#fff;
                font-size:12px;display:flex;align-items:center;justify-content:center">S</div>
    <svg viewBox="0 0 24 24" width="18" height="18" fill="{toolbar_icon}">
      <circle cx="12" cy="5" r="1.7"/><circle cx="12" cy="12" r="1.7"/>
      <circle cx="12" cy="19" r="1.7"/></svg>
  </div>
  <div class="ntp">
    <div class="wordmark">Google</div>
    <div class="searchbox">
      <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="{PLACEHOLDER}"
           stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="6"/>
        <path d="M16 16l4 4"/></svg>
      <div class="placeholder">Search Google or type a URL</div>
      <svg viewBox="0 0 24 24" width="18" height="18" fill="{ICON_GRAY}">
        <path d="M12 15a3 3 0 0 0 3-3V6a3 3 0 0 0-6 0v6a3 3 0 0 0 3 3z"/>
        <path d="M18 12a6 6 0 0 1-12 0" fill="none" stroke="{ICON_GRAY}" stroke-width="1.8"/>
        <path d="M12 18v3" fill="none" stroke="{ICON_GRAY}" stroke-width="1.8"/></svg>
      <svg viewBox="0 0 24 24" width="19" height="19" fill="none" stroke="{LENS_BLUE}"
           stroke-width="1.9"><circle cx="11" cy="11" r="6.2"/><path d="M16 16l4.5 4.5"/></svg>
    </div>
    <div class="shortcuts">
      <div class="shortcut"><div class="sicon" style="background:#FFFFFF;
        box-shadow:0 1px 4px rgba(32,33,36,.16)">
        <svg viewBox="0 0 24 24" width="24" height="24"><rect x="1.5" y="5" width="21"
          height="14" rx="4" fill="#FF0033"/><path d="M10 9l6 3-6 3z" fill="#fff"/></svg>
        </div><div class="slabel">YouTube</div></div>
      <div class="shortcut"><div class="sicon" style="background:#FFFFFF;
        box-shadow:0 1px 4px rgba(32,33,36,.16)">
        <svg viewBox="0 0 24 24" width="24" height="24"><circle cx="12" cy="12" r="9"
          fill="#4285F4"/><circle cx="12" cy="12" r="3.4" fill="#fff"/></svg>
        </div><div class="slabel">Chrome Web Store</div></div>
      <div class="shortcut"><div class="sicon" style="background:#958DFF">
        <svg viewBox="0 0 24 24" width="22" height="22" stroke="#fff" stroke-width="2.2"
          stroke-linecap="round"><path d="M12 6v12M6 12h12"/></svg>
        </div><div class="slabel">Add shortcut</div></div>
    </div>
    <div class="pill">
      <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="{PILL_TEXT}"
           stroke-width="1.8" stroke-linecap="round"><path d="M4 20h4L20 8l-4-4L4 16z"/></svg>
      Customize Chrome
    </div>
  </div>
</body></html>"""


def main():
    c = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    html = build_html(c["theme"]["colors"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": W, "height": H},
                               device_scale_factor=1)
        page.set_content(html, wait_until="load")
        page.screenshot(path=str(OUT))
        browser.close()
    print("wrote", OUT, W, H)


if __name__ == "__main__":
    main()
