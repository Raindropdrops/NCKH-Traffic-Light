import json
import os

FLOWS_PATH = r'd:\Nam 2(D)\NCKH\traffic-mqtt-demo\node-red\flows.json'
SVG_JS_PATH = r'd:\Nam 2(D)\NCKH\traffic-mqtt-demo\node-red\svg_gen.js'
MAP_TPL_PATH = r'd:\Nam 2(D)\NCKH\traffic-mqtt-demo\node-red\map_template.html'
CTRL_TPL_PATH = r'd:\Nam 2(D)\NCKH\traffic-mqtt-demo\node-red\controls_template.html'

def load_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    print("Loading flows...")
    with open(FLOWS_PATH, 'r', encoding='utf-8') as f:
        flows = json.load(f)

    svg_js = load_file(SVG_JS_PATH)
    map_html = load_file(MAP_TPL_PATH)
    ctrl_html = load_file(CTRL_TPL_PATH)

    # 1. Groups & Map Template
    group_ctrl = next((n for n in flows if n.get('id') == 'ui-group.dashboard'), None)
    if group_ctrl:
        group_ctrl['width'] = "8"
        group_ctrl['name'] = "Controls & Charts"
    else:
        # Create if missing (simplified for update logic)
        pass 

    group_map = next((n for n in flows if n.get('id') == 'ui-group.map'), None)
    if not group_map:
        group_map = {
            "id": "ui-group.map", "type": "ui_group", "name": "Intersection Map",
            "tab": "ui-tab.main", "order": 1, "disp": False, "width": "16"
        }
        flows.append(group_map)

    tpl_map = next((n for n in flows if n.get('id') == 'ui.tpl.map'), None)
    if not tpl_map:
        tpl_map = {
            "id": "ui.tpl.map", "type": "ui_template", "z": "flow.traffic-dashboard",
            "group": "ui-group.map", "width": "16", "height": "20",
            "format": map_html, "storeOutMessages": True, "fwdInMessages": True,
            "x": 600, "y": 440, "wires": [[]]
        }
        flows.append(tpl_map)
    else:
        tpl_map['format'] = map_html
    
    # 2. Controls Template
    tpl_ctrl = next((n for n in flows if n.get('id') == 'ui.tpl.dashboard'), None)
    if tpl_ctrl:
        tpl_ctrl['format'] = ctrl_html
        tpl_ctrl['width'] = "8"
        tpl_ctrl['height'] = "14" # Make room for charts

    # 3. SVG Generator
    svg_node = next((n for n in flows if n.get('id') == 'func.intersection-svg'), None)
    if svg_node:
        svg_node['func'] = svg_js
        svg_node['wires'] = [['ui.tpl.map']] # Rewire to map

    # 4. Charts Logic
    # RTT Chart
    chart_rtt = next((n for n in flows if n.get('id') == 'ui_chart.rtt'), None)
    if not chart_rtt:
        chart_rtt = {
            "id": "ui_chart.rtt", "type": "ui_chart", "z": "flow.traffic-dashboard",
            "name": "RTT", "group": "ui-group.dashboard", "order": 4, 
            "width": "8", "height": "4", "label": "Command Latency (ms)",
            "chartType": "line", "ymin": "0", "ymax": "200", "removeOlder": "5",
            "colors": ["#38bdf8"], "x": 600, "y": 660, "wires": [[]]
        }
        flows.append(chart_rtt)

    # RSSI Chart
    chart_rssi = next((n for n in flows if n.get('id') == 'ui_chart.rssi'), None)
    if not chart_rssi:
        chart_rssi = {
            "id": "ui_chart.rssi", "type": "ui_chart", "z": "flow.traffic-dashboard",
            "name": "RSSI", "group": "ui-group.dashboard", "order": 5,
            "width": "4", "height": "3", "label": "Signal (dBm)",
            "chartType": "line", "ymin": "-90", "ymax": "-30", "removeOlder": "5",
            "colors": ["#22c55e"], "x": 600, "y": 520, "wires": [[]]
        }
        flows.append(chart_rssi)

    # Heap Chart
    chart_heap = next((n for n in flows if n.get('id') == 'ui_chart.heap'), None)
    if not chart_heap:
        chart_heap = {
            "id": "ui_chart.heap", "type": "ui_chart", "z": "flow.traffic-dashboard",
            "name": "Heap", "group": "ui-group.dashboard", "order": 6,
            "width": "4", "height": "3", "label": "Free Heap (KB)",
            "chartType": "line", "ymin": "0", "ymax": "300", "removeOlder": "5",
            "colors": ["#f59e0b"], "x": 600, "y": 560, "wires": [[]]
        }
        flows.append(chart_heap)

    # 4. Wiring & Logic
    # Telemetry Splitter
    func_tel = next((n for n in flows if n.get('id') == 'func.parse-telemetry'), None)
    if func_tel:
        func_tel['outputs'] = 3
        func_tel['func'] = """
const d = msg.payload || {};
const out = {
    rssi_dbm: (d.rssi_dbm !== undefined ? d.rssi_dbm : null),
    heap_free_kb: (d.heap_free_kb !== undefined ? d.heap_free_kb : null),
    uptime_s: (d.uptime_s !== undefined ? d.uptime_s : null),
    ts_ms: (d.ts_ms !== undefined ? d.ts_ms : null)
};
return [
    { topic: 'telemetry', payload: out },
    (out.rssi_dbm !== null) ? { payload: out.rssi_dbm, topic: 'RSSI' } : null,
    (out.heap_free_kb !== null) ? { payload: out.heap_free_kb, topic: 'Heap' } : null
];
"""
        func_tel['wires'] = [['func.dashboard-store'], ['ui_chart.rssi'], ['ui_chart.heap']]

    # ACK Log & RTT
    func_ack = next((n for n in flows if n.get('id') == 'func.ack-log'), None)
    if func_ack:
        func_ack['outputs'] = 2
        func_ack['func'] = """
let log = flow.get('ack_log') || [];
let pending = flow.get('pending_cmds') || {};
const d = msg.payload || {};
const id = d.cmd_id;
const now = Date.now();
let rtt = null;

if (id && pending[id]) {
    rtt = now - pending[id];
    delete pending[id];
    flow.set('pending_cmds', pending);
}

log.unshift({
    t: new Date().toLocaleTimeString(),
    id: (id || '').substring(0, 8),
    type: d.type || 'ACK',
    ok: !!d.ok,
    err: d.err || '',
    rtt: rtt
});
if (log.length > 20) log.pop();
flow.set('ack_log', log);

return [
    { topic: 'ack_log', payload: log },
    (rtt !== null) ? { payload: rtt, topic: 'RTT' } : null
];
"""
        func_ack['wires'] = [['func.dashboard-store'], ['ui_chart.rtt']]

    # Save
    with open(FLOWS_PATH, 'w', encoding='utf-8') as f:
        json.dump(flows, f, indent=4)
    print("Success: Flows rebuilt for Dashboard PRO.")

if __name__ == '__main__':
    main()
