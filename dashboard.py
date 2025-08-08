import streamlit as st
import json
import os

# 📁 مسار ملف الردود
REPLIES_FILE = "replies.json"

# 🟡 تحميل الردود
def load_replies():
    if os.path.exists(REPLIES_FILE):
        with open(REPLIES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# 🟢 حفظ الردود
def save_replies(replies):
    with open(REPLIES_FILE, "w", encoding="utf-8") as f:
        json.dump(replies, f, ensure_ascii=False, indent=2)

# ⚙️ إعداد الواجهة
st.set_page_config(page_title="لوحة تحكم البوت", layout="centered")
st.title("📦 لوحة التحكم بالردود الجاهزة")

# 📄 تحميل الردود الحالية
replies = load_replies()

# ✅ عرض الردود
st.subheader("📋 الردود الحالية")
if not replies:
    st.info("🚫 لا يوجد ردود بعد.")
else:
    for i, item in enumerate(replies):
        st.markdown(f"**{item['keyword']}** → {item['response']}")
        if st.button(f"🗑️ حذف", key=f"delete_{i}"):
            replies.pop(i)
            save_replies(replies)
            st.experimental_rerun()

# ➕ إضافة رد جديد
st.subheader("➕ إضافة رد جديد")
new_keyword = st.text_input("🔑 الكلمة المفتاحية")
new_response = st.text_area("✉️ الرد المناسب")

if st.button("💾 حفظ الرد"):
    if not new_keyword or not new_response:
        st.warning("⚠️ الرجاء تعبئة كل الحقول")
    elif any(r["keyword"] == new_keyword.strip() for r in replies):
        st.error("⚠️ هذه الكلمة المفتاحية مضافة مسبقًا")
    else:
        replies.append({
            "keyword": new_keyword.strip(),
            "response": new_response.strip()
        })
        replies.sort(key=lambda x: x["keyword"])  # ترتيب أبجدي
        save_replies(replies)
        st.success("✅ تم الحفظ بنجاح!")
        st.experimental_rerun()
