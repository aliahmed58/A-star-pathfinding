## Visualizing A* path finding algorithm
A hobby project by Ali Ahmed :)
### How to run:
- Install required packages by `pip install -r 
  requirements.txt`
- Run `main.py`

### How to play:  
- How to select the start node (red):
  - Press 's' and then a square on the grid
  - Undo by pressing 's' and then right-click on the 
    start node
- How to select the goal node (green):
  - Press 'g' and then a square on the grid
  - Undo by pressing 'g' and then right-click on the 
    goal node
- Reset the screen by pressing R
- Draw on screen by pressing 'D'
- Clear screen drawing by pressing 'C'
- Exit drawing mode by pressing 'spacebar'
### Unresolved Issues:
Due to lack of time, some minor issues are unresolved
1. Pixel index out of range error when the path tries to 
   search at the corner of the screen.
   - Fix by setting limits 
2. Memory problem, inserting too many nodes causes the 
   screen to freeze (Not responding), then suddenly ends by 
   finding a path