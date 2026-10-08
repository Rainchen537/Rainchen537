#!/usr/bin/env python3
"""Build the English pixel profile. Python standard library; no network access."""
from pathlib import Path
import base64
import html
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/pixel'
SOURCE = OUT / 'source'
BG, PANEL, LINE = '#0a0d19', '#101628', '#2c3855'
INK, MUTED, PURPLE, CYAN = '#edf2ff', '#a0adc5', '#ae93ff', '#72e4fa'
FONT = '-apple-system,BlinkMacSystemFont,Segoe UI,Arial,sans-serif'
# Five-column bitmap alphabet: vector paths keep headings identical on GitHub.
GLYPHS = dict(zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', [
 '01110 10001 10001 11111 10001 10001 10001',
 '11110 10001 10001 11110 10001 10001 11110',
 '01111 10000 10000 10000 10000 10000 01111',
 '11110 10001 10001 10001 10001 10001 11110',
 '11111 10000 10000 11110 10000 10000 11111',
 '11111 10000 10000 11110 10000 10000 10000',
 '01111 10000 10000 10111 10001 10001 01111',
 '10001 10001 10001 11111 10001 10001 10001',
 '11111 00100 00100 00100 00100 00100 11111',
 '00111 00010 00010 00010 10010 10010 01100',
 '10001 10010 10100 11000 10100 10010 10001',
 '10000 10000 10000 10000 10000 10000 11111',
 '10001 11011 10101 10101 10001 10001 10001',
 '10001 11001 10101 10011 10001 10001 10001',
 '01110 10001 10001 10001 10001 10001 01110',
 '11110 10001 10001 11110 10000 10000 10000',
 '01110 10001 10001 10001 10101 10010 01101',
 '11110 10001 10001 11110 10100 10010 10001',
 '01111 10000 10000 01110 00001 00001 11110',
 '11111 00100 00100 00100 00100 00100 00100',
 '10001 10001 10001 10001 10001 10001 01110',
 '10001 10001 10001 10001 10001 01010 00100',
 '10001 10001 10001 10101 10101 10101 01010',
 '10001 10001 01010 00100 01010 10001 10001',
 '10001 10001 01010 00100 00100 00100 00100',
 '11111 00001 00010 00100 01000 10000 11111',
 '01110 10001 10011 10101 11001 10001 01110',
 '00100 01100 00100 00100 00100 00100 01110',
 '01110 10001 00001 00010 00100 01000 11111',
 '11110 00001 00001 01110 00001 00001 11110',
 '00010 00110 01010 10010 11111 00010 00010',
 '11111 10000 10000 11110 00001 00001 11110',
 '01110 10000 10000 11110 10001 10001 01110',
 '11111 00001 00010 00100 01000 01000 01000',
 '01110 10001 10001 01110 10001 10001 01110',
 '01110 10001 10001 01111 00001 00001 01110',
]))
GLYPHS.update({
 ' ': '00000 '*7, '.': '00000 00000 00000 00000 00000 00110 00110',
 '/': '00001 00001 00010 00100 01000 10000 10000',
 '-': '00000 00000 00000 11111 00000 00000 00000',
 '>': '10000 01000 00100 00010 00100 01000 10000',
})

PROJECTS = [
 dict(id='bnbu', title='BNBU.ME', repo='BNBUME-client', color=PURPLE,
      desc='Timetables, deadlines, mail and campus tools.',
      note='Unofficial client / Desktop preview',
      tech='Flutter / Dart', platform='iOS / Android / macOS / Windows',
      url='https://bnbu.me/', link='Website'),
 dict(id='y-clip', title='Y-Clip', repo='Y-Clip', color='#f19fd5',
      desc='Clipboard history for macOS.', tech='Swift / AppKit', platform='macOS'),
 dict(id='y-dock', title='Y-Dock', repo='Y-Dock', color=CYAN,
      desc='Dock previews and window switching.', tech='Swift / AppKit', platform='macOS'),
 dict(id='y-keys', title='Y-Keys', repo='Y-Keys', color='#96edc2',
      desc='Shortcut reference for macOS.', tech='Swift / AppKit', platform='macOS'),
 dict(id='landirect', title='Dungeons2-LanDirect', repo='Dungeons2-LanDirect', color='#edce8b',
      desc='A LAN mod prototype for Minecraft Dungeons II.',
      note='Experimental / Multiplayer unverified', tech='C# / .NET', platform='Windows',
      url='https://github.com/Rainchen537/Dungeons2-LanDirect#readme', link='Compatibility'),
]


