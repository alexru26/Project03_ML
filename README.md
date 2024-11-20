# Machine Learning Project 03: A* Pathfinding Project
This is a program to create network graphs and run the A* pathfinding algorithm.

## How to run
Make sure you have the necessary packages.

```
pip install -r requirements.txt
```

Run ```main.py``` to use the program.

## Resources Used
- ChatGPT
- [networkx](https://networkx.org/documentation/stable/tutorial.html)
- [pickle](https://docs.python.org/3/library/pickle.html)
- https://www.youtube.com/watch?v=i0x5fj4PqP4&ab_channel=Tarodev

## Functionality
- Create and load new graphs
- Graph generation and visualization wit*h networkx
- Save and modify graphs
- Can choose start and end nodes and run A* pathfinding algorithm

## Reasoning and Issues
- Visualization
  - I used the shell layout because it was the most clear
  - Tried spring, spectral, etc. layouts, but too condensed and confusing
- h score
  - No good way to find node's distance to target
  - Only feasible way is with Euclidean distance
  - Issue is that Euclidean distance is not very accurate

## Further Improvements
- Interactive UI instead of CLI
  - More intuitive and less clunky
- More consistent way of getting h score
- Better visualization
