"""Itens consumíveis.

Todo item herda de `Item` e implementa `usar()`. Assim o inventário e o
combate não precisam saber qual item é qual: só chamam `item.usar(alvo)`
(isso é polimorfismo).
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from rpg.personagem import Personagem


class Item(ABC):
    def __init__(self, nome: str, descricao: str, preco: int) -> None:
        self.nome = nome
        self.descricao = descricao
        self.preco = preco

    @abstractmethod
    def usar(self, alvo: Personagem) -> str:
        """Aplica o efeito no alvo e retorna uma mensagem descrevendo o que aconteceu."""

    def __str__(self) -> str:
        return f"{self.nome} - {self.descricao}"


class Pocao(Item):
    """Recupera vida."""

    def __init__(self, nome: str, cura: int, preco: int) -> None:
        super().__init__(nome, f"Recupera {cura} de vida.", preco)
        self.cura = cura

    def usar(self, alvo: Personagem) -> str:
        curado = alvo.curar(self.cura)
        return f"{alvo.nome} bebeu {self.nome} e recuperou {curado} de vida."


class Elixir(Item):
    """Aumenta o ataque permanentemente."""

    def __init__(self, nome: str, bonus_ataque: int, preco: int) -> None:
        super().__init__(nome, f"+{bonus_ataque} de ataque permanente.", preco)
        self.bonus_ataque = bonus_ataque

    def usar(self, alvo: Personagem) -> str:
        alvo.ataque += self.bonus_ataque
        return f"{alvo.nome} sente o poder crescer! Ataque +{self.bonus_ataque}."


# --- Fábricas: sempre criam uma instância nova -----------------------------

def pocao_pequena() -> Pocao:
    return Pocao("Poção de Vida", cura=40, preco=20)


def pocao_grande() -> Pocao:
    return Pocao("Poção Grande", cura=90, preco=45)


def elixir_de_forca() -> Elixir:
    return Elixir("Elixir de Força", bonus_ataque=3, preco=80)
