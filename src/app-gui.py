import sys
import webbrowser
import ssl
from urllib import request
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QClipboard
from PyQt6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QApplication,
    QWidget,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QMessageBox,
)
from qt_material import apply_stylesheet


class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("src/gui/form.ui", self)
        self.pushButton_add.clicked.connect(self.addButtonPressed)
        self.pushButton_copy.clicked.connect(self.copyButtonPressed)
        self.pushButton_import.clicked.connect(self.importButtonPressed)
        self.pushButton_export.clicked.connect(self.exportButtonPressed)
        self.pushButton_generate.clicked.connect(self.generateButtonPressed)
        self.pushButton_delete_item.clicked.connect(self.deleteItemButtonClicked)
        self.pushButton_clear_playlist.clicked.connect(self.clearPlaylistButtonClicked)
        self.listWidget_playlist_items.itemDoubleClicked.connect(self.doubleClicked)

    def doubleClicked(self, item):
        listwidget = self.listWidget_playlist_items
        for index in range(listwidget.count()):
            item = listwidget.item(index)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
        Ui.make_item_editable(self)

    def make_item_editable(self):
        index = self.listWidget_playlist_items.currentIndex()
        if index.isValid():
            item = self.listWidget_playlist_items.itemFromIndex(index)
            if not item.isSelected():
                item.setSelected(True)
            self.listWidget_playlist_items.edit(index)

    def addButtonPressed(self):
        text = self.textEdit_url_id.toPlainText()
        if text != "":
            if Ui.is_string_valid_url(self, text) and Ui.is_string_valid_youtube_url(
                self, text
            ):
                id = Ui.cut_url_to_id(self, text)
                self.listWidget_playlist_items.addItem(str(id))
            else:
                self.listWidget_playlist_items.addItem(str(text))
            self.textEdit_url_id.clear()
            self.pushButton_clear_playlist.setEnabled(True)
            self.pushButton_delete_item.setEnabled(True)
            if Ui.playlist_widget_has_enough_items(self):
                self.pushButton_generate.setEnabled(True)

    def is_string_valid_url(self, string):
        if "http://" in string or "https://" in string:
            return True

    def is_string_valid_youtube_url(self, string):
        if "watch?" in string or "be/" in string:
            return True

    def cut_url_to_id(self, url):
        if "v=" in url:
            get_id = url.split("v=")
            return get_id[-1]
        elif "be/" in url:
            get_id = url.split("be/")
            return get_id[-1]

    def playlist_widget_has_enough_items(self):
        playlist = self.listWidget_playlist_items
        playlist_items = [playlist.item(x) for x in range(playlist.count())]
        if len(playlist_items) >= 2:
            return True

    def is_playlist_widget_empty(self):
        playlist = self.listWidget_playlist_items
        playlist_items = [playlist.item(x) for x in range(playlist.count())]
        if not playlist_items:
            return True

    def disable_delete_clear_generate_buttons(self):
        self.pushButton_clear_playlist.setEnabled(False)
        self.pushButton_delete_item.setEnabled(False)
        self.pushButton_generate.setEnabled(False)

    def clearPlaylistButtonClicked(self):
        dlg = AskClearDialog(self)
        if dlg.exec():
            self.listWidget_playlist_items.clear()
            if Ui.is_playlist_widget_empty(self):
                Ui.disable_delete_clear_generate_buttons(self)
                self.pushButton_copy.setEnabled(False)
        else:
            print("No item was deleted!")

    def deleteItemButtonClicked(self):
        listItems = self.listWidget_playlist_items.selectedItems()
        if not listItems:
            return
        for item in listItems:
            self.listWidget_playlist_items.takeItem(
                self.listWidget_playlist_items.row(item)
            )
        if Ui.is_playlist_widget_empty(self):
            Ui.disable_delete_clear_generate_buttons(self)
        elif not Ui.playlist_widget_has_enough_items(self):
            self.pushButton_generate.setEnabled(False)

    def has_textedit_playlist_generated_url_content(self):
        if self.textEdit_playlist_generated_url.toPlainText() != "":
            return True

    def copyButtonPressed(self):
        text = self.textEdit_playlist_generated_url.toPlainText()
        QApplication.clipboard().setText(text)

    def importButtonPressed(self):
        import_dlg = QFileDialog(self)
        import_dlg.setWindowTitle("Please import your playlist-file")
        import_dlg.exec()

    def exportButtonPressed(self):
        export_dlg = QFileDialog(self)
        export_dlg.setWindowTitle(
            "Please define a location to export your playlist-file"
        )
        export_dlg.exec()

    def generateButtonPressed(self):
        self.textEdit_playlist_generated_url.setText("Button 'Generate' clicked!")
        if Ui.has_textedit_playlist_generated_url_content(self):
            self.pushButton_copy.setEnabled(True)
            playlist = self.listWidget_playlist_items
            playlist_items = [playlist.item(x).text() for x in range(playlist.count())]
            print(playlist_items)

            comma_seperated_string = Ui.create_comma_seperated_string(playlist_items)
            Ui.generate_video_ids_url(self, comma_seperated_string)

    def create_comma_seperated_string(list):
        return ",".join(list)

    def generate_video_ids_url(self, comma_seperated_string):
        if self.textEdit_playlist_title.toPlainText() != "":
            playlist_url = Ui.create_playlist_url_with_title(
                comma_seperated_string, self.textEdit_playlist_title.toPlainText()
            )
        else:
            playlist_url = Ui.create_playlist_url_without_title(comma_seperated_string)

        self.textEdit_playlist_generated_url.setText(playlist_url)
        Ui.open_playlist_url_in_webbrowser(playlist_url)

    def create_playlist_url_with_title(video_ids, playlist_title):
        return f"https://www.youtube.com/watch_videos?video_ids={video_ids}&title={playlist_title}"

    def create_playlist_url_without_title(video_ids):
        return f"https://www.youtube.com/watch_videos?video_ids={video_ids}"

    def generate_playlist_url(video_ids_url):
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
            response = request.urlopen(video_ids_url)

            playlist_link = response.geturl()
            playlist_link = playlist_link.split("list=")[1]

            config.youtube_generated_playlist_url = (
                f"https://www.youtube.com/playlist?list={playlist_link}"
                + "&disable_polymer=true"
            )
            return True
        except Exception as error:
            print(
                "\nThere was an error with creating the playlist url. Check if all video ids are valid and correct.\n"
            )
            return False

    def open_url_in_webbrowser(url):
        print(f"\nOpening {url} in new Web browser tab...\n")
        webbrowser.open_new_tab(url)

    def open_playlist_url_in_webbrowser(playlist_url):
        Ui.open_url_in_webbrowser(playlist_url)


class AskClearDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Are you sure?")
        self.setFixedSize(450, 140)

        QBtn = QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(
            "Do you really want to clear your playlist? That deletes all of your items!"
        )
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


def main():
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme="dark_red.xml")
    window = Ui()
    window.show()  # show window
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
