class Style:

    @staticmethod
    def get_window_style():
        return "QWidget {\
            background-color: white;\
            text-align: center;\
        }"

    @staticmethod
    def get_button_style():
        return "QPushButton {\
            background-color: lightgray;\
            border: 4px solid lightgray;\
            border-radius: 4px;\
            text-align: center;\
            font-size: 11pt;\
            font-family: Tahoma;\
            color: black;\
        }\
        QPushButton::hover {\
            background-color: gray;\
            border: 4px solid gray;\
            border-radius: 4px;\
            color: white;\
        }"

    @staticmethod
    def get_text_style():
        return "QWidget {\
            background-color: white;\
            text-align: center;\
            font-size: 11pt;\
            font-family: Tahoma;\
        }"

    @staticmethod
    def get_list_style():
        return "QComboBox {\
            background-color: lightgray;\
            border: 4px solid lightgray;\
            border-radius: 4px;\
            padding: 1px 18px 1px 3px;\
            text-align: center;\
            font-size: 11pt;\
            font-family: Tahoma;\
            color: black;\
        }\
        QComboBox:!editable {\
            background: lightgray;\
            color: black;\
        }\
        QComboBox:!editable:on {\
            background: lightgray;\
            color: black;\
        }\
        QComboBox::drop-down {\
            border-radius: 4px;\
        }"
