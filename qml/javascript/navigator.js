.pragma library

function getCurrentAction(path, tree) {

    var way = tree;
    var ended = false;

    /*
     * Get the action pointed by the path.
     */
    path.forEach( function(element, index, array) {
        if (!ended && element < way.length) {
            way = way[element];
        } else {
            ended = true;
        }
    });

    if ( !ended ) {
        return way;
    } else {
        return undefined;
    }

}

/**
  * return the next move to play in the tree.
  */
function getMove(color, tree) {

    var element;

    if (color) {
        element = tree.W;
    } else {
        element = tree.B;
    }

    if (element !== undefined) {
        return element[0];
    }
    return undefined;

}

/*
 * return true if the branch is wrong.
 */
function isWrong(branch) {
    return (["WV", "TR"].some(function (element, index, array){
        return branch.hasOwnProperty(element);
    }))
}

function getNextMove(path, tree, player) {

    if (path === undefined) {
        return false;
    }

    var way = getCurrentAction(path, tree);
     if (Array.isArray(way)) {
         /* get all the possibilities, except the one which are mark wrong */
         var filtered = way.filter(function callback(element) {
             return !isWrong(element[0]);
         });
         var newIndex = Math.ceil(Math.random() * filtered.length) - 1;
         return getMove(player, filtered[newIndex][0]);

     } else {
         return getMove(player, way);
     }
}

/**
 * Compare the player move with the level tree, and check if the player move is allowed.
 * return undefined if the move was not in the level, or return the new path.
 */
function checkAction(path, tree, player, playedPosition, action) {

    if (path === undefined) {
        return false;
    }

    var way = getCurrentAction(path, tree);
    var pathIndex;
    var properties = {};

    if (Array.isArray(way)) {
        /*
         * We have choice between different possibilities.
         * We check each of them to get the player action.
         */
        if (way.some( function(element, index, array) {

            /*
             * Increment the path to the next position, and check the expected
             * result.
             */
            path.push(index);
            var next = getCurrentAction(path, tree)[0];

            var expectedIndex = getMove(player, next);

            if (playedPosition === expectedIndex) {

                /*
                 * Check for wrong variation.
                 */
                if  (isWrong(next)) {
                    properties.wrong = true;
                }

                path.push(0);
                return true;
            }

            /*
             * The position was not the expected one. Restore the path to the
             * original one.
             */
            path.pop();
            return false;

        })) {
            /*
             * We got the rigth action. Now, get the next position in the path.
             */
            pathIndex = path.length - 1;
            path[pathIndex] = path[pathIndex] + 1;
            action(path, properties);
            return true;
        }
    } else {

        /*
         * We only have one possibility, return it.
         */
        var move = getMove(player, way);
        if (move === playedPosition) {
            /*
             * The player played the good move.
             */
            pathIndex = path.length - 1;
            path[pathIndex] = path[pathIndex] + 1;
            action(path, properties);
            return true;
        }
    }
    return false;

}

/**
 * Play the computer action.
 * path: the current path
 * tree: the level
 * player: the current player
 * addPiece: function called with the new move and the new path.
 */
function playComputer(path, tree, player, addPiece) {

    var way = getCurrentAction(path, tree);

    var newPath;

    if (Array.isArray(way)) {
        /* We have differents branches. We take one at random.
         */
        var newIndex = Math.ceil(Math.random() * way.length) - 1;
        newPath = way[newIndex][0]; /* the player move (index 0) */
        path.push(newIndex, 1); /* return the oponent move (index 1)*/
    } else {
        var pathIndex;
        pathIndex = path.length - 1;
        path[pathIndex] = path[pathIndex] + 1;
        newPath = way;
    }
    var move = getMove(!player, newPath);
    addPiece(move, path);
}

function undo(path) {
    var way = getCurrentAction(path, tree);

}
