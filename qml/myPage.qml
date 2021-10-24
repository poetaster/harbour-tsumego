import QtQuick 2.0
import Sailfish.Silica 1.0


// MyPage.qml
Page {
        Text { text: "Page " + pageStack.depth }

        Button {
            text: "Start Game"
            onClicked: pageStack.push("pages/Board.qml")

            anchors.centerIn: parent;


        }
}
