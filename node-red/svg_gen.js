const phase = msg.payload.phase;
// 0:NS_GREEN 1:NS_YELLOW 2:ALL_RED 3:EW_GREEN 4:EW_YELLOW 5:ALL_RED
const DIM = { r: '#3a1e1e', y: '#3a321e', g: '#1e3a2e' };
const BRIGHT = { r: '#ff2222', y: '#ffbf00', g: '#00ff44' };

const P = {
    NS: { r: DIM.r, y: DIM.y, g: DIM.g },
    EW: { r: DIM.r, y: DIM.y, g: DIM.g }
};

let phaseColor = '#475569';

switch(phase) {
    case 0: P.NS.g=BRIGHT.g; P.EW.r=BRIGHT.r; phaseColor='#22c55e'; break;
    case 1: P.NS.y=BRIGHT.y; P.EW.r=BRIGHT.r; phaseColor='#eab308'; break;
    case 2: P.NS.r=BRIGHT.r; P.EW.r=BRIGHT.r; phaseColor='#ef4444'; break;
    case 3: P.EW.g=BRIGHT.g; P.NS.r=BRIGHT.r; phaseColor='#22c55e'; break;
    case 4: P.EW.y=BRIGHT.y; P.NS.r=BRIGHT.r; phaseColor='#eab308'; break;
    case 5: P.NS.r=BRIGHT.r; P.EW.r=BRIGHT.r; phaseColor='#ef4444'; break;
    default: P.NS.r=BRIGHT.r; P.EW.r=BRIGHT.r;
}

const phaseNames=['NS GREEN','NS YELLOW','ALL RED','EW GREEN','EW YELLOW','ALL RED'];
const pName = phaseNames[phase] || 'UNKNOWN';

function drawPole(x, y, rot, lights, label) {
    return `
    <g transform="translate(${x}, ${y}) rotate(${rot})">
        <circle cx="0" cy="0" r="12" fill="#111" opacity="0.5" />
        <rect x="-6" y="-10" width="12" height="60" fill="#475569" rx="4" />
        <rect x="-24" y="40" width="48" height="110" rx="12" fill="#1e293b" stroke="#334155" stroke-width="2" />
        <circle cx="0" cy="60" r="14" fill="${lights.r}" filter="url(#glow-${lights.r === BRIGHT.r ? 'red' : 'none'})" />
        <circle cx="0" cy="95" r="14" fill="${lights.y}" filter="url(#glow-${lights.y === BRIGHT.y ? 'yellow' : 'none'})" />
        <circle cx="0" cy="130" r="14" fill="${lights.g}" filter="url(#glow-${lights.g === BRIGHT.g ? 'green' : 'none'})" />
    </g>
    `;
}

let svg = `
<svg viewBox="0 0 800 800" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:100%; max-height:600px; display:block; margin:auto; background: radial-gradient(circle at 50% 50%, #1e293b 0%, #0f172a 100%); border-radius:16px; border:1px solid #334155;">
  <defs>
    <filter id="glow-red" height="300%" width="300%" x="-100%" y="-100%">
      <feGaussianBlur stdDeviation="8" result="coloredBlur"/>
      <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glow-yellow" height="300%" width="300%" x="-100%" y="-100%">
      <feGaussianBlur stdDeviation="8" result="coloredBlur"/>
      <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glow-green" height="300%" width="300%" x="-100%" y="-100%">
      <feGaussianBlur stdDeviation="8" result="coloredBlur"/>
      <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glow-none"><feGaussianBlur stdDeviation="0"/></filter>
  </defs>

  <rect x="0" y="0" width="800" height="800" fill="#0f172a" />
  <path d="M 250 0 L 550 0 L 550 800 L 250 800 Z" fill="#1e293b" stroke="#334155" stroke-width="2"/>
  <path d="M 0 250 L 800 250 L 800 550 L 0 550 Z" fill="#1e293b" stroke="#334155" stroke-width="2"/>
  <rect x="250" y="250" width="300" height="300" fill="#1e293b" />

  <line x1="400" y1="0" x2="400" y2="250" stroke="#f8fafc" stroke-width="4" stroke-dasharray="20 30" opacity="0.3"/>
  <line x1="400" y1="550" x2="400" y2="800" stroke="#f8fafc" stroke-width="4" stroke-dasharray="20 30" opacity="0.3"/>
  <line x1="0" y1="400" x2="250" y2="400" stroke="#f8fafc" stroke-width="4" stroke-dasharray="20 30" opacity="0.3"/>
  <line x1="550" y1="400" x2="800" y2="400" stroke="#f8fafc" stroke-width="4" stroke-dasharray="20 30" opacity="0.3"/>
  
  <rect x="250" y="240" width="150" height="10" fill="white" opacity="0.8" />
  <rect x="400" y="550" width="150" height="10" fill="white" opacity="0.8" />
  <rect x="240" y="400" width="10" height="150" fill="white" opacity="0.8" />
  <rect x="550" y="250" width="10" height="150" fill="white" opacity="0.8" />

  ${drawPole(220, 220, 135, P.NS, 'N')}
  ${drawPole(580, 580, -45, P.NS, 'S')}
  ${drawPole(220, 580, 45, P.EW, 'W')}
  ${drawPole(580, 220, 225, P.EW, 'E')}

  <g transform="translate(400, 400)">
    <circle r="45" fill="#0f172a" stroke="#334155" stroke-width="4" />
    <circle r="40" fill="none" stroke="${phaseColor}" stroke-width="2" opacity="0.5">
        <animate attributeName="r" values="40;55;40" dur="2s" repeatCount="indefinite" />
        <animate attributeName="opacity" values="0.6;0;0.6" dur="2s" repeatCount="indefinite" />
    </circle>
    <text y="10" text-anchor="middle" fill="${phaseColor}" font-family="monospace" font-size="28" font-weight="900" style="text-shadow: 0 0 10px ${phaseColor};">${phase}</text>
  </g>
  
  <text x="400" y="760" text-anchor="middle" fill="#94a3b8" font-size="18" font-weight="600" letter-spacing="3" opacity="0.8">${pName}</text>
</svg>`;

msg.topic = 'intersection';
msg.payload = svg;
return msg;
