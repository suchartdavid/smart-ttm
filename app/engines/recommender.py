"""CDSS Recommender — แนะนำอาหารรส/ตำรับยา พร้อมตรวจสอบข้อห้าม
หลักการ: ใช้รสอาหารที่ "ตัดทอน" ธาตุที่กำเริบ และสมุนไพรที่เหมาะกับตรีโทษที่เสียสมดุล
"""
import json, pathlib

KB = json.loads(pathlib.Path(__file__).parent.parent
                .joinpath("knowledge/thai_medicine.json").read_text(encoding="utf-8"))

def recommend(element: str, dosha: dict, current_meds: list[str],
              pregnant: bool = False) -> dict:
    el = KB["elements"][element]
    dom = dosha["dominant_dosha"]
    # อาหาร: เน้นรสที่ช่วยตัดทอนธาตุเจ้าเรือนที่เสี่ยงกำเริบ
    foods = {
        "ดิน": ["ผักสด ผลไม้ไม่หวานจัด", "น้ำเปล่าให้เพียงพอ", "งดของทอดมัน"],
        "น้ำ": ["อาหารรสขม ฝาด เผ็ด (ผักจืด ฟัก ใบแมงลัก)", "งดของหวานและน้ำอัดลม", "ออกกำลังกายสม่ำเสมอ"],
        "ลม": ["อาหารรสหวาน มัน พอดี (ข้าวต้ม โจ๊ก น้ำมะพร้าว)", "งดของเย็นและเครื่องดื่มแอลกอฮอล์", "นอนหลับให้เพียงพอ"],
        "ไฟ": ["อาหารรสขม เปรี้ยว ฝาด (น้ำใบเตย มะนาว)", "งดของทอดเผ็ดจัดและกาแฟมากเกิน", "สมาธิ/ฝึกลมหายใจ"],
    }[element]

    # ตำรับยา: เลือกสมุนไพรที่เหมาะกับตรีโทษเด่น
    herb_pool = {k: v for k, v in KB["herbs"].items() if dom.split("/")[0] in v["for_dosha"]}
    if not herb_pool: herb_pool = KB["herbs"]

    warnings = []
    safe_herbs = {}
    for name, info in herb_pool.items():
        blockers = []
        if pregnant and "หญิงมีครรภ์" in info["caution"]:
            blockers.append("หญิงมีครรภ์ต้องงด")
        for med in current_meds:
            if med in KB["modern_drug_interactions"].get(name, []):
                blockers.append(f"ใช้ร่วมกับ {med} ไม่ได้ (อาจเพิ่มการฟกช้ำ/เลือดออก)")
        if blockers:
            warnings.append({"herb": name, "reason": blockers})
        else:
            safe_herbs[name] = info["effect"]

    return {
        "element_profile": {"ธาตุเจ้าเรือน": element, "ธรรมชาติ": el["nature"]},
        "diet_advice": foods,
        "taste_guideline": " + ".join(el["balancing_tastes"]),
        "suggested_herbs": safe_herbs,
        "contraindication_warnings": warnings,
    }
