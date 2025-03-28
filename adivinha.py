# %%
import random

print("*************************************")
print("* Bem vindo ao jogo de Adivinhação! *")
print("*************************************\n")

print("Qual o nível de dificuldade?")
print("(1) Fácil (2) Médio (3) Difícil")

level = int(input("Defina o nível: "))

total_de_tentativas = 20 if level == 1 else 10 if level == 2 else 5

pontos = 1000
secreto = random.randrange(1, 101)

for rodada in range(1, total_de_tentativas + 1):
    print(f"\nTentativa {rodada} de {total_de_tentativas}.")

    chute = int(input("Digite um número entre 1 e 100: "))

    if not 1 <= chute <= 100:
        print("Você deve digitar um número entre 1 e 100!")
        continue

    acertou = chute == secreto
    maior = chute > secreto
    menor = chute < secreto

    if acertou:
        print(f"Você acertou e fez {pontos} pontos!")
        break
    else:
        pontos -= abs(secreto - chute)

        if maior:
            print("Seu chute foi maior que o número secreto.")
            if rodada == total_de_tentativas:
                print(f"\nO número secreto era {secreto} e você fez {pontos} pontos.")
        elif menor:
            print("Errou! Seu chute foi menor do que o número secreto.")
            if rodada == total_de_tentativas:
                print(f"\nO número secreto era {secreto} e você fez {pontos} pontos.")

print("Fim do jogo!")

# %%
import numpy as np

tentativas = 10

print(f"Adivinhe o número entre 1 e 50. Você tem até {tentativas} tentativas de acertar.")

numero_secreto = np.random.randint(1, 50)

while tentativas > 0:
    tentativas -= 1
    chute = int(input(">>> Adivinha um número secreto: "))
    if chute > numero_secreto:
        print("O número secreto é menor!")
    elif chute < numero_secreto:
        print("O número secreto é maior!")
    else:
        print("Parabéns! Acertou o número secreto!")

    if tentativas >= 0:
        print(f"Tentativas restantes: {tentativas}.")

if tentativas == 0:
    print("=" * 38)
    print("Infelizmente suas tentativas acabaram...")
    print(f"O número secreto é {secreto}.")
