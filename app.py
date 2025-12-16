import streamlit as st
from crossword import build_puzzle

st.set_page_config(page_title="Para Jazmín 💛", page_icon="🧩", layout="centered")

# ===== Fondo capibara (SVG embebido) + casillas grandes =====
CAPY_SVG = r"""
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0b1020"/>
      <stop offset="1" stop-color="#101827"/>
    </linearGradient>
    <filter id="blur" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur stdDeviation="14"/>
    </filter>
  </defs>

  <rect width="1200" height="800" fill="url(#g)"/>

  <!-- soft blobs -->
  <circle cx="250" cy="160" r="140" fill="#ffffff" opacity="0.05" filter="url(#blur)"/>
  <circle cx="980" cy="220" r="170" fill="#ffffff" opacity="0.04" filter="url(#blur)"/>
  <circle cx="700" cy="640" r="210" fill="#ffffff" opacity="0.035" filter="url(#blur)"/>

  <!-- cute capybara silhouette -->
  <g opacity="0.20" transform="translate(660,420) scale(1.2)">
    <ellipse cx="120" cy="120" rx="170" ry="120" fill="#c89b6f"/>
    <ellipse cx="260" cy="105" rx="90" ry="70" fill="#c89b6f"/>
    <circle cx="285" cy="90" r="10" fill="#1b1f2a"/>
    <ellipse cx="305" cy="112" rx="18" ry="12" fill="#1b1f2a" opacity="0.45"/>
    <ellipse cx="250" cy="55" rx="24" ry="18" fill="#c89b6f"/>
    <ellipse cx="278" cy="55" rx="24" ry="18" fill="#c89b6f"/>
    <ellipse cx="70" cy="220" rx="40" ry="22" fill="#b88a61"/>
    <ellipse cx="160" cy="230" rx="45" ry="24" fill="#b88a61"/>
  </g>

  <!-- tiny hearts -->
  <g opacity="0.10" fill="#ffb6c1">
    <path d="M140 610c0-18 14-32 32-32 10 0 19 5 25 12 6-7 15-12 25-12 18 0 32 14 32 32 0 34-57 61-57 61s-57-27-57-61z"/>
    <path d="M1060 520c0-16 12-28 28-28 9 0 16 4 22 10 5-6 13-10 22-10 16 0 28 12 28 28 0 30-50 54-50 54s-50-24-50-54z"/>
  </g>
</svg>
"""

