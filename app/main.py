"""Smart-TTM API — แพลตฟอร์มคัดกรองโรค NCD ทางแพทย์แผนไทย (Open Source, Public Good)
Safety Rails บังคับ: ทุก response ต้องมี disclaimer และไม่ใช่คำวินิจฉัย
"""
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

from app.engines.thai_element import birth_element, assess_tri_dosha
from app.engines.ncd_engine import bmi, diabetes_risk, hypertension_risk, dyslipidemia_risk
from app.engines.recommender import recommend
from app.privacy.deidentify import deidentify

DISCLAIMER = ("ผลลัพธ์นี้เป็นการคัดกรองเบื้องต้นจากหลักการแพทย์แผนไทยและเกณฑ์สุขภาพทั่วไป "
              "ไม่ใช่การวินิจฉัยโรค โปรดปรึกษาแพทย์แผนไทย/แพทย์แผนปัจจุบันก่อนตัดสินใจรักษา")

app = FastAPI(title="Smart-TTM NCD Screening",
              description="Open-source NCD screening via Thai Traditional Medicine — AI for Public Good Foundation")

class ScreenRequest(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    gender: Optional[str] = Field(None, pattern="^(ชาย|หญิง|อื่น ๆ)$")
    birth_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}")
    height_cm: float = Field(..., gt=80, lt=250)
    weight_kg: float = Field(..., gt=15, lt=400)
    systolic_bp: Optional[int] = Field(None, ge=60, le=300)
    diastolic_bp: Optional[int] = Field(None, ge=30, le=200)
    fasting_glucose: Optional[float] = Field(None, ge=20, le=1000)
    smoker: bool = False
    salty_food: bool = False
    fatty_food: bool = False
    family_history_dm_ht: bool = False
    exercise_weekly: int = Field(0, ge=0, le=14)
    current_meds: List[str] = []
    pregnant: bool = False
    dosha_quiz: dict = Field(default_factory=lambda: {"pitta_like": 0, "vata_like": 0, "kapha_like": 0})

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "Smart-TTM", "for_public_good": True}

@app.post("/api/screen")
def screen(req: ScreenRequest):
    age = (date.today() - date.fromisoformat(req.birth_date)).days // 365
    element = birth_element(req.birth_date)
    dosha = assess_tri_dosha(req.dosha_quiz)
    bmi_v = bmi(req.height_cm, req.weight_kg)

    results = {
        "diabetes": diabetes_risk(bmi_v, age, req.fasting_glucose,
                                  req.family_history_dm_ht, req.exercise_weekly),
        "hypertension": hypertension_risk(req.systolic_bp, req.diastolic_bp,
                                          bmi_v, req.smoker, req.salty_food),
        "dyslipidemia": dyslipidemia_risk(bmi_v, age, req.fatty_food,
                                          req.family_history_dm_ht),
    }
    high = any(r["risk_level"] == "สูง" for r in results.values())

    return {
        "name": req.name,
        "gender": req.gender,
        "age": age,
        "bmi": bmi_v,
        "thai_element": element,
        "tri_dosha": dosha,
        "ncd_screening": results,
        "recommendation": recommend(element, dosha, req.current_meds, req.pregnant),
        "flags": {
            "high_risk_detected": high,
            "advice": "ควรพบแพทย์เพื่อตรวจยืนยันเร็วที่สุด" if high else "ดูแลสุขภาพตามคำแนะนำ และตรวจสุขภาพประจำปี",
        },
        "disclaimer": DISCLAIMER,
        "note": "Human-in-the-loop: แพทย์มีอำนาจตัดสินใจสุดท้ายเสมอ",
    }

@app.post("/api/deidentify")
def deidentify_demo(record: dict):
    return deidentify(dict(record))

@app.get("/", include_in_schema=False)
def index():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/index.html")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
