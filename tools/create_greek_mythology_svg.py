"""
Generate Greek Mythology SVG image
"""
from pathlib import Path

svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <!-- Background -->
  <rect width="200" height="200" fill="#1a237e"/>

  <!-- Greek key pattern border -->
  <rect x="5" y="5" width="190" height="190" fill="none" stroke="#ffd700" stroke-width="3"/>
  <rect x="10" y="10" width="180" height="180" fill="none" stroke="#ffd700" stroke-width="1.5"/>

  <!-- Greek column -->
  <g transform="translate(30, 40)">
    <!-- Column base -->
    <rect x="10" y="110" width="30" height="8" fill="#e0e0e0" stroke="#bdbdbd" stroke-width="1"/>
    <!-- Column shaft -->
    <rect x="13" y="30" width="24" height="80" fill="#f5f5f5" stroke="#bdbdbd" stroke-width="1"/>
    <!-- Column lines -->
    <line x1="17" y1="35" x2="17" y2="105" stroke="#bdbdbd" stroke-width="0.5"/>
    <line x1="21" y1="35" x2="21" y2="105" stroke="#bdbdbd" stroke-width="0.5"/>
    <line x1="25" y1="35" x2="25" y2="105" stroke="#bdbdbd" stroke-width="0.5"/>
    <line x1="29" y1="35" x2="29" y2="105" stroke="#bdbdbd" stroke-width="0.5"/>
    <line x1="33" y1="35" x2="33" y2="105" stroke="#bdbdbd" stroke-width="0.5"/>
    <!-- Column capital -->
    <rect x="8" y="22" width="34" height="8" fill="#e0e0e0" stroke="#bdbdbd" stroke-width="1"/>
  </g>

  <!-- Greek column (right) -->
  <g transform="translate(120, 40)">
    <!-- Column base -->
    <rect x="10" y="110" width="30" height="8" fill="#e0e0e0" stroke="#bdbdbd" stroke-width="1"/>
    <!-- Column shaft -->
    <rect x="13" y="30" width="24" height="80" fill="#f5f5f5" stroke="#bdbdbd" stroke-width="1"/>
    <!-- Column lines -->
    <line x1="17" y1="35" x2="17" y2="105" stroke="#bdbdbd" stroke-width="0.5"/>
    <line x1="21" y1="35" x2="21" y2="105" stroke="#bdbdbd" stroke-width="0.5"/>
    <line x1="25" y1="35" x2="25" y2="105" stroke="#bdbdbd" stroke-width="0.5"/>
    <line x1="29" y1="35" x2="29" y2="105" stroke="#bdbdbd" stroke-width="0.5"/>
    <line x1="33" y1="35" x2="33" y2="105" stroke="#bdbdbd" stroke-width="0.5"/>
    <!-- Column capital -->
    <rect x="8" y="22" width="34" height="8" fill="#e0e0e0" stroke="#bdbdbd" stroke-width="1"/>
  </g>

  <!-- Lightning bolt (Zeus symbol) -->
  <g transform="translate(85, 50)">
    <path d="M 15 0 L 5 20 L 12 20 L 2 40 L 18 18 L 11 18 Z" fill="#ffd700" stroke="#ffb300" stroke-width="1"/>
  </g>

  <!-- Laurel wreath -->
  <g transform="translate(100, 90)">
    <!-- Left branch -->
    <path d="M -30 0 Q -25 -10, -20 -5 Q -15 0, -10 -3 Q -5 -6, 0 0"
          fill="none" stroke="#4caf50" stroke-width="2" stroke-linecap="round"/>
    <ellipse cx="-28" cy="-2" rx="2" ry="3" fill="#4caf50"/>
    <ellipse cx="-23" cy="-7" rx="2" ry="3" fill="#4caf50" transform="rotate(-20 -23 -7)"/>
    <ellipse cx="-18" cy="-4" rx="2" ry="3" fill="#4caf50" transform="rotate(10 -18 -4)"/>
    <ellipse cx="-13" cy="-2" rx="2" ry="3" fill="#4caf50"/>
    <ellipse cx="-8" cy="-5" rx="2" ry="3" fill="#4caf50" transform="rotate(-15 -8 -5)"/>

    <!-- Right branch -->
    <path d="M 30 0 Q 25 -10, 20 -5 Q 15 0, 10 -3 Q 5 -6, 0 0"
          fill="none" stroke="#4caf50" stroke-width="2" stroke-linecap="round"/>
    <ellipse cx="28" cy="-2" rx="2" ry="3" fill="#4caf50"/>
    <ellipse cx="23" cy="-7" rx="2" ry="3" fill="#4caf50" transform="rotate(20 23 -7)"/>
    <ellipse cx="18" cy="-4" rx="2" ry="3" fill="#4caf50" transform="rotate(-10 18 -4)"/>
    <ellipse cx="13" cy="-2" rx="2" ry="3" fill="#4caf50"/>
    <ellipse cx="8" cy="-5" rx="2" ry="3" fill="#4caf50" transform="rotate(15 8 -5)"/>
  </g>

  <!-- Greek helmet (center bottom) -->
  <g transform="translate(100, 130)">
    <!-- Helmet dome -->
    <path d="M -15 20 Q -15 0, 0 -10 Q 15 0, 15 20" fill="#cd7f32" stroke="#8b4513" stroke-width="1.5"/>
    <!-- Crest -->
    <path d="M -3 -8 L 0 -15 L 3 -8" fill="#dc143c" stroke="#8b0000" stroke-width="1"/>
    <path d="M -2 -7 L 0 -12 L 2 -7" fill="#ff1744"/>
    <!-- Face opening -->
    <rect x="-8" y="5" width="16" height="12" fill="#424242" opacity="0.6"/>
    <!-- Cheek guards -->
    <path d="M -15 15 L -12 22 L -10 20 L -12 15 Z" fill="#cd7f32" stroke="#8b4513" stroke-width="1"/>
    <path d="M 15 15 L 12 22 L 10 20 L 12 15 Z" fill="#cd7f32" stroke="#8b4513" stroke-width="1"/>
  </g>

  <!-- Greek text "ΜΥΘΟΙ" (MYTHOI - Myths) -->
  <text x="100" y="175" font-family="serif" font-size="24" font-weight="bold"
        fill="#ffd700" text-anchor="middle" stroke="#ffb300" stroke-width="0.5">ΜΥΘΟΙ</text>

  <!-- Greek key pattern decoration -->
  <g transform="translate(20, 185)">
    <path d="M 0 0 L 5 0 L 5 5 L 10 5 L 10 0 L 15 0 L 15 5 L 20 5 L 20 0 L 25 0 L 25 5 L 30 5 L 30 0 L 35 0"
          fill="none" stroke="#ffd700" stroke-width="1.5"/>
  </g>

  <g transform="translate(145, 185)">
    <path d="M 0 0 L 5 0 L 5 5 L 10 5 L 10 0 L 15 0 L 15 5 L 20 5 L 20 0 L 25 0 L 25 5 L 30 5 L 30 0 L 35 0"
          fill="none" stroke="#ffd700" stroke-width="1.5"/>
  </g>
</svg>'''

# Save the SVG
output_path = Path("src/main/resources/META-INF/resources/images/greek-mythology.svg")
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(svg_content)

print(f"✓ Greek Mythology SVG created: {output_path}")
print(f"  Size: 200x200")
print(f"  Features: Columns, lightning bolt, laurel wreath, Greek helmet, Greek text")

