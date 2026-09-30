from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.dml import MSO_LINE_DASH_STYLE

# ============================================================
# SPARKY — 12-SLIDE COMPETITION PRESENTATION
# Built according to the supplied competition slide framework
# ============================================================

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# ---------- Theme ----------
BG = RGBColor(6, 10, 19)
PANEL = RGBColor(13, 20, 34)
PANEL2 = RGBColor(18, 28, 46)
WHITE = RGBColor(241, 246, 250)
MUTED = RGBColor(157, 173, 193)

CYAN = RGBColor(0, 220, 255)
BLUE = RGBColor(70, 125, 255)
GREEN = RGBColor(55, 225, 145)
ORANGE = RGBColor(255, 171, 65)
PURPLE = RGBColor(175, 105, 255)
RED = RGBColor(255, 80, 100)

FONT = "Aptos"
MONO = "Consolas"

def set_bg(slide):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = BG

def add_text(slide, text, x, y, w, h, size=18, color=WHITE,
             bold=False, font=FONT, align=PP_ALIGN.LEFT,
             valign=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(
        Inches(x), Inches(y), Inches(w), Inches(h)
    )
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.vertical_anchor = valign
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    return box

def panel(slide, x, y, w, h, fill=PANEL, line=None):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(x), Inches(y), Inches(w), Inches(h)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    if line:
        shape.line.color.rgb = line
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    return shape

def title(slide, text, subtitle=None, n=None):
    add_text(slide, text, 0.65, 0.35, 11.8, 0.55,
             size=28, bold=True)
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.67), Inches(1.00), Inches(1.15), Inches(0.045)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = CYAN
    line.line.fill.background()

    if subtitle:
        add_text(slide, subtitle, 0.68, 1.10, 11.7, 0.42,
                 size=11.5, color=MUTED)

    if n is not None:
        add_text(slide, f"{n:02d}", 12.15, 0.37, 0.5, 0.35,
                 size=11, color=CYAN, bold=True, align=PP_ALIGN.RIGHT)

def footer(slide):
    add_text(slide, "SPARKY  •  AI-ASSISTED SMART ROBOTIC SYSTEM",
             0.65, 7.08, 8, 0.2, size=7.5, color=MUTED)

def pill(slide, text, x, y, w, color=CYAN):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(x), Inches(y), Inches(w), Inches(0.38)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    add_text(slide, text, x, y+0.02, w, 0.28,
             size=8.5, color=BG, bold=True,
             align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

def node(slide, text, x, y, w, h, color=CYAN, size=12):
    panel(slide, x, y, w, h, PANEL2, color)
    add_text(slide, text, x+0.08, y+0.05, w-0.16, h-0.1,
             size=size, bold=True, align=PP_ALIGN.CENTER,
             valign=MSO_ANCHOR.MIDDLE)

def arrow(slide, x1, y1, x2, y2, color=CYAN, width=2):
    line = slide.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT,
        Inches(x1), Inches(y1), Inches(x2), Inches(y2)
    )
    line.line.color.rgb = color
    line.line.width = Pt(width)
    return line

def bullets(slide, items, x, y, w, h, size=14, color=WHITE):
    box = slide.shapes.add_textbox(
        Inches(x), Inches(y), Inches(w), Inches(h)
    )
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = "• " + item
        p.font.name = FONT
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.space_after = Pt(7)
    return box

def codebox(slide, text, x, y, w, h, size=12):
    panel(slide, x, y, w, h, RGBColor(4, 8, 14), CYAN)
    add_text(slide, text, x+0.18, y+0.13, w-0.36, h-0.26,
             size=size, color=GREEN, font=MONO)

# ============================================================
# 1 — COVER
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s)

add_text(s, "SPARKY", 0.75, 1.25, 11.8, 0.9,
         size=54, color=CYAN, bold=True, align=PP_ALIGN.CENTER)
add_text(s, "AI-ASSISTED SMART ROBOTIC SYSTEM",
         0.8, 2.22, 11.7, 0.5,
         size=22, bold=True, align=PP_ALIGN.CENTER)
add_text(s, "SEE  →  SENSE  →  UNDERSTAND  →  DECIDE  →  ACT",
         0.8, 3.02, 11.7, 0.45,
         size=16, color=GREEN, bold=True, align=PP_ALIGN.CENTER)

