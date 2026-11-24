# ⚔️ A Masmorra do Dragão

RPG de turnos jogado no terminal, feito em **Python puro** (sem bibliotecas externas).
Escolha uma classe, desça 5 andares de uma masmorra, derrote monstros, suba de nível
e enfrente o **Dragão Ancião** no final.

O foco do projeto é ser **simples de jogar e bem estruturado por dentro**: cada arquivo
tem uma única responsabilidade, a lógica do jogo é separada da interface e tudo é
coberto por testes automatizados.

```
====================================================
                 KAEL VS ESQUELETO
====================================================
----------------------------------------------------
Kael             [##############------] 88/125
Esqueleto        [######--------------] 21/66
----------------------------------------------------

O que você vai fazer?
  1) Atacar
  2) Bola de Fogo (pronta)
  3) Usar item (2)
  4) Fugir
>
```

---

## 🎮 Funcionalidades

- **3 classes jogáveis**, cada uma com uma habilidade especial que tem tempo de recarga
  | Classe | Estilo | Habilidade |
  |---|---|---|
  | Guerreiro | Muita vida e defesa | **Golpe Brutal**: 2x de dano |
  | Mago | Frágil, mas forte | **Bola de Fogo**: 1.5x de dano ignorando a defesa |
  | Arqueiro | Equilibrado | **Chuva de Flechas**: 1.7x de dano, recarrega mais rápido |
- **Combate por turnos** com variação de dano e golpes críticos
- **Sistema de níveis**: ganhe XP, suba de nível e fique mais forte
- **Inventário e itens**: poções de vida e elixires que aumentam o ataque
- **Loja** para gastar o ouro ganho nas batalhas
- **Dificuldade progressiva**: os inimigos ficam mais fortes a cada andar
- **Chefe final** do qual não dá para fugir

---

## 🚀 Como rodar

### 1. Pré-requisito

Ter o **Python 3.8 ou superior** instalado. Para conferir, abra o terminal e rode:

```bash
python --version
```

> No Windows, se o comando acima não funcionar, tente `py --version`.
> Se não tiver o Python, baixe em [python.org/downloads](https://www.python.org/downloads/)
> e, na instalação, marque a opção **"Add Python to PATH"**.

### 2. Baixar o projeto

```bash
git clone https://github.com/SEU-USUARIO/rpg-python.git
cd rpg-python
```

(Ou baixe o `.zip` pelo botão verde **Code → Download ZIP** no GitHub e extraia.)

### 3. Jogar

```bash
python main.py
```

No Windows também funciona `py main.py`. Não precisa instalar nada além do Python.

**Controles:** digite o número da opção e aperte **ENTER**.
Para sair a qualquer momento, aperte **Ctrl + C**.

---

## 🧪 Como rodar os testes

Os testes usam o `unittest`, que já vem com o Python:

```bash
python -m unittest -v
```

Saída esperada (resumida):

```
Ran 21 tests in 0.005s

OK
```

---

## 📁 Estrutura do projeto

```
rpg-python/
├── main.py              # Ponto de entrada: só inicia o jogo
├── rpg/
│   ├── config.py        # Números de balanceamento (dificuldade, XP, chances...)
│   ├── personagem.py    # Classe base Personagem: vida, ataque, dano, cura
│   ├── heroi.py         # Heroi: nível, XP, ouro, inventário, habilidade especial
│   ├── classes.py       # Guerreiro, Mago e Arqueiro (dados de cada classe)
│   ├── inimigos.py      # Inimigo + fábrica que gera monstros por andar
│   ├── itens.py         # Item (abstrato), Pocao e Elixir
│   ├── inventario.py    # Guarda e usa os itens do herói
│   ├── combate.py       # Batalha por turnos
│   ├── loja.py          # Compra de itens com ouro
│   ├── ui.py            # Tudo que imprime na tela ou lê o teclado
│   └── jogo.py          # Fluxo do jogo: criar herói → andares → final
└── tests/               # Testes automatizados
```

### Como as peças se conectam

```
main.py → Jogo ──► Batalha ──► Heroi / Inimigo ──► Personagem
            │                     │
            ├──► Loja             └──► Inventario ──► Item
            └──► ui  (única parte que conversa com o terminal)
```

### Decisões de design

- **Herança:** `Heroi` e `Inimigo` herdam de `Personagem`, então a fórmula de ataque
  e dano existe em um só lugar.
- **Polimorfismo:** todo item herda de `Item` e implementa `usar()`. O inventário não
  precisa saber se é uma poção ou um elixir.
- **Separação entre lógica e interface:** só o `ui.py` usa `print` e `input`. As regras
  do jogo poderiam ser reaproveitadas numa interface gráfica sem mudanças.
- **Dados em vez de código repetido:** classes e inimigos são declarados como dados
  (`dataclass`), então adicionar um novo é só acrescentar uma linha.
- **Aleatoriedade injetável:** o combate recebe o gerador de números aleatórios como
  parâmetro, o que permite testes previsíveis.
- **Configuração centralizada:** todo o balanceamento fica em `config.py`.

---

## 🛠️ Como modificar

**Deixar o jogo mais fácil/difícil:** altere os valores em `rpg/config.py`.

**Adicionar um inimigo:** em `rpg/inimigos.py`, acrescente em `MODELOS_COMUNS`:

```python
ModeloInimigo("Orc", Atributos(vida_max=70, ataque=16, defesa=6), xp=55, ouro=20),
```

**Adicionar uma classe:** em `rpg/classes.py`, crie um `ClasseHeroi` e coloque-o em
`CLASSES_DISPONIVEIS`.

**Adicionar um tipo de item:** crie uma classe que herda de `Item` em `rpg/itens.py`
e implemente o método `usar()`.

---

## 💡 Ideias para próximas versões

- [ ] Salvar e carregar o progresso (JSON)
- [ ] Sistema de mana para as habilidades
- [ ] Equipamentos (armas e armaduras)
- [ ] Efeitos de status (veneno, atordoamento)
- [ ] Interface colorida com a biblioteca `rich`
- [ ] Versão gráfica com `pygame`

---

## 👤 Autor

Feito por **VINICIUS FURTADO**: [LinkedIn](https://www.linkedin.com/in/vifurtado/) · [GitHub](https://github.com/vnniwzx)
