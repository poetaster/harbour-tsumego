import QtQuick 2.0

import "../javascript/goban_util.js" as Actions
import "../javascript/navigator.js" as TreeNavigator

Item {

    /**
     * This property represent a case size on the board.
     * The value is calculated at initialization, and depends on the goban size.
     */
    property int caseSize

    /**
     * Booleans flags telling if the board is limited in each directions
     */
    property bool limitTop: true;
    property bool limitBottom: true;
    property bool limitLeft: true;
    property bool limitRight: true;

    property bool completed: false;

    /*
     * The current color to play :
     * - true for white
     * - false for black
     */
    property bool currentPlayer: true;

    property bool initialPlayer: true;

    property bool freePlay: false;

    /*
     * flag to tell if player is on a wrong branch.
     */
    property bool isWrong: false;

    /**
     * The game tree.
     */
    property variant tree;

    /**
     * Path in the tree.
     */
    property variant path;

    /*
     * History for cancelling a move.
     */
    property variant history;

    signal completedLevel(bool status);
    signal startup();

    /*
     * Start the game. Initialize the board with the stones, and set player color.
     * Function called at first launch, or whene resetting the game.
     */
    function start() {

        startup();
        completed = false;

        for (var i = 0; i < goban.rows * goban.columns; i++) {
            repeater.itemAt(i).remove(false);
        }

        var initial;
        currentPlayer = initialPlayer;

        i = 0;

        while (tree[i].AW === undefined && tree[i].AB === undefined) {
            i++;
        }

        initial = tree[i];
        history = [];
        path = [i + 1];

        var aw = initial.AW;
        if (aw !== undefined) {
            aw.forEach(function (pos) {
                goban.itemAt(pos).put(true, false);
            });
        }

        var ab = initial.AB;
        if (ab !== undefined) {
            ab.forEach(function (pos) {
                goban.itemAt(pos).put(false, false);
            });
        }
        isWrong = false;
    }

    function setGoban(ret) {

        limitTop = ret.side.TOP;
        limitBottom = ret.side.BOTTOM;
        limitLeft = ret.side.LEFT;
        limitRight = ret.side.RIGHT;

        goban.columns = ret.size[0]
        goban.rows = ret.size[1]


        var maxWidth = width / ret.size[0]
        var maxHeight = height / ret.size[1]

        if (maxWidth > maxHeight)  {
            caseSize = maxHeight;
        } else {
            caseSize = maxWidth;
        }

        initialPlayer = (ret.current_player === 'W');

        /*
         * Put the initials stones
         */
        tree = ret.tree;
        start();
    }

    function showHint() {

        if (path === undefined) {
            console.log("no hint to show");
            return;
        }
        var action = TreeNavigator.getNextMove(path, tree, currentPlayer);
        clickHandler(action);
    }

    /*
     * Undo the last move.
     */
    function undo() {
        if (history.length === 0) {
            return;
        }

        completed = false;
        var currentHistory = history;

        var actions = currentHistory.pop();
        actions.reverse();

        actions.forEach(function (x) {
            Actions.undo(goban, x);
            currentPlayer = x.player;
            path = x.path;
            if (x.wrong !== undefined) {
                isWrong = false;
            }
        });

        history = currentHistory;

    }

    /**
     * Handle a click on the goban.
     */
    function clickHandler(index) {

        if ( (!limitLeft && Actions.isFirstCol(index, goban.columns))
          || (!limitRight && Actions.isLastCol(index, goban.columns))
          || (!limitTop && Actions.isFirstRow(index, goban.columns))
          || (!limitBottom && Actions.isLastRow(index, goban.columns, goban.rows)) ) {

            return;
        }

        var step = Actions.addPiece(index, goban, currentPlayer, true, false, false);
        if (step === undefined) {
            /* Movement not allowed. */
            return;
        }

        if (completed) {
            completed = false;
        }

        /*
         * Update the path.
         */
        step.path = path;

        /*
         * Update the history with the last move.
         */
        var currentHistory = history;
        var actions = [step];

        var followLevel = TreeNavigator.checkAction(path, tree, currentPlayer, index, function (newPath, properties) {

            if (properties.wrong !== undefined) {
                isWrong = true;
                step.wrong = true;
            }

            if (TreeNavigator.getCurrentAction(newPath, tree) === undefined) {
                completed = true;
                completedLevel(isWrong);
            } else {
                /* Play the openent move. */
                path = newPath;
                TreeNavigator.playComputer(newPath, tree, currentPlayer, function(x, newPath) {
                    var oponentAction = Actions.addPiece(x, goban, !currentPlayer, true, false, false)
                    oponentAction.path = path;
                    path = newPath;
                    actions.push(oponentAction);
                });
                if (TreeNavigator.getCurrentAction(path, tree) === undefined) {
                    /*
                     * Level has been completed by the computer move.
                     */
                    completed = true;
                    currentPlayer = !currentPlayer;
                    completedLevel(isWrong);
                }

            }
        });

        if (!followLevel || completed) {
            path = undefined;
            currentPlayer = !currentPlayer;
        }

        currentHistory.push(actions);
        history = currentHistory;

    }

    /**
     * Background
     */
    Image {
        width: goban.width + (caseSize / 2); height: goban.height + (caseSize / 2);
        source: "../content/gfx/board.png"
        anchors.centerIn: goban
    }

    /*
     * Horizontal lines
     */
    Repeater {
        model: goban.rows

        Rectangle {

            x: goban.x + (caseSize / 2)

            y: goban.y + (caseSize / 2) + (index * caseSize)

            width: goban.width - caseSize;

            color: "black"

            visible: (!((index === goban.rows - 1 && !limitBottom) || (index === 0 && !limitTop)))

            height: 1

        }
    }

    /*
     * Verticals lines
     */
    Repeater {
        model: goban.columns

        Rectangle {

            x: goban.x + (caseSize / 2) + (index * caseSize)

            y: goban.y + (caseSize / 2)

            height: goban.height - caseSize;

            color: "black"

            width: 1

            visible: (!((index === goban.columns - 1 && !limitRight) || (index === 0 && !limitLeft)));
        }
    }

    /*
     * The grid for the game.
     */
    Grid {
        id: goban
        anchors.centerIn: parent
        columns: 0
        rows : 0
        spacing: 0

        function getItemAt(x, y) {
            return repeater.itemAt(x + y * columns)
        }

        function itemAt(pos) {
            return repeater.itemAt(pos);
        }

        Repeater {
            model: goban.columns * goban.rows
            id : repeater

            Point{
                width: caseSize; height: caseSize
                id : piece

                MouseArea {

                    id: interactiveArea
                    anchors.fill: parent
                    onClicked: clickHandler(index);
                }

            }
        }
    }
}
