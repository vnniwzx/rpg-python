"""Classes jogáveis (Guerreiro, Mago, Arqueiro) e suas habilidades especiais.

Para criar uma classe nova, basta declarar um novo ClasseHeroi
e adicioná-lo em CLASSES_DISPONIVEIS.
"""

from __future__ import annotations

from dataclasses import dataclass

from rpg.personagem import Atributos


@dataclass(frozen=True)
class Habilidade:
    nome: str
    descricao: str
    multiplicador: float
    recarga: int               # turnos até poder usar de novo
    ignora_defesa: bool = False


@dataclass(frozen=True)
class ClasseHeroi:
    nome: str
    descricao: str
    atributos: Atributos
    habilidade: Habilidade


GUERREIRO = ClasseHeroi(
    nome="Guerreiro",
    descricao="Muita vida e defesa. Aguenta pancada.",
    atributos=Atributos(vida_max=130, ataque=14, defesa=7),
    habilidade=Habilidade(
        nome="Golpe Brutal",
        descricao="Causa o dobro de dano.",
        multiplicador=2.0,
        recarga=3,
    ),
)

MAGO = ClasseHeroi(
    nome="Mago",
    descricao="Frágil, mas seus feitiços ignoram armadura.",
    atributos=Atributos(vida_max=95, ataque=17, defesa=3),
    habilidade=Habilidade(
        nome="Bola de Fogo",
        descricao="Dano 1.5x que ignora a defesa do inimigo.",
        multiplicador=1.5,
        recarga=3,
        ignora_defesa=True,
    ),
)

ARQUEIRO = ClasseHeroi(
    nome="Arqueiro",
    descricao="Equilibrado. Sua habilidade recarrega mais rápido.",
    atributos=Atributos(vida_max=115, ataque=16, defesa=5),
    habilidade=Habilidade(
        nome="Chuva de Flechas",
        descricao="Causa 1.7x de dano.",
        multiplicador=1.7,
        recarga=2,
    ),
)

CLASSES_DISPONIVEIS: tuple[ClasseHeroi, ...] = (GUERREIRO, MAGO, ARQUEIRO)
