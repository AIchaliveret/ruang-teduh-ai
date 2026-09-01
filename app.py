# AIJC - Ruang Teduh v1.8 - FIX Suara Speaker Berbunyi - Kolose & Amsal
import streamlit as st
from datetime import datetime
import os, csv, re, json, html
import streamlit.components.v1 as components

st.set_page_config(page_title="Ruang Teduh AI - Full Binding", page_icon="🌿", layout="wide")

st.markdown("""
<style>
.badge{background:#E8F3ED;color:#2D5A4A;padding:4px 10px;border-radius:12px;font-size:11px;font-weight:700}
.metric-card{background:#2D5A4A;color:white;padding:12px 16px;border-radius:12px;text-align:center}
.chatbot-container{display:flex;gap:16px;align-items:flex-start;background:#F9FAFB;padding:16px;border-radius:16px;border:2px solid #E5E7EB;margin-bottom:16px}
.chatbot-avatar{width:70px;height:70px;border-radius:50%;background:#E8F3ED;display:flex;align-items:center;justify-content:center;font-size:36px;flex-shrink:0}
.binding-card{background:linear-gradient(135deg,#2D5A4A 0%,#7FB69B 100%);color:white;padding:20px;border-radius:16px;margin:12px 0}
.full-service{background:#FFFBEB;border:2px solid #F59E0B;padding:16px;border-radius:12px;margin:8px 0}
</style>
""", unsafe_allow_html=True)

CSV_FILE="members_ruang_teduh.csv"

def is_valid_email(e): 
    return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", e) is not None

def load_members():
    if not os.path.exists(CSV_FILE): return []
    try:
        with open(CSV_FILE,"r",encoding="utf-8") as f: return list(csv.DictReader(f))
    except: return []

