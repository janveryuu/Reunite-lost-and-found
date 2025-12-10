import streamlit as st
import datetime

# --- 1. SETUP & CONFIGURATION ---
st.set_page_config(
    page_title="REUNITE", 
    page_icon="🤝", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ADVANCED CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #020617;
        border-right: 1px solid #1e293b;
    }

    /* BIG CARD BUTTONS */
    div.stButton > button {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
        height: 140px; /* Taller for better click area */
        width: 100%;
        border-radius: 20px;
        font-size: 24px;
        transition: all 0.3s;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 1px;
        cursor: pointer;
        z-index: 1;
    }
    div.stButton > button:hover {
        background-color: rgba(255, 255, 255, 0.1);
        border-color: #60A5FA;
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        color: #60A5FA;
    }
    
    /* Hide Radio Circles */
    div[role="radiogroup"] > label > div:first-child { display: none; }
    div[role="radiogroup"] > label {
        padding: 15px 20px; border-radius: 12px; margin-bottom: 8px; border: 1px solid transparent; transition: all 0.2s;
    }
    div[role="radiogroup"] > label:hover { background: rgba(255, 255, 255, 0.1); cursor: pointer; }
    div[role="radiogroup"] label[data-checked="true"] {
        background: linear-gradient(90deg, #2563EB 0%, #1d4ed8 100%) !important;
        border: none; font-weight: bold; box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
    }
    
    /* Inputs */
    .stTextInput input, .stSelectbox div, .stDateInput input {
        background-color: rgba(0,0,0,0.3) !important;
        border-radius: 10px !important;
        border: 1px solid #334155 !important;
        color: white !important;
    }
    
    /* Animation */
    @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-10px); } 100% { transform: translateY(0px); } }
    .floating-logo { animation: float 3s ease-in-out infinite; display: block; margin-left: auto; margin-right: auto; }

