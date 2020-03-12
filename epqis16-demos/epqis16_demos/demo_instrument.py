# FIXME: 2to3
from __future__ import division, print_function

import errno
import socket
import sys

from collections import namedtuple

import click
from PyQt5.QtCore import (QCoreApplication, QFile, QObject, QThread, QTimer, 
                          pyqtSignal)
from PyQt5.QtWidgets import ( QApplication, QWidget,QCheckBox, QDialog,  QHBoxLayout,
                         QLabel, QLCDNumber, QMainWindow, QProgressBar,
                         QVBoxLayout)
from PyQt5.QtGui import (  QFont)


Channel = namedtuple('Channel', ['voltage', 'enable_cb', 'enable_label'])


class DemoInstrumentWindow(QMainWindow):
    name = "EPQIS16 Demonstration Instrument"
    communicator = None
    thread = None
    channels = []

    def __init__(self, parent=None):
        super(DemoInstrumentWindow, self).__init__(parent)
        self.setWindowTitle(self.name)

        vbox = QVBoxLayout()

        # self._counts_widget = QLCDNumber()
        # vbox.addWidget(self._counts_widget)

        for idx_channel in range(4):

            voltage_layout = QHBoxLayout()
            voltage_label = QLCDNumber()
            voltage_layout.addWidget(voltage_label)
            voltage_layout.addWidget(QLabel("VOLTS"))
            vbox.addLayout(voltage_layout)

            enable_layout = QHBoxLayout()
            enable_label = QLabel()
            enable_cb = QCheckBox("", self)
            enable_layout.addWidget(enable_cb)
            enable_cb.stateChanged.connect(
                lambda state, label=enable_label:
                label.setText("ON" if state else "OFF")
            )
            enable_layout.addWidget(enable_label)
            enable_label.setText("OFF")


            vbox.addLayout(enable_layout)

            channel = Channel(
                voltage=voltage_label, enable_cb=enable_cb, enable_label=enable_label
            )
            self.channels.append(channel)

        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)

        self.resize(400, 100)

    def send(self, fmt, *args, **kwargs):
        self.communicator.send(fmt.format(*args, **kwargs).encode("ascii"))

    def on_new_command(self, cmd):
        args = [arg.decode("ascii") for arg in bytes(cmd).split(" ".encode("ascii"))]

        if args[0] == "*IDN?":
            self.send("{}\n", self.name)
            return

        # NB: 1-indexed, because why be sensible? We *want* people to run into this
        #     confusion.
        try:
            channel = self.channels[int(args[0][2:]) - 1]
        except:
            self.send("ERR 1\n")
            raise
            return

        if args[1] == "VOLTS?":
            # Just so the instrument is consistant it reports in mV too.
            self.send("{}\n", float(channel.voltage.value()) * 1000)
        elif args[1] == "VOLTS":
            # This command takes mV, but is named and displays V... tricky!
            channel.voltage.display(float(args[2]) / 1000)
        elif args[1] == "ENABLE?":
            self.send("{}\n", "ON" if channel.enable_cb.isChecked() else "OFF")
        elif args[1] == "ENABLE":
            channel.enable_cb.setChecked(args[2] == "ON")
        else:
            self.send("ERR 2\n")

    def closeEvent(self, event):
        print('demo_instrument is closing.')
        self.communicator.active = False
        self.thread.quit()
        self.thread.wait()


class SocketCommunicator(QObject):
    def __init__(self, connection, parent=None):
        self._connection = connection
        super(SocketCommunicator, self).__init__(parent)

    new_command = pyqtSignal(str if sys.version_info.major <= 2 else bytes)
    recv_buffer = bytes()
    send_buffer = bytes()
    active = True

    def send(self, data):
        self.send_buffer += data
        print(self.send_buffer)

    def loop(self):
        while self.active:
            try:
                self.recv_buffer += self._connection.recv(1024)
            except socket.timeout:
                pass
            except socket.error as ex:
                if ex.errno != errno.EWOULDBLOCK:
                    raise

            if bytes("\n".encode("ascii")) in self.recv_buffer:
                cmd, self.recv_buffer = self.recv_buffer.split("\n".encode("ascii"), 1)
                self.new_command.emit(cmd.strip())


            if self.send_buffer:
                self._connection.sendall(self.send_buffer)
                self.send_buffer = bytes()

            if not self.active:
                continue
        # def close(self):
        #     self.thread.exit()
        #     self.quit()
        #     self.exit()



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
    root.thread = socket_thread

    QTimer.singleShot(0, socket_thread.start)

    root.show()

    sys.exit(app.exec_())
