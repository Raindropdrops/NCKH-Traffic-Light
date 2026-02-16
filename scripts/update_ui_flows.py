import json

FLOWS_PATH = r'd:\Nam 2(D)\NCKH\traffic-mqtt-demo\node-red\flows.json'
SVG_JS_PATH = r'd:\Nam 2(D)\NCKH\traffic-mqtt-demo\node-red\svg_gen.js'
DASH_HTML_PATH = r'd:\Nam 2(D)\NCKH\traffic-mqtt-demo\node-red\dashboard.html'

def load_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    print("Loading flows...")
    with open(FLOWS_PATH, 'r', encoding='utf-8') as f:
        flows = json.load(f)

    print("Loading new UI components...")
    svg_js = load_file(SVG_JS_PATH)
    dash_html = load_file(DASH_HTML_PATH)
    
    updated_svg = False
    updated_html = False
    groups_updated = 0

    for node in flows:
        if node.get('id') == 'func.intersection-svg':
            node['func'] = svg_js
            updated_svg = True
            print("Updated SVG Generator")
        
        if node.get('id') == 'ui.tpl.dashboard':
            node['format'] = dash_html
            node['width'] = "24"
            updated_html = True
            print("Updated UI Template")
            
        if node.get('id') == 'ui-group.dashboard':
            node['width'] = "24"
            groups_updated += 1
            print("Updated UI Group Width")

    if updated_svg and updated_html:
        with open(FLOWS_PATH, 'w', encoding='utf-8') as f:
            json.dump(flows, f, indent=4)
        print("Success! flows.json updated.")
    else:
        print("Error: Could not locate target nodes.")

if __name__ == '__main__':
    main()
