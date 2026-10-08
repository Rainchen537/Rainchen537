"""Pixel wordmark replacement confined to the approved GIF's BNBU scene."""
from collections import Counter
from PIL import Image
from build_readme import GLYPHS

BOUNDS = {False:(503,128,1062,472), True:(40,210,560,570)}
EXTRA_BOUNDS = {False:(600,110,965,128), True:None}
BACKGROUND_COLORS = {
    (13,18,34),(12,15,19),(13,16,21),(28,41,66),(37,52,80),
    (59,69,102),(41,56,88),(37,47,73),(101,118,155),
}


def palette_index(palette, rgb):
    return min(range(256),key=lambda i:sum((palette[3*i+c]-rgb[c])**2 for c in range(3)))


def make_backdrop(source, mobile, palette):
    """Recover dark stage pixels from corresponding holds in the original scenes."""
    result={name:sample_backdrop(source,box,palette) for name,box in
            [('main',BOUNDS[mobile]),('extra',EXTRA_BOUNDS[mobile])] if box}
    if not mobile:
        # The rejected oversized icon obscured part of this existing heading.
        source.seek(0)
        crop=source.convert('RGB').crop((600,110,680,121))
        colors={tuple(palette[i:i+3]):i//3 for i in range(0,len(palette),3)}
        patch=Image.frombytes('P',crop.size,bytes(map(colors.__getitem__,crop.get_flattened_data())))
        patch.putpalette(palette)
        result['extra'].paste(patch,(0,0))
    return result


def sample_backdrop(source,box,palette):
    samples=[]
    for n in (0,72,144,216,288,360,432):
        source.seek(n)
        samples.append(source.convert('RGB').crop(box).tobytes())
    colors={tuple(palette[i:i+3]):i//3 for i in range(0,len(palette),3)}
    background=palette_index(palette,(12,15,19))
    result=bytearray()
    for i in range(0,len(samples[0]),3):
        choices=[tuple(s[i:i+3]) for s in samples]
        common,count=Counter(choices).most_common(1)[0]
        basic=[c for c in choices if c in {(13,18,34),(12,15,19),(13,16,21)}]
        if common in BACKGROUND_COLORS and count>=4:
            result.append(colors[common])
        elif basic:
            result.append(colors[Counter(basic).most_common(1)[0][0]])
        else:
            result.append(background)
    im=Image.frombytes('P',(box[2]-box[0],box[3]-box[1]),bytes(result))
    im.putpalette(palette)
    return im


def word_pixels(mobile,palette):
    word='BNBU.ME'
    scale=8
    cx,cy=(300,382) if mobile else (782,288)
    x0=cx-(len(word)*6-1)*scale//2
    y0=cy-7*scale//2
    pixels=[]
    for i,char in enumerate(word):
        color=palette_index(palette,(114,228,250) if i<4 else (174,147,255))
        for row,bits in enumerate(GLYPHS[char].split()):
            for col,bit in enumerate(bits):
                if bit=='1':
                    for dy in range(0,scale,2):
                        for dx in range(0,scale,2):
                            pixels.append((x0+(i*6+col)*scale+dx,y0+row*scale+dy,color))
    return pixels


def replace(frame, source_rgb, source_index, mobile, backdrop, pixels):
    """Use original foreground positions as the transition field for the new letters."""
    if not 130<=source_index<=201:
        return
    box=BOUNDS[mobile]
    frame.paste(backdrop['main'],box[:2])
    if EXTRA_BOUNDS[mobile]: frame.paste(backdrop['extra'],EXTRA_BOUNDS[mobile][:2])
    if source_index<144:
        amount=(source_index-130)/14
    elif source_index>=188:
        amount=1-(source_index-188)/14
    else:
        amount=1
    amount=amount*amount*(3-2*amount)
    field=[]
    if amount<1:
        crop=source_rgb.crop(box)
        data=crop.load()
        for y in range(0,crop.height,2):
            for x in range(0,crop.width,2):
                if max(data[x,y])>110:
                    field.append((box[0]+x,box[1]+y))
    for i,(x,y,color) in enumerate(pixels):
        if field:
            fx,fy=field[(i*1543)%len(field)]
            x=round(fx+(x-fx)*amount)
            y=round(fy+(y-fy)*amount)
        for dx in (0,1):
            for dy in (0,1):
                if box[0]<=x+dx<box[2] and box[1]<=y+dy<box[3]:
                    frame.putpixel((x+dx,y+dy),color)
