import os.path
import unittest
import json

import slurminade
from slurminade.function import SlurmFunction

f_file = "./f_test_file.txt"
g_file = "./g_test_file.txt"


@slurminade.slurmify()
def f():
    with open(f_file, "w") as file:
        file.write("test")


def delete_f():
    if os.path.exists(f_file):
        os.remove(f_file)


@slurminade.slurmify()
def g(x, y):
    with open(g_file, "w") as file:
        file.write(f"{x}:{y}")


def delete_g():
    if os.path.exists(g_file):
        os.remove(g_file)


class TestLocal(unittest.TestCase):
    def test_1(self):
        delete_f()
        SlurmFunction.call(f.func_id)
        self.assertTrue(os.path.exists(f_file))
        delete_f()

    def test_2(self):
        delete_g()
        SlurmFunction.call(g.func_id, x="a", y=2)
        self.assertTrue(os.path.exists(g_file))
        with open(g_file, "r") as file:
            self.assertEqual(file.readline(), "a:2")
        delete_g()
