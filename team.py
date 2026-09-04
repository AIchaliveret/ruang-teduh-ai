
# team.py - LEMBAR 4 BIRU - Tim & Paket - Paket Freemium 3/3 + Direct Selling Upline/Downline
OWNER="aichaliveret"
QR="081291904422"
def hitung_direct_selling(emp, ent):
    # A share link ?ref=OWNER -> B jadi downline L1, C jadi downline L2 dari A
    gross = emp*55000 + ent*75000
    l1 = emp*11000 + ent*15000
    l2 = emp*4000 + ent*5000
    netto = gross - l1 - l2
    # Total cashback full 12: Employee 11k*3+4k*9=69k, Entrepreneur 15k*3+5k*9=90k + Gratis + Billboard Top!
    return {"gross":gross, "l1":l1, "l2":l2, "netto":netto, "total_cashback_emp":69000, "total_cashback_ent":90000}
