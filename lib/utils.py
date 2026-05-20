import sys, time, re, os, subprocess, collections
from datetime import datetime

class Colors:
    GREEN = '\033[32m'
    RED = '\033[31m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

WEB_LOGS = collections.deque(maxlen=100)

def add_web_log(msg):
    clean_msg = re.sub(r'\033\[[0-9;]*m', '', msg)
    WEB_LOGS.append(f"[{datetime.now().strftime('%H:%M:%S')}] {clean_msg}")

def info(msg):
    print(f"{Colors.DIM}•{Colors.RESET} {msg}")
    add_web_log(f"• {msg}")

def success(msg):
    print(f"{Colors.GREEN}✓{Colors.RESET} {msg}")
    add_web_log(f"✓ {msg}")

def error(msg):
    print(f"{Colors.RED}✗{Colors.RESET} {msg}")
    add_web_log(f"✗ {msg}")

def warning(msg):
    print(f"{Colors.YELLOW}!{Colors.RESET} {msg}")
    add_web_log(f"! {msg}")

def ani(z):
    for e in z + '\n':
        sys.stdout.write(e)
        sys.stdout.flush()
        time.sleep(0.005)

def show_banner():
    print(f"\n{Colors.BOLD}WPS AUDITOR{Colors.RESET} {Colors.DIM}v1.0.2{Colors.RESET}")
    print(f"{Colors.DIM}──────────────────────────────────────────{Colors.RESET}")

def recvuntil(pipe, what):
    s = ''
    while True:
        inp = pipe.stdout.read(1)
        if inp == '':
            return s
        s += inp
        if what in s:
            return s

def get_hex(line):
    a = line.split(':', 3)
    return a[2].replace(' ', '').upper()

def check_and_disconnect(iface):
    # Check for active connection
    cmd = f"iw dev {iface} link"
    proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
    if "Not connected" not in proc.stdout:
        # Detectar SSH para avisar al usuario
        if os.environ.get('SSH_CONNECTION') or os.environ.get('SSH_CLIENT'):
            warning("!!! ATENCIÓN: EstÁS USANDO SSH. SI DESCONECTAS LA WIFI PERDERÁS EL CONTROL !!!")
            time.sleep(2)
        warning(f"Active connection detected on {iface}. Disconnecting for auditing...")
        subprocess.run(f"iw dev {iface} disconnect", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1)

def ifaceUp(iface, down=False):
    if down:
        action = 'down'
    else:
        action = 'up'
    cmd = 'ip link set {} {}'.format(iface, action)
    res = subprocess.run(cmd, shell=True, stdout=sys.stdout, stderr=sys.stdout)
    return res.returncode == 0

def die(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(1)
