# FIXME: 2to3
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
    QHBoxLayout, QVBoxLayout, QMainWindow,
    QLCDNumber
)

class DemoInstrumentWindow(QMainWindow):
    name = "EPQIS16 Demonstration Instrument"
    communicator = None

    def __init__(self, parent=None):
        super(DemoInstrumentWindow, self).__init__(parent)
        self.setWindowTitle(self.name)

        vbox = QVBoxLayout()

        self._counts_widget = QLCDNumber()
        vbox.addWidget(self._counts_widget)

        voltage_layout = QHBoxLayout()
        self._voltage_label = QLabel()
        voltage_layout.addWidget(self._voltage_label)
        self._voltage_label.setText("0")
        voltage_layout.addWidget(QLabel(" VOLTS"))
        vbox.addLayout(voltage_layout)

        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)

        self.resize(400, 100)

    def send(self, fmt, *args, **kwargs):
        self.communicator.send(fmt.format(*args, **kwargs).encode("ascii"))

    def on_new_command(self, cmd):
        args = [arg.decode("ascii") for arg in cmd.split(" ".encode("ascii"))]

        if args[0] == "*IDN?":
            self.send("{}\n", self.name)
        elif args[0] == "COUNTS?":
            self.send("{}\n", self._counts_widget.value())
        elif args[0] == "VOLTS?":
            self.send("{}\n", self._voltage_label.text())
        elif args[0] == "VOLTS":
            # This command takes mV, but is named and displays V... tricky!
            self._voltage_label.setText("{}".format(float(args[1]) / 1000))
        else:
            self.send("ERR\n")

class SocketCommunicator(QObject):
    def __init__(self, connection, parent=None):
        self._connection = connection
        super(SocketCommunicator, self).__init__(parent)

    new_command = pyqtSignal(str if sys.version_info.major <= 2 else bytes)
    recv_buffer = bytes()
    send_buffer = bytes()
    running = True

    def send(self, data):
        self.send_buffer += data
        print(self.send_buffer)

    def loop(self):
        while self.running:
            try:
                self.recv_buffer += self._connection.recv(1024)
            except socket.timeout:
                pass
            except socket.error as ex:
                if ex.errno != errno.EWOULDBLOCK:
                    raise

            if bytes("\n".encode("ascii")) in self.recv_buffer:
                cmd, self.recv_buffer = self.recv_buffer.split("\n".encode("ascii"), 2)
                self.new_command.emit(cmd.strip())


            if self.send_buffer:                
                self._connection.sendall(self.send_buffer)
                self.send_buffer = bytes()


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
    listen_socket.settimeout(1.0)
    listen_socket.bind(('', port))
    listen_socket.listen(0)

    # Now we cycle through and wait for a connection.
    print("Waiting for a connection from InstrumentKit on port {}...".format(port), end='')
    try:
        sys.stdout.flush()
    except:
        pass
    while True:
        try:
            connection, address = listen_socket.accept()
            break
        except socket.timeout as ex:
            print(".", end='')
            try:
                sys.stdout.flush()
            except:
                pass

    print("\nInstrumentKit connected, opening instrument!")
    connection.settimeout(0.2)


    app = QApplication(sys.argv)

    root = DemoInstrumentWindow()

    socket_thread = QThread()
    socket_communicator = SocketCommunicator(connection)
    socket_communicator.moveToThread(socket_thread)
    socket_thread.started.connect(socket_communicator.loop)
    socket_communicator.new_command.connect(root.on_new_command)

    root.communicator = socket_communicator

    QTimer.singleShot(0, socket_thread.start)

    root.show()

    sys.exit(app.exec_())
