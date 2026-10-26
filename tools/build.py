#!/usr/bin/env python3
"""
Generates every graphic used by the profile README into ../assets.

    python3 tools/build.py

Design system: "paper & ink". Cream paper, thick ink outlines, hard offset
shadows, four loud accents. Pure SVG, no external services, no fonts to load.
"""
import math
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

INK = "#141414"
PAPER = "#F5EFE0"
WHITE = "#FFFDF6"
TOMATO = "#FF5B3A"
MUSTARD = "#FFC83D"
MINT = "#7BDCB5"
LILAC = "#C9B6FF"

DISPLAY = "'Arial Black','Helvetica Neue',Arial,sans-serif"
MONO = "'Courier New',Courier,monospace"


# ───────────────────────────── helpers ─────────────────────────────
def e(s):
    return escape(s)


def text(x, y, s, size=18, fill=INK, weight=700, family=MONO, anchor="start",
         ls=None, tl=None, extra=""):
    a = (f'x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
         f'font-weight="{weight}" fill="{fill}"')
    if anchor != "start":
        a += f' text-anchor="{anchor}"'
    if ls:
        a += f' letter-spacing="{ls}"'
    if tl:
        a += f' textLength="{tl}" lengthAdjust="spacingAndGlyphs"'
    return f'<text {a} {extra}>{e(s)}</text>'


def rect(x, y, w, h, fill, stroke=None, sw=4, dash=None, rx=0, extra=""):
    a = f'x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"'
    if rx:
        a += f' rx="{rx}"'
    if stroke:
        a += f' stroke="{stroke}" stroke-width="{sw}"'
    if dash:
        a += f' stroke-dasharray="{dash}"'
    return f'<rect {a} {extra}/>'


def card(x, y, w, h, fill, shadow=INK, off=8, sw=4, dash=None, rx=0):
    return (rect(x + off, y + off, w, h, shadow, rx=rx)
            + rect(x, y, w, h, fill, INK, sw, dash, rx))


def star(cx, cy, big, small, n):
    pts = []
    for i in range(n * 2):
        r = big if i % 2 == 0 else small
        ang = math.pi * i / n - math.pi / 2
        pts.append(f"{cx + r * math.cos(ang):.1f},{cy + r * math.sin(ang):.1f}")
    return " ".join(pts)


def dots_defs(pid="dots"):
    return (f'<pattern id="{pid}" width="22" height="22" patternUnits="userSpaceOnUse">'
            f'<circle cx="3" cy="3" r="1.6" fill="{INK}" fill-opacity="0.14"/></pattern>')


def svg(w, h, body, title, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-label="{e(title)}">'
            f'<title>{e(title)}</title><defs>{defs}</defs>{body}</svg>\n')


def ticker(cid, x, y, w, h, s, unit, size, bg, fg, dur=14):
    copies = int(math.ceil((w + unit) / unit)) + 1
    base = y + h / 2 + size * 0.35
    items = "".join(
        text(x + i * unit, base, s, size, fg, 900, DISPLAY, tl=unit, extra='xml:space="preserve"')
        for i in range(copies))
    return (f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>'
            + rect(x, y, w, h, bg)
            + f'<g clip-path="url(#{cid})"><g>'
              f'<animateTransform attributeName="transform" type="translate" '
              f'from="0 0" to="{-unit} 0" dur="{dur}s" repeatCount="indefinite"/>'
              f'{items}</g></g>')


def tilted(x, y, w, h, deg, fill, label, size=28):
    cx, cy = x + w / 2, y + h / 2
    return (f'<g transform="rotate({deg} {cx} {cy})">'
            + card(x, y, w, h, fill, INK, 7)
            + text(cx, cy + size * 0.35, label, size, INK, 900, DISPLAY,
                   anchor="middle", tl=round(w * 0.82))
            + '</g>')


