"""Inventário do herói."""

from __future__ import annotations

from rpg.itens import Item
from rpg.personagem import Personagem


class Inventario:
    def __init__(self) -> None:
        self._itens: list[Item] = []

    @property
    def itens(self) -> tuple[Item, ...]:
        """Cópia somente-leitura dos itens (ninguém mexe na lista por fora)."""
        return tuple(self._itens)

    @property
    def vazio(self) -> bool:
        return not self._itens

    def adicionar(self, item: Item) -> None:
        self._itens.append(item)

    def usar(self, indice: int, alvo: Personagem) -> str:
        """Consome o item da posição `indice` no alvo e retorna a mensagem do efeito."""
        if not 0 <= indice < len(self._itens):
            raise IndexError(f"Não existe item na posição {indice}.")
        item = self._itens.pop(indice)
        return item.usar(alvo)

    def __len__(self) -> int:
        return len(self._itens)
