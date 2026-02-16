const phase = msg.payload.phase;
// 0:NS_GREEN 1:NS_YELLOW 2:ALL_RED 3:EW_GREEN 4:EW_YELLOW 5:ALL_RED
// Colors: Off state is dim, On state is bright
const DIM = { r: '#3a1e1e', y: '#3a321e', g: '#1e3a2e' };
const BRIGHT = { r: '#ff2222', y: '#ffbf00', g: '#00ff44' };

const P = {
    NS: { r: DIM.r, y: DIM.y, g: DIM.g },
    EW: { r: DIM.r, y: DIM.y, g: DIM.g }
};

// Logic for light states
switch(phase) {
    case 0: P.NS.g=BRIGHT.g; P.EW.r=BRIGHT.r; break; // NS Green
    case 1: P.NS.y=BRIGHT.y; P.EW.r=BRIGHT.r; break; // NS Yellow
    case 2: P.NS.r=BRIGHT.r; P.EW.r=BRIGHT.r; break; // All Red
    case 3: P.EW.g=BRIGHT.g; P.NS.r=BRIGHT.r; break; // EW Green
    case 4: P.EW.y=BRIGHT.y; P.NS.r=BRIGHT.r; break; // EW Yellow
    case 5: P.NS.r=BRIGHT.r; P.EW.r=BRIGHT.r; break; // All Red
    default: P.NS.r=BRIGHT.r; P.EW.r=BRIGHT.r; // Safe default
}

const phaseNames=['NS GREEN','NS YELLOW','ALL RED','EW GREEN','EW YELLOW','ALL RED'];
const pName = phaseNames[phase] || 'UNKNOWN';

// Helper to draw a traffic light pole
// x,y: position
// rot: rotation degrees
// lights: object {r,y,g} colors
// label: N/S/E/W
function drawPole(x, y, rot, lights, label) {
    return `
    <g transform="translate(${x}, ${y}) rotate(${rot})">
        <!-- Pole Shadow -->
        <circle cx="0" cy="0" r="12" fill="#111" opacity="0.5" />
        <!-- Arm -->
        <rect x="-6" y="-10" width="12" height="60" fill="#475569" rx="4" />
        <!-- Housing -->
        <rect x="-24" y="40" width="48" height="110" rx="12" fill="#1e293b" stroke="#334155" stroke-width="2" />
        <!-- Lights -->
        <!-- Red -->
        <circle cx="0" cy="60" r="14" fill="${lights.r}" filter="url(#glow-${lights.r === BRIGHT.r ? 'red' : 'none'})" />
        <!-- Yellow -->
        <circle cx="0" cy="95" r="14" fill="${lights.y}" filter="url(#glow-${lights.y === BRIGHT.y ? 'yellow' : 'none'})" />
        <!-- Green -->
        <circle cx="0" cy="130" r="14" fill="${lights.g}" filter="url(#glow-${lights.g === BRIGHT.g ? 'green' : 'none'})" />
        <!-- Visors (visual touch) -->
        <path d="M-16 50 Q 0 44 16 50" stroke="#0f172a" stroke-width="2" fill="none" />
        <path d="M-16 85 Q 0 79 16 85" stroke="#0f172a" stroke-width="2" fill="none" />
        <path d="M-16 120 Q 0 114 16 120" stroke="#0f172a" stroke-width="2" fill="none" />
        <!-- Label -->
        <text x="0" y="170" fill="#94a3b8" font-size="14" font-weight="bold" text-anchor="middle" transform="rotate(${-rot} 0 170)">${label}</text>
    </g>
    `;
}

// SVG Construction
let svg = `
<svg viewBox="0 0 800 800" style="width:100%; height:100%; max-height:600px; display:block; margin:auto; background:#0f172a; border-radius:16px;">
  <defs>
    <!-- Glow Filters -->
    <filter id="glow-red" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="6" result="coloredBlur"/>
      <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glow-yellow" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur stdDeviation="6" result="coloredBlur"/>
        <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glow-green" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur stdDeviation="6" result="coloredBlur"/>
        <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glow-none"><feGaussianBlur stdDeviation="0"/></filter>
    <!-- Patterns -->
    <pattern id="road-texture" x="0" y="0" width="10" height="10" patternUnits="userSpaceOnUse">
        <rect width="10" height="10" fill="#334155" />
        <circle cx="1" cy="1" r="1" fill="#475569" opacity="0.3"/>
    </pattern>
  </defs>

  <!-- Grass/Ground -->
  <rect x="0" y="0" width="800" height="800" fill="#0f172a" />
  
  <!-- Roads (Cross) -->
  <rect x="250" y="0" width="300" height="800" fill="#1e293b" stroke="#334155" stroke-width="2"/>
  <rect x="0" y="250" width="800" height="300" fill="#1e293b" stroke="#334155" stroke-width="2"/>
  <rect x="250" y="250" width="300" height="300" fill="#1e293b" /> <!-- Intersection Center -->

  <!-- Lane Markings (Dashed) -->
  <line x1="400" y1="0" x2="400" y2="250" stroke="#f1f5f9" stroke-width="4" stroke-dasharray="20 20" opacity="0.5"/>
  <line x1="400" y1="550" x2="400" y2="800" stroke="#f1f5f9" stroke-width="4" stroke-dasharray="20 20" opacity="0.5"/>
  <line x1="0" y1="400" x2="250" y2="400" stroke="#f1f5f9" stroke-width="4" stroke-dasharray="20 20" opacity="0.5"/>
  <line x1="550" y1="400" x2="800" y2="400" stroke="#f1f5f9" stroke-width="4" stroke-dasharray="20 20" opacity="0.5"/>

  <!-- Stop Lines -->
  <rect x="255" y="240" width="135" height="8" fill="#f1f5f9" opacity="0.8"/> <!-- N Stop -->
  <rect x="410" y="552" width="135" height="8" fill="#f1f5f9" opacity="0.8"/> <!-- S Stop -->
  <rect x="240" y="410" width="8" height="135" fill="#f1f5f9" opacity="0.8"/> <!-- W Stop -->
  <rect x="552" y="255" width="8" height="135" fill="#f1f5f9" opacity="0.8"/> <!-- E Stop -->

  <!-- Traffic Light Poles -->
  <!-- North (Rotated 180 to face oncoming traffic) -->
  ${drawPole(220, 220, 135, P.NS, 'NORTH')}
  
  <!-- South -->
  ${drawPole(580, 580, -45, P.NS, 'SOUTH')}

  <!-- West -->
  ${drawPole(220, 580, 45, P.EW, 'WEST')}

  <!-- East -->
  ${drawPole(580, 220, 225, P.EW, 'EAST')}

  <!-- Center Info Overlay -->
  <g transform="translate(400, 400)">
    <circle r="40" fill="#0f172a" stroke="#4ecdc4" stroke-width="2" opacity="0.9"/>
    <text y="5" text-anchor="middle" fill="#fff" font-family="monospace" font-size="24" font-weight="bold">${phase}</text>
  </g>
  
  <!-- Phase Label -->
  <text x="400" y="780" text-anchor="middle" fill="#94a3b8" font-size="20" letter-spacing="2">${pName}</text>
</svg>`;

msg.topic = 'intersection';
msg.payload = svg;
return msg;