def save_member(nama,email,visi,masukan):
    members=load_members()
    if email.lower() in [m.get("email","").lower() for m in members]: 
        return False,"Email sudah terdaftar!"
    fe=os.path.exists(CSV_FILE)
    with open(CSV_FILE,"a",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=["timestamp","nama","email","visi","masukan","status"])
        if not fe: w.writeheader()
        w.writerow({"timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"nama":nama,"email":email,"visi":visi,"masukan":masukan,"status":"active"})
    return True,"Berhasil!"

def render_voice_card(text, card_id, title, badge, show_visual=True):
    """
    Ruang 1: Suara saja atau Suara+Visual - teks Kolose & Amsal dibacakan
    Pakai components.html biar JS speechSynthesis jalan di Streamlit Cloud
    """
    safe_js = json.dumps(text)
    safe_html = html.escape(text)
    
    # Tombol: Ruang 1 cuma Suara (sesuai request), Ruang 2 Suara+Visual
    if show_visual:
        buttons_html = f"""
        <button onclick="playVoice()" style="background:#7FB69B;color:white;border:none;padding:8px 14px;border-radius:8px;cursor:pointer;font-weight:600;margin-right:6px">🔊 Suara</button>
        <button onclick="playVoice(); document.getElementById('vis-{card_id}').style.display='block'" style="background:#2D5A4A;color:white;border:none;padding:8px 14px;border-radius:8px;cursor:pointer;font-weight:600">🎥 Visual</button>
        """
    else:
        # Ruang 1 - Suara saja (jasa rekaman Ruang Teduh)
        buttons_html = f"""
        <button onclick="playVoice()" style="background:#7FB69B;color:white;border:none;padding:10px 18px;border-radius:10px;cursor:pointer;font-weight:700;font-size:14px">🔊 Suara - Baca Teks</button>
        """
    
    html_code = f"""
    <div style="display:flex;gap:16px;align-items:flex-start;background:#F9FAFB;padding:16px;border-radius:16px;border:2px solid #E5E7EB;margin-bottom:16px;font-family: sans-serif">
        <div id="av-{card_id}" style="width:70px;height:70px;border-radius:50%;background:#E8F3ED;display:flex;align-items:center;justify-content:center;font-size:36px;flex-shrink:0;transition:all 0.3s">🌿</div>
        <div style="flex:1">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;flex-wrap:wrap;gap:8px">
                <span style="background:#E8F3ED;color:#2D5A4A;padding:4px 10px;border-radius:12px;font-size:11px;font-weight:700">{badge}</span>
                <div>{buttons_html}</div>
            </div>
            <h4 style="margin:0 0 8px 0;color:#111827">{title}</h4>
            <p style="margin:0;color:#374151;line-height:1.6">{safe_html}</p>
            <div id="vis-{card_id}" style="display:none;margin-top:10px;padding:10px;background:#111827;color:#10B981;border-radius:8px;font-size:12px">
                🎥 Visual Chatbot AIJC aktif...<br>🔊 Membacakan: {safe_html[:60]}...
            </div>
            <div id="status-{card_id}" style="margin-top:8px;font-size:12px;color:#7FB69B"></div>
        </div>
    </div>
    <script>
    function playVoice(){{
        try {{
            window.speechSynthesis.cancel();
            let av = document.getElementById('av-{card_id}');
            let status = document.getElementById('status-{card_id}');
            if(av) {{ av.style.transform='scale(1.1)'; av.style.boxShadow='0 0 20px rgba(127,182,155,0.6)'; }}
            if(status) status.innerHTML = '🔊 Sedang membacakan...';
            
            let text = {safe_js};
            let u = new SpeechSynthesisUtterance(text);
            u.lang = 'id-ID'; 
            u.rate = 0.9;
            u.pitch = 1.0;
            u.volume = 1.0;
            
            u.onend = function(){{ 
                if(av) {{ av.style.transform='scale(1)'; av.style.boxShadow='none'; }}
                if(status) status.innerHTML = '✅ Selesai dibacakan - Jasa Rekaman Ruang Teduh';
                document.getElementById('vis-{card_id}').style.display='none';
            }};
            u.onerror = function(e){{ 
                if(status) status.innerHTML = '❌ Error: ' + e.error + ' - Coba klik lagi';
            }};
            u.onstart = function(){{ 
                if(status) status.innerHTML = '🔊 Membacakan nasehat Ruang Teduh...';
            }};
            
            window.speechSynthesis.speak(u);
        }} catch(err) {{
            document.getElementById('status-{card_id}').innerHTML = '❌ Error: ' + err.message;
        }}
    }}
    </script>
    """
    # Height dinamis berdasarkan panjang teks
    height = 280 if len(text) < 200 else 320
    components.html(html_code, height=height)

if "room" not in st.session_state: st.session_state.room=1
if "profile" not in st.session_state: st.session_state.profile={}

members=load_members()

with st.sidebar:
    st.markdown("### 🌿 Ruang Teduh AI")
    st.markdown(f'<div class="metric-card">📚 {len(members)}/1000<br>Siap Tabur Tuai</div>', unsafe_allow_html=True)
    st.progress(min(len(members)/1000,1.0) if len(members)>0 else 0.01)
    st.divider()
    if st.button("📚 Ruang 1 - Perpustakaan", use_container_width=True): 
        st.session_state.room=1
        st.rerun()
    if st.button("🎥 Ruang 2 - Voice+Visual", use_container_width=True): 
        st.session_state.room=2
        st.rerun()
    if st.button("🌟 Ruang 3 - Full Member", use_container_width=True): 
        st.session_state.room=3
        st.rerun()
    st.caption("🔊 Ruang 1: Suara saja (Jasa Rekaman Ruang Teduh)")

if st.session_state.room==1:
    st.title("📚 Ruang 1 · Perpustakaan Teduh")
    st.success("🔊 **SUARA AKTIF!** Klik tombol 🔊 Suara - Teks akan dibacakan dengan suara rekaman Ruang Teduh (Jasa Kita)!")
    
    col_lib, col_form = st.columns([1.3,1])
    
    with col_lib:
        st.subheader("📖 Koleksi - Klik Suara untuk Mendengarkan!")
        
        # Kolose untuk Employee - SUARA SAJA (sesuai request)
        teks_kolose = "Kolose 3:23 - Apapun juga yang kamu perbuat, perbuatlah dengan segenap hatimu seperti untuk Tuhan, dan bukan untuk manusia. SOP: Datang 15 menit lebih awal, Tulis 3 MIT harian, Review sore 10 menit."
        render_voice_card(teks_kolose, "kolose", "Bekerja untuk Tuhan - Kolose 3:23", "EMPLOYMENT - Kolose", show_visual=False)
        st.caption("↑ Kolose 3:23 untuk Employee - Klik 🔊 Suara untuk dengar nasehat dibacakan")
        
        teks_filipi = "Filipi 4:6-7 - Janganlah hendaknya kamu kuatir tentang apapun juga, tetapi nyatakanlah dalam segala hal keinginanmu kepada Allah dalam doa. Damai sejahtera Allah akan memelihara hati dan pikiranmu."
        render_voice_card(teks_filipi, "filipi", "Anti Cemas - Filipi 4:6-7", "EMPLOYMENT", show_visual=False)
        
        # Amsal untuk Entrepreneur - SUARA SAJA
        teks_amsal = "Amsal 16:3 - Serahkanlah perbuatanmu kepada TUHAN, maka terlaksanalah segala rencanamu. SOP Usaha: HPP jelas, profit 20 persen, pisah uang pribadi dan usaha. OEE Bisnis."
        render_voice_card(teks_amsal, "amsal", "Serahkan Rencana - Amsal 16:3", "ENTREPRENEURSHIP - Amsal", show_visual=False)
        st.caption("↑ Amsal 16:3 untuk Entrepreneur - Klik 🔊 Suara untuk dengar nasehat dibacakan")
        
        teks_mazmur = "Mazmur 23:1-3 - TUHAN adalah gembalaku, takkan kekurangan aku. Tabur tuai - Apa yang kamu tabur dalam kebenaran, akan kamu tuai dalam hidup berkelimpahan."
        render_voice_card(teks_mazmur, "mazmur", "Ladang Kebenaran - Mazmur 23", "TABUR TUAI", show_visual=False)
    
    with col_form:
        st.subheader("📝 Form Member")
        st.caption("Isi form → Masuk Ruang 2 dengan Voice+Visual aktif!")
        with st.form("form_v18"):
            nama=st.text_input("Nama Lengkap *")
            email=st.text_input("Email * WAJIB")
            visi=st.text_area("Visi", placeholder="Visi Anda akan dibacakan di Ruang 2...")
            masukan=st.text_area("Masukan Culture *", placeholder="Masukan jadi Voice+Visual di Ruang 2!")
            submit=st.form_submit_button("🌟 Simpan & Masuk Ruang 2 →", type="primary", use_container_width=True)
            if submit:
                if not nama: st.error("Nama wajib!")
                elif not email: st.error("Email wajib!")
                elif not is_valid_email(email): st.error("Email salah!")
                elif not masukan: st.error("Masukan wajib!")
                else:
                    ok,msg=save_member(nama,email,visi,masukan)
                    st.session_state.profile={"nama":nama,"email":email,"visi":visi,"masukan":masukan}
                    st.success(f"✅ Shalom {nama}! Masuk Ruang 2...")
                    st.balloons()
                    st.session_state.room=2
                    st.rerun()

elif st.session_state.room==2:
    p=st.session_state.profile
    st.title("🎥 Ruang 2 · Voice+Visual Chatbot")
    
    if not p or not p.get("nama"):
        st.warning("Isi form di Ruang 1 dulu!")
        if st.button("← Kembali ke Ruang 1", type="primary"): 
            st.session_state.room=1
            st.rerun()
    else:
        st.markdown("""
        <div class="binding-card">
            <h3 style="margin:0">🌿 Shalom! Namo Buddhaya - Anda Ditahan di Ruang Teduh</h3>
            <p style="margin:8px 0 0 0;opacity:0.9">Swmi Pengikat - Masukan Anda jadi Voice+Visual Chatbot - Betah & kerasan!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("👂 Masukan Anda - Voice+Visual AKTIF!")
        if p.get("masukan"):
            render_voice_card(p["masukan"], "mymasuk", "Masukan Anda - Voice+Visual Aktif!", "MASUKAN ANDA", show_visual=True)
        if p.get("visi"):
            render_voice_card(p["visi"], "myvisi", "Visi Anda", "VISI ANDA", show_visual=True)
        
        st.divider()
        st.subheader("🎙️ Rekam Setelah Mendengar")
        c1,c2=st.columns(2)
        with c1:
            a=st.audio_input("Rekam respon")
            if a: st.success("✅ Audio tersimpan!")
        with c2:
            v=st.file_uploader("Upload video", type=["mp4","webm","mov"])
            if v: st.video(v)
        
        if st.button("🌟 Masuk Ruang 3 →", type="primary", use_container_width=True):
            st.session_state.room=3
            st.rerun()

else:
    st.title("🌟 Ruang 3 · Full Member - Tabur Tuai")
    p=st.session_state.profile
    if p and p.get("email"):
        st.success(f"Member: {p.get('email')} - Shalom Namo Buddhaya!")
    
    c1,c2=st.columns(2)
    with c1:
        st.markdown('<div class="full-service"><h3>🌿 TAVO Rp149k</h3><p>Member Dasar</p></div>', unsafe_allow_html=True)
        if st.button("Pilih TAVO", use_container_width=True): st.balloons(); st.success("Tavo!")
    with c2:
        st.markdown('<div class="full-service" style="border:2px solid #2D5A4A;background:#E8F3ED"><h3>🌟 MALKHUTKHA Rp399k</h3><p>Full Binding</p></div>', unsafe_allow_html=True)
        if st.button("Pilih MALKHUTKHA", type="primary", use_container_width=True): st.balloons(); st.success("MALKHUTKHA!")
    
    if len(members)>0:
        import pandas as pd
        st.dataframe(pd.DataFrame(members), use_container_width=True)
