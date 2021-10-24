import QtQuick 2.2
import Sailfish.Silica 1.0


Page {
    RemorsePopup { id: remorse; text: qsTr("Cleared config settings") }

    Column {
        spacing: Theme.paddingMedium
        anchors.fill: parent
        PageHeader { title: qsTr("Options") }
        SectionHeader { text: qsTr("Configuration Values") }
        DetailItem { label: "Problem File Name"; value: conf.gameFileName}
        DetailItem { label: "Problem File Path"; value: conf.gameFile}
        DetailItem { label: "Current Problem Index"; value: conf.problemIdx + 1 }
        SectionHeader { text: qsTr("Reset") }
        Button {
            text: qsTr("Reset")
            anchors.horizontalCenter: parent.horizontalCenter
            onClicked: {
                remorse.execute( qsTr("Cleared config settings"), function () { conf.clear() } )
            }
        }
    }
}
