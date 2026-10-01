"""คำนวณธาตุเจ้าเรือน (Birth Element) และประเมินสมดุลตรีโทษ
หมายเหตุ: การคำนวณธาตุเป็นหลักเกณฑ์เชิงตัวอย่าง (เกณฑ์ทับแบบประยุกต์)
สถาบันแพทย์แผนไทยสามารถปรับแผนที่ (mapping) ได้ที่ไฟล์นี้
"""
ELEMENTS = ["ดิน", "น้ำ", "ลม", "ไฟ"]  # ภูมิ อาโป วาโย เตโช

def birth_element(birth_date: str) -> str:
    """คำนวณธาตุเจ้าเรือนจากวันเดือนปีเกิด (รูปแบบ YYYY-MM-DD)"""
    try:
        y, m, d = map(int, birth_date.split("-"))
    except ValueError:
        raise ValueError("birth_date ต้องอยู่ในรูปแบบ YYYY-MM-DD")
    # เกณฑ์ทับแบบประยุกต์: ผลรวมม็อดูโล 4
    return ELEMENTS[(y + m + d) % 4]

def assess_tri_dosha(quiz: dict) -> dict:
    """ประเมินความแปรปรวนของสมุฏฐาน (ตรีโทษ) จากแบบสอบถามพฤติกรรม/อาการ
    quiz keys: pitta_like, vata_like, kapha_like (คะแนน 0-10)
    """
    scores = {
        "ปิตตะ": min(max(quiz.get("pitta_like", 0), 0), 10),
        "วาตะ":  min(max(quiz.get("vata_like", 0), 0), 10),
        "เสมหะ": min(max(quiz.get("kapha_like", 0), 0), 10),
    }
    dominant = max(scores, key=scores.get)
    balance = 10 - (max(scores.values()) - min(scores.values()))  # ยิ่งใกล้ 10 ยิ่งสมดุล
    return {
        "scores": scores,
        "dominant_dosha": dominant,
        "imbalance_level": "เกิน" if scores[dominant] >= 7 else "เพิ่มขึ้น" if scores[dominant] >= 4 else "ปกติ",
        "balance_index": balance,  # 0-10
    }
