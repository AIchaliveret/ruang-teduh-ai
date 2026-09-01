# AIJC - Ruang Teduh v1.5-simple - TANPA AVATAR FILE - Voice+Visual Emoji
import streamlit as st
from datetime import datetime
import os, csv, re

st.set_page_config(page_title="Ruang Teduh AI - Full Binding", page_icon="🌿", layout="wide")
st.markdown("""
<style>
.library-card{background:white;padding:20px;border-radius:16px;border:1px solid #E5E7EB;box-shadow:0 2px 12px rgba(0,0,0,0.04);margin-bottom:14px}
.badge{background:#E8F3ED;color:#2D5A4A;padding:4px 10px;border-radius:12px;font-size:11px;font-weight:700}
.metric-card{background:#2D5A4A;color:white;padding:12px 16px;border-radius:12px;text-align:center}
.chatbot-container{display:flex;gap:16px;align-items:flex-start;background:#F9FAFB;padding:16px;border-radius:16px;border:2px solid #E5E7EB;margin-bottom:16px}
.chatbot-avatar{width:80px;height:80px;border-radius:50%;background:#E8F3ED;display:flex;align-items:center;justify-content:center;font-size:40px;flex-shrink:0}
.chatbot-avatar.speaking{transform:scale(1.1);box-shadow:0 0 30px rgba(127,182,155,0.6);border:3px solid #7FB69B}
.binding-card{background:linear-gradient(135deg,#2D5A4A 0%,#7FB69B 100%);color:white;padding:24px;border-radius:20px;margin:16px 0}
.full-service{background:#FFFBEB;border:2px solid #F59E0B;padding:20px;border-radius:16px;margin:12px 0}
</style>
""", unsafe_allow_html=True)

CSV_FILE="members_ruang_teduh.csv"
def is_valid_email(e): return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", e) is not None
def load_members():
    if not os.path.exists(CSV_FILE): return []
    try:
        with open(CSV_FILE,"r",encoding="utf-8") as f: return list(csv.DictReader(f))
    except: return []
