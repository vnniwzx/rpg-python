import unittest

from rpg import itens
from rpg.classes import MAGO
from rpg.heroi import Heroi
from rpg.loja import comprar


class TestInventarioEItens(unittest.TestCase):
    def setUp(self):
        self.heroi = Heroi("Teste", MAGO)

    def test_pocao_cura_e_some_do_inventario(self):
        self.heroi.receber_dano(50)
        self.heroi.inventario.adicionar(itens.pocao_pequena())
        self.heroi.inventario.usar(0, self.heroi)
        self.assertEqual(self.heroi.vida, self.heroi.vida_max - 10)
        self.assertTrue(self.heroi.inventario.vazio)

    def test_elixir_aumenta_ataque(self):
        ataque_antes = self.heroi.ataque
        elixir = itens.elixir_de_forca()
        elixir.usar(self.heroi)
        self.assertEqual(self.heroi.ataque, ataque_antes + elixir.bonus_ataque)

    def test_usar_indice_invalido_gera_erro(self):
        with self.assertRaises(IndexError):
            self.heroi.inventario.usar(0, self.heroi)


class TestLoja(unittest.TestCase):
    def setUp(self):
        self.heroi = Heroi("Teste", MAGO)

    def test_compra_com_ouro_suficiente(self):
        self.heroi.ouro = 100
        comprar(self.heroi, itens.pocao_pequena)
        self.assertEqual(self.heroi.ouro, 100 - itens.pocao_pequena().preco)
        self.assertEqual(len(self.heroi.inventario), 1)

    def test_compra_sem_ouro_nao_faz_nada(self):
        self.heroi.ouro = 0
        comprar(self.heroi, itens.elixir_de_forca)
        self.assertEqual(self.heroi.ouro, 0)
        self.assertTrue(self.heroi.inventario.vazio)


if __name__ == "__main__":
    unittest.main()
