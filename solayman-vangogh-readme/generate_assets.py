#!/usr/bin/env python3
"""
Generate all SVG assets for Solayman El Mouden's GitHub Profile README.
Visual identity: Van Gogh flowing spirals — teal/blue-green sky, golden fields.
"""
import math
import os

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# ─── Color Palettes ────────────────────────────────────────────────
DARK = {
    "bg1": "#0A1A1F", "bg2": "#0F2832", "bg3": "#112E38",
    "text1": "#F0F5F0", "text2": "#D0DFE2", "text3": "#9BB8BC",
    "teal1": "#3B7A8C", "teal2": "#5BA3A0", "teal3": "#6FB5A2", "teal4": "#2D6B77",
    "gold1": "#C4A843", "gold2": "#D4B64A", "gold3": "#8FA055",
    "accent": "#8BBFC4", "card_border": "rgba(59,122,140,0.3)",
    "card_bg1": "#0C1E25", "card_bg2": "#112A33",
}
LIGHT = {
    "bg1": "#FAFDF7", "bg2": "#F0F5EE", "bg3": "#E8EFE5",
    "text1": "#1A2F35", "text2": "#2D4A52", "text3": "#5A7A7F",
    "teal1": "#2D6B77", "teal2": "#3B7A8C", "teal3": "#5BA3A0", "teal4": "#1F5560",
    "gold1": "#8A7030", "gold2": "#A08838", "gold3": "#6B7A3A",
    "accent": "#3B7A8C", "card_border": "rgba(45,107,119,0.35)",
    "card_bg1": "#F5F8F2", "card_bg2": "#EDF2E9",
}

# ─── Spiral Path Generator ─────────────────────────────────────────
def spiral_path(cx, cy, start_r, end_r, turns, start_angle=0, steps_per_turn=30):
    """Generate SVG path data for a spiral using smooth cubic beziers."""
    total_steps = max(int(turns * steps_per_turn), 8)
    points = []
    for i in range(total_steps + 1):
        t = i / total_steps
        angle = start_angle + t * turns * 2 * math.pi
        r = start_r + t * (end_r - start_r)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        points.append((x, y))
    return points_to_smooth_path(points)

def wave_path(x1, y1, x2, y2, amplitude=20, waves=3):
    """Generate a wavy line path."""
    dx = x2 - x1
    dy = y2 - y1
    length = math.sqrt(dx*dx + dy*dy)
    nx, ny = -dy/length, dx/length  # normal
    points = []
    steps = waves * 20
    for i in range(steps + 1):
        t = i / steps
        wave = math.sin(t * waves * 2 * math.pi) * amplitude
        x = x1 + t * dx + wave * nx
        y = y1 + t * dy + wave * ny
        points.append((x, y))
    return points_to_smooth_path(points)

def points_to_smooth_path(points):
    """Convert points to smooth SVG cubic bezier path."""
    if len(points) < 2:
        return ""
    d = f"M {points[0][0]:.1f} {points[0][1]:.1f}"
    for i in range(1, len(points)):
        if i == 1:
            cp1x = points[0][0] + (points[1][0] - points[0][0]) / 3
            cp1y = points[0][1] + (points[1][1] - points[0][1]) / 3
            cp2x = points[1][0] - (points[min(2, len(points)-1)][0] - points[0][0]) / 3
            cp2y = points[1][1] - (points[min(2, len(points)-1)][1] - points[0][1]) / 3
        else:
            prev = points[i-2]
            curr = points[i-1]
            next_p = points[i]
            cp1x = curr[0] + (next_p[0] - prev[0]) / 6
            cp1y = curr[1] + (next_p[1] - prev[1]) / 6
            if i < len(points) - 1:
                next_next = points[i+1]
                cp2x = next_p[0] - (next_next[0] - curr[0]) / 6
                cp2y = next_p[1] - (next_next[1] - curr[1]) / 6
            else:
                cp2x = next_p[0] - (next_p[0] - curr[0]) / 3
                cp2y = next_p[1] - (next_p[1] - curr[1]) / 3
        d += f" C {cp1x:.1f} {cp1y:.1f}, {cp2x:.1f} {cp2y:.1f}, {points[i][0]:.1f} {points[i][1]:.1f}"
    return d

def flowing_curve(x1, y1, x2, y2, bend=40):
    """Simple flowing curve between two points."""
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2 - bend
    return f"M {x1:.1f} {y1:.1f} Q {mx:.1f} {my:.1f} {x2:.1f} {y2:.1f}"

