# AIJC - Ruang Teduh v1.5 - FULL BINDING - Voice + Visual Video Chatbot + Tabur Tuai
import streamlit as st
from datetime import datetime
import os, csv, re, base64

st.set_page_config(page_title="Ruang Teduh AI - Full Binding", page_icon="🌿", layout="wide")

# Load avatar image as base64 for HTML
AVATAR_PATH = "/mnt/data/resource/aijc_peaceful_avatar.webp"
avatar_b64 = ""
if os.path.exists(AVATAR_PATH):
    with open(AVATAR_PATH, "rb") as f:
        avatar_b64 = base64.b64encode(f.read()).decode()

st.markdown("""
<style>
.library-card{background:white;padding:20px;border-radius:16px;border:1px solid #E5E7EB;box-shadow:0 2px 12px rgba(0,0,0,0.04);margin-bottom:14px}
.badge{background:#E8F3ED;color:#2D5A4A;padding:4px 10px;border-radius:12px;font-size:11px;font-weight:700}
.badge-emp{background:#DBEAFE;color:#1E40AF}
.badge-ent{background:#FEF3C7;color:#92400E}
.badge-bind{background:#FDE68A;color:#92400E;border:1px solid #F59E0B}
.metric-card{background:#2D5A4A;color:white;padding:12px 16px;border-radius:12px;text-align:center}
.chatbot-container{display:flex;gap:16px;align-items:flex-start;background:#F9FAFB;padding:16px;border-radius:16px;border:2px solid #E5E7EB;margin-bottom:16px}
.chatbot-avatar{width:80px;height:80px;border-radius:50%;background:#E8F3ED;display:flex;align-items:center;justify-content:center;font-size:40px;flex-shrink:0;transition:all 0.3s}
.chatbot-avatar.speaking{transform:scale(1.1);box-shadow:0 0 30px rgba(127,182,155,0.6);border:3px solid #7FB69B;animation:pulse 1s infinite}
@keyframes pulse{0%{transform:scale(1.1)}50%{transform:scale(1.15)}100%{transform:scale(1.1)}}
.binding-card{background:linear-gradient(135deg,#2D5A4A 0%,#7FB69B 100%);color:white;padding:24px;border-radius:20px;margin:16px 0;box-shadow:0 8px 24px rgba(45,90,74,0.3)}
.full-service{background:#FFFBEB;border:2px solid #F59E0B;padding:20px;border-radius:16px;margin:12px 0}
.tabur-card{background:white;border-left:4px solid #7FB69B;padding:16px;margin:8px 0;border-radius:0 12px 12px 0}
</style>
""", unsafe_allow_html=True)

CSV_FILE="members_ruang_teduh.csv"
def is_valid_email(e): return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", e) is not None
def load_members():
    if not os.path.exists(CSV_FILE): return []
    try:
        with open(CSV_FILE,"r",encoding="utf-8") as f: return list(csv.DictReader(f))
    except: return []
