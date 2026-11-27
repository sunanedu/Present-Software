"""Render SVG files with local Edge and Thai system fonts for GitHub previews."""
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image, ImageOps, ImageDraw

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--edge', default=r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')
    args=parser.parse_args()
    svgs=sorted(list((ROOT/'assets'/'diagrams').glob('*.svg'))+list((ROOT/'examples').glob('*/*.svg')))
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=args.edge,headless=True)
        page=browser.new_page(viewport={'width':1600,'height':900}, device_scale_factor=1)
        for svg in svgs:
            page.goto(svg.as_uri(),wait_until='load')
            page.evaluate('document.fonts.ready')
            page.locator('svg').screenshot(path=str(svg.with_suffix('.png')))
        browser.close()
    qa=ROOT/'.qa'
    qa.mkdir(exist_ok=True)
    for start in range(0,len(svgs),6):
        sheet=Image.new('RGB',(1600,3*490),'#E4E8ED')
        draw=ImageDraw.Draw(sheet)
        for i,svg in enumerate(svgs[start:start+6]):
            im=Image.open(svg.with_suffix('.png')).convert('RGB').resize((780,439))
            x=(i%2)*800+10; y=(i//2)*490+35
            sheet.paste(im,(x,y))
            draw.text((x,y-25),str(svg.relative_to(ROOT)),fill='#10243A')
        sheet.save(qa/f'contact-{start//6+1:02}.jpg')
    print(f'Rendered {len(svgs)} images. Contact sheets in .qa/')

if __name__=='__main__':
    main()
