"""Loja onde o herói gasta o ouro ganho nas batalhas."""

from __future__ import annotations

from typing import Callable

from rpg import itens, ui
from rpg.heroi import Heroi
from rpg.itens import Item

# Cada entrada é uma função que cria o item. Assim cada compra gera um item novo.
CATALOGO: tuple[Callable[[], Item], ...] = (
    itens.pocao_pequena,
    itens.pocao_grande,
    itens.elixir_de_forca,
)


def comprar(heroi: Heroi, fabrica: Callable[[], Item]) -> str:
    """Tenta comprar um item. Retorna a mensagem do resultado."""
    item = fabrica()
    if heroi.ouro < item.preco:
        return f"Ouro insuficiente! Você tem {heroi.ouro} e {item.nome} custa {item.preco}."
    heroi.ouro -= item.preco
    heroi.inventario.adicionar(item)
    return f"Você comprou {item.nome}!"


def abrir_loja(heroi: Heroi) -> None:
    ui.titulo("Loja do Mercador")
    produtos = [fabrica() for fabrica in CATALOGO]

    while True:
        ui.mensagem(f"\nSeu ouro: {heroi.ouro}")
        opcoes = [f"{p} ({p.preco} de ouro)" for p in produtos] + ["Sair da loja"]
        escolha = ui.escolher_opcao("O que deseja comprar?", opcoes)
        if escolha == len(opcoes) - 1:
            return
        ui.mensagem(comprar(heroi, CATALOGO[escolha]))
