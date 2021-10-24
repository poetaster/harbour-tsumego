import QtQuick 2.0
import Sailfish.Silica 1.0

CoverBackground {
        Label {
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: icon.top
            id: label
            height: Theme.itemSizeLarge
            text: "Tsumego"
            color: Theme.primaryColor
            font.pixelSize: Theme.fontSizeMedium

        }
        Image {
            id: icon
            anchors.centerIn: parent
            source: Qt.resolvedUrl("/usr/share/icons/hicolor/86x86/apps/openrepos-tsumego.png")
            //width: parent.width / 2
            height: Theme.itemSizeLarge
            //sourceSize.width: parent.width / 2
            fillMode: Image.PreserveAspectFit
        }
}
