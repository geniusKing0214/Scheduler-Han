import os
import json
import firebase_admin
from firebase_admin import credentials, auth, firestore
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
SERVICE_ACCOUNT_PATH = PROJECT_DIR / "serviceAccountKey.json"

if not firebase_admin._apps:
    firebase_json = os.getenv("FIREBASE_JSON", "").strip()

    if firebase_json:
        cred = credentials.Certificate(json.loads(firebase_json))
    elif SERVICE_ACCOUNT_PATH.exists():
        cred = credentials.Certificate(str(SERVICE_ACCOUNT_PATH))
    else:
        raise RuntimeError(
            "Firebase 인증 정보를 찾을 수 없습니다. "
            "Railway Variables에 FIREBASE_JSON을 넣거나 "
            "로컬에서는 프로젝트 루트에 serviceAccountKey.json 파일을 두세요."
        )

    firebase_admin.initialize_app(cred)

db = firestore.client()


def verify_firebase_token(id_token: str):
    return auth.verify_id_token(id_token)