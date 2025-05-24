import locale
from datetime import date

import pandas as pd
import streamlit as st

from apps import toggle_sidebar

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

minhas_apostas: list[str] = [
    "05 15 26 27 46 53",  # aposta n.° 1
    "03 12 19 20 45 47",  # aposta n.° 2
    "01 10 17 41 42 56",  # aposta n.° 3
    "02 10 13 27 53 55",  # aposta n.° 4
    "06 07 08 11 43 56",  # aposta n.° 5
    "08 10 14 25 33 34",  # aposta n.° 6
    "05 11 16 40 43 57",  # aposta n.° 7
    "04 05 08 13 17 38",  # aposta n.° 8
    "13 24 32 49 51 60",  # aposta n.° 9
    "11 16 19 43 58 60",  # aposta n.° 10
    "03 05 10 20 35 46",  # aposta n.° 11
    "02 09 10 19 31 57",  # aposta n.° 12
    "04 18 20 21 39 57",  # aposta n.° 13
    "02 11 22 36 49 60",  # aposta n.° 14
    "02 21 39 48 52 57",  # aposta n.° 15
    "14 41 45 50 54 59",  # aposta n.° 16
    "13 20 22 25 28 39",  # aposta n.° 17
    "01 16 21 34 49 54",  # aposta n.° 18
]


@st.cache_data(show_spinner="⏳Obtendo os dados, aguarde...")
def load_megasena() -> pd.DataFrame:
    df: pd.DataFrame = pd.read_excel(io=st.session_state["xlsx_file"], engine="openpyxl")

    for coluna in df.columns[2:8]:
        df[coluna] = df[coluna].astype(str).str.zfill(2)

    df["bolas"] = df[df.columns[2:8]].apply(" ".join, axis=1)

    for coluna in ["Rateio 6 acertos", "Rateio 5 acertos", "Rateio 4 acertos"]:
        df[coluna] = df[coluna].astype(str).str.replace(r"\D", "", regex=True).astype(float) / 100

    df = df[["Concurso", "Data do Sorteio", "bolas", "Ganhadores 6 acertos", "Rateio 6 acertos",
             "Ganhadores 5 acertos", "Rateio 5 acertos", "Ganhadores 4 acertos", "Rateio 4 acertos"]]
    df.columns = ["id_sorteio", "dt_sorteio", "bolas", "acerto_6", "rateio_6",
                  "acerto_5", "rateio_5", "acerto_4", "rateio_4"]
    df.set_index(["id_sorteio"], inplace=True)
    df.loc[2701] = ["16/03/2024", "06 15 18 31 32 47", 0, 0.0, 72, 59349.01, 5712, 1068.7]
    df["dt_sorteio"] = pd.to_datetime(df["dt_sorteio"], format="%d/%m/%Y")
    df = df.reset_index().sort_values(by=["id_sorteio", "dt_sorteio"], ignore_index=True)

    return df


st.columns(3)[0].file_uploader("Importar", type="xlsx", key="xlsx_file", label_visibility="hidden")

