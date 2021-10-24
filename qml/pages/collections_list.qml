import QtQuick 2.0
import Sailfish.Silica 1.0

import io.thp.pyotherside 1.3

Page {
    width: Screen.width; height: Screen.height;

    signal openCollection(string path);

    Column {
        Text {
            id: txt;
            text: qsTr("Select the collection to open");

        }

        SilicaListView {

            width: parent.width; height: Screen.height;

            model: ListModel {id: levelsList}

            delegate: ListItem {
                Label {
                    text: name
                }
                onClicked: {
                    openCollection(path);
                    pageStack.pop()
                }

            }
        }

    }


    Python {
        id:py
        Component.onCompleted: {
            var pythonpath = Qt.resolvedUrl('../python').substr('file://'.length);
            addImportPath(pythonpath);
            console.log(pythonpath);

            importModule('configuration', function() {
                console.log('module loaded');
                console.log('Python version: ' + pythonVersion());
            });

            setHandler('log', function (content) {
                console.log(content);
            });

            call('configuration.get_levels', [pythonpath + "/../content", StandardPaths.documents + "/tsumego"], function(result) {
                result.forEach(function(elem) {
                    console.log(elem);
                    levelsList.append(elem);
                })
            });
        }
    }

}