def save_member(nama,email,visi,masukan):
    members=load_members()
    if email.lower() in [m.get("email","").lower() for m in members]: return False,"Email sudah terdaftar!"
    fe=os.path.exists(CSV_FILE)
    with open(CSV_FILE,"a",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=["timestamp","nama","email","visi","masukan","status"])
        if not fe: w.writeheader()
        w.writerow({"timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"nama":nama,"email":email,"visi":visi,"masukan":masukan,"status":"active"})
    return True,"Berhasil!"

def chatbot_card(text,id,title="",badge=""):
    safe=text.replace("'","").replace('"',"")
    return f"""
    <div class="chatbot-container">
        <div class="chatbot-avatar" id="av{id}">🌿</div>
        <div style="flex:1">
            <div style="display:flex;justify-content:space-between;margin-bottom:8px">
                <span class="badge">{badge}</span>
                <div>
                    <button onclick="speak{id}()" style="background:#7FB69B;color:white;border:none;padding:6px 12px;border-radius:8px;margin-right:4px">🔊 Suara</button>
                    <button onclick="speak{id}()" style="background:#2D5A4A;color:white;border:none;padding:6px 12px;border-radius:8px">🎥 Visual</button>
                </div>
            </div>
            <h4>{title}</h4><p>{text}</p>
        </div>
    </div>
    <script>
    function speak{id}(){{
        window.speechSynthesis.cancel();
        let av=document.getElementById('av{id}'); av.classList.add('speaking');
        let u=new SpeechSynthesisUtterance('{safe}'); u.lang='id-ID'; u.rate=0.9;
        u.onend=function(){{av.classList.remove('speaking');}};
        window.speechSynthesis.speak(u);
    }}
    </script>
    """

if "room" not in st.session_state: st.session_state.room=1
if "profile" not in st.session_state: st.session_state.profile={}

members=load_members()
with st.sidebar:
    st.markdown(f'<div class="metric-card">📚 {len(members)}/1000<br>Siap</div>', unsafe_allow_html=True)
    if st.button("📚 Ruang 1", use_container_width=True): st.session_state.room=1
    if st.button("🎥 Ruang 2", use_container_width=True): st.session_state.room=2
    if st.button("🌟 Ruang 3", use_container_width=True): st.session_state.room=3

if st.session_state.room==1:
    st.title("📚 Ruang 1 · Perpustakaan Teduh")
    col1,col2=st.columns([1.3,1])
    with col1:
        st.info("🎥 Klik 🔊 Suara atau 🎥 Visual - Voice+Visual Chatbot!")
        st.markdown(chatbot_card("Kolose 3:23 - Apapun yang kamu perbuat, perbuatlah dengan segenap hatimu seperti untuk Tuhan. SOP: Datang 15 menit awal, 3 MIT, Review sore.", "e1", "Bekerja untuk Tuhan", "EMPLOYMENT"), unsafe_allow_html=True)
        st.markdown(chatbot_card("Amsal 16:3 - Serahkanlah perbuatanmu kepada TUHAN, maka terlaksanalah rencanamu.", "e2", "Serahkan Rencana", "ENTREPRENEURSHIP"), unsafe_allow_html=True)
    with col2:
        with st.form("f"):
            nama=st.text_input("Nama *")
            email=st.text_input("Email *")
            visi=st.text_area("Visi")
            masukan=st.text_area("Masukan *")
            s=st.form_submit_button("Simpan & Ruang 2 →", type="primary")
            if s:
                if not nama: st.error("Nama wajib!")
                elif not email: st.error("Email wajib!")
                elif not is_valid_email(email): st.error("Email salah!")
                elif not masukan: st.error("Masukan wajib!")
                else:
                    ok,msg=save_member(nama,email,visi,masukan)
                    if ok:
                        st.session_state.profile={"nama":nama,"email":email,"visi":visi,"masukan":masukan}
                        st.success("✅ Tersimpan!")
                        st.session_state.room=2
                        st.rerun()
                    else: st.warning(msg)

elif st.session_state.room==2:
    p=st.session_state.profile
    st.title(f"🎥 Ruang 2 · Voice+Visual - {p.get('nama','Member')}")
    if not p:
        st.warning("Isi Ruang 1 dulu!")
    else:
        st.markdown(f'<div class="binding-card"><h3>🌿 Shalom {p["nama"]}! Anda Ditahan di Ruang Teduh</h3><p>Betah & kerasan - Swmi Pengikat</p></div>', unsafe_allow_html=True)
        if p.get("masukan"): st.markdown(chatbot_card(p["masukan"], "m1", f"Masukan {p['nama']}", "MASUKAN ANDA"), unsafe_allow_html=True)
        st.subheader("🎙️ Rekam")
        c1,c2=st.columns(2)
        with c1: a=st.audio_input("Rekam"); 
        with c2: v=st.file_uploader("Video", type=["mp4","webm","mov"]); 
        if v: st.video(v)
        if st.button("🌟 Masuk Ruang 3 →", type="primary", use_container_width=True):
            st.session_state.room=3
            st.rerun()

else:
    st.title("🌟 Ruang 3 · Full Member - Tabur Tuai")
    p=st.session_state.profile
    if p: st.success(f"Member: {p.get('nama')} - {p.get('email')}")
    c1,c2=st.columns(2)
    with c1:
        st.markdown('<div class="full-service"><h3>🌿 TAVO Rp149k</h3></div>', unsafe_allow_html=True)
        if st.button("Pilih TAVO", use_container_width=True): st.balloons(); st.success("Tavo!")
    with c2:
        st.markdown('<div class="full-service"><h3>🌟 MALKHUTKHA Rp399k</h3><p>Full Binding Istimewa</p></div>', unsafe_allow_html=True)
        if st.button("Pilih MALKHUTKHA", type="primary", use_container_width=True): st.balloons(); st.success("MALKHUTKHA!")
