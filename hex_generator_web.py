import streamlit as st
import struct


# --- Вспомогательные функции ---
def float_to_hex(f):
    return struct.pack('<f', f).hex()


def hex_to_float(hex_str):
    try:
        return round(struct.unpack('<f', bytes.fromhex(hex_str))[0], 6)
    except:
        return 0.0


# --- Все строки из оригинального сообщения ---
original_hex_lines = [
    # Sharp very low
    "0000e0401d8fc2753d",
    "250000803f2d0000803f0a140d",
    "cdcc44401d0ad7233d",
    "250000803f2d0000803f0a140d",
    "0000f03f1d68916d3d",
    "250000803f2d0000803f12050d0000a03f0a490a140d",

    # Sharp low
    "9a9909411d8fc2753d",
    "250000803f2d0000803f0a140d",
    "f6286c401d0ad7233d",
    "250000803f2d0000803f0a140d",
    "000010401d68916d3d",
    "250000803f2d0000803f12050d000020400a490a140d",

    # Sharp med
    "000020411d8fc2753d",
    "250000803f2d0000803f0a140d",
    "333387401d0ad7233d",
    "250000803f2d0000803f0a140d",
    "000020401d68916d3d",
    "250000803f2d0000803f12050d0000a0400a490a140d",

    # Sharp high
    "000020411d022b873d",
    "250000803f2d0000803f0a140d",
    "14ae77401d0ad7233d",
    "250000803f2d0000803f0a140d",
    "0ad793401d3480b73c",
    "250000803f2d0000803f12050d000020410a490a140d",

    # Sharp very high
    "cdcc34411dea95323d",
    "250000803f2d0000803f0a140d",
    "cdcc6c401d6f12033d",
    "250000803f2d0000803f0a140d",
    "333303401ded0dbe3c",
    "250000803f2d0000803f12050d0000a0410a490a140d",

    # Sharp bento low
    "000080411d77be9f3c",
    "250000803f2d0000803f0a140d",
    "666646401dc1caa13c",
    "250000803f2d0000803f0a140d",
    "85ebf13f1d0ad7a33c",
    "250000803f2d0000803f12050d000020420a490a140d",

    # Sharp bento high
    "000094411d728a8e3c",
    "250000803f2d0000803f0a140d",
    "cdcc2c401dbe30993c",
    "250000803f2d0000803f0a140d",
    "9a99d93f1d0ad7a33c",
    "250000803f2d0000803f12050d0000a042000000"
]


# --- Индексы для двух групп ---
level_slices_main = {
    "Sharp very low": (0, 6),
    "Sharp low": (6, 12),
    "Sharp med": (12, 18),
    "Sharp high": (18, 24),
    "Sharp very high": (24, 30),
}

level_slices_bento = {
    "Sharp bento low": (30, 36),
    "Sharp bento high": (36, 42)
}


# --- Все уровни резкости ---
all_sharp_levels = [
    {"name": "Sharp very low",  "default": [7.0, 0.060, 3.075, 0.040, 1.875, 0.058]},
    {"name": "Sharp low",       "default": [8.6, 0.060, 3.69, 0.040, 2.25, 0.058]},
    {"name": "Sharp med",       "default": [10.0, 0.060, 4.225, 0.040, 2.5, 0.058]},
    {"name": "Sharp high",      "default": [10.0, 0.066, 3.87, 0.040, 4.62, 0.0224]},
    {"name": "Sharp very high", "default": [11.3, 0.0436, 3.70, 0.032, 2.05, 0.0232]},
    {"name": "Sharp bento low", "default": [16.0, 0.0195, 3.10, 0.01975, 1.89, 0.02]},
    {"name": "Sharp bento high","default": [18.5, 0.0174, 2.70, 0.0187, 1.70, 0.02]}
]

main_levels = all_sharp_levels[:5]
bento_levels = all_sharp_levels[5:]
all_levels = all_sharp_levels.copy()


