# 2024 Fall Final Projects

## Project Overview

This project presents an implementation of a puzzle-solving and generating algorithm based on variant of **Nurikabe**, a classic Japanese logic puzzle. The project generates random Nurikabe puzzles, verifies their validity, and provides solutions, adhering to strict rules ensuring a unique solution for each puzzle.

This repository includes the following components:

1. **Puzzle Generator**: Creates puzzles based on customizable grid dimensions and randomization of ocean and island placements.
2. **Solver**: Implements recursive backtracking to find and verify solutions, ensuring that each generated puzzle has exactly one valid solution.
3. **Validation Tools**: Ensures that generated puzzles and solutions comply with Nurikabe rules (e.g., continuous oceans, valid island sizes, and no forbidden 2x2 grids).
4. **Analysis**: Includes performance measurement and algorithmic complexity analysis.

## Features

- **Random Puzzle Generation**: Puzzles are generated with customizable dimensions, ensuring unique solutions.
- **Solver**: The backtracking algorithm finds all possible solutions or confirms the absence of a valid solution.
- **Validation**: Multiple checks are performed during puzzle solving and generation, including:
  - Ocean continuity.
  - Island size constraints.
  - Absence of forbidden 2x2 configurations.
- **Prefill Optimization**: Reduces the search space by marking certain cells based on provided clues.

## Usage

### Generating a Puzzle

You can generate a random puzzle by specifying the grid size, or use solver.solve to solve specific puzzles.

## Algorithmic Analysis

### Critical Functions and Complexity

1. **Puzzle Solver**:
   - **DFS Search**: O(n^2) per call for a grid of size n × n.
   - **Backtracking**: Worst-case complexity is also O(n^2).

2. **Puzzle Generator**:
   - **Ocean Randomization**: O(k), where k is the target ocean size.
   - **Validation**: O(n^2) for checking islands, oceans, and 2x2 configurations.
   - **Whole generation**: O(∞).

   See the output file and profiler for more detailed analysis.

### Performance Measurement

- **Solver Runtime**: Profiling shows a dependency on grid size and clue distribution.
- **Puzzle Generator Runtime**: Performance heavily depends on achieving a valid single-solution puzzle.

## Project Contributions

### Team Contributions

For projects involving two students, ensure to document contributions explicitly in the README:

- **Yi Wu**: Implemented the solver and validation logic, made the slides for presentation.
- **Jiajun Zhang**: Initialized the solver structure and basic data structural design, designed the puzzle generator and integrated performance measurement tools and this README file.


## Possible Enhancements

- Improving algorithm efficiency for solving and generating puzzles.
- Like using ture backtracking instead of nested functions.
- Use better recording data structure instead of DFS searching for island after every moves.
