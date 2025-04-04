# README

## Introducción

Este repositorio contiene una implementación de varios juegos de mesa clásicos, incluyendo Gato (Tic Tac Toe), Conecta 4 y Dominó. La estructura del código está diseñada para ser modular y extensible, permitiendo la adición de nuevos juegos y funcionalidades de manera sencilla. Utiliza un enfoque orientado a objetos para representar los juegos y los jugadores, y se implementa un algoritmo minimax para la toma de decisiones en los juegos.

Además de la implementación en módulos Python, se incluye un notebook de Jupyter (`game_notebook.ipynb`) que proporciona ejemplos prácticos y demostraciones de cómo utilizar las diferentes clases y funcionalidades del proyecto.

## Estructura del Proyecto

El proyecto está organizado en varias carpetas y archivos:

- **game/game.py**: Define la clase `Game`, que representa un juego de mesa, considerando tablero, turnos, y lógica de juego.
- **game/player.py**: Define la clase `Player`, que representa a los jugadores en los juegos.
- **game/minimax.py**: Implementa el algoritmo minimax, que se utiliza para calcular el mejor movimiento posible en los juegos.
- **game/board_games/**: Contiene las implementaciones específicas de cada juego, como Tic Tac Toe, Conecta 4 y Dominó.
- **game_notebook.ipynb**: Un notebook de Jupyter que contiene ejemplos de cómo crear y jugar los diferentes juegos implementados, así como demostraciones del uso del algoritmo minimax.

## Funcionalidades

### Juegos Implementados

1. **Tic Tac Toe**:
   - Dos jugadores se turnan para colocar sus símbolos en un tablero de 3x3.
   - El primer jugador en alinear tres de sus símbolos en línea, columna o diagonal gana.

2. **Conecta 4**:
   - Dos jugadores se turnan para dejar caer fichas en una cuadrícula de 7 columnas y 6 filas.
   - El objetivo es alinear cuatro fichas en línea, ya sea horizontal, vertical o diagonalmente.

3. **Dominó**:
   - Los jugadores colocan fichas en un tablero, tratando de coincidir los números en los extremos de las fichas.
   - El juego puede jugarse en modo individual o en equipos.

### Algoritmo Minimax

El algoritmo minimax se utiliza para calcular el mejor movimiento posible dado un estado del juego. Este algoritmo evalúa todos los posibles movimientos y sus resultados, eligiendo el movimiento que maximiza la probabilidad de ganar.
Se realizaron dos implementaciones del algoritmo minimax:
- Una implementación con cache:
  - Esta implementación guarda los resultados de las evaluaciones de los nodos en una cache para evitar recalcularlos.
  - Es muy útil para juegos donde el espacio de estados es recurrente, es decir, el mismo estado puede aparecer más de una vez durante el juego.
- Una implementación con poda alfa-beta:
  - Esta implementación es una optimización del algoritmo minimax que reduce el número de nodos evaluados.
  - Básicamente, la poda alfa-beta consiste en eliminar los nodos que no son necesarios evaluar. Es altamente eficiente para juegos con espacios de estados grandes y profundos, que no cuentan con estados recurrentes.

### Interfaz de Usuario

El juego se puede jugar a través de la consola, donde los jugadores pueden ingresar sus movimientos. La IA también puede ser utilizada como oponente, proporcionando una experiencia de juego desafiante.

## Cómo Ejecutar el Proyecto

Para ejecutar el proyecto, asegúrate de tener Python instalado en tu sistema. Si deseas explorar los ejemplos interactivos, también necesitarás tener Jupyter Notebook instalado. Luego, sigue estos pasos:

1. **Clona el repositorio:**
   ```bash
   gh repo clone bruno-rda/minimax-games
   cd minimax-games
   ```

2. **Para ejecutar los juegos directamente desde la consola:**
   ```python
   from game.board_games import TicTacToe, TicTacToePlayer, TicTacToeAI

   game = TicTacToe()
   player = TicTacToePlayer('Jugador 1')
   ai = TicTacToeAI('IA')
   game.play(player, ai)
   ```
   Puedes adaptar este ejemplo para jugar otros juegos implementados.

3. **Para explorar los ejemplos en el notebook:**
   ```bash
   jupyter notebook game_notebook.ipynb
   ```
   Esto abrirá el notebook en tu navegador, donde podrás ejecutar las celdas de código y ver ejemplos de cómo utilizar las diferentes clases y funcionalidades del proyecto, incluyendo la creación de juegos y el uso de jugadores humanos y la IA basada en el algoritmo minimax.