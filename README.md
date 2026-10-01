# Smart-TTM: NCD Screening Platform (แพลตฟอร์มคัดกรองโรค NCD ทางแพทย์แผนไทย)
โครงการ Open Source เพื่อประโยชน์สาธารณะ โดย AI for Public Good Foundation

> ⚠️ **ข้อจำกัดความรับผิดชอบ (Disclaimer):** ระบบนี้เป็น "เครื่องมือช่วยคัดกรองและให้ความรู้เบื้องต้น"
> ไม่ใช่การวินิจฉัยโรค ไม่ใช่ Medical Device และไม่แทนคำแนะนำของแพทย์/เภสัชกร
> ผลการประเมินทุกกรณีต้องได้รับการยืนยันโดยบุคลากรทางการแพทย์ (Human-in-the-loop)

## สถาปัตยกรรม
```
smart-ttm/
├── app/
│   ├── main.py                  # FastAPI entry point + Safety Rails
│   ├── engines/
│   │   ├── thai_element.py      # คำนวณธาตุเจ้าเรือนจากวันเกิด + แบบประเมินลักษณะนิสัย
│   │   ├── ncd_engine.py        # ประเมินความเสี่ยง NCD (เบาหวาน/ความดัน/ไขมัน) แบบ rule-based
│   │   └── recommender.py       # คำแนะนำอาหารรส 6 + ตำรับยา + ตรวจสอบข้อห้าม (Contraindications)
│   ├── privacy/
│   │   └── deidentify.py        # PDPA: De-identification ด้วย UUID + HMAC hash
│   ├── knowledge/
│   │   └── thai_medicine.json   # คลังความรู้ (องค์ประกอบธาตุ/ตรีโทษ/รสอาหาร/สมุนไพร/ข้อห้าม)
│   └── static/index.html        # หน้าเว็บภาษาไทย (บริจาคโดย AI for Public Good Foundation)
└── requirements.txt
```

## วิธีรัน
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# เปิด http://localhost:8000
```

## API หลัก
| Method | Endpoint | คำอธิบาย |
|---|---|---|
| POST | `/api/screen` | คัดกรอง NCD: input ข้อมูลสุขภาพ+วันเกิด → ผลธาตุ/ตรีโทษ/ความเสี่ยง/คำแนะนำ |
| POST | `/api/deidentify` | ตัวอย่างกระบวนการ PDPA De-identification (UUID + hash) |

## หลักการทำงาน (อ้างอิงเอกสารโครงการ)
1. **Smart Diagnosis**: คำนวณธาตุเจ้าเรือนจากวันเดือนปีเกิด + ประเมินสมดุลตรีโทษ (ปิตตะ วาตะ เสมหะ)
2. **NCD Risk Engine**: ผสานข้อมูลคลินิก (BMI, BP, น้ำตาล, สถิติครอบครัว) กับตรีโทษ เพื่อให้คะแนนความเสี่ยง
3. **CDSS Recommender**: แนะนำอาหารรสที่เหมาะกับธาตุ + ตำรับยาปรับสมดุล พร้อมตรวจสอบข้อห้ามยา
4. **Safety Rails**: ทุกผลลัพธ์บังคับแสดงคำเตือน และระบบถูกออกแบบให้เป็น Decision Support เท่านั้น

## แนวทางพัฒนาต่อ (Roadmap ตามเอกสาร)
- [ ] แทน rule-based engine ด้วยโมเดล ML ที่เทรนจากข้อมูลจริง (Accuracy ≥ 85%)
- [ ] Thai Medical NLP + Knowledge Graph จากคัมภีร์ (ตักศิลา, ประถมจินดา)
- [ ] Computer Vision วิเคราะห์ลิ้น (Tongue Diagnosis)
- [ ] Sandbox Clinical Validation (Shadow Mode → Clinical Assistant Mode)

## License
MIT License — เพื่อประโยชน์สาธารณะ


## 🚀 Deploy ขึ้นเว็บจริง (ฟรี)

### ตัวเลือก 1: Hugging Face Spaces (แนะนำ — ฟรี ไม่หลับ ง่ายสุด)
1. สมัคร huggingface.co → สร้าง Space ใหม่ → เลือก SDK: **Docker**
2. เลือก Public → กด Create
3. อัปโหลดไฟล์ทั้งหมดใน zip (รวม Dockerfile)
4. รอ build ~2 นาที → ได้ URL เช่น `https://your-name-smart-ttm.hf.space`

### ตัวเลือก 2: Render.com (ฟรี แต่หลับเมื่อไม่มีคนใช้ 15 นาที)
1. render.com → New Web Service → Connect GitHub (push โค้ดขึ้น repo ก่อน)
2. Build Command: `pip install -r requirements.txt`
3. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### ตัวเลือก 3: Railway.app / PythonAnywhere
- Railway: ต่อ GitHub repo เลือก repo → deploy อัตโนมัติ (ฟรี $5 เครดิต/เดือน)
- PythonAnywhere: เหมาะกับผู้เริ่มต้น มีเว็บ Python ฟรี (ต้องปรับ WSGI file ชี้ไปที่ app.main:app)
