"""Fluxo principal: criação do herói, exploração da masmorra e final."""

from __future__ import annotations

import random

from rpg import config, itens, ui
from rpg.classes import CLASSES_DISPONIVEIS
from rpg.combate import Batalha, Resultado
from rpg.heroi import Heroi
from rpg.inimigos import Inimigo, criar_chefe, criar_inimigo
from rpg.loja import abrir_loja

# Itens que podem cair dos inimigos (pesos: mais comuns aparecem mais).
DROPS = (itens.pocao_pequena, itens.pocao_grande, itens.elixir_de_forca)
PESOS_DROPS = (70, 25, 5)


class SairDoJogo(Exception):
    """Lançada quando o jogador escolhe sair no meio da partida."""


class Jogo:
    def __init__(self, rng: random.Random | None = None) -> None:
        self.rng = rng or random.Random()
        self.heroi: Heroi | None = None
        self.inimigos_derrotados = 0

    def iniciar(self) -> None:
        ui.limpar_tela()
        self._mostrar_introducao()
        self.heroi = self._criar_heroi()
        try:
            venceu = self._explorar_masmorra()
        except SairDoJogo:
            ui.mensagem("\nVocê deixou a masmorra. Até a próxima!")
            return
        self._mostrar_final(venceu)

    # --- Etapas do jogo -----------------------------------------------------

    def _mostrar_introducao(self) -> None:
        ui.titulo("A Masmorra do Dragão")
        ui.mensagem(
            f"Desça {config.TOTAL_ANDARES} andares, derrote os monstros e\n"
            "enfrente o Dragão Ancião no fundo da masmorra."
        )

    def _criar_heroi(self) -> Heroi:
        nome = ui.perguntar_texto("\nQual o nome do seu herói?", padrao="Herói")
        opcoes = [f"{c.nome} - {c.descricao}" for c in CLASSES_DISPONIVEIS]
        classe = CLASSES_DISPONIVEIS[ui.escolher_opcao("Escolha sua classe:", opcoes)]

        heroi = Heroi(nome, classe)
        for _ in range(config.POCOES_INICIAIS):
            heroi.inventario.adicionar(itens.pocao_pequena())

        ui.mensagem(f"\n{nome}, o {classe.nome}, entra na masmorra...")
        ui.mensagem(f"Habilidade especial: {classe.habilidade.nome} - {classe.habilidade.descricao}")
        ui.pausar()
        return heroi

    def _explorar_masmorra(self) -> bool:
        """Retorna True se o herói derrotou o chefe."""
        for andar in range(1, config.TOTAL_ANDARES + 1):
            ui.limpar_tela()
            ui.titulo(f"Andar {andar} de {config.TOTAL_ANDARES}")

            if andar == config.TOTAL_ANDARES:
                ui.mensagem("Um rugido ecoa pela caverna... O CHEFE apareceu!")
                ui.pausar()
                return self._lutar(criar_chefe(), pode_fugir=False) == Resultado.VITORIA

            vitorias = 0
            while vitorias < config.BATALHAS_POR_ANDAR:
                inimigo = criar_inimigo(andar, self.rng)
                ui.mensagem(f"\nUm {inimigo.nome} aparece!")
                resultado = self._lutar(inimigo)
                if resultado == Resultado.DERROTA:
                    return False
                if resultado == Resultado.VITORIA:
                    vitorias += 1

            self._descansar()
            self._menu_entre_andares()
        return True

    def _lutar(self, inimigo: Inimigo, pode_fugir: bool = True) -> Resultado:
        resultado = Batalha(self.heroi, inimigo, self.rng, pode_fugir).executar()
        if resultado == Resultado.VITORIA:
            self._recompensar(inimigo)
        return resultado

    def _recompensar(self, inimigo: Inimigo) -> None:
        heroi = self.heroi
        self.inimigos_derrotados += 1
        heroi.ouro += inimigo.ouro_recompensa
        ui.mensagem(f"+{inimigo.xp_recompensa} XP  |  +{inimigo.ouro_recompensa} de ouro")

        niveis = heroi.ganhar_xp(inimigo.xp_recompensa)
        if niveis:
            ui.mensagem(f"*** SUBIU PARA O NÍVEL {heroi.nivel}! Vida restaurada. ***")

        if self.rng.random() < config.CHANCE_DROP_ITEM:
            fabrica = self.rng.choices(DROPS, weights=PESOS_DROPS)[0]
            item = fabrica()
            heroi.inventario.adicionar(item)
            ui.mensagem(f"O inimigo deixou cair: {item.nome}!")
        ui.pausar()

    def _descansar(self) -> None:
        cura = self.heroi.curar(round(self.heroi.vida_max * config.CURA_DESCANSO))
        if cura:
            ui.mensagem(f"\nVocê descansa antes de descer. Recuperou {cura} de vida.")
        else:
            ui.mensagem("\nVocê descansa um pouco. Sua vida já está cheia.")

    def _menu_entre_andares(self) -> None:
        opcoes = ["Descer para o próximo andar", "Ver status", "Usar item", "Loja", "Sair do jogo"]
        while True:
            escolha = ui.escolher_opcao("O que deseja fazer?", opcoes)
            if escolha == 0:
                return
            if escolha == 1:
                self._mostrar_status()
            elif escolha == 2:
                self._usar_item_fora_de_combate()
            elif escolha == 3:
                abrir_loja(self.heroi)
            elif escolha == 4:
                raise SairDoJogo

    # --- Auxiliares ---------------------------------------------------------

    def _mostrar_status(self) -> None:
        h = self.heroi
        ui.titulo("Status")
        ui.mostrar_vida(h)
        ui.mensagem(f"Classe: {h.classe.nome}   Nível: {h.nivel}   XP: {h.xp}/{h.xp_proximo_nivel}")
        ui.mensagem(f"Ataque: {h.ataque}   Defesa: {h.defesa}   Ouro: {h.ouro}")
        ui.mensagem("Inventário: " + (", ".join(i.nome for i in h.inventario.itens) or "vazio"))

    def _usar_item_fora_de_combate(self) -> None:
        inventario = self.heroi.inventario
        if inventario.vazio:
            ui.mensagem("Seu inventário está vazio!")
            return
        opcoes = [str(item) for item in inventario.itens] + ["Voltar"]
        escolha = ui.escolher_opcao("Qual item?", opcoes)
        if escolha < len(opcoes) - 1:
            ui.mensagem(inventario.usar(escolha, self.heroi))

    def _mostrar_final(self, venceu: bool) -> None:
        h = self.heroi
        if venceu:
            ui.titulo("Vitória!")
            ui.mensagem(f"{h.nome} derrotou o Dragão Ancião e se tornou uma lenda!")
        else:
            ui.titulo("Fim de jogo")
            ui.mensagem("A masmorra fez mais uma vítima...")
        ui.mensagem(
            f"\nNível final: {h.nivel}  |  Inimigos derrotados: {self.inimigos_derrotados}"
            f"  |  Ouro: {h.ouro}"
        )
