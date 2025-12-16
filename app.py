import streamlit as st
from crossword import build_puzzle

st.set_page_config(page_title="Para Jazmín 💛", page_icon="🧩", layout="centered")

st.title("🧩 Un pequeño juego para decirte algo")
st.write("Completa las palabras usando las pistas. 💛")

# 🎵 Música (YouTube) - autoplay con sonido suele bloquearse; por eso lo dejamos con controles.
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

grid, _, placements = build_puzzle()
SIZE = len(grid)

# Conjunto de casillas "jugables" (solo donde van las palabras)
playable = set()
for p in placements:
    for pos in p.positions:
        playable.add(pos)

# Estado: lo que escribe el usuario
if "entries" not in st.session_state:
    # Inicializa con vacío para jugables y con la letra random (solución) para no-jugables
    st.session_state.entries = [["" for _ in range(SIZE)] for _ in range(SIZE)]
    for r in range(SIZE):
        for c in range(SIZE):
            if (r, c) not in playable:
                st.session_state.entries[r][c] = grid[r][c]  # letras random bloqueadas

with st.expander("📌 Pistas", expanded=True):
    for p in placements:
        st.write(p.clue)

st.subheader("🧠 Tablero")

# Render del tablero
for r in range(SIZE):
    cols = st.columns(SIZE, gap="small")
    for c in range(SIZE):
        key = f"cell_{r}_{c}"

        if (r, c) in playable:
            # Editable: el usuario completa estas letras
            current = st.session_state.entries[r][c]
            val = cols[c].text_input(
                label="",
                value=current,
                max_chars=1,
                key=key,
                label_visibility="collapsed",
                placeholder="",
            )
            st.session_state.entries[r][c] = (val or "").strip().upper()[:1]
        else:
            # No editable: se muestran letras aleatorias (relleno)
            cols[c].text_input(
                label="",
                value=st.session_state.entries[r][c],
                key=key,
                max_chars=1,
                disabled=True,
                label_visibility="collapsed",
            )

def check_solution() -> bool:
    # Verifica solo posiciones de las palabras
    for p in placements:
        for (rr, cc), ch in zip(p.positions, p.word):
            user = (st.session_state.entries[rr][cc] or "").strip().upper()
            if user != ch:
                return False
    return True

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("💛 Verificar", use_container_width=True):
        if check_solution():
            st.balloons()  # “confeti” nativo en Streamlit
            st.success("¡Lo lograste! 💛")
            st.markdown("## Jazmín…\n### perdón.\n### te amo.")
        else:
            st.warning("Aún no… revisa las letras 😉")

with col2:
    if st.button("🧼 Limpiar", use_container_width=True):
        # Limpia solo las casillas jugables
        for (rr, cc) in playable:
            st.session_state.entries[rr][cc] = ""
        st.rerun()

with col3:
    if st.button("👀 Mostrar solución", use_container_width=True):
        for p in placements:
            for (rr, cc), ch in zip(p.positions, p.word):
                st.session_state.entries[rr][cc] = ch
        st.rerun()

st.divider()
st.caption("Tip: solo puedes editar las casillas que forman las palabras. Las demás son letras aleatorias de relleno.")
