#!/usr/bin/env python3
"""Surgically trim the user's approved GIF; never regenerate particle motion.

Requires Pillow. Originals are immutable in assets/pixel/source/confirmed-*.gif.
Every retained frame is checked pixel-for-pixel outside the documented UI masks.
"""
from pathlib import Path
import hashlib
import json

from PIL import Image, ImageChops, ImageDraw, GifImagePlugin
from build_readme import GLYPHS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/pixel'
SOURCE = OUT / 'source'
APPROVED_HASHES = {
    'hero': '4c2f8363f5e6fc9304317ec17f69fe125316a10cd6a7ec0e7a186d98f1994079',
    'hero-mobile': '9fbb5ce6f37591fee1e13989132404d4f58290d3cca31a6623599fcf2ae69898',
}
KEEP = tuple(range(58)) + tuple(range(130, 504))
NAMES = ('PERSONA / ENTJ', 'BNBU.ME', 'Y-CLIP', 'Y-DOCK', 'Y-KEYS', 'LANDIRECT')
COLORS = ('#edce8b', '#ae93ff', '#f19fd5', '#72e4fa', '#96edc2', '#edce8b')
MASKS = {
    False: ((47,310,431,498), (990,103,1064,126), (875,560,987,581)),
    True: ((472,175,550,199), (208,708,402,720)),
}


def color_index(palette, color):
    rgb = tuple(bytes.fromhex(color.lstrip('#')))
    return min(range(256), key=lambda i: sum((palette[3*i+c]-rgb[c])**2 for c in range(3)))


def pixel_text(draw, value, x, y, scale, fill):
    for i, char in enumerate(value.upper()):
        for row, bits in enumerate(GLYPHS[char].split()):
            for col, bit in enumerate(bits):
                if bit == '1':
                    left, top = x + (i*6+col)*scale, y + row*scale
                    draw.rectangle((left, top, left+scale-1, top+scale-1), fill=fill)


def patch(frame, owner, mobile, palette):
    """Only edit navigation/counts. Portrait and particle-stage pixels are untouched."""
    draw = ImageDraw.Draw(frame)
    bg = color_index(palette, '#0a0d19')
    stage_bg = color_index(palette, '#0d1222')
    accent = color_index(palette, COLORS[owner])
    muted = color_index(palette, '#657693')
    for x0,y0,x1,y1 in MASKS[mobile]:
        draw.rectangle((x0,y0,x1-1,y1-1),fill=bg)
    if mobile:
        draw.rectangle((472,175,549,198),fill=stage_bg)
        pixel_text(draw,f'0{owner+1}/06',478,180,2,accent)
        for i in range(6):
            draw.rectangle((223+i*28,711,240+i*28,715),fill=accent if i==owner else color_index(palette,'#2c3855'))
    else:
        y=310+owner*27
        draw.rectangle((47,y,429,y+24),fill=color_index(palette,'#222541'))
        draw.rectangle((47,y,50,y+24),fill=accent)
        for i, name in enumerate(NAMES):
            pixel_text(draw,f'0{i+1} {name}',60,315+i*27,2,color_index(palette,'#edf2ff') if i==owner else muted)
        draw.rectangle((990,103,1063,125),fill=stage_bg)
        pixel_text(draw,f'0{owner+1}/06',998,108,2,accent)
        pixel_text(draw,'06 SCENES',878,564,2,muted)


def assert_untouched(original, patched, mobile):
    diff = ImageChops.difference(original,patched.convert('RGB'))
    draw=ImageDraw.Draw(diff)
    for x0,y0,x1,y1 in MASKS[mobile]: draw.rectangle((x0,y0,x1-1,y1-1),fill=(0,0,0))
    assert diff.getbbox() is None, 'Pixels changed outside the navigation/count masks'


def trim(mobile):
    name='hero-mobile' if mobile else 'hero'
    source=SOURCE/f'confirmed-{name}.gif'
    assert hashlib.sha256(source.read_bytes()).hexdigest()==APPROVED_HASHES[name], 'Approved source changed'
    im=Image.open(source)
    assert im.n_frames==504 and im.size==((600,740) if mobile else (1120,600))
    palette=im.getpalette()
    # Map the existing colors exactly; Pillow's quantizer uses an approximate LUT.
    by_rgb={tuple(palette[i:i+3]):i//3 for i in range(0,len(palette),3)}
    output=OUT/f'{name}.gif'
    previous=None
    with output.open('wb') as fp:
        for output_index, source_index in enumerate(KEEP):
            im.seek(source_index)
            assert im.info['duration']==50
            original=im.convert('RGB')
            frame=Image.frombytes('P',original.size,bytes(map(by_rgb.__getitem__,original.get_flattened_data())))
            frame.putpalette(palette)
            assert frame.convert('RGB').tobytes()==original.tobytes(), 'Source palette changed'
            old_owner=((source_index+14)//72)%7
            assert old_owner!=1, 'Independent ENTJ scene must not survive'
            owner=old_owner if old_owner==0 else old_owner-1
            patch(frame,owner,mobile,palette)
            assert_untouched(original,frame,mobile)
            if previous is None:
                header,_=GifImagePlugin.getheader(frame,palette=bytes(palette),info={'loop':0,'optimize':False})
                for block in header: fp.write(block)
                frame.convert('RGB').save(OUT/f'{name}-poster.png')
                box=(0,0,*frame.size)
            else:
                box=ImageChops.difference(previous,frame).getbbox() or (0,0,1,1)
            delta=frame.crop(box)
            for block in GifImagePlugin.getdata(delta,offset=box[:2],duration=50,disposal=1): fp.write(block)
            previous=frame
        fp.write(b';')
    # Decode the delivered GIF and compare again, including compression/compositing.
    delivered=Image.open(output)
    assert delivered.n_frames==len(KEEP) and delivered.info.get('loop')==0
    for i, source_index in enumerate(KEEP):
        delivered.seek(i);im.seek(source_index)
        assert delivered.info['duration']==50
        assert_untouched(im.convert('RGB'),delivered,mobile)
    return {'source':source.name,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'output':output.name,'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
            'source_frames':504,'output_frames':len(KEEP),'frame_duration_ms':50,
            'removed_source_frames_inclusive':[58,129], 'kept_duration_ms':len(KEEP)*50,
            'modified_rectangles_xyxy':MASKS[mobile], 'outside_masks':'pixel-identical for every retained frame'}


if __name__=='__main__':
    results=[trim(False),trim(True)]
    report=ROOT/'.local/verification/confirmed-animation.json'
    report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))
