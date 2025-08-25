from fastapi import FastAPI
from pydantic import BaseModel
from app.db_setup import SessionMaker, init_db
from app.models import SessionChat, MsgLog, OrderData
from app.ollama_wrap import get_client
import json, re

app = FastAPI(title="jr-ai-chatbot")
init_db()
ollama = get_client()

class ChatIn(BaseModel):
    session_id: str
    user_id: int | None = None
    message: str

def ambil_session(db, session_id, user_id=None):
    s = db.query(SessionChat).filter_by(session_id=session_id).first()
    if not s:
        s = SessionChat(session_id=session_id, user_id=user_id)
        db.add(s); db.commit(); db.refresh(s)
    return s

def last_msgs(db, sid, n=6):
    data = (
        db.query(MsgLog)
        .filter_by(session_id=sid)
        .order_by(MsgLog.created_at.desc())
        .limit(n)
        .all()
    )
    return list(reversed([{"role": m.role, "content": m.content} for m in data]))

def call_model(messages):
    try:
        r = ollama.chat(model="llama3.2:3b", messages=messages)

        # object-style (dataclass) -> r.message.content
        if hasattr(r, "message") and hasattr(r.message, "content"):
            return r.message.content

        # dict-style
        if isinstance(r, dict):
            if "message" in r and isinstance(r["message"], dict):
                return r["message"].get("content", "")
            if "response" in r:
                return r["response"]
            if "choices" in r:
                c = r["choices"][0]
                if "message" in c:
                    return c["message"].get("content", "")
                return c.get("text", "")

        return str(r)
    except Exception as e:
        return f"[err model] {e}"

@app.post("/chat")
def chat(body: ChatIn):
    db = SessionMaker()
    sess = ambil_session(db, body.session_id, body.user_id)

    # simpan pesan user
    db.add(MsgLog(session_id=sess.id, role="user", content=body.message)); db.commit()

    # memory: 3 interaksi terakhir (6 msg)
    prev = last_msgs(db, sess.id, 6)

    # instruksi singkat
    sys_prompt = (
        "Asisten CS toko. Kalau user minta status pesanan, keluarkan JSON call_tool valid "
        "di dalam code block seperti: ```json {\"tool\":\"get_order_status\",\"order_number\":\"ORD001\"} ``` "
        "Kalau gak butuh tool, jawab singkat dan santai."
    )

    msgs = [{"role":"system","content":sys_prompt}] + prev + [{"role":"user","content":body.message}]
    out = call_model(msgs)

    # deteksi tool call dari code block json
    m = re.search(r'```json\s*(\{.*?\})\s*```', out, re.S)
    parsed = json.loads(m.group(1)) if m else None

    if parsed and parsed.get("tool") == "get_order_status":
        ordno = parsed.get("order_number")
        ord_db = db.query(OrderData).filter_by(order_number=ordno).first()
        tool_res = {"found": bool(ord_db)}
        if ord_db:
            tool_res["status"] = ord_db.status

        # balikin hasil tool ke model untuk bikin jawaban final
        follow = [
            {"role":"system","content":"ini hasil tool dlm json"},
            {"role":"assistant","content": json.dumps(tool_res)},
            {"role":"user","content":"tolong jawab singkat ke user pakai bahasa santai"},
        ]
        out = call_model([{"role":"system","content":sys_prompt}] + prev + follow)

    # simpan jawaban bot
    db.add(MsgLog(session_id=sess.id, role="assistant", content=out)); db.commit()
    return {"reply": out}