# CSS: background + bigger cells + nicer buttons
st.markdown(
    f"""
    <style>
      .stApp {{
        background-image: url("data:image/svg+xml;utf8,{CAPY_SVG.replace("#","%23").replace("%","%25").replace("<","%3C").replace(">","%3E").replace('"','%22')}");
        background-size: cover;
        background-attachment: fixed;
      }}

      /* Make the grid buttons look like big tiles */
      div[data-testid="stHorizontalBlock"] {{ gap: 0.45rem; }}

      button[kind="secondary"] {{
        width: 58px !important;
        height: 58px !important;
        padding: 0 !important;
        border-radius: 14px !important;
        font-weight: 800 !important;
        font-size: 18px !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        background: rgba(255,255,255,0.05) !important;
        backdrop-filter: blur(6px);
      }}
      button[kind="secondary"]:hover {{
        background: rgba(255,255,255,0.08) !important;
      }}

      .pill {{
        display:inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        background: rgba(0,0,0,0.35);
        border: 1px solid rgba(255,255,255,0.12);
        margin-right: 8px;
        font-size: 0.9rem;
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🧩 Sopa de letras para Jazmín 💛")
st.write("Encuentra y **selecciona** las palabras: **JAZMIN**, **PERDON**, **TEAMO**.")

# 🎵 Música (visible; autoplay con sonido suele bloquearse)
st.markdown("### 🎵 Música (toca ▶️ para reproducir)")
st.markdown(
    """
    <iframe width="420" height="240"
    src="https://www.youtube.com/embed/LLFokwpQfHQ?controls=1&rel=0"
    title="Coldplay - Trouble"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen></iframe>
    """,
    unsafe_allow_html=True,
)

# ====== CONGELAR EL TABLERO: generar SOLO una vez ======
if "puzzle" not in st.session_state:
    grid, _, placements = build_puzzle()
    st.session_state.puzzle = {"grid": grid, "placements": placements}
else:
    grid = st.session_state.puzzle["grid"]
    placements = st.session_state.puzzle["placements"]

SIZE = len(grid)

TARGETS = {"JAZMIN", "PERDON", "TEAMO"}

# Diccionario palabra -> posiciones
word_to_positions = {}
for p in placements:
    w = (p.word or "").strip().upper()
    if w in TARGETS:
        word_to_positions[w] = list(p.positions)

missing = TARGETS - set(word_to_positions.keys())
if missing:
    st.warning(
        f"Faltan placements en crossword.py para: {', '.join(sorted(missing))}. "
        "Asegúrate de que build_puzzle() incluya esas palabras."
    )

# Session state
if "selected" not in st.session_state:
    st.session_state.selected = []  # lista de (r,c)

if "found" not in st.session_state:
    st.session_state.found = set()

def selected_string():
    return "".join(grid[r][c] for (r, c) in st.session_state.selected)

def matches_word(selection, target_positions):
    return selection == target_positions or selection == list(reversed(target_positions))

def found_cells_set():
    cells = set()
    for w in st.session_state.found:
        for pos in word_to_positions.get(w, []):
            cells.add(tuple(pos))
    return cells

def confirm_selection():
    sel = st.session_state.selected
    if not sel:
        st.warning("Selecciona letras primero 🙂")
        return

    for w in sorted(TARGETS):
        if w in st.session_state.found:
            continue
        pos = word_to_positions.get(w)
        if pos and matches_word(sel, pos):
            st.session_state.found.add(w)
            st.session_state.selected = []
            st.success(f"✅ Encontraste: {w}")
            return

    st.error("❌ Esa selección no corresponde. Intenta otra 🙂")

# ====== Estado arriba ======
found_list = sorted(st.session_state.found)
remaining = sorted(TARGETS - st.session_state.found)

st.markdown(
    f"""
    <span class="pill">✅ Encontradas: {(" / ".join(found_list) if found_list else "—")}</span>
    <span class="pill">🔎 Faltan: {(" / ".join(remaining) if remaining else "—")}</span>
    """,
    unsafe_allow_html=True,
)
st.write("**Selección actual:**", selected_string() if st.session_state.selected else "—")

# ====== Controles (texto corto para que no se parta) ======
c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
with c1:
    if st.button("✔️ Confirmar", use_container_width=True):
        confirm_selection()
with c2:
    if st.button("↩️ Deshacer", use_container_width=True):
        if st.session_state.selected:
            st.session_state.selected.pop()
            st.rerun()
with c3:
    if st.button("🧼 Limpiar", use_container_width=True):
        st.session_state.selected = []
        st.rerun()
with c4:
    if st.button("🔄 Nuevo", use_container_width=True):
        # Genera un nuevo tablero solo si tú lo pides
        grid2, _, placements2 = build_puzzle()
        st.session_state.puzzle = {"grid": grid2, "placements": placements2}
        st.session_state.selected = []
        st.session_state.found = set()
        st.rerun()

# ====== Tablero ======
st.subheader("🧠 Tablero (toca letras para seleccionar)")

found_cells = found_cells_set()
selected_cells = set(st.session_state.selected)

for r in range(SIZE):
    cols = st.columns(SIZE, gap="small")
    for c in range(SIZE):
        letter = grid[r][c]
        is_found = (r, c) in found_cells
        is_sel = (r, c) in selected_cells

        # etiquetas visuales
        if is_found:
            label = f"✅{letter}"
        elif is_sel:
            label = f"🔸{letter}"
        else:
            label = letter

        if cols[c].button(
            label,
            key=f"cellbtn_{r}_{c}",
            disabled=is_found,
            use_container_width=True,
        ):
            if (r, c) not in selected_cells:
                st.session_state.selected.append((r, c))
            st.rerun()

# ====== Final ======
if TARGETS.issubset(st.session_state.found):
    st.balloons()
    st.success("💛 ¡Ganaste!")

    st.markdown("## Jazmín…")
    st.markdown("### Perdón.")
    st.markdown("### Te amo.")

    # Mostrar imagen final
    img = Image.open("perdon.png")
    st.image(
        img,
        caption="",
        use_container_width=True
    )