panel(s, 2.05, 3.85, 9.25, 1.25, PANEL)
add_text(s,
         "A computer-driven robotic system combining AI reasoning, "
         "computer vision, sensor fusion, wireless communication and physical control.",
         2.4, 4.13, 8.55, 0.7, size=16, color=WHITE,
         align=PP_ALIGN.CENTER)

pill(s, "AI", 3.35, 5.55, 0.7, PURPLE)
pill(s, "VISION", 4.25, 5.55, 1.05, CYAN)
pill(s, "SENSORS", 5.55, 5.55, 1.25, GREEN)
pill(s, "ROBOTICS", 7.05, 5.55, 1.25, ORANGE)

add_text(s, "Team Sparky  •  Competition Prototype",
         3.3, 6.35, 6.7, 0.35, size=11, color=MUTED,
         align=PP_ALIGN.CENTER)

# ============================================================
# 2 — PROBLEM & OPPORTUNITY
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s)
title(s, "Problem & Opportunity",
      "Why a robot needs more than isolated sensors and predefined actions.", 2)

panel(s, 0.7, 1.65, 3.75, 4.85, PANEL, RED)
add_text(s, "THE PROBLEM", 1.0, 1.98, 3.1, 0.4,
         size=18, color=RED, bold=True)
bullets(s, [
    "Conventional robots often depend on fixed commands.",
    "Sensors provide data, but data alone is not understanding.",
    "Vision, environmental sensing and control are often separate systems.",
    "Adding new behavior can require rewriting large parts of the program."
], 1.0, 2.65, 3.1, 2.8, 14)

panel(s, 4.8, 1.65, 3.75, 4.85, PANEL, ORANGE)
add_text(s, "THE OPPORTUNITY", 5.1, 1.98, 3.1, 0.4,
         size=18, color=ORANGE, bold=True)
bullets(s, [
    "Use modern AI to interpret human instructions.",
    "Combine visual and physical sensor information.",
    "Separate intelligence from low-level hardware control.",
    "Create a modular platform that can keep gaining capabilities."
], 5.1, 2.65, 3.1, 2.8, 14)

panel(s, 8.9, 1.65, 3.75, 4.85, PANEL, GREEN)
add_text(s, "SPARKY'S RESPONSE", 9.2, 1.98, 3.1, 0.4,
         size=18, color=GREEN, bold=True)
add_text(s,
         "Perceive\n+\nUnderstand\n+\nDecide\n+\nAct",
         9.2, 2.7, 3.1, 2.6, size=24, color=WHITE,
         bold=True, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.MIDDLE)

footer(s)

# ============================================================
# 3 — EXISTING SOLUTIONS & GAP
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s)
title(s, "Existing Solutions & Gap Analysis",
      "Sparky combines capabilities that are usually treated as separate systems.", 3)

headers = ["Existing approach", "What it does", "Gap Sparky addresses"]

rows = [
    ("Basic IoT automation",
     "Sensor → fixed rule → actuator",
     "Limited context and natural-language interaction"),
    ("Camera robots",
     "Camera + object detection",
     "Visual information is not always connected to physical safety/control"),
    ("Voice / AI assistants",
     "Natural-language interaction",
     "Usually not connected to a mobile physical platform"),
    ("Traditional robots",
     "Motors + sensors + programmed behavior",
     "Harder to extend with AI-driven interpretation"),
]

x = [0.7, 3.25, 7.0]
w = [2.35, 3.35, 5.6]

for i, h in enumerate(headers):
    panel(s, x[i], 1.75, w[i], 0.7, PANEL2, CYAN)
    add_text(s, h, x[i]+0.1, 1.93, w[i]-0.2, 0.3,
             size=12, color=CYAN, bold=True,
             align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

y = 2.55
for a, b, c in rows:
    panel(s, x[0], y, w[0], 0.95, PANEL)
    panel(s, x[1], y, w[1], 0.95, PANEL)
    panel(s, x[2], y, w[2], 0.95, PANEL)
    add_text(s, a, x[0]+0.12, y+0.12, w[0]-0.24, 0.7,
             size=11.5, bold=True)
    add_text(s, b, x[1]+0.12, y+0.12, w[1]-0.24, 0.7,
             size=11.5, color=MUTED)
    add_text(s, c, x[2]+0.12, y+0.12, w[2]-0.24, 0.7,
             size=11.5, color=WHITE)
    y += 1.02

panel(s, 2.0, 6.6, 9.4, 0.35, PANEL2)
add_text(s, "THE GAP: connecting natural-language intelligence + perception + physical action",
         2.1, 6.66, 9.2, 0.22, size=10.5, color=GREEN,
         bold=True, align=PP_ALIGN.CENTER)
footer(s)

# ============================================================
# 4 — OUR SOLUTION
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s)
title(s, "Our Solution",
      "A layered architecture connecting the real world to an AI-driven computer brain.", 4)

