import os
import sys
import argparse
import weasyprint
import pandas as pd
import markdown as md
from pathlib import Path


def get_cmd_args():
    description: str = 'A tool for creating and organizing personal reviews on music, books, movies, or anything else!'
    parser = argparse.ArgumentParser(description=description)
    commands = parser.add_subparsers(title='commands', dest='command', required=True)
    create_parser = commands.add_parser('create', help='create a new review database')
    add_parser = commands.add_parser('add', help='add a new entry to an existing review database')
    generate_parser = commands.add_parser('generate', help='generate a PDF from the database and template files')

    # parser.add_argument('-v', '--verbose', action='store_true', help='enable verbose output')

    create_parser.add_argument('-o', '--output', type=Path, help='output database CSV file path', required=True)

    add_parser.add_argument('database_file', type=Path, help='path to existing review database file')

    generate_parser.add_argument('database_file', type=Path, help='path to existing reviews database file')
    generate_parser.add_argument('-d', '--dir', default='.', type=Path, help='directory that contains review write-up files')
    generate_parser.add_argument('-s', '--sort', action='append',
            help='attribute to organize pdf by. can be used more than once to sort by multiple attributes')
    generate_parser.add_argument('-o', '--output', default='./reviews.pdf', type=Path, help='output PDF file path (default: %(default)s)')
    generate_parser.add_argument('-t', '--template', type=Path, help='template file used to generate pages', required=True)

    return parser.parse_args()


def create(args: argparse.Namespace):
    out_file: Path = args.output.resolve()
    print(f'Creating reviews database "{out_file.name}" in "{out_file.parent}"\n')
    # print('Attributes are information about each review such as an album title, and author, a director, etc.')
    # print('Attributes can also be an image URL or path. All spaces in the attribute name are automatically replaced with underscores.')
    # print('To refer to an attribute in a markdown file, surround the attribute with curly brackets.')
    # print('In the final PDF, these attribute tags will be replaced with text from the database.')
    # print('Example:\n\t{album}, {artist} --> "The Dark Side of the Moon, Pink Floyd"')
    print('Enter attribute names. Leave blank when finished.')
    print('See README.md for information about attributes.')

    num_attribute: int = 1
    attributes: list[str] = []

    while True:
        attr: str = input(f'{num_attribute}. ')
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
            
                choice: str = input('\n(F)inish / (q)uit / (c)ontinue / (r)estart: ')

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

    attributes.append('entry_page')
    df = pd.DataFrame(columns=attributes)
    print(f'\nWriting database to "{out_file}"')

    try:
        df.to_csv(out_file, index=False)
        print('Done')
    except OSError as error:
        print(f'Failed writing CSV to {out_file}:\n\t{error}')
        return
    

def add_entry(args: argparse.Namespace):
    db_file: Path = args.database_file.resolve()
    print(f'Opening {db_file}\n')

    if not db_file.exists():
        print('Database file does not exist.')
        print('Quitting...')
        return

    try:
        df: pd.DataFrame = pd.read_csv(db_file)
    except OSError as error:
        print(f'Error opening {db_file}:\n\t{error}')
        return

    while True:
        print('Enter values for each attribute.')
        new_entry: list[str] = []
        
        for attr in list(df.keys()):
            val: str = input(f'{attr}: ')
            new_entry.append(val)

        df.loc[len(df.index)] = new_entry
        df.to_csv(db_file, index=False)

        choice: str = input('Added entry. Would you like to add another? (Y/n): ')

        if choice in ('n', 'N', 'no'):
            break


def generate(args: argparse.Namespace):
    writeup_dir: Path = args.dir.resolve()
    out_file: Path = args.output.resolve()
    template_file: Path = args.template.resolve()
    db_file: Path = args.database_file.resolve()

    sort_by: list[str] = args.sort

    try:
        with open(template_file) as f:
            template: str = f.read()
    except OSError as error:
        print(f'Error opening {template_file}:\n\t{error}')
        return
    
    try:
        df: pd.DataFrame = pd.read_csv(db_file)
    except OSError as error:
        print(f'Error opening {db_file}:\n\t{error}')
        return

    doc: str = ''

    for _, review in df.iterrows():
        review_md: str = template
        for attr in list(df.keys()):
            review_md = review_md.replace(f'{{{attr}}}', review[attr])
        doc += md.markdown(review_md)

    css = weasyprint.CSS(string='body { font-family: calibri }')
    weasyprint.HTML(string=doc).write_pdf(out_file, stylesheets=[css])


if __name__ == '__main__':
    args: argparse.Namespace = get_cmd_args()
    
    try:
        match args.command:
            case 'create':
                create(args)
            case 'add':
                add_entry(args)
            case 'generate':
                generate(args)
                
    except KeyboardInterrupt:
        print('\nQuitting...')
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)