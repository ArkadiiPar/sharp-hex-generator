import streamlit as st
import struct


# --- Вспомогательные функции ---
def float_to_hex(f):
    """Конвертирует float в hex-строку little-endian (8 символов)"""
    return struct.pack('<f', f).hex()


# --- Значения по умолчанию и служебные строки ---

sharp_levels = [
    {
        "name": "Sharp very low",
        "default": [7.0, 0.060, 3.075, 0.040, 1.875, 0.058],
        "service_lines": [
            "250000803f2d0000803f0a140d",
            "250000803f2d0000803f0a140d",
            "250000803f2d0000803f12050d0000a03f"
        ]
    },
    {
        "name": "Sharp low",
        "default": [8.6, 0.060, 3.69, 0.040, 2.25, 0.058],
        "service_lines": [
            "250000803f2d0000803f0a140d",
            "250000803f2d0000803f0a140d",
            "250000803f2d0000803f12050d00002040"
        ]
    },
    {
        "name": "Sharp med",
        "default": [10.0, 0.060, 4.225, 0.040, 2.5, 0.058],
        "service_lines": [
            "250000803f2d0000803f0a140d",
            "250000803f2d0000803f0a140d",
            "250000803f2d0000803f12050d0000a040"
        ]
    },
    {
        "name": "Sharp high",
        "default": [10.0, 0.066, 3.87, 0.040, 4.62, 0.0224],
        "service_lines": [
            "250000803f2d0000803f0a140d",
            "250000803f2d0000803f0a140d",
            "250000803f2d0000803f12050d00002041"
        ]
    },
    {
        "name": "Sharp very high",
        "default": [11.3, 0.0436, 3.70, 0.032, 2.05, 0.0232],
        "service_lines": [
            "250000803f2d0000803f0a140d",
            "250000803f2d0000803f0a140d",
            "250000803f2d0000803f12050d0000a041"
        ]
    },
    {
        "name": "Sharp bento low",
        "default": [16.0, 0.0195, 3.10, 0.01975, 1.89, 0.02],
        "service_lines": [
            "250000803f2d0000803f0a140d",
            "250000803f2d0000803f0a140d",
            "250000803f2d0000803f12050d00002042"
        ]
    },
    {
        "name": "Sharp bento high",
        "default": [18.5, 0.0174, 2.70, 0.0187, 1.70, 0.02],
        "service_lines": [
            "250000803f2d0000803f0a140d",
            "250000803f2d0000803f0a140d",
            "250000803f2d0000803f12050d0000a042000000"
        ]
    }
]

# --- Интерфейс ---
st.set_page_config(page_title="HEX Sharp Config Generator", layout="wide")
st.title("🔧 Sharp Level HEX Code Generator")

st.markdown("Измените параметры ниже и получите готовый HEX-код.")

all_inputs = []

for idx, level in enumerate(sharp_levels):
    with st.expander(level["name"], expanded=True):
        cols = st.columns(3)
        l1 = cols[0].number_input("L1", value=level["default"][0], format="%.4f", key=f"{idx}_l1")
        l1a = cols[1].number_input("L1A", value=level["default"][1], format="%.4f", key=f"{idx}_l1a")
        l2 = cols[0].number_input("L2", value=level["default"][2], format="%.4f", key=f"{idx}_l2")
        l2a = cols[1].number_input("L2A", value=level["default"][3], format="%.4f", key=f"{idx}_l2a")
        l3 = cols[0].number_input("L3", value=level["default"][4], format="%.4f", key=f"{idx}_l3")
        l3a = cols[1].number_input("L3A", value=level["default"][5], format="%.4f", key=f"{idx}_l3a")
        all_inputs.append([l1, l1a, l2, l2a, l3, l3a])

if st.button("🚀 Сгенерировать HEX"):
    header = "0a490a140d"
    lines = [header]

    for idx, values in enumerate(all_inputs):
        l1, l1a, l2, l2a, l3, l3a = values
        service_lines = sharp_levels[idx]["service_lines"]

        lines.append(f"{float_to_hex(l1)}1d{float_to_hex(l1a)}")
        lines.append(service_lines[0])
        lines.append(f"{float_to_hex(l2)}1d{float_to_hex(l2a)}")
        lines.append(service_lines[1])
        lines.append(f"{float_to_hex(l3)}1d{float_to_hex(l3a)}")
        lines.append(service_lines[2])

    full_hex = ''.join(lines)  # Без переносов строк
    st.text_area("Сгенерированный HEX-код:", value=full_hex, height=400)

    st.download_button(
        label="⬇️ Скачать как .hex файл",
        data=full_hex,
        file_name="generated_output.hex",
        mime="text/plain"
    )