if st.session_state["xlsx_file"] and st.session_state["xlsx_file"].name == "Mega-Sena.xlsx":
    megasena: pd.DataFrame = load_megasena()

    tab0, tab1, tab2, tab3 = st.tabs(["**Apostas Sorteadas**", "**Minhas apostas**",
                                      "**Sua aposta da Mega-Sena**", "**Mega-Sena da Virada**"])

    with tab0:
        col = st.columns([1, 4])

        with col[0]:
            st.slider("**Mês:**", min_value=1, max_value=12, value=date.today().month, key="month_tab0")
            st.selectbox("**Ano:**", options=range(date.today().year, 1995, -1), key="year_tab0")

        with col[1]:
            all_mega: pd.DataFrame = megasena[megasena["dt_sorteio"].dt.year.eq(st.session_state["year_tab0"]) &
                                              megasena["dt_sorteio"].dt.month.eq(st.session_state["month_tab0"])].copy()
            all_mega["dt_sorteio"] = all_mega["dt_sorteio"].dt.strftime("%x (%a)")

            st.data_editor(
                data=all_mega,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "id_sorteio": st.column_config.NumberColumn(label="Concurso", format="%04d"),
                    "dt_sorteio": st.column_config.TextColumn(label="Data do Sorteio"),
                    "bolas": st.column_config.ListColumn(label="Bolas Sorteadas"),
                    "acerto_6": st.column_config.NumberColumn(label="Acerto de 6"),
                    "rateio_6": st.column_config.NumberColumn(label="Rateio de 6", format="dollar"),
                    "acerto_5": st.column_config.NumberColumn(label="Acerto de 5"),
                    "rateio_5": st.column_config.NumberColumn(label="Rateio de 5", format="dollar"),
                    "acerto_4": st.column_config.NumberColumn(label="Acerto de 4"),
                    "rateio_4": st.column_config.NumberColumn(label="Rateio de 4", format="dollar"),
                },
                key="de_all_mega",
                row_height=25,
            )

    with tab1:
        col1, col2 = st.columns([1.3, 2.8])

        with col1:
            minhas: list[str] = [f"Aposta n.° {x + 1:02d} ➟ {" - ".join(aposta.split())}"
                                 for x, aposta in enumerate(minhas_apostas)]

            st.data_editor(
                data=minhas,
                use_container_width=True,
                hide_index=True,
                column_config={"value": st.column_config.TextColumn(label="Minhas Apostas")},
                key="de_apostas",
                row_height=25,
            )

        with col2:
            for r in range(6, 3, -1):
                st.write(f"**Acerto de {r} bolas**")

                mega_copy: dict[str, list[int | str]] = {"Concurso": [], "Data do Sorteio": [],
                                                         "Suas bolas acertadas": [], "Sua aposta n.°": []}

                for row in megasena[["id_sorteio", "dt_sorteio", "bolas", f"acerto_{r}", f"rateio_{r}"]].copy() \
                        .itertuples(index=False, name=None):
                    for aposta in minhas_apostas:
                        bolas: list[str] = aposta.split()

                        match: list[str] = [bolas[x] for x in range(6) if bolas[x] in row[2]]

                        if len(match) == r:
                            mega_copy["Concurso"].append(str(row[0]).zfill(4))
                            mega_copy["Data do Sorteio"].append(row[1].strftime("%x (%a)"))
                            mega_copy["Suas bolas acertadas"].append(" ".join(match))
                            mega_copy["Sua aposta n.°"].append(minhas_apostas.index(aposta) + 1)

                st.columns([2.5, 0.5])[0].dataframe(
                    data=mega_copy,
                    use_container_width=True,
                    hide_index=True,
                    key="de_acertas",
                    row_height=25,
                )

    with tab2:
        st.columns(5)[0].text_input("Sua aposta:", key="sua_aposta", placeholder="Ex: 01 02 03 04 05 06")

        st.button("**Acertei?**", key="btn_acertas", type="primary")

        mega_copy2: dict[str, list[int | str]] = {"Concurso": [], "Data de Sorteio": [],
                                                  "Bolas Sorteadas": [], "Seus Acertos": []}

        if st.session_state["btn_acertas"]:
            if st.session_state["sua_aposta"]:
                with st.spinner("Obtendo as apostas, aguarde...", show_time=True):
                    for row in megasena.copy().itertuples(index=False, name=None):
                        match: list[str] = [aposta for aposta in st.session_state["sua_aposta"].split()
                                            if aposta in row[2]]

                        if len(match) >= 4:
                            mega_copy2["Concurso"].append(str(row[0]).zfill(4))
                            mega_copy2["Data de Sorteio"].append(row[1].strftime("%x (%a)"))
                            mega_copy2["Bolas Sorteadas"].append(row[2])
                            mega_copy2["Seus Acertos"].append(len(match))

                st.columns([2.5, 1, 1])[0].data_editor(
                    data=mega_copy2,
                    use_container_width=True,
                    hide_index=True,
                    key="de_acertas",
                    row_height=25,
                )

            else:
                st.toast("**Preencha suas bolas!**", icon=":material/warning:")

    with tab3:
        mega_da_virada: pd.DataFrame = megasena.copy()
        mega_da_virada["ano"] = mega_da_virada["dt_sorteio"].dt.year
        mega_da_virada = mega_da_virada[mega_da_virada["dt_sorteio"]. \
            isin(mega_da_virada[mega_da_virada["ano"] != pd.Timestamp.now().year]. \
                 groupby(["ano"])["dt_sorteio"].transform("max"))].reset_index(drop=True). \
            drop(["ano"], axis=1)
        mega_da_virada["dt_sorteio"] = mega_da_virada["dt_sorteio"].dt.strftime("%x (%a)")

        st.data_editor(
            data=mega_da_virada,
            use_container_width=True,
            hide_index=True,
            column_config={
                "id_sorteio": st.column_config.NumberColumn(label="Concurso", format="%04d"),
                "dt_sorteio": st.column_config.TextColumn(label="Data do Sorteio"),
                "bolas": st.column_config.ListColumn(label="Bolas Sorteadas"),
                "acerto_6": st.column_config.NumberColumn(label="Acerto de 6"),
                "rateio_6": st.column_config.NumberColumn(label="Rateio de 6", format="dollar"),
                "acerto_5": st.column_config.NumberColumn(label="Acerto de 5"),
                "rateio_5": st.column_config.NumberColumn(label="Rateio de 5", format="dollar"),
                "acerto_4": st.column_config.NumberColumn(label="Acerto de 4"),
                "rateio_4": st.column_config.NumberColumn(label="Rateio de 4", format="dollar"),
            },
            key="de_mega_da_virada",
            row_height=25,
        )

if st.button("**Voltar**", key="back", type="primary", icon=":material/reply:", on_click=toggle_sidebar):
    st.switch_page("apps.py")
