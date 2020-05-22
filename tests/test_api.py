import subprocess


_PACKAGE_NAME = 'neuron.api'
_SERVER_ADDRESS = '127.0.0.1', 8000


def test_cli_unsupported_database():
    host, port = _SERVER_ADDRESS
    process = subprocess.Popen(
        ['python', '-m', _PACKAGE_NAME, 'run-server',
            '-H', host, '-p', str(port), '-d', 'postgresql://127.0.0.1:9000'],
        stdout=subprocess.PIPE,
    )

    stdout, _ = process.communicate()

    assert process.returncode != 0
    assert b'Unsupported database type.' in stdout
