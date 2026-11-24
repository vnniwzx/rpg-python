import unittest
from unittest.mock import patch

from rpg.classes import GUERREIRO
from rpg.combate import Batalha, Resultado
from rpg.heroi import Heroi
from rpg.inimigos import Inimigo
from rpg.personagem import Atributos
from tests.auxiliares import RngFixo


def inimigo_fraco():
    return Inimigo("Rato", Atributos(vida_max=10, ataque=1, defesa=0), 5, 1)


def inimigo_forte():
    return Inimigo("Titã", Atributos(vida_max=9999, ataque=999, defesa=99), 5, 1)


# "print" é silenciado para não poluir a saída dos testes;
# "input" simula o que o jogador digitaria.
@patch("builtins.print")
class TestBatalha(unittest.TestCase):
    def test_heroi_vence_inimigo_fraco(self, _print):
        with patch("builtins.input", return_value="1"):  # sempre "Atacar"
            resultado = Batalha(Heroi("H", GUERREIRO), inimigo_fraco(), RngFixo()).executar()
        self.assertEqual(resultado, Resultado.VITORIA)

    def test_heroi_perde_para_inimigo_forte(self, _print):
        with patch("builtins.input", return_value="1"):
            resultado = Batalha(Heroi("H", GUERREIRO), inimigo_forte(), RngFixo()).executar()
        self.assertEqual(resultado, Resultado.DERROTA)

    def test_fuga_bem_sucedida(self, _print):
        with patch("builtins.input", return_value="4"):  # "Fugir"
            resultado = Batalha(Heroi("H", GUERREIRO), inimigo_forte(), RngFixo(random=0.0)).executar()
        self.assertEqual(resultado, Resultado.FUGA)

    def test_nao_pode_fugir_do_chefe(self, _print):
        # Tenta fugir (bloqueado, não gasta turno) e depois ataca.
        with patch("builtins.input", side_effect=["4", "1"]):
            resultado = Batalha(
                Heroi("H", GUERREIRO), inimigo_fraco(), RngFixo(random=0.0), pode_fugir=False
            ).executar()
        self.assertEqual(resultado, Resultado.VITORIA)


if __name__ == "__main__":
    unittest.main()
