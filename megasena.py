# %%
import locale

import pandas as pd

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
locale.setlocale(locale.LC_MONETARY, "pt_BR.UTF-8")

pd.set_option("display.expand_frame_repr", False)
pd.set_option("display.float_format", lambda val: f"R$ {locale.currency(val=val, symbol=False, grouping=True)}")
pd.set_option("display.max_columns", None)

minhas_apostas: tuple = (
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
)

# %%
megasena: pd.DataFrame = pd.read_excel(io="~/Downloads/mega-Sena.xlsx", engine="openpyxl")

for col in megasena.columns[2:8]:
    megasena[col] = megasena[col].astype(str).str.zfill(2)

megasena["bolas"] = megasena[megasena.columns[2:8]].apply(" ".join, axis=1)

for col in ["Rateio 6 acertos", "Rateio 5 acertos", "Rateio 4 acertos"]:
    megasena[col] = megasena[col].astype(str).str.replace(r"\D", "", regex=True).astype(float) / 100

megasena = megasena[["Concurso", "Data do Sorteio", "bolas", "Ganhadores 6 acertos", "Rateio 6 acertos",
                     "Ganhadores 5 acertos", "Rateio 5 acertos", "Ganhadores 4 acertos", "Rateio 4 acertos"]]

megasena.columns = ["id_sorteio", "dt_sorteio", "bolas", "acerto_6", "rateio_6",
                    "acerto_5", "rateio_5", "acerto_4", "rateio_4"]

megasena.set_index(["id_sorteio"], inplace=True)

megasena.loc[2701] = ["16/03/2024", "06 15 18 31 32 47", 0, 0.0, 72, 59349.01, 5712, 1068.7]

megasena = megasena.reset_index().sort_values(by=["id_sorteio", "dt_sorteio"], ignore_index=True)

print(megasena.tail(15))

# %%
for r in range(6, 3, -1):
    mega_copy: dict[str: list] = {"Concurso": [], "Data": [], "Bolas": [], "Aposta n.°": []}

    for row in megasena[["id_sorteio", "dt_sorteio", "bolas", f"acerto_{r}", f"rateio_{r}"]] \
            .itertuples(index=False, name=None):
        for aposta in minhas_apostas:
            bolas: list[str] = aposta.split()

            match: list[str] = [bolas[x] for x in range(6) if bolas[x] in row[2]]

            if len(match) == r:
                mega_copy["Concurso"].append(str(row[0]).zfill(4))
                mega_copy["Data"].append(pd.to_datetime(row[1], format="%d/%m/%Y").strftime("%x (%a)"))
                mega_copy["Bolas"].append(" ".join(match))
                mega_copy["Aposta n.°"].append(minhas_apostas.index(aposta) + 1)

    print(f"\nLista de {r} acertos:")
    print(pd.DataFrame(mega_copy)) if len(pd.DataFrame(mega_copy)) != 0 \
        else print("Suas apostas não tiveram acertos...")

# %%
sua_aposta: str = input("Sua aposta: ")

mega_copy = {"Concurso": [], "Data": [], "Bolas": [], "Acertos": []}

for row in megasena.itertuples(index=False, name=None):
    match = [aposta for aposta in sua_aposta.split() if aposta in row[2]]

    if len(match) >= 4:
        mega_copy["Concurso"].append(str(row[0]).zfill(4))
        mega_copy["Data"].append(pd.to_datetime(row[1], format="%d/%m/%Y").strftime("%x (%a)"))
        mega_copy["Bolas"].append(row[2])
        mega_copy["Acertos"].append(len(match))

print(pd.DataFrame(mega_copy)) if len(pd.DataFrame(mega_copy)) != 0 \
    else print("Sua aposta não teve acertos...\n")

# %%
"""
SELECT * FROM megasena WHERE dt_sorteio IN (
    SELECT MAX(dt_sorteio) FROM megasena GROUP BY YEAR(dt_sorteio)
        HAVING YEAR(dt_sorteio) <> YEAR(CURRENT_DATE)
)
"""

df_mega_da_virada = megasena.copy()

df_mega_da_virada["dt_sorteio"] = pd.to_datetime(df_mega_da_virada["dt_sorteio"], format="%d/%m/%Y")
df_mega_da_virada["ano"] = df_mega_da_virada["dt_sorteio"].dt.year

df_mega_da_virada = df_mega_da_virada[df_mega_da_virada["dt_sorteio"]. \
    isin(df_mega_da_virada[df_mega_da_virada["ano"] != pd.Timestamp.now().year]. \
         groupby(["ano"])["dt_sorteio"].transform("max"))].reset_index(drop=True)

df_mega_da_virada["ano"] = df_mega_da_virada["dt_sorteio"].dt.strftime("%d/%m/%Y")

print(df_mega_da_virada)

# %%
apostas: dict[int: int] = {}

for x in minhas_apostas:
    y: list[str] = x.split()
    for z in range(len(y)):
        try:
            apostas[int(y[z])] += 1
        except KeyError:
            apostas[int(y[z])] = 1

apostas_ordenadas: dict[int: int] = {k: v for k, v in sorted(apostas.items(), key=lambda s: s[0])}

acertos: pd.DataFrame = pd.DataFrame(data=apostas_ordenadas, index=["acertos"])
acertos.index.name = "bolas"
print(acertos)

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
