"""

Simple command line client for reading and writing from/to the online text
resources. More than one command can be used at the same time.

To see the usage, see help: `python client.py -h`

To use any commands, first made sure the user is created:
`python client --create -u user1, -p password1`

Example of of printing the user data to the console:
`python client.py -u user1 -p password1 -t user -r`

Example of writing a file to the global resource:
`python client.py -u user1 -p password1 -t global -w ./a_file.txt`

"""
import argparse

def create_user(username:str , password: str):
    # TODO
    return

def read_global_text(username: str, password: str) -> str:
    # TODO: 1. Login
    # TODO: 2. fetch the global text resouce from the server.
    return ''

def read_user_text(username: str, password: str) -> str:
    # TODO: 1. Login
    # TODO: 2. fetch the user text resouce from the server.
    return ''

def write_global_text(username: str, password: str, content: str):
    # TODO
    return

def write_user_text(username: str, password: str, content: str):
    # TODO
    return

def main():
    # Define arguments
    parser = argparse.ArgumentParser(description='Interact with online text resources.')
    parser.add_argument('--username', '-u', required=True, nargs=1, type=str, help='username')
    parser.add_argument('--password', '-p', required=True, nargs=1, type=str, help='password')
    parser.add_argument('--type', '-t', required=True, nargs=1, choices=['user', 'global'], help='type of online file to read/write.')
    # Commands
    parser.add_argument('--create', '-c', action='store_const', const=True, default=None, help='create a user with the given username and password')
    parser.add_argument('--get', '-g', nargs=1, type=argparse.FileType('w', encoding='latin-1'), help='get the online resource and write it to file')
    parser.add_argument('--read', '-r', action='store_const', const=True, default=None, help='read the online resource and print it to the console')
    parser.add_argument('--write', '-w', nargs=1, type=argparse.FileType('r', encoding='latin-1'), help='write file to online resource')
    args = parser.parse_args()

    # get login credentials (plain text)
    _username = args.username[0]
    _password = args.password[0]
    _type = args.type[0]

    # Process 'crate' command if defined.
    if args.create is not None:
        create_user(_username, _password)

    # Process 'read' command if defined.
    _read = args.read
    if _read is not None:
        if _type == 'user':
            contents = read_user_text(_username, _password)
        else:
            contents = read_global_text(_username, _password)
        print(contents)

    # Process 'get' command if defined.
    _get = args.get
    if _get is not None:
        _get = _get[0]
        if _type == 'user':
            contents = read_user_text(_username, _password)
        else:
            contents = read_global_text(_username, _password)
        _get.write(contents)
        print(f'Online {_type} data written to file: {_get.name}')

    # Process 'write' command if defined
    _write = args.write
    if _write is not None:
        _write = _write[0]
        contents = _write.read()
        if _type == 'user':
            write_user_text(_username, _password, contents)
        else:
            write_global_text(_username, _password, contents)
        print(f'File {_write.name} written to online {_type} data.')


if __name__ == '__main__':
    main()