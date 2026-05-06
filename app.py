import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="🎬 CinemaVault Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');
  html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background-color: #0d0d14; color: #e8e0d5; }
  .stApp { background: linear-gradient(135deg, #0d0d14 0%, #12101e 60%, #0a1520 100%); }
  [data-testid="stSidebar"] { background: linear-gradient(180deg, #13111f 0%, #0e1a2a 100%); border-right: 1px solid #2a2540; }
  [data-testid="stSidebar"] * { color: #ddd6cc !important; }
  .dash-title { font-family: 'Playfair Display', serif; font-size: 3rem; font-weight: 900; background: linear-gradient(90deg, #f5c518, #e8956d, #c96baf); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .dash-sub { font-size: 0.95rem; color: #8a8299; letter-spacing: 3px; text-transform: uppercase; }
  .metric-card { background: linear-gradient(135deg, #1a1730 0%, #141228 100%); border: 1px solid #2e2a45; border-radius: 16px; padding: 22px 24px; text-align: center; }
  .metric-emoji { font-size: 2rem; }
  .metric-val { font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 700; color: #f5c518; }
  .metric-label { font-size: 0.78rem; color: #8a8299; text-transform: uppercase; letter-spacing: 2px; }
  .section-hdr { font-family: 'Playfair Display', serif; font-size: 1.4rem; color: #f5c518; border-left: 4px solid #c96baf; padding-left: 12px; margin: 28px 0 14px; }
  .stButton > button { background: linear-gradient(90deg, #f5c518, #e8956d) !important; color: #0d0d14 !important; font-weight: 700 !important; border: none !important; border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

DEFAULT_MOVIES = [
    {"title": "Metropolis",          "filmmaker": "Fritz Lang",           "year": 1927, "genre": "Sci-Fi",    "medium": "35mm Film",  "price": 18.00, "attendance": 1840, "era": "Silent Era"},
    {"title": "Citizen Kane",        "filmmaker": "Orson Welles",         "year": 1941, "genre": "Drama",     "medium": "35mm Film",  "price": 22.00, "attendance": 3200, "era": "Golden Age"},
    {"title": "Vertigo",             "filmmaker": "Alfred Hitchcock",     "year": 1958, "genre": "Thriller",  "medium": "35mm Film",  "price": 24.00, "attendance": 4100, "era": "Golden Age"},
    {"title": "2001: A Space Odyssey","filmmaker": "Stanley Kubrick",     "year": 1968, "genre": "Sci-Fi",    "medium": "70mm Film",  "price": 28.00, "attendance": 5200, "era": "New Wave"},
    {"title": "Apocalypse Now",      "filmmaker": "Francis Ford Coppola", "year": 1979, "genre": "War",       "medium": "70mm Film",  "price": 26.00, "attendance": 4500, "era": "New Hollywood"},
    {"title": "Blade Runner",        "filmmaker": "Ridley Scott",         "year": 1982, "genre": "Sci-Fi",    "medium": "35mm Film",  "price": 25.00, "attendance": 4800, "era": "New Hollywood"},
    {"title": "Pulp Fiction",        "filmmaker": "Quentin Tarantino",    "year": 1994, "genre": "Crime",     "medium": "35mm Film",  "price": 27.00, "attendance": 6100, "era": "Modern"},
    {"title": "Mulholland Drive",    "filmmaker": "David Lynch",          "year": 2001, "genre": "Mystery",   "medium": "Digital",    "price": 20.00, "attendance": 2700, "era": "Modern"},
    {"title": "There Will Be Blood", "filmmaker": "Paul Thomas Anderson", "year": 2007, "genre": "Drama",     "medium": "Digital",    "price": 23.00, "attendance": 3300, "era": "Modern"},
    {"title": "Parasite",            "filmmaker": "Bong Joon-ho",         "year": 2019, "genre": "Thriller",  "medium": "Digital 4K", "price": 30.00, "attendance": 7200, "era": "Contemporary"},
    {"title": "Tár",                 "filmmaker": "Todd Field",           "year": 2022, "genre": "Drama",     "medium": "Digital 4K", "price": 29.00, "attendance": 4100, "era": "Contemporary"},
]

if "movies" not in st.session_state:
    st.session_state.movies = DEFAULT_MOVIES.copy()

with st.sidebar:
    st.markdown("## 🎬 CinemaVault")
    st.markdown("<p style='color:#8a8299;font-size:0.8rem;'>Curated Film Collection</p>", unsafe_allow_html=True)
    st.divider()
    st.markdown("### ➕ Add New Film")
    title      = st.text_input("🎞️ Film Title")
    filmmaker  = st.text_input("🎥 Filmmaker")
    year       = st.number_input("📅 Year", min_value=1888, max_value=datetime.now().year, value=2000, step=1)
    genre      = st.selectbox("🎭 Genre", ["Drama","Sci-Fi","Thriller","Crime","Horror","Romance","War","Comedy","Mystery","Noir","Animation","Documentary","Other"])
    medium     = st.selectbox("📽️ Medium", ["35mm Film","70mm Film","Digital","Digital 4K","IMAX","16mm Film"])
    era        = st.selectbox("🕰️ Cinema Era", ["Silent Era","Golden Age","New Wave","New Hollywood","Modern","Contemporary"])
    price      = st.number_input("💰 Ticket Price ($)", min_value=1.0, max_value=200.0, value=25.0, step=0.5)
    attendance = st.number_input("👥 Attendance", min_value=0, max_value=100000, value=3000, step=100)
    if st.button("🎬 Add to Collection", use_container_width=True):
        if title.strip() and filmmaker.strip():
            st.session_state.movies.append({"title": title.strip(), "filmmaker": filmmaker.strip(), "year": int(year), "genre": genre, "medium": medium, "price": float(price), "attendance": int(attendance), "era": era})
            st.success(f"✅ {title} added!")
            st.balloons()
        else:
            st.error("Please fill in Title and Filmmaker.")
    st.divider()
    if st.button("🔄 Reset to Defaults", use_container_width=True):
        st.session_state.movies = DEFAULT_MOVIES.copy()
        st.rerun()

df = pd.DataFrame(st.session_state.movies)

st.markdown('<p class="dash-title">🎬 CinemaVault</p>', unsafe_allow_html=True)
st.markdown('<p class="dash-sub">✦ Curated Cinematic Archive ✦</p>', unsafe_allow_html=True)
st.markdown("")

c1, c2, c3, c4, c5 = st.columns(5)
metrics = [
    ("🎞️", len(df), "Films"),
    ("🎥", df["filmmaker"].nunique(), "Filmmakers"),
    ("👥", f"{df['attendance'].sum():,}", "Total Viewers"),
    ("💰", f"${df['price'].mean():.2f}", "Avg. Ticket"),
    ("🏆", str(df.loc[df["attendance"].idxmax(), "year"]) if not df.empty else "—", "Best Year"),
]
for col, (emoji, val, label) in zip([c1,c2,c3,c4,c5], metrics):
    with col:
        st.markdown(f'<div class="metric-card"><div class="metric-emoji">{emoji}</div><div class="metric-val">{val}</div><div class="metric-label">{label}</div></div>', unsafe_allow_html=True)

st.markdown("")
left, right = st.columns([3, 2])

with left:
    st.markdown('<div class="section-hdr">📊 Attendance by Film</div>', unsafe_allow_html=True)
    chart_df = df.nlargest(12, "attendance").sort_values("attendance")
    fig_bar = go.Figure(go.Bar(
        x=chart_df["attendance"], y=chart_df["title"], orientation="h",
        marker=dict(color=chart_df["attendance"], colorscale=[[0,"#3a2060"],[0.4,"#c96baf"],[0.7,"#e8956d"],[1.0,"#f5c518"]], showscale=False),
        text=[f"  {v:,}" for v in chart_df["attendance"]], textposition="outside",
        textfont=dict(color="#e8e0d5", size=11),
    ))
    fig_bar.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#a09aaa"), xaxis=dict(showgrid=False, showticklabels=False, zeroline=False), yaxis=dict(tickfont=dict(size=12, color="#ddd6cc")), margin=dict(l=0,r=60,t=10,b=10), height=380)
    st.plotly_chart(fig_bar, use_container_width=True)

with right:
    st.markdown('<div class="section-hdr">🎭 Genre Distribution</div>', unsafe_allow_html=True)
    genre_counts = df["genre"].value_counts().reset_index()
    genre_counts.columns = ["genre", "count"]
    PALETTE = ["#f5c518","#e8956d","#c96baf","#7b62d4","#4fa8d8","#5dcea0","#f06060","#a0c96b"]
    fig_pie = go.Figure(go.Pie(labels=genre_counts["genre"], values=genre_counts["count"], hole=0.52, marker=dict(colors=PALETTE[:len(genre_counts)], line=dict(color="#0d0d14", width=3)), textfont=dict(size=11, color="#e8e0d5")))
    fig_pie.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#a09aaa"), margin=dict(l=0,r=0,t=10,b=10), height=380)
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown('<div class="section-hdr">🕰️ Films Through Time</div>', unsafe_allow_html=True)
ERA_COLORS = {"Silent Era":"#f5c518","Golden Age":"#e8956d","New Wave":"#c96baf","New Hollywood":"#7b62d4","Modern":"#4fa8d8","Contemporary":"#5dcea0"}
fig_time = px.scatter(df, x="year", y="attendance", size="price", color="era", color_discrete_map=ERA_COLORS, hover_name="title", size_max=40)
fig_time.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#a09aaa"), xaxis=dict(gridcolor="rgba(255,255,255,0.05)", zeroline=False), yaxis=dict(gridcolor="rgba(255,255,255,0.05)", zeroline=False), margin=dict(l=0,r=0,t=10,b=10), height=300)
st.plotly_chart(fig_time, use_container_width=True)

st.markdown('<div class="section-hdr">🗂️ Film Archive</div>', unsafe_allow_html=True)
search = st.text_input("🔍 Search by filmmaker or title…")
display_df = df.copy()
if search.strip():
    mask = df["title"].str.contains(search, case=False, na=False) | df["filmmaker"].str.contains(search, case=False, na=False)
    display_df = df[mask]
    if display_df.empty:
        st.warning(f"No films found matching '{search}'")

if not display_df.empty:
    show = display_df[["title","filmmaker","year","genre","era","medium","price","attendance"]].copy()
    show = show.sort_values("attendance", ascending=False).reset_index(drop=True)
    show.index += 1
    show.columns = ["🎞️ Title","🎥 Filmmaker","📅 Year","🎭 Genre","🕰️ Era","📽️ Medium","💰 Price ($)","👥 Attendance"]
    st.dataframe(show, use_container_width=True, height=min(40+38*len(show), 520))

st.divider()
st.markdown("<p style='text-align:center;color:#3a3555;font-size:0.78rem;'>🎬 CinemaVault Dashboard | Built with Streamlit & Plotly</p>", unsafe_allow_html=True)
