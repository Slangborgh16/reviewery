import sys
import os
import argparse
from pathlib import Path


def get_cmd_args():
    parser = argparse.ArgumentParser(description='A tool for creating and organizing personal reviews on music, books, movies, or anything else!')
    commands = parser.add_subparsers(title='commands', dest='command', required=True)
    create_parser = commands.add_parser('create', help='create a new review database')
    generate_parser = commands.add_parser('generate', help='generate a PDF from the database and template files')

    parser.add_argument('-v', '--verbose', action='store_true', help='enable verbose output')

    create_parser.add_argument('output_file', type=Path, help='output database CSV file path')

    generate_parser.add_argument('output_file', nargs='?', default='./reviews.pdf', type=Path, help='output PDF file path (default: %(default)s)')

    return parser.parse_args()


def create(args: argparse.Namespace):
    out_file = args.output_file.resolve()
    print(f'Creating reviews database "{out_file.name}" in "{out_file.parent}"\n')
    # print('Attributes are information about each review such as an album title, and author, a director, etc.')
    # print('Attributes can also be an image URL or path. All spaces in the attribute name are automatically replaced with underscores.')
    # print('To refer to an attribute in a markdown file, surround the attribute with curly brackets.')
    # print('In the final PDF, these attribute tags will be replaced with text from the database.')
    # print('Example:\n\t{album}, {artist} --> "The Dark Side of the Moon, Pink Floyd"')
    print('Enter attribute names. Leave blank when finished.')
    print('See README.md for information about attributes.\n')

    num_attribute: int = 1
    attributes: list[str] = []

    while True:
        attr = input(f'{num_attribute}. ')
        if attr.isspace() or attr == '':
            if len(attributes) == 0:
                print('No attributes entered. Database will not be created.')
                choice = input('(Q)uit / (r)estart: ')

                if choice in ('r', 'R', 'restart'):
                    print('Restarting.')
                    print('Enter attribute names. Leave blank when finished.')
                else:
                    print('Quitting...')
                    return
            else:
                print('Attributes: ', end='')
                for a in attributes:
                    print(a, end=' ')
            
                choice = input('\n(F)inish / (q)uit / (c)ontinue / (r)estart: ')

                if choice in ('f', 'F', 'finish'):
                    break
                elif choice in ('q', 'Q', 'quit'):
                    print('Quitting...')
                    return
                elif choice in ('c', 'C', 'continue'):
                    continue
                elif choice in ('r', 'R', 'restart'):
                    num_attribute = 1
                    attributes = []
                    print('Restarting.')
                    print('Enter attribute names. Leave blank when finished.')
                else:
                    break
        else:
            num_attribute += 1
            attributes.append(str(attr.replace(' ', '_')))

    print(attributes)
    print('Done')
    

def generate(args: argparse.Namespace):
    print('Generate!')
    print(args.verbose)


if __name__ == '__main__':
    args: argparse.Namespace = get_cmd_args()
    
    try:
        match args.command:
            case 'create':
                create(args)
            case 'generate':
                generate(args)
                
    except KeyboardInterrupt:
        print('\nQuitting...')
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)