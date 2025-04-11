# %%
import locale
import os
from datetime import date

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sqlalchemy as sa
from dotenv import load_dotenv

load_dotenv()

locale.setlocale(category=locale.LC_ALL, locale="pt_BR.UTF-8")
locale.setlocale(category=locale.LC_MONETARY, locale="pt_BR.UTF-8")

pd.set_option("display.expand_frame_repr", False)
pd.set_option("display.float_format", lambda val: f"R$ {locale.currency(val=val, symbol=False, grouping=True)}")
pd.set_option("display.max_columns", None)

engine: sa.Engine = sa.engine.create_engine(url=os.getenv("AIVEN_PG"))

year: int = date.today().year
year_month: int = year*100 + date.today().month

# %%
stmt: str = """
CREATE TABLE IF NOT EXISTS lançamento (
    id_lançamento SERIAL PRIMARY KEY,
    lançamento VARCHAR(60) NOT NULL
)
"""
with engine.begin() as cnx:
    cnx.execute(sa.text(stmt))
print("Tabela 'lançamento' criada com sucesso!")

# %%
stmt: str = """
CREATE TABLE IF NOT EXISTS espelho (
    id SERIAL PRIMARY KEY,
    id_lançamento INTEGER NOT NULL,
    período INTEGER NOT NULL,
    acerto BOOLEAN DEFAULT FALSE NOT NULL,
    valor REAL NOT NULL
)
"""
with engine.begin() as cnx:
    cnx.execute(sa.text(stmt))
print("Tabela 'espelho' criada com sucesso!")

# %%
# inserir novos registros para a tabela espelho
row_inserted: int = pd.read_csv("src/espelho.csv", sep=",", encoding="utf-8-sig") \
    .to_sql(name="espelho", con=engine, if_exists="append", index=False)
print(f"Foram {row_inserted} lançamentos inseridos com sucesso.")

# %%
release: pd.DataFrame = pd.read_sql(sql=sa.text(f"SELECT * FROM lançamento"), con=engine)
mirror: pd.DataFrame = pd.read_sql(sql=sa.text(f"SELECT * FROM espelho"), con=engine)

joints: pd.DataFrame = pd.merge(left=release, right=mirror, how="inner", on=["id_lançamento"]) \
    .drop(["id", "id_lançamento"], axis=1)

# %%
# exibir a tabela de lançamento
print(release.rename(columns=dict(id_lançamento="Código", lançamento="Lançamento")))

# %%
# exibir os períodos com seus soldos mensais do ano desejado
"""
SELECT período AS Período, SUM(valor) AS Total
FROM espelho
WHERE período / 100 = EXTRACT(YEAR FROM CURRENT_DATE)
GROUP BY período
"""

dict_months: dict[int, str] = {
    int(f"{year}01"): f"janeiro de {year}",
    int(f"{year}02"): f"fevereiro de {year}",
    int(f"{year}03"): f"março de {year}",
    int(f"{year}04"): f"abril de {year}",
    int(f"{year}05"): f"maio de {year}",
    int(f"{year}06"): f"junho de {year}",
    int(f"{year}07"): f"julho de {year}",
    int(f"{year}08"): f"agosto de {year}",
    int(f"{year}09"): f"setembro de {year}",
    int(f"{year}10"): f"outubro de {year}",
    int(f"{year}11"): f"novembro de {year}",
    int(f"{year}12"): f"dezembro de {year}",
}

df_year_month: pd.DataFrame = joints.copy()
df_year_month["ano"] = pd.to_datetime(df_year_month["período"], format="%Y%m").dt.year
df_year_month = df_year_month[df_year_month["ano"].eq(year)] \
    .groupby(["período"])["valor"].sum() \
    .rename(index=dict_months)

print(df_year_month)

# %%
# exibir a tabela espelho para o mês atual
"""
SELECT l.lançamento, e.período, e.acerto, e.valor
FROM espelho e INNER JOIN lançamento l ON e.id_lançamento = l.id_lançamento
WHERE e.período = (SELECT MAX(período) FROM espelho)
ORDER BY e.acerto DESC, e.valor DESC
"""

df_mes: pd.DataFrame = joints[joints["período"].eq(year_month)].copy() \
    .sort_values(["acerto", "valor"], ascending=False).reset_index(drop=True)
df_mes["período"] = pd.to_datetime(df_mes["período"], format="%Y%m").dt.strftime("%B de %Y")
df_mes["acerto"] = df_mes["acerto"].map({False: "mês", True: "acerto"})

print(df_mes)

# %%
# exibir o gráfico do total de mês a mês para o ano atual
"""
SELECT l.lançamento, e.período, e.acerto, e.valor
FROM espelho e INNER JOIN lançamento l ON e.id_lançamento = l.id_lançamento
WHERE e.período / 100 = :year
ORDER BY e.período, e.acerto DESC, e.valor DESC
"""

df_ano: pd.DataFrame = joints.copy()
df_ano["ano"] = pd.to_datetime(df_ano["período"], format="%Y%m").dt.year
df_ano["acerto"] = df_ano["acerto"].map({False: "mês", True: "acerto"})
df_ano = df_ano[df_ano["ano"].eq(year)].drop(["ano"], axis=1) \
    .pivot(values=["valor"], index=["lançamento", "acerto"], columns=["período"])