def concentric_spirals_svg(cx, cy, count=5, min_r=5, max_r=60, opacity_start=0.4, opacity_end=0.05, color="#3B7A8C", turns_range=(1.5, 3)):
    """Generate multiple concentric spiral paths."""
    lines = []
    for i in range(count):
        t = i / max(count - 1, 1)
        r_start = min_r + t * (max_r - min_r) * 0.3
        r_end = min_r + t * (max_r - min_r)
        turns = turns_range[0] + t * (turns_range[1] - turns_range[0])
        angle = i * math.pi * 0.7
        opacity = opacity_start - t * (opacity_start - opacity_end)
        d = spiral_path(cx, cy, r_start, r_end, turns, start_angle=angle)
        lines.append(f'  <path d="{d}" fill="none" stroke="{color}" stroke-width="{1.2 - t*0.6:.1f}" opacity="{opacity:.2f}"/>')
    return "\n".join(lines)

def dot_nodes(positions, color="#C4A843", r=2, opacity=0.5):
    """Generate small decorative dot nodes."""
    return "\n".join(
        f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}" opacity="{opacity}"/>'
        for x, y in positions
    )

def grid_pattern(pid="grid", size=40, color="#3B7A8C", opacity=0.03):
    """SVG pattern for subtle background grid."""
    return f'''<pattern id="{pid}" width="{size}" height="{size}" patternUnits="userSpaceOnUse">
      <path d="M {size} 0 L 0 0 0 {size}" fill="none" stroke="{color}" stroke-width="0.5" opacity="{opacity}"/>
    </pattern>'''

# ─── CSS Animations ─────────────────────────────────────────────────
HEADER_ANIMATIONS = """
  <style>
    @keyframes spiralPulse {
      0%, 100% { opacity: 0.35; }
      50% { opacity: 0.55; }
    }
    @keyframes nodePulse {
      0%, 100% { opacity: 0.3; r: 2; }
      50% { opacity: 0.7; r: 3; }
    }
    @keyframes flowDrift {
      0% { stroke-dashoffset: 0; }
      100% { stroke-dashoffset: -200; }
    }
    .spiral-animated { animation: spiralPulse 12s ease-in-out infinite; }
    .node-animated { animation: nodePulse 8s ease-in-out infinite; }
    .flow-animated {
      stroke-dasharray: 8 12;
      animation: flowDrift 16s linear infinite;
    }
  </style>
"""

