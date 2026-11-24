"""Ponto de entrada do jogo. Execute com: python main.py"""

from rpg.jogo import Jogo


def main() -> None:
    try:
        Jogo().iniciar()
    except (KeyboardInterrupt, EOFError):
        print("\n\nJogo encerrado. Até a próxima!")


if __name__ == "__main__":
    main()
