#!/usr/bin/env python3
"""
premium_ascii.py — Generate a super premium, modern, and clean portfolio header banner.
Features a glassmorphic macOS terminal window, neon-gradient ASCII art, and dashboard stats.
"""
import os
import math
from PIL import Image, ImageOps, ImageEnhance

# ---- 1. ASCII portrait configuration ----------------------------------
PORTRAIT_PATH = "assets/portrait.png"
ASCII_COLS = 54
ASCII_FS = 13
ASCII_LH = 14
ASCII_CW = 7.8
RAMP = " .'`^\",:;Il!i~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

def portrait_rows(path, cols=ASCII_COLS):
    """Luminance-based ASCII conversion with shadow lift and autocontrast."""
    im = Image.open(path).convert("L")
    im = im.point(lambda v: int(((v / 255.0) ** 0.55) * 255)) # lift shadows
    im = ImageOps.autocontrast(im, cutoff=2)
    im = ImageEnhance.Contrast(im).enhance(1.25)
    w, h = im.size
    rows = max(1, int(cols * (h / w) * (ASCII_CW / ASCII_LH)))
    im = im.resize((cols, rows))
    px = im.load()
    n = len(RAMP) - 1
    out = []
    for y in range(rows):
        out.append("".join(RAMP[int((255 - px[x, y]) / 255 * n)] for x in range(cols)).rstrip())
    return out

def placeholder_rows(cols=ASCII_COLS, rows=30):
    out = []
    box = [
        "".ljust(cols),
        ("+" + "-" * (cols - 2) + "+"),
    ]
    mid_lines = rows - 6
    for i in range(mid_lines):
        if i == mid_lines // 3:
            line = "|" + "DROP portrait.png HERE".center(cols - 2) + "|"
        elif i == mid_lines // 3 + 2:
            line = "|" + "(56 cols wide, cropped to face)".center(cols - 2) + "|"
        else:
            line = "|" + " " * (cols - 2) + "|"
        out.append(line)
    out.append("+" + "-" * (cols - 2) + "+")
    return box + out

if os.path.exists(PORTRAIT_PATH):
    ASCII_ROWS = portrait_rows(PORTRAIT_PATH)
else:
    ASCII_ROWS = placeholder_rows()

# ---- 2. Right-panel content -------------------------------------------
NAME = "vartik@anand"
INFO = [
    ("header", NAME),
    ("kv", (["OS"], "macOS · Linux · Windows")),
    ("kv", (["Host"], "Full-Stack Web & Mobile Dev")),
    ("kv", (["Kernel"], "React · Next.js · Flutter")),
    ("kv", (["IDE"], "VSCode, Claude Code")),
    ("blank", None),
    ("kv", (["Languages", "Web"], "TypeScript, JavaScript, Node.js")),
    ("kv", (["Languages", "Mobile"], "Flutter, Dart")),
    ("kv", (["Languages", "Backend"], "Firebase, Supabase, NestJS")),
    ("kv", (["Styling"], "Tailwind CSS")),
    ("blank", None),
    ("kv", (["Currently"], "Building LeanHive")),
    ("kv", (["Learning"], "Next.js, Flutter, Python")),
    ("blank", None),
    ("section", "Contact"),
    ("kv", (["Portfolio"], "vartik.vercel.app")),
    ("kv", (["GitHub"], "VartikAnand")),
    ("kv", (["LinkedIn"], "vartikanand")),
    ("kv", (["YouTube"], "@dev-vartik")),
    ("blank", None),
    ("section", "GitHub Stats"),
    ("stats1", None),
]

VALUE_COL = 26
CW = 10.0
INFO_X = 520
W = 1120

