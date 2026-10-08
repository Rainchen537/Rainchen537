#!/usr/bin/env python3
"""Build the English pixel profile. Python standard library; no network access."""
from pathlib import Path
import html
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/pixel'
SOURCE = OUT / 'source'
BG, PANEL, LINE = '#0a0d19', '#101628', '#2c3855'
PIXEL_PAPER = '#0d1117'
INK, MUTED, PURPLE, CYAN = '#edf2ff', '#a0adc5', '#ae93ff', '#72e4fa'
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
 '#': '01010 01010 11111 01010 11111 01010 01010',
 '+': '00000 00100 00100 11111 00100 00100 00000',
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


def icon(key, x, y, size):
    if key == 'bnbu':
        return ''
    raw = (SOURCE / f'{key}.svg').read_text()
    inner = raw[raw.index('>')+1:raw.rindex('</svg>')]
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="35 20 145 150">{inner}</svg>'


def svg(w, h, title, body):
    title = html.escape(title, quote=True)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" shape-rendering="crispEdges" role="img" aria-label="{title}"><title>{title}</title>{body}</svg>\n'


def write(name, content):
    ET.fromstring(content)
    (OUT / name).write_text(content)


def dot_rule(w, y, color=LINE):
    return ''.join(f'<rect x="{x}" y="{y}" width="2" height="2" fill="{color}"/>' for x in range(24,w-24,8))


def pixel_label(value, x, y, size, color=INK):
    # One-pixel shadow is part of the letter bitmap, not a UI panel.
    return px(value,x+size,y+size,size,'#18243c')+px(value,x,y,size,color)


def card(p, mobile):
    w=600 if mobile else 1120
    has_note='note' in p
    h=(186 if has_note else 150) if mobile else (142 if has_note else 112)
    s=f'<rect width="{w}" height="{h}" fill="{PIXEL_PAPER}"/>'
    x=26 if p['id']=='bnbu' else (112 if mobile else 122)
    if p['id']!='bnbu': s+=icon(p['id'],28,27,58 if mobile else 60)
    size=(3 if p['id']=='landirect' else 4) if mobile else 3
    s+=pixel_label(p['title'],x,28,size,p['color'])
    topic={'bnbu':'CAMPUS','y-clip':'CLIPBOARD','y-dock':'WINDOWS','y-keys':'SHORTCUTS','landirect':'LAN MOD'}[p['id']]
    if mobile:
        s+=px(topic,x,74,2.5,MUTED)
        s+=px(p['tech'],26,112,2.4,'#73829d')
        platform='IOS / ANDROID / MACOS / WINDOWS' if p['id']=='bnbu' else p['platform']
        s+=px(platform,26,137,2.2,MUTED)
        if has_note:s+=px('UNOFFICIAL / DESKTOP PREVIEW' if p['id']=='bnbu' else 'EXPERIMENTAL / MULTIPLAYER UNVERIFIED',26,164,2.2,'#73829d')
    else:
        s+=px(topic,x,64,2,MUTED)
        s+=px(p['tech'],520,31,2,'#73829d')
        platform='IOS / ANDROID / MACOS / WINDOWS' if p['id']=='bnbu' else p['platform']
        s+=px(platform,520,64,2,MUTED)
        if has_note:s+=px('UNOFFICIAL / DESKTOP PREVIEW' if p['id']=='bnbu' else 'EXPERIMENTAL / MULTIPLAYER UNVERIFIED',x,104,2,'#73829d')
    s+=px('>',w-43,31,2,p['color'])
    return svg(w,h,f'{p["title"]}: {p["desc"]}',s)


def section(label, mobile):
    w,h=(600,84) if mobile else (1120,76)
    s=f'<rect width="{w}" height="{h}" fill="{PIXEL_PAPER}"/>'
    s+=dot_rule(w,14)
    s+=pixel_label(label,26,36,3 if mobile else 2.5,'#edce8b')
    return svg(w, h, label.title(), s)


