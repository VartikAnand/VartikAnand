#!/usr/bin/env python3
"""
premium_ascii.py — Generate a super premium, modern, and clean portfolio header banner.
Features a glassmorphic macOS terminal window, neon-gradient ASCII art, and dashboard stats
with real-time typing animations (SMIL in SVG and live print in python).
"""
import os
import sys
import time
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
CW = 9.0 # Character width advance for 15px font
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
        "ascii_gradient": ["#818cf8", "#c084fc", "#f472b6"], # Indigo -> Purple -> Pink
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

def get_plain_text(kind, payload, n_dash):
    if kind == "header":
        dash = "-" * max(4, n_dash - len(payload))
        return f"{payload} -{dash}-"
    elif kind == "section":
        dash = "-" * max(4, n_dash - len(payload) - 2)
        return f"- {payload} -{dash}-"
    elif kind == "blank":
        return ". "
    elif kind == "kv":
        keys, value = payload
        key_txt = ".".join(keys)
        prefix_len = 2 + len(key_txt) + 1
        dots = leader(prefix_len)
        return f". {key_txt}: {'.' * dots} {value}"
    elif kind == "stats1":
        return ". Repos ..... 29 | Stars ..... 15 | Followers . 6"
    return ""

def build_svg(theme_name):
    t = THEMES[theme_name]
    parts = []
    
    # Dynamic heights calculation
    card_x = 40
    card_y = 40
    top_h = 45
    line_spacing = 20
    
    ascii_height = len(ASCII_ROWS) * ASCII_LH
    right_panel_lines_count = len(INFO)
    info_height = right_panel_lines_count * line_spacing + 40
    
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
        f'<stop offset="0%" stop-color="{t["border_gradient"][0]}">'
        f'<animate attributeName="stop-color" values="{t["border_gradient"][0]}; {t["border_gradient"][1]}; {t["border_gradient"][2] if len(t["border_gradient"]) > 2 else t["border_gradient"][0]}; {t["border_gradient"][0]}" dur="6s" repeatCount="indefinite" />'
        f'</stop>'
        f'<stop offset="50%" stop-color="{t["border_gradient"][1]}">'
        f'<animate attributeName="stop-color" values="{t["border_gradient"][1]}; {t["border_gradient"][2] if len(t["border_gradient"]) > 2 else t["border_gradient"][0]}; {t["border_gradient"][0]}; {t["border_gradient"][1]}" dur="6s" repeatCount="indefinite" />'
        f'</stop>'
        f'<stop offset="100%" stop-color="{t["border_gradient"][2] if len(t["border_gradient"]) > 2 else t["border_gradient"][1]}">'
        f'<animate attributeName="stop-color" values="{t["border_gradient"][2] if len(t["border_gradient"]) > 2 else t["border_gradient"][1]}; {t["border_gradient"][0]}; {t["border_gradient"][1]}; {t["border_gradient"][2] if len(t["border_gradient"]) > 2 else t["border_gradient"][1]}" dur="6s" repeatCount="indefinite" />'
        f'</stop>'
        f'</linearGradient>'
    )
    # ASCII Art Gradient
    parts.append(
        f'<linearGradient id="ascii-grad" x1="0%" y1="0%" x2="0%" y2="100%">'
        f'<stop offset="0%" stop-color="{t["ascii_gradient"][0]}">'
        f'<animate attributeName="stop-color" values="{t["ascii_gradient"][0]}; {t["ascii_gradient"][1]}; {t["ascii_gradient"][2] if len(t["ascii_gradient"]) > 2 else t["ascii_gradient"][0]}; {t["ascii_gradient"][0]}" dur="4s" repeatCount="indefinite" />'
        f'</stop>'
        f'<stop offset="50%" stop-color="{t["ascii_gradient"][1]}">'
        f'<animate attributeName="stop-color" values="{t["ascii_gradient"][1]}; {t["ascii_gradient"][2] if len(t["ascii_gradient"]) > 2 else t["ascii_gradient"][0]}; {t["ascii_gradient"][0]}; {t["ascii_gradient"][1]}" dur="4s" repeatCount="indefinite" />'
        f'</stop>'
        f'<stop offset="100%" stop-color="{t["ascii_gradient"][2] if len(t["ascii_gradient"]) > 2 else t["ascii_gradient"][1]}">'
        f'<animate attributeName="stop-color" values="{t["ascii_gradient"][2] if len(t["ascii_gradient"]) > 2 else t["ascii_gradient"][1]}; {t["ascii_gradient"][0]}; {t["ascii_gradient"][1]}; {t["ascii_gradient"][2] if len(t["ascii_gradient"]) > 2 else t["ascii_gradient"][1]}" dur="4s" repeatCount="indefinite" />'
        f'</stop>'
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
    
    # CRT monitor hum and text vibration keyframes
    parts.append(
        "<style>"
        "/* CRT monitor flicker / hum */"
        "@keyframes terminal-hum {"
        "  0% { opacity: 0.97; }"
        "  50% { opacity: 1.0; }"
        "  100% { opacity: 0.98; }"
        "}"
        "/* Text typing jitter / shake */"
        "@keyframes text-jitter {"
        "  0% { transform: translate(0, 0); }"
        "  10% { transform: translate(-0.3px, 0.3px); }"
        "  20% { transform: translate(-0.3px, -0.3px); }"
        "  30% { transform: translate(0.3px, 0.3px); }"
        "  40% { transform: translate(0.3px, -0.3px); }"
        "  50% { transform: translate(-0.3px, 0.3px); }"
        "  60% { transform: translate(0.3px, 0.3px); }"
        "  70% { transform: translate(-0.3px, -0.3px); }"
        "  80% { transform: translate(0.3px, -0.3px); }"
        "  90% { transform: translate(-0.3px, 0.3px); }"
        "  100% { transform: translate(0, 0); }"
        "}"
        "text {"
        "  animation: terminal-hum 0.15s infinite, text-jitter 0.25s infinite;"
        "}"
        "</style>"
    )
    
    # 3. Animation ClipPaths for Right-Panel Info Rows (Typing Effect)
    px = INFO_X
    info_y_start = card_y + top_h + 30
    y = info_y_start
    n_dash = int((W - px - 60) / CW) - 4
    
    # ASCII art reveal starts at 0s, runs for 1.2s
    # Right panel starts typing at 0.8s (overlapping)
    line_dur = 0.28 # seconds per line
    start_delay = 0.8
    
    # Reveal wipe for ASCII Art
    parts.append(
        f'<clipPath id="ascii-wipe">'
        f'<rect x="{card_x + 24}" y="{card_y + top_h}" width="500" height="0">'
        f'<animate attributeName="height" from="0" to="{ascii_height + 40}" '
        f'begin="0s" dur="1.2s" fill="freeze" calcMode="linear"/>'
        f'</rect>'
        f'</clipPath>'
    )
    
    # Generate clip-paths for info lines
    for i, (kind, payload) in enumerate(INFO):
        plain_text = get_plain_text(kind, payload, n_dash)
        text_w = len(plain_text) * CW
        line_start = start_delay + i * line_dur
        
        parts.append(
            f'<clipPath id="clip-row-{i}">'
            f'<rect x="{px}" y="{y - 15}" width="0" height="24">'
            f'<animate attributeName="width" from="0" to="{text_w:.1f}" '
            f'begin="{line_start:.3f}s" dur="{line_dur:.3f}s" '
            f'fill="freeze" calcMode="linear"/>'
            f'</rect>'
            f'</clipPath>'
        )
        y += line_spacing
        
    parts.append("</defs>")
    
    # 4. Ambient Background
    parts.append(f'<rect width="100%" height="100%" fill="url(#bg-grad)"/>')
    
    if theme_name == "dark":
        parts.append(
            f'<circle cx="200" cy="{H//2}" r="150" fill="#4f46e5" opacity="0.15" filter="url(#ascii-glow)">'
            f'<animate attributeName="r" values="130;170;130" dur="6s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.1;0.2;0.1" dur="6s" repeatCount="indefinite"/>'
            f'</circle>'
            f'<circle cx="920" cy="{H//2 - 50}" r="180" fill="#06b6d4" opacity="0.1" filter="url(#ascii-glow)">'
            f'<animate attributeName="r" values="160;200;160" dur="6s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.07;0.15;0.07" dur="6s" repeatCount="indefinite"/>'
            f'</circle>'
        )
    else:
        parts.append(
            f'<circle cx="200" cy="{H//2}" r="150" fill="#bfdbfe" opacity="0.3" filter="url(#ascii-glow)">'
            f'<animate attributeName="r" values="130;170;130" dur="6s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.2;0.4;0.2" dur="6s" repeatCount="indefinite"/>'
            f'</circle>'
            f'<circle cx="920" cy="{H//2 - 50}" r="180" fill="#ccfbf1" opacity="0.3" filter="url(#ascii-glow)">'
            f'<animate attributeName="r" values="160;200;160" dur="6s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.2;0.4;0.2" dur="6s" repeatCount="indefinite"/>'
            f'</circle>'
        )

    # 5. Main Glassmorphic Terminal Card
    parts.append(
        f'<rect x="{card_x}" y="{card_y}" width="{card_w}" height="{card_h}" '
        f'fill="{t["bg_card"]}" rx="20" stroke="url(#card-border)" stroke-width="1.5" '
        f'filter="url(#card-shadow)" />'
    )
    
    # 6. Terminal Header Top-Bar
    parts.append(
        f'<path d="M {card_x} {card_y + 20} '
        f'A 20 20 0 0 1 {card_x + 20} {card_y} '
        f'L {card_x + card_w - 20} {card_y} '
        f'A 20 20 0 0 1 {card_x + card_w} {card_y + 20} '
        f'L {card_x + card_w} {card_y + top_h} '
        f'L {card_x} {card_y + top_h} Z" '
        f'fill="{t["top_bar"]}" />'
    )
    
    parts.append(
        f'<circle cx="{card_x + 25}" cy="{card_y + 22.5}" r="6" fill="#ff5f56"/>'
        f'<circle cx="{card_x + 45}" cy="{card_y + 22.5}" r="6" fill="#ffbd2e"/>'
        f'<circle cx="{card_x + 65}" cy="{card_y + 22.5}" r="6" fill="#27c93f"/>'
    )
    parts.append(
        f'<text x="{card_x + card_w/2}" y="{card_y + 28}" text-anchor="middle" '
        f'fill="{t["title_text"]}" font-size="14px" font-family="Consolas, monospace" font-weight="bold">'
        f'vartik@terminal:~'
        f'</text>'
    )
    parts.append(
        f'<line x1="{card_x}" y1="{card_y + top_h}" x2="{card_x + card_w}" y2="{card_y + top_h}" '
        f'stroke="url(#card-border)" stroke-width="1" opacity="0.3"/>'
    )
    
    # 7. Left Panel - Glowing ASCII portrait (reveals top-to-bottom)
    ascii_y_start = card_y + top_h + 24
    parts.append(f'<g>')
    parts.append(
        f'<animateTransform attributeName="transform" type="translate" '
        f'values="0,0; 0,5; 0,0" dur="6s" repeatCount="indefinite"/>'
    )
    parts.append(
        f'<text x="{card_x + 24}" y="{ascii_y_start}" fill="url(#ascii-grad)" '
        f'font-size="{ASCII_FS}px" font-family="Consolas, \'DejaVu Sans Mono\', monospace" '
        f'filter="url(#ascii-glow)" xml:space="preserve" letter-spacing="0" '
        f'clip-path="url(#ascii-wipe)">'
    )
    y_offset = ascii_y_start
    for row in ASCII_ROWS:
        parts.append(f'<tspan x="{card_x + 24}" y="{y_offset}">{esc(row)}</tspan>')
        y_offset += ASCII_LH
    parts.append("</text>")
    
    # Glowing Laser Scanline Sweep across the ASCII portrait
    parts.append(
        f'<rect x="{card_x + 24}" y="{ascii_y_start}" width="{ASCII_COLS * ASCII_CW}" height="2" '
        f'fill="url(#ascii-grad)" opacity="0.6" filter="url(#ascii-glow)">'
        f'<animate attributeName="y" values="{ascii_y_start}; {ascii_y_start + ascii_height}; {ascii_y_start}" '
        f'dur="6s" repeatCount="indefinite"/>'
        f'</rect>'
    )
    parts.append("</g>")
    
    # 8. Right Panel - Terminal Info Showcase (individual typing lines & cursors)
    y = info_y_start
    for i, (kind, payload) in enumerate(INFO):
        plain_text = get_plain_text(kind, payload, n_dash)
        text_w = len(plain_text) * CW
        line_start = start_delay + i * line_dur
        
        # Render the specific line
        parts.append(
            f'<text x="{px}" y="{y}" font-family="Consolas, \'DejaVu Sans Mono\', monospace" '
            f'font-size="15px" fill="{t["text"]}" clip-path="url(#clip-row-{i})">'
        )
        
        if kind == "header":
            dash = "-" * max(4, n_dash - len(payload))
            body = (f'<tspan fill="{t["text"]}" font-weight="bold">{esc(payload)}</tspan>'
                    f'<tspan fill="{t["cc"]}"> -{dash}-</tspan>')
        elif kind == "section":
            dash = "-" * max(4, n_dash - len(payload) - 2)
            body = (f'<tspan fill="{t["text"]}" font-weight="bold">- {esc(payload)}</tspan>'
                    f'<tspan fill="{t["cc"]}"> -{dash}-</tspan>')
        elif kind == "blank":
            body = f'<tspan fill="{t["cc"]}">. </tspan>'
        elif kind == "kv":
            keys, value = payload
            body = kv_line(keys, value, t)
        elif kind == "stats1":
            body = (f'<tspan fill="{t["cc"]}">. </tspan>'
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
                    f'<tspan fill="{t["value"]}" font-weight="bold">6</tspan>')
                    
        parts.append(body)
        parts.append("</text>")
        
        # Active typing block cursor for this row
        parts.append(
            f'<rect y="{y - 13}" width="{CW}" height="17" fill="{t["add"]}" opacity="0">'
            f'<animate attributeName="x" from="{px}" to="{px + text_w:.1f}" '
            f'begin="{line_start:.3f}s" dur="{line_dur:.3f}s" fill="freeze" calcMode="linear"/>'
            f'<set attributeName="opacity" to="1" begin="{line_start:.3f}s"/>'
            f'<set attributeName="opacity" to="0" begin="{line_start + line_dur:.3f}s"/>'
            f'</rect>'
        )
        y += line_spacing
        
    # Blinking prompt + cursor at the bottom (shows after all rows are typed)
    prompt_y = y + 8
    final_start = start_delay + len(INFO) * line_dur
    
    parts.append(
        f'<text x="{px}" y="{prompt_y}" font-family="Consolas, \'DejaVu Sans Mono\', monospace" '
        f'font-size="15px" fill="{t["text"]}" clip-path="url(#clip-prompt)">'
    )
    # Clip for prompt line
    prompt_w = 17 * CW
    parts.append(
        f'<clipPath id="clip-prompt">'
        f'<rect x="{px}" y="{prompt_y - 15}" width="0" height="24">'
        f'<animate attributeName="width" from="0" to="{prompt_w:.1f}" '
        f'begin="{final_start:.3f}s" dur="{line_dur:.3f}s" fill="freeze"/>'
        f'</rect>'
        f'</clipPath>'
    )
    parts.append(
        f'<tspan fill="{t["add"]}" font-weight="bold">vartik@github</tspan>'
        f'<tspan fill="{t["text"]}">:~$</tspan>'
    )
    parts.append("</text>")
    
    # Prompt active cursor: sweeps during prompt typing, then blinks indefinitely
    cur_x_start = px
    cur_x_end = px + 17 * CW
    parts.append(
        f'<rect y="{prompt_y - 13}" width="{CW}" height="17" fill="{t["add"]}" opacity="0">'
        # Sweep sweep
        f'<animate attributeName="x" from="{cur_x_start}" to="{cur_x_end:.1f}" '
        f'begin="{final_start:.3f}s" dur="{line_dur:.3f}s" fill="freeze"/>'
        f'<set attributeName="opacity" to="1" begin="{final_start:.3f}s"/>'
        # Indefinite blink after it settles
        f'<animate attributeName="opacity" values="1;1;0;0" dur="1.1s" '
        f'keyTimes="0;0.5;0.5;1" repeatCount="indefinite" begin="{final_start + line_dur:.3f}s"/>'
        f'</rect>'
    )
    
    # Glowing Laser Scanline Sweep across the Right-Panel Text
    right_panel_w = card_w - (px - card_x) - 24
    parts.append(
        f'<rect x="{px}" y="{info_y_start}" width="{right_panel_w}" height="2" '
        f'fill="url(#ascii-grad)" opacity="0.4" filter="url(#ascii-glow)">'
        f'<animate attributeName="y" values="{info_y_start}; {info_y_start + info_height}; {info_y_start}" '
        f'dur="6s" repeatCount="indefinite"/>'
        f'</rect>'
    )
    
    parts.append("</svg>")
    return "\n".join(parts)

# Print terminal typewriter animation to console
def console_typewriter():
    n_dash = int((W - INFO_X - 60) / CW) - 4
    
    print("\n\033[1;36mInitializing Premium Portfolio Terminal...\033[0m")
    time.sleep(0.5)
    
    # 1. Print ASCII Art
    print("\033[1;35mLoading ASCII portrait...\033[0m")
    for row in ASCII_ROWS:
        sys.stdout.write("  " + row + "\n")
        sys.stdout.flush()
        time.sleep(0.015)
        
    print("\033[1;32mConnection established.\033[0m\n")
    time.sleep(0.3)
    
    # 2. Type out Right Panel
    for kind, payload in INFO:
        plain_text = get_plain_text(kind, payload, n_dash)
        
        # Style console output based on row type
        if kind == "header" or kind == "section":
            styled_text = f"\033[1;37m{plain_text}\033[0m"
        elif kind == "blank":
            styled_text = "  ."
        elif kind == "stats1":
            styled_text = f"  \033[90m. \033[37mRepos \033[90m..... \033[1;34m29 \033[90m| \033[37mStars \033[90m..... \033[1;34m15 \033[90m| \033[37mFollowers \033[90m. \033[1;34m6\033[0m"
        else:
            # key value line formatting for terminal
            keys, value = payload
            key_txt = ".".join(keys)
            prefix_len = 2 + len(key_txt) + 1
            dots = leader(prefix_len)
            styled_text = f"  \033[90m. \033[33m{key_txt}\033[90m: {'.' * dots} \033[1;34m{value}\033[0m"
            
        # Character-by-character print
        sys.stdout.write("  ")
        for char in plain_text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.008)
        sys.stdout.write("\n")
        time.sleep(0.08)
        
    # Prompt line
    sys.stdout.write("  \033[1;32mvartik@github\033[0m:~$ ")
    sys.stdout.flush()
    time.sleep(0.2)
    prompt_text = "neofetch"
    for char in prompt_text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\n\n")

if __name__ == "__main__":
    # Generate the premium SVGs
    for name in ("dark", "light"):
        out_filename = f"{name}_mode.svg"
        with open(out_filename, "w", encoding="utf-8") as f:
            f.write(build_svg(name))
        print("Generated and wrote:", out_filename)
        
    # Trigger terminal typewriter presentation
    console_typewriter()
