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


# --- Функция генерации HEX ---
def generate_hex(values_list, level_names, level_slices, start_header=True):
    lines = []

    for i, values in enumerate(values_list):
        l1, l1a, l2, l2a, l3, l3a = values
        name = level_names[i]["name"]
        start, end = level_slices[name]

        modified_block = original_hex_lines[start:end]
        modified_block[0] = f"{float_to_hex(l1)}1d{float_to_hex(l1a)}"
        modified_block[2] = f"{float_to_hex(l2)}1d{float_to_hex(l2a)}"
        modified_block[4] = f"{float_to_hex(l3)}1d{float_to_hex(l3a)}"

        lines.extend(modified_block)

    full_hex = "".join(lines)
    if start_header:
        full_hex = "0a490a140d" + full_hex
    return full_hex


# --- Функция парсинга HEX -> параметры ---
def parse_hex_to_params(hex_input):
    hex_string = hex_input.strip()

    # Убираем заголовок, если есть
    if hex_string.startswith("0a490a140d"):
        hex_string = hex_string[10:]

    parsed_values = []

    idx = 0
    for level in main_levels:
        name = level["name"]
        start, end = level_slices_main[name]
        block_size = end - start
        block_data = []

        for i in range(block_size):
            line_idx = idx * 6 + i * 2  # Lx и LxA находятся на позициях 0, 2, 4 внутри блока
            if line_idx >= len(original_hex_lines): break

            line = hex_string[line_idx*16:(line_idx+1)*16]
            if not line:
                continue

            parts = line.split("1d")
            if len(parts) == 2:
                l = hex_to_float(parts[0])
                la = hex_to_float(parts[1][:8])
                block_data.append((l, la))
            else:
                block_data.append((0.0, 0.0))

        if len(block_data) >= 3:
            parsed_values.append([
                block_data[0][0], block_data[0][1],
                block_data[1][0], block_data[1][1],
                block_data[2][0], block_data[2][1]
            ])
        else:
            parsed_values.append([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

    return parsed_values


# --- Интерфейс ---
st.set_page_config(page_title="HEX Sharp Config Generator", layout="wide")
st.title("🔧 Sharp Level HEX Code Generator (Разделённый + импорт)")

tab1, tab2 = st.tabs(["🛠️ Генератор", "📤 Импорт и редактирование"])


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
        st.download_button(label="⬇️ Скачать main_output.hex", data=full_hex, file_name="main_output.hex")


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
        st.download_button(label="⬇️ Скачать bento_output.hex", data=full_hex, file_name="bento_output.hex")


# --- ИМПОРТ И РЕДАКТИРОВАНИЕ ---
with tab2:
    st.markdown("### 📥 Вставьте HEX-строку для редактирования")

    hex_input = st.text_area("HEX-строка:", placeholder="Введите HEX-строку...", height=200)

    if st.button("🔍 Распарсить HEX"):
        if not hex_input:
            st.warning("Введите HEX-строку")
        else:
            parsed = parse_hex_to_params(hex_input)

            st.markdown("### ✏️ Отредактируйте значения")

            imported_inputs = []
            for idx, level in enumerate(main_levels):
                with st.expander(level["name"], expanded=True):
                    cols = st.columns(3)
                    l1 = cols[0].number_input("L1", value=parsed[idx][0], format="%.4f", key=f"import_l1_{idx}")
                    l1a = cols[1].number_input("L1A", value=parsed[idx][1], format="%.4f", key=f"import_l1a_{idx}")
                    l2 = cols[0].number_input("L2", value=parsed[idx][2], format="%.4f", key=f"import_l2_{idx}")
                    l2a = cols[1].number_input("L2A", value=parsed[idx][3], format="%.4f", key=f"import_l2a_{idx}")
                    l3 = cols[0].number_input("L3", value=parsed[idx][4], format="%.4f", key=f"import_l3_{idx}")
                    l3a = cols[1].number_input("L3A", value=parsed[idx][5], format="%.4f", key=f"import_l3a_{idx}")
                    imported_inputs.append([l1, l1a, l2, l2a, l3, l3a])

            if st.button("💾 Сохранить как обновлённый HEX", key="save_parsed"):
                full_hex = generate_hex(imported_inputs, main_levels, level_slices_main, start_header=True)
                st.text_area("Обновлённый HEX:", value=full_hex, height=300)
                st.download_button(label="⬇️ Скачать обновлённый HEX", data=full_hex, file_name="updated_main_output.hex")
