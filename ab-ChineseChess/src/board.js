var SQUARE_SIZE = 57;

var imgArr = [
  "assets/oo.gif", "assets/oos.gif", null, null, null, null, null, null,
  "assets/rk.gif", "assets/ra.gif", "assets/rb.gif", "assets/rn.gif", "assets/rr.gif", "assets/rc.gif", "assets/rp.gif", null,
  "assets/bk.gif", "assets/ba.gif", "assets/bb.gif", "assets/bn.gif", "assets/br.gif", "assets/bc.gif", "assets/bp.gif", null,
];   //img图片路径数组

class Board {
    // chesses = "rnbakabnr/8/1c5c1/p1p1p1p1p/8/8/P1P1P1P1P/1C5C1/8/RNBAKABNR";

    constructor (container, chesses) {
	    console.log(container);

      this.computing = false;
      this.imageSquares= []; // img元素数组，对应棋盘上的90个位置区域
      this.lastSelect = -1;    // 当前选中的棋子
      this.red_retractPath = [];
      this.black_retractPath = [];
      this.lastMove = [];
      this.pos = new Position(chesses);
      this.search = new Search(this.pos);
      this.initialboard(container);
  }

  initialboard(container) {
	  console.log(container);

    for (var i = 0; i < 90; ++i) {
      var img = document.createElement("img");
      //添加样式
      var style = img.style;
      style.position = "absolute";
      style.left = (i % 9) * SQUARE_SIZE + "px";
      style.top =  Math.floor(i / 9) * SQUARE_SIZE + "px";
      style.width = SQUARE_SIZE;
      style.height = SQUARE_SIZE;
      style.zIndex = 0;
      //绑定点击事件
      img.onmousedown = function(pos, self) {
        return function() {
          console.log("click");
          console.log(pos);
          self.clickSquare(pos);
        }
      } (i, this);
      //添加到棋盘中
      container.appendChild(img);
      //存储到img元素数组中
      this.imageSquares.push(img);
    }
    //为img元素添加对应图片
    this.initialChess();
  }

  initialChess() {
    for (var i = 0; i < 90; ++i) {
      this.updateChess(i, false);
    }
  }

  updateChess(pos, selected) {
    var img = this.imageSquares[pos];
    img.src = imgArr[this.pos.board_pos[pos]];
    img.style.backgroundImage = selected ? "url(" + imgArr[1] + ")" : "";
    console.log(pos);
    console.log(img.style.backgroundImage);
  }

  clickSquare(pos) {
    if (this.computing) {
      return;
    }
    var chess = this.pos.board_pos[pos];
    console.log(chess);
    // console.log(chess & 8 != 0);
    if (this.pos.OWN_CHESS(chess)) {
      
        // 清除上次移动的步伐
      if (this.lastMove.length > 0) {
        this.updateChess(this.lastMove[0], false);
        this.updateChess(this.lastMove[1], false);
        this.lastMove = [];
      }
      
      // 去除上次选中的棋子边框
      if (this.lastSelect != -1) {
        this.updateChess(this.lastSelect, false);
      }
      // 更新当前选中的棋子边框
      this.lastSelect = pos;
      this.updateChess(this.lastSelect, true);
    } else if (this.lastSelect != -1) {
      // 选中了对方的棋子或空白处
      this.move(this.lastSelect, pos);
    }
  }

  move(lastSelect, curSelect) {
    // 判断是否合法
    if (!this.pos.legalMove(lastSelect, curSelect)) {
      return;
    }

    let chess = this.pos.board_pos[curSelect];
    this.pos.board_pos[curSelect] = this.pos.board_pos[lastSelect];
    this.pos.board_pos[lastSelect] = 0;
    this.updateChess(curSelect, true);
    this.updateChess(lastSelect, true);
    this.lastMove =[lastSelect, curSelect, chess];
    this.red_retractPath.push(this.lastMove);
    this.lastSelect = -1;

    //电脑回一步棋
    this.pos.changeSide();
    this.response();
  }

  response() {
    if (this.pos.getCurPlayer()) {
      return;
    }
    this.computing = true;
    this.search.begin();
  }

  retract() {
    this.helpTOretract(this.red_retractPath);
    this.helpTOretract(this.black_retractPath);
  }

  helpTOretract(retractPath) {
    if (retractPath.length > 0) {
      this.lastMove = [];
      let lastTract = retractPath.pop();
      this.pos.board_pos[lastTract[0]] = this.pos.board_pos[lastTract[1]];
      this.pos.board_pos[lastTract[1]] = lastTract[2];
      this.updateChess(lastTract[0], false);
      this.updateChess(lastTract[1], false);

      // 清除原本选中的棋子边框
      if (this.lastSelect != -1) {
        this.updateChess(this.lastSelect, false);
        this.lastSelect = -1;
      }
    }
  }

  restart(chesses) {
    this.pos.initialBoardPos(chesses);
    this.initialChess();
  }

}
