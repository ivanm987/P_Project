import streamlit as st
from crossword import build_puzzle, is_cell_playable, solution_letter_at

st.set_page_config(page_title="Crucigrama: ¿Me perdonas?", page_icon="🧩", layout="centered")

grid, is_block, placements = build_puzzle()
SIZE = len(grid)

st.title("🧩 Crucigrama")
st.write("Completa las palabras. **Sin excusas, con cariño.**")

with st.expander("📌 Pistas", expanded=True):
    for p in placements:
        st.markdown(f"- **{p.clue}**")

# Session state for user entries
if "entries" not in st.session_state:
    st.session_state.entries = [["" for _ in range(SIZE)] for _ in range(SIZE)]

def normalize(ch: str) -> str:
    ch = (ch or "").strip().upper()
    return ch[:1]  # single letter

# Render the grid as inputs
st.subheader("🧠 Tablero")
for r in range(SIZE):
    cols = st.columns(SIZE, gap="small")
    for c in range(SIZE):
        if not is_cell_playable(is_block, r, c):
            cols[c].markdown(
                "<div style='height:42px; background:#111827; border-radius:8px;'></div>",
                unsafe_allow_html=True
            )
        else:
            key = f"cell_{r}_{c}"
            current = st.session_state.entries[r][c]
            val = cols[c].text_input(
                label="",
                value=current,
                key=key,
                max_chars=1,
                placeholder="",
                label_visibility="collapsed",
            )
            st.session_state.entries[r][c] = normalize(val)

def check_solution() -> bool:
    for r in range(SIZE):
        for c in range(SIZE):
            if is_cell_playable(is_block, r, c):
                target = solution_letter_at(grid, r, c).strip().upper()
                user = (st.session_state.entries[r][c] or "").strip().upper()
                if target == "":
                    continue
                if user != target:
                    return False
    return True

colA, colB, colC = st.columns([1, 1, 1])
with colA:
    if st.button("✅ Verificar", use_container_width=True):
        if check_solution():
            st.success("¡LO LOGRASTE! 💛")
            st.balloons()
            st.markdown("### Jazmín… ¿me perdonas? 🥺")
        else:
            st.warning("Casi… revisa las letras 😉")

with colB:
    if st.button("🧼 Limpiar", use_container_width=True):
        st.session_state.entries = [["" for _ in range(SIZE)] for _ in range(SIZE)]
        st.rerun()

with colC:
    if st.button("👀 Mostrar solución", use_container_width=True):
        for r in range(SIZE):
            for c in range(SIZE):
                if is_cell_playable(is_block, r, c):
                    st.session_state.entries[r][c] = solution_letter_at(grid, r, c).strip().upper()
        st.rerun()

st.divider()
st.caption("Tip: en la pista vertical, escribe **MEPERDONAS** (sin espacio).")