# Palette matching the premium glassmorphic neon styling
THEMES = {
    "dark": {
        "bg_radial": "#060913",
        "bg_card": "rgba(10, 15, 30, 0.75)",
        "top_bar": "rgba(22, 30, 56, 0.9)",
        "border_gradient": ["#6366f1", "#a855f7", "#ec4899"], # Indigo -> Purple -> Pink
        "text": "#f8fafc",
        "key": "#cbd5e1",
        "value": "#60a5fa", # Light blue
        "cc": "#475569", # Slate-600
        "add": "#34d399", # Emerald-400
        "dele": "#f87171",
        "ascii_gradient": ["#818cf8", "#c084fc", "#f472b6"], # Indigo -> Purple -> Pink gradient
        "glow_color": "#818cf8",
        "title_text": "#94a3b8"
    },
    "light": {
        "bg_radial": "#f8fafc",
        "bg_card": "rgba(255, 255, 255, 0.75)",
        "top_bar": "rgba(241, 245, 249, 0.9)",
        "border_gradient": ["#3b82f6", "#6366f1", "#4f46e5"], # Blue -> Indigo
        "text": "#0f172a",
        "key": "#334155",
        "value": "#2563eb",
        "cc": "#94a3b8",
        "add": "#059669",
        "dele": "#dc2626",
        "ascii_gradient": ["#3b82f6", "#6366f1", "#8b5cf6"], # Blue -> Indigo -> Violet
        "glow_color": "#3b82f6",
        "title_text": "#64748b"
    }
}

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def leader(prefix_len):
    return max(1, VALUE_COL - prefix_len)

def kv_line(keys, value, t):
    key_txt = ".".join(keys)
    prefix_len = 2 + len(key_txt) + 1
    dots = leader(prefix_len)
    key_spans = (f'<tspan fill="{t["key"]}">'
                 + f'</tspan>.<tspan fill="{t["key"]}">'.join(esc(k) for k in keys)
                 + f'</tspan>')
    return (f'<tspan fill="{t["cc"]}">. </tspan>{key_spans}'
            f'<tspan fill="{t["cc"]}">:</tspan>'
            f'<tspan fill="{t["cc"]}"> {"." * dots} </tspan>'
            f'<tspan fill="{t["value"]}">{esc(value)}</tspan>')

