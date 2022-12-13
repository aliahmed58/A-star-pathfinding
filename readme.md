## Visualizing A* path finding algorithm
Visualizing the A* search algorithm in pygame. :)

### Cost criteria:
- **H cost** = dx + dy, where dx and dy is the absolute 
  distance between goal and current cell
- **G cost** = 14 if cell is diagonal else G cost = 10
- **Total cost** = H cost + G cost



### How to run:
- Install required packages by `pip install -r 
  requirements.txt`
- Run `main.py`

### How to use:  
- How to select the start node (**red**):
  - Press `S` and then click a square on the grid
  - Undo by pressing `S` and then right-click on the 
    start node
- How to select the goal node (**green**):
  - Press `G` and then click on a square on the grid
  - Undo by pressing `G` and then right-click on the 
    goal node
- Reset the screen by pressing `R`
- Draw walls on the screen by pressing `D`
- Clear walls drawn on screen by pressing `C`
- Exit drawing mode by pressing `Spacebar`
- To start visualizing search, press `Enter` : only 
  after start and goal node has been set.
