Sokoban
1. CO REALIZUJE PROJEKT
Basic version of sokoban game implemented as a terminal game with opion to add new legal levels.


2. Jak go uruchomić, zainstalować dependencje, etc.
To install the game you must do following steps:

1. Create virtual environment:
```
mkdir your_dorectory &&
cd your_directory &&
python3 -m venv .venv
```
2. Activate virtual environment:
```
source .venv/bin/activate
```
3. Clone repository
```
git clone thisdirecory
```
To start the game do the following commands:
```
cd sokobane_game
python3 sokoban.py
```

To create your own level:
Create a <level_number>.txt file where <level_number> is the number of your level
Format used for representing Sokoban level involves:
|Level element|Character|
|:------------ |:---------------:|
|Wall|#|
|Player|@|
|Player on goal|+|
|Box|$|
|Box on goal|*|
|Goal|.|
|Floor|(space)|

For example, level 1 may look like this:

```
  ###
  #.#
  # ####
###$ $.#
#. $@###
####$#
   #.#
   ###
```

Important

The whole level should be souranded by walls.

First level must have nember equal 1. Folowing levels shold have numbers incremented by one.

Level file must not have any other characters then from above.

Default color of a level and a player is white. However, you can change their colors while starting the game. In order to do so, you need to add additionl parameters:
1. '--game_color' or '-g', with preferred color to change game's color, for example:
```
python3 sokoban.py --game_color 'green'
```
2. '--player' or '-p', with preferred color to change player-s color, for example:
```
python3 sokoban.py --player_color 'red'
```

Available colors:
blue cyan, green, magenta, red, white, yellow

White is a default color for both map and player

3. Diagram architektury projektu z opisem tej architektury.

![Diagram UML](./graphics/sokoban_uml_diagram.png)