# --- Функция генерации HEX ---
def generate_hex(values_list, level_names, level_slices, start_header=True):
    lines = []

    for i, values in enumerate(values_list):
        l1, l1a, l2, l2a, l3, l3a = values
        name = level_names[i]["name"]
        if name in level_slices:
            start, end = level_slices[name]
        else:
            continue

        modified_block = original_hex_lines[start:end]
        modified_block[0] = f"{float_to_hex(l1)}1d{float_to_hex(l1a)}"
        modified_block[2] = f"{float_to_hex(l2)}1d{float_to_hex(l2a)}"
        modified_block[4] = f"{float_to_hex(l3)}1d{float_to_hex(l3a)}"

        lines.extend(modified_block)

    full_hex = "".join(lines)
    if start_header:
        full_hex = "0a490a140d" + full_hex
    return full_hex


# --- Парсеры ---
def parse_full_hex(hex_string):
    hex_string = hex_string.strip()
    if hex_string.startswith("0a490a140d"):
        hex_string = hex_string[10:]
    parsed = []
    idx = 0
    for level in main_levels + bento_levels:
        name = level["name"]
        if name in level_slices_main:
            start, end = level_slices_main[name]
        elif name in level_slices_bento:
            start, end = level_slices_bento[name]
        else:
            continue

        block_size = end - start
        block_data = []

        for i in range(block_size):
            line = hex_string[i*16:i*16+16]
            if not line:
                break

            parts = line.split("1d")
            if len(parts) == 2:
                l = hex_to_float(parts[0])
                la = hex_to_float(parts[1][:8])
                block_data.append((l, la))
            else:
                block_data.append((0.0, 0.0))

        if len(block_data) >= 3:
            parsed.append([
                block_data[0][0], block_data[0][1],
                block_data[1][0], block_data[1][1],
                block_data[2][0], block_data[2][1]
            ])
        else:
            parsed.append([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    return parsed


def parse_sharp_only(hex_string):
    hex_string = hex_string.strip()
    if hex_string.startswith("0a490a140d"):
        hex_string = hex_string[10:]

    parsed = []
    for level in main_levels:
        name = level["name"]
        start, end = level_slices_main[name]
        block_data = []

        for i in range(start, end):
            line = hex_string[i*16:i*16+16]
            if not line:
                break

            parts = line.split("1d")
            if len(parts) == 2:
                l = hex_to_float(parts[0])
                la = hex_to_float(parts[1][:8])
                block_data.append((l, la))
            else:
                block_data.append((0.0, 0.0))

        if len(block_data) >= 3:
            parsed.append([
                block_data[0][0], block_data[0][1],
                block_data[1][0], block_data[1][1],
                block_data[2][0], block_data[2][1]
            ])
        else:
            parsed.append([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    return parsed


def parse_bento_only(hex_string):
    hex_string = hex_string.strip()
    parsed = []
    for level in bento_levels:
        name = level["name"]
        start, end = level_slices_bento[name]
        block_data = []

        for i in range(start, end):
            line = hex_string[i*16:i*16+16]
            if not line:
                break

            parts = line.split("1d")
            if len(parts) == 2:
                l = hex_to_float(parts[0])
                la = hex_to_float(parts[1][:8])
                block_data.append((l, la))
            else:
                block_data.append((0.0, 0.0))

        if len(block_data) >= 3:
            parsed.append([
                block_data[0][0], block_data[0][1],
                block_data[1][0], block_data[1][1],
                block_data[2][0], block_data[2][1]
            ])
        else:
            parsed.append([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    return parsed


# --- Интерфейс ---
st.set_page_config(page_title="HEX Sharp Config Generator", layout="wide")
st.title("🔧 Sharp Level HEX Code Generator + Парсер")

tab1, tab2 = st.tabs(["🛠️ Генератор", "📄 Парсер"])


# --- ГЕНЕРАТОР ---
with tab1:
    st.markdown("### 🧱 Генератор 1: Основные уровни резкости")

    main_inputs = []
    for idx, level in enumerate(main_levels):
        with st.expander(level["name"], expanded=True):
            cols = st.columns(3)
            l1 = cols[0].number_input("L1", value=level["default"][0], format="%.4f", key=f"main_l1_{idx}")
            l1a = cols[1].number_input("L1A", value=level["default"][1], format="%.4f", key=f"main_l1a_{idx}")
            l2 = cols[0].number_input("L2", value=level["default"][2], format="%.4f", key=f"main_l2_{idx}")
            l2a = cols[1].number_input("L2A", value=level["default"][3], format="%.4f", key=f"main_l2a_{idx}")
            l3 = cols[0].number_input("L3", value=level["default"][4], format="%.4f", key=f"main_l3_{idx}")
            l3a = cols[1].number_input("L3A", value=level["default"][5], format="%.4f", key=f"main_l3a_{idx}")
            main_inputs.append([l1, l1a, l2, l2a, l3, l3a])

    if st.button("🚀 Сгенерировать основной HEX"):
        full_hex = generate_hex(main_inputs, main_levels, level_slices_main, start_header=True)
        st.text_area("Сгенерированный HEX (основные уровни):", value=full_hex, height=300)
        st.download_button(label="⬇️ main_output.hex", data=full_hex, file_name="main_output.hex")


    st.markdown("### 🍜 Генератор 2: Уровни Bento")

    bento_inputs = []
    for idx, level in enumerate(bento_levels):
        with st.expander(level["name"], expanded=True):
            cols = st.columns(3)
            l1 = cols[0].number_input("L1", value=level["default"][0], format="%.4f", key=f"bento_l1_{idx}")
            l1a = cols[1].number_input("L1A", value=level["default"][1], format="%.4f", key=f"bento_l1a_{idx}")
            l2 = cols[0].number_input("L2", value=level["default"][2], format="%.4f", key=f"bento_l2_{idx}")
            l2a = cols[1].number_input("L2A", value=level["default"][3], format="%.4f", key=f"bento_l2a_{idx}")
            l3 = cols[0].number_input("L3", value=level["default"][4], format="%.4f", key=f"bento_l3_{idx}")
            l3a = cols[1].number_input("L3A", value=level["default"][5], format="%.4f", key=f"bento_l3a_{idx}")
            bento_inputs.append([l1, l1a, l2, l2a, l3, l3a])

    if st.button("🚀 Сгенерировать Bento HEX"):
        full_hex = generate_hex(bento_inputs, bento_levels, level_slices_bento, start_header=False)
        st.text_area("Сгенерированный HEX (Bento):", value=full_hex, height=300)
        st.download_button(label="⬇️ bento_output.hex", data=full_hex, file_name="bento_output.hex")


# --- ПАРСЕР ---
with tab2:
    st.markdown("### 🔍 1. Полный парсер (все уровни)")
    full_hex_input = st.text_area("Введите полный HEX:", key="full_parser", height=200)
    if st.button("🔍 Распарсить полный HEX"):
        parsed = parse_full_hex(full_hex_input)
        st.session_state.parsed_full = parsed

    if "parsed_full" in st.session_state:
        inputs = st.session_state.parsed_full
        edited_inputs = []
        for idx, level in enumerate(all_levels):
            with st.expander(level["name"], expanded=True):
                cols = st.columns(3)
                l1 = cols[0].number_input("L1", value=inputs[idx][0], format="%.4f", key=f"full_l1_{idx}")
                l1a = cols[1].number_input("L1A", value=inputs[idx][1], format="%.4f", key=f"full_l1a_{idx}")
                l2 = cols[0].number_input("L2", value=inputs[idx][2], format="%.4f", key=f"full_l2_{idx}")
                l2a = cols[1].number_input("L2A", value=inputs[idx][3], format="%.4f", key=f"full_l2a_{idx}")
                l3 = cols[0].number_input("L3", value=inputs[idx][4], format="%.4f", key=f"full_l3_{idx}")
                l3a = cols[1].number_input("L3A", value=inputs[idx][5], format="%.4f", key=f"full_l3a_{idx}")
                edited_inputs.append([l1, l1a, l2, l2a, l3, l3a])

        if st.button("💾 Сохранить как полный HEX"):
            full_hex = generate_hex(edited_inputs, all_levels, {**level_slices_main, **level_slices_bento}, start_header=True)
            st.text_area("Обновлённый HEX:", value=full_hex, height=300)
            st.download_button(label="⬇️ Скачать updated_full.hex", data=full_hex, file_name="updated_full.hex")


    st.markdown("---")
    st.markdown("### 🔎 2. Парсер только Sharp-уровней")
    sharp_hex_input = st.text_area("Введите HEX только для Sharp-уровней:", key="sharp_parser", height=200)
    if st.button("🔍 Распарсить Sharp HEX"):
        parsed = parse_sharp_only(sharp_hex_input)
        st.session_state.parsed_sharp = parsed

    if "parsed_sharp" in st.session_state:
        inputs = st.session_state.parsed_sharp
        edited_inputs = []
        for idx, level in enumerate(main_levels):
            with st.expander(level["name"], expanded=True):
                cols = st.columns(3)
                l1 = cols[0].number_input("L1", value=inputs[idx][0], format="%.4f", key=f"sharp_l1_{idx}")
                l1a = cols[1].number_input("L1A", value=inputs[idx][1], format="%.4f", key=f"sharp_l1a_{idx}")
                l2 = cols[0].number_input("L2", value=inputs[idx][2], format="%.4f", key=f"sharp_l2_{idx}")
                l2a = cols[1].number_input("L2A", value=inputs[idx][3], format="%.4f", key=f"sharp_l2a_{idx}")
                l3 = cols[0].number_input("L3", value=inputs[idx][4], format="%.4f", key=f"sharp_l3_{idx}")
                l3a = cols[1].number_input("L3A", value=inputs[idx][5], format="%.4f", key=f"sharp_l3a_{idx}")
                edited_inputs.append([l1, l1a, l2, l2a, l3, l3a])

        if st.button("💾 Сохранить как Sharp HEX"):
            full_hex = generate_hex(edited_inputs, main_levels, level_slices_main, start_header=True)
            st.text_area("Обновлённый HEX (Sharp):", value=full_hex, height=300)
            st.download_button(label="⬇️ sharp_updated.hex", data=full_hex, file_name="sharp_updated.hex")


    st.markdown("---")
    st.markdown("### 🔍 3. Парсер только Bento-уровней")
    bento_hex_input = st.text_area("Введите HEX только для Bento-уровней:", key="bento_parser", height=200)
    if st.button("🔍 Распарсить Bento HEX"):
        parsed = parse_bento_only(bento_hex_input)
        st.session_state.parsed_bento = parsed

    if "parsed_bento" in st.session_state:
        inputs = st.session_state.parsed_bento
        edited_inputs = []
        for idx, level in enumerate(bento_levels):
            with st.expander(level["name"], expanded=True):
                cols = st.columns(3)
                l1 = cols[0].number_input("L1", value=inputs[idx][0], format="%.4f", key=f"bento_l1_{idx}")
                l1a = cols[1].number_input("L1A", value=inputs[idx][1], format="%.4f", key=f"bento_l1a_{idx}")
                l2 = cols[0].number_input("L2", value=inputs[idx][2], format="%.4f", key=f"bento_l2_{idx}")
                l2a = cols[1].number_input("L2A", value=inputs[idx][3], format="%.4f", key=f"bento_l2a_{idx}")
                l3 = cols[0].number_input("L3", value=inputs[idx][4], format="%.4f", key=f"bento_l3_{idx}")
                l3a = cols[1].number_input("L3A", value=inputs[idx][5], format="%.4f", key=f"bento_l3a_{idx}")
                edited_inputs.append([l1, l1a, l2, l2a, l3, l3a])

        if st.button("💾 Сохранить как Bento HEX"):
            full_hex = generate_hex(edited_inputs, bento_levels, level_slices_bento, start_header=False)
            st.text_area("Обновлённый HEX (Bento):", value=full_hex, height=300)
            st.download_button(label="⬇️ bento_updated.hex", data=full_hex, file_name="bento_updated.hex")
