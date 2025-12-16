import streamlit as st
from crossword import build_puzzle

st.set_page_config(page_title="Para Jazmín 💛", page_icon="🧩", layout="centered")

# 🎵 Música de fondo (Coldplay – Trouble)
# Nota: en algunos navegadores el autoplay puede estar bloqueado hasta que el usuario interactúe.
st.markdown(
    """
    <iframe width="0" height="0"
    src="https://www.youtube.com/embed/LLFokwpQfHQ?autoplay=1&loop=1&playlist=LLFokwpQfHQ"
    frameborder="0"
    allow="autoplay">
    </iframe>
    """,
    unsafe_allow_html=True,
)

st.title("🧩 Un pequeño juego para decirte algo")
st.write("Completa las palabras usando las pistas. 💛")

grid, _, placements = build_puzzle()
SIZE = len(grid)

# Estado de la grilla (lo que escribe el usuario)
if "entries" not in st.session_state:
    st.session_state.entries = [["" for _ in range(SIZE)] for _ in range(SIZE)]

with st.expander("📌 Pistas", expanded=True):
    for p in placements:
        st.write(p.clue)

st.subheader("🧠 Tablero")

# Render del tablero como inputs
for r in range(SIZE):
    cols = st.columns(SIZE, gap="small")
    for c in range(SIZE):
        key = f"cell_{r}_{c}"
        current = st.session_state.entries[r][c]
        val = cols[c].text_input(
            label="",
            value=current,
            max_chars=1,
            key=key,
            label_visibility="collapsed",
        )
        st.session_state.entries[r][c] = (val or "").strip().upper()[:1]

def check_solution() -> bool:
    # Solo verificamos las casillas que pertenecen a las palabras objetivo
    for p in placements:
        for (r, c), ch in zip(p.positions, p.word):
            user = (st.session_state.entries[r][c] or "").strip().upper()
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
        st.session_state.entries = [["" for _ in range(SIZE)] for _ in range(SIZE)]
        st.rerun()

with col3:
    if st.button("👀 Mostrar solución", use_container_width=True):
        # Rellena SOLO las posiciones de las palabras (no toda la sopa)
        for p in placements:
            for (r, c), ch in zip(p.positions, p.word):
                st.session_state.entries[r][c] = ch
        st.rerun()

st.divider()
st.caption("Tip: escribe una letra por casilla (en MAYÚSCULAS).")
