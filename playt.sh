#!/bin/bash

# Play agent against specified program

# to see AI play with AI
# 6 is the difficulty
# min: 1
# max: 18
# ./playt.sh "python3 agent.py" "./lookt -d 6" 12345

# person vs person 
# open three terminal:
# terminal 1: ./servet -p port_number
# terminal 2: python3 player1.py -p port_number
# terminal 3: python3 player2.py -p port_number

# person vs AI
# play with agent.py AI
# open three terminal:
# terminal 1: ./servet -p port_number
# terminal 2: python3 player1.py -p port_number
# terminal 3: python3 agent.py -p port_number

# play with lookt AI
# open three terminal:
# terminal 1: ./servet -p port_number
# terminal 2: python3 player1.py -p port_number
# terminal 3: python3 ./lookt -d 6 -p port_number

# ./playt.sh "python3 player1.py" "player2.py" 12345
if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <player1> <player2> <port>" >&2
  exit 1
fi

./servt -p $3 & sleep 0.5
$1 -p $3 & sleep 0.5
$2 -p $3
