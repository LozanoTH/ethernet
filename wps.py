#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, time, argparse
from lib.utils import Colors, info, error, warning, show_banner, die, ifaceUp, check_and_disconnect, ani
from lib.core import WiFiScanner, Companion
from lib.web import start_web_server

def main():
    parser = argparse.ArgumentParser(description='WPS Auditor PRO (Modular)')
    parser.add_argument('-i', '--interface', type=str, required=True, help='Interfaz WiFi')
    parser.add_argument('-b', '--bssid', type=str, help='BSSID del objetivo')
    parser.add_argument('-p', '--pin', type=str, help='PIN WPS manual')
    parser.add_argument('-K', '--pixie-dust', action='store_true', help='Usar Pixie Dust')
    parser.add_argument('-W', '--web', action='store_true', help='Iniciar App Web')
    parser.add_argument('--web-port', type=int, default=8080, help='Puerto Web')
    parser.add_argument('--demo', action='store_true', help='Modo simulación')
    parser.add_argument('-w', '--write', action='store_true', help='Guardar resultados')
    parser.add_argument('-v', '--verbose', action='store_true', help='Modo detallado')
    parser.add_argument('-l', '--loop', action='store_true', help='Bucle infinito')
    parser.add_argument('--vuln-list', type=str, default=os.path.dirname(os.path.realpath(__file__)) + '/vulnwsc.txt')

    args = parser.parse_args()
    if args.demo: args.interface = 'demo'

    show_banner()

    if not args.demo and os.getuid() != 0:
        error("Error: Requiere ROOT."); sys.exit(1)

    if not args.demo:
        if not ifaceUp(args.interface): die(f"No se pudo activar {args.interface}")
        check_and_disconnect(args.interface)

    try:
        with open(args.vuln_list, 'r', encoding='utf-8') as f: vuln_list = f.read().splitlines()
    except: vuln_list = []

    scanner = WiFiScanner(args.interface, vuln_list)

    if args.web:
        start_web_server(scanner, args, args.web_port)
        try:
            while True: time.sleep(1)
        except KeyboardInterrupt: ani(f"\n{Colors.RED}[!] Saliendo...{Colors.RESET}"); sys.exit(0)

    companion = None
    while True:
        try:
            if not args.bssid: args.bssid = scanner.prompt_network()
            if args.bssid:
                if not companion: companion = Companion(args.interface, args.write, print_debug=args.verbose)
                companion.single_connection(args.bssid, args.pin, args.pixie_dust, auto=False)
            if not args.loop: break
            else: args.bssid = None
        except KeyboardInterrupt:
            ani(f"\n{Colors.RED}[!] Saliendo...{Colors.RESET}"); break

if __name__ == '__main__':
    main()
