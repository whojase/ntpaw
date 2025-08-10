import sys
import platform
import termios
import tty
import msvcrt

def hidden_input(prompt: str = "", mask: str = "") -> str:
    if platform.system() == "Windows":
        return _hidden_input_windows(prompt, mask)
    else:
        return _hidden_input_unix(prompt, mask)

def _hidden_input_windows(prompt: str, mask: str) -> str:
    print(prompt, end="", flush=True)
    result = []
    while True:
        ch = msvcrt.getch()
        if ch in (b'\r', b'\n'):
            print()
            break
        elif ch == b'\x08':
            if result:
                result.pop()
                sys.stdout.write('\b \b')
        else:
            result.append(ch.decode(sys.stdin.encoding))
            if mask:
                sys.stdout.write(mask)
    return ''.join(result)

def _hidden_input_unix(prompt: str, mask: str) -> str:
    print(prompt, end="", flush=True)
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        result = []
        while True:
            ch = sys.stdin.read(1)
            if ch == '\r' or ch == '\n':
                print()
                break
            elif ch == '\x7f':
                if result:
                    result.pop()
                    sys.stdout.write('\b \b')
                result.append(ch)
                if mask:
                    sys.stdout.write(mask)
        return ''.join(result)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
