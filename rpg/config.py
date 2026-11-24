"""Constantes de balanceamento do jogo.

Quer deixar o jogo mais fácil ou mais difícil? Mude os valores aqui.
Nenhum outro arquivo precisa ser alterado.
"""

# --- Masmorra ---------------------------------------------------------------
TOTAL_ANDARES = 5          # o último andar sempre tem o chefe
BATALHAS_POR_ANDAR = 2     # inimigos comuns a vencer em cada andar
ESCALA_POR_ANDAR = 0.20    # +20% nos atributos dos inimigos a cada andar
CURA_DESCANSO = 0.30       # % da vida máxima recuperada ao fim de cada andar

# --- Combate ----------------------------------------------------------------
CHANCE_CRITICO = 0.10
MULTIPLICADOR_CRITICO = 2.0
VARIACAO_DANO = 2          # o dano varia entre -2 e +2
CHANCE_FUGA = 0.5

# --- Progressão do herói ----------------------------------------------------
XP_POR_NIVEL = 80          # XP necessária = XP_POR_NIVEL * nível atual
BONUS_NIVEL_VIDA = 15
BONUS_NIVEL_ATAQUE = 3
BONUS_NIVEL_DEFESA = 2

# --- Itens ------------------------------------------------------------------
POCOES_INICIAIS = 2
CHANCE_DROP_ITEM = 0.40
