# main.py

from tcp_gui import TCPGUI
from tcp_state_machine import TCPStateMachine
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Máquina de Estados TCP")
    state_machine = TCPStateMachine()
    app = TCPGUI(root, state_machine)
    root.mainloop()

if __name__ == "__main__":
    main()