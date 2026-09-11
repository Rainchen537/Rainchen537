#!/usr/bin/env python3
"""Regenerate self-contained profile SVGs. Run from any directory with Python 3."""
import base64
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
BODY = 'PingFang SC,Hiragino Sans GB,Microsoft YaHei,Arial,sans-serif'
DISPLAY = 'Avenir Next,Helvetica Neue,Arial,sans-serif'
MONO = 'SFMono-Regular,Consolas,Liberation Mono,monospace'
C = dict(ink='#101a32', paper='#eef3ff', blue='#b7d2f5', lilac='#d1bae2', pink='#e7afce', muted='#a9bad8')

def text(x,y,value,size=32,color='paper',family=BODY,weight=400,spacing=0):
    return f'<text x="{x}" y="{y}" fill="{C.get(color,color)}" font-family="{family}" font-size="{size}" font-weight="{weight}" letter-spacing="{spacing}">{escape(value)}</text>'

def image(name,x,y,w,h):
    mime='jpeg' if name.endswith('.jpg') else 'png'
    data=base64.b64encode((ASSETS/name).read_bytes()).decode()
    return f'<image href="data:image/{mime};base64,{data}" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice"/>'

def svg(w,h,title,body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title>{body}</svg>\n'

def save(name,w,h,title,body):
    (ASSETS/name).write_text(svg(w,h,title,body))

def arrow(x,y):
    return f'<path d="M{x} {y+22}l28-28m-28 0h28v28" fill="none" stroke="{C["blue"]}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'

def hero():
    template=(ASSETS/'atmosphere-card.template.svg').read_text()
    data=base64.b64encode((ASSETS/'atmosphere.jpg').read_bytes()).decode()
    (ASSETS/'profile-hero.svg').write_text(template.replace('__BACKGROUND_DATA__',data))

def bnbu(mobile=False):
    w,h=(720,372) if mobile else (1200,294)
    x=44 if mobile else 56
    body=f'''<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#152a48"/><stop offset="1" stop-color="#161d35"/></linearGradient></defs>
    <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="24" fill="url(#bg)" stroke="#394c6c"/>
    <rect x="{x}" y="43" width="38" height="4" rx="2" fill="#b7d2f5"/>'''
    body+=text(x,132,'BNBU.ME',64 if mobile else 70,'paper',DISPLAY,700,1)
    body+=text(x,192,'校园客户端 · 小U AI 助手',32,'blue')
    body+=text(x,252 if mobile else 250,'FLUTTER / PYTHON',21,'muted',MONO,spacing=1)
    if mobile:
        body+=text(x,322,'iOS · Android · macOS · Windows',25,'paper',DISPLAY)
    else:
        body+='<path d="M760 56V238" stroke="#394c6c"/>'
        body+=text(810,120,'iOS / Android',34,'paper',DISPLAY,500)
        body+=text(810,175,'macOS / Windows',34,'paper',DISPLAY,500)
    body+=arrow(w-82,60)
    save('project-bnbu'+('.mobile' if mobile else '')+'.svg',w,h,'BNBU.ME — 校园客户端与小U AI助手；iOS、Android、macOS、Windows',body)

PROJECTS=[('y-clip','Y-Clip','剪贴板历史','SWIFT / APPKIT'),('y-dock','Y-Dock','窗口预览与切换','SWIFT / APPKIT'),('y-keys','Y-Keys','快捷键速查','SWIFT / APPKIT')]
def project(key,name,label,stack,mobile=False):
    w,h=(720,230) if mobile else (1200,188)
    body=f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="22" fill="#101a2c" stroke="#33415b"/>'
    body+=image(key+'.png',30 if mobile else 34,44 if mobile else 30,128,128)
    platform='macOS'
    tx=184 if mobile else 202
    body+=text(tx,91 if mobile else 80,name,44,'paper',DISPLAY,600)
    body+=text(tx,139 if mobile else 127,label,30,'blue')
    if mobile:
        body+=text(tx,184,platform,23,'muted',DISPLAY)
    else:
        body+=text(775,94,platform,30,'paper',DISPLAY)
        body+=text(775,131,stack,20,'muted',MONO)
    body+=arrow(w-82,65 if mobile else 74)
    save('project-'+key+('.mobile' if mobile else '')+'.svg',w,h,name+' — '+label+'；'+platform,body)

if __name__=='__main__':
    hero()
    for mobile in (False,True):
        bnbu(mobile)
        for p in PROJECTS:project(*p,mobile=mobile)
    print('Rendered 9 profile SVGs.')
