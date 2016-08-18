import pytest
import subprocess
import re


FLAMEGRAPH_RE = re.compile(r'^\S+ \d+$')


@pytest.yield_fixture
def proc():
    # start the process and wait for it to print its pid... we explicitly do
    # this instead of using the pid attribute so we can ensure that the process
    # is initialized
    dijkstra = subprocess.Popen(
        ['python', './tests/dijkstra.py'], stdout=subprocess.PIPE)
    dijkstra.stdout.readline()

    try:
        yield dijkstra
    finally:
        dijkstra.kill()


def test_monitor(proc):
    """Basic test for the monitor mode."""
    proc = subprocess.Popen(['./src/pyflame', str(proc.pid)],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = proc.communicate()
    assert not err
    assert proc.returncode == 0
    lines = out.split('\n')
    assert lines.pop(-1) == ''  # output should end in a newline
    for line in lines:
        assert FLAMEGRAPH_RE.match(line) is not None