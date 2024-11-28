# tests/test_tcp_state_machine.py

import unittest
from src.tcp_state_machine import TCPStateMachine

class TestTCPStateMachine(unittest.TestCase):

    def setUp(self):
        self.tcp = TCPStateMachine()

    def test_initial_state(self):
        self.assertEqual(self.tcp.state, "CLOSED")

    def test_send_syn(self):
        self.tcp.send_syn()
        self.assertEqual(self.tcp.state, "SYN_SENT")

    def test_receive_syn_ack(self):
        self.tcp.send_syn()
        self.tcp.receive_syn_ack()
        self.assertEqual(self.tcp.state, "ESTABLISHED")

    def test_send_fin(self):
        self.tcp.send_syn()
        self.tcp.receive_syn_ack()
        self.tcp.send_fin()
        self.assertEqual(self.tcp.state, "FIN_WAIT_1")

    def test_receive_fin(self):
        self.tcp.send_syn()
        self.tcp.receive_syn_ack()
        self.tcp.send_fin()
        self.tcp.receive_fin()
        self.assertEqual(self.tcp.state, "FIN_WAIT_2")

    def test_timeout(self):
        self.tcp.send_syn()
        self.tcp .receive_syn_ack()
        self.tcp.send_fin()
        self.tcp.receive_fin()
        self.tcp.timeout()
        self.assertEqual(self.tcp.state, "CLOSED")

if __name__ == "__main__":
    unittest.main()