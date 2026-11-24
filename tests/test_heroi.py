import unittest

from rpg import config
from rpg.classes import GUERREIRO
from rpg.heroi import Heroi
from rpg.inimigos import criar_inimigo
from tests.auxiliares import RngFixo


class TestHeroi(unittest.TestCase):
    def setUp(self):
        self.heroi = Heroi("Teste", GUERREIRO)

    def test_comeca_no_nivel_1_com_atributos_da_classe(self):
        self.assertEqual(self.heroi.nivel, 1)
        self.assertEqual(self.heroi.vida, GUERREIRO.atributos.vida_max)
        self.assertEqual(self.heroi.ataque, GUERREIRO.atributos.ataque)

    def test_sobe_de_nivel_e_melhora_atributos(self):
        ataque_antes = self.heroi.ataque
        niveis = self.heroi.ganhar_xp(config.XP_POR_NIVEL)
        self.assertEqual(niveis, 1)
        self.assertEqual(self.heroi.nivel, 2)
        self.assertEqual(self.heroi.ataque, ataque_antes + config.BONUS_NIVEL_ATAQUE)
        self.assertEqual(self.heroi.vida, self.heroi.vida_max)

    def test_pode_subir_varios_niveis_de_uma_vez(self):
        # Nível 1->2 custa 1x, 2->3 custa 2x: total 3x
        niveis = self.heroi.ganhar_xp(config.XP_POR_NIVEL * 3)
        self.assertEqual(niveis, 2)
        self.assertEqual(self.heroi.nivel, 3)
        self.assertEqual(self.heroi.xp, 0)

    def test_habilidade_entra_em_recarga(self):
        inimigo = criar_inimigo(1, RngFixo())
        self.heroi.usar_habilidade(inimigo, RngFixo())
        self.assertFalse(self.heroi.habilidade_pronta)
        with self.assertRaises(RuntimeError):
            self.heroi.usar_habilidade(inimigo, RngFixo())

    def test_recarga_diminui_a_cada_rodada(self):
        self.heroi.usar_habilidade(criar_inimigo(1, RngFixo()), RngFixo())
        for _ in range(GUERREIRO.habilidade.recarga):
            self.heroi.reduzir_recarga()
        self.assertTrue(self.heroi.habilidade_pronta)


if __name__ == "__main__":
    unittest.main()
