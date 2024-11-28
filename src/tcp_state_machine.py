class TCPStateMachine:
    def __init__(self):
        self.states = [
            "CLOSED", "LISTEN", "SYN_SENT", "SYN_RCVD", "ESTABLISHED",
            "FIN_WAIT_1", "FIN_WAIT_2", "CLOSE_WAIT", "LAST_ACK", "TIME_WAIT"
        ]
        self.current_state = "CLOSED"
        self.transitions = {
            "CLOSED": ["LISTEN", "SYN_SENT"],
            "LISTEN": ["SYN_RCVD", "SYN_SENT", "CLOSED"],
            "SYN_SENT": ["ESTABLISHED", "SYN_RCVD", "CLOSED"],
            "SYN_RCVD": ["ESTABLISHED", "FIN_WAIT_1", "LISTEN", "SYN_SENT"],
            "ESTABLISHED": ["FIN_WAIT_1", "CLOSE_WAIT", "SYN_SENT"],
            "FIN_WAIT_1": ["FIN_WAIT_2", "CLOSE_WAIT", "ESTABLISHED",  "CLOSED"],
            "FIN_WAIT_2": ["TIME_WAIT"],
            "CLOSE_WAIT": ["LAST_ACK"],
            "LAST_ACK": ["CLOSED"],
            "TIME_WAIT": ["CLOSED","FIN_WAIT_1"]
        }
        
    def get_current_state(self):
        return self.current_state

    def get_states(self):
        return self.states

    def get_transitions(self):
        return [(state, next_state) for state in self.transitions for next_state in self.transitions[state]]

    def transition(self, new_state):
        """
        Realiza la transición de un estado a otro y muestra los mensajes correspondientes.
        """
        print(f"Intentando transición de '{self.current_state}' a '{new_state}'...") 

        if new_state in self.transitions.get(self.current_state, []):
            previous_state = self.current_state
            self.current_state = new_state
            print(f"Transición exitosa: ahora en estado '{self.current_state}'.")  
            self.display_transition_message(previous_state, new_state)  
            return True
        else:
            print(f"Transición no válida de '{self.current_state}' a '{new_state}'.") 
            self.display_warning(new_state)
            return False

    def display_transition_message(self, previous_state, new_state):
        """
        Muestra un mensaje correspondiente a la transición realizada.
        """
        print(f"Ejecutando display_transition_message para la transición '{previous_state}' -> '{new_state}'...")
        
        if previous_state == "CLOSED" and new_state == "SYN_SENT":
            print("Iniciando conexión. Se envía SYN para iniciar el handshake.")
        elif previous_state == "LISTEN" and new_state == "SYN_RCVD":
            print("Conexión solicitada. Se ha recibido un SYN del cliente.")
        elif previous_state == "SYN_SENT" and new_state == "ESTABLISHED":
            print("Conexión establecida. El servidor ha respondido con SYN+ACK.")
        elif previous_state == "ESTABLISHED" and new_state == "FIN_WAIT_1":
            print("Iniciando cierre de conexión. Se envía FIN.")
        elif previous_state == "FIN_WAIT_1" and new_state == "TIME_WAIT":
            print("Esperando para cerrar. Recibido FIN y esperando el ACK final.")
        elif new_state == "CLOSED":
            print("Conexión cerrada. El protocolo TCP ha completado su proceso.")
        elif previous_state == "SYN_RCVD" and new_state == "SYN_SENT":
            print("¡Posible interbloqueo! Ambos sistemas están esperando la respuesta del otro.")
        elif previous_state == "SYN_SENT" and new_state == "SYN_RCVD":
            print("¡Interbloqueo! El cliente y servidor no pueden sincronizarse. Verifica el tráfico SYN.")
        elif previous_state == "FIN_WAIT_1" and new_state == "CLOSED":
            print("¡Cierre abrupto! La conexión fue cerrada antes de completar el proceso de cierre.")
        elif previous_state == "TIME_WAIT" and new_state == "CLOSED":
            print("¡Condición de 'TIME_WAIT'! La conexión está esperando antes de cerrarse completamente.")
        else:
            print(f"Transición '{previous_state}' -> '{new_state}' realizada sin mensaje específico.")

    def display_warning(self, new_state):
        """
        Muestra un mensaje de advertencia si la transición no es válida o potencialmente peligrosa.
        """
        print(f"Advertencia: Transición no válida a '{new_state}' desde '{self.current_state}'.")

    def reset(self):
        self.current_state = "CLOSED"
        print("La máquina de estados ha sido reiniciada a 'CLOSED'.")