# Left flow
node(s, "REAL WORLD", 0.7, 2.05, 1.55, 0.8, GREEN)
node(s, "CAMERA +\nSENSORS", 2.8, 2.05, 1.7, 0.8, CYAN)
node(s, "PC / AI\nBRAIN", 5.05, 2.05, 1.7, 0.8, PURPLE)
node(s, "DECISION /\nCOMMAND", 7.3, 2.05, 1.75, 0.8, ORANGE)
node(s, "CONTROLLER", 9.6, 2.05, 1.7, 0.8, BLUE)
node(s, "ACTION", 11.65, 2.05, 1.0, 0.8, RED)

arrow(s, 2.25, 2.45, 2.8, 2.45)
arrow(s, 4.5, 2.45, 5.05, 2.45)
arrow(s, 6.75, 2.45, 7.3, 2.45)
arrow(s, 9.05, 2.45, 9.6, 2.45)
arrow(s, 11.3, 2.45, 11.65, 2.45)

panel(s, 0.85, 3.55, 11.65, 2.25, PANEL)
add_text(s, "THE SPARKY LOOP", 1.15, 3.85, 2.4, 0.35,
         size=16, color=CYAN, bold=True)
add_text(s,
         "1. Observe the environment\n"
         "2. Convert raw inputs into useful information\n"
         "3. Interpret commands and context using the computer intelligence layer\n"
         "4. Select a structured action\n"
         "5. Apply safety constraints\n"
         "6. Send the action to physical hardware",
         1.15, 4.35, 10.5, 1.2, size=13.5, color=WHITE)

add_text(s,
         "The architecture is modular: the AI layer can evolve without replacing the entire hardware system.",
         1.25, 6.18, 10.8, 0.45, size=13, color=GREEN,
         bold=True, align=PP_ALIGN.CENTER)
footer(s)

# ============================================================
# 5 — TECHNOLOGY & INNOVATION
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s)
title(s, "Technology & Innovation",
      "The PC-side architecture is the intelligence layer of Sparky.", 5)

# PC architecture
panel(s, 0.6, 1.55, 8.25, 5.25, PANEL, CYAN)
pill(s, "COMPUTER / AI LAYER", 0.95, 1.78, 2.25, CYAN)

node(s, "Wi-Fi\nCamera", 0.95, 2.45, 1.3, 0.72, CYAN, 11)
node(s, "OpenCV", 2.55, 2.45, 1.3, 0.72, BLUE, 11)
node(s, "YOLO + Face\nRecognition", 4.15, 2.45, 1.65, 0.72, PURPLE, 10)
node(s, "Sensor\nInput", 6.15, 2.45, 1.3, 0.72, GREEN, 11)

arrow(s, 2.25, 2.81, 2.55, 2.81)
arrow(s, 3.85, 2.81, 4.15, 2.81)

node(s, "Qwen 27B-class\nAI", 1.2, 3.75, 1.65, 0.8, PURPLE, 12)
node(s, "Command\nClassifier", 3.55, 3.75, 1.65, 0.8, ORANGE, 12)
node(s, "JSON Command\nRegistry", 5.9, 3.75, 1.65, 0.8, CYAN, 11)

arrow(s, 2.85, 4.15, 3.55, 4.15)
arrow(s, 5.2, 4.15, 5.9, 4.15)

node(s, "Decision +\nSafety", 2.25, 5.2, 1.65, 0.8, RED, 12)
node(s, "Dispatcher /\nHardware API", 4.75, 5.2, 1.85, 0.8, GREEN, 11)

arrow(s, 4.35, 5.6, 4.75, 5.6)

# Innovation panel
panel(s, 9.15, 1.55, 3.55, 5.25, PANEL2, ORANGE)
add_text(s, "WHAT IS INNOVATIVE?", 9.48, 1.92, 2.9, 0.42,
         size=16, color=ORANGE, bold=True)
