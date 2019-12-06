from datetime import datetime
import pathlib
from .website import Website

_INDEX_HTML = '''
<html>
    <head></head>
    <body>
        <ul>
            {users}
        </ul>
    </body>
</html>
'''

_USER_LINE_HTML = '''
<li><a href="/users/{user_id}">user {user_id}</a></li>
'''

_MESSAGES_HTML = '''
<tr>
    <td>{timestamp}</td>
    <td>{thought}</td>
</tr>
'''

_USER_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface: User {user_id}</title>
    </head>
    <body>
        <table>
            {messages}
        </table>
    </body>
</html>
'''

website = Website()
data_dir = None


@website.route('/')
def index():
    users_html = []
    for user_dir in data_dir.iterdir():
        users_html.append(_USER_LINE_HTML.format(user_id=user_dir.name))
    index_html = _INDEX_HTML.format(users='\n'.join(users_html))

    return 200, index_html


@website.route('/users/([0-9]+)')
def user(user_id):
    user_dir = data_dir / str(user_id)

    if not user_dir.exists():
        return 404, ''

    msgs_html = []
    for msg in user_dir.iterdir():
        timestamp = extract_timestamp(msg.name)
        thought = msg.read_text()
        msgs_html.append(_MESSAGES_HTML.format(
            timestamp=timestamp, thought=thought))
    user_html = _USER_HTML.format(
        user_id=user_id, messages='\n'.join(msgs_html))

    return 200, user_html


def extract_timestamp(file_name):
    dt = datetime.strptime(file_name, '%Y-%m-%d_%H-%M-%S.txt')
    return datetime.strftime(dt, '%Y-%m-%d %H:%M:%S')


def run_webserver(address, data):
    global data_dir
    data_dir = pathlib.Path(data)
    website.run(address)


def main(argv):
    if len(argv) != 3:
        print(f'USAGE: {argv[0]} <address> <data_dir>')
        return 1
    try:
        ip, port = argv[1].split(':')
        address = ip, int(port)
        data_dir = argv[2]
        run_webserver(address, data_dir)
        print('done')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


def signal_handler(sig, frame):
    sys.exit(0)


if __name__ == '__main__':
    import signal
    import sys
    signal.signal(signal.SIGINT, signal_handler)
    sys.exit(main(sys.argv))