# ───────────────────────────── hero ─────────────────────────────
def hero():
    W, H = 1200, 440
    b = []
    b.append(rect(0, 0, W, H, PAPER))
    b.append(rect(0, 0, W, H, "url(#dots)"))

    b.append(text(44, 58, "TALHA33177  /  FULL-STACK  /  DHAKA, BD", 16, INK, 700, MONO, ls=2))
    b.append(card(530, 32, 236, 40, MINT, INK, 4, 3))
    b.append(f'<circle cx="554" cy="52" r="7" fill="{INK}">'
             '<animate attributeName="opacity" values="1;1;0.15;0.15" keyTimes="0;0.5;0.5;1" '
             'dur="1.4s" repeatCount="indefinite"/></circle>')
    b.append(text(574, 58, "OPEN TO COLLABS", 16, INK, 900, MONO, ls=1))

    # name with hard tomato shadow
    for dx, dy, col in ((7, 7, TOMATO), (0, 0, INK)):
        b.append(text(44 + dx, 190 + dy, "TALHA", 128, col, 900, DISPLAY, tl=470))
        b.append(text(44 + dx, 318 + dy, "AHMED", 128, col, 900, DISPLAY, tl=520))

    b.append(text(46, 362, "Full-Stack Software Engineer  ·  .NET  ·  React  ·  Clean Architecture",
                  21, INK, 700, MONO))

    b.append(tilted(690, 88, 240, 72, -5, TOMATO, ".NET 10"))
    b.append(tilted(840, 170, 300, 72, 3, MUSTARD, "ASP.NET CORE"))
    b.append(tilted(700, 246, 330, 72, -3, MINT, "REACT + BLAZOR"))

    # rotating starburst
    cx, cy = 1090, 112
    b.append(f'<g><animateTransform attributeName="transform" type="rotate" '
             f'from="0 {cx} {cy}" to="360 {cx} {cy}" dur="30s" repeatCount="indefinite"/>'
             f'<polygon points="{star(cx + 6, cy + 6, 68, 54, 14)}" fill="{INK}"/>'
             f'<polygon points="{star(cx, cy, 68, 54, 14)}" fill="{LILAC}" stroke="{INK}" '
             f'stroke-width="4" stroke-linejoin="round"/></g>')
    b.append(text(cx, cy - 2, "3 SITES", 21, INK, 900, DISPLAY, anchor="middle", tl=84))
    b.append(text(cx, cy + 24, "LIVE", 21, INK, 900, DISPLAY, anchor="middle", tl=50))

    b.append(ticker("hero-tick", 0, 388, W, 52,
                    "SHIP IT CLEAN  //  KEEP IT RUNNING  //  ", 760, 24, INK, MUSTARD, 14))
    b.append(rect(3, 3, W - 6, H - 6, "none", INK, 6))
    return svg(W, H, "".join(b), "Talha Ahmed, Full-Stack Software Engineer from Dhaka, Bangladesh",
               dots_defs())


# ───────────────────────────── section headings ─────────────────────────────
def heading(n, title, color):
    W, H = 1200, 80
    b = [card(4, 4, 1180, 64, PAPER, color, 8, 4)]
    b.append(rect(4, 4, 96, 64, INK))
    b.append(text(52, 50, n, 36, PAPER, 900, DISPLAY, anchor="middle"))
    b.append(text(124, 51, title, 38, INK, 900, DISPLAY))
    line_x = 124 + len(title) * 36 + 26
    b.append(f'<line x1="{line_x}" y1="36" x2="1120" y2="36" stroke="{INK}" stroke-width="4" '
             f'stroke-dasharray="2 12" stroke-linecap="round"/>')
    b.append(f'<circle cx="1146" cy="36" r="17" fill="{color}" stroke="{INK}" stroke-width="4"/>')
    return svg(W, H, "".join(b), f"{n} {title}")


# ───────────────────────────── now ─────────────────────────────
def now():
    W, H = 1200, 232
    cards = [
        (TOMATO, "NOW BUILDING", "ONEDROP", ["Multi-tenant courier", "platform on .NET 10"]),
        (MUSTARD, "NOW LEARNING", "MICROSERVICES", ["Cloud architecture and", "microservices"]),
        (MINT, "OPEN TO", "C# / .NET", ["Open-source collabs in", "C# and .NET"]),
    ]
    b = []
    for i, (col, tag, big, sub) in enumerate(cards):
        x, y = 12 + i * 396, 14
        b.append(card(x, y, 360, 196, col, INK, 9))
        tw = len(tag) * 10 + 28
        b.append(rect(x + 20, y + 20, tw, 30, INK))
        b.append(text(x + 20 + tw / 2, y + 41, tag, 15, PAPER, 700, MONO, anchor="middle", ls=1.5))
        b.append(text(x + 20, y + 106, big, 36, INK, 900, DISPLAY, tl=min(len(big) * 27, 316)))
        for j, line in enumerate(sub):
            b.append(text(x + 20, y + 142 + j * 25, line, 18, INK, 700, MONO))
    return svg(W, H, "".join(b), "Now building OneDrop, learning cloud architecture, open to C# and .NET collabs")


# ───────────────────────────── project cards ─────────────────────────────
def chip(x, y, label):
    w = len(label) * 8.8 + 24
    return (rect(x, y, w, 30, WHITE, INK, 3, rx=15)
            + text(x + w / 2, y + 20, label, 14, INK, 700, MONO, anchor="middle")), w


