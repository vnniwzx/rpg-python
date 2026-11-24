"""Tudo que aparece na tela ou lê o teclado fica aqui.

Separar a interface da lógica permite trocar o terminal por outra coisa
(uma janela com pygame, um bot do Discord...) sem mexer nas regras do jogo.
"""

from __future__ import annotations

import os
from typing import Sequence

from rpg.personagem import Personagem

LARGURA = 52


def limpar_tela() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def titulo(texto: str) -> None:
    print()
    print("=" * LARGURA)
    print(texto.upper().center(LARGURA))
    print("=" * LARGURA)


def separador() -> None:
    print("-" * LARGURA)


def mensagem(texto: str = "") -> None:
    print(texto)


def pausar() -> None:
    input("\nPressione ENTER para continuar...")


def barra_vida(atual: int, maximo: int, tamanho: int = 20) -> str:
    """Ex.: [##########----------] 50/100"""
    cheios = round(tamanho * atual / maximo) if maximo else 0
    return f"[{'#' * cheios}{'-' * (tamanho - cheios)}] {atual}/{maximo}"


def mostrar_vida(personagem: Personagem) -> None:
    print(f"{personagem.nome:<16} {barra_vida(personagem.vida, personagem.vida_max)}")


def perguntar_texto(pergunta: str, padrao: str = "") -> str:
    resposta = input(f"{pergunta} ").strip()
    return resposta or padrao


def escolher_opcao(pergunta: str, opcoes: Sequence[str]) -> int:
    """Mostra opções numeradas e devolve o índice escolhido (começando em 0).

    Continua perguntando até o jogador digitar um número válido.
    """
    print(f"\n{pergunta}")
    for numero, opcao in enumerate(opcoes, start=1):
        print(f"  {numero}) {opcao}")

    while True:
        resposta = input("> ").strip()
        if resposta.isdigit() and 1 <= int(resposta) <= len(opcoes):
            return int(resposta) - 1
        print(f"Opção inválida. Digite um número de 1 a {len(opcoes)}.")