bullets(s, [
    "AI is separated from low-level hardware control.",
    "Commands become structured before execution.",
    "Vision and sensor information can feed the same decision layer.",
    "The architecture is modular and extensible.",
    "Safety can override unsafe movement commands."
], 9.48, 2.65, 2.85, 2.8, 12.5)

add_text(s, "Exact Qwen model identifier can be updated here before final submission.",
         9.48, 5.75, 2.8, 0.55, size=9.5, color=MUTED)

footer(s)

# ============================================================
# 6 — PROTOTYPE / MVP
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s)
title(s, "Prototype / MVP Demonstration",
      "Show what has actually been built and tested — not only what is planned.", 6)

implemented = [
    ("Wi-Fi camera streaming", CYAN),
    ("OpenCV camera pipeline", BLUE),
    ("YOLO vision integration", PURPLE),
    ("Face recognition pipeline", ORANGE),
    ("Qwen / LLM integration", GREEN),
    ("JSON-based command architecture", CYAN),
    ("Arduino home automation", ORANGE),
    ("PIR + DHT11 testing", GREEN),
    ("HC-SR04 integration/testing", BLUE),
]

for i, (item, color) in enumerate(implemented):
    col = i % 3
    row = i // 3
    x = 0.7 + col * 4.15
    y = 1.75 + row * 1.2
    panel(s, x, y, 3.7, 0.9, PANEL, color)
    add_text(s, "✓", x+0.18, y+0.2, 0.35, 0.35,
             size=18, color=color, bold=True)
    add_text(s, item, x+0.62, y+0.15, 2.85, 0.55,
             size=12.5, bold=True, valign=MSO_ANCHOR.MIDDLE)

panel(s, 1.1, 5.55, 11.1, 0.95, PANEL2, ORANGE)
add_text(s,
         "INTEGRATION PHASE",
         1.45, 5.75, 2.1, 0.3, size=13, color=ORANGE, bold=True)
add_text(s,
         "Combining the independent modules into one reliable closed-loop robot.",
         3.45, 5.72, 8.2, 0.35, size=13, color=WHITE)

add_text(s,
         "Recommended evidence on the final slide: camera-stream screenshot • YOLO output • command JSON • hardware prototype • sensor readings",
         1.05, 6.65, 11.2, 0.3, size=9.5, color=MUTED,
         align=PP_ALIGN.CENTER)
footer(s)

# ============================================================
# 7 — TARGET USERS & USE CASES
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s)
title(s, "Target Users & Use Cases",
      "A modular platform can serve different environments by changing its command and hardware modules.", 7)

cases = [
    ("SMART HOME", "Automation\nMonitoring\nSafety alerts", CYAN),
    ("EDUCATION", "AI + robotics\nLearning platform\nSTEM demonstrations", BLUE),
    ("SECURITY", "Visual awareness\nMotion detection\nEnvironmental sensing", RED),
    ("ASSISTIVE ROBOTICS", "Context-aware actions\nRemote interaction\nRoutine assistance", GREEN),
]

for i, (name, desc, color) in enumerate(cases):
    x = 0.75 + (i % 2) * 6.25
    y = 1.75 + (i // 2) * 2.35
    panel(s, x, y, 5.65, 1.9, PANEL, color)
    add_text(s, name, x+0.3, y+0.28, 4.9, 0.35,
             size=17, color=color, bold=True)
    add_text(s, desc, x+0.3, y+0.85, 4.9, 0.75,
             size=14, color=MUTED)

panel(s, 1.6, 6.15, 10.1, 0.55, PANEL2)
add_text(s,
         "Primary opportunity: configurable robotics for homes, schools and real-world automation scenarios.",
         1.8, 6.27, 9.7, 0.25, size=11.5, color=WHITE,
         bold=True, align=PP_ALIGN.CENTER)
footer(s)

# ============================================================
# 8 — IMPACT & OUTCOMES
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s)
title(s, "Impact & Outcomes",
      "Expected value comes from combining automation, perception and adaptable intelligence.", 8)

metrics = [
    ("AUTOMATION", "Reduces repetitive manual actions", CYAN),
    ("SAFETY", "Adds sensor-based protection to physical actions", RED),
    ("ADAPTABILITY", "Commands can evolve without redesigning the whole system", PURPLE),
    ("LEARNING", "Creates a practical AI + robotics platform", GREEN),
]

