// 棋子编号
CHESS_KING = 0;		  // 将
CHESS_ADVISOR = 1;	// 士
CHESS_BISHOP = 2;	  // 象
CHESS_KNIGHT = 3;	  // 马
CHESS_ROOK = 4;		  // 车
CHESS_CANNON = 5;	  // 炮
CHESS_PAWN = 6;		  // 卒

PLAYER = 0;       // 玩家
COMPUTER = 1;     // 电脑

MattsArr = [3, 4, 5, 12, 13, 14, 21, 22, 23, 66, 67, 68, 75, 76, 77, 84, 85, 86]; //田字格位置

//判断将能否移动的辅助数组
kingMove = [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]; 
//判断士能否移动的辅助数组
advisorMove = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
//判断象能否移动的辅助数组
bishopMove = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1];
// 判断马能否移动的辅助数组
knightMove = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0];
class Position {
  
  constructor(chesses) {
    this.player = PLAYER;
    this.initialBoardPos(chesses);
  }

  initialBoardPos(chesses) {
    this.board_pos = Array.from({length:90}, ()=> 0);
    let x = 0;
    let y = 0;
    for (let c of chesses) {
      console.log(x)
      console.log(y)
      console.log(c)
      let moveNext = 1;
      if (c === '/') {
        x = 0;
        ++y;
        continue;
      }
      if (c >= "1" && c <= "9") {
        moveNext = parseInt(c);
      } else if (c >= "A" && c <= "Z") {
          let chess = this.CHAR_TO_CHESS(c);
          this.setChess(this.COORD_XY(x, y), chess + 8, false);
      } else if (c >= "a" && c <= "z") {
          let chess = this.CHAR_TO_CHESS(c.toUpperCase());
          this.setChess(this.COORD_XY(x, y), chess + 16, false);
      }
      x += moveNext;
    }
  }

  // 将二维矩阵转换为一维矩阵
  COORD_XY(x, y) {
    return y * 9 + x;
  }

  CHAR_TO_CHESS(c) {
    switch (c) {
      case "K":
        return CHESS_KING;
      case "A":
        return CHESS_ADVISOR;
      case "B":
        return CHESS_BISHOP;
      case "N":
        return CHESS_KNIGHT;
      case "R":
        return CHESS_ROOK;
      case "C":
        return CHESS_CANNON;
      case "P":
        return CHESS_PAWN;
      default:
        return -1;
    }
  }

  GET_CHESS(chess) {
    return this.player === PLAYER ? chess - 8 : chess - 16;
  }

  GET_CHESS_ROW(pos) {
    return Math.floor(pos / 9);
  }

  GET_CHESS_COL(pos) {
    return Math.floor(pos % 9);
  }

  setChess(pos, chess, del) {
    this.board_pos[pos] = del ? 0 : chess;
  }

  // 判断是否在田字格中
  IN_MATTS(pos) {
    return MattsArr.includes(pos);
  }

  // 判断将移动的距离是否正确 (对将除外)
  KING_CAN_MOVE(src, des) {
    return  kingMove[Math.abs(des - src)] === 1; 
  }

  // 判断士移动的距离是否正确
  ADVISOR_CAN_MOVE(src, des) {
    return advisorMove[Math.abs(des - src)] === 1;
  }

  // 判断象移动的距离是否正确
  BISHOP_CAN_MOVE(src, des) {
    return bishopMove[Math.abs(des - src)] === 1;
  }

  // 判断马移动的距离是否正确
  KINGHT_CAN_MOVE(src, des) {
    return knightMove[Math.abs(des - src)] === 1;
  }

  // 判断象眼是否为空
  BISHOP_CENTER_EMPTY(src, des) {
    return this.board_pos[(src + des) / 2] === 0;
  }

  // 判断马脚是否为空
  KNIGHT_FOOT_EMPTY(src, des) {
    let delta_x = this.GET_CHESS_COL(des) - this.GET_CHESS_COL(src);
    let delta_y = this.GET_CHESS_ROW(des) - this.GET_CHESS_ROW(src);
    let foot_pos = 0;
    if (Math.abs(delta_x) == 2) {
      foot_pos = src + (delta_x < 0 ? -1 : 1);
    } else {
      foot_pos = src + (delta_y < 0 ? -9 : 9);
    }
    return this.board_pos[foot_pos] == 0;
  }

  // 判断是否过河
  CORSS_REVER(pos) {
    return this.player === PLAYER ? pos < 44 : pos >= 45;
  }

  // 判断兵是否往前走
  MOVE_FORWARD(src, des) {
    let delta = des - src;
    return this.player === PLAYER ? delta === -9 : delta === 9;
  }

  // 判断车、炮是否移动正确 
  ROOK_OR_CANNON_CAN_MOVE(src, des, chess) {
    let delta = 0;
    if (this.GET_CHESS_ROW(src) === this.GET_CHESS_ROW(des)) {
      delta = des > src ? 1 : -1;
    } else if (this.GET_CHESS_COL(src) === this.GET_CHESS_COL(des)) {
      delta = des > src ? 9 : -9;
    } else {
      return false;
    }
    let src_temp = src + delta;
    while (src_temp != des && this.board_pos[src_temp] === 0) {
      src_temp += delta;
    }
    if (src_temp === des) {
      return this.board_pos[des] === 0 || chess === CHESS_ROOK;
    }
    if (this.board_pos[des] === 0 || chess === CHESS_ROOK) {
      return false;
    }
    src_temp += delta;
    while (src_temp != des && this.board_pos[src_temp] === 0) {
      src_temp += delta;
    }
    return src_temp === des;
  }


  legalMove(src, des) {
    let chess = this.GET_CHESS(this.board_pos[src]);
    switch(chess) {
      case CHESS_KING:
        return this.IN_MATTS(des) && this.KING_CAN_MOVE(src, des); 
      case CHESS_ADVISOR:
        return this.IN_MATTS(des) && this.ADVISOR_CAN_MOVE(src, des);
      case CHESS_BISHOP:
        return !this.CORSS_REVER(des) && this.BISHOP_CENTER_EMPTY(src, des) && this.BISHOP_CAN_MOVE(src, des); 
      case CHESS_KNIGHT:
        return this.KINGHT_CAN_MOVE(src, des) && this.KNIGHT_FOOT_EMPTY(src, des);
      case CHESS_ROOK:
        return this.ROOK_OR_CANNON_CAN_MOVE(src, des, CHESS_ROOK);
      case CHESS_CANNON:
        return this.ROOK_OR_CANNON_CAN_MOVE(src, des, CHESS_CANNON);
      case CHESS_PAWN:
        return (this.CORSS_REVER(src) && Math.abs(des - src) == 1) || this.MOVE_FORWARD(src, des);
    }
  }

  // 更换下棋方
  changeSide() {  
    this.player = this.player === PLAYER ? COMPUTER : PLAYER;
  }

  // 判断下棋方是否为玩家
  getCurPlayer() {
    return this.player === PLAYER;
  }

  OWN_CHESS(chess) {
    if (this.player === PLAYER) {
      return chess & 8;
    } else {
      return chess & 16;
    }
  }

  // 电脑下棋时，生成所有走法
  generateAllMove() {
    // 遍历棋盘
    for (c of this.board_pos) {
      if (this.OWN_CHESS(c)) {
        switch (this.GET_CHESS()) {
        }
      }
    }
  }
}
