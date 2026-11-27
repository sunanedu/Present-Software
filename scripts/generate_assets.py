"""Build original, self-contained SVG teaching diagrams (no image generation API)."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'diagrams'
OUT.mkdir(parents=True, exist_ok=True)
FONT = 'Tahoma, Leelawadee UI, sans-serif'

def rect(x, y, w, h, fill, rx=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"/>'

def text(x, y, s, size=32, fill='#183153', weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}">{escape(s)}</text>'

def lines(x, y, strings, size=32, fill='#183153', gap=54, weight=400):
    return ''.join(text(x, y+i*gap, s, size, fill, weight) for i, s in enumerate(strings))

def save(path, title, body, bg='#F8FAFC', desc='ภาพประกอบต้นฉบับสำหรับหลักสูตร AI Presentation Studio'):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc><g font-family="{FONT}">{rect(0,0,1600,900,bg)}{body}</g></svg>', encoding='utf-8')

def diagrams():
    b = text(100,130,'AI PRESENTATION STUDIO',28,'#B9A7FF',700)
    b += lines(100,275,['ออกแบบความคิด','สร้างสไลด์ด้วย AI'],76,'#FFFFFF',115,700)
    b += lines(100,565,['บทเรียนภาษาไทย 6 หน่วย','พื้นฐานการออกแบบ · Gamma · เวิร์กช็อปมืออาชีพ'],30,'#D2DAEB',60)
    b += text(100,805,'ฉบับบทเรียน 21 พฤศจิกายน 2569',25,'#D2DAEB')
    for x,y,c in [(1040,180,'#4D3A8C'),(1100,290,'#7561B5'),(1160,400,'#B9A7FF')]:
        b += rect(x,y,330,220,c,22)+rect(x+30,y+35,180,12,'#FFFFFF',6)+rect(x+30,y+65,120,9,'#E8E1FF',4)
    save(OUT/'course-cover.svg','หลักสูตรออกแบบงานนำเสนอด้วย AI',b,'#0B1020')

    b = text(80,105,'จัดหน้าใหม่ ให้เห็นสารหลักใน 5 วินาที',48,weight=700)
    b += rect(80,175,680,550,'#E8EDF3',20)+rect(840,175,680,550,'#FFFFFF',20)
    b += text(115,235,'ก่อนปรับ',30,'#526273')+text(875,235,'หลังปรับ',30,'#356859')
    b += text(130,320,'ข้อมูลประกอบ',38,'#7B3E90',700)
    b += lines(130,390,['เรื่องที่หนึ่ง เรื่องที่สอง เรื่องที่สาม','รายละเอียดที่ผู้ฟังต้องอ่านทั้งหมด','ข้อความสำคัญซ่อนอยู่ในย่อหน้า','ภาพตกแต่งหลายภาพแย่งความสนใจ'],27,'#596B7D',60)
    b += rect(160,620,170,50,'#A7B4C3')+rect(410,620,220,50,'#B6A4C5')
    b += lines(890,335,['พกแก้วส่วนตัว','เริ่มวันจันทร์นี้'],49,'#10243A',75,700)
    b += rect(890,510,520,6,'#356859')
    b += lines(890,580,['เลือกแก้วที่พกสะดวก','ตั้งเตือนก่อนออกจากบ้าน'],30,'#356859',60)
    b += text(80,820,'ตัดส่วนเกิน · จัดแนว · เน้นประเด็นเดียว · เว้นพื้นที่',32)
    save(OUT/'before-after.svg','ก่อนและหลังปรับองค์ประกอบสไลด์',b)

    b = text(80,100,'4 ระบบสีสำหรับเริ่มออกแบบ',48,weight=700)
    palettes=[('Calm Editorial',['#F7F5F0','#202124','#356859']),('Formal Navy',['#F8FAFC','#10243A','#8A5A14']),('Digital Indigo',['#0B1020','#FFFFFF','#B9A7FF']),('Research Teal',['#FFFFFF','#183153','#006D77'])]
    for i,(name,colors) in enumerate(palettes):
        y=155+i*155
        b+=text(80,y+50,name,29,weight=700)
        for j,c in enumerate(colors):
            x=530+j*335
            b+=rect(x,y,285,75,c,10)+text(x,y+115,c,25)
    b+=text(80,845,'สีพื้น / สีข้อความ / สีเน้น ตามลำดับ · ชุดสีออกแบบเพื่อฝึก ไม่ใช่สีแบรนด์',25)
    save(OUT/'color-palettes.svg','ตัวอย่างสีพื้น ข้อความ และสีเน้น 4 ชุด',b)

    b=text(80,105,'ประสบการณ์ที่ดี เริ่มจากผู้ฟัง',48,weight=700)
    b+=rect(80,180,680,540,'#E4F1EE',20)+rect(840,180,680,540,'#EBE8FA',20)
    b+=text(125,270,'UX',70,'#356859',700)+text(885,270,'UI',70,'#51418D',700)
    b+=lines(125,370,['ผู้ฟังคือใคร','เรื่องเรียงอย่างไร','เข้าใจและทำอะไรต่อ'],37,'#183153',95)
    b+=lines(885,370,['หัวข้ออ่านชัด','สีและเลย์เอาต์สม่ำเสมอ','ลิงก์และปุ่มเข้าใจง่าย'],37,'#183153',95)
    b+=text(80,820,'ทดสอบกับคนจริง แล้วแก้จุดที่อ่านหรือเข้าใจติดขัด',32)
    save(OUT/'ux-ui.svg','UX และ UI สำหรับงานนำเสนอ',b)

    b=text(80,105,'จากโจทย์ สู่สไลด์ที่ตรวจแล้ว',48,weight=700)
    steps=[('01','เตรียมโจทย์','ผู้ฟัง / สาร / หลักฐาน'),('02','สั่ง AI','ภาษาไทย / 5 หน้า'),('03','ตรวจแก้','ข้อมูล / ภาพ / ภาษา'),('04','ทดลองใช้','ฉายจริง / ซ้อมพูด')]
    for i,(n,t,d) in enumerate(steps):
        x=80+i*385
        b+=rect(x,240,340,390,'#FFFFFF',18)+text(x+30,330,n,64,'#7561B5',700)
        b+=text(x+30,430,t,36,weight=700)+text(x+30,505,d,23)
        if i<3:
            b+=f'<path d="M {x+345} 425 h 28 m -8 -8 l 8 8 -8 8" stroke="#356859" stroke-width="4" fill="none"/>'
    b+=text(80,760,'ภาพสรุปกระบวนการ ไม่ใช่ภาพหน้าจอโปรแกรม Gamma',29,'#526273')
    save(OUT/'gamma-workflow.svg','ขั้นตอนเรียนรู้การสร้างสไลด์ด้วย Gamma',b)

if __name__ == '__main__':
    diagrams()
    print('Built 5 original teaching diagrams.')
