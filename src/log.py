from datetime import datetime
from main import PATH

def error(cmd, output):
    time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    file = f"{PATH}/logs/error.log"
    message = f"{time}: The command '{cmd}' generated the following response: \"{output}\"\n"
    __log__(file, message)

def unauthorized(user, channel, cmd):
    time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    file = f"{PATH}/logs/access.log"
    message = f"{time}: User '{str(user)}' attempted to execute '{cmd}' on #{channel}\n"
    __log__(file, message)


def __log__(file, message):
    with open(file, "a") as fp:
        fp.write(message)