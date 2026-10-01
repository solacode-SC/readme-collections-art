import math, random
random.seed(7)
T = {
 'dark':  dict(bg='#07090d', a='#ff5a52', a2='#ffb0a4', b='#3a5670', grid='#1b2a38', txt='#9aa7b4'),
 'light': dict(bg='#f7f2ee', a='#c7352d', a2='#e8847a', b='#4a6580', grid='#d9d0ca', txt='#5b6670'),
}
def spiral(cx, cy, r0, r1, turns, n=260, k=0):
    pts=[]
    for i in range(n):
        t=i/(n-1); r=r0*(r1/r0)**t; th=t*turns*2*math.pi+k
        pts.append((cx+r*math.cos(th), cy+r*math.sin(th)))
    return 'M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in pts)
def rings(cx,cy,r,n,c,sw=1.6,op=1):
    return ''.join(f'<circle cx="{cx}" cy="{cy}" r="{r*(i+1)/n:.1f}" fill="none" stroke="{c}" stroke-width="{sw}" opacity="{op}"/>' for i in range(n))
def flow(W,H,c,n,sw=1.1,op=.8):
    out=[]
    for i in range(n):
        y0=H*(i+.5)/n
        d=f'M-20,{y0:.1f}'
        pts=[]
        for s in range(0,int(W)+60,60):
            y=y0+46*math.sin(s/190+i*.35)+30*math.sin(s/90-i*.2)
            pts.append((s,y))
        d='M'+' L'.join(f'{x},{y:.1f}' for x,y in pts)
        out.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{sw}" opacity="{op}"/>')
    return ''.join(out)
def spin(cx,cy,dur,rev=False):
    a,b=(360,0) if rev else (0,360)
    return f'<animateTransform attributeName="transform" type="rotate" from="{a} {cx} {cy}" to="{b} {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/>'
def spiral_disc(cx,cy,R,c,c2,dur,rev=False):
    s=''
    for k in range(5):
        s+=f'<path d="{spiral(cx,cy,R*.04,R,3.2,k=k*2*math.pi/5)}" fill="none" stroke="{c if k%2==0 else c2}" stroke-width="{2.2 if k%2==0 else 1.2}" stroke-linecap="round"/>'
    s+=f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{c}" stroke-width="1" opacity=".5"/>'
    return f'<g>{spin(cx,cy,dur,rev)}{s}</g>'
def hero(m):
    p=T[m]; W,H=1200,520
    mesh=''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}"/>' for x in range(780,1200,30))+''.join(f'<line x1="760" y1="{y}" x2="{W}" y2="{y}"/>' for y in range(0,H,30))
    nodes=''.join(f'<circle cx="{x}" cy="{y}" r="3" fill="{p["a"]}"/>' for x,y in [(80,70),(1130,450),(640,260)])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Generative artwork: spiral fields, flow lines and concentric rings">
<rect width="{W}" height="{H}" fill="{p['bg']}"/>
<g stroke="{p['grid']}" stroke-width="1" opacity=".9">{mesh}</g>
<g>{flow(W,H,p['b'],22,1,.55)}<animateTransform attributeName="transform" type="translate" values="0 0;0 10;0 0" dur="16s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/></g>
{spiral_disc(190,300,230,p['a'],p['a2'],90)}
{spiral_disc(900,200,150,p['a'],p['a2'],70,True)}
<g>{rings(1010,120,70,9,p['a'],1.6,.9)}</g>
<g>{rings(560,430,46,6,p['a2'],1.2,.9)}<circle cx="560" cy="430" r="3" fill="{p['a']}"/></g>
{nodes}
<text x="24" y="{H-20}" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="12" fill="{p['txt']}">z → z² + c</text>
<text x="{W-24}" y="{H-20}" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="12" fill="{p['txt']}" text-anchor="end">r = a·e^(bθ)</text>
</svg>'''
def divider(m):
    p=T[m]; W,H=1200,40
    d='M0,20 '+' '.join(f'L{x},{20+8*math.sin(x/60):.1f}' for x in range(0,W+1,20))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="presentation"><path d="{d}" fill="none" stroke="{p['b']}" stroke-width="1.2"/><circle r="3.5" fill="{p['a']}"><animateMotion dur="14s" repeatCount="indefinite" path="{d}" calcMode="linear"/></circle><circle cx="600" cy="20" r="9" fill="none" stroke="{p['a']}" stroke-width="1.2"/></svg>'''
def tile(m,seed):
    p=T[m]; W,H=400,200
    s=spiral_disc(300 if seed%2 else 100,100,90,p['a'],p['a2'],80)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="presentation"><rect width="{W}" height="{H}" fill="{p['bg']}"/>{flow(W,H,p['b'],9,1,.5)}{s}<rect x=".5" y=".5" width="{W-1}" height="{H-1}" fill="none" stroke="{p['grid']}"/></svg>'''
for m in T:
    open(f'assets/hero-{m}.svg','w').write(hero(m))
    open(f'assets/divider-{m}.svg','w').write(divider(m))
    for i in (1,2,3): open(f'assets/project-{i}-{m}.svg','w').write(tile(m,i))
