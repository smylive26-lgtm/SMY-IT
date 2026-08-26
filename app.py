import streamlit as st
import pandas as pd
import os
import datetime
import random

# Cuba import library auto-refresh
try:
    from streamlit_autorefresh import st_autorefresh
except ImportError:
    st_autorefresh = None

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="SMY IT PORTAL",
    page_icon="🏢",
    layout="wide"
)

# ==========================================
# TEMA KORPORAT MODEN
# ==========================================
def apply_corporate_theme():
    st.markdown(
        f"""
        <style>
        .stApp {{ background-color: #F4F6F9; }}
        .main .block-container {{
            background-color: #FFFFFF !important; 
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
            margin-top: 1rem;
            margin-bottom: 2rem;
        }}
        [data-testid="stSidebar"] {{
            background-color: #FFFFFF;
            border-right: 1px solid #E5E7EB;
        }}
        .stButton>button {{
            border-radius: 6px;
            font-weight: 500;
        }}
        h1, h2, h3 {{ color: #1F2937; }}
        </style>
        """,
        unsafe_allow_html=True
    )

apply_corporate_theme()

# ==========================================
# PEMBOLEHUBAH & FAIL SISTEM
# ==========================================
COMPANY_LOGO_PATH = "uploaded_images/company_logo.png"
ANNOUNCEMENT_MEDIA_DIR = "uploaded_announcements" 
PROFILE_PICS_DIR = "uploaded_profiles"    
EXCEL_FILE = "PC Master Data In SMY.xlsx"
REQUESTS_FILE = "IT_Requests.csv"
ANNOUNCEMENTS_FILE = "IT_Announcements.csv"
COMMUNITY_FILE = "IT_Community.csv"       
ONLINE_USERS_FILE = "Online_Users.csv"    
PRIVATE_CHAT_FILE = "IT_Private_Chat.csv" 
GLOBAL_ALIASES_FILE = "IT_Global_Aliases.csv"
ROLES_FILE = "IT_Roles.csv" 
SETTINGS_FILE = "IT_Settings.csv"

# --- SISTEM LOG MASUK (HARDCODED BACKUP SAHAJA) ---
USER_CREDENTIALS = {
    "admin": "admin123",
    "srm09814": "Afifi1123!",
    "smy_it": "smy2026",
    "staff": "staff123",
    "srm09298": "saiful8923!",
    "srm12399": "Sab130716!",
}

SUPER_ADMIN_ROLES = ["admin", "srm09814"]

# ==========================================
# FUNGSI PEMBANTU (HELPER) UNTUK PENYIMPANAN
# ==========================================
def init_system_files():
    if not os.path.exists(ANNOUNCEMENT_MEDIA_DIR):
        os.makedirs(ANNOUNCEMENT_MEDIA_DIR)
    if not os.path.exists(PROFILE_PICS_DIR):
        os.makedirs(PROFILE_PICS_DIR)
        
    if not os.path.exists(SETTINGS_FILE):
        df = pd.DataFrame([
            {"Setting": "Community_Chat_Enabled", "Value": "True"},
            {"Setting": "Private_Chat_Enabled", "Value": "True"}
        ])
        df.to_csv(SETTINGS_FILE, index=False)

    if not os.path.exists(ROLES_FILE):
        default_roles = [
            {"Username": "admin", "Is_Admin": True, "Is_Super_Admin": True, "Is_Section_Head": True, "Is_Dept_Head": True, "Is_IT_Sec_Head": True, "Is_IT_Dept_Head": True},
            {"Username": "srm09814", "Is_Admin": True, "Is_Super_Admin": True, "Is_Section_Head": True, "Is_Dept_Head": True, "Is_IT_Sec_Head": True, "Is_IT_Dept_Head": True}
        ]
        pd.DataFrame(default_roles).to_csv(ROLES_FILE, index=False)
        
    if not os.path.exists(REQUESTS_FILE):
        df = pd.DataFrame(columns=[
            "Ticket_ID", "Tarikh", "Pengguna", "Jabatan", "Need_Before", 
            "Section_Head", "Dept_Head", "Kategori", "Deskripsi", 
            "IT_Report", "Done_By", "Date_Completed", "IT_Sec_Head", "IT_Dept_Head", "Status"
        ])
        df.to_csv(REQUESTS_FILE, index=False)
    else:
        df_req = pd.read_csv(REQUESTS_FILE, dtype=str).fillna("")
        perlu_simpan_tiket = False
        if "Ticket_ID" not in df_req.columns:
            df_req.insert(0, "Ticket_ID", [f"TKT-{random.randint(1000, 9999)}" for _ in range(len(df_req))])
            perlu_simpan_tiket = True
            
        kolum_baru_isr = ["Need_Before", "Section_Head", "Dept_Head", "IT_Report", "Done_By", "Date_Completed", "IT_Sec_Head", "IT_Dept_Head"]
        for kolum in kolum_baru_isr:
            if kolum not in df_req.columns:
                if kolum in ["IT_Sec_Head", "IT_Dept_Head"]:
                    df_req[kolum] = "⏳ Menunggu"
                else:
                    df_req[kolum] = ""
                perlu_simpan_tiket = True
                
        if perlu_simpan_tiket:
            df_req.to_csv(REQUESTS_FILE, index=False)
        
    if not os.path.exists(ANNOUNCEMENTS_FILE):
        df = pd.DataFrame(columns=["Tarikh", "Tajuk", "Kandungan", "Media_Path", "Media_Type", "Tarikh_Tamat"])
        df.to_csv(ANNOUNCEMENTS_FILE, index=False)
    else:
        df = pd.read_csv(ANNOUNCEMENTS_FILE, dtype=str).fillna("")
        perlu_simpan = False
        if "Media_Path" not in df.columns:
            df["Media_Path"] = ""
            df["Media_Type"] = ""
            perlu_simpan = True
        if "Tarikh_Tamat" not in df.columns:
            df["Tarikh_Tamat"] = ""
            perlu_simpan = True
        if perlu_simpan:
            df.to_csv(ANNOUNCEMENTS_FILE, index=False)

    if not os.path.exists(COMMUNITY_FILE):
        df = pd.DataFrame(columns=["Tarikh", "Pengguna", "Mesej"])
        df.to_csv(COMMUNITY_FILE, index=False)
    if not os.path.exists(ONLINE_USERS_FILE):
        df = pd.DataFrame(columns=["Username", "Last_Active"])
        df.to_csv(ONLINE_USERS_FILE, index=False)
    if not os.path.exists(PRIVATE_CHAT_FILE):
        df = pd.DataFrame(columns=["Tarikh", "Pengirim", "Penerima", "Mesej"])
        df.to_csv(PRIVATE_CHAT_FILE, index=False)
    if not os.path.exists(GLOBAL_ALIASES_FILE):
        df = pd.DataFrame(columns=["Username", "Alias"])
        df.to_csv(GLOBAL_ALIASES_FILE, index=False)

init_system_files()

# --- FUNGSI MENDAPATKAN & MENYIMPAN TETAPAN ---
def get_setting(setting_name, default_value="True"):
    if not os.path.exists(SETTINGS_FILE):
        return default_value
    try:
        df = pd.read_csv(SETTINGS_FILE, dtype=str).fillna("")
        row = df[df["Setting"] == setting_name]
        if not row.empty:
            return str(row.iloc[0]["Value"])
    except:
        pass
    return default_value

def set_setting(setting_name, value):
    if not os.path.exists(SETTINGS_FILE):
        df = pd.DataFrame([{"Setting": setting_name, "Value": str(value)}])
        df.to_csv(SETTINGS_FILE, index=False)
        return
    df = pd.read_csv(SETTINGS_FILE, dtype=str).fillna("")
    if setting_name in df["Setting"].values:
        df.loc[df["Setting"] == setting_name, "Value"] = str(value)
    else:
        new_row = pd.DataFrame([{"Setting": setting_name, "Value": str(value)}])
        df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(SETTINGS_FILE, index=False)

# ==========================================
# FUNGSI MEMBACA USER & PERANAN (ROLES)
# ==========================================
@st.cache_data
def get_excel_users(filepath):
    users = {}
    if os.path.exists(filepath):
        try:
            df = pd.read_excel(filepath, sheet_name="SMY Master Data")
            df.columns = df.columns.str.strip()
            if 'Pc Username' in df.columns and 'Pc Password' in df.columns:
                valid_users = df.dropna(subset=['Pc Username', 'Pc Password'])
                for _, row in valid_users.iterrows():
                    uname = str(row['Pc Username']).strip()
                    pwd = str(row['Pc Password']).strip()
                    if uname and pwd:
                        users[uname] = pwd
        except Exception as e:
            st.error(f"Ralat membaca pangkalan data pengguna: {e}")
    return users

def get_user_roles(username):
    roles = {
        "Is_Admin": False, 
        "Is_Super_Admin": False, 
        "Is_Section_Head": False, 
        "Is_Dept_Head": False, 
        "Is_IT_Sec_Head": False,
        "Is_IT_Dept_Head": False
    }
    if os.path.exists(ROLES_FILE):
        df_roles = pd.read_csv(ROLES_FILE)
        bool_cols = ["Is_Admin", "Is_Super_Admin", "Is_Section_Head", "Is_Dept_Head", "Is_IT_Sec_Head", "Is_IT_Dept_Head"]
        for col in bool_cols:
            if col in df_roles.columns:
                df_roles[col] = df_roles[col].astype(str).str.lower().map({'true': True, 'false': False}).fillna(False)
                
        user_row = df_roles[df_roles["Username"] == username]
        if not user_row.empty:
            roles["Is_Admin"] = bool(user_row.iloc[0].get("Is_Admin", False))
            roles["Is_Super_Admin"] = bool(user_row.iloc[0].get("Is_Super_Admin", False))
            roles["Is_Section_Head"] = bool(user_row.iloc[0].get("Is_Section_Head", False))
            roles["Is_Dept_Head"] = bool(user_row.iloc[0].get("Is_Dept_Head", False))
            roles["Is_IT_Sec_Head"] = bool(user_row.iloc[0].get("Is_IT_Sec_Head", False))
            roles["Is_IT_Dept_Head"] = bool(user_row.iloc[0].get("Is_IT_Dept_Head", False))
            
    if username in SUPER_ADMIN_ROLES:
        roles["Is_Super_Admin"] = True
        roles["Is_Admin"] = True
        
    return roles

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False
if "roles" not in st.session_state:
    st.session_state["roles"] = {}

