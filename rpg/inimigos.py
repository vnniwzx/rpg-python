"""Inimigos e a fábrica que os cria de acordo com o andar da masmorra."""

from __future__ import annotations

import random
from dataclasses import dataclass

from rpg import config
from rpg.personagem import Atributos, Personagem


class Inimigo(Personagem):
    def __init__(
        self,
        nome: str,
        atributos: Atributos,
        xp_recompensa: int,
        ouro_recompensa: int,
        chefe: bool = False,
    ) -> None:
        super().__init__(nome, atributos)
        self.xp_recompensa = xp_recompensa
        self.ouro_recompensa = ouro_recompensa
        self.chefe = chefe


@dataclass(frozen=True)
class ModeloInimigo:
    """Molde usado para gerar inimigos.

    Para adicionar um inimigo novo, basta acrescentar um ModeloInimigo
    em MODELOS_COMUNS.
    """

    nome: str
    atributos: Atributos
    xp: int
    ouro: int


MODELOS_COMUNS: tuple[ModeloInimigo, ...] = (
    ModeloInimigo("Slime", Atributos(vida_max=35, ataque=10, defesa=1), xp=25, ouro=8),
    ModeloInimigo("Goblin", Atributos(vida_max=45, ataque=12, defesa=3), xp=35, ouro=15),
    ModeloInimigo("Esqueleto", Atributos(vida_max=55, ataque=13, defesa=5), xp=45, ouro=18),
    ModeloInimigo("Lobo Sombrio", Atributos(vida_max=50, ataque=15, defesa=2), xp=45, ouro=12),
)

MODELO_CHEFE = ModeloInimigo(
    "Dragão Ancião", Atributos(vida_max=280, ataque=28, defesa=10), xp=500, ouro=300
)


def _escalar(valor: int, andar: int) -> int:
    """Deixa o inimigo mais forte quanto mais fundo na masmorra."""
    return round(valor * (1 + config.ESCALA_POR_ANDAR * (andar - 1)))


def criar_inimigo(andar: int, rng: random.Random) -> Inimigo:
    """Sorteia um inimigo comum com atributos ajustados ao andar."""
    modelo = rng.choice(MODELOS_COMUNS)
    base = modelo.atributos
    atributos = Atributos(
        vida_max=_escalar(base.vida_max, andar),
        ataque=_escalar(base.ataque, andar),
        defesa=_escalar(base.defesa, andar),
    )
    return Inimigo(
        nome=modelo.nome,
        atributos=atributos,
        xp_recompensa=_escalar(modelo.xp, andar),
        ouro_recompensa=_escalar(modelo.ouro, andar),
    )


def criar_chefe() -> Inimigo:
    m = MODELO_CHEFE
    return Inimigo(m.nome, m.atributos, m.xp, m.ouro, chefe=True)
