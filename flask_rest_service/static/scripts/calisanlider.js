function Leader() {

//    this.board = new Board(this);
//    this.model = new Model();
//    this.view = new View();
//
//    this.updateInterval = undefined;

    var self = this;
    this.leaderId = null;

    $('form').submit(function (e) {
        var formData = {};
        $("#donateform").serializeArray().map(function(x){formData[x.name] = x.value;});\
        self.setup(JSON.stringify(formData));
        $.post('/pharma/api/leader', JSON.stringify(formData), null, 'json')
            .done(function (data) {
                console.log(data);
                self.leaderId = data.leaderId;
                console.log(self.leaderId);
            });
    });
}

Leader.prototype.setup = function(params) {
    var self = this;

    return $.post('/pharma/api/leader', params, null, 'json')
        .done(function (data) {
            console.log(data);
            self.leaderId = data.leaderId;
            console.log(self.leaderId);
        });
}

new Leader();


//Leader.prototype.setup = function() {
//
//    // Check to see if we're logging in.
//
//    var hashMatches = window.location.hash.match('#/leader/(.*)');
//
//    if (hashMatches !== null) {
//        var leaderId = hashMatches[1];
//        this.joinGame(gameId);
//        window.location.hash = "";
//    }
//
//}

//
//Game.prototype.updateBoardAndState = function() {
//
//    var self = this;
//
//    this.model.getBoard()
//        .done(function (data) {
//            self.board.updateBoard(data.horizontalLines, data.verticalLines, data.boxes);
//        })
//        .fail(function (jqXHR) {
//            if (jqXHR.status == 404) {
//                self.view.postErrorWithCode("Unable to update the game board because the game was not found.",
//                    jqXHR.status, jqXHR.statusText);
//            }
//            else
//                self.view.postErrorWithCode("Unable to update the game board.", jqXHR.status, jqXHR.statusText);
//            clearInterval(self.updateInterval);
//        });
//
//    this.model.getState()
//        .done(function (data) {
//            self.view.updateState(data.state, data.whoseTurn, data.redScore, data.blueScore,
//                self.model.playerType, self.model.gameId);
//        })
//        .fail(function (jqXHR) {
//            if (jqXHR.status == 404) {
//                self.view.postErrorWithCode("Unable to update the game state because the game was not found.",
//                    jqXHR.status, jqXHR.statusText);
//            }
//            else
//                self.view.postErrorWithCode("Unable to update the game state.", jqXHR.status, jqXHR.statusText);
//            clearInterval(self.updateInterval);
//        });
//}
//
//
//Game.prototype.createGame = function(playerType) {
//
//    var self = this;
//
//    this.model.createGame(playerType)
//        .done(function (data) {
//            self.board.resetBoard();
//            self.updateError = false;
//            self.updateBoardAndState();
//            if (self.updateInterval == undefined)
//                self.updateInterval = setInterval(function() { self.updateBoardAndState(); }, 1000);
//        })
//        .fail(function (jqXHR) {
//            self.view.postErrorWithCode("Unable to create game.", jqXHR.status, jqXHR.statusText);
//        });
//}
//
//
//Game.prototype.joinGame = function(gameId) {
//
//    var self = this;
//
//    this.model.joinGame(gameId)
//        .done(function (data) {
//            self.updateBoardAndState();
//            if (self.updateInterval == undefined)
//                self.updateInterval = setInterval(function() { self.updateBoardAndState(); }, 1000);
//        })
//        .fail(function (jqXHR) {
//            switch (jqXHR.status) {
//            case 404:
//                self.view.postErrorWithCode("The requested game could not be found.", jqXHR.status, jqXHR.statusText);
//                break;
//            case 410:
//                self.view.postInfoWithCode("Another player has already joined the game.", jqXHR.status, jqXHR.statusText);
//                break;
//            default:
//                self.view.postErrorWithCode("Unable to join game.", jqXHR.status, jqXHR.statusText);
//            }
//        });
//}
//
//
//Game.prototype.makeHorizontalMove = function(row, col) {
//
//    var self = this;
//
//    return this.model.makeHorizontalMove(row, col)
//        .done(function (data) {
//            self.updateBoardAndState();
//        })
//        .fail(function (jqXHR) {
//            switch (jqXHR.status) {
//            case 404:
//                self.view.postErrorWithCode("The requested game or player could not be found.", jqXHR.status, jqXHR.statusText);
//                break;
//            case 422:
//                self.view.postInfoWithCode("You cannot make a move there. "+
//                    "You either made an illegal move or it is not your turn.", jqXHR.status, jqXHR.statusText);
//                break;
//            default:
//                self.view.postErrorWithCode("Unable to process horizontal move.", jqXHR.status, jqXHR.statusText);
//            }
//        });
//}
//
//Game.prototype.makeVerticalMove = function(row, col) {
//
//    var self = this;
//
//    return this.model.makeVerticalMove(row, col)
//        .done(function (data) {
//            self.updateBoardAndState();
//        })
//        .fail(function (jqXHR) {
//            switch (jqXHR.status) {
//            case 404:
//                self.view.postErrorWithCode("The requested game or player could not be found.", jqXHR.status, jqXHR.statusText);
//                break;
//            case 422:
//                self.view.postInfoWithCode("You cannot make a move there. "+
//                    "You either made an illegal move or it is not your turn.", jqXHR.status, jqXHR.statusText);
//                break;
//            default:
//                self.view.postErrorWithCode("Unable to process horizontal move.", jqXHR.status, jqXHR.statusText);
//            }
//        });
//}
//
//
//
