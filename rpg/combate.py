"""Sistema de batalha por turnos entre o herói e um inimigo."""

from __future__ import annotations

import random
from enum import Enum, auto

from rpg import config, ui
from rpg.heroi import Heroi
from rpg.inimigos import Inimigo
from rpg.personagem import Personagem, ResultadoAtaque


class Resultado(Enum):
    VITORIA = auto()
    DERROTA = auto()
    FUGA = auto()


class Batalha:
    def __init__(
        self,
        heroi: Heroi,
        inimigo: Inimigo,
        rng: random.Random,
        pode_fugir: bool = True,
    ) -> None:
        self.heroi = heroi
        self.inimigo = inimigo
        self.rng = rng
        self.pode_fugir = pode_fugir

    def executar(self) -> Resultado:
        """Roda a batalha até alguém cair ou o herói fugir."""
        ui.titulo(f"{self.heroi.nome} vs {self.inimigo.nome}")
        self.heroi.resetar_recarga()

        while True:
            self._mostrar_estado()

            if self._turno_heroi():
                ui.mensagem("Você fugiu da batalha!")
                return Resultado.FUGA

            if not self.inimigo.esta_vivo:
                ui.mensagem(f"\n{self.inimigo.nome} foi derrotado!")
                return Resultado.VITORIA

            self._turno_inimigo()
            if not self.heroi.esta_vivo:
                ui.mensagem(f"\n{self.heroi.nome} caiu em batalha...")
                return Resultado.DERROTA

            self.heroi.reduzir_recarga()

    # --- Turnos -------------------------------------------------------------

    def _turno_heroi(self) -> bool:
        """Pede uma ação até que uma seja realizada. Retorna True se o herói fugiu."""
        while True:
            acao = ui.escolher_opcao("O que você vai fazer?", self._opcoes_de_acao())

            if acao == 0:
                self._anunciar_ataque(self.heroi, self.heroi.atacar(self.inimigo, self.rng))
                return False
            if acao == 1 and self._usar_habilidade():
                return False
            if acao == 2 and self._usar_item():
                return False
            if acao == 3:
                fugiu = self._tentar_fugir()
                if fugiu is not None:
                    return fugiu
            # Se chegou aqui, a ação não foi possível: pergunta de novo.

    def _turno_inimigo(self) -> None:
        self._anunciar_ataque(self.inimigo, self.inimigo.atacar(self.heroi, self.rng))

    # --- Ações do herói -----------------------------------------------------

    def _opcoes_de_acao(self) -> list[str]:
        h = self.heroi
        if h.habilidade_pronta:
            status = "pronta"
        else:
            status = f"recarregando: {h.recarga_restante} turno(s)"
        return [
            "Atacar",
            f"{h.habilidade.nome} ({status})",
            f"Usar item ({len(h.inventario)})",
            "Fugir",
        ]

    def _usar_habilidade(self) -> bool:
        if not self.heroi.habilidade_pronta:
            ui.mensagem("A habilidade ainda está recarregando!")
            return False
        ui.mensagem(f"\n{self.heroi.nome} usa {self.heroi.habilidade.nome}!")
        self._anunciar_ataque(self.heroi, self.heroi.usar_habilidade(self.inimigo, self.rng))
        return True

    def _usar_item(self) -> bool:
        inventario = self.heroi.inventario
        if inventario.vazio:
            ui.mensagem("Seu inventário está vazio!")
            return False

        opcoes = [str(item) for item in inventario.itens] + ["Voltar"]
        escolha = ui.escolher_opcao("Qual item?", opcoes)
        if escolha == len(opcoes) - 1:
            return False

        ui.mensagem(inventario.usar(escolha, self.heroi))
        return True

    def _tentar_fugir(self) -> bool | None:
        """True = fugiu, False = falhou (perde o turno), None = não é possível fugir."""
        if not self.pode_fugir:
            ui.mensagem("Não há como fugir desta batalha!")
            return None
        if self.rng.random() < config.CHANCE_FUGA:
            return True
        ui.mensagem("Você tentou fugir, mas não conseguiu!")
        return False

    # --- Exibição -----------------------------------------------------------

    def _mostrar_estado(self) -> None:
        ui.separador()
        ui.mostrar_vida(self.heroi)
        ui.mostrar_vida(self.inimigo)
        ui.separador()

    @staticmethod
    def _anunciar_ataque(atacante: Personagem, resultado: ResultadoAtaque) -> None:
        texto = f"{atacante.nome} causou {resultado.dano} de dano."
        if resultado.critico:
            texto = "CRÍTICO! " + texto
        ui.mensagem(texto)
