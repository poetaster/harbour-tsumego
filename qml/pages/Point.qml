import QtQuick 2.0

Item {

    /**
     * A mark on the stone for identify it easily.
     */
    property bool mark: false

    /*
     * Make the stone appear.
     */
    function put(isWhite, animation) {
        if (animation) {
            state = "shown";
        } else {
            piece.opacity = 1;
            piece.scale = 1;
            state = "";
        }
        piece.type = isWhite ? "white" : "black";
    }

    /**
     * Make the stone disappear.
     */
    function remove(animation) {
        if (animation) {
            state = "remove"
        } else {
            piece.type = "";
            state = "";
        }
    }

    /*
     * return the current stone type.
     */
    function getType() {
        if (state == "remove")  {
            return "";
        } else {
            return piece.type;
        }
    }

    states: [
        State {
            name: "shown"
            PropertyChanges  { target: piece; opacity:1 }
        }, State {
            name: "remove"
            onCompleted: piece.type = "";
        }
    ]

    transitions: [
        Transition {
            to: "remove"
            NumberAnimation {
                targets: piece;
                property: "opacity";
                from: 1;
                to: 0
                duration: 500;
            }
        },
        Transition {
            to: "shown"
            PropertyAnimation {
                target: piece;
                property: "scale";
                from: 0;
                to: 1
                easing.type: Easing.OutBack
            }
        }
    ]

    Image {
        id: piece
        anchors.fill: parent
        source: getImageForType();

        property string type: "";

        function getImageForType() {
            if ("" === type) {
                return ""
            }
            return "../content/gfx/" + type + ".png"
        }

    }
}