for i, (name, desc, color) in enumerate(metrics):
    x = 0.65 + i * 3.15
    panel(s, x, 1.9, 2.8, 2.55, PANEL, color)
    add_text(s, name, x+0.18, 2.25, 2.45, 0.35,
             size=15, color=color, bold=True, align=PP_ALIGN.CENTER)
    add_text(s, desc, x+0.25, 2.95, 2.3, 1.0,
             size=13, color=WHITE, align=PP_ALIGN.CENTER,
             valign=MSO_ANCHOR.MIDDLE)

panel(s, 1.15, 4.95, 11.0, 1.15, PANEL2)
add_text(s, "MEASURABLE OUTCOMES TO TRACK", 1.45, 5.2, 3.3, 0.3,
         size=13, color=ORANGE, bold=True)
add_text(s,
         "command success rate  •  response time  •  obstacle-stop reliability  •  detection accuracy  •  automation time saved",
         4.5, 5.15, 7.2, 0.45, size=12.5, color=WHITE)

add_text(s,
         "For the final competition version, replace expected outcomes with measured prototype data wherever possible.",
         1.3, 6.45, 10.7, 0.3, size=9.5, color=MUTED,
         align=PP_ALIGN.CENTER)
footer(s)

# ============================================================
# 9 — BUSINESS MODEL & IMPLEMENTATION
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s)
title(s, "Business Model & Implementation",
      "A modular architecture allows deployment at different hardware and cost levels.", 9)

panel(s, 0.7, 1.7, 3.75, 4.75, PANEL, CYAN)
add_text(s, "DEPLOYMENT MODEL", 1.0, 2.0, 3.0, 0.35,
         size=17, color=CYAN, bold=True)
bullets(s, [
    "Prototype kit for education",
    "Custom robotics deployments",
    "Home automation integration",
    "AI / vision module as an upgrade",
    "Software-first architecture reduces hardware lock-in"
], 1.0, 2.7, 3.05, 2.8, 13.5)

panel(s, 4.8, 1.7, 3.75, 4.75, PANEL, GREEN)
add_text(s, "IMPLEMENTATION", 5.1, 2.0, 3.0, 0.35,
         size=17, color=GREEN, bold=True)
bullets(s, [
    "Start with a PC + controller prototype",
    "Integrate modules independently",
    "Validate each sensor and actuator",
    "Add safety checks before autonomous movement",
    "Move toward a compact embedded version later"
], 5.1, 2.7, 3.05, 2.8, 13.5)

panel(s, 8.9, 1.7, 3.75, 4.75, PANEL, ORANGE)
add_text(s, "COST STRATEGY", 9.2, 2.0, 3.0, 0.35,
         size=17, color=ORANGE, bold=True)
bullets(s, [
    "Use affordable microcontrollers",
    "Reuse existing computing hardware",
    "Modular replacement of components",
    "Separate high-compute AI from low-cost hardware",
    "Scale hardware according to the use case"
], 9.2, 2.7, 3.05, 2.8, 13.5)

footer(s)

# ============================================================
# 10 — FEASIBILITY & SCALABILITY
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s)
title(s, "Feasibility & Scalability",
      "The system is designed to grow from a prototype into a larger robotics platform.", 10)

stages = [
    ("NOW", "PC + camera\nArduino / ESP\nSensors", CYAN),
    ("NEXT", "Integrated robot body\nMotor control\nFull safety loop", ORANGE),
    ("LATER", "Embedded AI\nEdge deployment\nMore autonomous behavior", PURPLE),
    ("SCALE", "Multiple robots\nDifferent environments\nReusable software modules", GREEN),
]

for i, (stage, desc, color) in enumerate(stages):
    x = 0.65 + i * 3.15
    node(s, stage, x, 2.0, 2.55, 0.75, color, 15)
    panel(s, x, 3.0, 2.55, 1.75, PANEL)
    add_text(s, desc, x+0.2, 3.35, 2.15, 1.0,
             size=13, color=WHITE, align=PP_ALIGN.CENTER,
             valign=MSO_ANCHOR.MIDDLE)
    if i < 3:
        arrow(s, x+2.55, 2.38, x+3.15, 2.38, MUTED)

