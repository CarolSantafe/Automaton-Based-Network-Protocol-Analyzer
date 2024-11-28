# src/protocol_analyzer.py

from tcp_state_machine import TCPStateMachine

def simulate_events(tcp, events):
    for event in events:
        if event == "send_syn":
            tcp.send_syn()
        elif event == "receive_syn_ack":
            tcp.receive_syn_ack()
        elif event == "send_fin":
            tcp.send_fin()
        elif event == "receive_fin":
            tcp.receive_fin()
        elif event == "timeout":
            tcp.timeout()
        else:
            print("Evento desconocido:", event)

def analyze_protocol(events):
    tcp = TCPStateMachine()
    simulate_events(tcp, events)
    tcp.check_for_issues()