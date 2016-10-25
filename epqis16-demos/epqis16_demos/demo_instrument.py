from __future__ import print_function, division

import click
import sys
import socket
import errno
import time
from PyQt5.QtCore import (
    pyqtSignal, QObject, QThread, QTimer,
    QCoreApplication, QFile
)
from PyQt5.QtGui import (
    QFont
)
from PyQt5.QtWidgets import (
    QApplication, QWidget, QDialog,
    QLabel, QProgressBar,
    QHBoxLayout, QVBoxLayout, QMainWindow
)

class DemoInstrumentWindow(QMainWindow):
    def __init__(self, parent=None):
        super(DemoInstrumentWindow, self).__init__(parent)

    def on_new_command(self, cmd=None):
        print(cmd)


class SocketListener(QObject):
    def __init__(self, connection, parent=None):
        self._connection = connection
        super(SocketListener, self).__init__(parent)

    new_command = pyqtSignal(str)
    buffer = ""
    running = True

    def loop(self):
        while self.running:
            try:
                self.buffer += self._connection.recv()
            except socket.error as ex:
                if ex.errno == errno.EWOULDBLOCK:
                    pass
                else:
                    raise

            if "\n" in self.buffer:
                cmd, self.buffer = self.buffer.split("\n", 2)
                self.new_command.emit(cmd)


## COMMAND MAIN ##############################################################

@click.command()
@click.option('--port',
    type=int, help="TCP port number to listen for connections on.",
    default=8042
)
def demo_instrument(port):


    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # This is *critical* so that we don't block the GUI thread!
    # As a consequence, all calls to recv() can now raise exceptions
    # if there's no data available, so we need to check for that
    # every time.
    # TODO: move recv() calls to their own thread that can accumulate
    #       and look for \n, etc.
    listen_socket.setblocking(False)
    listen_socket.bind(('', port))
    listen_socket.listen(1)

    # Now we cycle through and wait for a connection.
    print("Waiting for a connection from InstrumentKit on port {}...".format(port), end='')
    while True:
        try:
            connection, address = listen_socket.accept()
        except socket.error as ex:
            if ex.errno == errno.EWOULDBLOCK:
                print(".", end='')
                time.sleep(1)
            else:
                raise

    print("InstrumentKit connected, opening instrument!")


    app = QApplication(sys.argv)

    root = DemoInstrumentWindow()

    socket_thread = QThread()
    socket_listener = SocketListener(connection)
    socket_listener.moveToThread(socket_thread)
    socket_thread.started.connect(socket_listener.loop)
    socket_listener.new_command.connect(root.on_new_command)

    root.show()

    sys.exit(app.exec_())
