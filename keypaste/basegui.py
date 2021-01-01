#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QDialogButtonBox,
    QComboBox,
    QLabel

)
from keypaste.base import BaseKeyClass


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
    def __init__(self):
        super().__init__()
        self._create_entry_widgets()

    def _cancel_app(self):
        self.debug("Killing App via cancel button")
        self.exit_app()

    def _start_event(self):
        print("hope this works")

    def _create_entry_widgets(self):
        self.debug("Starting entry widgets")
        dlgLayout = QVBoxLayout()
        formLayout = QFormLayout()
        formLayout.addRow("Key:", QLineEdit())
        formLayout.addRow("Paste:", QLineEdit())
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
    def __init__(self):
        super().__init__()
        self._create_delete_widgets()

    def _cancel_app(self):
        self.exit_app()

    def _start_event(self):
        print('hope it works')

    def _make_combo(self):
        combo = QComboBox()
        return combo

    def _create_delete_widgets(self):
        self.debug("Creating deleting widgets")
        dlgLayout = QVBoxLayout()
        formLayout = QFormLayout()
        formLayout.addRow("Key:", self._make_combo())
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
        self.exit_app()

    def _create_viewer(self):
        self.debug("Createing Viewer Widget")
        testing = {"0": "Hopfully", "1": "this", "2": "works"}
        dlgLayout = QVBoxLayout()
        formLayout = QFormLayout()
        for key, paste in testing.items():
            formLayout.addRow(QLabel(f"{key}"), QLabel(paste))
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