def px(value, x, y, size=2, color=INK):
    d = []
    for i, c in enumerate(value.upper()):
        for row, bits in enumerate(GLYPHS[c].split()):
            for col, bit in enumerate(bits):
                if bit == '1':
                    d.append(f'M{x+(i*6+col)*size:g} {y+row*size:g}h{size:g}v{size:g}h{-size:g}Z')
    return f'<path d="{"".join(d)}" fill="{color}"/>'


def text(value, x, y, size=18, color=MUTED, weight=400, anchor='start'):
    return f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{html.escape(value)}</text>'


def panel(x, y, w, h, fill=PANEL, cut=10):
    return f'<path d="M{x+cut} {y}H{x+w-cut}V{y+cut}H{x+w}V{y+h-cut}H{x+w-cut}V{y+h}H{x+cut}V{y+h-cut}H{x}V{y+cut}H{x+cut}Z" fill="{fill}" stroke="{LINE}"/>'


def image(path, x, y, w, h):
    data = base64.b64encode(path.read_bytes()).decode()
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="data:image/png;base64,{data}"/>'


def icon(key, x, y, size):
    if key == 'bnbu':
        return image(ROOT / 'assets/bnbu.png', x, y, size, size)
    raw = (SOURCE / f'{key}.svg').read_text()
    inner = raw[raw.index('>')+1:raw.rindex('</svg>')]
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="35 20 145 150">{inner}</svg>'


def svg(w, h, title, body):
    title = html.escape(title, quote=True)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{title}"><title>{title}</title>{body}</svg>\n'


def write(name, content):
    ET.fromstring(content)
    (OUT / name).write_text(content)


def card(p, mobile):
    w = 600 if mobile else 1120
    has_note = 'note' in p
    h = (268 if has_note else 238) if mobile else (196 if has_note else 166)
    s = panel(1, 1, w-2, h-2)
    s += f'<path d="M22 1H112" stroke="{p["color"]}" stroke-width="2"/>'
    if mobile:
        s += icon(p['id'], 22, 22, 82)
        title_size = 2.8 if p['id']=='landirect' else 4
        s += px(p['title'], 128, 49, title_size)
        s += text(p['desc'], 26, 140, 22)
        if has_note:
            s += text(p['note'], 26, 175, 19, '#8290aa')
        s += text(p['tech'], 26, h-40, 19, p['color'])
        s += text(p['platform'], 26, h-16, 18, '#8290aa')
    else:
        s += icon(p['id'], 32, (h-104)/2, 104)
        s += px(p['title'], 174, 31, 3)
        s += text(p['desc'], 174, 90, 18)
        if has_note:
            s += text(p['note'], 174, 121, 15, '#8290aa')
        s += text(p['tech'], 174, h-25, 15, p['color'])
        s += text(p['platform'], w-30, h-25, 15, '#8290aa', anchor='end')
    return svg(w, h, f'{p["title"]}: {p["desc"]}', s)


def section(label, mobile):
    w, h = (600, 68) if mobile else (1120, 68)
    s = f'<rect width="{w}" height="{h}" fill="{BG}"/>'
    s += px('>', 12, 26, 2, PURPLE) + px(label, 42, 22, 3 if mobile else 2.5)
    s += f'<path d="M0 64H{w}" stroke="{LINE}"/>'
    return svg(w, h, label.title(), s)


