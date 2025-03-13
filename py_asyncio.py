# %%
import asyncio


async def temporizador():
    print("Iniciando temporizador...")
    await asyncio.sleep(3)
    print("Tempo finalizado após 3 segundos!")


asyncio.run(temporizador())

# %%
import asyncio


async def baixar_dados():
    print("Iniciando download...")
    await asyncio.sleep(2)
    print("Download concluído!")


async def analisar_dados():
    print("Iniciando análise de dados...")
    await asyncio.sleep(3)
    print("Análise de dados concluída!")


async def main():
    await asyncio.gather(baixar_dados(), analisar_dados())


asyncio.run(main())

# %%
import asyncio
import math

number = [5, 3, 7, 4, 6]


async def calcular_fatorial(n):
    await asyncio.sleep(n)
    print(f"Fatorial de {n} = {math.factorial(n)}")


async def main():
    tarefas = (asyncio.create_task(calcular_fatorial(n)) for n in number)
    await asyncio.gather(*tarefas)


asyncio.run(main())

# %%
import asyncio

usuarios = [
    {"nome": "Ana", "vip": True, "notificações_ativadas": True},
    {"nome": "João", "vip": False, "notificações_ativadas": True},
    {"nome": "Carla", "vip": False, "notificações_ativadas": False},
]


async def enviar_notificacao(usuario):
    if not usuario["notificações_ativadas"]:
        print(f"{usuario['nome']} desativou as notificações. Nada foi enviado.")
        return

    if usuario["vip"]:
        print(f"Notificação VIP para {usuario['nome']} enviada!")

    print(f"Notificação normal para {usuario['nome']} enviada!")


async def main():
    print("Enviando notificações...")
    tarefas = (asyncio.create_task(enviar_notificacao(u)) for u in usuarios)
    await asyncio.gather(*tarefas)
    print("Todas as notificações foram processadas!")


asyncio.run(main())

# %%
import asyncio

pedidos = [
    {"id": 101, "pagamento_aprovado": True, "estoque_disponível": True},
    {"id": 102, "pagamento_aprovado": True, "estoque_disponível": False},
    {"id": 103, "pagamento_aprovado": False, "estoque_disponível": True},
    {"id": 104, "pagamento_aprovado": True, "estoque_disponível": True},
    {"id": 105, "pagamento_aprovado": False, "estoque_disponível": False},
]


async def verificar_pagamento(pedido):
    await asyncio.sleep(1)
    if pedido["pagamento_aprovado"]:
        print(f"Pagamento aprovado para pedido #{pedido['id']}.\n")
        return True
    else:
        print(f"Pagamento recusado para pedido #{pedido['id']}. Pedido cancelado.\n")
        return False


async def verificar_estoque(pedido):
    await asyncio.sleep(1)
    if pedido["estoque_disponível"]:
        print(f"Estoque disponível para pedido #{pedido['id']}.\n")
        return True
    else:
        print(f"Estoque indisponível para pedido #{pedido['id']}. Pedido cancelado.\n")
        return False


async def processar_pedido(pedido):
    print(f"Processando pedido #{pedido['id']}...\n")

    pagamento_ok = await verificar_pagamento(pedido)
    if not pagamento_ok:
        return
    estoque_ok = await verificar_estoque(pedido)
    if not estoque_ok:
        return
    print(f"Pedido #{pedido['id']} confirmado! Enviado para entrega.\n")


async def main():
    for pedido in pedidos:
        await processar_pedido(pedido)
    print("\nTodos os pedidos foram processados!\n")


asyncio.run(main())

# %%
import asyncio

cursos = {
    "Python Avançado": {"vagas": 2, "inscritos": []},
    "Java para Iniciantes": {"vagas": 1, "inscritos": []},
    "Machine Learning": {"vagas": 0, "inscritos": []},
}

alunos = [
    {"nome": "Alice", "curso": "Python Avançado"},
    {"nome": "Bruno", "curso": "Python Avançado"},
    {"nome": "Carlos", "curso": "Java para Iniciantes"},
    {"nome": "Daniela", "curso": "Machine Learning"},
    {"nome": "Alice", "curso": "Python Avançado"},
]


