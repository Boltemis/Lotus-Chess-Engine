# Lotus Chess Engine

## Table of contents
* Description
* How to Use
* v1
* V2

## Description
This is a protoversion of my attempt at a chess AI.
This is also my first big soloproject.
The end goal for this project is to create a Chess Engine that has no problem beating me (1750 rapid on chess.com)

## How to Use
    1. run the main.py file
    2. select 'PLAY A FRIEND' or 'PLAY THE LOTUS CHESS ENGINE'
    3. if the latter has been chosen, select 'PLAY AS WHITE' or 'PLAY AS BLACK'
    4. click on the piece you want to move.
    5. click on the square you want to piece to go (has to be a legal move)

## v1 (16th of December 2023)
    Basic functionality:
        Menu
        PvP and PvE modes, can play as both white and black
        Able to moves pieces if legal move
        TODO: promoting a pawn
        TODO: correct implementation of castling
        TODO: dragging a piece instead of clicking
        TODO: able to safe/load a current gamestate by FEN
    Search:
        Creates array of possible gamestates based on input gamestate
        TODO: optimizing the algorithms (very slow for now)
        TODO: generate_sliding_moves can be written in a simpler way
    Evaluation:
        Minimax has been coded, but not implemented
        Evaluates a position by adding up the value of each piece
        Engine makes a random legal move taking checks into account
        TODO: implement Minimax
        TODO: other parameters for evaluating a position (supported passed pawns, king safety, center control, bishop pair, ..)
        TODO: make move based on evaluation

## v2 (8th of March 2024)
    Worked on the evalation of a chess position by
    * Implementing mimimax
    * Adding positional value to a piece
    The computer makes (not so optimal) moves based on its evaluation