def project(num, title, accent, pill, pill_fill, tag_lines, url, url_link, bullets, chips,
            button, dashed=False, alt=""):
    W, H = 600, 382
    b = [card(10, 10, 570, 352, WHITE, accent, 10, 4, "14 9" if dashed else None)]
    b.append(rect(10, 10, 570, 56, accent, INK, 4))
    b.append(text(30, 46, f"{num} / {title}", 20, INK, 700, MONO, ls=2))

    pw = len(pill) * 11 + 46
    px = 562 - pw
    b.append(rect(px, 22, pw, 32, pill_fill, INK, 3, rx=16))
    b.append(f'<circle cx="{px + 20}" cy="38" r="6" fill="{INK}">'
             '<animate attributeName="opacity" values="1;1;0.2;0.2" keyTimes="0;0.5;0.5;1" '
             'dur="1.4s" repeatCount="indefinite"/></circle>')
    b.append(text(px + 34, 44, pill, 16, INK, 900, MONO, ls=1))

    b.append(text(30, 128, title, 46, INK, 900, DISPLAY, tl=len(title) * 36))
    for i, line in enumerate(tag_lines):
        b.append(text(30, 162 + i * 22, line, 18, "#3a3a3a", 700, MONO))
    b.append(text(30, 212, url, 16, INK, 700, MONO,
                  extra='text-decoration="underline"' if url_link else ""))
    for i, line in enumerate(bullets):
        b.append(text(30, 248 + i * 26, "→  " + line, 17, INK, 700, MONO))

    x = 30
    for c in chips:
        s, w = chip(x, 318, c)
        b.append(s)
        x += w + 10

    bw = len(button) * 12 + 40
    bx = 560 - bw
    b.append(rect(bx + 4, 316, bw, 40, accent, rx=0))
    b.append(rect(bx, 312, bw, 40, INK))
    b.append(text(bx + bw / 2, 338, button, 17, PAPER, 900, MONO, anchor="middle", ls=1))
    return svg(W, H, "".join(b), alt or title)


# ───────────────────────────── stack ─────────────────────────────
def stack():
    W = 1200
    rows = [
        ("BACKEND", TOMATO, ["C#", ".NET 10", "ASP.NET Core", "Blazor", "SQL Server"]),
        ("FRONTEND", MUSTARD, ["React", "TypeScript", "JavaScript", "HTML", "CSS", "Tailwind", "Bootstrap"]),
        ("PRACTICES", MINT, ["Clean Architecture", "Multi-tenancy", "REST APIs"]),
        ("TOOLING", LILAC, ["Git", "GitHub", "Visual Studio", "VS Code", "Postman"]),
    ]
    x_label, chip_x0, max_x = 32, 232, 1150
    y = 28
    parts = []
    for label, col, items in rows:
        lines, x = [[]], chip_x0
        for it in items:
            w = len(it) * 10.9 + 30
            if x + w > max_x and lines[-1]:
                lines.append([])
                x = chip_x0
            lines[-1].append((x, w, it))
            x += w + 14
        rowh = len(lines) * 58 + 14
        parts.append(card(x_label, y + 4, 168, 46, col, INK, 5, 4))
        parts.append(text(x_label + 84, y + 34, label, 19, INK, 900, DISPLAY, anchor="middle",
                          tl=min(len(label) * 15, 140)))
        for li, line in enumerate(lines):
            for (cx_, w, it) in line:
                top = y + 6 + li * 58
                parts.append(rect(cx_ + 4, top + 4, w, 42, col, rx=21))
                parts.append(rect(cx_, top, w, 42, WHITE, INK, 3, rx=21))
                parts.append(text(cx_ + w / 2, top + 28, it, 18, INK, 700, MONO, anchor="middle"))
        y += rowh
        parts.append(f'<line x1="{x_label}" y1="{y - 2}" x2="{W - 32}" y2="{y - 2}" stroke="{INK}" '
                     f'stroke-opacity="0.35" stroke-width="2" stroke-dasharray="3 8" stroke-linecap="round"/>')
    H = y + 20
    body = (rect(0, 0, W, H, PAPER) + rect(0, 0, W, H, "url(#dots4)") + "".join(parts)
            + rect(3, 3, W - 6, H - 6, "none", INK, 6))
    return svg(W, H, body, "Tech stack: C#, .NET 10, ASP.NET Core, Blazor, SQL Server, React, TypeScript, "
                           "Tailwind, Bootstrap, Git, Visual Studio", dots_defs("dots4"))