def get_all_global_aliases():
    if not os.path.exists(GLOBAL_ALIASES_FILE):
        return {}
    try:
        df = pd.read_csv(GLOBAL_ALIASES_FILE, dtype=str).fillna("")
        return dict(zip(df["Username"], df["Alias"]))
    except:
        return {}

def save_global_alias(username, alias):
    df = pd.read_csv(GLOBAL_ALIASES_FILE, dtype=str).fillna("")
    mask = df["Username"] == username
    if mask.any():
        df.loc[mask, "Alias"] = alias
    else:
        new_row = pd.DataFrame([{"Username": username, "Alias": alias}])
        df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(GLOBAL_ALIASES_FILE, index=False)

GLOBAL_ALIASES = get_all_global_aliases()

def display_name(target_user):
    if pd.isna(target_user) or target_user == "" or target_user == "⏳ Menunggu":
        return target_user
    if target_user in GLOBAL_ALIASES and pd.notna(GLOBAL_ALIASES[target_user]) and str(GLOBAL_ALIASES[target_user]).strip() != "":
        return f"{GLOBAL_ALIASES[target_user]} ({target_user})"
    return target_user

def generate_isr_html(row):
    html_content = f"""<div style="font-family: Arial, sans-serif; max-width: 800px; margin: auto; border: 1px solid #ccc; padding: 30px; border-radius: 8px; background-color: white;">
<h2 style="text-align: center; color: #1F2937; border-bottom: 2px solid #eee; padding-bottom: 10px;">IT SERVICE REQUISITION FORM (ISR)</h2>
<table style="width: 100%; margin-bottom: 20px; font-size: 14px; border-collapse: collapse;">
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>Ticket ID:</strong> {row.get('Ticket_ID', '')}</td>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>Date Request:</strong> {row.get('Tarikh', '')}</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>Requested By:</strong> {display_name(row.get('Pengguna', ''))}</td>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>Need Before:</strong> {row.get('Need_Before', '')}</td>
</tr>
<tr>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>Sec/Dept:</strong> {row.get('Jabatan', '')}</td>
<td style="padding: 8px; border: 1px solid #ddd;"><strong>Status:</strong> {row.get('Status', '')}</td>
</tr>
</table>
<div style="background-color: #f9f9f9; padding: 15px; border-radius: 6px; margin-bottom: 20px; border: 1px solid #eee;">
<h4 style="margin-top: 0; color: #374151;">Request Details</h4>
<p style="margin-bottom: 5px;"><strong>Category:</strong> {row.get('Kategori', '')}</p>
<p style="white-space: pre-wrap; margin-top: 0;"><strong>Description/Requirements:</strong><br/>{row.get('Deskripsi', '')}</p>
</div>
<table style="width: 100%; margin-bottom: 30px; text-align: center; font-size: 14px; border-collapse: collapse;">
<tr>
<td style="width: 50%; padding: 15px; border: 1px solid #ddd; background-color: #fafafa;">
<p style="margin: 0; color: #666; font-size: 12px;">Confirmed By (Sec Head)</p>
<p style="margin: 10px 0 0 0; font-size: 16px;"><strong>{display_name(row.get('Section_Head', ''))}</strong></p>
</td>
<td style="width: 50%; padding: 15px; border: 1px solid #ddd; background-color: #fafafa;">
<p style="margin: 0; color: #666; font-size: 12px;">Approved By (Dept Head)</p>
<p style="margin: 10px 0 0 0; font-size: 16px;"><strong>{display_name(row.get('Dept_Head', ''))}</strong></p>
</td>
</tr>
</table>
<div style="background-color: #f0f7ff; padding: 15px; border-radius: 6px; margin-bottom: 20px; border: 1px solid #cce3ff;">
<h4 style="margin-top: 0; color: #004085;">IT Report (Repair / Purchase / Action)</h4>
<p style="white-space: pre-wrap; margin-bottom: 0;">{row.get('IT_Report', '<i>(Belum diisi)</i>')}</p>
</div>
<table style="width: 100%; margin-bottom: 20px; text-align: center; font-size: 14px; border-collapse: collapse;">
<tr>
<td style="width: 50%; padding: 15px; border: 1px solid #ddd; background-color: #fafafa;">
<p style="margin: 0; color: #666; font-size: 12px;">Confirmed By (IT Sec Head)</p>
<p style="margin: 10px 0 0 0; font-size: 16px;"><strong>{display_name(row.get('IT_Sec_Head', ''))}</strong></p>
</td>
<td style="width: 50%; padding: 15px; border: 1px solid #ddd; background-color: #fafafa;">
<p style="margin: 0; color: #666; font-size: 12px;">Approved By (IT Dept Head)</p>
<p style="margin: 10px 0 0 0; font-size: 16px;"><strong>{display_name(row.get('IT_Dept_Head', ''))}</strong></p>
</td>
</tr>
</table>
<table style="width: 100%; text-align: left; font-size: 14px; border-top: 2px solid #eee; padding-top: 15px;">
<tr>
<td style="width: 50%;"><strong>Done By (IT Staff):</strong> {row.get('Done_By', '')}</td>
<td style="width: 50%;"><strong>Date Completed:</strong> {row.get('Date_Completed', '')}</td>
</tr>
</table>
</div>"""
    return html_content

def update_online_status(username):
    if not username: return
    sekarang = datetime.datetime.now()
    sekarang_str = sekarang.strftime("%Y-%m-%d %H:%M:%S")
    
    df = pd.read_csv(ONLINE_USERS_FILE, dtype=str).fillna("")
    if username in df["Username"].values:
        df.loc[df["Username"] == username, "Last_Active"] = sekarang_str
    else:
        new_row = pd.DataFrame([{"Username": username, "Last_Active": sekarang_str}])
        df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(ONLINE_USERS_FILE, index=False)

def get_online_users():
    df = pd.read_csv(ONLINE_USERS_FILE, dtype=str).fillna("")
    sekarang = datetime.datetime.now()
    online_list = []
    for _, row in df.iterrows():
        try:
            last_active = datetime.datetime.strptime(str(row["Last_Active"]), "%Y-%m-%d %H:%M:%S")
            if (sekarang - last_active).total_seconds() < 300:
                online_list.append(row["Username"])
        except:
            pass
    return online_list

def get_avatar(uname):
    path = os.path.join(PROFILE_PICS_DIR, f"{uname}.png")
    if os.path.exists(path):
        return path
    r = get_user_roles(uname)
    return "👑" if r["Is_Admin"] else "👤"

