import locale

import pandas as pd
import streamlit as st

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

if "xlsx_file" not in st.session_state:
    st.session_state["xlsx_file"] = None

st.set_page_config(layout="wide")

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


@st.cache_data(show_spinner="Obtendo os dados, aguarde...")
def load_megasena(xlsx_file: str) -> pd.DataFrame:
    df: pd.DataFrame = pd.read_excel(io=xlsx_file, engine="openpyxl")

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

    df = df.reset_index().sort_values(by=["id_sorteio", "dt_sorteio"], ignore_index=True)

    df["dt_sorteio"] = pd.to_datetime(df["dt_sorteio"], format="%d/%m/%Y")

    return df


st.title("Megasena")

st.session_state["xlsx_file"] = st.columns(3)[0].file_uploader("Importar", type="xlsx", label_visibility="hidden")

if st.session_state["xlsx_file"] and st.session_state["xlsx_file"].name == "Mega-Sena.xlsx":
    megasena: pd.DataFrame = load_megasena(st.session_state["xlsx_file"])

    tab1, tab2, tab3, tab4 = st.tabs(["**Minhas apostas**", "**Sorteios da Mega-Sena**",
                                      "**Sua aposta da Mega-Sena**", "**Mega-Sena da Virada**"])

    with tab1:
        minhas = [f"Aposta n.° {x + 1:02d} ➟ {" - ".join(aposta.split())}" for x, aposta in enumerate(minhas_apostas)]

        st.columns(3)[0].dataframe(
            data=minhas,
            use_container_width=True,
            row_height=25,
            height=387,
            column_config={"value": st.column_config.TextColumn(label="Minhas Apostas")}
        )

    with tab2:
        col = st.columns([2, 1, 1])

        with col[0]:
            for r in range(6, 3, -1):
                st.write(f"**Acerto de {r} bolas**")

                mega_copy: dict[str: list] = {"id_sorteio": [], "dt_sorteio": [], "bolas": [], "apostas": []}

                for row in megasena[["id_sorteio", "dt_sorteio", "bolas", f"acerto_{r}", f"rateio_{r}"]].copy() \
                        .itertuples(index=False, name=None):
                    for aposta in minhas_apostas:
                        bolas: list[str] = aposta.split()

                        match: list[str] = [bolas[x] for x in range(6) if bolas[x] in row[2]]

                        if len(match) == r:
                            mega_copy["id_sorteio"].append(row[0])
                            mega_copy["dt_sorteio"].append(row[1].strftime("%x (%a)"))
                            mega_copy["bolas"].append(" ".join(match))
                            mega_copy["apostas"].append(minhas_apostas.index(aposta) + 1)

                st.dataframe(
                    data=mega_copy,
                    row_height=25,
                    use_container_width=True,
                    column_config={
                        "id_sorteio": st.column_config.NumberColumn(label="Concurso", format="%04d"),
                        "dt_sorteio": st.column_config.TextColumn(label="Data do Sorteio"),
                        "bolas": st.column_config.ListColumn(label="Suas bolas acertadas"),
                        "apostas": st.column_config.NumberColumn(label="Sua aposta n.°"),
                    }
                )

    with tab3:
        sua_aposta = st.columns(5)[0].text_input("Sua aposta:")

        col = st.columns(3)

        with col[0]:
            if st.button("**Acertei?**", type="primary"):
                if sua_aposta:
                    with st.spinner("Obtendo as apostas, aguarde...", show_time=True):
                        mega_copy2 = {"id_sorteio": [], "dt_sorteio": [], "bolas": [], "acertos": []}

                        for row in megasena.copy().itertuples(index=False, name=None):
                            match = [aposta for aposta in sua_aposta.split() if aposta in row[2]]

                            if len(match) >= 4:
                                mega_copy2["id_sorteio"].append(row[0])
                                mega_copy2["dt_sorteio"].append(row[1].strftime("%x (%a)"))
                                mega_copy2["bolas"].append(row[2])
                                mega_copy2["acertos"].append(len(match))

                        st.dataframe(
                            data=mega_copy2,
                            row_height=25,
                            use_container_width=True,
                            column_config={
                                "id_sorteio": st.column_config.NumberColumn(label="Concurso", format="%04d"),
                                "dt_sorteio": st.column_config.TextColumn(label="Data de Sorteio"),
                                "bolas": st.column_config.ListColumn(label="Bolas Sorteadas"),
                                "acertos": st.column_config.NumberColumn(label="Seus acertos"),
                            }
                        )

                    st.button("**Recomeçar**", type="primary")
                else:
                    st.toast("**Preencha suas bolas!**")

    with tab4:
        # SELECT * FROM megasena WHERE dt_sorteio IN (
        #     SELECT MAX(dt_sorteio) FROM megasena GROUP BY YEAR(dt_sorteio)
        #         HAVING YEAR(dt_sorteio) <> YEAR(CURRENT_DATE)
        # )
        mega_da_virada = megasena.copy()

        col = st.columns([2, 0.5, 0.5])

        with col[0]:
            mega_da_virada["ano"] = mega_da_virada["dt_sorteio"].dt.year
            mega_da_virada = mega_da_virada[mega_da_virada["dt_sorteio"]. \
                isin(mega_da_virada[mega_da_virada["ano"] != pd.Timestamp.now().year]. \
                     groupby(["ano"])["dt_sorteio"].transform("max"))].reset_index(drop=True). \
                drop(["ano"], axis=1)
            mega_da_virada["dt_sorteio"] = mega_da_virada["dt_sorteio"].dt.strftime("%x (%a)")

            st.dataframe(
                data=mega_da_virada,
                hide_index=True,
                row_height=25,
                height=387,
                use_container_width=True,
                column_config={
                    "id_sorteio": st.column_config.NumberColumn(label="Concurso", format="%04d"),
                    "dt_sorteio": st.column_config.TextColumn(label="Data do Sorteio"),
                    "bolas": st.column_config.ListColumn(label="Suas bolas acertadas"),
                    "acerto_6": st.column_config.NumberColumn(label="Acerto de 6"),
                    "rateio_6": st.column_config.NumberColumn(label="Rateio de 6", format="dollar"),
                    "acerto_5": st.column_config.NumberColumn(label="Acerto de 5"),
                    "rateio_5": st.column_config.NumberColumn(label="Rateio de 5", format="dollar"),
                    "acerto_4": st.column_config.NumberColumn(label="Acerto de 4"),
                    "rateio_4": st.column_config.NumberColumn(label="Rateio de 4", format="dollar"),
                }
            )

# def verificar_acertos(escolhidas, sorteadas):
#     acertos = set(sorteadas).intersection(escolhidas)
#
#     if len(acertos) == 4:
#         return f"Você acertou 4 números -> {sorted(acertos)}"
#     elif len(acertos) == 5:
#         return f"Você acertou 5 números -> {sorted(acertos)}"
#     elif len(acertos) == 6:
#         return f"Você acertou 6 números -> {sorted(acertos)}"
#     else:
#         return f"Você não acertou nem 4, 5 e 6 números..."


# bolas_escolhidas = [6, 13, 25, 33, 42, 50]
# bolas_sorteadas = [6, 13, 25, 33, 42, 50]

# resultado = verificar_acertos(bolas_escolhidas, bolas_sorteadas)
# print(resultado)