df_ano.columns = df_ano.columns.droplevel(level=0)
df_ano = df_ano.reset_index().fillna(value=0)
df_ano.columns.rename("", inplace=True)
df_ano["média"] = df_ano.mean(axis=1, numeric_only=True)
df_ano["total"] = df_ano[df_ano.columns[:-1]].sum(axis=1, numeric_only=True)
df_ano.loc[100] = df_ano.sum(numeric_only=True)
df_ano.iloc[-1, 0] = "Sumário"
df_ano.iloc[-1, 1] = "total"
df_ano = df_ano.sort_values(["acerto", "total"], ascending=[True, False]) \
    .rename(columns={year * 100 + 1: "jan", year * 100 + 2: "fev", year * 100 + 3: "mar", year * 100 + 4: "abr",
                     year * 100 + 5: "mai", year * 100 + 6: "jun", year * 100 + 7: "jul", year * 100 + 8: "ago",
                     year * 100 + 9: "set", year * 100 + 10: "out", year * 100 + 11: "nov", year * 100 + 12: "dez"}) \
    .reset_index(drop=True)

print(df_ano)

# %%
# resumos totais anuais
"""
SELECT período / 100 AS ano, 'mês ' || período % 100 AS mês, SUM(valor) AS valor
FROM espelho
GROUP BY período
ORDER BY período
"""

df_anuais: pd.DataFrame = joints[["período", "valor"]].copy()
df_anuais = df_anuais.groupby(["período"])["valor"].sum().reset_index()
df_anuais["ano"] = pd.to_datetime(df_anuais["período"], format="%Y%m").dt.year
df_anuais["mês"] = pd.to_datetime(df_anuais["período"], format="%Y%m").dt.month
df_anuais = df_anuais.pivot(columns=["mês"], index=["ano"], values=["valor"])
df_anuais.columns = df_anuais.columns.droplevel(level=0)
df_anuais = df_anuais.fillna(0).rename(columns={1: "jan", 2: "fev", 3: "mar", 4: "abr", 5: "mai", 6: "jun",
                                                7: "jul", 8: "ago", 9: "set", 10: "out", 11: "nov", 12: "dez"})
df_anuais["média"] = df_anuais.mean(axis=1)
df_anuais["total"] = df_anuais[df_anuais.columns[:-1]].sum(axis=1)

print(df_anuais)

# %%
# exibir o gráfico do total de mês a mês para o ano atual
plt.figure(figsize=(16, 6))
plt.style.use("ggplot")

ax: plt.Axes = sns.barplot(data=df_anuais.loc[[year], df_anuais.columns[:-2]])
ax.set_title(f"Espelho {year}", loc="center", fontweight="bold", fontsize=12)
ax.set(xlabel="", ylabel="", yticks=[])

for mes in range(12):
    ax.bar_label(ax.containers[mes], fmt=lambda i: locale.currency(val=i, symbol=False, grouping=True), fontsize=10)

plt.show()

'''
import locale
from datetime import date

import pandas as pd
import streamlit as st
from streamlit.connections import SQLConnection

st.set_page_config(page_title="Contracheque BB", layout="wide")

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

engine: SQLConnection = st.connection(name="AIVEN_PG", type=SQLConnection)

st.title("💰Contracheque BB")


@st.cache_data(show_spinner="**Obtendo os dados, aguarde...**")
def load_mensal(year: int, month: int) -> pd.DataFrame:
    return engine.query(
        sql="""
            select t2.lançamento, t1.período, t1.acerto, t1.valor
            from espelho t1
                inner join lançamento t2
                    on t2.id_lançamento = t1.id_lançamento
            where t1.período / 100 = :year and t1.período % 100 = :month
            order by t1.período, t1.acerto DESC, t1.valor DESC
        """,
        show_spinner=False,
        ttl=3600,
        params=dict(year=year, month=month),
    )


@st.cache_data(show_spinner="**Obtendo os dados, aguarde...**")
def load_anual(year: int) -> pd.DataFrame:
    return engine.query(
        sql="""
            select t2.lançamento, t1.período, t1.acerto, t1.valor
            from espelho t1
                inner join lançamento t2
                    on t2.id_lançamento = t1.id_lançamento
            where t1.período / 100 = :year
            order by t1.período, t1.acerto DESC, t1.valor DESC
        """,
        show_spinner=False,
        ttl=3600,
        params=dict(year=year),
    )


tab1, tab2 = st.tabs(["**Mensal**", "**Anual**"])

with tab1:
    col1, col2 = st.columns([1, 2], border=True)

    with col1:
        mes = st.slider(label="**Mês:**", min_value=1, max_value=12, value=date.today().month)

        ano = st.columns(3)[0].selectbox(label="**Ano:**", options=range(date.today().year, 2004, -1))

    with col2:
        df1 = load_mensal(ano, mes)
        df1.columns = [str(column).capitalize() for column in df1.columns]
        df1["Período"] = pd.to_datetime(df1["Período"], format="%Y%m").dt.strftime("%B de %Y")

        st.data_editor(
            data=df1, hide_index=True, use_container_width=True,
            column_config={"Valor": st.column_config.NumberColumn(format="dollar")}
        )

with tab2:
    col1, col2 = st.columns([1, 2], border=True)

    with col1:
        anual = st.slider(label="**Ano:**", min_value=2005, max_value=date.today().year, value=date.today().year)

    with col2:
        df2 = load_anual(anual)
        df2.columns = [str(column).capitalize() for column in df2.columns]
        df2["Período"] = pd.to_datetime(df2["Período"], format="%Y%m").dt.strftime("%B de %Y")

        st.data_editor(
            data=df2, hide_index=True, use_container_width=True,
            column_config={"Valor": st.column_config.NumberColumn(format="dollar")}
        )
'''