def save_member(nama,email,visi,kesan,masukan):
    members=load_members()
    if email.lower() in [m.get("email","").lower() for m in members]: return False,"Email sudah terdaftar!"
    fe=os.path.exists(CSV_FILE)
    with open(CSV_FILE,"a",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=["timestamp","nama","email","visi","kesan","masukan","status","binding"])
        if not fe: w.writeheader()
        w.writerow({"timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"nama":nama,"email":email,"visi":visi,"kesan":kesan,"masukan":masukan,"status":"active","binding":"Ruang2"})
    return True,"Berhasil!"

def chatbot_visual_card(text, id, title="", badge_text="", avatar_char="🌿"):
    safe=text.replace("'","").replace('"',"").replace("\n"," ")
    # Chatbot visual with voice + video avatar
    avatar_img = f'<img src="data:image/webp;base64,{avatar_b64}" style="width:100%;height:100%;border-radius:50%;object-fit:cover">' if avatar_b64 else avatar_char
    return f"""
    <div class="chatbot-container">
        <div class="chatbot-avatar" id="avatar{id}">{avatar_img}</div>
        <div style="flex:1">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
                <span class="badge">{badge_text}</span>
                <div>
                    <button onclick="speakVisual{id}()" style="background:#7FB69B;color:white;border:none;padding:6px 12px;border-radius:8px;margin-right:4px;cursor:pointer">🔊 Suara</button>
                    <button onclick="speakVisual{id}();startVideo{id}()" style="background:#2D5A4A;color:white;border:none;padding:6px 12px;border-radius:8px;cursor:pointer">🎥 Suara+Visual</button>
                </div>
            </div>
            <h4 style="margin:0 0 6px 0">{title}</h4>
            <p style="margin:0;color:#374151;line-height:1.6">{text}</p>
            <div id="video{id}" style="display:none;margin-top:12px;padding:12px;background:#111827;color:#10B981;border-radius:12px;font-family:monospace;font-size:12px">
                🎥 AIJC Visual Chatbot sedang berbicara...<br>
                <span style="color:#7FB69B">▶ Video Avatar aktif - Suara + Gambar bergerak</span>
            </div>
        </div>
    </div>
    <script>
    function speakVisual{id}(){{
        window.speechSynthesis.cancel();
        let avatar=document.getElementById('avatar{id}');
        avatar.classList.add('speaking');
        let u=new SpeechSynthesisUtterance(`{safe}`);
        u.lang='id-ID'; u.rate=0.9; u.pitch=1.0;
        u.onend=function(){{ avatar.classList.remove('speaking'); document.getElementById('video{id}').style.display='none'; }};
        u.onstart=function(){{ document.getElementById('video{id}').style.display='block'; }};
        window.speechSynthesis.speak(u);
    }}
    function startVideo{id}(){{
        document.getElementById('video{id}').style.display='block';
        document.getElementById('video{id}').innerHTML='🎥 Visual Video Chatbot AIJC<br><span style=\"color:#7FB69B\">Avatar bergerak + suara nasehat - Member betah & kerasan ditahan!</span><br><br>📹 [Simulasi Video Avatar]<br>AIJC sedang mengucapkan nasehat dengan visual...';
    }}
    </script>
    """

if "room" not in st.session_state: st.session_state.room=1
if "profile" not in st.session_state: st.session_state.profile={}
if "my_cards" not in st.session_state: st.session_state.my_cards=[]

members=load_members()
with st.sidebar:
    st.markdown("### 🌿 Ruang Teduh AI\n**Full Binding**")
    st.markdown(f'<div class="metric-card">📚 {len(members)}/1000<br>Siap Tabur Tuai</div>', unsafe_allow_html=True)
    st.progress(min(len(members)/1000,1.0))
    st.divider()
    if st.button("📚 Ruang 1 - Perpustakaan", use_container_width=True): st.session_state.room=1
    if st.button("🎥 Ruang 2 - Voice+Visual Chatbot", use_container_width=True): st.session_state.room=2
    if st.button("🌟 Ruang 3 - Full Member Istimewa", use_container_width=True): st.session_state.room=3
    st.divider()
    st.caption("🎥 Voice+Visual: Avatar AIJC berbicara nasehat - Member betah & kerasan")

if st.session_state.room==1:
    st.title("📚 Ruang 1 · Perpustakaan Teduh")
    st.caption("Perpustakaan nasehat - Klik Suara atau Suara+Visual - Hemat TTS 0KB")
    col_lib, col_form = st.columns([1.3,1])
    with col_lib:
        st.subheader("📖 Koleksi - Voice + Visual Chatbot")
        st.info("🎥 Baru! Setiap nasehat bisa Suara saja (0KB) atau Suara+Visual Video Chatbot Avatar!")
        
        st.markdown("#### 💼 Employment Journey - Dengan Visual")
        emp1="Kolose 3:23 - Apapun juga yang kamu perbuat, perbuatlah dengan segenap hatimu seperti untuk Tuhan, dan bukan untuk manusia. SOP: Datang 15 menit lebih awal, Tulis 3 MIT harian, Review sore 10 menit."
        st.markdown(chatbot_visual_card(emp1, "emp1v", "Bekerja untuk Tuhan - Voice+Visual", "EMPLOYMENT + VISUAL"), unsafe_allow_html=True)
        
        emp2="Filipi 4:6-7 - Janganlah hendaknya kamu kuatir tentang apapun juga, tetapi nyatakanlah dalam segala hal keinginanmu kepada Allah dalam doa. Damai sejahtera Allah akan memelihara hati dan pikiranmu."
        st.markdown(chatbot_visual_card(emp2, "emp2v", "Anti Cemas - Chatbot Visual", "EMPLOYMENT + VISUAL"), unsafe_allow_html=True)
        
        st.markdown("#### 💡 Entrepreneurship Journey - Visual")
        ent1="Amsal 16:3 - Serahkanlah perbuatanmu kepada TUHAN, maka terlaksanalah segala rencanamu. SOP Usaha: HPP jelas, profit 20 persen, pisah uang pribadi dan usaha. OEE Bisnis."
        st.markdown(chatbot_visual_card(ent1, "ent1v", "Serahkan Rencana - Visual", "ENTREPRENEURSHIP + VISUAL"), unsafe_allow_html=True)
        
        st.markdown("#### 🌟 Ladang Kebenaran")
        ladang="Mazmur 23:1-3 - TUHAN adalah gembalaku, takkan kekurangan aku. Tabur tuai - Apa yang kamu tabur dalam kebenaran, akan kamu tuai dalam hidup. Ladang kebenaran dan hidup menanti."
        st.markdown(chatbot_visual_card(ladang, "ladang", "Ladang Kebenaran - Tabur Tuai", "TABUR TUAI"), unsafe_allow_html=True)
    
    with col_form:
        st.subheader("📝 Jadi Member - Dapat Voice+Visual")
        with st.form("member_v15"):
            nama=st.text_input("Nama Lengkap *")
            email=st.text_input("Email * WAJIB")
            visi=st.text_area("Visi", placeholder="Visi Anda akan dibacakan chatbot visual...")
            masukan=st.text_area("Masukan Culture *", placeholder="Masukan Anda akan jadi video chatbot!")
            submit=st.form_submit_button("🌟 Simpan & Masuk Ruang 2 Voice+Visual →", type="primary", use_container_width=True)
            if submit:
                if not nama: st.error("Nama wajib!")
                elif not email: st.error("Email wajib!")
                elif not is_valid_email(email): st.error("Format email salah!")
                elif not masukan: st.error("Masukan wajib!")
                else:
                    ok,msg=save_member(nama,email,visi,"",masukan)
                    if ok:
                        st.session_state.profile={"nama":nama,"email":email,"visi":visi,"masukan":masukan}
                        st.success(f"✅ {nama} - Siap Voice+Visual di Ruang 2!")
                        st.balloons()
                        st.session_state.room=2
                        st.rerun()
                    else:
                        st.warning(msg)
                        st.session_state.room=2
                        st.rerun()

elif st.session_state.room==2:
    p=st.session_state.profile
    st.title(f"🎥 Ruang 2 · Voice + Visual Chatbot - {p.get('nama','Member')}")
    st.caption("Sudah dibuat suara dan visual video bahkan seperti gambar chatbot visual - Dari pesan dan nasehat di kolom - Mereka betah dan kerasan ditahan")
    
    if not p:
        st.warning("Isi form Ruang 1 dulu!")
        if st.button("Ke Ruang 1"): st.session_state.room=1; st.rerun()
    else:
        # Chatbot visual utama
        st.markdown(f"""
        <div class="binding-card">
            <h3 style="margin:0 0 8px 0">🌿 Shalom {p['nama']}! Anda Ditahan di Ruang Teduh</h3>
            <p style="margin:0;opacity:0.9">Swmi Pengikat - Kasih yang menahan Anda betah & kerasan di sini. Chatbot visual AIJC akan membacakan masukan Anda dengan suara + video avatar!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("👂 Masukan Anda - Jadi Suara + Visual Video Chatbot")
        if p.get("masukan"):
            st.markdown(chatbot_visual_card(p["masukan"], "mymasuk_v", f"Masukan {p['nama']} - Voice+Visual Chatbot", "MASUKAN ANDA - VISUAL"), unsafe_allow_html=True)
            st.caption("🎥 Klik Suara+Visual - Lihat avatar AIJC bergerak + suara membacakan masukan Anda!")
        
        if p.get("visi"):
            st.markdown(chatbot_visual_card(p["visi"], "myvisi_v", f"Visi {p['nama']} - Chatbot Visual", "VISI ANDA - VISUAL"), unsafe_allow_html=True)
        
        st.divider()
        st.subheader("🎙️ Rekam Setelah Mendengarkan Voice+Visual")
        col1,col2=st.columns(2)
        with col1:
            st.markdown("**🎤 Audio Record - Hemat**")
            audio=st.audio_input("Rekam respon setelah lihat visual chatbot")
            if audio: st.success("Audio tersimpan! Anda betah!")
        with col2:
            st.markdown("**📹 Video Visual - Lebih Menarik**")
            video=st.file_uploader("Upload video refleksi Anda", type=["mp4","webm","mov"])
            if video: 
                st.video(video)
                st.caption("Video Anda + Video Chatbot AIJC = Double visual!")
        
        st.divider()
        # Pengikat langsung ajak jadi member full
        st.markdown(f"""
        <div class="binding-card">
            <h2 style="margin:0 0 12px 0">🌟 Anda Sudah Betah & Kerasan Ditahan!</h2>
            <p style="margin:0 0 16px 0;font-size:16px">Swmi Pengikat - Kasih di Ruang Teduh telah menahan Anda. Anda merasakan kedamaian, suara + visual chatbot yang membacakan nasehat & masukan Anda.</p>
            <p style="margin:0 0 16px 0;font-weight:bold">Ini saatnya naik ke Ruang 3 - Full Member Istimewa dengan motivasi dan pelayanan full cooperate dalam ladang kebenaran dan hidup!</p>
            <p style="margin:0;opacity:0.9">Tabur tuai - Tanam benih baik di ladang kebenaran, tuai hasil full berlangganan!</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🌟 LANGSUNG AJAK JADI MEMBER FULL - Masuk Ruang 3 Istimewa →", type="primary", use_container_width=True):
            st.session_state.room=3
            st.rerun()

else:
    # RUANG 3 - FULL MEMBER ISTIMEWA
    st.title("🌟 Ruang 3 · Full Member Istimewa - Tabur Tuai")
    st.caption("Istimewah dengan motivasi dan pelayanan full cooperate dalam ladang kebenaran dan hidup")
    
    p=st.session_state.profile
    if p:
        st.success(f"Member: {p.get('nama')} - {p.get('email')} - Sudah ditahan di Ruang 2, siap Full Binding!")
    
    st.markdown("""
    <div class="binding-card">
        <h2 style="margin:0 0 12px 0">🌱 Tabur Tuai - Menanam Benih Baik di Ladang Kebenaran</h2>
        <p style="margin:0;font-size:16px">Dkbrjanh 2 kita harus bisa menanamkan benih baik dan bisa memberikan member kalo terikat maksudnya berlangganan full hasilnya. Apa yang member tabur dalam kebenaran, akan dituai dalam hidup berkelimpahan.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1,col2=st.columns(2)
    with col1:
        st.markdown("""
        <div class="full-service">
            <h3>🌿 TAVO - Member Dasar - Rp149k/bulan</h3>
            <ul>
                <li>✅ Akses Perpustakaan Voice+Visual Chatbot full</li>
                <li>✅ Motivasi via email mingguan</li>
                <li>✅ Recording Studio Audio & Video</li>
                <li>✅ SOP Employment & Entrepreneurship</li>
                <li>✅ Community 1000 Member</li>
            </ul>
            <p><b>Cocok untuk:</b> Mulai menabur benih baik</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🌱 Tabur Benih - Pilih TAVO Rp149k", use_container_width=True):
            st.balloons()
            st.success("Tavo! Anda menabur benih pertama di ladang kebenaran!")
    
    with col2:
        st.markdown("""
        <div class="full-service" style="border:2px solid #2D5A4A;background:#E8F3ED">
            <h3>🌟 MALKHUTKHA - Full Member Istimewa - Rp399k/bulan</h3>
            <ul>
                <li>🔥 <b>Pelayanan Full Cooperate</b> dalam ladang kebenaran dan hidup</li>
                <li>🔥 <b>Membangkitkan</b> potensi penuh member</li>
                <li>🔥 <b>Layanan Full</b> - Jasa dan mendapatkan apa yang member inginkan</li>
                <li>🔥 <b>Benih Baik</b> - Menanamkan benih baik, hasil berlipat</li>
                <li>🔥 <b>Berlangganan Full Hasilnya</b> - Tabur tuai nyata</li>
                <li>🔥 1-on-1 Coaching AIJC + Mentor</li>
                <li>🔥 Full Binding - Kerasan & Betah selamanya</li>
            </ul>
            <p><b>Istimewah:</b> Untuk yang siap terikat full & tuai hasil!</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🌟 FULL BINDING - Pilih MALKHUTKHA Rp399k", type="primary", use_container_width=True):
            st.balloons()
            st.success("MALKHUTKHA! Full Binding! Anda terikat dalam ladang kebenaran dan hidup - Siap tuai hasil berlipat! Tavo Malkhutkha!")
    
    st.divider()
    st.subheader("🌱 Ladang Kebenaran dan Hidup - Apa yang Member Inginkan")
    st.markdown("""
    <div class="tabur-card">
        <b>🌾 Tabur:</b> Waktu, masukan, komitmen di Ruang Teduh
    </div>
    <div class="tabur-card">
        <b>🌱 Benih Baik:</b> SOP Kerja, SOP Usaha, Firman, Motivasi, Visual Chatbot
    </div>
    <div class="tabur-card">
        <b>🌟 Tumbuh:</b> Pelayanan full cooperate - Dibangkitkan & dilayani full
    </div>
    <div class="tabur-card">
        <b>🌾 Tuai:</b> Hasil full - Mendapatkan apa yang member inginkan karena berlangganan full - Tabur tuai nyata!
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **Kenapa Ruang 3 Istimewa?** Karena di Ruang 2 mereka sudah betah & kerasan ditahan oleh suara + visual video chatbot. Swmi pengikat kasih sudah bekerja. Langsung ajak jadi member full - mereka siap berlangganan untuk tuai hasil di ladang kebenaran dan hidup!")
    
    members=load_members()
    if len(members)>0:
        st.divider()
        st.caption(f"📧 {len(members)} calon member full sudah ditahan di Ruang 2")
        import pandas as pd
        df=pd.DataFrame(members)
        st.dataframe(df,use_container_width=True)
