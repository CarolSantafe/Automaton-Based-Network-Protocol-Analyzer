import tkinter as tk
from tkinter import messagebox
from tcp_state_machine import TCPStateMachine

class TCPGUI:
    def __init__(self, master, state_machine):
        self.master = master
        self.canvas = tk.Canvas(master, width=900, height=500) 
        self.canvas.pack()

        self.title_label = tk.Label(master, text="Máquina de Estados TCP", font=("Arial", 25, "bold"), fg="#3498db")
        self.title_label.place(relx=0.5, y=30, anchor="center")  

        self.state_machine = state_machine
        self.states = {} 
      
        self.label = tk.Label(master, text=f"Estado Actual: {self.state_machine.get_current_state()}", font=("Arial", 16, "bold"), fg="#f39c12")
        self.label.place(relx=0.5, y=500, anchor="center") 

    
        button_frame = tk.Frame(master)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)  
        self.create_transition_buttons(button_frame)

        self.update_graph()

    def create_transition_buttons(self, frame):
      
        columns = 2
        for i, state in enumerate(self.state_machine.get_states()):
     
            row = i // columns  
            column = i % columns  
            button = tk.Button(frame, text=f"Transitar a {state}", command=lambda s=state: self.perform_transition(s), bg="lightblue", width=12, height=2,
                               relief="solid", borderwidth=1, highlightthickness=2, highlightbackground="blue", highlightcolor="blue")

            button.grid(row=row, column=column, padx=10, pady=5, sticky="nsew") 

        for i in range(columns):
            frame.grid_columnconfigure(i, weight=1, uniform="equal")

    def perform_transition(self, new_state):
        if self.state_machine.transition(new_state):
            self.label.config(text=f"Estado Actual: {self.state_machine.get_current_state()}")
            self.update_graph() 

            if self.state_machine.get_current_state() == "CLOSED":
                self.update_graph()  
                self.master.after(500, self.show_success_message)  
        else:
            messagebox.showerror("Error", f"No se puede realizar la transición a {new_state} desde {self.state_machine.get_current_state()}.")

    def show_success_message(self):
        messagebox.showinfo("Éxito", "El protocolo ha sido validado correctamente.")
        self.reset_automaton() 

    def update_graph(self):
        state_positions = {
            "CLOSED": (100, 300),
            "LISTEN": (200, 400),
            "SYN_SENT": (300, 250),
            "SYN_RCVD": (400, 350),
            "ESTABLISHED": (500, 200),
            "FIN_WAIT_1": (600, 300),
            "FIN_WAIT_2": (700, 400),
            "CLOSE_WAIT": (500, 450),
            "LAST_ACK": (300, 450),
            "TIME_WAIT": (700, 100),
        }

        for state, position in state_positions.items():
            x, y = position
            if state not in self.states:
                self.add_state(state, x, y) 
        self.draw_transitions() 

    def draw_transition_with_label(self, start_x, start_y, end_x, end_y, label, color):
        mid_x, mid_y = (start_x + end_x) / 2, (start_y + end_y) / 2
        curve_offset = 30  
        dx, dy = end_x - start_x, end_y - start_y
        distance = (dx**2 + dy**2)**0.5  
        norm_dx, norm_dy = -dy / distance, dx / distance  
        control_x = mid_x + curve_offset * norm_dx
        control_y = mid_y + curve_offset * norm_dy
        self.canvas.create_line(start_x, start_y, control_x, control_y, end_x, end_y,
                                smooth=True, arrow=tk.LAST, fill=color, width=2)
        self.canvas.create_text(mid_x, mid_y - 10, text=label, fill=color, font=("Arial", 10))

    def add_state(self, name, x, y):
        color = self.get_state_color(name)
        state_id = self.canvas.create_oval(x-20, y-20, x+20, y+20, fill=color, outline="black", tags=name)  
        self.canvas.create_text(x, y + 30, text=name, font=("Arial", 8, "bold"))
        self.states[name] = (state_id, x, y)

    def draw_transitions(self):
        transitions = {
            "CLOSED": [("LISTEN", "Abrir conexión (passive open)"),
                    ("SYN_SENT", "Abrir conexión (active open)")],
            "LISTEN": [("SYN_RCVD", "Recibir SYN"),
                    ("SYN_SENT", "Enviar SYN (simultáneo)"),
                    ("CLOSED", "Cerrar conexión")],
            "SYN_SENT": [("SYN_RCVD", "Recibir SYN"),
                        ("ESTABLISHED", "Recibir SYN+ACK"),
                        ("CLOSED", "Tiempo de espera")],
            "SYN_RCVD": [("ESTABLISHED", "Enviar ACK"),
                        ("FIN_WAIT_1", "Recibir FIN"),
                        ("LISTEN", "Cerrar conexión")],
            "ESTABLISHED": [("FIN_WAIT_1", "Enviar FIN"),
                            ("CLOSE_WAIT", "Recibir FIN")],
            "FIN_WAIT_1": [("FIN_WAIT_2", "Recibir ACK"),
                        ("CLOSED", "Recibir FIN+ACK")],
            "FIN_WAIT_2": [("TIME_WAIT", "Recibir FIN")],
            "CLOSE_WAIT": [("LAST_ACK", "Enviar FIN")],
            "LAST_ACK": [("CLOSED", "Recibir ACK")],
            "TIME_WAIT": [("CLOSED", "Tiempo agotado")]
        }

        blue_palette = ["#1E90FF", "#4169E1", "#6495ED", "#87CEEB", "#4682B4"]
        orange_palette = ["#FF8C00", "#FFA500", "#FF4500", "#FF6347", "#FFD700"]
        green_palette = ["#32CD32", "#228B22", "#008000", "#00FF7F", "#9ACD32"]
        red_palette = ["#FF0000", "#DC143C", "#B22222", "#FF6347", "#8B0000"]

        transition_colors = {
            "Abrir conexión (passive open)": blue_palette[0],
            "Abrir conexión (active open)": orange_palette[0],
            "Recibir SYN": green_palette[0],
            "Enviar SYN (simultáneo)": red_palette[0],
            "Cerrar conexión": blue_palette[1],
            "Recibir SYN+ACK": orange_palette[1],
            "Tiempo de espera": green_palette[1],
            "Enviar ACK": red_palette[1],
            "Recibir FIN": blue_palette[2],
            "Recibir FIN+ACK": orange_palette[2],
            "Enviar FIN": green_palette[2],
            "Tiempo agotado": red_palette[2],
        }


        for start_state, transitions_list in transitions.items():
            for end_state, label in transitions_list:
                start_x, start_y = self.states[start_state][1], self.states[start_state][2]
                end_x, end_y = self.states[end_state][1], self.states[end_state][2]
                color = transition_colors.get(label, "black")  
                self.draw_transition_with_label(start_x, start_y, end_x, end_y, label, color)


    def get_state_color(self, state):
        colors = {
            "CLOSED": "lightgray",
            "LISTEN": "lightgreen",
            "SYN_SENT": "lightblue",
            "SYN_RCVD": "yellow",
            "ESTABLISHED": "orange",
            "FIN_WAIT_1": "pink",
            "FIN_WAIT_2": "lightpink",
            "CLOSE_WAIT": "lightcoral",
            "LAST_ACK": "red",
            "TIME_WAIT": "gold",
        }
        return colors.get(state, "white")
    
    def highlight_state(self, state):
        self.canvas.itemconfig(self.states[state][0], outline="red", width=3)

def draw_fsm(self):
    self.canvas.delete("all")
    
    for state, (state_id, x, y) in self.states.items():
        state_id = self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="lightblue")
        self.canvas.tag_bind(state_id, "<Button-1>", lambda event, state=state: self.highlight_state(state))
        self.states[state] = (state_id, x, y)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Máquina de Estados TCP")
    root.geometry("1000x900")
    state_machine = TCPStateMachine()
    app = TCPGUI(root, state_machine)
    root.mainloop()
