"""O personagem controlado pelo jogador."""

from __future__ import annotations

import random

from rpg import config
from rpg.classes import ClasseHeroi, Habilidade
from rpg.inventario import Inventario
from rpg.personagem import Personagem, ResultadoAtaque


class Heroi(Personagem):
    def __init__(self, nome: str, classe: ClasseHeroi) -> None:
        super().__init__(nome, classe.atributos)
        self.classe = classe
        self.nivel = 1
        self.xp = 0
        self.ouro = 0
        self.inventario = Inventario()
        self._recarga_restante = 0

    # --- Habilidade especial ------------------------------------------------

    @property
    def habilidade(self) -> Habilidade:
        return self.classe.habilidade

    @property
    def recarga_restante(self) -> int:
        return self._recarga_restante

    @property
    def habilidade_pronta(self) -> bool:
        return self._recarga_restante == 0

    def usar_habilidade(self, alvo: Personagem, rng: random.Random) -> ResultadoAtaque:
        if not self.habilidade_pronta:
            raise RuntimeError(f"{self.habilidade.nome} ainda está recarregando.")
        resultado = self.atacar(
            alvo,
            rng,
            multiplicador=self.habilidade.multiplicador,
            ignora_defesa=self.habilidade.ignora_defesa,
        )
        self._recarga_restante = self.habilidade.recarga
        return resultado

    def reduzir_recarga(self) -> None:
        """Chamado ao fim de cada rodada de combate."""
        if self._recarga_restante > 0:
            self._recarga_restante -= 1

    def resetar_recarga(self) -> None:
        """Toda batalha começa com a habilidade pronta."""
        self._recarga_restante = 0

    # --- Progressão ---------------------------------------------------------

    @property
    def xp_proximo_nivel(self) -> int:
        return config.XP_POR_NIVEL * self.nivel

    def ganhar_xp(self, quantidade: int) -> int:
        """Adiciona XP e sobe de nível quantas vezes for preciso.

        Retorna quantos níveis foram ganhos (0 se nenhum).
        """
        self.xp += quantidade
        niveis_ganhos = 0
        while self.xp >= self.xp_proximo_nivel:
            self.xp -= self.xp_proximo_nivel
            self._subir_nivel()
            niveis_ganhos += 1
        return niveis_ganhos

    def _subir_nivel(self) -> None:
        self.nivel += 1
        self.vida_max += config.BONUS_NIVEL_VIDA
        self.ataque += config.BONUS_NIVEL_ATAQUE
        self.defesa += config.BONUS_NIVEL_DEFESA
        self.vida = self.vida_max  # subir de nível cura totalmente