async def inscrever_aluno(aluno):
    curso_nome = aluno["curso"]
    nome_aluno = aluno["nome"]

    print(f"Inscrevendo {nome_aluno} no curso {curso_nome}...")

    if curso_nome not in cursos:
        print(f"Erro! O curso {curso_nome} não existe.\n")
        return

    curso = cursos[curso_nome]

    if nome_aluno in curso["inscritos"]:
        print(f"{nome_aluno} já está inscrito no curso {curso_nome}! Inscrição rejeitada.\n")
        return

    if curso["vagas"] > 0:
        curso["inscritos"].append(nome_aluno)
        curso["vagas"] -= 1
        print(f"Inscrição confirmada para {nome_aluno} no curso {curso_nome}!\n")
    else:
        print(f"Turma lotada! {nome_aluno} não pôde se inscrever no curso {curso_nome}.\n")


async def main():
    tarefas = (asyncio.create_task(inscrever_aluno(a)) for a in alunos)
    await asyncio.gather(*tarefas)
    print("Todas as inscrições foram processadas!\n")


asyncio.run(main())

# %%
import asyncio


async def tarefa(numero, tempo):
    await asyncio.sleep(tempo)
    print(f"Tarefa {numero} finalizada!")


async def main():
    tempos = [3, 5, 7]
    tarefas = [asyncio.create_task(tarefa(i + 1, tempos[i])) for i in range(3)]

    while any(not t.done() for t in tarefas):
        status = ['Finalizado' if t.done() else 'Em andamento' for t in tarefas]
        print(f"Status das tarefas: {status}")
        await asyncio.sleep(1)

    await asyncio.gather(*tarefas)


asyncio.run(main())

# %%
import asyncio
import random


async def sensor_temperatura():
    while True:
        await asyncio.sleep(2)
        temp = random.randint(20, 30)
        print(f"[{2}s] Temperatura: {temp}°C")


async def sensor_umidade():
    while True:
        await asyncio.sleep(3)
        umidade = random.randint(50, 70)
        print(f"[{3}s] Umidade: {umidade}%")


async def sensor_qualidade_ar():
    while True:
        await asyncio.sleep(5)
        qualidade = random.choice(["Boa", "Regular", "Ruim"])
        print(f"[{5}s] Qualidade do ar: {qualidade}")


async def main():
    await asyncio.gather(sensor_temperatura(), sensor_umidade(), sensor_qualidade_ar())


asyncio.run(main())

# %%
import asyncio

arquivos = {
    "arquivo_1.txt": 30,
    "arquivo_2.txt": 45,
    "arquivo_3.txt": 20,
    "arquivo_4.txt": 10,
    "arquivo_5.txt": 50,
}

VELOCIDADE_DOWNLOAD = 5


async def baixar_arquivo(nome, tamanho):
    print(f"Iniciando download de {nome} (tamanho: {tamanho}MB)...")

    baixado = 0
    segundos = 0

    while baixado < tamanho:
        await asyncio.sleep(1)
        baixado += VELOCIDADE_DOWNLOAD
        baixado = min(baixado, tamanho)
        segundos += 1
        print(f"[{segundos}s] {nome}: {baixado}MB baixados")

    print(f"{nome} concluído!\n")


async def main():
    tarefas = (asyncio.create_task(baixar_arquivo(nome, tamanho)) for nome, tamanho in arquivos.items())
    await asyncio.gather(*tarefas)
    print("\nTodos os downloads foram finalizados!")


asyncio.run(main())

# %%
import asyncio
import random

jogos = [
    {"id": 1, "times": "Flamengo vs Palmeiras"},
    {"id": 2, "times": "São Paulo vs Corinthians"},
    {"id": 3, "times": "Grêmio vs Internacional"},
]


async def processar_aposta(jogo, futuro):
    tempo = random.randint(2, 8)
    print(f"Aposta no jogo {jogo['id']} ({jogo['times'][0]} vs {jogo['times'][1]}) registrada! Aguardando resultado...\n")

    await asyncio.sleep(tempo)

    resultado = random.choice([f"Vitória do {jogo['times'][0]}", f"Vitória do {jogo['times'][1]}", "Empate"])
    futuro.set_result(resultado)

    print(f"Aposta no jogo {jogo['id']} definida: {resultado} (após {tempo}s).\n")


async def main():
    futuros = [asyncio.Future() for _ in jogos]
    tarefas = ([asyncio.create_task(processar_aposta(jogos[i], futuros[i])) for i in range(len(jogos))])

    await asyncio.gather(*tarefas)

    print("Todos os resultados foram revelados!\n")


asyncio.run(main())
