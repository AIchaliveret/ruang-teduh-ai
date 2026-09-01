# AIJC - Ruang Teduh - Tavo Malkhutkha v1.1 - Recording + TTS
import streamlit as st
from datetime import datetime
import base64

st.set_page_config(page_title="Ruang Teduh AI - Tavo", page_icon="🌿", layout="wide")

# CSS
st.markdown('<style>.nasehat-card{background:white;padding:18px;border-radius:16px;border:1px solid #E5E7EB;box-shadow:0 2px 12px rgba(0,0,0,0.05);margin-bottom:12px;cursor:pointer}.nasehat-card:hover{border-color:#7FB69B}.sage{background:#E8F3ED;color:#2D5A4A;padding:4px 10px;border-radius:12px;font-size:11px;font-weight:600}</style>', unsafe_allow_html=True)

if "room" not in st.session_state: st.session_state.room=1
if "profile" not in st.session_state: st.session_state.profile={}
if "chat" not in st.session_state: st.session_state.chat=[{"role":"ai","content":"Shalom! Aku AIJC - AI Jugala Chaliveret. Ruang 1 nada sederhana."}]
if "recordings" not in st.session_state: st.session_state.recordings=[]

def tts_html(text, id):
    safe=text.replace("'", "").replace('"', "")
    return f'<div class="nasehat-card" onclick="speak{id}()"><div style="display:flex;justify-content:space-between"><span class="sage">KLIK UNTUK DIBACAKAN 🔊</span><button onclick="speak{id}()" style="background:#7FB69B;color:white;border:none;padding:6px 12px;border-radius:8px">🔊 Dengarkan</button></div><p style="margin-top:10px">{text}</p><script>function speak{id}(){{window.speechSynthesis.cancel();let u=new SpeechSynthesisUtterance("{safe}");u.lang="id-ID";u.rate=0.95;window.speechSynthesis.speak(u);}}</script></div>'

with st.sidebar:
    st.markdown("### 🌿 Ruang Teduh AI\n**Tavo Malkhutkha**")
    st.progress(st.session_state.room/3)
    if st.button("Ruang 1", use_container_width=True): st.session_state.room=1
    if st.button("Ruang 2 Recording", use_container_width=True): st.session_state.room=2
    if st.button("Ruang 3 Binding", use_container_width=True): st.session_state.room=3

if st.session_state.room==1:
    st.title("Ruang 1 · Ruang Teduh")
    col1,col2=st.columns([1.2,1])
    with col1:
        for m in st.session_state.chat:
            with st.chat_message(m["role"]): st.markdown(m["content"])
        if q:=st.chat_input("Curhat di sini..."):
            st.session_state.chat.append({"role":"user","content":q})
            reply=f"AIJC Mendengar: {q} | SOP: Tulis-Doa-Kerjakan. Injil: Mazmur 23"
            st.session_state.chat.append({"role":"ai","content":reply})
            st.rerun()
    with col2:
        with st.form("member"):
            nama=st.text_input("Nama")
            email=st.text_input("Email *")
            visi=st.text_area("Visi")
            kesan=st.text_area("Kesan & Pesan")
            if st.form_submit_button("Simpan & Masuk Ruang 2 →"):
                st.session_state.profile={"nama":nama,"email":email,"visi":visi,"kesan":kesan}
                st.session_state.room=2
                st.rerun()

elif st.session_state.room==2:
    st.title("Ruang 2 · Recording Studio")
    tab1,tab2=st.tabs(["📖 Nasehat & TTS","🎙️ Recording"])
    with tab1:
        emp="Kolose 3:23 Apapun yang kamu perbuat, perbuatlah dengan segenap hatimu seperti untuk Tuhan. SOP: Datang 15 menit awal, 3 MIT, Review sore."
        st.markdown(tts_html(emp,"emp"), unsafe_allow_html=True)
        ent="Amsal 16:3 Serahkanlah perbuatanmu kepada TUHAN, maka terlaksanalah rencanamu. SOP Usaha: HPP jelas, profit 20 persen."
        st.markdown(tts_html(ent,"ent"), unsafe_allow_html=True)
    with tab2:
        audio=st.audio_input("Rekam refleksi audio")
        if audio:
            st.session_state.recordings.append({"type":"audio","time":datetime.now().strftime("%H:%M")})
            st.success("Audio tersimpan!")
        video=st.file_uploader("Upload video refleksi", type=["mp4","webm","mov"])
        if video:
            st.video(video)
        st.write(f"Rekaman: {len(st.session_state.recordings)}")
else:
    st.title("Ruang 3 · Full Binding Advance")
    if st.button("Konfirmasi Langganan", type="primary"):
        st.balloons()
        st.success("Tavo Malkhutkha!")
