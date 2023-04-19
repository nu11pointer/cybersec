from datetime import datetime
from main import PATH
import os

def error(cmd, output):
    time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    file = os.path.join(PATH, os.path.join("logs", "error.log"))
    output = str(output).replace('"', "\\\"")
    message = f"{time}: The command '{cmd}' generated the following response: \"{output}\"\n"
    __log__(file, message)

def unauthorized(user, channel, cmd):
    time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    file = os.path.join(PATH, os.path.join("logs", "access.log"))
    cmd = str(cmd).replace('"', "\\\"")
    message = f"{time}: User '{str(user)}' attempted to execute '{cmd}' on #{channel}\n"
    __log__(file, message)


def __log__(file, message):
    with open(file, "a") as fp:
        fp.write(message)