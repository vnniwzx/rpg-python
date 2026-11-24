"""Classe base para tudo que luta: heróis e inimigos."""

from __future__ import annotations

import random
from dataclasses import dataclass

from rpg import config


@dataclass(frozen=True)
class Atributos:
    """Atributos iniciais de um personagem."""

    vida_max: int
    ataque: int
    defesa: int


@dataclass(frozen=True)
class ResultadoAtaque:
    """O que aconteceu em um ataque (usado pela interface para exibir mensagens)."""

    dano: int
    critico: bool


class Personagem:
    """Qualquer criatura que tem vida, ataca e recebe dano."""

    def __init__(self, nome: str, atributos: Atributos) -> None:
        self.nome = nome
        self.vida_max = atributos.vida_max
        self.vida = atributos.vida_max
        self.ataque = atributos.ataque
        self.defesa = atributos.defesa

    @property
    def esta_vivo(self) -> bool:
        return self.vida > 0

    def receber_dano(self, quantidade: int) -> int:
        """Reduz a vida e retorna o dano realmente sofrido (a vida nunca fica negativa)."""
        dano_real = min(max(0, quantidade), self.vida)
        self.vida -= dano_real
        return dano_real

    def curar(self, quantidade: int) -> int:
        """Recupera vida sem passar do máximo. Retorna quanto foi curado de fato."""
        cura_real = min(max(0, quantidade), self.vida_max - self.vida)
        self.vida += cura_real
        return cura_real

    def atacar(
        self,
        alvo: Personagem,
        rng: random.Random,
        multiplicador: float = 1.0,
        ignora_defesa: bool = False,
    ) -> ResultadoAtaque:
        """Calcula o dano contra o alvo, aplica e retorna o resultado.

        Fórmula: (ataque - defesa do alvo + variação) * multiplicador * crítico.
        Todo ataque causa no mínimo 1 de dano.
        """
        defesa = 0 if ignora_defesa else alvo.defesa
        variacao = rng.randint(-config.VARIACAO_DANO, config.VARIACAO_DANO)
        critico = rng.random() < config.CHANCE_CRITICO

        dano = (self.ataque - defesa + variacao) * multiplicador
        if critico:
            dano *= config.MULTIPLICADOR_CRITICO

        dano_final = max(1, round(dano))
        return ResultadoAtaque(dano=alvo.receber_dano(dano_final), critico=critico)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.nome!r}, vida={self.vida}/{self.vida_max})"
