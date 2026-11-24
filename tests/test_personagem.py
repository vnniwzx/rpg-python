import unittest

from rpg import config
from rpg.personagem import Atributos, Personagem
from tests.auxiliares import RngFixo


def criar(vida=100, ataque=10, defesa=0):
    return Personagem("Teste", Atributos(vida_max=vida, ataque=ataque, defesa=defesa))


class TestPersonagem(unittest.TestCase):
    def test_receber_dano_reduz_vida(self):
        p = criar(vida=50)
        self.assertEqual(p.receber_dano(20), 20)
        self.assertEqual(p.vida, 30)

    def test_vida_nunca_fica_negativa(self):
        p = criar(vida=10)
        self.assertEqual(p.receber_dano(999), 10)
        self.assertEqual(p.vida, 0)
        self.assertFalse(p.esta_vivo)

    def test_cura_nao_passa_do_maximo(self):
        p = criar(vida=100)
        p.receber_dano(30)
        self.assertEqual(p.curar(500), 30)
        self.assertEqual(p.vida, 100)

    def test_ataque_desconta_defesa(self):
        atacante, alvo = criar(ataque=15), criar(defesa=5)
        resultado = atacante.atacar(alvo, RngFixo())
        self.assertEqual(resultado.dano, 10)
        self.assertFalse(resultado.critico)

    def test_ataque_causa_no_minimo_1_de_dano(self):
        atacante, alvo = criar(ataque=1), criar(defesa=50)
        self.assertEqual(atacante.atacar(alvo, RngFixo()).dano, 1)

    def test_critico_multiplica_dano(self):
        atacante, alvo = criar(ataque=10), criar()
        resultado = atacante.atacar(alvo, RngFixo(random=0.0))
        self.assertTrue(resultado.critico)
        self.assertEqual(resultado.dano, round(10 * config.MULTIPLICADOR_CRITICO))

    def test_ignora_defesa(self):
        atacante, alvo = criar(ataque=10), criar(defesa=8)
        self.assertEqual(atacante.atacar(alvo, RngFixo(), ignora_defesa=True).dano, 10)


if __name__ == "__main__":
    unittest.main()
