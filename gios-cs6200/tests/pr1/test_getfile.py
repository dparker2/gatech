import unittest
import functools
import subprocess
import socket
from time import sleep

popen = functools.partial(
    subprocess.Popen,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    cwd="/home/dparker/pr1/gflib/",
)


def print_out(p):
    out, err = p.communicate()
    print("STDOUT")
    print(out.decode())
    print("STDERR")
    print(err.decode())


def recv_until(sock, term):
    buf = b""
    while not buf.endswith(term):
        buf += sock.recv(1024)
    return buf


class TestServer(unittest.TestCase):
    def setUp(self):
        with popen(["make"]) as p:
            code = p.wait(1)
            if code:
                print_out(p)
                self.assertEqual(code, 0)

    def test_malformed_header(self):
        tests = [
            b"GETFIL GET /not/a/real/file\r\n\r\n",
            b"GETFILEGET /not/a/real/file\r\n\r\n",
            b"GETFILE GET/not/a/real/file\r\n\r\n",
            b"GETFILE GET not/a/real/file\r\n\r\n",
        ]
        with popen(["./gfserver_main", "-p", "4000"]) as p:
            sleep(0.1)  # Wait for startup
            try:
                for test in tests:
                    sock = socket.create_connection(("localhost", 4000), timeout=1)
                    sock.sendall(test)
                    resp = recv_until(sock, b"\r\n\r\n")
                    sock.close()
            except Exception as e:
                print_out(p)
                self.assertTrue(False, str(e))
            finally:
                p.terminate()
            self.assertEqual(resp, b"GETFILE INVALID \r\n\r\n")


if __name__ == "__main__":
    unittest.main()
