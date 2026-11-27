# แก้ไขและตรวจชุดบทเรียน

เนื้อหาใน `units/` และใบงานใน `worksheets/` ใช้ UTF-8 ก่อนเปลี่ยนข้อมูลเครื่องมือให้เปิดแหล่งทางการและปรับวันที่ตรวจใน [SOURCES.md](SOURCES.md) วันที่ฉบับบทเรียนเดิมยังคงเป็น 21 พฤศจิกายน 2569

## สร้างภาพใหม่บน Windows

ต้องมี Python และ Microsoft Edge ใช้ฟอนต์ Tahoma/Leelawadee ที่เครื่องมี สคริปต์ไม่ดาวน์โหลดฟอนต์หรือสร้างภาพผ่าน AI

```powershell
python -m pip install -r scripts/requirements.txt
python scripts/generate_assets.py
python scripts/generate_workshops.py
python scripts/generate_extensions.py
python scripts/render_assets.py
python scripts/check_course.py
```

หาก Edge อยู่ที่อื่น ให้ส่ง `--edge` พร้อมตำแหน่งโปรแกรมกับสคริปต์ render/check ตรวจภาพรวมใน `.qa/` ซึ่งไม่ถูก commit ตรวจทุกหน้าว่าข้อความไม่ซ้อนและสารไม่หาย การตรวจขอบข้อความอัตโนมัติไม่แทนการดูภาพจริง

## ก่อน commit และ push

ตรวจลิงก์ รูป ภาษาไทย ตัวเลข และจำนวนส่วนในไฟล์ prompt เปิดภาพและบทเรียนที่เปลี่ยนจริง ถ้าเปลี่ยนข้อความตัวอย่างให้แก้ทั้งสคริปต์ SVG/PNG และไฟล์ prompt ที่เกี่ยวข้องให้ตรงกัน เก็บสิทธิ์ภาพตาม [เครดิต](ASSET-CREDITS.md)

เครื่องมือตรวจเช็กไฟล์ในคลังเท่านั้น ไม่ได้ยืนยันการทำงานของบัญชี Gamma หรือสถานะเว็บภายนอก ผู้สอนควรทดลองเครื่องมือก่อนใช้กับชั้นเรียน