def stack(mobile):
    w, h = (600, 244) if mobile else (1120, 126)
    gap = 12
    cols = 2 if mobile else 4
    cw = (w-gap*(cols-1))/cols
    s = ''
    items = [('Swift / AppKit', 'macOS', PURPLE), ('Dart / Flutter', 'Cross-platform', CYAN),
             ('C# / .NET', 'Game mods', '#96edc2'), ('Python / Git / Shell', 'Tooling', '#edce8b')]
    for i,(name,domain,color) in enumerate(items):
        x, y = (i%cols)*(cw+gap), (i//cols)*124
        s += panel(x+1,y+1,cw-2,112)
        s += f'<path d="M{x+20} {y+1}h40" stroke="{color}" stroke-width="2"/>'
        s += text(name,x+20,y+48,22 if mobile else 18,INK,500)
        s += text(domain,x+20,y+82,19 if mobile else 15,color)
    return svg(w,h,'Swift / AppKit, Dart / Flutter, C# / .NET, Python / Git / Shell',s)


def picture(name, alt):
    return f'<picture>\n  <source media="(max-width: 600px)" srcset="./assets/pixel/{name}-mobile.svg" />\n  <img src="./assets/pixel/{name}.svg" width="1120" alt="{html.escape(alt,quote=True)}" />\n</picture>'


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    for name in ('hero.gif','hero-mobile.gif','hero-poster.png','hero-mobile-poster.png'):
        if not (OUT/name).is_file():
            raise FileNotFoundError(f'{name}: run tools/trim_confirmed_animation.py with Pillow first')
    for mobile in (False,True):
        suffix='-mobile' if mobile else ''
        write(f'section-stack{suffix}.svg',section('TECH STACK',mobile))
        write(f'section-projects{suffix}.svg',section('SELECTED PROJECTS',mobile))
        write(f'stack{suffix}.svg',stack(mobile))
        for p in PROJECTS: write(f'project-{p["id"]}{suffix}.svg',card(p,mobile))
        w=600 if mobile else 1120
        write(f'footer{suffix}.svg',svg(w,64,'Rainchen / GitHub',f'<path d="M0 1H{w}" stroke="{LINE}"/>'+px('RAINCHEN / GITHUB',12,28,2,'#73829d')))
    parts=['<!-- Generated by tools/build_readme.py. Edit the generator and source artwork. -->',
        '<p align="center">\n<picture>\n  <source media="(prefers-reduced-motion: reduce) and (max-width: 600px)" srcset="./assets/pixel/hero-mobile-poster.png" />\n  <source media="(prefers-reduced-motion: reduce)" srcset="./assets/pixel/hero-poster.png" />\n  <source media="(max-width: 600px)" srcset="./assets/pixel/hero-mobile.gif" />\n  <img src="./assets/pixel/hero.gif" width="1120" alt="Rainchen / Li Xingchen — independent developer. A pixel portrait with ENTJ, followed by five projects in the original particle animation." />\n</picture>\n</p>',
        '<p align="center"><b>Rainchen / Li Xingchen</b><br /><sub>Independent developer</sub></p>',
        '<p align="center"><a href="#tech-stack">Tech stack</a> · <a href="#selected-projects">Projects</a> · <a href="https://bnbu.me/">BNBU.ME</a> · <a href="./assets/pixel/hero-poster.png">Still cover</a></p>',
        '<a name="tech-stack"></a>',picture('section-stack','Tech stack'),
        picture('stack','Swift / AppKit, Dart / Flutter, C# / .NET, Python / Git / Shell'),
        '<a name="selected-projects"></a>',picture('section-projects','Selected projects')]
    for p in PROJECTS:
        repo=f'https://github.com/Rainchen537/{p["repo"]}'
        parts.append(f'<a href="{repo}">\n'+picture('project-'+p['id'],p['title']+': '+p['desc']+' '+p.get('note',''))+'\n</a>')
        url=p.get('url',repo+'/releases'); label=p.get('link','Releases')
        parts.append(f'<p align="right"><sub><a href="{repo}">Source</a> · <a href="{url}">{label}</a></sub></p>')
    parts.append(picture('footer','Rainchen / GitHub'))
    parts.append('<details>\n<summary>Text version</summary>\n<p><b>Rainchen / Li Xingchen</b> — Independent developer. ENTJ is a self-described personality label.</p>')
    for p in PROJECTS:
        parts.append(f'<p><a href="https://github.com/Rainchen537/{p["repo"]}"><b>{p["title"]}</b></a><br />{p["desc"]}<br /><sub>{p["tech"]} / {p["platform"]}'+(f'<br />{p["note"]}' if 'note' in p else '')+'</sub></p>')
    parts.append('</details>')
    (ROOT/'README.md').write_text('\n\n'.join(parts)+'\n')
    print('Generated README.md and 18 SVG assets; approved GIF animation left untouched.')


if __name__=='__main__': main()