panel(s, 1.1, 5.45, 11.1, 0.95, PANEL2, RED)
add_text(s, "KEY RISKS", 1.4, 5.72, 1.3, 0.3,
         size=12.5, color=RED, bold=True)
add_text(s,
         "latency • unreliable wireless links • false detections • hardware failures • model/API availability",
         2.85, 5.68, 8.9, 0.35, size=12, color=WHITE)

add_text(s,
         "Mitigation: modular software, local safety rules, hardware fallbacks and incremental testing.",
         1.35, 6.55, 10.6, 0.3, size=10.5, color=GREEN,
         bold=True, align=PP_ALIGN.CENTER)
footer(s)

# ============================================================
# 11 — COMPETITIVE ADVANTAGE
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s)
title(s, "Competitive Advantage",
      "The distinction is the architecture: AI reasoning connected to perception and physical control.", 11)

adv = [
    ("MODULAR", "AI, vision, sensors and hardware are separable modules.", CYAN),
    ("CONTEXT-AWARE", "Multiple inputs can contribute to one decision.", PURPLE),
    ("EXTENSIBLE", "Structured commands make new capabilities easier to add.", GREEN),
    ("SAFETY-FIRST", "Deterministic safety logic can override unsafe actions.", RED),
    ("COST-CONSCIOUS", "Commodity controllers and reusable computing hardware.", ORANGE),
    ("HARDWARE-INDEPENDENT", "The intelligence layer can work with different controllers.", BLUE),
]

for i, (name, desc, color) in enumerate(adv):
    x = 0.65 + (i % 3) * 4.2
    y = 1.75 + (i // 3) * 2.35
    panel(s, x, y, 3.75, 1.85, PANEL, color)
    add_text(s, name, x+0.25, y+0.28, 3.25, 0.35,
             size=15, color=color, bold=True, align=PP_ALIGN.CENTER)
    add_text(s, desc, x+0.28, y+0.85, 3.2, 0.7,
             size=12.5, color=WHITE, align=PP_ALIGN.CENTER)

panel(s, 1.55, 6.25, 10.25, 0.45, PANEL2)
add_text(s,
         "USP: a single modular system connecting language → perception → decision → physical action",
         1.7, 6.34, 9.95, 0.22, size=10.5, color=GREEN,
         bold=True, align=PP_ALIGN.CENTER)
footer(s)

# ============================================================
# 12 — TEAM & VISION
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s)

add_text(s, "TEAM & VISION", 0.75, 0.65, 11.8, 0.6,
         size=30, color=WHITE, bold=True, align=PP_ALIGN.CENTER)

add_text(s, "SPARKY", 0.75, 1.45, 11.8, 0.7,
         size=42, color=CYAN, bold=True, align=PP_ALIGN.CENTER)

panel(s, 1.2, 2.55, 10.9, 1.35, PANEL)
add_text(s,
         "Our vision is to turn Sparky from a competition prototype "
         "into a modular robotics platform where AI can understand, "
         "reason and safely interact with the physical world.",
         1.55, 2.85, 10.2, 0.8,
         size=17, color=WHITE, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.MIDDLE)

# Team placeholders
for i, label in enumerate(["TEAM MEMBER 1", "TEAM MEMBER 2", "TEAM MEMBER 3"]):
    x = 1.25 + i * 3.65
    panel(s, x, 4.35, 3.25, 1.0, PANEL2)
    add_text(s, label, x+0.2, 4.67, 2.85, 0.3,
             size=12.5, color=GREEN, bold=True,
             align=PP_ALIGN.CENTER)

add_text(s, "Mentor: ____________________",
         4.0, 5.75, 5.3, 0.3, size=11.5, color=MUTED,
         align=PP_ALIGN.CENTER)

add_text(s, "THANK YOU", 3.5, 6.25, 6.3, 0.5,
         size=24, color=CYAN, bold=True, align=PP_ALIGN.CENTER)

add_text(s, "Contact: ____________________",
         3.5, 6.78, 6.3, 0.25, size=9.5, color=MUTED,
         align=PP_ALIGN.CENTER)

# ============================================================
# SAVE
# ============================================================
ppt_path = "Sparky_Competition_12_Slide_Presentation.pptx"
prs.save(ppt_path)

# Also save the source script so the user can edit/re-run it.
# Reconstructing the exact source from the executed notebook is unnecessary;
# the PPT itself is the primary deliverable.
print(ppt_path)
