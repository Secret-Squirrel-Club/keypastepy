#!/usr/bin/env python3

import sys
import rumps
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QDialogButtonBox,
    QComboBox,
    QLabel,
)
from keypaste.keypaste import Keypaste
from keypaste.base import (
    BaseKeyClass, KeyPasteException,
)


class BaseGUIBuilder(BaseKeyClass):
    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.window.setWindowTitle("Keypaste")
        self.window.setGeometry(100, 100, 200, 200)

    def show_window(self):
        self.window.show()

    def run_event_loop(self):
        sys.exit(self.app.exec())

    def _start_event(self):
        pass

    def exit_app(self):
        self.app.exit()


class EntryGUI(BaseGUIBuilder):

    def __init__(self, menu):
        super().__init__()
        self.key_input = QLineEdit()
        self.paste_input = QLineEdit()
        self.menu = menu
        self._create_entry_widgets()

    def _cancel_app(self):
        self.debug("Killing App via cancel button")
        self.exit_app()

    def _start_event(self):
        self.debug(f"Inserting data into database \
                    {self.key_input.text()} as command\
                    {self.paste_input.text()} as key")
        keypaste = Keypaste(
            self.key_input.text(),
            self.paste_input.text()
        )
        try:
            self.pickle.append_and_reload(keypaste)
        except KeyPasteException:
            self.debug("Key is already in there")
            self.window.close()
        self.debug("Successfully ran query into database")
        self.debug("Updating app with new entries")
        pastes = self.menu.get("Pastes")
        if not self.copy_clipboard:
            self.debug("Config says to use write to screen")
            menu_add = rumps.MenuItem(
                title=keypaste.get_command(),
                callback=keypaste.write
                )
        else:
            self.debug("Config says to copy to buffer")
            menu_add = rumps.MenuItem(
                title=keypaste.get_command(),
                callback=keypaste.copy_to_clipboard
            )
        pastes.add(menu_add)
        self.debug("Killing Entry app cause operation is done")
        self.window.close()

    def _create_entry_widgets(self):
        self.debug("Starting entry widgets")
        dlgLayout = QVBoxLayout()
        formLayout = QFormLayout()
        formLayout.addRow("Key:", self.key_input)
        formLayout.addRow("Paste:", self.paste_input)
        dlgLayout.addLayout(formLayout)
        btns = QDialogButtonBox()
        btns.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok
        )

        btns.accepted.connect(self._start_event)
        btns.rejected.connect(self._cancel_app)
        dlgLayout.addWidget(btns)

        self.window.setLayout(dlgLayout)
        self.show_window()
        self.run_event_loop()


class DeleteEntryGUI(BaseGUIBuilder):
    def __init__(self, menu):
        super().__init__()
        self.combo = QComboBox()
        self.menu = menu
        self._create_delete_widgets()

    def _cancel_app(self):
        self.debug("Cancelled via cancel button")
        self.exit_app()

    def _start_event(self):
        current_text = self.combo.currentText()
        self.debug(f"Deleting {current_text}")
        self.pickle.delete_and_reload(current_text)
        self.debug("Deleted from menu")
        pastes = self.menu.get("Pastes")
        del pastes[current_text]
        self.debug("Deleted entry")
        self.debug("Delete Operation is complete, Closing app")
        self.exit_app()

    def add_items_to_combo(self):
        data = self.pickle.view_all()
        for tup in data:
            self.combo.addItem(tup[0])

    def _create_delete_widgets(self):
        self.debug("Creating deleting widgets")
        dlgLayout = QVBoxLayout()
        formLayout = QFormLayout()
        self.add_items_to_combo()
        formLayout.addRow("Key:", self.combo)
        dlgLayout.addLayout(formLayout)
        btns = QDialogButtonBox()
        btns.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok
        )
        btns.accepted.connect(self._start_event)
        btns.rejected.connect(self._cancel_app)
        dlgLayout.addWidget(btns)
        self.window.setLayout(dlgLayout)
        self.show_window()
        self.run_event_loop()


class ViewEntriesGUI(BaseGUIBuilder):
    def __init__(self):
        super().__init__()
        self._create_viewer()

    def _cancel_app(self):
        self.debug("Canceled app via cancel button")
        self.exit_app()

    def _create_viewer(self):
        self.debug("Creating Viewer Widget")
        data = self.pickle.view_all()
        dlgLayout = QVBoxLayout()
        formLayout = QFormLayout()
        formLayout.addRow(QLabel("Hot Key"), QLabel("Paste"))
        for tup in data:
            formLayout.addRow(QLabel(f"{tup[0]}"), QLabel(tup[1]))
        dlgLayout.addLayout(formLayout)
        btns = QDialogButtonBox()
        btns.setStandardButtons(
            QDialogButtonBox.Cancel
        )
        btns.rejected.connect(self._cancel_app)
        dlgLayout.addWidget(btns)
        self.window.setLayout(dlgLayout)

        self.show_window()
        self.run_event_loop()