</style>
""", unsafe_allow_html=True)

# --- 3. DATABASE ---
if 'database' not in st.session_state:
    st.session_state.database = [
        {"id": 1, "name": "Canon Calculator", "category": "Electronics", "color": "Black", "location": "Library", "date": datetime.date(2023, 11, 20), "question": "Back text?", "answer": "Nothing", "image": "https://m.media-amazon.com/images/I/71J1k-JkXUL.jpg"},
        {"id": 2, "name": "Hydroflask", "category": "Accessories", "color": "Blue", "location": "Gym", "date": datetime.date(2023, 11, 21), "question": "Dent?", "answer": "Yes", "image": "https://www.hydroflask.com/media/catalog/product/cache/9177cfe059281270017bcdd70e474368/w/3/w32ts415-white-32-oz-wide-mouth-straw-lid.jpg"},
        {"id": 3, "name": "Nike Jacket", "category": "Clothing", "color": "Black", "location": "Library", "date": datetime.date(2023, 11, 22), "question": "Size?", "answer": "Large", "image": None},
    ]

# --- 4. BACKEND FUNCTIONS ---
def get_hotspot():
    if not st.session_state.database: return "N/A"
    locs = [x['location'] for x in st.session_state.database]
    return max(set(locs), key=locs.count)

def add_item(name, category, color, location, date, question, answer, image_file):
    new_id = len(st.session_state.database) + 1
    new_item = {
        "id": new_id, "name": name, "category": category, "color": color,
        "location": location, "date": date, "question": question, "answer": answer, "image": image_file 
    }
    st.session_state.database.insert(0, new_item)

# --- 5. NAVIGATION LOGIC (The Fix) ---
# We define specific page names to avoid typos
PAGE_DASHBOARD = "🏠   Dashboard"
PAGE_SEARCH = "🔍   Search Items"
PAGE_REPORT = "📷   Report Found Item"

# Initialize Session State for Filters
if 'search_name' not in st.session_state: st.session_state.search_name = ""
if 'search_loc' not in st.session_state: st.session_state.search_loc = ""
if 'current_page' not in st.session_state: st.session_state.current_page = PAGE_DASHBOARD

# Callback functions to Force Page Switch
def go_to_search(filter_name="", filter_loc=""):
    st.session_state.current_page = PAGE_SEARCH
    st.session_state.search_name = filter_name
    st.session_state.search_loc = filter_loc

def set_page():
    # Update current_page based on Sidebar Selection
    st.session_state.current_page = st.session_state.nav_radio

# --- 6. SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4121/4121044.png", width=70)
    st.markdown("<h2 style='color: #60A5FA; margin:0;'>REUNITE</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 14px;'>Campus Asset Tracking</p>", unsafe_allow_html=True)
    st.write("")
    
    # We bind the radio button to 'nav_radio' key, but we set its index based on 'current_page'
    # This allows Buttons AND the Sidebar to control the same variable.
    options = [PAGE_DASHBOARD, PAGE_SEARCH, PAGE_REPORT]
    try:
        index = options.index(st.session_state.current_page)
    except ValueError:
        index = 0
        
    st.radio(
        "Navigation", 
        options,
        index=index,
        label_visibility="collapsed",
        key="nav_radio",
        on_change=set_page # When clicked, update the state
    )
    
    st.markdown("---")
    st.info("Logged in as **CpE Student**")

# ==========================================
# PAGE 1: HOME DASHBOARD
# ==========================================
if st.session_state.current_page == PAGE_DASHBOARD:
    # HERO
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("<h1 style='font-size: 4rem; font-weight: 700; background: -webkit-linear-gradient(#60A5FA, #FFFFFF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0;'>Lost it? <br> Let's find it.</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.2rem; color: #94A3B8;'>The centralized digital logbook for tracking and exchanging lost assets on campus.</p>", unsafe_allow_html=True)
    with c2:
        st.markdown('<img src="https://cdn-icons-png.flaticon.com/512/4121/4121044.png" class="floating-logo" width="200">', unsafe_allow_html=True)

    st.write("")
    st.write("")
    
    # STATS
    total = len(st.session_state.database)
    hotspot = get_hotspot()
    latest = st.session_state.database[0]['name'] if total > 0 else "None"

    # BUTTONS WITH CALLBACKS (The Clickable Fix)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Using on_click ensures the page switches BEFORE the app reruns
        st.button(f"{total}\nITEMS IN VAULT", on_click=go_to_search, args=("", ""))
            
    with col2:
        st.button(f"{hotspot}\nHOTSPOT LOCATION", on_click=go_to_search, args=("", hotspot))
            
    with col3:
        st.button(f"{latest}\nLATEST ARRIVAL", on_click=go_to_search, args=(latest, ""))

# ==========================================
# PAGE 2: SEARCH
# ==========================================
elif st.session_state.current_page == PAGE_SEARCH:
    st.title("🔍 Search Database")
    
    with st.container(border=True):
        c1, c2, c3, c4 = st.columns(4)
        
        # Inputs connected to session_state so they auto-fill
        s_name = c1.text_input("Item Name", value=st.session_state.search_name)
        s_loc = c2.text_input("Location", value=st.session_state.search_loc)
        cat = c3.selectbox("Category", ["All", "Electronics", "Clothing", "Documents", "Accessories"])
        col = c4.selectbox("Color", ["All", "Black", "White", "Blue", "Red", "Green"])
        
        if c4.button("Clear Filters"):
            st.session_state.search_name = ""
            st.session_state.search_loc = ""
            st.rerun()

    st.write("")

    matches = 0
    for item in st.session_state.database:
        # Flexible matching
        m_name = s_name.lower() in item['name'].lower()
        m_loc = s_loc.lower() in item['location'].lower()
        m_cat = True if cat == "All" else item['category'] == cat
        m_col = True if col == "All" else item['color'] == col
        
        if m_name and m_loc and m_cat and m_col:
            matches += 1
            
            with st.container(border=True):
                col_img, col_text = st.columns([1, 4])
                with col_img:
                    if item['image']:
                        st.image(item['image'], use_container_width=True)
                    else:
                        st.image("https://via.placeholder.com/150?text=No+Image", use_container_width=True)
                with col_text:
                    st.subheader(item['name'])
                    st.caption(f"📍 Found at {item['location']} | 📅 {item['date']}")
                    st.markdown(f"**Category:** `{item['category']}`  **Color:** `{item['color']}`")
                    
                    with st.expander("🔐 Claim this Item"):
                        st.write(f"Security Question: **{item['question']}**")
                        ans = st.text_input("Answer", key=item['id'])
                        if st.button("Verify Identity", key=f"btn_{item['id']}"):
                            if ans.lower().strip() == item['answer'].lower().strip():
                                st.balloons()
                                st.success("IDENTITY VERIFIED!")
                                st.markdown(f"""
                                    <div style="background:#dcfce7; color:#166534; padding:20px; border-radius:10px; text-align:center; border: 2px dashed #166534;">
                                        <h2>✅ APPROVED</h2>
                                        <p>Please pick up item <b>#{item['id']}</b> at the Student Office.</p>
                                    </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.error("Incorrect Answer")
    if matches == 0:
        st.info("No items found matching your filters.")

# ==========================================
# PAGE 3: REPORT
# ==========================================
elif st.session_state.current_page == PAGE_REPORT:
    st.title("📷 Report Found Item")
    
    with st.container(border=True):
        with st.form("report", clear_on_submit=True):
            c1, c2 = st.columns(2)
            name = c1.text_input("Item Name")
            loc = c2.text_input("Location Found")
            cat = c1.selectbox("Category", ["Electronics", "Clothing", "Documents", "Accessories", "Others"])
            color = c2.selectbox("Color", ["Black", "White", "Blue", "Red", "Green"])
            date = c1.date_input("Date")
            img = c2.file_uploader("Upload Image")
            
            st.divider()
            st.markdown("### 🔒 Security")
            q = st.text_input("Question (e.g. What is the wallpaper?)")
            a = st.text_input("Answer", type="password")
            
            if st.form_submit_button("Submit Report"):
                add_item(name, cat, color, loc, date, q, a, img)
                st.success("Item Reported Successfully!")