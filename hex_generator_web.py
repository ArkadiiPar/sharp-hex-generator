import streamlit as st
import struct


# --- Вспомогательные функции ---
def float_to_hex(f):
    return struct.pack('<f', f).hex()


# --- Sharp HEX Data ---
sharp_hex_lines = [
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

# --- Индексы для Sharp ---
sharp_slices_main = {
    "Sharp very low": (0, 6),
    "Sharp low": (6, 12),
    "Sharp med": (12, 18),
    "Sharp high": (18, 24),
    "Sharp very high": (24, 30),
}

sharp_slices_bento = {
    "Sharp bento low": (30, 36),
    "Sharp bento high": (36, 42)
}

# --- Уровни Sharp по умолчанию ---
sharp_all_levels = [
    {"name": "Sharp very low",  "default": [7.0, 0.060, 3.075, 0.040, 1.875, 0.058]},
    {"name": "Sharp low",       "default": [8.6, 0.060, 3.69, 0.040, 2.25, 0.058]},
    {"name": "Sharp med",       "default": [10.0, 0.060, 4.225, 0.040, 2.5, 0.058]},
    {"name": "Sharp high",      "default": [10.0, 0.066, 3.87, 0.040, 4.62, 0.0224]},
    {"name": "Sharp very high", "default": [11.3, 0.0436, 3.70, 0.032, 2.05, 0.0232]},
    {"name": "Sharp bento low", "default": [16.0, 0.0195, 3.10, 0.01975, 1.89, 0.02]},
    {"name": "Sharp bento high","default": [18.5, 0.0174, 2.70, 0.0187, 1.70, 0.02]}
]

# --- Генератор Sharp HEX ---
def generate_sharp_hex(values_list, level_names, level_slices, start_header=True):
    lines = []

    for i, values in enumerate(values_list):
        l1, l1a, l2, l2a, l3, l3a = values
        name = level_names[i]["name"]
        start, end = level_slices[name]

        modified_block = sharp_hex_lines[start:end]
        modified_block[0] = f"{float_to_hex(l1)}1d{float_to_hex(l1a)}"
        modified_block[2] = f"{float_to_hex(l2)}1d{float_to_hex(l2a)}"
        modified_block[4] = f"{float_to_hex(l3)}1d{float_to_hex(l3a)}"

        lines.extend(modified_block)

    full_hex = "".join(lines)
    if start_header:
        full_hex = "0a490a140d" + full_hex
    return full_hex


# --- LUMA HEX Data ---
luma_original_lines = [
    "00000a610a0f0d",

    # Bayer luma denoise very low — 14 строк
    "0000803f", "15", "cdcccc3d", "1d", "ae50223f", "0a0f0d",
    "6666663f", "15", "cdcccc3d", "1d", "95806d3e", "0a0f0d",
    "9a99593f", "15", "cdcc4c3d", "1d", "09997a3e", "0a0f0d",
    "cdcc4c3f", "15", "cdcc4c3d", "1d", "0e06743e", "0a0a0d",
    "0000403f", "1d", "68ceb13e", "12050d0000a0401dcdcccc3f250000003f0a610a0f0d",

    # Bayer luma denoise low — 14 строк
    "cdcc4c3f", "15", "cdcccc3d", "1d", "65a5113f", "0a0f0d",
    "3333333f", "15", "cdcccc3d", "1d", "5a469a3e", "0a0f0d",
    "3333333f", "15", "9a99993d", "1d", "6616913e", "0a0f0d",
    "9a99193f", "15", "0000803d", "1d", "f20bbf3e", "0a0a0d",
    "3333333f", "1d", "ffe6ed3e", "12050d000020411dcdcccc3f250000003f0a610a0f0d",

    # Bayer luma denoise med — 14 строк
    "3333333f", "15", "cdcccc3d", "1d", "14fa003f", "0a0f0d",
    "cdcc4c3f", "15", "cdcccc3d", "1d", "49ccbd3e", "0a0f0d",
    "9a99193f", "15", "cdcccc3d", "1d", "37e0a43e", "0a0f0d",
    "cdcccc3e", "15", "9a99993d", "1d", "7b0a023f", "0a0a0d",
    "0000003f", "1d", "d1ff143f", "12050d0000a0411dcdcccc3f250000003f0a610a0f0d",

    # Bayer luma denoise high — 14 строк
    "9a99193f", "15", "9a99193e", "1d", "1093243f", "0a0f0d",
    "0000003f", "15", "cdcccc3d", "1d", "d08a203f", "0a0f0d",
    "0000803e", "15", "cdcccc3d", "1d", "54eef13e", "0a0f0d",
    "0000803e", "15", "cdcccc3d", "1d", "93d7b93e", "0a0a0d",
    "cdcc4c3e", "1d", "af3c9f3d", "12050d000020421dcdcccc3f250000003f0a610a0f0d"
]

# --- Срезы для уровней LUMA ---
luma_slices = {
    "Bayer luma denoise very low": (1, 15),     # 1–14
    "Bayer luma denoise low":      (15, 29),    # 15–28
    "Bayer luma denoise med":      (29, 43),    # 29–42
    "Bayer luma denoise high":     (43, 57),    # 43–56
    "Bayer luma denoise very high": (57, 71)    # 57–70
}

# --- Параметры по умолчанию для LUMA ---
luma_levels = [
    {"name": "Bayer luma denoise very low", "default": [1.00, 0.10, 0.634044, 0.90, 0.10, 0.231936, 0.85, 0.05, 0.244724, 0.80, 0.05, 0.238304, 0.75, 0.347278]},
    {"name": "Bayer luma denoise low",     "default": [0.80, 0.10, 0.568930, 0.70, 0.10, 0.301318, 0.70, 0.075, 0.283374, 0.60, 0.0625, 0.373138, 0.70, 0.464653]},
    {"name": "Bayer luma denoise med",     "default": [0.70, 0.10, 0.503816, 0.80, 0.10, 0.370699, 0.60, 0.10, 0.322023, 0.40, 0.075, 0.507972, 0.50, 0.582028]},
    {"name": "Bayer luma denoise high",    "default": [0.60, 0.15, 0.642869, 0.50, 0.10, 0.627118, 0.25, 0.10, 0.472521, 0.25, 0.10, 0.362973, 0.20, 0.0777525]},
    {"name": "Bayer luma denoise very high", "default": [0.65, 0.15, 0.642869, 0.75, 0.10, 0.627118, 0.38, 0.10, 0.472521, 0.30, 0.10, 0.362973, 0.25, 0.0777525]}
]

# --- Генератор LUMA HEX ---
def generate_luma_hex(values_list, level_names, level_slices):
    lines = []

    for i, values in enumerate(values_list):
        l1, l1a, l1b, l2, l2a, l2b, l3, l3a, l3b, l4, l4a, l4b, l5, l5a = values
        name = level_names[i]["name"]
        start, end = level_slices[name]

        modified_block = luma_original_lines[start:end]

        # Проверяем длину блока
        if len(modified_block) < 28:
            st.error(f"❌ Блок '{name}' слишком короткий. Требуется 28 элементов")
            continue

        # Замена значений
        modified_block[0] = float_to_hex(l1)     # L1
        modified_block[2] = float_to_hex(l1a)    # L1A
        modified_block[4] = float_to_hex(l1b)    # L1B

        modified_block[6] = float_to_hex(l2)     # L2
        modified_block[8] = float_to_hex(l2a)    # L2A
        modified_block[10] = float_to_hex(l2b)   # L2B

        modified_block[12] = float_to_hex(l3)    # L3
        modified_block[14] = float_to_hex(l3a)   # L3A
        modified_block[16] = float_to_hex(l3b)   # L3B

        modified_block[18] = float_to_hex(l4)    # L4
        modified_block[20] = float_to_hex(l4a)   # L4A
        modified_block[22] = float_to_hex(l4b)   # L4B

        modified_block[24] = float_to_hex(l5)    # L5
        modified_block[26] = float_to_hex(l5a)   # L5A

        lines.extend(modified_block)

    full_hex = "".join(lines)
    full_hex = luma_original_lines[0] + full_hex  # добавляем заголовок
    return full_hex


# --- Интерфейс Streamlit ---
st.set_page_config(page_title="HEX Sharp & Luma Config Generator", layout="wide")
tab1, tab2 = st.tabs(["ImageSharp", "LUMA"])


# --- Вкладка: Sharp ---
with tab1:
    st.title("🔧 Sharp Level HEX Code Generator")

    main_inputs = []
    for idx, level in enumerate(sharp_all_levels[:5]):
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
        values_list = []
        for vals in main_inputs:
            values_list.append(vals)

        full_hex = generate_sharp_hex(values_list, sharp_all_levels[:5], sharp_slices_main, start_header=True)
        st.text_area("Сгенерированный HEX (основные уровни):", value=full_hex, height=300)
        st.download_button(label="⬇️ Скачать main_output.hex", data=full_hex, file_name="main_output.hex")


    bento_inputs = []
    for idx, level in enumerate(sharp_all_levels[5:], start=5):
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
        values_list = []
        for vals in bento_inputs:
            values_list.append(vals)

        full_hex = generate_sharp_hex(values_list, sharp_all_levels[5:], sharp_slices_bento, start_header=False)
        st.text_area("Сгенерированный HEX (Bento):", value=full_hex, height=300)
        st.download_button(label="⬇️ Скачать bento_output.hex", data=full_hex, file_name="bento_output.hex")


# --- Вкладка: LUMA ---
with tab2:
    st.title("🔧 LUMA Level HEX Code Generator")

    luma_inputs = []
    for idx, level in enumerate(luma_levels):
        with st.expander(level["name"], expanded=True):
            cols = st.columns(3)
            l1 = cols[0].number_input("L1", value=level["default"][0], format="%.4f", key=f"luma_l1_{idx}")
            l1a = cols[1].number_input("L1A", value=level["default"][1], format="%.4f", key=f"luma_l1a_{idx}")
            l1b = cols[2].number_input("L1B", value=level["default"][2], format="%.4f", key=f"luma_l1b_{idx}")

            l2 = cols[0].number_input("L2", value=level["default"][3], format="%.4f", key=f"luma_l2_{idx}")
            l2a = cols[1].number_input("L2A", value=level["default"][4], format="%.4f", key=f"luma_l2a_{idx}")
            l2b = cols[2].number_input("L2B", value=level["default"][5], format="%.4f", key=f"luma_l2b_{idx}")

            l3 = cols[0].number_input("L3", value=level["default"][6], format="%.4f", key=f"luma_l3_{idx}")
            l3a = cols[1].number_input("L3A", value=level["default"][7], format="%.4f", key=f"luma_l3a_{idx}")
            l3b = cols[2].number_input("L3B", value=level["default"][8], format="%.4f", key=f"luma_l3b_{idx}")

            l4 = cols[0].number_input("L4", value=level["default"][9], format="%.4f", key=f"luma_l4_{idx}")
            l4a = cols[1].number_input("L4A", value=level["default"][10], format="%.4f", key=f"luma_l4a_{idx}")
            l4b = cols[2].number_input("L4B", value=level["default"][11], format="%.4f", key=f"luma_l4b_{idx}")

            l5 = cols[0].number_input("L5", value=level["default"][12], format="%.4f", key=f"luma_l5_{idx}")
            l5a = cols[1].number_input("L5A", value=level["default"][13], format="%.4f", key=f"luma_l5a_{idx}")

            luma_inputs.append([l1, l1a, l1b, l2, l2a, l2b, l3, l3a, l3b, l4, l4a, l4b, l5, l5a])

    if st.button("🚀 Сгенерировать LUMA HEX"):
        values_list = []
        for vals in luma_inputs:
            values_list.append(vals)

        full_hex = generate_luma_hex(values_list, luma_levels, luma_slices)
        st.text_area("Сгенерированный HEX (LUMA):", value=full_hex, height=400)
        st.download_button(label="⬇️ Скачать luma_output.hex", data=full_hex, file_name="luma_output.hex")
