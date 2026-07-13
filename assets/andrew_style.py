#!/usr/bin/env python3
"""
Build an Andrew6rant-style neofetch profile SVG:
  - ASCII self-portrait on the left (fully visible, static)
  - terminal info panel on the right (typed-look, static reveal)
Generates dark_mode.svg and light_mode.svg (self-contained, SMIL).

Drop your photo next to this script as "portrait.jpg" (or change
PORTRAIT_PATH below) and re-run. If no photo is found, a placeholder
pattern is used so you can preview the layout.
"""
import os
from PIL import Image, ImageOps, ImageEnhance

# ---- 1. ASCII portrait ------------------------------------------------
PORTRAIT_PATH = "assets/portrait.png"   # <-- put your photo here
ASCII_COLS = 56
ASCII_FS = 13
ASCII_LH = 14
ASCII_CW = 7.8
RAMP = " .'`^\",:;Il!i~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"


def portrait_rows(path, cols=ASCII_COLS):
    im = Image.open(path)
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        bg.paste(im, (0, 0), im.convert("RGBA"))
        im = bg.convert("L")
    else:
        im = im.convert("L")
    im = im.point(lambda v: int(((v / 255.0) ** 0.55) * 255))  # lift shadows
    im = ImageOps.autocontrast(im, cutoff=2)
    im = ImageEnhance.Contrast(im).enhance(1.25)
    w, h = im.size
    rows = max(1, int(cols * (h / w) * (ASCII_CW / ASCII_LH)))
    im = im.resize((cols, rows))
    px = im.load()
    n = len(RAMP) - 1
    out = []
    for y in range(rows):
        out.append("".join(RAMP[int((255 - px[x, y]) / 255 * n)]
                            for x in range(cols)).rstrip())
    return out


def placeholder_rows(cols=ASCII_COLS, rows=34):
    """Used only when no portrait.jpg is present yet, so you can preview layout."""
    out = []
    box = [
        "".ljust(cols),
        ("+" + "-" * (cols - 2) + "+"),
    ]
    mid_lines = rows - 6
    for i in range(mid_lines):
        if i == mid_lines // 3:
            line = "|" + "DROP  portrait.jpg  HERE".center(cols - 2) + "|"
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
    ("kv", (["OS"], "macOS - Linux - Windows")),
    ("kv", (["Host"], "Full-Stack Web & Mobile Dev")),
    ("kv", (["Kernel"], "React - Next.js - Flutter")),
    ("kv", (["IDE"], "VSCode, Claude Code")),
    ("blank", None),
    ("kv", (["Languages", "Web"], "TypeScript, JavaScript, Node.js")),
    ("kv", (["Languages", "Mobile"], "Flutter, Dart")),
    ("kv", (["Languages", "Backend"], "Firebase, Supabase")),
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
THEMES = {
    "dark": dict(bg="#0a1128", text="#ffffff", key="#ffffff",
                 value="#4169e1", cc="#5a6ba8", add="#6d8bff", dele="#f85149"),
    "light": dict(bg="#ffffff", text="#0a1128", key="#0a1128",
                  value="#4169e1", cc="#8a97c4", add="#2947b3", dele="#cf222e"),
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def leader(prefix_len):
    return max(1, VALUE_COL - prefix_len)


def kv_line(keys, value):
    key_txt = ".".join(keys)
    prefix_len = 2 + len(key_txt) + 1
    dots = leader(prefix_len)
    key_spans = ('<tspan class="key">'
                 + '</tspan>.<tspan class="key">'.join(esc(k) for k in keys)
                 + '</tspan>')
    return (f'<tspan class="cc">. </tspan>{key_spans}'
            f'<tspan class="cc">:</tspan>'
            f'<tspan class="cc"> {"." * dots} </tspan>'
            f'<tspan class="value">{esc(value)}</tspan>')


CW = 10.0
INFO_X = 500
W, H = 1120, 540


def build_svg(theme_name):
    t = THEMES[theme_name]
    parts = []
    parts.append(
        f"<svg xmlns='http://www.w3.org/2000/svg' "
        f"font-family=\"Consolas,'DejaVu Sans Mono',monospace\" "
        f"width='{W}px' height='{H}px' font-size='16px'>")
    parts.append(
        "<style>"
        f".key{{fill:{t['key']};}} .value{{fill:{t['value']};}} "
        f".cc{{fill:{t['cc']};}} .add{{fill:{t['add']};}} "
        f".del{{fill:{t['dele']};}} "
        "text,tspan{white-space:pre;} "
        "</style>")
    parts.append(f"<rect width='{W}px' height='{H}px' fill='{t['bg']}' rx='15'/>")

    parts.append(f"<text x='15' y='24' fill='{t['text']}' font-size='{ASCII_FS}px'>")
    y = 24
    for row in ASCII_ROWS:
        parts.append(f"<tspan x='15' y='{y}'>{esc(row)}</tspan>")
        y += ASCII_LH
    parts.append("</text>")

    px = INFO_X
    y = 30
    n_dash = int((W - px) / CW) - 16
    for kind, payload in INFO:
        if kind == "header":
            dash = "-" * max(4, n_dash - len(payload))
            body = (f"<tspan x='{px}' y='{y}' fill='{t['text']}'>{esc(payload)}"
                    f"</tspan><tspan class='cc'> -{dash}-</tspan>")
        elif kind == "section":
            dash = "-" * max(4, n_dash - len(payload) - 2)
            body = (f"<tspan x='{px}' y='{y}' fill='{t['text']}'>- {esc(payload)}"
                    f"</tspan><tspan class='cc'> -{dash}-</tspan>")
        elif kind == "blank":
            body = f"<tspan x='{px}' y='{y}' class='cc'>. </tspan>"
        elif kind == "kv":
            keys, value = payload
            body = f"<tspan x='{px}' y='{y}'>{kv_line(keys, value)}</tspan>"
        elif kind == "stats1":
            body = (f"<tspan x='{px}' y='{y}'><tspan class='cc'>. </tspan>"
                    f"<tspan class='key'>Repos</tspan>"
                    f"<tspan class='cc'> ..... </tspan>"
                    f"<tspan class='value'>29</tspan>"
                    f"<tspan class='cc'> | </tspan>"
                    f"<tspan class='key'>Stars</tspan>"
                    f"<tspan class='cc'> ..... </tspan>"
                    f"<tspan class='value'>15</tspan>"
                    f"<tspan class='cc'> | </tspan>"
                    f"<tspan class='key'>Followers</tspan>"
                    f"<tspan class='cc'> . </tspan>"
                    f"<tspan class='value'>6</tspan></tspan>")
        parts.append(f"<text>{body}</text>")
        y += 20

    prompt_y = y + 8
    parts.append(
        f"<text x='{px}' y='{prompt_y}' fill='{t['add']}'>vartik@github</text>"
        f"<text x='{px + 13 * int(CW)}' y='{prompt_y}' fill='{t['text']}'>:~$</text>")
    cur_x = px + 17 * int(CW)
    parts.append(
        f"<rect x='{cur_x}' y='{prompt_y - 13}' width='{int(CW)}' height='17' "
        f"fill='{t['add']}'>"
        f"<animate attributeName='opacity' values='1;1;0;0' dur='1.1s' "
        f"keyTimes='0;0.5;0.5;1' repeatCount='indefinite'/></rect>")
    parts.append("</svg>")
    return "\n".join(parts)


for name in ("dark", "light"):
    out = f"{name}_mode.svg"
    with open(out, "w", encoding="utf-8") as f:
        f.write(build_svg(name))
    print("wrote", out)
