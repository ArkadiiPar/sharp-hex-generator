import streamlit as st
import struct


# --- Вспомогательные функции ---
def float_to_hex(f):
    return struct.pack('<f', f).hex()


# --- Все строки из оригинального сообщения ---
original_hex_lines = [
    "0a490a140d",  # Sharp very low
    "0000e0401d8fc2753d",
    "250000803f2d0000803f0a140d",
    "cdcc44401d0ad7233d",
    "250000803f2d0000803f0a140d",
    "0000f03f1d68916d3d",
    "250000803f2d0000803f12050d0000a03f0a490a140d",

    "0a490a140d",  # Sharp low
    "9a9909411d8fc2753d",
    "250000803f2d0000803f0a140d",
    "f6286c401d0ad7233d",
    "250000803f2d0000803f0a140d",
    "000010401d68916d3d",
    "250000803f2d0000803f12050d000020400a490a140d",

    "0a490a140d",  # Sharp med
    "000020411d8fc2753d",
    "250000803f2d0000803f0a140d",
    "333387401d0ad7233d",
    "250000803f2d0000803f0a140d",
    "000020401d68916d3d",
    "250000803f2d0000803f12050d0000a0400a490a140d",

    "0a490a140d",  # Sharp high
    "000020411d022b873d",
    "250000803f2d0000803f0a140d",
    "14ae77401d0ad7233d",
    "250000803f2d0000803f0a140d",
    "0ad793401d3480b73c",
    "250000803f2d0000803f12050d000020410a490a140d",

    "0a490a140d",  # Sharp very high
    "cdcc34411dea95323d",
    "250000803f2d0000803f0a140d",
    "cdcc6c401d6f12033d",
    "250000803f2d0000803f0a140d",
    "333303401ded0dbe3c",
    "250000803f2d0000803f12050d0000a0410a490a140d",

    "0a490a140d",  # Sharp bento low
    "000080411d77be9f3c",
    "250000803f2d0000803f0a140d",
    "666646401dc1caa13c",
    "250000803f2d0000803f0a140d",
    "85ebf13f1d0ad7a33c",
    "250000803f2d0000803f12050d000020420a490a140d",

    "0a490a140d",  # Sharp bento high
    "000094411d728a8e3c",
    "250000803f2d0000803f0a140d",
    "cdcc2c401dbe30993c",
    "250000803f2d0000803f0a140d",
    "9a99d93f1d0ad7a33c",
    "250000803f2d0000803f12050d0000a042000000"
]

# --- Индексы начала и конца для каждого уровня ---
level_slices = {
    "Sharp very low": (0, 7),
    "Sharp low": (7, 14),
    "Sharp med": (14, 21),
    "Sharp high": (21, 28),
    "Sharp very high": (28, 35),
    "Sharp bento low": (35, 42),
    "Sharp bento high": (42, 49)
}

# --- Значения по умолчанию ---

sharp_levels = [
    {"name": "Sharp very low",  "default": [7.0, 0.060, 3.075, 0.040, 1.875, 0.058]},
    {"name": "Sharp low",       "default": [8.6, 0.060, 3.69, 0.040, 2.25, 0.058]},
    {"name": "Sharp med",       "default": [10.0, 0.060, 4.225, 0.040, 2.5, 0.058]},
    {"name": "Sharp high",      "default": [10.0, 0.066, 3.87, 0.040, 4.62, 0.0224]},
    {"name": "Sharp very high", "default": [11.3, 0.0436, 3.70, 0.032, 2.05, 0.0232]},
    {"name": "Sharp bento low", "default": [16.0, 0.0195, 3.10, 0.01975, 1.89, 0.02]},
    {"name": "Sharp bento high","default": [18.5, 0.0174, 2.70, 0.0187, 1.70, 0.02]}
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
    lines = []

    for i, values in enumerate(all_inputs):
        l1, l1a, l2, l2a, l3, l3a = values

        start, end = level_slices[sharp_levels[i]["name"]]

        modified_block = original_hex_lines[start:end]
        modified_block[1] = f"{float_to_hex(l1)}1d{float_to_hex(l1a)}"
        modified_block[3] = f"{float_to_hex(l2)}1d{float_to_hex(l2a)}"
        modified_block[5] = f"{float_to_hex(l3)}1d{float_to_hex(l3a)}"

        lines.extend(modified_block)

    full_hex = '\n'.join(lines)

    st.text_area("Сгенерированный HEX-код:", value=full_hex, height=400)

    st.download_button(
        label="⬇️ Скачать как .hex файл",
        data=full_hex,
        file_name="generated_output.hex",
        mime="text/plain"
    )
