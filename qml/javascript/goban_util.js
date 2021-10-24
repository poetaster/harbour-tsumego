.pragma library

/**
 * Check if the case on the grid belongs to the first column.
 */
function isFirstCol(index, cols) {
    return index % cols == 0;
}

/**
 * Check if the case on the grid belongs to the last column.
 */
function isLastCol(index, cols) {
    return  index % cols == cols - 1;
}

/**
 * Check if the case on the grid belongs to the first row
 */
function isFirstRow(index, cols) {
    return index < cols;
}

/**
 * Check if the case on the grid belongs to the last row.
 */
function isLastRow(index, cols, rows) {
    return cols * (rows - 1) <= index;
}

/**
 * Get all the neighbors for a given position.
 */
function getNeighbors(index, cols, rows) {

    var neighbors = [];
    if (!isFirstCol(index, cols)) {
        neighbors.push(index - 1)
    }

    if (!isLastCol(index, cols)) {
        neighbors.push(index + 1)
    }

    if (!isFirstRow(index, cols)) {
        neighbors.push(index - cols)
    }

    if (!isLastRow(index, cols, rows)) {
        neighbors.push(index + cols)
    }

    return neighbors;
}



function getChainToRemove(index, grid, filter) {

    var piecesToCheck = [];
    var piecesToRemove = [];

    /*
     * filter wich keep only free places.
     */
    function freePlaces(x) {
        return grid.itemAt(x).getType() === "";
    }

    var piece = index;
    while (piece !== undefined) {

        /* if the case has already been marked, do not check it again.
         */
        if (!grid.itemAt(piece).mark) {
            grid.itemAt(piece).mark = true;
            piecesToRemove.push(piece);

            var neighbors = getNeighbors(piece, grid.columns, grid.rows);

            if (neighbors.length !== 0) {
                /*
                 * If the place has liberty, return empty list.
                 */
                if (neighbors.some(freePlaces)) {
                    return [];
                }

                /*
                 * Now update the check list.
                 */
                neighbors.filter(filter).forEach(function(x) {
                    piecesToCheck.push(x)
                });

            }
        } else {
            /*
             * The piece may have been marked outside of this call.
             * (We try to check chain in each direction, and return as soon as
             * we find an empty place).
             * If the piece is marked, but does not belongs to the piecesToRemove,
             * we assume the piece is connected to a living chain, and
             * subsequently this chain too.
             */
            if (! piecesToRemove.some(function(x) { return x === piece})) {
                return [];
            }
        }

        piece = piecesToCheck.pop();
    }
    return piecesToRemove;

}

/*
 * Undo a move on the board.
 */
function undo(grid, step) {

    /*
     * Fill the space with the given color.
     */
    function fillWith(index, color) {

        /*
         * filter wich keep only free places.
         */
        function freePlaces(x) {
            return grid.itemAt(x).getType() === "";
        }

        var piece = index;

        var space = [];

        while (piece !== undefined) {

            var point = grid.itemAt(piece);

            if (point.mark || !point.getType === "") {
                piece = space.pop();
                continue;
            }
            point.mark = true;

            point.put(color, false);

            getNeighbors(piece, grid.columns, grid.rows).filter(freePlaces).forEach(function(x) {
                space.push(x);
            });
            piece = space.pop();
        }
    }

    /*
     * First add each point marked as removed.
     * Only the first point is recorded, so we fill all the other points
     */

    if (step.suicide) {
        fillWith(step.added, step.player);
    } else {
        if (step.removed !== undefined) {
            step.removed.forEach(function(point){
                fillWith(point, !step.player);
            });
        }
        grid.itemAt(step.added).remove(false);
    }

    clearMarks(grid);
}

/**
 * Add a new stone on the goban.
 *
 * Check if there are dead chained and remove them from the goban.
 *
 * index(int):          the index where put the stone.
 * grid(object):        the grid where to put the stone:
 *  - grid.rows:        number of rows in the grid
 *  - grid.columns:     number of columes in the grid
 *  - grid.itemAt(index) should return the stone a the given index
 * currentPlayer(bool): player color
 * animation(bool):     should we add animation on the goban
 * allowSuicide(bool):  if suicide an autorized action
 *
 * return a step object if the movement has been allowed.
 */
function addPiece(index, grid, currentPlayer, animation, allowSuicide, allowOveride) {

    var point = grid.itemAt(index);
    var elementType = point.getType();

    if (!allowOveride && elementType !== "") {
        return undefined;
    }

    var neighbors = getNeighbors(index, grid.columns, grid.rows);

    var step = {};
    step.added = index;
    step.player = currentPlayer;

    function isPlayer(x) {
        return grid.itemAt(x).getType() === (currentPlayer ? "white" : "black");
    }

    function isOponnent(x) {
        return grid.itemAt(x).getType() === (currentPlayer ? "black" : "white");
    }

    function freeOrChain(x) {
        var pointType = grid.itemAt(x).getType();
        return pointType === "" || pointType === (currentPlayer ? "white" : "black");
    }

    point.put(currentPlayer, animation);

    if (neighbors.length === 0) {
        return step;
    }

    step.removed = [];
    var somethingToRemove = false;
    var movementAutorized = true;

    /*
     * Check for pieces to remove.
     */
    neighbors.forEach(function(neighbor) {

        if (!isOponnent(neighbor)) {
            return;
        }

        var piecesToRemove = getChainToRemove(neighbor, grid, isOponnent);
        if (piecesToRemove.length !== 0) {
            step.removed.push(neighbor);
            somethingToRemove = true;
            piecesToRemove.forEach(function(x) {
                grid.itemAt(x).remove(animation);
            });
        }
    });

    /*
     * Check for suicide.
     */
    if (!somethingToRemove) {
        var suicides = getChainToRemove(index, grid, isPlayer);
        if (suicides.length !== 0) {
            if (allowSuicide) {

                step.suicide = true;

                suicides.forEach(function(x) {
                    grid.itemAt(x).remove(animation);
                });
            } else {
                point.remove(false);
                movementAutorized = false;
            }
        }

    }

    /* We do not need to clear the marks before as we are not filtering the
     * same pieces.
     */
    clearMarks(grid);

    if (movementAutorized) {
        return step;
    } else {
        return undefined;
    }
}


/*
 * Remove the marks in the cases.
 *
 * Some functions add marks on each stone in order to prevent infinite looping.
 * We need to clean the cases before any new action.
 *
 */
function clearMarks(grid) {
    for (var i = 0; i < grid.columns * grid.rows; i++) {
        grid.itemAt(i).mark = false;
    }
}
