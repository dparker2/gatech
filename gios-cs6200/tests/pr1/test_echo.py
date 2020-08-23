import unittest
import subprocess
import socket
from time import sleep

p_kwargs = dict(
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    cwd="/home/dparker/pr1/echo/"
)

class TestEcho(unittest.TestCase):

    def test_it_compiles(self):
        with subprocess.Popen(["make"], **p_kwargs) as p:
            self.assertEqual(p.wait(), 0)
    
    def test_server_starts(self):
        with subprocess.Popen(["./echoserver"], **p_kwargs) as p:
            self.assertEqual(p.returncode, None)
            p.kill()
            self.assertNotEqual(p.wait(1), None)

    def test_server_can_restart(self):
        def start_stop():
            with subprocess.Popen(["./echoserver"], **p_kwargs) as p:
                p.kill()
                return p.wait(1)
        
        for _ in range(3):
            self.assertEqual(start_stop(), -9)
    
    def test_server_echoes(self):
        message = b"Foo Bar!!!"
        with subprocess.Popen(["./echoserver", "-p", "2345"], **p_kwargs) as p:
            sleep(0.1)  # Wait for startup
            sock = socket.create_connection(("localhost", 2345))
            sock.send(message)
            resp = sock.recv(16)
            sock.close()
            p.kill()
        
        self.assertEqual(resp, message)


if __name__ == '__main__':
    unittest.main()
