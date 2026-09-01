"""
Ruang Teduh - callback.py - Webhook Midtrans QRIS/VA/GoPay/OVO auto aktifkan langganan
Deploy: pisah dari app.py Streamlit, bisa di Railway / Render / Fly.io / VPS
URL Notifikasi di Midtrans Dashboard: https://your-domain.com/midtrans-callback

Pas user scan QRIS Rp200rb -> Midtrans kirim POST ke sini -> auto update GDrive/Supabase -> member asuveleikha@gmail.com jadi aktif -> bisa masuk Ruang 3
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import hashlib, os, json, time
from datetime import datetime

app = FastAPI(title="Ruang Teduh Webhook v2.7")

# --- CONFIG ---
MIDTRANS_SERVER_KEY = os.getenv("MIDTRANS_SERVER_KEY", "SB-Mid-server-xxxx")
# GDrive
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "1xxx-xxxx")
# Supabase (pilih salah satu atau dua-duanya)
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

def verify_midtrans_signature(order_id, status_code, gross_amount, signature_key):
    """Verifikasi SHA512(order_id+status_code+gross_amount+server_key)"""
    my_signature = hashlib.sha512(f"{order_id}{status_code}{gross_amount}{MIDTRANS_SERVER_KEY}".encode()).hexdigest()
    return my_signature == signature_key

def update_gdrive_member(email, paket, status_bayar, order_id, metode):
    """Update Google Sheet Pustaka Teduh - Member Status"""
    try:
        import gspread
        from oauth2client.service_account import ServiceAccountCredentials
        
        # credential dari env JSON string
        creds_json = json.loads(os.getenv("GOOGLE_CREDS_JSON", "{}"))
        if not creds_json:
            print("⚠️ GOOGLE_CREDS_JSON belum di set, skip GDrive")
            return False
            
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(GOOGLE_SHEET_ID).sheet1
        
        # Cari email
        try:
            cell = sheet.find(email)
            row = cell.row
            # Update kolom: Status, Paket, OrderID, Metode, Waktu
            # Asumsi kolom: A=Email, B=Status, C=Paket, D=OrderID, E=Metode, F=Waktu, G=Ruang
            sheet.update_cell(row, 2, "AKTIF")  # Status AKTIF
            sheet.update_cell(row, 3, paket)
            sheet.update_cell(row, 4, order_id)
            sheet.update_cell(row, 5, metode)
            sheet.update_cell(row, 6, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            sheet.update_cell(row, 7, "R3")  # Bisa masuk Ruang 3
            print(f"✅ GDrive updated: {email} -> AKTIF {paket}")
            return True
        except gspread.exceptions.CellNotFound:
            # Email belum ada, tambah baru
            sheet.append_row([email, "AKTIF", paket, order_id, metode, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "R3"])
            print(f"✅ GDrive new member: {email}")
            return True
    except Exception as e:
        print(f"❌ GDrive error: {e}")
        return False

def update_supabase_member(email, paket, status_bayar, order_id, metode):
    """Update Supabase table members"""
    try:
        if not SUPABASE_URL or not SUPABASE_KEY:
            print("⚠️ Supabase belum di set, skip")
            return False
        
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Upsert member
        data = {
            "email": email,
            "status": "AKTIF",
            "paket": paket,
            "order_id": order_id,
            "metode_bayar": metode,
            "waktu_bayar": datetime.now().isoformat(),
            "ruang_akses": "R3",
            "is_subscribed": True
        }
        result = supabase.table("members").upsert(data, on_conflict="email").execute()
        print(f"✅ Supabase updated: {email} -> {result}")
        return True
    except Exception as e:
        print(f"❌ Supabase error: {e}")
        return False

def update_streamlit_session_via_file(email):
    """Trik buat Streamlit: tulis file flag biar app.py bisa baca"""
    flag_path = f"/tmp/ruang_teduh_active_{email.replace('@','_at_')}.json"
    with open(flag_path, 'w') as f:
        json.dump({
            "email": email,
            "is_subscribed": True,
            "aktif_sejak": datetime.now().isoformat(),
            "trigger": "QRIS/VA/GoPay"
        }, f)

@app.get("/")
def home():
    return {"status": "Ruang Teduh Webhook v2.7 - Ready - Putin & Trump aman, koteka on 🥳", "time": datetime.now().isoformat()}

@app.post("/midtrans-callback")
async def midtrans_callback(request: Request):
    """
    Midtrans akan POST ke sini setiap ada transaksi QRIS/VA/GoPay/OVO
    Body contoh:
    {
      "order_id": "RUANGTEDUH-123456",
      "transaction_status": "settlement",
      "gross_amount": "200000",
      "payment_type": "qris",
      "customer_details": {"email": "asuveleikha@gmail.com"},
      "status_code": "200",
      "signature_key": "xxx"
    }
    """
    try:
        body = await request.json()
        print(f"📩 Webhook masuk: {json.dumps(body, indent=2)}")
        
        order_id = body.get('order_id', '')
        status_code = body.get('status_code', '')
        gross_amount = body.get('gross_amount', '')
        signature_key = body.get('signature_key', '')
        transaction_status = body.get('transaction_status', '')
        payment_type = body.get('payment_type', '')
        fraud_status = body.get('fraud_status', '')
        
        # 1. Verifikasi signature (PENTING BIAR GAK DITIPU)
        if not verify_midtrans_signature(order_id, status_code, gross_amount, signature_key):
            print(f"❌ Signature tidak valid! order_id={order_id}")
            raise HTTPException(status_code=403, detail="Invalid signature")
        
        # 2. Cek status sukses
        # qris, gopay, bank_transfer, ovo, danapay, shopeepay
        is_lunas = False
        if transaction_status == 'capture':
            if fraud_status == 'accept' or payment_type in ['qris', 'gopay', 'bank_transfer']:
                is_lunas = True
        elif transaction_status == 'settlement':
            is_lunas = True
        
        if not is_lunas:
            print(f"⏳ Belum lunas: {transaction_status}")
            return JSONResponse({"status": "pending", "transaction_status": transaction_status})
        
        # 3. Ambil email member
        customer = body.get('customer_details', {})
        email = customer.get('email', 'asuveleikha@gmail.com')  # fallback ke admin lo
        # Kalau dari order_id ada email
        if 'asuveleikha' in order_id.lower():
            email = 'asuveleikha@gmail.com'
        
        # Tentukan paket dari amount
        amount = float(gross_amount)
        if amount >= 250000:
            paket = "MALKHUTKHA Full Advance / Entrepreneur 300rb"
        else:
            paket = "TAVO Employee 200rb"
        
        # 4. UPDATE GDRIVE & SUPABASE - AUTO AKTIFKAN LANGGANAN
        gdrive_ok = update_gdrive_member(email, paket, transaction_status, order_id, payment_type)
        supabase_ok = update_supabase_member(email, paket, transaction_status, order_id, payment_type)
        update_streamlit_session_via_file(email)
        
        # 5. Kirim WA/Email notifikasi (opsional)
        print(f"🎉 MEMBER AKTIF: {email} - Paket {paket} - Metode {payment_type} - Order {order_id} - Jam {datetime.now()}")
        
        return JSONResponse({
            "status": "success",
            "message": f"Member {email} AKTIF - Bisa masuk Ruang 3",
            "order_id": order_id,
            "email": email,
            "paket": paket,
            "payment_type": payment_type,
            "gdrive": gdrive_ok,
            "supabase": supabase_ok,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

@app.post("/manual-activate")
async def manual_activate(request: Request):
    """Endpoint manual buat aktifin asuveleikha@gmail.com kalau QRIS test"""
    body = await request.json()
    email = body.get('email', 'asuveleikha@gmail.com')
    paket = body.get('paket', 'TAVO Employee 200rb')
    
    update_gdrive_member(email, paket, 'manual', f"MANUAL-{int(time.time())}", 'manual')
    update_supabase_member(email, paket, 'manual', f"MANUAL-{int(time.time())}", 'manual')
    update_streamlit_session_via_file(email)
    
    return {"status": "manual activated", "email": email}

# --- UNTUK TEST LOKAL ---
if __name__ == "__main__":
    import uvicorn
    print("🚀 Ruang Teduh Webhook jalan di http://localhost:8000")
    print("   POST /midtrans-callback  <- set ini di Midtrans Dashboard")
    print("   POST /manual-activate   <- buat test manual")
    uvicorn.run(app, host="0.0.0.0", port=8000)