def stack(mobile):
    w,h=(600,120) if mobile else (1120,72)
    s=f'<rect width="{w}" height="{h}" fill="{PIXEL_PAPER}"/>'
    names=['SWIFT / APPKIT','DART / FLUTTER','C# / .NET','PYTHON / GIT / SHELL']
    colors=[PURPLE,CYAN,'#96edc2','#edce8b']
    for i,(name,color) in enumerate(zip(names,colors)):
        x,y=(26+(i%2)*292,26+(i//2)*46) if mobile else (26+i*278,24)
        size=2.3 if mobile else 2
        s+=px(name,x,y,size,color)
    return svg(w,h,'Swift / AppKit, Dart / Flutter, C# / .NET, Python / Git / Shell',s)


def action(label):
    w=len(label)*12+8
    return svg(w,22,label,px(label,2,3,2,'#73829d'))


def action_image(label,height=14,alt=None):
    key=label.lower().replace(' ','-')
    width=round((len(label)*12+8)*height/22)
    return f'<img src="./assets/pixel/link-{key}.svg" width="{width}" height="{height}" alt="{alt or label.title()}" />'


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
        write(f'footer{suffix}.svg',svg(w,70,'Rainchen / GitHub',f'<rect width="{w}" height="70" fill="{PIXEL_PAPER}"/>'+dot_rule(w,8)+px('RAINCHEN / GITHUB',26,37,2,'#73829d')))
    for label in ('SOURCE','RELEASES','WEBSITE','COMPATIBILITY','TECH STACK','PROJECTS','STILL COVER','TEXT VERSION'):
        write(f'link-{label.lower().replace(" ","-")}.svg',action(label))
    parts=['<!-- Generated by tools/build_readme.py. Edit the generator and source artwork. -->',
        '<p align="center">\n<picture>\n  <source media="(prefers-reduced-motion: reduce) and (max-width: 600px)" srcset="./assets/pixel/hero-mobile-poster.png" />\n  <source media="(prefers-reduced-motion: reduce)" srcset="./assets/pixel/hero-poster.png" />\n  <source media="(max-width: 600px)" srcset="./assets/pixel/hero-mobile.gif" />\n  <img src="./assets/pixel/hero.gif" width="1120" alt="Rainchen / Li Xingchen — independent developer. A pixel portrait with ENTJ, followed by five projects in the original particle animation." />\n</picture>\n</p>',
        '<p align="center"><a href="#tech-stack">'+action_image('TECH STACK',18)+'</a> &nbsp; <a href="#selected-projects">'+action_image('PROJECTS',18)+'</a> &nbsp; <a href="https://bnbu.me/">'+action_image('WEBSITE',18,'BNBU.ME website')+'</a> &nbsp; <a href="./assets/pixel/hero-poster.png">'+action_image('STILL COVER',18)+'</a></p>',
        '<a name="tech-stack"></a>',picture('section-stack','Tech stack'),
        picture('stack','Swift / AppKit, Dart / Flutter, C# / .NET, Python / Git / Shell'),
        '<a name="selected-projects"></a>',picture('section-projects','Selected projects')]
    for p in PROJECTS:
        repo=f'https://github.com/Rainchen537/{p["repo"]}'
        parts.append(f'<a href="{repo}">\n'+picture('project-'+p['id'],p['title']+': '+p['desc']+' '+p.get('note',''))+'\n</a>')
        url=p.get('url',repo+'/releases'); label=p.get('link','Releases')
        parts.append(f'<p align="right"><a href="{repo}">'+action_image('SOURCE')+f'</a> &nbsp; <a href="{url}">'+action_image(label.upper())+'</a></p>')
    parts.append(picture('footer','Rainchen / GitHub'))
    parts.append('<details>\n<summary>'+action_image('TEXT VERSION')+'</summary>\n<p><b>Rainchen / Li Xingchen</b> — Independent developer. ENTJ is a self-described personality label.</p>')
    for p in PROJECTS:
        parts.append(f'<p><a href="https://github.com/Rainchen537/{p["repo"]}"><b>{p["title"]}</b></a><br />{p["desc"]}<br /><sub>{p["tech"]} / {p["platform"]}'+(f'<br />{p["note"]}' if 'note' in p else '')+'</sub></p>')
    parts.append('</details>')
    (ROOT/'README.md').write_text('\n\n'.join(parts)+'\n')
    print('Generated README.md and 26 pixel SVG assets; GIF files left untouched.')


if __name__=='__main__': main()
