# **九宫格井字棋 AI 代理介绍**

## **项目概述**
本项目实现了一个 **九宫格井字棋（Nine-Board Tic-Tac-Toe）AI 代理**，采用 **Minimax 算法 + Alpha-Beta 剪枝** 进行决策，能够智能落子，与人类或其他 AI 对手对战。

---

## **核心功能**
1. **智能决策：**  
   - 使用 **Minimax 算法** 评估所有可能的落子情况。  
   - 结合 **Alpha-Beta 剪枝** 提高计算效率，减少无效搜索。  
   
2. **游戏逻辑：**  
   - **`player_turn(board, curr)`**：根据局势评估最优落子点。  
   - **`curr_score(board, curr, position_to_place)`**：计算当前落子评分。  
   - **`alphabeta_algorithm()`**：使用递归搜索最佳策略。  
   - **`print_board(board)`**：打印棋盘状态。  

---

## **运行方式**
### **AI 对战 AI**
让 **agent.py** 与 **lookt AI** 进行对战，难度范围 `1-18`，默认 `6`：
```bash
./playt.sh "python3 agent.py" "./lookt -d 6" 12345

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
