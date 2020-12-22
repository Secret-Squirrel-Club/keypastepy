#!/usr/bin/env python3

from sqlite3.dbapi2 import Connection

from PyQt5.QtCore import QThread
from keypaste.sql_wrapper import Sqler
from keypaste.formulate_queries import (
    FormulateInsertData,
    FormulateViewQuery,
    FormulateDeleteEntry,
)
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

class CloneThread(QThread):
    
    def __init__(self) -> None:
        super.__init__(self)
    
    def run(self):
        pass
class EntryGUI(BaseGUIBuilder):
    def __init__(self, sql_client: Sqler):
        super().__init__()
        self.key_input = QLineEdit()
        self.paste_input = QLineEdit()
        self.sql_client = sql_client
        self.sql_conn = sql_client.connect_to_db()
        self._create_entry_widgets()

    def _cancel_app(self):
        self.debug("Killing App via cancel button")
        self.exit_app()

    def _start_event(self):
        self.debug(f"Inserting data into database \
                   {self.key_input.text()} as command\
                   {self.paste_input.text()} as key")
        insert_query = FormulateInsertData().query("keypaste",
                                                   self.key_input.text(),
                                                   self.paste_input.text())
        self.debug(f"Running query {insert_query}")
        self.sql_client.execute_sql(self.sql_conn, insert_query)
        self.debug("Successfully ran query into database")
        self.debug("Killing Entry app cause operation is done")
        self.exit_app()

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
    def __init__(self, sql_client: Sqler):
        super().__init__()
        self.sql_client = sql_client
        self.sql_conn = sql_client.connect_to_db()
        self.combo = QComboBox()
        self._create_delete_widgets()

    def _cancel_app(self):
        self.debug("Cancelled via cancel button")
        self.exit_app()

    def _start_event(self):
        current_text = self.combo.currentText()
        delete_query = FormulateDeleteEntry().query("keypaste", current_text)
        self.debug(f"Using Delete Query: {delete_query}")
        self.sql_client.execute_sql(self.sql_conn, delete_query)
        self.debug("Deleted entry")
        self.debug("Delete Operation is complete, Closing app")
        self.exit_app()

    def add_items_to_combo(self):
        view_query = FormulateViewQuery().query('keypaste')
        data = self.sql_client.execute_sql(self.sql_conn, view_query)
        for key, paste in data:
            self.combo.addItem(key)

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
    def __init__(self, sql_client: Sqler): 
        super().__init__()
        self.sql_client = sql_client
        self.sql_conn = sql_client.connect_to_db()
        self._create_viewer()

    def _cancel_app(self):
        self.debug("Canceled app via cancel button")
        self.exit_app()

    def _create_viewer(self):
        self.debug("Creating Viewer Widget")
        view_query = FormulateViewQuery().query('keypaste')
        self.debug(f"Executing view query {view_query}")
        data = self.sql_client.execute_sql(self.sql_conn, view_query)
        dlgLayout = QVBoxLayout()
        formLayout = QFormLayout()
        for key, paste in data:
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
