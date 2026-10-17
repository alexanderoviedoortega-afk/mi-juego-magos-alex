import random
import streamlit as st

st.set_page_config(page_title="Duelo de Magos", page_icon="🔮", layout="centered")

# ESTILO DE LA PÁGINA
st.markdown(
    """
<style>
.stApp {
    background: linear-gradient(135deg, #100d2e, #25134b, #111827);
    color: white;
}
h1, h2, h3, p, label {
    color: white !important;
}
.stButton button {
    width: 100%;
    border-radius: 12px;
    min-height: 48px;
    font-weight: bold;
}
</style>
""",
    unsafe_allow_html=True,
)

# INICIALIZAR EL JUEGO
if "iniciado" not in st.session_state:
    st.session_state.iniciado = False

if "vida_jugador" not in st.session_state:
    st.session_state.vida_jugador = 100
    st.session_state.vida_enemigo = 100
    st.session_state.mago = "1"
    st.session_state.enemigo_lento = False
    st.session_state.aturdido = False
    st.session_state.defendiendo = False
    st.session_state.enemigo_defendiendo = False
    st.session_state.quemadura_turnos = 0
    st.session_state.historial = []
    st.session_state.resultado = ""
    st.session_state.iniciado = False


# REINICIAR LA PARTIDA
def reiniciar():
    st.session_state.vida_jugador = 100
    st.session_state.vida_enemigo = 100
    st.session_state.enemigo_lento = False
    st.session_state.aturdido = False
    st.session_state.defendiendo = False
    st.session_state.enemigo_defendiendo = False
    st.session_state.quemadura_turnos = 0
    st.session_state.historial = []
    st.session_state.resultado = ""
    st.session_state.iniciado = False


# AÑADIR MENSAJES AL HISTORIAL
def mensaje(texto):
    st.session_state.historial.insert(0, texto)


# TURNO DEL ENEMIGO
def turno_enemigo():
    if st.session_state.vida_jugador <= 0 or st.session_state.vida_enemigo <= 0:
        return

    if st.session_state.aturdido:
        mensaje("💫 El mago oscuro está aturdido y pierde su turno.")
        st.session_state.aturdido = False
        return

    accion = random.randint(1, 3)

    if accion == 1:
        dano = random.randint(19, 30)

        if st.session_state.enemigo_lento:
            dano //= 2
            mensaje("❄️ El hielo debilita el ataque enemigo.")
            st.session_state.enemigo_lento = False

        if st.session_state.defendiendo:
            dano //= 2
            mensaje("🛡️ ¡Tu defensa reduce el daño!")
            st.session_state.defendiendo = False

        st.session_state.vida_jugador = max(0, st.session_state.vida_jugador - dano)

        mensaje(f"💀 El mago oscuro te ataca y causa {dano} de daño.")

    elif accion == 2:
        vida_anterior = st.session_state.vida_enemigo

        st.session_state.vida_enemigo = min(100, st.session_state.vida_enemigo + 20)

        curacion = st.session_state.vida_enemigo - vida_anterior

        mensaje(f"💚 El mago oscuro recupera {curacion} puntos de vida.")

    else:
        st.session_state.enemigo_defendiendo = True
        mensaje(
            "🛡️ El mago oscuro crea un escudo. Tu próximo ataque "
            "causará la mitad de daño."
        )


