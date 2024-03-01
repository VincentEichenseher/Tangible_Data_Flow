
from enum import Enum


class WidgetStyle(Enum):
    QMENU_ITEM_STYLE = \
        """
        QMenu {
            background-color: rgb(5, 5, 5);
            color: rgb(255,255,255);
            border: 1px solid ;
        }
    
        QMenu::item::selected {
            background-color: rgb(30, 30, 30);
        }        
        """

    QTEXTEDIT_STYLE = \
        """
        QTextEdit {
            background-color: rgb(255, 255, 255);
            color: rgb(0,0,0);
            border: 1px solid ;
        }
        """

    QLABEL_STYLE = \
        """
        QLabel { 
            background-color : black; color : white; 
        }
        """
    PALETTE_QLABEL_STYLE = \
        """
        QLabel { 
            background-color : #888; color : #FFF; 
        }
        """

    QPUSHBUTTON_STYLE = \
        """
        QPushButton {
            background-color : black; 
            border: 1px solid white;
        }
        """

    PALETTE_OUTLINE_COLOR = "#FFF"
    PALETTE_BACKGROUND_COLOR = "#000"
    PALETTE_TEXT_COLOR = "#FFF"
    BACKGROUND_COLOR = "#000"
