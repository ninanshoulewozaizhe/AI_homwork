window.onload = function() {

	var container = document.getElementById("chessboard");
	console.log(container);
	var chesses = "rnbakabnr/8/1c5c1/p1p1p1p1p/8/8/P1P1P1P1P/1C5C1/8/RNBAKABNR";

	var board = new Board(container, chesses);

	var btn_start = new Vue({
		el:'#btn_restart',
		methods: {
			restart_game: function() {
				board.restart(chesses);
			}
		}
	});

	var btn_retract = new Vue({
		el:'#btn_retract',
		methods: {
			retract: function() {
				board.retract();
			}
		}
	})
}



