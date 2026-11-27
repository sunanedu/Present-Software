"""Check student navigation, course inventory, and rendered SVG text bounds."""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--edge',default=r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')
    args=parser.parse_args()
    errors=[]; link_count=0
    files=[p for p in ROOT.rglob('*') if p.is_file() and not any(part in {'.git','.qa','__pycache__','.venv','node_modules'} for part in p.relative_to(ROOT).parts)]
    repo_paths={p.relative_to(ROOT).as_posix() for p in files}
    markdown=[p for p in files if p.suffix=='.md']
    for path in files:
        if path.suffix in {'.md','.txt','.svg','.py','.csv','.srt'}:
            try: content=path.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                errors.append(f'Invalid UTF-8: {path.relative_to(ROOT)}'); continue
            if '\ufffd' in content: errors.append(f'Replacement character: {path.relative_to(ROOT)}')
        if path.suffix!='.md': continue
        if path.parent.name=='units' and any(s in content for s in ['กำลังจัดทำ','เฉพาะหัวข้อ','กำลังขยาย']):
            errors.append(f'Unfinished unit: {path.name}')
        for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',content):
            if re.match(r'^[a-z]+:',target) or target.startswith('#'): continue
            target=unquote(target.split('#')[0])
            resolved=(path.parent/target).resolve()
            link_count+=1
            try: rel=resolved.relative_to(ROOT).as_posix()
            except ValueError:
                errors.append(f'Link outside repo: {path.name}: {target}'); continue
            if rel not in repo_paths: errors.append(f'Missing or case-mismatched link: {path.relative_to(ROOT)} -> {target}')
    units=sorted((ROOT/'units').glob('*.md'))
    if len(units)!=6: errors.append(f'Expected 6 units, found {len(units)}')
    for i in range(1,7):
        if not list((ROOT/'worksheets').glob(f'{i:02}-*.md')): errors.append(f'Missing worksheet {i}')
    prompts={'minimal-keynote.txt':5,'formal-meeting.txt':5,'academic.txt':5,'unit-02-practice.txt':5,'unit-04-data-story.txt':5,'unit-06-capstone.txt':8}
    for name,count in prompts.items():
        content=(ROOT/'examples'/'prompts'/name).read_text(encoding='utf-8')
        sections=re.split(r'(?m)^---\s*$',content)
        if len(sections)!=count: errors.append(f'{name}: expected {count} slide sections, found {len(sections)}')
    for folder in ['01-minimal-keynote','02-formal-meeting','03-academic']:
        if len(list((ROOT/'examples'/folder).glob('slide-*.png')))!=5: errors.append(f'{folder}: expected 5 slides')
    svgs=sorted([p for p in files if p.suffix=='.svg'])
    for svg in svgs:
        png=svg.with_suffix('.png')
        if not png.is_file(): errors.append(f'Missing PNG: {svg.name}'); continue
        with Image.open(png) as im:
            if im.size!=(1600,900): errors.append(f'Unexpected PNG dimensions: {png.name} {im.size}')
            im.verify()
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=args.edge,headless=True)
        page=browser.new_page(viewport={'width':1600,'height':900})
        for svg in svgs:
            page.goto(svg.as_uri(),wait_until='load')
            page.evaluate('document.fonts.ready')
            clipped=page.locator('text').evaluate_all('''els => els.map(e => {
                const b=e.getBBox(); return {text:e.textContent,x:b.x,y:b.y,right:b.x+b.width,bottom:b.y+b.height};
            }).filter(b => b.x < 0 || b.y < 0 || b.right > 1600 || b.bottom > 900)''')
            for b in clipped: errors.append(f'Text outside SVG: {svg.relative_to(ROOT)}: {b["text"]}')
        browser.close()
    result={'units':len(units),'markdown_files':len(markdown),'local_links_checked':link_count,'slide_previews':15,'teaching_diagrams':len(list((ROOT/'assets'/'diagrams').glob('*.png'))),'svg_text_bounds_checked':len(svgs),'errors':errors}
    print(json.dumps(result,ensure_ascii=True,indent=2))
    raise SystemExit(1 if errors else 0)

if __name__=='__main__': main()