# ACCIÓN DEL JUGADOR
def jugar(accion):
    if st.session_state.resultado:
        return

    if accion == "atacar":
        dano = random.randint(15, 20)

        if st.session_state.enemigo_defendiendo:
            dano //= 2
            st.session_state.enemigo_defendiendo = False
            mensaje("🛡️ El escudo enemigo reduce tu daño.")

        st.session_state.vida_enemigo = max(0, st.session_state.vida_enemigo - dano)

        if st.session_state.mago == "1":
            mensaje(f"❄️ ¡Ráfaga de hielo! Causas {dano} de daño.")

            if st.session_state.vida_enemigo > 0:
                st.session_state.enemigo_lento = True
                mensaje("🧊 El enemigo está ralentizado.")

        elif st.session_state.mago == "2":
            mensaje(f"🔥 ¡Bola de fuego! Causas {dano} de daño.")

            if (
                st.session_state.quemadura_turnos == 0
                and st.session_state.vida_enemigo > 0
            ):
                st.session_state.quemadura_turnos = 3
                mensaje("🔥 ¡El enemigo está en llamas!")

        else:
            mensaje(f"⚡ ¡Rayo eléctrico! Causas {dano} de daño.")

            if st.session_state.vida_enemigo > 0 and random.randint(1, 100) <= 40:
                st.session_state.aturdido = True
                mensaje("⚡ ¡El enemigo ha quedado aturdido!")

    elif accion == "curarse":
        vida_anterior = st.session_state.vida_jugador

        st.session_state.vida_jugador = min(100, st.session_state.vida_jugador + 20)

        curacion = st.session_state.vida_jugador - vida_anterior

        mensaje(f"❤️ Recuperas {curacion} puntos de vida.")

    elif accion == "defenderse":
        st.session_state.defendiendo = True
        mensaje("🛡️ Te preparas para bloquear el ataque.")

    elif accion == "rendirse":
        st.session_state.resultado = "rendicion"
        mensaje("🏳️ Te has rendido. El combate ha terminado.")
        return

    # DAÑO DE QUEMADURA
    if (
        st.session_state.mago == "2"
        and st.session_state.quemadura_turnos > 0
        and st.session_state.vida_enemigo > 0
    ):

        st.session_state.vida_enemigo = max(0, st.session_state.vida_enemigo - 3)

        st.session_state.quemadura_turnos -= 1

        mensaje("🔥 La quemadura causa 3 puntos de daño.")

        if st.session_state.quemadura_turnos > 0 and st.session_state.vida_enemigo > 0:
            mensaje(
                "🔥 Turnos de quemadura restantes: "
                f"{st.session_state.quemadura_turnos}"
            )

    # COMPROBAR SI EL ENEMIGO HA SIDO DERROTADO
    if st.session_state.vida_enemigo <= 0:
        st.session_state.resultado = "victoria"
        return

    # TURNO DEL ENEMIGO
    turno_enemigo()

    if st.session_state.vida_jugador <= 0:
        st.session_state.resultado = "derrota"


# TÍTULO
st.title("🔮⚔️ DUELO DE MAGOS ⚔️🔮")
st.caption("Elige tus poderes y derrota al mago oscuro.")

# ELEGIR MAGO
if not st.session_state.iniciado:
    st.subheader("🔮 Elige tu mago")

    mago = st.radio(
        "Selecciona tu personaje:",
        ["1", "2", "3"],
        format_func=lambda x: {
            "1": "❄️ Mago de hielo",
            "2": "🔥 Mago de fuego",
            "3": "⚡ Mago de rayo",
        }[x],
    )

    st.info(
        {
            "1": "❄️ Hielo: ralentiza el siguiente ataque enemigo.",
            "2": "🔥 Fuego: aplica una quemadura de 3 puntos por turno.",
            "3": "⚡ Rayo: tiene un 40 % de probabilidad de aturdir.",
        }[mago]
    )

    if st.button("⚔️ ¡Comenzar combate!"):
        reiniciar()
        st.session_state.mago = mago
        st.session_state.iniciado = True
        mensaje("💀 ¡El mago oscuro ha aparecido!")
        st.rerun()

# COMBATE
else:
    st.subheader("💀 ¡El mago oscuro ha aparecido!")

    nombre_mago = {
        "1": "❄️ Mago de hielo",
        "2": "🔥 Mago de fuego",
        "3": "⚡ Mago de rayo",
    }[st.session_state.mago]

    st.write(f"Tu personaje: **{nombre_mago}**")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🧙 Tu vida")
        st.progress(st.session_state.vida_jugador / 100)
        st.metric("❤️ HP", st.session_state.vida_jugador)

    with col2:
        st.markdown("### 💀 Enemigo")
        st.progress(st.session_state.vida_enemigo / 100)
        st.metric("💜 HP", st.session_state.vida_enemigo)

    # BOTONES DE ACCIÓN
    if not st.session_state.resultado:
        st.markdown("### ¿Qué quieres hacer?")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🪄 Lanzar ataque", key="atacar"):
                jugar("atacar")
                st.rerun()

            if st.button("🛡️ Defenderse", key="defender"):
                jugar("defenderse")
                st.rerun()

        with col2:
            if st.button("❤️ Curarse", key="curarse"):
                jugar("curarse")
                st.rerun()

            if st.button("🏳️ Rendirse", key="rendirse"):
                jugar("rendirse")
                st.rerun()

    # RESULTADO
    if st.session_state.resultado == "victoria":
        st.success("🏆 ¡VICTORIA! Has derrotado al mago oscuro.")

    elif st.session_state.resultado == "derrota":
        st.error("💀 ¡DERROTA! Te has quedado sin vida.")

    elif st.session_state.resultado == "rendicion":
        st.warning("🏳️ Has abandonado el combate.")

    # HISTORIAL
    st.markdown("### 📜 Historial del combate")

    if st.session_state.historial:
        for evento in st.session_state.historial[:12]:
            st.write(evento)

    # VOLVER A JUGAR
    if st.session_state.resultado:
        if st.button("🔄 Jugar de nuevo"):
            reiniciar()
            st.rerun()