# ───────────────────────────── footer + buttons ─────────────────────────────
def footer():
    W, H = 1200, 350
    b = [rect(0, 0, W, H, TOMATO), rect(0, 0, W, H, "url(#dots5)")]
    b.append(text(44 + 6, 140 + 6, "LET'S BUILD", 100, INK, 900, DISPLAY, tl=640))
    b.append(text(44, 140, "LET'S BUILD", 100, PAPER, 900, DISPLAY, tl=640))
    b.append(text(44 + 6, 240 + 6, "SOMETHING.", 100, INK, 900, DISPLAY, tl=700))
    b.append(text(44, 240, "SOMETHING.", 100, PAPER, 900, DISPLAY, tl=700))

    b.append('<g transform="rotate(-6 975 132)">'
             + card(810, 72, 330, 120, MINT, INK, 8, 4)
             + text(975, 118, "OPEN-SOURCE COLLABS", 22, INK, 900, DISPLAY, anchor="middle", tl=290)
             + text(975, 156, "IN C# / .NET", 30, INK, 900, DISPLAY, anchor="middle", tl=200)
             + '</g>')
    b.append(ticker("foot-tick", 0, 290, W, 54,
                    "SHIP IT CLEAN  //  KEEP IT RUNNING  //  ", 760, 24, INK, MUSTARD, 16))
    cx, cy = 1100, 240
    b.append(f'<g><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" '
             f'to="-360 {cx} {cy}" dur="26s" repeatCount="indefinite"/>'
             f'<polygon points="{star(cx + 6, cy + 6, 62, 50, 12)}" fill="{INK}"/>'
             f'<polygon points="{star(cx, cy, 62, 50, 12)}" fill="{MUSTARD}" stroke="{INK}" '
             f'stroke-width="4" stroke-linejoin="round"/></g>')
    b.append(text(cx, cy + 7, "SAY HI", 20, INK, 900, DISPLAY, anchor="middle", tl=70))
    b.append(rect(3, 3, W - 6, H - 6, "none", INK, 6))
    return svg(W, H, "".join(b), "Let's build something. Open to open-source collabs in C# and .NET",
               dots_defs("dots5"))


def button(glyph, label, value, color):
    W, H = 400, 108
    b = [card(8, 8, 376, 84, WHITE, color, 8, 4)]
    b.append(rect(8, 8, 84, 84, color, INK, 4))
    b.append(text(50, 66, glyph, 40, INK, 900, DISPLAY, anchor="middle"))
    b.append(text(110, 40, label, 14, "#3a3a3a", 700, MONO, ls=2))
    b.append(text(110, 70, value, 17, INK, 900, MONO))
    return svg(W, H, "".join(b), f"{label}: {value}")


# ───────────────────────────── build ─────────────────────────────
def main():
    files = {
        "hero.svg": hero(),
        "h1-now.svg": heading("01", "NOW", TOMATO),
        "h2-shipped.svg": heading("02", "SHIPPED", MUSTARD),
        "h3-toolbox.svg": heading("03", "TOOLBOX", MINT),
        "h4-sayhi.svg": heading("04", "SAY HI", TOMATO),
        "now.svg": now(),
        "p-grabity.svg": project(
            "01", "GRABITY", TOMATO, "LIVE", MINT,
            ["Gadget & accessories e-commerce", "for Bangladesh"],
            "grabity.bdcorex.com", True,
            ["Consumer storefront", "Full admin panel", "Real-time inventory"],
            ["ASP.NET CORE", "REACT"], "VISIT SITE",
            alt="Grabity: gadget and accessories e-commerce for Bangladesh, live"),
        "p-corex.svg": project(
            "02", "CORE X", MUSTARD, "LIVE", MINT,
            ["Fashion brand storefront"],
            "bdcorex.com", True,
            ["Modern elegance x traditional craft", "Brand-first product showcase", "Runs on its own domain"],
            ["FASHION", "STOREFRONT"], "VISIT SITE",
            alt="CORE X: fashion brand storefront, live"),
        "p-portfolio.svg": project(
            "03", "PORTFOLIO", LILAC, "LIVE", MINT,
            ["Personal site, pixel-perfect UI"],
            "talha.bdcorex.com", True,
            ["Projects & experience", "Responsive, fast, clean", "Front + back end by me"],
            ["ASP.NET CORE", "REACT"], "VISIT SITE",
            alt="Portfolio: personal site with a pixel-perfect UI, live"),
        "p-onedrop.svg": project(
            "04", "ONEDROP", MINT, "BUILDING", MUSTARD,
            ["Multi-tenant courier platform", "on .NET 10"],
            "in progress, not live yet", False,
            ["Many shops, one rider", "Merged orders, one drop-off", "Centralized routing"],
            [".NET 10", "MULTI-TENANT"], "SEE REPO", dashed=True,
            alt="OneDrop: multi-tenant courier platform on .NET 10, in progress"),
        "stack.svg": stack(),
        "footer.svg": footer(),
        "btn-email.svg": button("@", "EMAIL ME", "talha33177.net@gmail.com", TOMATO),
        "btn-portfolio.svg": button("W", "PORTFOLIO", "talha.bdcorex.com", MUSTARD),
        "btn-linkedin.svg": button("in", "LINKEDIN", "let's connect", MINT),
    }
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
    print(f"wrote {len(files)} files to {OUT}")


if __name__ == "__main__":
    main()