def build_svg(theme_name):
    t = THEMES[theme_name]
    parts = []
    
    # Dynamic heights calculation
    card_x = 40
    card_y = 40
    top_h = 45
    line_spacing = 20
    
    ascii_height = len(ASCII_ROWS) * ASCII_LH
    # Spacing for right-panel content
    right_panel_lines_count = len(INFO) + 2 # Add terminal prompt line
    info_height = right_panel_lines_count * line_spacing + 30
    
    content_height = max(ascii_height, info_height)
    card_h = top_h + content_height + 40
    H = card_h + 80
    card_w = W - 80
    
    # 1. Header
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'font-family="system-ui, -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, Consolas, monospace" '
        f'width="{W}px" height="{H}px" font-size="16px">'
    )
    
    # 2. Defs for Gradients, Filters and Shadows
    parts.append("<defs>")
    # Backdrop radial gradient
    if theme_name == "dark":
        parts.append(
            f'<radialGradient id="bg-grad" cx="50%" cy="50%" r="70%">'
            f'<stop offset="0%" stop-color="#1e1b4b" stop-opacity="0.6"/>'
            f'<stop offset="60%" stop-color="#090d16" stop-opacity="1"/>'
            f'</radialGradient>'
        )
    else:
        parts.append(
            f'<radialGradient id="bg-grad" cx="50%" cy="50%" r="70%">'
            f'<stop offset="0%" stop-color="#eff6ff" stop-opacity="0.8"/>'
            f'<stop offset="100%" stop-color="#f8fafc" stop-opacity="1"/>'
            f'</radialGradient>'
        )
        
    # Card Border Gradient
    parts.append(
        f'<linearGradient id="card-border" x1="0%" y1="0%" x2="100%" y2="100%">'
        f'<stop offset="0%" stop-color="{t["border_gradient"][0]}"/>'
        f'<stop offset="50%" stop-color="{t["border_gradient"][1]}"/>'
        f'<stop offset="100%" stop-color="{t["border_gradient"][2] if len(t["border_gradient"]) > 2 else t["border_gradient"][1]}"/>'
        f'</linearGradient>'
    )
    # ASCII Art Gradient
    parts.append(
        f'<linearGradient id="ascii-grad" x1="0%" y1="0%" x2="0%" y2="100%">'
        f'<stop offset="0%" stop-color="{t["ascii_gradient"][0]}"/>'
        f'<stop offset="50%" stop-color="{t["ascii_gradient"][1]}"/>'
        f'<stop offset="100%" stop-color="{t["ascii_gradient"][2] if len(t["ascii_gradient"]) > 2 else t["ascii_gradient"][1]}"/>'
        f'</linearGradient>'
    )
    # Card shadow
    parts.append(
        f'<filter id="card-shadow" x="-10%" y="-10%" width="120%" height="120%">'
        f'<feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="#000000" flood-opacity="0.25"/>'
        f'</filter>'
    )
    # Glow filter for ASCII Text
    parts.append(
        f'<filter id="ascii-glow" x="-20%" y="-20%" width="140%" height="140%">'
        f'<feGaussianBlur stdDeviation="1" result="blur" />'
        f'<feMerge>'
        f'<feMergeNode in="blur" />'
        f'<feMergeNode in="SourceGraphic" />'
        f'</feMerge>'
        f'</filter>'
    )
    parts.append("</defs>")
    
    # 3. Ambient Background
    parts.append(f'<rect width="100%" height="100%" fill="url(#bg-grad)"/>')
    
    # Glowing Ambient Orbs behind the Card
    if theme_name == "dark":
        parts.append(
            f'<circle cx="200" cy="{H//2}" r="150" fill="#4f46e5" opacity="0.15" filter="url(#ascii-glow)"/>'
            f'<circle cx="920" cy="{H//2 - 50}" r="180" fill="#06b6d4" opacity="0.1" filter="url(#ascii-glow)"/>'
        )
    else:
        parts.append(
            f'<circle cx="200" cy="{H//2}" r="150" fill="#bfdbfe" opacity="0.3" filter="url(#ascii-glow)"/>'
            f'<circle cx="920" cy="{H//2 - 50}" r="180" fill="#ccfbf1" opacity="0.3" filter="url(#ascii-glow)"/>'
        )

    # 4. Main Glassmorphic Terminal Card
    parts.append(
        f'<rect x="{card_x}" y="{card_y}" width="{card_w}" height="{card_h}" '
        f'fill="{t["bg_card"]}" rx="20" stroke="url(#card-border)" stroke-width="1.5" '
        f'filter="url(#card-shadow)" />'
    )
    
    # 5. Terminal Header Top-Bar
    parts.append(
        f'<path d="M {card_x} {card_y + 20} '
        f'A 20 20 0 0 1 {card_x + 20} {card_y} '
        f'L {card_x + card_w - 20} {card_y} '
        f'A 20 20 0 0 1 {card_x + card_w} {card_y + 20} '
        f'L {card_x + card_w} {card_y + top_h} '
        f'L {card_x} {card_y + top_h} Z" '
        f'fill="{t["top_bar"]}" />'
    )
    
    # macOS style Window Buttons
    parts.append(
        f'<circle cx="{card_x + 25}" cy="{card_y + 22.5}" r="6" fill="#ff5f56"/>'
        f'<circle cx="{card_x + 45}" cy="{card_y + 22.5}" r="6" fill="#ffbd2e"/>'
        f'<circle cx="{card_x + 65}" cy="{card_y + 22.5}" r="6" fill="#27c93f"/>'
    )
    # Terminal Title Text
    parts.append(
        f'<text x="{card_x + card_w/2}" y="{card_y + 28}" text-anchor="middle" '
        f'fill="{t["title_text"]}" font-size="14px" font-family="Consolas, monospace" font-weight="bold">'
        f'vartik@terminal:~'
        f'</text>'
    )
    
    # Separation line below the top bar
    parts.append(
        f'<line x1="{card_x}" y1="{card_y + top_h}" x2="{card_x + card_w}" y2="{card_y + top_h}" '
        f'stroke="url(#card-border)" stroke-width="1" opacity="0.3"/>'
    )
    
    # 6. Left Panel - Glowing ASCII portrait
    ascii_y_start = card_y + top_h + 24
    parts.append(
        f'<text x="{card_x + 24}" y="{ascii_y_start}" fill="url(#ascii-grad)" '
        f'font-size="{ASCII_FS}px" font-family="Consolas, \'DejaVu Sans Mono\', monospace" '
        f'filter="url(#ascii-glow)" xml:space="preserve" letter-spacing="0">'
    )
    y_offset = ascii_y_start
    for row in ASCII_ROWS:
        parts.append(f'<tspan x="{card_x + 24}" y="{y_offset}">{esc(row)}</tspan>')
        y_offset += ASCII_LH
    parts.append("</text>")
    
    # 7. Right Panel - Terminal Info Showcase
    px = INFO_X
    info_y_start = card_y + top_h + 30
    y = info_y_start
    
    n_dash = int((W - px - 60) / CW) - 4
    
    parts.append(
        f'<text font-family="Consolas, \'DejaVu Sans Mono\', monospace" '
        f'font-size="15px" fill="{t["text"]}">'
    )
    
    for kind, payload in INFO:
        if kind == "header":
            dash = "-" * max(4, n_dash - len(payload))
            body = (f'<tspan x="{px}" y="{y}" fill="{t["text"]}" font-weight="bold">{esc(payload)}</tspan>'
                    f'<tspan fill="{t["cc"]}"> -{dash}-</tspan>')
        elif kind == "section":
            dash = "-" * max(4, n_dash - len(payload) - 2)
            body = (f'<tspan x="{px}" y="{y}" fill="{t["text"]}" font-weight="bold">- {esc(payload)}</tspan>'
                    f'<tspan fill="{t["cc"]}"> -{dash}-</tspan>')
        elif kind == "blank":
            body = f'<tspan x="{px}" y="{y}" fill="{t["cc"]}">. </tspan>'
        elif kind == "kv":
            keys, value = payload
            body = f'<tspan x="{px}" y="{y}">{kv_line(keys, value, t)}</tspan>'
        elif kind == "stats1":
            body = (f'<tspan x="{px}" y="{y}"><tspan fill="{t["cc"]}">. </tspan>'
                    f'<tspan fill="{t["key"]}">Repos</tspan>'
                    f'<tspan fill="{t["cc"]}"> ..... </tspan>'
                    f'<tspan fill="{t["value"]}" font-weight="bold">29</tspan>'
                    f'<tspan fill="{t["cc"]}"> | </tspan>'
                    f'<tspan fill="{t["key"]}">Stars</tspan>'
                    f'<tspan fill="{t["cc"]}"> ..... </tspan>'
                    f'<tspan fill="{t["value"]}" font-weight="bold">15</tspan>'
                    f'<tspan fill="{t["cc"]}"> | </tspan>'
                    f'<tspan fill="{t["key"]}">Followers</tspan>'
                    f'<tspan fill="{t["cc"]}"> . </tspan>'
                    f'<tspan fill="{t["value"]}" font-weight="bold">6</tspan></tspan>')
        
        parts.append(body)
        y += line_spacing
        
    # Blinking prompt + cursor at the bottom
    prompt_y = y + 8
    parts.append(
        f'<tspan x="{px}" y="{prompt_y}" fill="{t["add"]}" font-weight="bold">vartik@github</tspan>'
        f'<tspan fill="{t["text"]}">:~$</tspan>'
    )
    parts.append("</text>")
    
    # Interactive cursor rect
    cur_x = px + 17 * int(CW)
    parts.append(
        f'<rect x="{cur_x}" y="{prompt_y - 13}" width="{int(CW)}" height="17" '
        f'fill="{t["add"]}">'
        f'<animate attributeName="opacity" values="1;1;0;0" dur="1.1s" '
        f'keyTimes="0;0.5;0.5;1" repeatCount="indefinite"/></rect>'
    )
    
    parts.append("</svg>")
    return "\n".join(parts)

# Generate and save the premium SVGs
if __name__ == "__main__":
    for name in ("dark", "light"):
        out_filename = f"{name}_mode.svg"
        with open(out_filename, "w", encoding="utf-8") as f:
            f.write(build_svg(name))
        print("Generated and wrote:", out_filename)