# ─── HEADER SVG ─────────────────────────────────────────────────────
def generate_header(mode="dark"):
    p = DARK if mode == "dark" else LIGHT
    W, H = 1100, 380

    # Generate spiral paths for the background
    spirals = []
    # Large flowing spirals on the right side
    for i, (cx, cy, sr, er, t, sa) in enumerate([
        (820, 120, 8, 120, 2.8, 0),
        (950, 200, 5, 90, 2.2, 1.2),
        (750, 280, 10, 100, 2.5, 2.5),
        (900, 80, 6, 70, 1.8, 0.8),
        (680, 160, 12, 80, 2.0, 3.8),
        (1000, 300, 4, 60, 1.5, 1.5),
        (600, 60, 8, 110, 2.3, 4.5),
        (850, 340, 6, 50, 1.6, 2.0),
    ]):
        opacity = 0.25 - i * 0.02 if mode == "dark" else 0.18 - i * 0.015
        d = spiral_path(cx, cy, sr, er, t, start_angle=sa)
        anim_class = ' class="spiral-animated"' if i % 3 == 0 else ""
        spirals.append(f'  <path d="{d}" fill="none" stroke="{p["teal2"]}" stroke-width="{1.5 - i*0.1:.1f}" opacity="{max(opacity, 0.06):.2f}"{anim_class}/>')

    # Flowing wave curves across the bottom (golden field lines)
    waves = []
    for i in range(5):
        y_base = 300 + i * 18
        amp = 15 - i * 2
        d = wave_path(0, y_base, W, y_base - 10 + i * 5, amplitude=amp, waves=4 + i)
        gold_opacity = 0.15 - i * 0.025 if mode == "dark" else 0.12 - i * 0.02
        flow_class = ' class="flow-animated"' if i % 2 == 0 else ""
        waves.append(f'  <path d="{d}" fill="none" stroke="{p["gold1"]}" stroke-width="{1.0:.1f}" opacity="{max(gold_opacity, 0.04):.2f}"{flow_class}/>')

    # Decorative nodes at spiral centers
    node_positions = [(820, 120), (950, 200), (750, 280), (680, 160), (900, 80), (1000, 300), (600, 60), (850, 340),
                      (770, 190), (880, 250), (920, 140), (980, 100)]
    nodes = []
    for i, (x, y) in enumerate(node_positions):
        anim = ' class="node-animated"' if i % 2 == 0 else ""
        op = 0.4 if mode == "dark" else 0.3
        nodes.append(f'  <circle cx="{x}" cy="{y}" r="2.5" fill="{p["gold1"]}" opacity="{op}"{anim}/>')

    # Small cloud-like spiral clusters (from Van Gogh reference)
    cloud_spirals = []
    for cx, cy in [(750, 50), (1050, 150), (650, 300)]:
        for j in range(3):
            d = spiral_path(cx + j*15, cy + j*8, 2, 15 + j*5, 1.2, start_angle=j*2.1)
            cloud_spirals.append(f'  <path d="{d}" fill="none" stroke="{p["text1"]}" stroke-width="0.6" opacity="0.08"/>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    <linearGradient id="hbg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{p['bg1']}"/>
      <stop offset="0.6" stop-color="{p['bg2']}"/>
      <stop offset="1" stop-color="{p['bg3']}"/>
    </linearGradient>
    {grid_pattern("hgrid", 50, p["teal1"], 0.025 if mode == "dark" else 0.04)}
    {HEADER_ANIMATIONS}
  </defs>

  <rect width="{W}" height="{H}" fill="url(#hbg)"/>
  <rect width="{W}" height="{H}" fill="url(#hgrid)"/>

  <!-- Flowing spiral patterns -->
{chr(10).join(spirals)}

  <!-- Golden field waves -->
{chr(10).join(waves)}

  <!-- Cloud spiral clusters -->
{chr(10).join(cloud_spirals)}

  <!-- Decorative nodes -->
{chr(10).join(nodes)}

  <!-- Text Content -->
  <text x="80" y="110" fill="{p['accent']}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="14" font-weight="300" letter-spacing="2">Hi, I'm</text>
  <text x="80" y="158" fill="{p['text1']}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="32" font-weight="700" letter-spacing="6">SOLAYMAN EL MOUDEN</text>
  <text x="82" y="195" fill="{p['gold1']}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="16" font-weight="500" letter-spacing="3">Software Engineer</text>
  <text x="82" y="228" fill="{p['teal2']}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="13" font-weight="400" letter-spacing="1.5">AI  ·  Math  ·  Newest Technologies</text>
  <line x1="80" y1="245" x2="420" y2="245" stroke="{p['gold1']}" stroke-width="0.5" opacity="0.3"/>
  <text x="82" y="272" fill="{p['text3']}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="12" font-weight="300" letter-spacing="0.5">Building systems, web applications, developer tools</text>
  <text x="82" y="292" fill="{p['text3']}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="12" font-weight="300" letter-spacing="0.5">and intelligent software for a better tomorrow.</text>
</svg>'''
    return svg

# ─── BUTTON SVGs ────────────────────────────────────────────────────
def generate_button(label, mode="dark"):
    p = DARK if mode == "dark" else LIGHT
    W = 120 if label == "Portfolio" else 110
    H = 34
    icon_map = {
        "GitHub": f'<path d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0012 2z" fill="{p["text1"]}" transform="translate(8,5) scale(0.85)"/>',
        "LinkedIn": f'<path d="M19 3H5a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2V5a2 2 0 00-2-2zM9 17H6.5v-7H9v7zM7.7 8.7c-.8 0-1.3-.5-1.3-1.2s.5-1.2 1.4-1.2 1.3.5 1.3 1.2-.5 1.2-1.4 1.2zM18 17h-2.5v-3.8c0-1-.7-1.2-1-1.2s-1.2.1-1.2 1.2V17h-2.5v-7h2.5v1c.3-.6 1.1-1 2.2-1 1.1 0 2.5.8 2.5 3.5V17z" fill="{p["text1"]}" transform="translate(8,5) scale(0.85)"/>',
        "Portfolio": f'<circle cx="20" cy="17" r="7" fill="none" stroke="{p["text1"]}" stroke-width="1.5"/><path d="M16 13l3 3 5-5" fill="none" stroke="{p["text1"]}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
    }
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <rect width="{W}" height="{H}" rx="8" fill="none" stroke="{p['teal1']}" stroke-width="1" opacity="0.5"/>
  {icon_map.get(label, "")}
  <text x="{38 if label != 'Portfolio' else 38}" y="22" fill="{p['text1']}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="12" font-weight="500" letter-spacing="1">{label}</text>
</svg>'''
    return svg

# ─── ABOUT SVG ──────────────────────────────────────────────────────
def generate_about(mode="dark"):
    p = DARK if mode == "dark" else LIGHT
    W, H = 1100, 300

    # Radial diagram behind "About" heading
    radial = []
    for i in range(8):
        angle = i * math.pi / 4
        x2 = 80 + 25 * math.cos(angle)
        y2 = 42 + 25 * math.sin(angle)
        radial.append(f'  <line x1="80" y1="42" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{p["teal2"]}" stroke-width="0.5" opacity="0.15"/>')
    radial.append(f'  <circle cx="80" cy="42" r="25" fill="none" stroke="{p["teal2"]}" stroke-width="0.5" opacity="0.1"/>')
    radial.append(f'  <circle cx="80" cy="42" r="15" fill="none" stroke="{p["teal2"]}" stroke-width="0.4" opacity="0.08"/>')

    # Approach cards
    approaches = [
        ("Systems", "C / C++"),
        ("Intelligence", "Python / AI"),
        ("Web", "TypeScript / React"),
        ("Infrastructure", "Docker / Linux"),
        ("Exploration", "Math / New Tech"),
    ]
    cards = []
    card_w = 180
    card_h = 52
    total_w = len(approaches) * card_w + (len(approaches) - 1) * 12
    start_x = (W - total_w) / 2
    card_y = 210

    for i, (label, tech) in enumerate(approaches):
        x = start_x + i * (card_w + 12)
        # Card background
        cards.append(f'  <rect x="{x:.0f}" y="{card_y}" width="{card_w}" height="{card_h}" rx="6" fill="none" stroke="{p["teal1"]}" stroke-width="0.8" opacity="0.3"/>')
        # Small spiral ornament
        mini_spiral = spiral_path(x + 16, card_y + 26, 2, 8, 1.0, start_angle=i * 1.3)
        cards.append(f'  <path d="{mini_spiral}" fill="none" stroke="{p["teal2"]}" stroke-width="0.5" opacity="0.2"/>')
        # Label
        cards.append(f'  <text x="{x + 32:.0f}" y="{card_y + 22}" fill="{p["gold1"]}" font-family="\'Segoe UI\',sans-serif" font-size="11" font-weight="600">{label}</text>')
        # Arrow
        cards.append(f'  <text x="{x + 32:.0f}" y="{card_y + 40}" fill="{p["text3"]}" font-family="\'JetBrains Mono\',monospace" font-size="9.5">→ {tech}</text>')

    # Connecting curves between cards
    connectors = []
    for i in range(len(approaches) - 1):
        x1 = start_x + i * (card_w + 12) + card_w
        x2 = start_x + (i + 1) * (card_w + 12)
        d = flowing_curve(x1, card_y + 26, x2, card_y + 26, bend=-8)
        connectors.append(f'  <path d="{d}" fill="none" stroke="{p["teal2"]}" stroke-width="0.6" opacity="0.15"/>')

    # Background spirals
    bg_spirals = []
    for cx, cy, r1, r2, t in [(950, 80, 5, 50, 1.5), (150, 250, 3, 35, 1.2), (1050, 250, 4, 40, 1.3)]:
        d = spiral_path(cx, cy, r1, r2, t, start_angle=cx/100)
        bg_spirals.append(f'  <path d="{d}" fill="none" stroke="{p["teal2"]}" stroke-width="0.6" opacity="0.07"/>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    <linearGradient id="abg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{p['bg2']}"/>
      <stop offset="1" stop-color="{p['bg1']}"/>
    </linearGradient>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#abg)"/>

  <!-- Background spirals -->
{chr(10).join(bg_spirals)}

  <!-- Radial diagram -->
{chr(10).join(radial)}

  <!-- Section title -->
  <text x="115" y="50" fill="{p['gold1']}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="20" font-weight="600" letter-spacing="3">About</text>
  <line x1="115" y1="60" x2="250" y2="60" stroke="{p['gold1']}" stroke-width="0.5" opacity="0.3"/>

  <!-- Bio text -->
  <text x="115" y="95" fill="{p['text2']}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="13" font-weight="400">I'm Solayman El Mouden, a software engineer focused on systems,</text>
  <text x="115" y="115" fill="{p['text2']}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="13" font-weight="400">web technologies, artificial intelligence and mathematics.</text>
  <text x="115" y="148" fill="{p['text3']}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="12" font-weight="300">I enjoy understanding how things work underneath the abstraction</text>
  <text x="115" y="168" fill="{p['text3']}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="12" font-weight="300">and turning that knowledge into useful software.</text>

  <!-- My Approach heading -->
  <text x="{(W/2):.0f}" y="200" fill="{p['accent']}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="14" font-weight="500" letter-spacing="2" text-anchor="middle">My Approach</text>

  <!-- Approach cards -->
{chr(10).join(cards)}

  <!-- Connectors -->
{chr(10).join(connectors)}
</svg>'''
    return svg

# ─── SKILLS SVG ─────────────────────────────────────────────────────
def generate_skills(mode="dark"):
    p = DARK if mode == "dark" else LIGHT
    W, H = 1100, 270

    technologies = [
        ["C / C++", "Python", "JavaScript", "TypeScript"],
        ["React", "Next.js", "Django", "FastAPI"],
        ["PostgreSQL", "Docker", "Linux", "Git"],
    ]

    card_w, card_h = 130, 52
    gap_x, gap_y = 16, 14
    total_w = 4 * card_w + 3 * gap_x
    start_x = (W - total_w) / 2
    start_y = 75

    cards = []
    all_positions = []
    for row_i, row in enumerate(technologies):
        for col_i, tech in enumerate(row):
            x = start_x + col_i * (card_w + gap_x)
            y = start_y + row_i * (card_h + gap_y)
            all_positions.append((x + card_w/2, y + card_h/2))
            cards.append(f'  <rect x="{x:.0f}" y="{y:.0f}" width="{card_w}" height="{card_h}" rx="6" fill="{p["card_bg1"]}" stroke="{p["teal1"]}" stroke-width="0.7" opacity="0.85"/>')
            # Golden dot ornament
            cards.append(f'  <circle cx="{x + 14:.0f}" cy="{y + card_h/2:.0f}" r="2" fill="{p["gold1"]}" opacity="0.5"/>')
            cards.append(f'  <text x="{x + 24:.0f}" y="{y + card_h/2 + 4:.0f}" fill="{p["text2"]}" font-family="\'JetBrains Mono\',\'SF Mono\',monospace" font-size="11.5" font-weight="500">{tech}</text>')

    # Connecting flow lines between cards
    flow_lines = []
    for i in range(len(all_positions) - 1):
        if (i + 1) % 4 != 0:  # don't connect across rows
            x1, y1 = all_positions[i]
            x2, y2 = all_positions[i + 1]
            flow_lines.append(f'  <line x1="{x1 + card_w/2 - 5:.0f}" y1="{y1:.0f}" x2="{x2 - card_w/2 + 5:.0f}" y2="{y2:.0f}" stroke="{p["teal2"]}" stroke-width="0.4" opacity="0.1"/>')

    # Background spirals
    bg_spirals = []
    for cx, cy, r in [(100, 130, 40), (1000, 200, 35), (550, 30, 25)]:
        d = spiral_path(cx, cy, 3, r, 1.3, start_angle=cx/80)
        bg_spirals.append(f'  <path d="{d}" fill="none" stroke="{p["teal2"]}" stroke-width="0.5" opacity="0.06"/>')

    # Title spiral ornament
    title_spiral = spiral_path(100, 35, 3, 15, 1.0, start_angle=0)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    <linearGradient id="sbg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{p['bg1']}"/>
      <stop offset="1" stop-color="{p['bg2']}"/>
    </linearGradient>
    {grid_pattern("sgrid", 45, p["teal1"], 0.02 if mode == "dark" else 0.035)}
  </defs>
  <rect width="{W}" height="{H}" fill="url(#sbg)"/>
  <rect width="{W}" height="{H}" fill="url(#sgrid)"/>

  <!-- Background spirals -->
{chr(10).join(bg_spirals)}

  <!-- Title -->
  <path d="{title_spiral}" fill="none" stroke="{p['teal2']}" stroke-width="0.6" opacity="0.2"/>
  <text x="125" y="42" fill="{p['gold1']}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="18" font-weight="600" letter-spacing="2">Technologies &amp; Skills</text>
  <line x1="125" y1="52" x2="400" y2="52" stroke="{p['gold1']}" stroke-width="0.4" opacity="0.25"/>

  <!-- Tech cards -->
{chr(10).join(cards)}

  <!-- Flow lines -->
{chr(10).join(flow_lines)}
</svg>'''
    return svg

# ─── PROJECTS TITLE SVG ────────────────────────────────────────────
def generate_projects_title(mode="dark"):
    p = DARK if mode == "dark" else LIGHT
    W, H = 1100, 60

    spiral_d = spiral_path(35, 30, 3, 18, 1.2, start_angle=0.5)
    wave_d = wave_path(70, 45, W - 70, 45, amplitude=4, waves=8)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <rect width="{W}" height="{H}" fill="{p['bg1']}"/>
  <path d="{spiral_d}" fill="none" stroke="{p['teal2']}" stroke-width="0.7" opacity="0.2"/>
  <text x="60" y="35" fill="{p['gold1']}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="18" font-weight="600" letter-spacing="2">Selected Projects</text>
  <path d="{wave_d}" fill="none" stroke="{p['gold1']}" stroke-width="0.5" opacity="0.2"/>
  <line x1="0" y1="58" x2="{W}" y2="58" stroke="{p['teal1']}" stroke-width="0.3" opacity="0.1"/>
</svg>'''
    return svg

# ─── PROJECT CARD SVG ───────────────────────────────────────────────
def generate_project_card(num, name, desc, tags, pattern_type, mode="dark"):
    p = DARK if mode == "dark" else LIGHT
    W, H = 320, 210

    # Generate unique pattern based on type
    pattern_paths = []
    if pattern_type == "orbital":
        # LazyEquation: orbital ellipses
        for i in range(4):
            cx, cy = W/2, 42
            rx = 30 + i * 20
            ry = 12 + i * 8
            angle = i * 25
            pattern_paths.append(f'  <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{p["teal2"]}" stroke-width="0.7" opacity="{0.2 - i*0.04:.2f}" transform="rotate({angle} {cx} {cy})"/>')
        # Center dot
        pattern_paths.append(f'  <circle cx="{W/2}" cy="42" r="3" fill="{p["gold1"]}" opacity="0.4"/>')
        # Small orbiting dots
        for angle in [0, 90, 180, 270]:
            x = W/2 + 40 * math.cos(math.radians(angle))
            y = 42 + 15 * math.sin(math.radians(angle))
            pattern_paths.append(f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="1.5" fill="{p["teal3"]}" opacity="0.3"/>')

    elif pattern_type == "network":
        # LeetResume: branching tree/network
        nodes = [(W/2, 20), (W/2-60, 45), (W/2+60, 45), (W/2-90, 70), (W/2-30, 70), (W/2+30, 70), (W/2+90, 70)]
        for i, (x, y) in enumerate(nodes):
            pattern_paths.append(f'  <circle cx="{x}" cy="{y}" r="3" fill="{p["teal2"]}" opacity="0.25"/>')
        edges = [(0,1),(0,2),(1,3),(1,4),(2,5),(2,6)]
        for a, b in edges:
            d = flowing_curve(nodes[a][0], nodes[a][1], nodes[b][0], nodes[b][1], bend=-8)
            pattern_paths.append(f'  <path d="{d}" fill="none" stroke="{p["teal2"]}" stroke-width="0.8" opacity="0.2"/>')

    elif pattern_type == "pages":
        # Libora: page rectangles with flowing curves
        for i in range(3):
            x = W/2 - 50 + i * 30
            y = 15 + i * 5
            pattern_paths.append(f'  <rect x="{x}" y="{y}" width="40" height="55" rx="3" fill="none" stroke="{p["teal2"]}" stroke-width="0.7" opacity="{0.2 - i*0.05:.2f}"/>')
        # Flowing curve through pages
        d = wave_path(W/2 - 60, 40, W/2 + 70, 40, amplitude=15, waves=2)
        pattern_paths.append(f'  <path d="{d}" fill="none" stroke="{p["gold1"]}" stroke-width="0.6" opacity="0.2"/>')

    elif pattern_type == "routing":
        # Webserv: network routing nodes
        nodes = [(50, 40), (W/2-40, 25), (W/2+40, 25), (W-50, 40), (W/2, 55), (80, 65), (W-80, 65)]
        for x, y in nodes:
            pattern_paths.append(f'  <circle cx="{x}" cy="{y}" r="3" fill="{p["teal2"]}" opacity="0.2"/>')
            pattern_paths.append(f'  <circle cx="{x}" cy="{y}" r="6" fill="none" stroke="{p["teal2"]}" stroke-width="0.4" opacity="0.12"/>')
        connections = [(0,1),(1,2),(2,3),(1,4),(2,4),(4,5),(4,6)]
        for a, b in connections:
            pattern_paths.append(f'  <line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" stroke="{p["teal2"]}" stroke-width="0.6" opacity="0.15"/>')

    elif pattern_type == "radial":
        # solaJobs: radial search structure
        cx, cy = W/2, 42
        for r in [15, 30, 45]:
            pattern_paths.append(f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{p["teal2"]}" stroke-width="0.5" opacity="{0.18 - r*0.003:.2f}"/>')
        for i in range(8):
            angle = i * math.pi / 4
            x2 = cx + 50 * math.cos(angle)
            y2 = cy + 50 * math.sin(angle)
            pattern_paths.append(f'  <line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{p["teal2"]}" stroke-width="0.4" opacity="0.1"/>')
        pattern_paths.append(f'  <circle cx="{cx}" cy="{cy}" r="3" fill="{p["gold1"]}" opacity="0.35"/>')

    # Tags
    tag_text = " · ".join(tags)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    <linearGradient id="cbg{num}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{p['card_bg1']}"/>
      <stop offset="0.7" stop-color="{p['card_bg2']}"/>
      <stop offset="1" stop-color="{p['bg2']}"/>
    </linearGradient>
    <clipPath id="cclip{num}"><rect x="1" y="1" width="{W-2}" height="80" rx="10"/></clipPath>
  </defs>

  <!-- Card background -->
  <rect width="{W}" height="{H}" rx="10" fill="url(#cbg{num})" stroke="{p['teal1']}" stroke-width="0.8" opacity="0.9"/>

  <!-- Pattern area (clipped) -->
  <g clip-path="url(#cclip{num})">
{chr(10).join(pattern_paths)}
  </g>

  <!-- Divider -->
  <line x1="20" y1="85" x2="{W-20}" y2="85" stroke="{p['teal1']}" stroke-width="0.4" opacity="0.2"/>

  <!-- Project number -->
  <text x="20" y="108" fill="{p['teal2']}" font-family="'JetBrains Mono',monospace" font-size="9" font-weight="400" opacity="0.5">PROJECT {num:02d}</text>

  <!-- Project name -->
  <text x="20" y="130" fill="{p['text1']}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="15" font-weight="700">{name}</text>

  <!-- Description -->
  <text x="20" y="152" fill="{p['text3']}" font-family="'Segoe UI',sans-serif" font-size="10" font-weight="300">{desc[:50]}</text>
  <text x="20" y="166" fill="{p['text3']}" font-family="'Segoe UI',sans-serif" font-size="10" font-weight="300">{desc[50:] if len(desc) > 50 else ''}</text>

  <!-- Tags -->
  <text x="20" y="{H - 16}" fill="{p['gold1']}" font-family="'JetBrains Mono',monospace" font-size="9" font-weight="500" opacity="0.7">{tag_text}</text>
</svg>'''
    return svg

# ─── FOOTER SVG ─────────────────────────────────────────────────────
def generate_footer(mode="dark"):
    p = DARK if mode == "dark" else LIGHT
    W, H = 1100, 160

    # Fading spiral patterns
    fading_spirals = []
    positions = [
        (150, 30, 5, 60, 1.8, 0, 0.2),
        (400, 40, 3, 45, 1.5, 1.2, 0.12),
        (650, 25, 4, 55, 1.6, 2.5, 0.15),
        (900, 35, 6, 50, 1.4, 0.8, 0.1),
        (250, 80, 3, 30, 1.0, 3.2, 0.06),
        (750, 90, 4, 35, 1.2, 1.8, 0.05),
        (1050, 50, 3, 40, 1.3, 4.0, 0.08),
        (50, 60, 5, 35, 1.1, 2.2, 0.07),
    ]
    for cx, cy, r1, r2, t, sa, op in positions:
        d = spiral_path(cx, cy, r1, r2, t, start_angle=sa)
        fading_spirals.append(f'  <path d="{d}" fill="none" stroke="{p["teal2"]}" stroke-width="0.6" opacity="{op}"/>')

    # Horizontal fading wave
    wave_d = wave_path(0, 130, W, 130, amplitude=5, waves=12)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    <linearGradient id="fbg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{p['bg2']}"/>
      <stop offset="1" stop-color="{p['bg1']}"/>
    </linearGradient>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#fbg)"/>

  <!-- Fading spirals -->
{chr(10).join(fading_spirals)}

  <!-- Fading wave -->
  <path d="{wave_d}" fill="none" stroke="{p['gold1']}" stroke-width="0.4" opacity="0.1"/>

  <!-- Footer text -->
  <text x="{W/2:.0f}" y="50" fill="{p['gold1']}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="18" font-weight="600" letter-spacing="4" text-anchor="middle">Build  ·  Explore  ·  Understand</text>
  <text x="{W/2:.0f}" y="78" fill="{p['teal2']}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="12" font-weight="400" letter-spacing="2" text-anchor="middle">Software Engineering  ·  Systems  ·  AI  ·  Mathematics</text>
  <text x="{W/2:.0f}" y="105" fill="{p['accent']}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="11" font-weight="300" letter-spacing="1" text-anchor="middle">solaymantech.me  ·  LinkedIn</text>

  <!-- Bottom fade line -->
  <line x1="300" y1="120" x2="{W-300}" y2="120" stroke="{p['gold1']}" stroke-width="0.3" opacity="0.15"/>
</svg>'''
    return svg


# ─── GENERATE ALL ASSETS ───────────────────────────────────────────
def main():
    projects = [
        (1, "LazyEquation", "Interactive mathematics and physics visualization platform.", ["React", "TS", "Fastify", "PostgreSQL"], "orbital"),
        (2, "LeetResume", "AI-powered resume builder and optimizer.", ["Next.js", "Prisma", "PostgreSQL"], "network"),
        (3, "Libora", "Flutter PDF reader with a modern reading experience.", ["Flutter", "Dart", "Riverpod"], "pages"),
        (4, "Webserv", "C++98 HTTP server built from scratch.", ["C++98", "Networking"], "routing"),
        (5, "solaJobs v2", "Job platform project.", ["Web Platform"], "radial"),
    ]

    file_map = {
        "card-solajobs-v2": "solajobs-v2",
    }

    assets = []

    # Header
    for mode in ["dark", "light"]:
        fname = f"header-{mode}.svg"
        with open(os.path.join(ASSETS_DIR, fname), "w") as f:
            f.write(generate_header(mode))
        assets.append(fname)

    # Buttons
    for label, slug in [("GitHub", "github"), ("LinkedIn", "linkedin"), ("Portfolio", "portfolio")]:
        for mode in ["dark", "light"]:
            fname = f"btn-{slug}-{mode}.svg"
            with open(os.path.join(ASSETS_DIR, fname), "w") as f:
                f.write(generate_button(label, mode))
            assets.append(fname)

    # About
    for mode in ["dark", "light"]:
        fname = f"about-{mode}.svg"
        with open(os.path.join(ASSETS_DIR, fname), "w") as f:
            f.write(generate_about(mode))
        assets.append(fname)

    # Skills
    for mode in ["dark", "light"]:
        fname = f"skills-{mode}.svg"
        with open(os.path.join(ASSETS_DIR, fname), "w") as f:
            f.write(generate_skills(mode))
        assets.append(fname)

    # Projects title
    for mode in ["dark", "light"]:
        fname = f"projects-title-{mode}.svg"
        with open(os.path.join(ASSETS_DIR, fname), "w") as f:
            f.write(generate_projects_title(mode))
        assets.append(fname)

    # Project cards
    for num, name, desc, tags, pattern in projects:
        slug = name.lower().replace(" ", "-").replace("solajobs-v2", "solajobs-v2")
        # Handle special case for solaJobs v2
        if name == "solaJobs v2":
            slug = "solajobs-v2"
        for mode in ["dark", "light"]:
            fname = f"card-{slug}-{mode}.svg"
            with open(os.path.join(ASSETS_DIR, fname), "w") as f:
                f.write(generate_project_card(num, name, desc, tags, pattern, mode))
            assets.append(fname)

    # Footer
    for mode in ["dark", "light"]:
        fname = f"footer-{mode}.svg"
        with open(os.path.join(ASSETS_DIR, fname), "w") as f:
            f.write(generate_footer(mode))
        assets.append(fname)

    print(f"Generated {len(assets)} SVG assets:")
    for a in sorted(assets):
        path = os.path.join(ASSETS_DIR, a)
        size = os.path.getsize(path)
        print(f"  {a:45s} {size:>8,d} bytes")

if __name__ == "__main__":
    main()
