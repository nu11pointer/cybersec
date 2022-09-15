import argparse
from src.version import __version__

def parse(version):
    argv = argparse.ArgumentParser(add_help=True)
    
    settings = argv.add_argument_group(title="Settings")
    settings.add_argument("-r", "--management-role", action="store", metavar="role", type=str, help="Management role", required=True)
    settings.add_argument("-c", "--management-channel", action="store", metavar="channel", type=str, help="Management channel", required=False)
    settings.add_argument("-p", "--prefix", action="store", metavar="prefix", type=str, default="$", help="Bot prefix (default: $)")
    #settings.add_argument("-v", "--verbose", action="store_true", default=False, help="Verbose output")

    argv.add_argument("-V", "--version", action="version", version=f"v{__version__}")


    return argv.parse_args()