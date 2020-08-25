import unittest
import functools
import subprocess
import socket

popen = functools.partial(
    subprocess.Popen,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    cwd="/home/dparker/pr1/transfer/",
)


class TestClient(unittest.TestCase):
    def setUp(self):
        with popen(["make"]) as p:
            self.assertEqual(p.wait(1), 0)

    def test_connects_to_port_ipv4(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as test_server:
            test_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            test_server.bind(("", 3254))
            test_server.listen(1)
            test_server.settimeout(1)
            with popen(["./transferclient", "-p", "3254"]) as p:
                try:
                    conn, _ = test_server.accept()
                except socket.timeout:
                    self.assert_(False, "Should not timeout")
                conn.close()

    def test_connects_to_port_ipv6(self):
        with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as test_server:
            test_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            test_server.bind(("", 3254))
            test_server.listen(1)
            test_server.settimeout(1)
            with popen(["./transferclient", "-p", "3254"]) as p:
                try:
                    conn, _ = test_server.accept()
                except socket.timeout:
                    self.assert_(False, "Should not timeout")
                conn.close()

    def test_multiple_clients(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as test_server:
            test_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            test_server.bind(("", 2364))
            test_server.listen(2)
            test_server.settimeout(1)
            with popen(["./transferclient", "-p", "2364"]) as p1:
                with popen(["./transferclient", "-p", "2364"]) as p2:
                    try:
                        conn1, _ = test_server.accept()
                        conn2, _ = test_server.accept()
                    except socket.timeout:
                        self.assert_(False, "Should not timeout")
                    conn1.close()
                    conn2.close()

    def test_writes_to_file(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as test_server:
            test_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            test_server.bind(("", 5034))
            test_server.listen(1)
            test_server.settimeout(1)
            with popen(["rm", "test_writes_to_file.txt"]) as p:
                p.wait()
            with popen(
                ["./transferclient", "-p", "5034", "-o", "test_writes_to_file.txt"]
            ) as p:
                conn, _ = test_server.accept()
                conn.sendall(b"This should be a file!!!")
                conn.close()
                p.wait(1)
            with popen(["cat", "test_writes_to_file.txt"]) as p:
                contents, err = p.communicate()
                self.assertEqual(contents, b"This should be a file!!!", err)
            with popen(["rm", "test_writes_to_file.txt"]) as p:
                p.wait()

    def test_writes_large_file(self):
        file_content = b"""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam sagittis rhoncus mi a volutpat. Sed ac felis iaculis, sollicitudin felis ut, luctus erat. In sit amet velit magna. Ut dolor lacus, ultricies ut laoreet at, malesuada nec metus. Ut odio urna, viverra eget justo eu, molestie fermentum mauris. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Suspendisse potenti. Curabitur at malesuada est, sed viverra nulla. Vestibulum eu sollicitudin diam. Sed faucibus leo quam, nec aliquam lectus consectetur in. Nulla facilisi. Sed eget diam rutrum, convallis enim in, accumsan orci. Ut ac accumsan magna. Nam bibendum sagittis dolor sit amet laoreet. Proin lobortis, dui ac tristique tincidunt, quam dolor venenatis nibh, at laoreet orci augue non nulla.

Pellentesque vitae eros mi. Nunc interdum metus et erat elementum cursus. Aliquam erat volutpat. Nunc cursus odio lorem. Donec vel justo congue, ornare mi a, lobortis dolor. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Maecenas viverra magna quis sapien ullamcorper ultricies. Integer id iaculis lectus. Nulla tempus, ipsum id sollicitudin placerat, turpis felis lobortis ex, non faucibus neque enim vitae mauris. Suspendisse rutrum rhoncus elit sit amet lobortis. Sed turpis urna, fermentum in sem consectetur, consectetur gravida justo. Vestibulum efficitur suscipit orci id suscipit. Praesent ac gravida orci. In pretium finibus mauris quis accumsan. Mauris a urna eget magna interdum sodales at sed ante.

Cras finibus facilisis nunc varius laoreet. Nulla pharetra tellus nec est mattis, eget porttitor diam semper. Fusce risus ante, condimentum nec lorem commodo, laoreet sagittis neque. Phasellus mattis ultrices velit et suscipit. Quisque a libero tempor purus dignissim mollis. Nullam ut massa vestibulum, lobortis nisi ut, sodales erat. Aenean sit amet orci aliquet, eleifend ligula eget, tincidunt ex. Morbi non sollicitudin quam. Maecenas tincidunt porttitor libero eget aliquam. Cras vel maximus mi. Proin rutrum sit amet massa quis condimentum.

Phasellus vel placerat dolor, nec pharetra enim. Cras congue pulvinar lorem, ut egestas orci lacinia id. Quisque posuere nunc ac imperdiet porttitor. Curabitur consectetur convallis libero, tincidunt luctus libero sodales vitae. Sed in mauris nibh. Praesent egestas a ante id pulvinar. Suspendisse potenti. Donec diam arcu, porttitor eget nibh non, mollis scelerisque erat.

Morbi commodo ullamcorper elit, in cursus nisi vehicula a. Phasellus nec aliquam nisi. Sed a imperdiet nisi. Nullam est turpis, luctus vitae pulvinar vel, commodo varius eros. Sed eu justo elementum, rutrum metus eu, cursus risus. Suspendisse porttitor nulla quam, vel luctus justo varius sed. Morbi posuere libero quam, at consequat nunc facilisis eu. Vestibulum porta elit auctor, auctor leo at, dapibus ex. Suspendisse sed turpis a turpis iaculis congue. Quisque pretium elit ex, non gravida augue pulvinar nec. Sed ultrices, metus eget gravida maximus, leo sapien euismod nisl, nec vulputate urna arcu vel neque. Maecenas aliquam sem orci, sed dictum sem aliquam eget. Aenean tortor libero, vehicula eu odio nec, lobortis scelerisque mauris.

Fusce dapibus lacus sed bibendum faucibus. Phasellus viverra eros purus, sit amet sollicitudin nibh fermentum quis. Praesent eu justo vitae est tempor mollis sed nec nibh. Nunc non risus a lacus mollis varius. Integer ac auctor justo. Curabitur posuere, tortor ac sodales pellentesque, purus sapien luctus elit, id lacinia sapien sapien interdum neque. Fusce commodo lorem sit amet vulputate pharetra. Etiam porta metus velit, id tincidunt lacus auctor non. Nulla sit amet eros a nibh efficitur aliquet. Vivamus vel consequat sem. Aenean semper tempor metus id interdum. Cras neque turpis, sollicitudin nec molestie pellentesque, dictum a ipsum. Donec leo quam, maximus at eleifend non, consequat ac dolor. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Interdum et malesuada fames ac ante ipsum primis in faucibus. Donec eget odio libero.

Cras non tellus non quam eleifend suscipit. Etiam blandit finibus lacus vitae fringilla. Suspendisse pretium aliquet libero, nec venenatis sapien aliquam quis. Suspendisse elit lorem, tincidunt ut lorem vitae, bibendum mollis risus. Duis gravida elit vel feugiat venenatis. Nulla lobortis mattis erat sit amet congue. Nullam ac tristique dui. Praesent imperdiet posuere enim, sit amet vulputate est placerat eu. Nullam ultrices ex eget augue interdum lobortis. Phasellus sollicitudin ut nunc dictum laoreet. Nam nunc metus, condimentum ac ultrices faucibus, hendrerit eu lectus. Quisque ornare libero at porttitor posuere. Nulla nec dui iaculis, placerat elit in, rutrum urna.

Morbi eu auctor enim. Proin ligula libero, vulputate id feugiat sed, hendrerit non velit. Praesent ultrices eget sapien eu interdum. Sed cursus justo sed mauris convallis convallis. Integer aliquet nibh non metus ornare consectetur. Nullam quis lectus est.
"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as test_server:
            test_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            test_server.bind(("", 5034))
            test_server.listen(1)
            test_server.settimeout(1)
            with popen(["rm", "test_writes_large_file.txt"]) as p:
                p.wait()
            with popen(
                ["./transferclient", "-p", "5034", "-o", "test_writes_large_file.txt"]
            ) as p:
                conn, _ = test_server.accept()
                conn.sendall(file_content)
                conn.close()
                p.wait(1)
            with popen(["cat", "test_writes_large_file.txt"]) as p:
                contents, err = p.communicate()
                self.assertEqual(contents, file_content, err)
            with popen(["rm", "test_writes_large_file.txt"]) as p:
                p.wait()


class TestServer(unittest.TestCase):
    def setUp(self):
        with popen(["make"]) as p:
            self.assertEqual(p.wait(1), 0)

    def test_accepts(self):
        with popen(["./transferserver", "-p", "1054"]) as p:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as test_client:
                test_client.settimeout(1)
                try:
                    test_client.connect(("localhost", 1054))
                except socket.timeout:
                    self.assert_(False, "Should not timeout")
                test_client.close()
            p.kill()
            p.wait(1)

    def test_accepts_multiple(self):
        with popen(["./transferserver", "-p", "1054"]) as p:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tc1:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tc2:
                    tc1.settimeout(1)
                    tc2.settimeout(1)
                    try:
                        tc1.connect(("localhost", 1054))
                        tc2.connect(("localhost", 1054))
                    except socket.timeout:
                        self.assert_(False, "Should not timeout")
                tc1.close()
                tc2.close()
            p.kill()
            p.wait(1)


if __name__ == "__main__":
    unittest.main()
