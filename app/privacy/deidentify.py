"""PDPA De-identification — ตัดข้อมูลระบุตัวตนออกก่อนส่งเข้า AI Pipeline
อ้างอิง: พ.ร.บ.คุ้มครองข้อมูลส่วนบุคคล พ.ศ.2562 (De-identification + UUID mapping แยกเก็บ)
"""
import uuid, hashlib, hmac, os

_SALT = os.environ.get("PDPA_HMAC_SALT", "change-me-in-production").encode()

def deidentify(record: dict) -> dict:
    """คืนข้อมูลที่ตัดชื่อ/เลขบัตรออก แทนด้วย subject_uuid + hash เพื่อเชื่อมโยงภายหลัง"""
    pid = record.pop("national_id", None)
    record.pop("full_name", None)
    subject_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS,
                       (pid or "").encode() if pid else str(uuid.uuid4())))
    record["subject_uuid"] = subject_uuid
    record["link_token"] = hmac.new(_SALT, subject_uuid.encode(), hashlib.sha256).hexdigest()[:16]
    return record
