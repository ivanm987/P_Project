import streamlit as st
from crossword import build_puzzle

st.set_page_config(page_title="Para Jazmín 💛", page_icon="🧩", layout="centered")

# ====== Estilos para que los botones parezcan casillas ======
st.markdown(
    """
    <style>
      div[data-testid="stHorizontalBlock"] { gap: 0.35rem; }
      button[kind="secondary"] {
        width: 40px !important;
        height: 40px !important;
        padding: 0 !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
      }
      .legend-pill {
        display:inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.10);
        margin-right: 8px;
        font-size: 0.9rem;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🧩 Sopa de letras")
st.write("Encuentra y **selecciona** las palabras: **JAZMIN**, **PERDON**, **TEAMO**.")

# 🎵 Música (visible, porque autoplay con sonido suele bloquearse)
st.markdown("### 🎵 Música (toca ▶️ para reproducir)")
st.markdown(
    """
    <iframe width="380" height="215"
    src="https://www.youtube.com/embed/LLFokwpQfHQ?controls=1&rel=0"
    title="Coldplay - Trouble"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen>
    </iframe>
    """,
    unsafe_allow_html=True,
)

# ====== Construye puzzle ======
grid, _, placements = build_puzzle()
SIZE = len(grid)

# Nos quedamos SOLO con estas palabras objetivo
TARGETS = {"JAZMIN", "PERDON", "TEAMO"}

# Normaliza placements a un diccionario word -> positions
word_to_positions = {}
for p in placements:
    w = (p.word or "").strip().upper()
    if w in TARGETS:
        word_to_positions[w] = list(p.positions)

missing = TARGETS - set(word_to_positions.keys())
if missing:
    st.warning(
        f"Tu crossword.py no está colocando estas palabras aún: {', '.join(sorted(missing))}. "
        "Asegúrate de que build_puzzle() incluya placements para esas palabras."
    )

# ====== Session state ======
if "selected" not in st.session_state:
    st.session_state.selected = []  # lista de (r,c) en orden de selección

if "found" not in st.session_state:
    st.session_state.found = set()  # palabras encontradas

def selected_string():
    return "".join(grid[r][c] for (r, c) in st.session_state.selected)

def selected_coords_set():
    return set(st.session_state.selected)

def found_cells_set():
    cells = set()
    for w in st.session_state.found:
        for pos in word_to_positions.get(w, []):
            cells.add(tuple(pos))
    return cells

def matches_word(selection, target_positions):
    """Acepta selección exacta o invertida."""
    if not selection or not target_positions:
        return False
    return selection == target_positions or selection == list(reversed(target_positions))

def confirm_selection():
    sel = st.session_state.selected
    if not sel:
        st.warning("Selecciona letras primero 🙂")
        return

    # Verifica contra cada target (solo si aún no fue encontrado)
    for w in sorted(TARGETS):
        if w in st.session_state.found:
            continue
        pos = word_to_positions.get(w)
        if pos and matches_word(sel, pos):
            st.session_state.found.add(w)
            st.session_state.selected = []
            st.success(f"✅ Encontraste: {w}")
            return

    st.error("❌ Esa selección no corresponde a una palabra objetivo. Intenta otra 🙂")

# ====== Barra de estado ======
found_list = sorted(list(st.session_state.found))
remaining = sorted(list(TARGETS - st.session_state.found))

st.markdown(
    f"""
    <span class="legend-pill">✅ Encontradas: {(" / ".join(found_list) if found_list else "—")}</span>
    <span class="legend-pill">🔎 Faltan: {(" / ".join(remaining) if remaining else "—")}</span>
    """,
    unsafe_allow_html=True,
)

st.write("**Selección actual:**", selected_string() if st.session_state.selected else "—")

# ====== Controles ======
c1, c2, c3 = st.columns([1, 1, 1])

with c1:
    if st.button("✔️ Confirmar selección", use_container_width=True):
        confirm_selection()

with c2:
    if st.button("↩️ Deshacer último", use_container_width=True):
        if st.session_state.selected:
            st.session_state.selected.pop()
            st.rerun()

with c3:
    if st.button("🧼 Limpiar selección", use_container_width=True):
        st.session_state.selected = []
        st.rerun()

# ====== Render tablero como botones ======
st.subheader("🧠 Tablero (toca letras para seleccionar)")

found_cells = found_cells_set()
selected_cells = selected_coords_set()

for r in range(SIZE):
    cols = st.columns(SIZE, gap="small")
    for c in range(SIZE):
        letter = grid[r][c]

        is_found = (r, c) in found_cells
        is_sel = (r, c) in selected_cells

        # Señal visual: si está seleccionado o encontrado
        if is_found:
            label = f"✅{letter}"
        elif is_sel:
            label = f"🔸{letter}"
        else:
            label = letter

        if cols[c].button(
            label,
            key=f"cellbtn_{r}_{c}",
            use_container_width=True,
            disabled=is_found,  # si ya es parte de una palabra encontrada, se bloquea
        ):
            # Evita seleccionar la misma celda dos veces
            if (r, c) not in selected_cells:
                st.session_state.selected.append((r, c))
            st.rerun()

# ====== Final ======
if TARGETS.issubset(st.session_state.found):
    st.balloons()
    st.success("💛 ¡Ganaste! Encontraste todo.")
    st.markdown("## Jazmín…\n### perdón.\n### te amo.")

