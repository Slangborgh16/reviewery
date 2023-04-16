import argparse
from pathlib import Path


def get_cmd_args():
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(title='commands', dest='command')
    create_parser = commands.add_parser('create', help='create a new review database')
    generate_parser = commands.add_parser('generate', help='generate a PDF from the database and template files')

    parser.add_argument('-v', '--verbose', action='store_true', help='enable verbose output')

    create_parser.add_argument('output', type=Path, help='output database CSV file path')

    generate_parser.add_argument('output', nargs='?', default='./reviews.pdf', type=Path, help='output PDF file path (default: %(default)s)')

    return parser.parse_args()


def create(args: argparse.Namespace):
    print('Create!')


def generate(args: argparse.Namespace):
    print('Generate!')


if __name__ == '__main__':
    args: argparse.Namespace = get_cmd_args()
    
    match args.command:
        case 'create':
            create(args)
        case 'generate':
            generate(args)