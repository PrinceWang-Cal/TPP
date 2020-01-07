# Turkey Avocalgorithm for Traveling Purchaser Problem
UC Berkeley CS 170 Fall 2019 Project

Name of the algorithm inspired by our favorite food at UC Berkeley: turkey avocado sandwich

## Overview
This is a solver that computes suboptimal paths for a variant of the traveling purchaser problem, which is a well-known NP hard problem. Given a weighted graph represented by an adjacency matrix, a starting location(node) and a series of markets(nodes), our solver gives a solution for a optimal path with drop-off locations.

## Implementation

The solver is implemented in python 3.6.

## Dependencies

The only python package we used is networkx 2.4, a popular python package for graph creation and graph-related algorithms.
For more details please refer to: https://networkx.github.io/

## Installation

Install <a href="https://networkx.github.io/" target="_blank">networkx</a>. The latest(2.5) version is not needed.

To install networkx for Python through pip:
```bash
pip install networkx
```

## Usage
To run our solver on a given input:

    python3 solver.py <input/file/path> <output/directory/path>

where **<input/file/path>** is the file path to your input file(.in files), and **<output/directory/path>** is the path where you want to store your outputs.

To run our solver on all inputs:

    python3 solver.py --all <input/directory/path> <output/directory/path>

where **<input/directory/path>** is the directory where you store all your input files.

## Acknowledgement

Our algorithm is inspired by the greedy approximation of TSP problem.
