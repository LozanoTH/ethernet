import json, threading, time, os, re
from http.server import HTTPServer, BaseHTTPRequestHandler
from lib.utils import info, success, error, WEB_LOGS
from lib.core import Companion

GLOBAL_STATE = {
    'networks': {},
    'is_scanning': False,
    'current_attack': None,
    'scanner': None,
    'companion': None,
    'args': None
}

class WebHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args): pass

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
        else: self.send_error(404)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        try: params = json.loads(post_data)
        except: params = {}

        if self.path == '/api/scan':
            if not GLOBAL_STATE['is_scanning']:
                threading.Thread(target=self._bg_scan).start()
                self._send_json({'status': 'ok'})
        elif self.path == '/api/attack':
            bssid = params.get('bssid')
            if bssid and not GLOBAL_STATE['current_attack']:
                threading.Thread(target=self._bg_attack, args=(bssid,)).start()
                self._send_json({'status': 'ok'})

    def _bg_scan(self):
        GLOBAL_STATE['is_scanning'] = True
        try:
            nets = GLOBAL_STATE['scanner'].iw_scanner()
            if nets: GLOBAL_STATE['networks'] = nets
        except Exception as e: error(f"Error scan web: {e}")
        GLOBAL_STATE['is_scanning'] = False

    def _bg_attack(self, bssid):
        GLOBAL_STATE['current_attack'] = bssid
        try:
            args = GLOBAL_STATE['args']
            if not GLOBAL_STATE['companion']:
                GLOBAL_STATE['companion'] = Companion(args.interface, args.write, print_debug=args.verbose)
            GLOBAL_STATE['companion'].single_connection(bssid, pixiemode=args.pixie_dust, auto=True)
        except Exception as e: error(f"Error ataque web: {e}")
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
                :root { --primary: #00ffa3; --primary-dim: rgba(0, 255, 163, 0.1); --bg: #050505; --card: #111111; --border: #222222; --text: #ffffff; --text-dim: #888888; --danger: #ff4444; }
                * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
                body { font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); margin:0; padding-bottom: 70px; }
                .header { padding: 15px 20px; background: rgba(17, 17, 17, 0.9); backdrop-filter: blur(10px); border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 100; }
                .logo { font-size: 18px; font-weight: 800; }
                .logo span { color: var(--primary); }
                .tab-content { display: none; padding: 15px; animation: fadeIn 0.3s ease; }
                .tab-content.active { display: block; }
                @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
                .nav-bar { position: fixed; bottom: 0; left: 0; width: 100%; background: #111; border-top: 1px solid var(--border); display: flex; justify-content: space-around; padding: 10px 0; z-index: 1000; }
                .nav-item { background: none; border: none; color: var(--text-dim); font-size: 12px; font-weight: 600; display: flex; flex-direction: column; align-items: center; gap: 5px; cursor: pointer; transition: 0.2s; flex: 1; }
                .nav-item.active { color: var(--primary); }
                .nav-icon { width: 20px; height: 20px; fill: currentColor; }
                .networks-grid { display: grid; grid-template-columns: 1fr; gap: 12px; }
                @media (min-width: 768px) { .networks-grid { grid-template-columns: repeat(2, 1fr); } }
                .net-item { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 15px; display: flex; flex-direction: column; gap: 12px; }
                .net-essid { font-weight: 800; font-size: 16px; color: var(--text); }
                .net-essid.vuln { color: var(--primary); text-shadow: 0 0 10px var(--primary-dim); }
                .badge { padding: 3px 8px; border-radius: 5px; background: #222; font-size: 10px; font-weight: 700; }
                .badge.vuln { color: var(--primary); background: var(--primary-dim); }
                .btn-attack { width: 100%; padding: 12px; border-radius: 8px; border: none; background: #2196F3; color: white; font-weight: 800; font-size: 13px; }
                .console-wrapper { background: #000; border-radius: 12px; border: 1px solid var(--border); height: calc(100vh - 180px); display: flex; flex-direction: column; }
                .console-header { padding: 10px 15px; border-bottom: 1px solid #222; font-size: 11px; color: #555; font-family: 'JetBrains Mono', monospace; }
                .logs-container { flex: 1; padding: 15px; overflow-y: auto; font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #00ff41; line-height: 1.6; }
                .log-line { margin-bottom: 6px; border-bottom: 1px solid #0a0a0a; }
                .log-time { color: #444; margin-right: 10px; }
                .btn-scan-main { background: var(--primary); color: black; padding: 15px; border-radius: 10px; width: 100%; font-weight: 800; border: none; margin-bottom: 20px; }
            </style>
        </head>
        <body>
            <div class="header">
                <div class="logo">WPS<span>AUDITOR</span></div>
                <div id="statusDot" style="width:10px; height:10px; background:#444; border-radius:50%"></div>
            </div>
            <div id="tab-networks" class="tab-content active">
                <button class="btn-scan-main" onclick="startScan()" id="scanBtn">ESCANEAR REDES</button>
                <div id="networksList" class="networks-grid">
                    <div style="text-align:center; color:#555; padding:50px">Cargando redes...</div>
                </div>
            </div>
            <div id="tab-console" class="tab-content">
                <div class="console-wrapper">
                    <div class="console-header">WPS_AUDITOR_TERMINAL_V1.0.2</div>
                    <div class="logs-container" id="logs"></div>
                </div>
            </div>
            <div class="nav-bar">
                <button class="nav-item active" onclick="switchTab('networks', this)">
                    <svg class="nav-icon" viewBox="0 0 24 24"><path d="M12 3L2 12h3v8h6v-6h2v6h6v-8h3L12 3z"/></svg>
                    REDES
                </button>
                <button class="nav-item" onclick="switchTab('console', this)">
                    <svg class="nav-icon" viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zM4 18V6h16v12H4z"/></svg>
                    CONSOLA
                </button>
            </div>
            <script>
                function switchTab(tabId, el) {
                    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
                    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
                    document.getElementById('tab-' + tabId).classList.add('active');
                    el.classList.add('active');
                }
                async function startScan() {
                    const btn = document.getElementById('scanBtn');
                    btn.disabled = true; btn.innerText = 'ESCANEANDO...';
                    await fetch('/api/scan', {method: 'POST'});
                }
                async function attack(bssid) {
                    if(!confirm('¿Atacar ' + bssid + '?')) return;
                    switchTab('console', document.querySelectorAll('.nav-item')[1]);
                    await fetch('/api/attack', {method: 'POST', body: JSON.stringify({bssid: bssid})});
                }
                function updateLogs() {
                    fetch('/api/logs').then(r => r.json()).then(logs => {
                        const div = document.getElementById('logs');
                        const isAtBottom = div.scrollHeight - div.clientHeight <= div.scrollTop + 2;
                        div.innerHTML = logs.map(l => {
                            const time = l.match(/\[(.*?)\]/)?.[1] || '--:--';
                            const msg = l.replace(/\[.*?\] /, '');
                            return `<div class="log-line"><span class="log-time">${time}</span>${msg}</div>`;
                        }).join('');
                        if (isAtBottom) div.scrollTop = div.scrollHeight;
                    });
                }
                function updateNetworks() {
                    fetch('/api/networks').then(r => r.json()).then(nets => {
                        const container = document.getElementById('networksList');
                        let html = '';
                        const netArray = Array.isArray(nets) ? nets : Object.values(nets);
                        netArray.forEach(n => {
                            const isVuln = n.Model && (n.Model.includes('Archer') || n.Model.includes('TD-W'));
                            const locked = n['WPS locked'];
                            html += `<div class="net-item">
                                <div class="net-essid ${isVuln ? 'vuln' : ''}">${n.ESSID || '<Oculto>'}</div>
                                <div style="font-size:11px; color:#555; font-family:monospace">${n.BSSID}</div>
                                <div style="display:flex; gap:8px; margin-top:5px">
                                    <span class="badge ${locked ? '' : 'vuln'}">WPS: ${locked ? 'LOCKED' : 'OPEN'}</span>
                                    <span class="badge">PWR: ${n.Level}dBm</span>
                                </div>
                                <button class="btn-attack" onclick="attack('${n.BSSID}')" ${locked ? 'disabled style="opacity:0.3"' : ''}>${locked ? 'BLOQUEADO' : 'ATACAR'}</button>
                            </div>`;
                        });
                        if(html) container.innerHTML = html;
                    });
                }
                function updateStatus() {
                    fetch('/api/status').then(r => r.json()).then(st => {
                        const dot = document.getElementById('statusDot');
                        dot.style.background = st.current_attack ? '#ff4444' : (st.is_scanning ? '#00ffa3' : '#444');
                        if(!st.is_scanning) {
                            const btn = document.getElementById('scanBtn');
                            btn.disabled = false; btn.innerText = 'ESCANEAR REDES';
                        }
                    });
                }
                setInterval(updateLogs, 1500); setInterval(updateNetworks, 4000); setInterval(updateStatus, 2000);
                updateLogs();
            </script>
        </body>
        </html>
        """

def start_web_server(scanner, args, port=8080):
    GLOBAL_STATE['scanner'] = scanner
    GLOBAL_STATE['args'] = args
    class ReusableHTTPServer(HTTPServer):
        def server_bind(self):
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try: self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            except AttributeError: pass
            super().server_bind()

    def run():
        try:
            server = ReusableHTTPServer(('0.0.0.0', port), WebHandler)
            server.serve_forever()
        except Exception as e:
            if "Address already in use" in str(e): error(f"Puerto {port} ocupado.")
            else: error(f"Error servidor web: {e}")

    threading.Thread(target=run, daemon=True).start()
    print(f"\nApp Web iniciada en http://localhost:{port}\n")
