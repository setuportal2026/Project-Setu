# modules/guard.py

import requests
import re
from modules.router import search_krc_by_district, format_krc_card

HF_TOKEN = None  # loaded from .streamlit/secrets.toml -> st.secrets["HF_TOKEN"]


# ---------- 1. Scam-prone keyword triggers ----------
SCAM_KEYWORDS = [
    "fast degree", "without exam", "backdoor", "paise dekar",
    "under table", "agent se degree", "fake marksheet",
    "jaldi certificate", "bina exam", "guarantee pass",
    "cash for degree", "paisa dekar pass"
]

def is_scam_prone(query: str) -> bool:
    q = query.lower()
    return any(kw in q for kw in SCAM_KEYWORDS)


# ---------- 2. Document guidance data ----------
DOCUMENT_GUIDANCE = {
    "migration certificate": {
        "online": (
            "MMHAPU ki official website (mmhapu.ac.in) ke 'STUDENTS SECTION' "
            "> 'Application for online certificate' link se apply karo. "
            "Yeh CCAvenue-based secure form hai jaha request + online payment "
            "dono ho jaate hain. Documents by post ~21 din me deliver hote hain. "
            "Current fee amount portal par apply karte waqt hi dikhegi."
        ),
        "offline": (
            "Apne KRC ke director se ek recommendation/declaration letter likhwao, "
            "phir MMHAPU Patna office counter par jaakar submit karo. "
            "24-48 ghante me wahi se document mil jaata hai."
        ),
    },
    "transfer certificate": {
        "online": (
            "Same online certificate portal (mmhapu.ac.in > Application for online certificate) "
            "se request kar sakte ho, payment online hoti hai, delivery by post ~21 din."
        ),
        "offline": (
            "KRC director se recommendation letter lekar MMHAPU office counter par submit karo, "
            "24-48 ghante me mil jaata hai."
        ),
    },
    "marksheet": {
        "online": (
            "Online certificate portal se request kar sakte ho; agar recent result ka hai, "
            "original marksheet result declaration ke ~2 hafte baad respective college se bhi mil sakti hai."
        ),
        "offline": (
            "KRC director recommendation letter ke saath MMHAPU office counter par submit karo, "
            "24-48 ghante me milega."
        ),
    },
    "degree": {
        "online": (
            "Online certificate portal se apply karo, payment online, delivery by post ~21 din. "
            "Convocation ke baad hi degree certificate issue hota hai, isliye status pehle confirm kar lena."
        ),
        "offline": (
            "KRC director se recommendation letter lekar MMHAPU office counter par submit karo, "
            "24-48 ghante me milega."
        ),
    },
}

DOC_ALIASES = {
    "migration": "migration certificate",
    "mc": "migration certificate",
    "tc": "transfer certificate",
    "transfer": "transfer certificate",
    "marksheet": "marksheet",
    "mark sheet": "marksheet",
    "degree": "degree",
}


def detect_document(query: str):
    q = query.lower()
    for alias, doc in DOC_ALIASES.items():
        if alias in q:
            return doc
    return None


# ---------- 3. Llama 3.2 AI check (fail-safe, works even without token) ----------
def ai_scam_check(query: str) -> bool:
    if not HF_TOKEN:
        return False  # no token yet -> skip AI check, keyword check still works
    api_url = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-3B-Instruct"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    prompt = (
        "Classify if this student query is trying to find an illegitimate/scam way "
        "to get a university document (fake, bribe, skip process). "
        f"Reply only 'yes' or 'no'.\nQuery: {query}"
    )
    try:
        response = requests.post(api_url, headers=headers, json={"inputs": prompt}, timeout=15)
        text = response.json()[0]["generated_text"].lower()
        return "yes" in text
    except Exception:
        return False  # fail-safe: don't block on API error


# ---------- 4. Main guard entry point ----------
def guard_and_guide(query: str, student_district: str = None):
    if is_scam_prone(query) or ai_scam_check(query):
        return {
            "status": "warning",
            "message": (
                "⚠️ Yeh request university ke official process se bahar lag rahi hai. "
                "Kripya sirf official online portal ya apne KRC ke through hi documents apply karein. "
                "Kisi bhi agent/third-party ko paisa na dein."
            ),
        }

    doc = detect_document(query)
    if doc:
        guidance = DOCUMENT_GUIDANCE[doc]
        krc_info = ""
        if student_district:
            matches = search_krc_by_district(student_district)
            if matches:
                nearest = matches[0]
                krc_info = format_krc_card(nearest["krc_code"], nearest)
        return {
            "status": "guidance",
            "document": doc,
            "online_process": guidance["online"],
            "offline_process": guidance["offline"],
            "nearest_krc": krc_info,
        }

    return {"status": "unrecognized", "message": "Please specify which document you need."}