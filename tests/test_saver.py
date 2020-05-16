from neuron.saver import Saver
import subprocess


_PACKAGE_NAME = 'neuron.saver'


def test_cli_unsupprted_queue(tmp_path):
    process = subprocess.Popen(
            ['python', '-m', _PACKAGE_NAME, 'run-saver', 'postgresql://127.0.0.1:100',
                'kafka://127.0.0.1:90'],
        stdout=subprocess.PIPE,
    )

    stdout, stderr = process.communicate()

    assert b'Unsupported message queue type.' in stdout
    assert process.returncode != 0
