import argparse

def argParser(command_line_args):
    pars = argparse.ArgumentParser()
    group = pars.add_mutually_exclusive_group(required=False)
    group.add_argument("-a", "--add", action='store_true', help="Adding notes", )
    group.add_argument("-d", "--delete", action='store_true', help="Delete notes")
    group.add_argument("-v", "--search_notes", action='store_true', help="View and search_notes for notes")
    group.add_argument("-e", "--exp", nargs=1, default='-', choices=["csv", "json"],
                       help="Export to CSV or JSON format")
    group.add_argument("-i", "--imp", nargs=1, default='-', choices=["csv", "json"],
                       help="Import from CSV or JSON format")
    pars.add_argument("--title", nargs="*", default="", help="note title")
    pars.add_argument("--text", nargs="*", default="", help="note text")
    pars.add_argument("--id", nargs="?", default="", )
    pars.add_argument("--filename", nargs=1, default="", help="Name of file") 
    return pars.parse_args(command_line_args)
