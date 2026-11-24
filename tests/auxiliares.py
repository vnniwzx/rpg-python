"""Ferramentas compartilhadas pelos testes."""


class RngFixo:
    """Substitui o random.Random para que os testes sejam previsíveis.

    Por padrão: variação de dano = 0 e nunca acerta crítico.
    """

    def __init__(self, randint: int = 0, random: float = 0.99) -> None:
        self._randint = randint
        self._random = random

    def randint(self, a: int, b: int) -> int:
        return self._randint

    def random(self) -> float:
        return self._random

    def choice(self, seq):
        return seq[0]
