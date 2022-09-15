"""settings.settings module"""
import logging
import sys

import darkdetect
from fbs_runtime.application_context.PyQt6 import ApplicationContext
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QApplication, QDialog
from qt_material import apply_stylesheet

app = QApplication(sys.argv)
app_context = ApplicationContext()


class SettingsDialog(QDialog):
    """
    Class for the settings dialog with all its components and functions.
    """

    def __init__(self, parent=None) -> None:
        """
        The __init__ function is called automatically every time
        the class is being used to create a new object.
        The first argument of every class method, including init,
        is always a reference to the current instance of the class.
        By convention, this argument is always named self.
        In init __self__ refers to the newly created object; in other
        class methods, it refers to the instance whose method was called.

        :param self: Used to Access the attributes and methods of the class.
        :param parent=None: Used to Ensure that the dialog box does not close when it is launched.
        :return: None.
        """

        super().__init__(parent)
        uic.loadUi(
            app_context.get_resource("forms/settings_dialog.ui"),
            self,
        )
        self.setWindowIcon(QIcon(app_context.get_resource("icon/youtube-play.icns")))
        self.setFont(QFont("Roboto"))
        self.radioButton_OS.clicked.connect(self.change_theme)
        self.radioButton_white.clicked.connect(self.change_theme)
        self.radioButton_dark.clicked.connect(self.change_theme)
        self.pushButton_change_option1.clicked.connect(
            self.change_button_option1_clicked
        )
        self.pushButton_change_option2.clicked.connect(
            self.change_button_option2_clicked
        )
        self.pushButton_change_option3.clicked.connect(
            self.change_button_option3_clicked
        )
        self.pushButton_change_option4.clicked.connect(
            self.change_button_option4_clicked
        )
        self.pushButton_change_option5.clicked.connect(
            self.change_button_option5_clicked
        )
        self.pushButton_change_option6.clicked.connect(
            self.change_button_option6_clicked
        )
        self.pushButton_change_option7.clicked.connect(
            self.change_button_option7_clicked
        )
        self.pushButton_change_option8.clicked.connect(
            self.change_button_option8_clicked
        )
        self.pushButton_change_option9.clicked.connect(
            self.change_button_option9_clicked
        )
        self.pushButton_change_option10.clicked.connect(
            self.change_button_option10_clicked
        )
        self.pushButton_change_option11.clicked.connect(
            self.change_button_option11_clicked
        )
        self.pushButton_change_option12.clicked.connect(
            self.change_button_option12_clicked
        )

    def load_settings(self, settings_dict: dict) -> None:  # FIXME doesn't work yet
        """
        The load_settings function loads the settings from a dictionary into the dialog.
        The function takes one argument, which is a dictionary containing all of the settings.

        :param self: Used to Access variables, methods etc in the rest of the class.
        :param settings_dict:dict: Used to Pass the settings_dict to the function.
        :return: None.
        """
        open_url_automatically = settings_dict["general"][0]["openURLautomatically"]
        copy_url_to_clipboard = settings_dict["general"][0]["copyURLtoClipboard"]
        program_language = settings_dict["general"][0]["programLanguage"]

        shortcut_new_playlist = settings_dict["keyboard_shortcuts"][0]["newPlaylist"]
        shortcut_open_playlist = settings_dict["keyboard_shortcuts"][0]["openPlaylist"]
        shortcut_save_playlist = settings_dict["keyboard_shortcuts"][0]["savePlaylist"]
        shortcut_add_item = settings_dict["keyboard_shortcuts"][0]["addItem"]
        shortcut_delete_item = settings_dict["keyboard_shortcuts"][0]["deleteItem"]
        shortcut_rename_item = settings_dict["keyboard_shortcuts"][0]["renameItem"]
        shortcut_shuffle_playlist = settings_dict["keyboard_shortcuts"][0][
            "shufflePlaylist"
        ]

        shortcut_generate_playlist = settings_dict["keyboard_shortcuts"][0][
            "generatePlaylist"
        ]
        shortcut_count_items = settings_dict["keyboard_shortcuts"][0]["countItems"]
        shortcut_clear_all_items = settings_dict["keyboard_shortcuts"][0][
            "clearAllItems"
        ]
        shortcut_get_video_information = settings_dict["keyboard_shortcuts"][0][
            "getVideoInformation"
        ]
        shortcut_remove_duplicates = settings_dict["keyboard_shortcuts"][0][
            "removeDuplicates"
        ]
        shortcut_copy_url = settings_dict["keyboard_shortcuts"][0]["copyURL"]

        self.comboBox_language.setCurrentText(program_language)

        if open_url_automatically is True:
            self.checkBox_option1.setCheckState(Qt.CheckState.Checked)

        elif open_url_automatically is False:
            self.checkBox_option1.setCheckState(Qt.CheckState.Unchecked)

        if copy_url_to_clipboard is True:
            self.checkBox_option2.setCheckState(Qt.CheckState.Checked)

        elif copy_url_to_clipboard is False:
            self.checkBox_option2.setCheckState(Qt.CheckState.Unchecked)

        self.label_keyboard_shortcuts_option1.setText(shortcut_new_playlist)
        self.label_keyboard_shortcuts_option2.setText(shortcut_open_playlist)
        self.label_keyboard_shortcuts_option3.setText(shortcut_save_playlist)
        self.label_keyboard_shortcuts_option4.setText(shortcut_add_item)
        self.label_keyboard_shortcuts_option5.setText(shortcut_delete_item)
        self.label_keyboard_shortcuts_option6.setText(shortcut_rename_item)
        self.label_keyboard_shortcuts_option7.setText(shortcut_shuffle_playlist)
        self.label_keyboard_shortcuts_option8.setText(shortcut_generate_playlist)
        self.label_keyboard_shortcuts_option9.setText(shortcut_count_items)
        self.label_keyboard_shortcuts_option10.setText(shortcut_clear_all_items)
        self.label_keyboard_shortcuts_option11.setText(shortcut_get_video_information)
        self.label_keyboard_shortcuts_option12.setText(shortcut_remove_duplicates)
        self.label_keyboard_shortcuts_option13.setText(shortcut_copy_url)

    def change_theme(self) -> None:
        """
        The change_theme function changes the theme of the application.
        It is called when a user clicks on one of three radio buttons,
        which are used to select between three different themes: OS theme, white and dark.

        :param self: Used to Access the attributes and methods of the class in python.
        :return: None.
        """
        if self.radioButton_OS.isChecked():
            if darkdetect.isDark():
                apply_stylesheet(
                    app, theme=app_context.get_resource("theme/yt-dark-red.xml")
                )
            elif darkdetect.isLight():
                apply_stylesheet(
                    app,
                    theme=app_context.get_resource("theme/yt-white-red.xml"),
                    invert_secondary=True,
                )
            logging.debug("Theme regarding to OS theme set: %s", darkdetect.theme())
        elif self.radioButton_white.isChecked():
            apply_stylesheet(
                app,
                theme=app_context.get_resource("theme/yt-white-red.xml"),
                invert_secondary=True,
            )
            logging.debug("White theme set!")
        elif self.radioButton_dark.isChecked():
            apply_stylesheet(
                app, theme=app_context.get_resource("theme/yt-dark-red.xml")
            )
            logging.debug("Dark theme set!")

    def change_language(self) -> None:
        """
        The change_language function will change the language in runtime.

        :param self: Used to Reference the instance of the object itself.
        :return: None.
        """
        logging.debug("This will change the language...")

    def change_button_option1_clicked(self) -> None:
        """Get text from keySequenceEdit field and display in label."""
        if self.keySequenceEdit.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option1.setText(
                self.keySequenceEdit.keySequence().toString()
            )

    def change_button_option2_clicked(self) -> None:
        """Get text from keySequenceEdit field and display in label."""
        if self.keySequenceEdit.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option2.setText(
                self.keySequenceEdit.keySequence().toString()
            )

    def change_button_option3_clicked(self) -> None:
        """Get text from keySequenceEdit field and display in label."""
        if self.keySequenceEdit.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option3.setText(
                self.keySequenceEdit.keySequence().toString()
            )

    def change_button_option4_clicked(self) -> None:
        """Get text from keySequenceEdit field and display in label."""
        if self.keySequenceEdit.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option4.setText(
                self.keySequenceEdit.keySequence().toString()
            )

    def change_button_option5_clicked(self) -> None:
        """Get text from keySequenceEdit field and display in label."""
        if self.keySequenceEdit.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option5.setText(
                self.keySequenceEdit.keySequence().toString()
            )

    def change_button_option6_clicked(self) -> None:
        """Get text from keySequenceEdit field and display in label."""
        if self.keySequenceEdit.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option6.setText(
                self.keySequenceEdit.keySequence().toString()
            )

    def change_button_option7_clicked(self) -> None:
        """Get text from keySequenceEdit field and display in label."""
        if self.keySequenceEdit.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option7.setText(
                self.keySequenceEdit.keySequence().toString()
            )

    def change_button_option8_clicked(self) -> None:
        """Get text from keySequenceEdit field and display in label."""
        if self.keySequenceEdit.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option8.setText(
                self.keySequenceEdit.keySequence().toString()
            )

    def change_button_option9_clicked(self) -> None:
        """Get text from keySequenceEdit field and display in label."""
        if self.keySequenceEdit.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option9.setText(
                self.keySequenceEdit.keySequence().toString()
            )

    def change_button_option10_clicked(self) -> None:
        """Get text from keySequenceEdit field and display in label."""
        if self.keySequenceEdit.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option10.setText(
                self.keySequenceEdit.keySequence().toString()
            )

    def change_button_option11_clicked(self) -> None:
        """Get text from keySequenceEdit field and display in label."""
        if self.keySequenceEdit.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option11.setText(
                self.keySequenceEdit.keySequence().toString()
            )

    def change_button_option12_clicked(self) -> None:
        """Get text from keySequenceEdit field and display in label."""
        if self.keySequenceEdit.keySequence().toString() != "":
            self.label_keyboard_shortcuts_option12.setText(
                self.keySequenceEdit.keySequence().toString()
            )