# ==========================================
# HALAMAN LOG MASUK
# ==========================================
def login_page():
    if os.path.exists(COMPANY_LOGO_PATH):
        col_logo1, col_logo2, col_logo3 = st.columns([1, 1, 1])
        with col_logo2:
            st.image(COMPANY_LOGO_PATH, use_container_width=True)
            
    st.markdown("<h2 style='text-align: center; color: #1F2937;'>Sistem Pengurusan IT SMY</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("Sila masukkan ID anda Eg: srm09814.")
        username_input = st.text_input("ID Pengguna")
        password_input = st.text_input("Kata Laluan", type="password")
        
        if st.button("Log Masuk", use_container_width=True, type="primary"):
            excel_users = get_excel_users(EXCEL_FILE)
            ALL_CREDENTIALS = {**excel_users, **USER_CREDENTIALS}
            
            if username_input in ALL_CREDENTIALS and ALL_CREDENTIALS[username_input] == password_input:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username_input
                
                user_roles = get_user_roles(username_input)
                st.session_state["roles"] = user_roles
                st.session_state["is_admin"] = user_roles["Is_Admin"]
                
                update_online_status(username_input)
                st.success("Log masuk berjaya!")
                st.rerun()
            else:
                st.error("Ralat: ID Pengguna atau Kata Laluan tidak sah.")

if not st.session_state["logged_in"]:
    login_page()
    st.stop()

# ==========================================
# SETELAH LOG MASUK BERJAYA (MAIN DASHBOARD)
# ==========================================

update_online_status(st.session_state["username"])

if os.path.exists(COMPANY_LOGO_PATH):
    st.sidebar.image(COMPANY_LOGO_PATH, use_container_width=True)
    st.sidebar.markdown("---")

profile_path = os.path.join(PROFILE_PICS_DIR, f"{st.session_state['username']}.png")
if os.path.exists(profile_path):
    col_p1, col_p2, col_p3 = st.sidebar.columns([1, 2, 1])
    with col_p2:
        st.image(profile_path, use_container_width=True)

role_label = "👑 Admin (IT Team)" if st.session_state["is_admin"] else "👤 Pengguna (Staff)"
if st.session_state["roles"].get("Is_Super_Admin", False):
    role_label = "🌟 Super Admin"

st.sidebar.markdown(f"**Akaun:** `{display_name(st.session_state['username'])}`\n\n**Peranan:** {role_label}")

if st.sidebar.button("Keluar (Logout)", use_container_width=True):
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.session_state["is_admin"] = False
    st.session_state["roles"] = {}
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.header("📁 Navigasi Modul")

if st.session_state["is_admin"]:
    pilihan_menu = st.sidebar.radio("Pilih Modul:", [
        "Dashboard & Hebahan", 
        "Bantuan & Permohonan IT (ISR)", 
        "Inventori IT (Master Data)", 
        "Pengurusan Tiket (ISR)",
        "🗨️ Ruangan Komuniti",
        "👤 Profil Saya",  
        "Tetapan Portal"
    ])
else:
    pilihan_menu = st.sidebar.radio("Pilih Modul:", [
        "Papan Hebahan IT", 
        "Bantuan & Permohonan IT (ISR)", 
        "🗨️ Ruangan Komuniti",
        "👤 Profil Saya"   
    ])

# ==========================================
# LOGIK ANTARAMUKA (UI) MENGIKUT MENU
# ==========================================

# ---------------------------------------------------------
# MODUL: 👤 PROFIL SAYA (USER PROFILE)
# ---------------------------------------------------------
if pilihan_menu == "👤 Profil Saya":
    st.title("👤 Profil Pengguna")
    st.write("Uruskan gambar profil dan nama paparan (alias) anda di sini supaya rakan sekerja mudah mengenali anda.")
    st.markdown("---")
    
    col_prof1, col_prof2 = st.columns([1, 2])
    
    with col_prof1:
        st.subheader("Gambar Profil Semasa")
        if os.path.exists(profile_path):
            st.image(profile_path, width=200)
            if st.button("🗑️ Buang Gambar", type="secondary"):
                os.remove(profile_path)
                st.toast("Gambar profil telah dibuang.", icon="🗑️")
                st.rerun()
        else:
            st.info("Anda belum menetapkan sebarang gambar profil.")
            st.markdown(f"<h1>{get_avatar(st.session_state['username'])}</h1>", unsafe_allow_html=True)
            
    with col_prof2:
        st.subheader("Butiran Akaun & Profil")
        current_my_alias = GLOBAL_ALIASES.get(st.session_state["username"], "")
        
        with st.form("profile_details_form"):
            new_alias = st.text_input("Nama Paparan (Alias):", value=current_my_alias, help="Contoh: 'Ahmad Logistic' atau 'Sarah HR'")
            st.write("Muat Naik Gambar Baharu (Nisbah 1:1 digalakkan). **Had saiz: Maksimum 5MB.**")
            uploaded_profile = st.file_uploader("Format disokong: JPG, PNG", type=["jpg", "png", "jpeg"])
            
            if st.form_submit_button("💾 Simpan Perubahan Profil", type="primary"):
                save_global_alias(st.session_state["username"], new_alias)
                
                if uploaded_profile is not None:
                    max_size_bytes = 5 * 1024 * 1024  
                    if uploaded_profile.size > max_size_bytes:
                        st.error("Ralat: Saiz gambar anda melebihi had maksimum 5MB. Sila pilih gambar yang lebih kecil.")
                    else:
                        with open(profile_path, "wb") as f:
                            f.write(uploaded_profile.getbuffer())
                        st.toast("Profil anda telah berjaya dikemaskini!", icon="✅")
                        st.rerun()
                else:
                    st.toast("Profil anda telah berjaya dikemaskini!", icon="✅")
                    st.rerun()

# ---------------------------------------------------------
# MODUL: 🗨️ RUANGAN KOMUNITI (CHAT UMUM & PM)
# ---------------------------------------------------------
elif pilihan_menu == "🗨️ Ruangan Komuniti":
    
    if st_autorefresh:
        st_autorefresh(interval=5000, key="chat_autorefresh")

    st.title("💬 Ruangan Komuniti IT SMY")
    st.write("Bersembang secara umum di Ruang Komuniti atau hantar Mesej Peribadi (PM) kepada rakan anda.")
    st.markdown("---")
    
    excel_users = get_excel_users(EXCEL_FILE)
    semua_pengguna_sistem = list(USER_CREDENTIALS.keys()) + list(excel_users.keys())
    semua_pengguna_sistem = sorted(list(set(semua_pengguna_sistem))) 
    
    pilihan_pm_user = semua_pengguna_sistem.copy()
    if st.session_state["username"] in pilihan_pm_user:
        pilihan_pm_user.remove(st.session_state["username"])
        
    col_chat, col_online = st.columns([3, 1])
    
    with col_online:
        st.markdown("#### 🟢 Sedang Aktif")
        senarai_online = get_online_users()
        if st.session_state["username"] in senarai_online:
            senarai_online.remove(st.session_state["username"])
            senarai_online.insert(0, f"{st.session_state['username']} (Anda)")
            
        for u in senarai_online:
            if "(Anda)" in u:
                st.markdown(f"• 🟢 **{display_name(st.session_state['username'])} (Anda)**")
            else:
                st.markdown(f"• 🟢 **{display_name(u)}**")
            
        if not senarai_online:
            st.write("Tiada pengguna aktif.")

    with col_chat:
        is_super_admin = st.session_state["roles"].get("Is_Super_Admin", False)
        
        if is_super_admin:
            tabs_komuniti = st.tabs(["💬 Komuniti Umum", "🔒 Mesej Peribadi (PM)", "👁️ Pantauan PM (Admin)"])
            tab_umum = tabs_komuniti[0]
            tab_pm = tabs_komuniti[1]
            tab_monitor = tabs_komuniti[2]
        else:
            tabs_komuniti = st.tabs(["💬 Komuniti Umum", "🔒 Mesej Peribadi (PM)"])
            tab_umum = tabs_komuniti[0]
            tab_pm = tabs_komuniti[1]
            tab_monitor = None
        
        with tab_umum:
            st.markdown("#### Bual Bicara Umum")
            
            is_chat_enabled = (get_setting("Community_Chat_Enabled", "True") == "True")
            
            df_chat = pd.read_csv(COMMUNITY_FILE, dtype=str).fillna("")
            if not df_chat.empty:
                try:
                    df_chat['temp_date'] = pd.to_datetime(df_chat['Tarikh'], format='%d-%m-%Y %H:%M', errors='coerce')
                    today_date = datetime.datetime.now().date()
                    df_chat_filtered = df_chat[df_chat['temp_date'].dt.date == today_date].copy()
                    if len(df_chat_filtered) < len(df_chat):
                        df_chat = df_chat_filtered.drop(columns=['temp_date'])
                        df_chat.to_csv(COMMUNITY_FILE, index=False)
                    else:
                        df_chat = df_chat.drop(columns=['temp_date'])
                except:
                    pass

            if st.session_state["is_admin"]:
                if st.button("🗑️ Padam Semua Chat Umum", type="secondary", use_container_width=True):
                    df_chat = pd.DataFrame(columns=["Tarikh", "Pengguna", "Mesej"])
                    df_chat.to_csv(COMMUNITY_FILE, index=False)
                    st.toast("Semua perbualan umum telah dibersihkan!", icon="🧹")
                    st.rerun()
                st.markdown("---")

            chat_container = st.container(height=500)
            
            with chat_container:
                if df_chat.empty:
                    st.info("👋 Ruangan masih sunyi. Jadilah orang pertama yang menegur sapa!")
                else:
                    for idx, msg in df_chat.tail(100).iterrows():
                        pengirim = str(msg['Pengguna'])
                        tarikh_msg = str(msg['Tarikh'])
                        isi_mesej = str(msg['Mesej'])
                        is_user = pengirim == st.session_state["username"]
                        avatar_icon = get_avatar(pengirim)
                        p_roles = get_user_roles(pengirim)
                        
                        with st.chat_message("user" if is_user else "assistant", avatar=avatar_icon):
                            if is_user:
                                nama_papar = f"👤 **Anda ({display_name(pengirim)})**"
                            elif p_roles.get("Is_Admin", False):
                                nama_papar = f"👑 **{display_name(pengirim)} (IT)**"
                            else:
                                nama_papar = f"👤 **{display_name(pengirim)}**"
                            
                            if st.session_state["is_admin"]:
                                c1, c2 = st.columns([11, 1])
                                with c1:
                                    st.markdown(f"{nama_papar} <span style='font-size:0.7em;color:gray;'>• {tarikh_msg}</span>", unsafe_allow_html=True)
                                    st.write(isi_mesej)
                                with c2:
                                    if st.button("🗑️", key=f"del_chat_umum_{idx}", help="Padam mesej ini"):
                                        df_chat = df_chat.drop(idx)
                                        df_chat.to_csv(COMMUNITY_FILE, index=False)
                                        st.toast("Mesej berjaya dipadam!", icon="✅")
                                        st.rerun()
                            else:
                                st.markdown(f"{nama_papar} <span style='font-size:0.7em;color:gray;'>• {tarikh_msg}</span>", unsafe_allow_html=True)
                                st.write(isi_mesej)

            if is_chat_enabled:
                prompt_umum = st.chat_input("Taip mesej anda kepada semua...", key="input_umum")
                if prompt_umum:
                    new_msg = {
                        "Tarikh": datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
                        "Pengguna": st.session_state["username"],
                        "Mesej": prompt_umum
                    }
                    df_chat = pd.concat([df_chat, pd.DataFrame([new_msg])], ignore_index=True)
                    df_chat.to_csv(COMMUNITY_FILE, index=False)
                    st.rerun()
            else:
                st.warning("🔒 Ruangan Bual Bicara Umum telah ditutup buat sementara waktu oleh pihak Admin.")

        with tab_pm:
            st.markdown("#### Hantar Mesej Peribadi (Private Chat)")
            
            is_pm_enabled = (get_setting("Private_Chat_Enabled", "True") == "True")
            
            if is_pm_enabled:
                df_pm = pd.read_csv(PRIVATE_CHAT_FILE, dtype=str).fillna("")
                my_pms = df_pm[(df_pm["Pengirim"] == st.session_state["username"]) | (df_pm["Penerima"] == st.session_state["username"])]
                
                recent_targets = []
                for p, r in zip(my_pms["Pengirim"], my_pms["Penerima"]):
                    if p != st.session_state["username"] and p not in recent_targets:
                        recent_targets.append(p)
                    if r != st.session_state["username"] and r not in recent_targets:
                        recent_targets.append(r)
                        
                other_targets = [u for u in pilihan_pm_user if u not in recent_targets]
                
                display_to_id = {}
                options = ["-- Pilih Pengguna --"]
                
                if recent_targets:
                    options.append("--- SEJARAH PERBUALAN ---")
                    for u in recent_targets:
                        lbl = f"💬 {display_name(u)}"
                        options.append(lbl)
                        display_to_id[lbl] = u
                        
                if other_targets:
                    options.append("--- SEMUA PENGGUNA ---")
                    for u in other_targets:
                        lbl = f"👤 {display_name(u)}"
                        options.append(lbl)
                        display_to_id[lbl] = u
                
                penerima_pm_display = st.selectbox("Pilih kakitangan untuk dihubungi:", options)
                
                penerima_pm = None
                if penerima_pm_display in display_to_id:
                    penerima_pm = display_to_id[penerima_pm_display]
                
                if penerima_pm:
                    st.markdown(f"#### 🔒 Mesej Bersama: {display_name(penerima_pm)}")
                    
                    mask = ((df_pm["Pengirim"] == st.session_state["username"]) & (df_pm["Penerima"] == penerima_pm)) | \
                           ((df_pm["Pengirim"] == penerima_pm) & (df_pm["Penerima"] == st.session_state["username"]))
                    pm_history = df_pm[mask]
                    
                    pm_container = st.container(height=350)
                    with pm_container:
                        if pm_history.empty:
                            st.info(f"Mulakan perbualan peribadi baru dengan {display_name(penerima_pm)}.")
                        else:
                            for _, msg in pm_history.iterrows():
                                is_me = msg["Pengirim"] == st.session_state["username"]
                                avatar_icon = get_avatar(msg["Pengirim"])
                                
                                with st.chat_message("user" if is_me else "assistant", avatar=avatar_icon):
                                    nama_papar = "Anda" if is_me else display_name(msg["Pengirim"])
                                    st.markdown(f"**{nama_papar}** <span style='font-size:0.7em;color:gray;'>• {msg['Tarikh']}</span>", unsafe_allow_html=True)
                                    st.write(msg["Mesej"])
                                    
                    prompt_pm = st.chat_input(f"Mesej rahsia kepada {display_name(penerima_pm)}...", key="input_pm")
                    if prompt_pm:
                        new_pm = {
                            "Tarikh": datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
                            "Pengirim": st.session_state["username"],
                            "Penerima": penerima_pm,
                            "Mesej": prompt_pm
                        }
                        df_pm = pd.concat([df_pm, pd.DataFrame([new_pm])], ignore_index=True)
                        df_pm.to_csv(PRIVATE_CHAT_FILE, index=False)
                        st.rerun()
            else:
                st.warning("🔒 Ruangan Mesej Peribadi (PM) telah ditutup buat sementara waktu oleh pihak Admin.")

        if tab_monitor:
            with tab_monitor:
                st.markdown("#### 👁️ Pantauan Mesej Peribadi (Super Admin)")
                st.write("Sebagai Super Admin, anda boleh memantau dan memadam log perbualan staf atas faktor keselamatan.")
                
                df_pm_all = pd.read_csv(PRIVATE_CHAT_FILE, dtype=str).fillna("")
                if df_pm_all.empty:
                    st.info("Tiada sebarang rekod mesej peribadi (PM) dalam pangkalan data.")
                else:
                    pantau_user = st.selectbox("1. Pilih Pengguna Pertama:", ["-- Pilih --"] + semua_pengguna_sistem, key="pantau_user1")
                    if pantau_user != "-- Pilih --":
                        
                        chat_partners = df_pm_all[(df_pm_all["Pengirim"] == pantau_user) | (df_pm_all["Penerima"] == pantau_user)]
                        partners = set(chat_partners["Pengirim"].tolist() + chat_partners["Penerima"].tolist())
                        if pantau_user in partners:
                            partners.remove(pantau_user)
                            
                        if not partners:
                            st.info(f"Pengguna '{pantau_user}' belum pernah membalas PM dengan sesiapa.")
                        else:
                            pantau_partner = st.selectbox("2. Pilih Pasangan Chat (Orang yang dihubungi):", ["-- Pilih --"] + list(partners), key="pantau_user2")
                            
                            if pantau_partner != "-- Pilih --":
                                st.markdown("---")
                                st.markdown(f"**Rekod Perbualan Antara:** `{display_name(pantau_user)}` & `{display_name(pantau_partner)}`")
                                
                                mask_pantau = ((df_pm_all["Pengirim"] == pantau_user) & (df_pm_all["Penerima"] == pantau_partner)) | \
                                              ((df_pm_all["Pengirim"] == pantau_partner) & (df_pm_all["Penerima"] == pantau_user))
                                pantau_history = df_pm_all[mask_pantau]
                                
                                pantau_container = st.container(height=400)
                                with pantau_container:
                                    for idx, msg in pantau_history.iterrows():
                                        avatar_icon = get_avatar(msg['Pengirim'])
                                        with st.chat_message("assistant", avatar=avatar_icon):
                                            c_pm1, c_pm2 = st.columns([11, 1])
                                            with c_pm1:
                                                st.markdown(f"**{display_name(msg['Pengirim'])}** <span style='font-size:0.8em;color:gray;'>({msg['Tarikh']})</span>", unsafe_allow_html=True)
                                                st.info(msg['Mesej'])
                                            with c_pm2:
                                                if st.button("🗑️", key=f"del_pm_admin_{idx}", help="Padam mesej peribadi ini"):
                                                    df_pm_all = df_pm_all.drop(idx)
                                                    df_pm_all.to_csv(PRIVATE_CHAT_FILE, index=False)
                                                    st.toast("Mesej peribadi berjaya dipadam!", icon="✅")
                                                    st.rerun()

# ---------------------------------------------------------
# MODUL: PAPAN HEBAHAN & DASHBOARD MULTIMEDIA
# ---------------------------------------------------------
elif pilihan_menu in ["Dashboard & Hebahan", "Papan Hebahan IT"]:
    st.title("📢 Papan Hebahan IT SMY")
    st.write("Maklumat terkini, pengumuman, dan panduan dari Jabatan IT.")
    st.markdown("---")
    
    df_announcements = pd.read_csv(ANNOUNCEMENTS_FILE, dtype=str).fillna("")
    sekarang = datetime.datetime.now()
    
    if st.session_state["is_admin"]:
        tab_feed, tab_new, tab_manage = st.tabs(["📢 Paparan Utama", "➕ Terbit Hebahan Baru", "⚙️ Arkib & Pengurusan"])
    else:
        tab_feed = st.container()
        tab_new = None
        tab_manage = None

    with tab_feed:
        ada_post_dipaparkan = False
        if not df_announcements.empty:
            for index, row in df_announcements[::-1].iterrows():
                tamat_tempoh = False
                label_status = ""
                
                if pd.notna(row.get('Tarikh_Tamat')) and str(row.get('Tarikh_Tamat')).strip() != "":
                    try:
                        waktu_tamat = datetime.datetime.strptime(str(row['Tarikh_Tamat']), "%Y-%m-%d %H:%M:%S")
                        if sekarang > waktu_tamat:
                            tamat_tempoh = True
                        else:
                            baki = waktu_tamat - sekarang
                            hari = baki.days
                            jam = baki.seconds // 3600
                            minit = (baki.seconds % 3600) // 60
                            
                            if hari > 0:
                                label_status = f" ⏳ (Tamat dalam: {hari} hari {jam} jam)"
                            elif jam > 0:
                                label_status = f" ⏳ (Tamat dalam: {jam} jam {minit} minit)"
                            else:
                                label_status = f" ⏳ (Tamat dalam: {minit} minit)"
                    except Exception:
                        pass
                
                if not tamat_tempoh:
                    ada_post_dipaparkan = True
                    with st.expander(f"📌 {row['Tajuk']} ({row['Tarikh']}){label_status}", expanded=True):
                        st.write(row['Kandungan'])
                        
                        media_path = str(row.get('Media_Path', ''))
                        media_type = str(row.get('Media_Type', ''))
                        
                        if pd.notna(media_path) and media_path.strip() not in ["", "None", "nan", "NaN"]:
                            if os.path.exists(media_path):
                                st.markdown("<br>", unsafe_allow_html=True)
                                if media_type == "Image":
                                    st.image(media_path, use_container_width=True)
                                elif media_type == "Video":
                                    try:
                                        with open(media_path, 'rb') as video_file:
                                            video_bytes = video_file.read()
                                        st.video(video_bytes)
                                    except Exception as e:
                                        st.error(f"Gagal memuatkan video: {e}")

        if not ada_post_dipaparkan:
            st.info("Tiada pengumuman atau hebahan aktif pada masa ini.")

    if st.session_state["is_admin"]:
        with tab_new:
            st.subheader("Borang Hebahan Baharu")
            with st.form("form_hebahan"):
                tajuk_baru = st.text_input("Tajuk Pengumuman / Hebahan")
                isi_baru = st.text_area("Kandungan / Penerangan")
                tempoh_paparan = st.selectbox("Tempoh Paparan (Bila hebahan ini patut diturunkan?):", 
                                              ["1 Jam", "12 Jam", "24 Jam", "3 Hari", "1 Minggu", "Kekal (Tiada Had)"])
                media_baru = st.file_uploader("Sertakan Gambar atau Video (Opsyenal)", type=["png", "jpg", "jpeg", "mp4", "mov", "avi"])
                
                if st.form_submit_button("🚀 Terbitkan Hebahan", type="primary"):
                    if tajuk_baru and isi_baru:
                        sekarang = datetime.datetime.now()
                        tarikh_tamat_str = ""
                        if tempoh_paparan == "1 Jam":
                            tarikh_tamat_str = (sekarang + datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
                        elif tempoh_paparan == "12 Jam":
                            tarikh_tamat_str = (sekarang + datetime.timedelta(hours=12)).strftime("%Y-%m-%d %H:%M:%S")
                        elif tempoh_paparan == "24 Jam":
                            tarikh_tamat_str = (sekarang + datetime.timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")
                        elif tempoh_paparan == "3 Hari":
                            tarikh_tamat_str = (sekarang + datetime.timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
                        elif tempoh_paparan == "1 Minggu":
                            tarikh_tamat_str = (sekarang + datetime.timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")

                        media_path_to_save = ""
                        media_type_to_save = ""
                        if media_baru is not None:
                            media_path_to_save = os.path.join(ANNOUNCEMENT_MEDIA_DIR, media_baru.name)
                            with open(media_path_to_save, "wb") as f:
                                f.write(media_baru.getbuffer())
                            file_ext = media_baru.name.split('.')[-1].lower()
                            if file_ext in ['png', 'jpg', 'jpeg'] or media_baru.type.startswith('image'):
                                media_type_to_save = "Image"
                            elif file_ext in ['mp4', 'mov', 'avi'] or media_baru.type.startswith('video'):
                                media_type_to_save = "Video"

                        new_row = {
                            "Tarikh": sekarang.strftime("%d-%m-%Y %H:%M"), 
                            "Tajuk": tajuk_baru, 
                            "Kandungan": isi_baru,
                            "Media_Path": media_path_to_save,
                            "Media_Type": media_type_to_save,
                            "Tarikh_Tamat": tarikh_tamat_str
                        }
                        
                        df_announcements = pd.concat([df_announcements, pd.DataFrame([new_row])], ignore_index=True)
                        df_announcements.to_csv(ANNOUNCEMENTS_FILE, index=False)
                        st.toast(f"Hebahan diterbitkan! (Tempoh sah: {tempoh_paparan})", icon="✅")
                        st.rerun()
                    else:
                        st.error("Sila isikan sekurang-kurangnya tajuk dan kandungan.")

        with tab_manage:
            st.subheader("Pengurusan Senarai Hebahan")
            if st.button("🗑️ Padam SEMUA Hebahan Tamat Tempoh", type="secondary"):
                to_keep = []
                for idx, row in df_announcements.iterrows():
                    if pd.notna(row['Tarikh_Tamat']) and str(row['Tarikh_Tamat']).strip() != "":
                        try:
                            wt = datetime.datetime.strptime(str(row['Tarikh_Tamat']), "%Y-%m-%d %H:%M:%S")
                            if sekarang <= wt:
                                to_keep.append(idx)
                        except:
                            to_keep.append(idx)
                    else:
                        to_keep.append(idx)
                        
                df_announcements = df_announcements.loc[to_keep]
                df_announcements.to_csv(ANNOUNCEMENTS_FILE, index=False)
                st.toast("Hebahan tamat tempoh telah dibersihkan!", icon="🧹")
                st.rerun()
                
            st.markdown("---")
            
            if df_announcements.empty:
                st.info("Tiada sebarang rekod hebahan.")
            else:
                post_options = {}
                for idx, row in df_announcements[::-1].iterrows():
                    status_teks = "🟢 Aktif"
                    if pd.notna(row['Tarikh_Tamat']) and str(row['Tarikh_Tamat']).strip() != "":
                        try:
                            wt = datetime.datetime.strptime(str(row['Tarikh_Tamat']), "%Y-%m-%d %H:%M:%S")
                            if sekarang > wt:
                                status_teks = "🔴 Expired"
                        except:
                            pass
                    post_options[f"[{status_teks}] {row['Tarikh']} - {row['Tajuk']}"] = idx
                    
                selected_post_label = st.selectbox("Pilih Hebahan untuk Diuruskan:", list(post_options.keys()))
                selected_idx = post_options[selected_post_label]
                selected_row = df_announcements.loc[selected_idx]
                
                st.write(f"**Tajuk:** {selected_row['Tajuk']}")
                st.write(f"**Kandungan Ringkas:** {str(selected_row['Kandungan'])[:100]}...")
                
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    if st.button("🗑️ Padam Hebahan Ini", use_container_width=True):
                        df_announcements = df_announcements.drop(selected_idx)
                        df_announcements.to_csv(ANNOUNCEMENTS_FILE, index=False)
                        st.toast("Hebahan berjaya dipadam!", icon="✅")
                        st.rerun()
                        
                with col_m2:
                    with st.expander("🔄 Klik untuk Repost Hebahan Ini"):
                        tempoh_repost = st.selectbox("Pilih Tempoh Sah Baharu:", 
                                      ["1 Jam", "12 Jam", "24 Jam", "3 Hari", "1 Minggu", "Kekal (Tiada Had)"], key="repost_dur")
                        if st.button("Sahkan Repost", type="primary", use_container_width=True):
                            tarikh_tamat_str = ""
                            if tempoh_repost == "1 Jam":
                                tarikh_tamat_str = (sekarang + datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
                            elif tempoh_repost == "12 Jam":
                                tarikh_tamat_str = (sekarang + datetime.timedelta(hours=12)).strftime("%Y-%m-%d %H:%M:%S")
                            elif tempoh_repost == "24 Jam":
                                tarikh_tamat_str = (sekarang + datetime.timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")
                            elif tempoh_repost == "3 Hari":
                                tarikh_tamat_str = (sekarang + datetime.timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
                            elif tempoh_repost == "1 Minggu":
                                tarikh_tamat_str = (sekarang + datetime.timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
                            
                            df_announcements.at[selected_idx, 'Tarikh'] = sekarang.strftime("%d-%m-%Y %H:%M")
                            df_announcements.at[selected_idx, 'Tarikh_Tamat'] = tarikh_tamat_str
                            row_to_move = df_announcements.loc[[selected_idx]]
                            df_announcements = df_announcements.drop(selected_idx)
                            df_announcements = pd.concat([df_announcements, row_to_move], ignore_index=True)
                            
                            df_announcements.to_csv(ANNOUNCEMENTS_FILE, index=False)
                            st.toast("Hebahan berjaya di-repost ke Paparan Utama!", icon="🚀")
                            st.rerun()

# ---------------------------------------------------------
# MODUL: BANTUAN & PERMOHONAN IT (USER VIEW & ADMIN VIEW) 
# ---------------------------------------------------------
elif pilihan_menu == "Bantuan & Permohonan IT (ISR)":
    st.title("🛠️ Borang Permohonan IT (ISR Form)")
    st.write("Sila lengkapkan borang *IT Service Requisition (ISR)* di bawah.")
    st.markdown("---")
    
    is_approver = st.session_state["roles"].get("Is_Section_Head", False) or st.session_state["roles"].get("Is_Dept_Head", False)
    
    if is_approver:
        user_tabs = st.tabs(["📋 Borang Permohonan Baru", "📋 Senarai Permohonan Saya", "✅ Pengesahan Ketua (Sect/Dept)"])
        tab_form = user_tabs[0]
        tab_history = user_tabs[1]
        tab_approval = user_tabs[2]
    else:
        user_tabs = st.tabs(["📋 Borang Permohonan Baru", "📋 Senarai Permohonan Saya"])
        tab_form = user_tabs[0]
        tab_history = user_tabs[1]
        tab_approval = None

    with tab_form:
        st.subheader("📋 Maklumat Asas")
        nama_user = st.text_input("Requested By (Nama Pemohon)", value=display_name(st.session_state["username"]), disabled=True)
        col_a, col_b = st.columns(2)
        with col_a:
            jabatan = st.text_input("Sec.Dept (Jabatan/Seksyen)")
        with col_b:
            need_before = st.date_input("Date to complete (Need Before)")
            
        st.info("💡 Nama Section Head & Department Head tidak perlu diisi. Mereka akan membuat pengesahan terus dari sistem.")
        st.markdown("---")
        st.subheader("⚙️ Kategori Permohonan")

        kategori = st.selectbox("Pilih Jenis Permohonan (Request Type)", [
            "New Equipment Request (New or Replacement)",
            "Maintenance / Repair (Existing Device)",
            "Software / ID / Access Request",
            "Peripheral Request (Monitor, Keyboard, etc.)",
            "Network",
            "Others"
        ])
        deskripsi_lanjut = ""

        if kategori == "New Equipment Request (New or Replacement)":
            st.write("Sila nyatakan butiran peralatan baharu:")
            dev_type = st.radio("Device Type", ["Laptop", "Desktop", "Tablet", "Printer"], horizontal=True)
            os_pref = st.radio("Operating System Preference", ["Windows", "Others"], horizontal=True)
            spec_req = st.text_area("Special Requirements (e.g., High RAM for Video Editing, extra storage)")
            deskripsi_lanjut = f"Device: {dev_type} | OS: {os_pref} | Special Reqs: {spec_req}"
        elif kategori == "Network":
            st.write("Sila tandakan keperluan rangkaian anda:")
            net_type = st.multiselect("Network Type", ["Lan Cable", "Fibre", "Wifi"])
            net_desc = st.text_area("Additional Network Details (Lokasi / Port)")
            deskripsi_lanjut = f"Network Setup: {', '.join(net_type)} | Details: {net_desc}"
        elif kategori == "Software / ID / Access Request":
            st.write("Sila nyatakan ID atau perisian yang diperlukan:")
            soft_desc = st.text_area("Contoh: Slack, E-Mail, Sistem ERP, dsb.")
            deskripsi_lanjut = f"Software/Access Reqs: {soft_desc}"
        elif kategori == "Peripheral Request (Monitor, Keyboard, etc.)":
            peri_desc = st.text_input("Sila nyatakan barang peripheral yang diperlukan:")
            deskripsi_lanjut = f"Peripheral Reqs: {peri_desc}"
        else:
            st.write("Sila berikan butiran atau huraian masalah:")
            deskripsi_lanjut = st.text_area("Huraian Masalah / Spesifikasi (Please describe in detail)")

        st.markdown("<br>", unsafe_allow_html=True)
        hantar_btn = st.button("🚀 Hantar Permohonan (Submit ISR)", type="primary", use_container_width=True)
        
        if hantar_btn:
            if jabatan and deskripsi_lanjut.strip():
                df_req = pd.read_csv(REQUESTS_FILE, dtype=str).fillna("")
                tarikh_hari_ini = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
                ticket_id = f"TKT-{random.randint(10000, 99999)}"
                need_before_str = need_before.strftime("%d-%m-%Y")
                
                new_req = {
                    "Ticket_ID": ticket_id,
                    "Tarikh": tarikh_hari_ini,
                    "Pengguna": st.session_state["username"], 
                    "Jabatan": jabatan,
                    "Need_Before": need_before_str,
                    "Section_Head": "⏳ Menunggu", 
                    "Dept_Head": "⏳ Menunggu",
                    "Kategori": kategori,
                    "Deskripsi": deskripsi_lanjut,
                    "IT_Report": "", 
                    "Done_By": "",
                    "Date_Completed": "",
                    "IT_Sec_Head": "⏳ Menunggu",
                    "IT_Dept_Head": "⏳ Menunggu",
                    "Status": "🔴 Belum Diproses (Pending)"
                }
                df_req = pd.concat([df_req, pd.DataFrame([new_req])], ignore_index=True)
                df_req.to_csv(REQUESTS_FILE, index=False)
                
                st.toast(f"Berjaya! Tiket {ticket_id} telah dihantar.", icon="🚀")
                st.success(f"✅ Borang ISR telah berjaya dihantar. ID Rujukan anda ialah **{ticket_id}**.")
            else:
                st.error("Sila isi ruangan Jabatan dan pastikan butiran permohonan telah dilengkapkan.")

    with tab_history:
        st.subheader("📋 Senarai Permohonan Saya (ISR History)")
        df_req = pd.read_csv(REQUESTS_FILE, dtype=str).fillna("")
        my_reqs = df_req[df_req["Pengguna"] == st.session_state["username"]].copy()
        
        if my_reqs.empty:
            st.info("Anda belum membuat sebarang permohonan ISR.")
        else:
            def color_my_ticket_rows(row):
                status_val = str(row['Status']) if pd.notna(row['Status']) else ""
                if 'Pending' in status_val:
                    return ['background-color: #FEE2E2; color: #991B1B'] * len(row)
                elif 'In Progress' in status_val:
                    return ['background-color: #FEF3C7; color: #92400E'] * len(row)
                elif 'Completed' in status_val:
                    return ['background-color: #D1FAE5; color: #065F46'] * len(row)
                elif 'Cancelled' in status_val:
                    return ['background-color: #F3F4F6; color: #6B7280; font-style: italic'] * len(row)
                return [''] * len(row)

            sub_tabs = st.tabs(["Semua", "Baru (Pending)", "Dalam Proses", "Selesai", "Dibatalkan"])
            filters = ["Semua Tiket", "🔴 Belum Diproses (Pending)", "🟡 Sedang Disemak (In Progress)", "🟢 Selesai (Completed)", "⚫ Dibatalkan (Cancelled)"]
            
            for i, s_tab in enumerate(sub_tabs):
                with s_tab:
                    f = filters[i]
                    if f == "Semua Tiket":
                        df_view = my_reqs.copy()
                    else:
                        df_view = my_reqs[my_reqs["Status"] == f].copy()
                        
                    if df_view.empty:
                        st.write("Tiada rekod.")
                    else:
                        df_hide_it = df_view.drop(columns=["IT_Report", "IT_Sec_Head", "IT_Dept_Head", "Done_By", "Date_Completed"], errors='ignore')
                        
                        for idx, v_row in df_view.iterrows():
                            with st.expander(f"🎫 {v_row['Ticket_ID']} - {v_row['Kategori']}"):
                                st.write(f"**Status Semasa:** {v_row['Status']}")
                                html_preview = generate_isr_html(v_row)
                                st.markdown(html_preview, unsafe_allow_html=True)
                                st.download_button(
                                    label="📥 Muat Turun Borang ISR (HTML)",
                                    data=html_preview,
                                    file_name=f"{v_row['Ticket_ID']}_ISR.html",
                                    mime="text/html",
                                    key=f"dl_user_{v_row['Ticket_ID']}_{i}"
                                )

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 🗑️ Batal / Padam Permohonan")
            col_del1, col_del2 = st.columns([2,1])
            with col_del1:
                ticket_to_cancel = st.selectbox("Pilih ID Tiket yang ingin dibatalkan:", my_reqs["Ticket_ID"].tolist())
            with col_del2:
                st.write("")
                st.write("")
                if st.button("Batal & Padam Tiket", type="secondary", use_container_width=True):
                    df_req_new = pd.read_csv(REQUESTS_FILE, dtype=str).fillna("")
                    df_req_new = df_req_new[df_req_new["Ticket_ID"] != ticket_to_cancel]
                    df_req_new.to_csv(REQUESTS_FILE, index=False)
                    st.toast(f"Tiket {ticket_to_cancel} berjaya dibatalkan!", icon="🗑️")
                    st.rerun()

    if tab_approval:
        with tab_approval:
            st.subheader("✅ Pengesahan Ketua (Section/Dept Head)")
            st.write("Sila semak permohonan kakitangan dan sahkan/luluskan agar pihak IT dapat memulakan tugas.")
            
            df_all = pd.read_csv(REQUESTS_FILE, dtype=str).fillna("")
            pending_app = df_all[(df_all["Section_Head"] == "⏳ Menunggu") | (df_all["Dept_Head"] == "⏳ Menunggu")]
            
            if pending_app.empty:
                st.success("🎉 Tiada permohonan baharu yang memerlukan pengesahan/kelulusan anda buat masa ini.")
            else:
                for idx, row in pending_app.iterrows():
                    with st.expander(f"🎫 {row['Ticket_ID']} - {display_name(row['Pengguna'])} ({row['Kategori']})", expanded=False):
                        html_preview = generate_isr_html(row)
                        st.markdown(html_preview, unsafe_allow_html=True)
                        st.download_button(
                            label="📥 Muat Turun Borang ISR",
                            data=html_preview,
                            file_name=f"{row['Ticket_ID']}_ISR.html",
                            mime="text/html",
                            key=f"dl_app_user_{row['Ticket_ID']}"
                        )
                        col_c1, col_c2 = st.columns(2)
                        with col_c1:
                            if st.session_state["roles"].get("Is_Section_Head", False) and row['Section_Head'] == "⏳ Menunggu":
                                if st.button("✅ Confirm (Sahkan)", key=f"user_sec_btn_{row['Ticket_ID']}"):
                                    df_all.at[idx, "Section_Head"] = st.session_state["username"]
                                    df_all.to_csv(REQUESTS_FILE, index=False)
                                    st.toast("Pengesahan direkodkan!", icon="✅")
                                    st.rerun()
                        with col_c2:
                            if st.session_state["roles"].get("Is_Dept_Head", False) and row['Dept_Head'] == "⏳ Menunggu":
                                if row['Section_Head'] == "⏳ Menunggu":
                                    st.warning("Perlu tunggu Confirm dari Section Head dahulu.")
                                else:
                                    if st.button("✅ Approve (Luluskan)", key=f"user_dept_btn_{row['Ticket_ID']}", type="primary"):
                                        df_all.at[idx, "Dept_Head"] = st.session_state["username"]
                                        df_all.to_csv(REQUESTS_FILE, index=False)
                                        st.toast("Kelulusan direkodkan!", icon="✅")
                                        st.rerun()

# ---------------------------------------------------------
# MODUL: PENGURUSAN TIKET (ADMIN ONLY) MENGGUNAKAN ISR
# ---------------------------------------------------------
elif pilihan_menu == "Pengurusan Tiket (ISR)":
    st.title("📨 Pengurusan Tiket IT (ISR)")
    st.write("Semak aduan dan masukkan laporan teknikal IT untuk tindakan selanjutnya.")
    st.markdown("---")
    
    df_req = pd.read_csv(REQUESTS_FILE, dtype=str).fillna("")
    
    if df_req.empty:
        st.info("Tiada sebarang permohonan ISR pada masa ini.")
    else:
        pending_count = len(df_req[df_req["Status"] == "🔴 Belum Diproses (Pending)"])
        progress_count = len(df_req[df_req["Status"] == "🟡 Sedang Disemak (In Progress)"])
        completed_count = len(df_req[df_req["Status"] == "🟢 Selesai (Completed)"])
        cancelled_count = len(df_req[df_req["Status"] == "⚫ Dibatalkan (Cancelled)"])
        
        if pending_count > 0:
            st.toast(f"Terdapat {pending_count} tiket belum disemak!", icon="🔔")

        st.subheader("📊 Ringkasan Status Tiket")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🔴 Belum Diproses", pending_count)
        col2.metric("🟡 Sedang Disemak", progress_count)
        col3.metric("🟢 Selesai", completed_count)
        col4.metric("⚫ Dibatalkan", cancelled_count)
        st.markdown("---")

        def color_ticket_rows(row):
            status_val = str(row['Status']) if pd.notna(row['Status']) else ""
            if 'Pending' in status_val:
                return ['background-color: #FEE2E2; color: #991B1B'] * len(row)
            elif 'In Progress' in status_val:
                return ['background-color: #FEF3C7; color: #92400E'] * len(row)
            elif 'Completed' in status_val:
                return ['background-color: #D1FAE5; color: #065F46'] * len(row)
            elif 'Cancelled' in status_val:
                return ['background-color: #F3F4F6; color: #6B7280; font-style: italic'] * len(row)
            return [''] * len(row)

        tabs_tiket = st.tabs([
            "📋 Semua Tiket", 
            "🔴 Baru (Pending)", 
            "🟡 Dalam Proses", 
            "🟢 Selesai", 
            "⚫ Dibatalkan",
            "✅ Pengesahan Ketua (Sect/Dept)",
            "🛡️ Pengesahan IT (IT Head)"
        ])
        
        status_filters = [
            "Semua Tiket", 
            "🔴 Belum Diproses (Pending)", 
            "🟡 Sedang Disemak (In Progress)", 
            "🟢 Selesai (Completed)", 
            "⚫ Dibatalkan (Cancelled)"
        ]
        
        for i in range(5):
            with tabs_tiket[i]:
                status_filter = status_filters[i]
                if status_filter == "Semua Tiket":
                    df_paparan = df_req.copy()
                else:
                    df_paparan = df_req[df_req["Status"] == status_filter].copy()
                    
                if df_paparan.empty:
                    st.info("Tiada rekod ISR untuk kategori ini.")
                else:
                    st.write("💡 Anda boleh edit ruangan `Status`, `IT_Report`, `Done_By` dan `Date_Completed` di bawah.")
                    
                    df_paparan["IT_Report"] = df_paparan["IT_Report"].astype(str)
                    df_paparan["Done_By"] = df_paparan["Done_By"].astype(str)
                    df_paparan["Date_Completed"] = df_paparan["Date_Completed"].astype(str)
                    df_paparan["Status"] = df_paparan["Status"].astype(str)
                    
                    edited_df = st.data_editor(
                        df_paparan.style.apply(color_ticket_rows, axis=1),
                        column_config={
                            "IT_Report": st.column_config.TextColumn("Laporan IT (Tindakan)", width="large"),
                            "Done_By": st.column_config.TextColumn("Dilakukan Oleh (Nama IT)"),
                            "Date_Completed": st.column_config.TextColumn("Tarikh Siap (DD-MM-YYYY)"),
                            "Status": st.column_config.SelectboxColumn("Status Tindakan", options=["🔴 Belum Diproses (Pending)", "🟡 Sedang Disemak (In Progress)", "🟢 Selesai (Completed)", "⚫ Dibatalkan (Cancelled)"], required=True)
                        },
                        disabled=["Ticket_ID", "Tarikh", "Pengguna", "Jabatan", "Need_Before", "Section_Head", "Dept_Head", "Kategori", "Deskripsi", "IT_Sec_Head", "IT_Dept_Head"],
                        use_container_width=True,
                        num_rows="dynamic",
                        key=f"ticket_editor_{i}"
                    )
                    
                    if st.button(f"💾 Simpan Perubahan IT Report & Status", key=f"btn_save_tiket_{i}", type="primary"):
                        df_req_latest = pd.read_csv(REQUESTS_FILE, dtype=str).fillna("")
                        df_req_latest.set_index("Ticket_ID", inplace=True)
                        edited_df.set_index("Ticket_ID", inplace=True)
                        df_req_latest.update(edited_df)
                        df_req_latest.reset_index(inplace=True)
                        df_req_latest.to_csv(REQUESTS_FILE, index=False)
                        st.toast("Laporan IT & Status berjaya disimpan!", icon="✅")
                        st.rerun()

                    st.markdown("#### 📄 Paparan Borang ISR (Cetak / Muat Turun)")
                    for idx, v_row in df_paparan.iterrows():
                        with st.expander(f"🎫 {v_row['Ticket_ID']} - {display_name(v_row['Pengguna'])} ({v_row['Kategori']})"):
                            html_preview = generate_isr_html(v_row)
                            st.markdown(html_preview, unsafe_allow_html=True)
                            st.download_button(
                                label="📥 Muat Turun Borang ISR (HTML)",
                                data=html_preview,
                                file_name=f"{v_row['Ticket_ID']}_ISR.html",
                                mime="text/html",
                                key=f"dl_admin_{v_row['Ticket_ID']}_{i}"
                            )

        with tabs_tiket[5]:
            st.subheader("✅ Pengesahan Ketua (Section/Dept Head)")
            st.write("Ruangan untuk Ketua Seksyen / Jabatan mengesahkan permohonan sebelum diproses IT.")
            
            pending_app = df_req[(df_req["Section_Head"] == "⏳ Menunggu") | (df_req["Dept_Head"] == "⏳ Menunggu")]
            if pending_app.empty:
                st.success("🎉 Tiada permohonan yang memerlukan pengesahan/kelulusan buat masa ini.")
            else:
                for idx, row in pending_app.iterrows():
                    with st.expander(f"🎫 {row['Ticket_ID']} - {display_name(row['Pengguna'])} ({row['Kategori']})", expanded=False):
                        html_preview = generate_isr_html(row)
                        st.markdown(html_preview, unsafe_allow_html=True)
                        st.download_button(
                            label="📥 Muat Turun Borang ISR",
                            data=html_preview,
                            file_name=f"{row['Ticket_ID']}_ISR.html",
                            mime="text/html",
                            key=f"dl_app_admin_{row['Ticket_ID']}"
                        )
                        col_c1, col_c2 = st.columns(2)
                        with col_c1:
                            if st.session_state["roles"].get("Is_Section_Head", False) and row['Section_Head'] == "⏳ Menunggu":
                                if st.button("✅ Confirm (Sahkan)", key=f"admin_sec_btn_{row['Ticket_ID']}"):
                                    df_req.at[idx, "Section_Head"] = st.session_state["username"]
                                    df_req.to_csv(REQUESTS_FILE, index=False)
                                    st.toast("Pengesahan direkodkan!", icon="✅")
                                    st.rerun()
                        with col_c2:
                            if st.session_state["roles"].get("Is_Dept_Head", False) and row['Dept_Head'] == "⏳ Menunggu":
                                if row['Section_Head'] == "⏳ Menunggu":
                                    st.warning("Perlu tunggu Confirm dari Section Head dahulu.")
                                else:
                                    if st.button("✅ Approve (Luluskan)", key=f"admin_dept_btn_{row['Ticket_ID']}", type="primary"):
                                        df_req.at[idx, "Dept_Head"] = st.session_state["username"]
                                        df_req.to_csv(REQUESTS_FILE, index=False)
                                        st.toast("Kelulusan direkodkan!", icon="✅")
                                        st.rerun()

        with tabs_tiket[6]:
            st.subheader("🛡️ Pengesahan Ketulenan Borang (IT Management)")
            st.write("Ruangan khas untuk Ketua IT mengesahkan borang bagi pihak IT.")
            
            st.markdown("#### ⏳ Senarai Dalam Giliran IT (Kerja Belum Disiapkan)")
            st.write("Senarai tiket di bawah telah diluluskan oleh Ketua Jabatan dan sedia untuk dilaksanakan oleh IT.")
            belum_siap_it = df_req[(df_req["Dept_Head"] != "⏳ Menunggu") & (df_req["Status"] != "🟢 Selesai (Completed)") & (df_req["Status"] != "⚫ Dibatalkan (Cancelled)")]
            
            if belum_siap_it.empty:
                st.info("Tiada tiket dalam giliran kerja IT.")
            else:
                df_view_belum_siap = belum_siap_it[["Ticket_ID", "Tarikh", "Pengguna", "Kategori", "Status"]]
                st.dataframe(df_view_belum_siap, use_container_width=True)

            st.markdown("---")
            st.markdown("#### 🟢 Sedia Untuk Disahkan (Oleh IT Head)")
            
            pending_it_app = df_req[(df_req["Section_Head"] != "⏳ Menunggu") & (df_req["Dept_Head"] != "⏳ Menunggu") & ((df_req["IT_Sec_Head"] == "⏳ Menunggu") | (df_req["IT_Dept_Head"] == "⏳ Menunggu"))]
            
            if pending_it_app.empty:
                st.success("Tiada tiket yang memerlukan pengesahan IT buat masa ini.")
            else:
                for idx, row in pending_it_app.iterrows():
                    with st.expander(f"🎫 {row['Ticket_ID']} - {row['Kategori']}", expanded=False):
                        html_preview = generate_isr_html(row)
                        st.markdown(html_preview, unsafe_allow_html=True)
                        st.download_button(
                            label="📥 Muat Turun Borang ISR",
                            data=html_preview,
                            file_name=f"{row['Ticket_ID']}_ISR.html",
                            mime="text/html",
                            key=f"dl_it_app_{row['Ticket_ID']}"
                        )
                        col_it1, col_it2 = st.columns(2)
                        with col_it1:
                            if st.session_state["roles"].get("Is_IT_Sec_Head", False) and row.get('IT_Sec_Head') == "⏳ Menunggu":
                                if st.button("✅ Confirm (IT Sec Head)", key=f"it_sec_btn_{row['Ticket_ID']}"):
                                    df_req.at[idx, "IT_Sec_Head"] = st.session_state["username"]
                                    df_req.to_csv(REQUESTS_FILE, index=False)
                                    st.toast("Pengesahan IT direkodkan!", icon="✅")
                                    st.rerun()
                        with col_it2:
                            if st.session_state["roles"].get("Is_IT_Dept_Head", False) and row.get('IT_Dept_Head') == "⏳ Menunggu":
                                if row.get('IT_Sec_Head') == "⏳ Menunggu":
                                    st.warning("Perlu tunggu Confirm dari IT Section Head dahulu.")
                                else:
                                    if st.button("✅ Approve (IT Dept Head)", key=f"it_dept_btn_{row['Ticket_ID']}", type="primary"):
                                        df_req.at[idx, "IT_Dept_Head"] = st.session_state["username"]
                                        df_req.to_csv(REQUESTS_FILE, index=False)
                                        st.toast("Kelulusan IT direkodkan!", icon="✅")
                                        st.rerun()

        st.markdown("---")
        st.markdown("#### 🗑️ Padam Rekod Tiket")
        
        col_del1, col_del2 = st.columns([2, 1])
        with col_del1:
            tiket_untuk_dipadam = st.selectbox(
                "Pilih ID Tiket yang ingin dipadam sepenuhnya:", 
                df_req["Ticket_ID"].tolist(),
                key="admin_delete_ticket"
            )
        with col_del2:
            st.write("")
            st.write("")
            if st.button("🗑️ Padam Tiket Ini", type="secondary", use_container_width=True):
                df_req_terkini = pd.read_csv(REQUESTS_FILE, dtype=str).fillna("")
                df_req_terkini = df_req_terkini[df_req_terkini["Ticket_ID"] != tiket_untuk_dipadam]
                df_req_terkini.to_csv(REQUESTS_FILE, index=False)
                st.toast(f"Tiket {tiket_untuk_dipadam} berjaya dipadam sepenuhnya!", icon="🗑️")
                st.rerun()

# ---------------------------------------------------------
# MODUL: INVENTORI IT (ADMIN ONLY)
# ---------------------------------------------------------
elif pilihan_menu == "Inventori IT (Master Data)":
    @st.cache_data
    def load_all_sheets(file_path):
        xls = pd.ExcelFile(file_path)
        sheets_data = {}
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            sheets_data[sheet_name] = df
        return sheets_data

    if not os.path.exists(EXCEL_FILE):
        st.error(f"Fail '{EXCEL_FILE}' tidak dijumpai.")
        st.stop()

    data_dict = load_all_sheets(EXCEL_FILE)
    sheet_list = list(data_dict.keys())

    if st.sidebar.button("🔄 Refresh Data Excel"):
        st.cache_data.clear()
        st.toast("Data Excel disegerakkan!", icon="🔄")
        st.rerun()

    st.sidebar.markdown("---")
    try:
        with open(EXCEL_FILE, "rb") as file:
            st.sidebar.download_button(
                label="📥 Muat Turun Excel Terkini",
                data=file,
                file_name="PC Master Data In SMY_Terkini.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    except Exception as e:
        pass

    col_title, col_sheet = st.columns([2, 1])
    with col_title:
        st.title("🖥️ Master Inventori PC")
    with col_sheet:
        selected_sheet = st.selectbox("Pilih Pangkalan Data (Sheet):", sheet_list)

    st.markdown("---")
    df_current = data_dict[selected_sheet].copy()

    if "Remark" not in df_current.columns:
        df_current["Remark"] = "" 

    tab1, tab2 = st.tabs(["🔍 Semakan & Carian", "✏️ Kemaskini Rekod"])

    with tab1:
        def color_remark_rows(row):
            if 'Remark' in row:
                remark_val = str(row['Remark']).strip().upper() if pd.notna(row['Remark']) else ""
                if remark_val in ['BERHENTI', 'DEACTIVATED']:
                    return ['background-color: #FEE2E2; color: #991B1B'] * len(row)
                elif remark_val == 'OKTA VERIFY':
                    return ['background-color: #DBEAFE; color: #1E40AF'] * len(row)
                elif remark_val == 'YUBIKEY':
                    return ['background-color: #E0E7FF; color: #3730A3'] * len(row)
                elif remark_val == 'GOOGLE PASSWORD MANAGER':
                    return ['background-color: #FCE7F3; color: #9D174D'] * len(row)
                elif remark_val == 'KONTRAK':
                    return ['background-color: #FEF3C7; color: #92400E'] * len(row)
                elif remark_val == 'AKTIF':
                    return ['background-color: #D1FAE5; color: #065F46'] * len(row)
            return [''] * len(row)
            
        search_term = st.text_input("Carian umum (Nama, Hostname, IP, dsb.):", "")
        if search_term:
            mask = df_current.astype(str).apply(lambda row: row.str.contains(search_term, case=False, na=False)).any(axis=1)
            filtered_df = df_current[mask]
            st.dataframe(filtered_df.style.apply(color_remark_rows, axis=1), use_container_width=True)
        else:
            st.dataframe(df_current.style.apply(color_remark_rows, axis=1), use_container_width=True)

    with tab2:
        action = st.radio("Tindakan:", ["➕ Tambah Rekod Baharu", "✏️ Edit Rekod Sedia Ada"], horizontal=True)
        st.markdown("---")
        
        if action == "➕ Tambah Rekod Baharu":
            with st.form("add_form"):
                new_data = {}
                cols = st.columns(2)
                for idx, col_name in enumerate(df_current.columns):
                    with cols[idx % 2]:
                        if col_name == "Remark":
                            new_data[col_name] = st.selectbox(col_name, ["Aktif", "Berhenti", "Deactivated", "Kontrak", "OKTA Verify", "Yubikey", "Lain-lain"], key=f"add_{col_name}")
                        else:
                            new_data[col_name] = st.text_input(col_name, key=f"add_{col_name}")
                if st.form_submit_button("Simpan Rekod", type="primary"):
                    for k, v in new_data.items():
                        if v == "": new_data[k] = None
                    new_row_df = pd.DataFrame([new_data])
                    df_updated = pd.concat([df_current, new_row_df], ignore_index=True)
                    with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
                        df_updated.to_excel(writer, sheet_name=selected_sheet, index=False)
                    
                    st.toast("Rekod berjaya ditambah!", icon="✅")
                    st.cache_data.clear()
                    st.rerun() 

        elif action == "✏️ Edit Rekod Sedia Ada":
            search_edit = st.text_input("🔍 Taipkan identiti pekerja atau peranti untuk mencari:", key="search_edit_input")
            if search_edit:
                mask = df_current.astype(str).apply(lambda row: row.str.contains(search_edit, case=False, na=False)).any(axis=1)
                filtered_df = df_current[mask]
                
                if not filtered_df.empty:
                    options = {}
                    for idx, row in filtered_df.iterrows():
                        primary_info = ""
                        for possible_col in ["Username", "Name", "Nama"]:
                            if possible_col in df_current.columns and pd.notna(row[possible_col]):
                                primary_info = f"[{row[possible_col]}] "
                                break
                        info_ringkas = " | ".join([f"{str(row[col])}" for col in df_current.columns[:2] if pd.notna(row[col]) and str(row[col]).strip() != ""])
                        options[f"Baris {idx} -> {primary_info}{info_ringkas}"] = idx 
                    
                    selected_label = st.selectbox("Pilih rekod spesifik untuk disunting:", options=list(options.keys()))
                    row_to_edit = options[selected_label] 
                    current_row = df_current.loc[row_to_edit]
                    
                    with st.form("edit_form"):
                        updated_data = {}
                        cols = st.columns(2)
                        for idx_col, col_name in enumerate(df_current.columns):
                            val = str(current_row[col_name]) if pd.notna(current_row[col_name]) else ""
                            with cols[idx_col % 2]:
                                if col_name == "Remark":
                                    remark_options = ["Aktif", "Berhenti", "Deactivated", "Kontrak", "OKTA Verify", "Yubikey", "Lain-lain"]
                                    if val and val not in remark_options: remark_options.append(val)
                                    default_index = remark_options.index(val) if val in remark_options else 0
                                    updated_data[col_name] = st.selectbox(col_name, options=remark_options, index=default_index, key=f"edit_{row_to_edit}_{col_name}")
                                else:
                                    updated_data[col_name] = st.text_input(col_name, value=val, key=f"edit_{row_to_edit}_{col_name}")
                        
                        if st.form_submit_button("Kemaskini Maklumat", type="primary"):
                            df_current = df_current.astype(object)
                            for col_name in df_current.columns:
                                val = updated_data[col_name]
                                df_current.at[row_to_edit, col_name] = None if val == "" else val
                            
                            with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
                                df_current.to_excel(writer, sheet_name=selected_sheet, index=False)
                            
                            st.toast(f"Rekod baris {row_to_edit} telah dikemaskini!", icon="✅")
                            st.cache_data.clear()
                            st.rerun()

# ---------------------------------------------------------
# MODUL: TETAPAN PORTAL (ADMIN / SUPER ADMIN ONLY)
# ---------------------------------------------------------
elif pilihan_menu == "Tetapan Portal":
    st.title("⚙️ Tetapan Portal & Pengurusan Peranan")
    st.write("Uruskan logo syarikat dan tetapkan tahap akses untuk pengguna.")
    st.markdown("---")
    
    if st.session_state["roles"].get("Is_Super_Admin", False) or st.session_state["roles"].get("Is_Admin", False):
        
        st.subheader("💬 Tetapan Ruangan Komuniti & PM")
        st.write("Kawal akses fungsi sembang di sini.")
        
        chat_enabled_str = get_setting("Community_Chat_Enabled", "True")
        is_chat_enabled = (chat_enabled_str == "True")
        new_chat_status = st.toggle("Buka Ruangan Komuniti Umum (Benarkan staf bersembang)", value=is_chat_enabled)
        if new_chat_status != is_chat_enabled:
            set_setting("Community_Chat_Enabled", "True" if new_chat_status else "False")
            st.toast("Tetapan Ruangan Komuniti dikemaskini!", icon="✅")
            st.rerun()
            
        pm_enabled_str = get_setting("Private_Chat_Enabled", "True")
        is_pm_enabled = (pm_enabled_str == "True")
        new_pm_status = st.toggle("Buka Ruangan Mesej Peribadi (PM)", value=is_pm_enabled)
        if new_pm_status != is_pm_enabled:
            set_setting("Private_Chat_Enabled", "True" if new_pm_status else "False")
            st.toast("Tetapan Mesej Peribadi (PM) dikemaskini!", icon="✅")
            st.rerun()
            
        st.markdown("---")

        st.subheader("👥 Pengurusan Peranan Akses (Role Management)")
        st.write("Tandakan kotak pada jadual untuk memberi atau menarik balik kuasa staf.")
        
        df_roles = pd.read_csv(ROLES_FILE)
        bool_cols = ["Is_Admin", "Is_Section_Head", "Is_Dept_Head", "Is_IT_Sec_Head", "Is_IT_Dept_Head"]
        for col in bool_cols:
            if col not in df_roles.columns:
                df_roles[col] = False 
            df_roles[col] = df_roles[col].astype(str).str.lower().map({'true': True, 'false': False}).fillna(False)

        excel_users = get_excel_users(EXCEL_FILE)
        semua_pengguna = list(USER_CREDENTIALS.keys()) + list(excel_users.keys())
        semua_pengguna = sorted(list(set(semua_pengguna))) 
        
        with st.form("tambah_role_form"):
            new_role_user = st.selectbox("Pilih Staf untuk Ditambah / Dikemaskini Peranan:", ["-- Pilih --"] + semua_pengguna)
            st.write("Tandakan jenis akses yang mahu diberikan:")
            c1, c2, c3, c4, c5 = st.columns(5)
            with c1: is_adm = st.checkbox("Admin IT")
            with c2: is_shead = st.checkbox("Section Head")
            with c3: is_dhead = st.checkbox("Dept Head")
            with c4: is_it_shead = st.checkbox("IT Sec Head")
            with c5: is_it_dhead = st.checkbox("IT Dept Head")
            
            if st.form_submit_button("Simpan Akses Pengguna", type="primary"):
                if new_role_user != "-- Pilih --":
                    mask = df_roles["Username"] == new_role_user
                    if mask.any():
                        df_roles.loc[mask, "Is_Admin"] = is_adm
                        df_roles.loc[mask, "Is_Section_Head"] = is_shead
                        df_roles.loc[mask, "Is_Dept_Head"] = is_dhead
                        df_roles.loc[mask, "Is_IT_Sec_Head"] = is_it_shead
                        df_roles.loc[mask, "Is_IT_Dept_Head"] = is_it_dhead
                    else:
                        new_role = pd.DataFrame([{
                            "Username": new_role_user, "Is_Admin": is_adm, "Is_Super_Admin": False, 
                            "Is_Section_Head": is_shead, "Is_Dept_Head": is_dhead, 
                            "Is_IT_Sec_Head": is_it_shead, "Is_IT_Dept_Head": is_it_dhead
                        }])
                        df_roles = pd.concat([df_roles, new_role], ignore_index=True)
                    df_roles.to_csv(ROLES_FILE, index=False)
                    st.toast(f"Akses untuk {new_role_user} telah dikemaskini!", icon="✅")
                    st.rerun()
                else:
                    st.warning("Sila pilih pengguna dari senarai.")

        st.markdown("<br>", unsafe_allow_html=True)
        st.write("**Senarai Kuasa Semasa (Boleh edit terus di dalam jadual):**")
        
        df_roles_view = df_roles.drop(columns=["Is_Super_Admin"], errors="ignore")
        edited_roles = st.data_editor(df_roles_view, num_rows="dynamic", use_container_width=True)
        
        if st.button("💾 Simpan Perubahan Jadual Role", type="primary"):
            if "Is_Super_Admin" in df_roles.columns:
                edited_roles["Is_Super_Admin"] = df_roles["Is_Super_Admin"]
            else:
                edited_roles["Is_Super_Admin"] = False
                
            edited_roles.to_csv(ROLES_FILE, index=False)
            st.toast("Jadual peranan dikemaskini!", icon="✅")
            st.rerun()

        st.markdown("---")

    st.subheader("🖼️ Tetapan Logo Syarikat")
    uploaded_file = st.file_uploader("Sila muat naik fail logo (.png, .jpg disyorkan)", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Pratonton Logo", width=300)
        col_a, col_b = st.columns([1, 1])
        with col_a:
            if st.button("Simpan & Jadikan Logo Rasmi", type="primary", use_container_width=True):
                if not os.path.exists("uploaded_images"):
                    os.makedirs("uploaded_images")
                with open(COMPANY_LOGO_PATH, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.toast("Logo rasmi berjaya dikemaskini!", icon="🏢")
                st.rerun()
                
    if os.path.exists(COMPANY_LOGO_PATH):
        if st.button("Alih Keluar Logo Semasa (Reset)"):
            os.remove(COMPANY_LOGO_PATH)
            st.rerun()