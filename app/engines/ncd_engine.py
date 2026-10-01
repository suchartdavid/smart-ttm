"""NCD Risk Engine — ประเมินความเสี่ยงเบาหวาน/ความดัน/ไขมันสูง
เป็น rule-based เวอร์ชันต้นแบบ (เทียบกับเกณฑ์ระบาดวิทยาทั่วไป)
เป้าหมายตาม Roadmap: เปลี่ยนเป็นโมเดล ML (XGBoost) หลังมีข้อมูลจริง ≥10,000 ชุด
"""
def bmi(height_cm: float, weight_kg: float) -> float:
    h = height_cm / 100
    return round(weight_kg / (h * h), 1)

def diabetes_risk(bmi_v: float, age: int, fasting_glucose: float | None,
                  family_history: bool, exercise_weekly: int) -> dict:
    score = 0
    if bmi_v >= 30: score += 3
    elif bmi_v >= 25: score += 2
    elif bmi_v >= 23: score += 1          # เกณฑ์เอเชีย
    if age >= 45: score += 2
    if fasting_glucose and fasting_glucose >= 100: score += 3
    if family_history: score += 2
    if exercise_weekly < 3: score += 1
    level = "สูง" if score >= 6 else "ปานกลาง" if score >= 3 else "ต่ำ"
    return {"score": score, "risk_level": level,
            "ttm_mapping": "มธุเมหะ (ธาตุน้ำ-ไฟ เสมหะ/ปิตตะ เสียสมดุล)"}

def hypertension_risk(systolic: int | None, diastolic: int | None,
                      bmi_v: float, smoker: bool, salty_food: bool) -> dict:
    score = 0
    if systolic and systolic >= 140: score += 3
    if diastolic and diastolic >= 90: score += 3
    if bmi_v >= 25: score += 2
    if smoker: score += 2
    if salty_food: score += 2
    level = "สูง" if score >= 6 else "ปานกลาง" if score >= 3 else "ต่ำ"
    return {"score": score, "risk_level": level,
            "ttm_mapping": "วาตะกำเริบ / เสมหะพิการ (ลมและเมือกมันขัดขวางทางเลือดลม)"}

def dyslipidemia_risk(bmi_v: float, age: int, fatty_food: bool,
                      family_history: bool) -> dict:
    score = 0
    if bmi_v >= 25: score += 2
    if age >= 40: score += 1
    if fatty_food: score += 2
    if family_history: score += 2
    level = "สูง" if score >= 5 else "ปานกลาง" if score >= 2 else "ต่ำ"
    return {"score": score, "risk_level": level,
            "ttm_mapping": "เสมหะสมุฏฐานสะสม (เมือกมันเกิน ต้องรสขม ฝาด ตัดทอน)"}
