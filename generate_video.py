import os
import math
from PIL import Image, ImageDraw, ImageFont
import imageio.v3 as iio

# Output directory and paths
WORKSPACE_DIR = "/Users/sandeepkumarchoudhary/ demo"
ARTIFACT_DIR = "/Users/sandeepkumarchoudhary/.gemini/antigravity-ide/brain/c95b3504-b3d0-48b2-bca7-efb69538add8"
os.makedirs(WORKSPACE_DIR, exist_ok=True)
os.makedirs(ARTIFACT_DIR, exist_ok=True)

WIDTH, HEIGHT = 1200, 675  # 16:9 ratio crisp resolution
FPS = 15  # 15 fps gives great smoothness while keeping file size fast and lightweight

# Fonts
try:
    font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
    font_subtitle = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22)
    font_body = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
    font_bold = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 20)
    font_bold_lg = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 28)
    font_code = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 17)
    font_code_lg = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 22)
    font_badge = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 14)
except Exception as e:
    font_title = ImageFont.load_default()
    font_subtitle = ImageFont.load_default()
    font_body = ImageFont.load_default()
    font_bold = ImageFont.load_default()
    font_bold_lg = ImageFont.load_default()
    font_code = ImageFont.load_default()
    font_code_lg = ImageFont.load_default()
    font_badge = ImageFont.load_default()

# Colors (Modern Tech Dark Palette)
BG_COLOR = (11, 15, 25)
PANEL_BG = (19, 26, 42)
PANEL_BORDER = (38, 52, 78)
CYAN = (34, 211, 238)
PURPLE = (168, 85, 247)
GREEN = (52, 211, 153)
RED = (248, 113, 113)
YELLOW = (251, 191, 36)
TEXT_WHITE = (248, 250, 252)
TEXT_MUTED = (148, 163, 184)
TEXT_DIM = (100, 116, 139)
CODE_BG = (15, 23, 42)

def draw_rounded_rect(draw, bbox, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def draw_header(draw, title, subtitle, step_num, total_steps=5):
    # Top banner
    draw_rounded_rect(draw, (40, 25, WIDTH - 40, 95), 14, fill=PANEL_BG, outline=PANEL_BORDER, width=2)
    
    # Badge
    badge_w = 90
    draw_rounded_rect(draw, (55, 38, 55 + badge_w, 64), 6, fill=(30, 41, 59), outline=CYAN, width=1)
    draw.text((68, 43), f"STEP {step_num}/{total_steps}", font=font_badge, fill=CYAN)
    
    # Title & Subtitle
    draw.text((160, 36), title, font=font_bold, fill=TEXT_WHITE)
    draw.text((160, 64), subtitle, font=font_body, fill=TEXT_MUTED)
    
    # Live Indicator
    draw.ellipse((WIDTH - 150, 45, WIDTH - 140, 55), fill=GREEN)
    draw.text((WIDTH - 130, 42), "LIVE DEMO", font=font_badge, fill=GREEN)

def draw_footer_progress(draw, current_frame, total_frames, scene_name):
    # Bottom control bar
    draw_rounded_rect(draw, (40, HEIGHT - 55, WIDTH - 40, HEIGHT - 18), 10, fill=PANEL_BG, outline=PANEL_BORDER, width=1)
    
    # Progress track
    track_x1, track_x2 = 60, WIDTH - 260
    track_y = HEIGHT - 37
    draw.line((track_x1, track_y, track_x2, track_y), fill=(30, 41, 59), width=6)
    
    pct = current_frame / max(1, total_frames - 1)
    prog_x = track_x1 + (track_x2 - track_x1) * pct
    draw.line((track_x1, track_y, prog_x, track_y), fill=CYAN, width=6)
    draw.ellipse((prog_x - 5, track_y - 5, prog_x + 5, track_y + 5), fill=TEXT_WHITE)
    
    # Scene label & duration
    cur_sec = current_frame / FPS
    tot_sec = total_frames / FPS
    time_str = f"{int(cur_sec):02d}:{int((cur_sec % 1)*100):02d} / {int(tot_sec):02d}:00"
    draw.text((WIDTH - 240, HEIGHT - 45), time_str, font=font_badge, fill=TEXT_MUTED)
    draw.text((WIDTH - 140, HEIGHT - 45), f"• {scene_name}", font=font_badge, fill=CYAN)

def create_base_canvas():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    # Subtle grid dots
    for x in range(20, WIDTH, 40):
        for y in range(20, HEIGHT, 40):
            draw.point((x, y), fill=(20, 28, 45))
    return img, draw

frames = []

print("Generating Video Scenes...")

# ==========================================
# SCENE 1: What is a Database? & Architecture (Frames: 0 to 45 -> 3 seconds)
# ==========================================
scene_frames_1 = 45
for i in range(scene_frames_1):
    img, draw = create_base_canvas()
    draw_header(draw, "What is a Database?", "An organized, persistent storage system managed by a DBMS for ultra-fast access", 1)
    
    # Left Card: Core Definition & Concept
    draw_rounded_rect(draw, (40, 115, 460, HEIGHT - 75), 14, fill=PANEL_BG, outline=PANEL_BORDER, width=2)
    draw.text((65, 140), "Why Databases Instead of Files?", font=font_bold, fill=CYAN)
    
    points = [
        ("• Structured Storage:", "Organized in tables, columns & datatypes."),
        ("• ACID Reliability:", "Guarantees transactions & no data corruption."),
        ("• Fast Querying:", "B-Tree indexes find 1 row in millions instantly."),
        ("• Multi-User Concurrency:", "Thousands of users read/write simultaneously."),
        ("• Data Integrity:", "PRIMARY KEY prevents duplicate identities.")
    ]
    y_pos = 185
    for title, desc in points:
        draw.text((65, y_pos), title, font=font_bold, fill=TEXT_WHITE)
        draw.text((65, y_pos + 24), desc, font=font_body, fill=TEXT_MUTED)
        y_pos += 60

    # Right Card: How Data is Stored & Retrieved in Applications
    draw_rounded_rect(draw, (485, 115, WIDTH - 40, HEIGHT - 75), 14, fill=PANEL_BG, outline=PANEL_BORDER, width=2)
    draw.text((510, 140), "Application Architecture (Data Flow)", font=font_bold, fill=PURPLE)
    
    # 4 Architecture blocks
    t = i / scene_frames_1
    blocks = [
        ("1. Client App", "Browser / Mobile App", "Sends user request: 'Find Sales Staff'", CYAN),
        ("2. Backend API", "Node.js / Python / Go", "Executes SQL query over connection pool", YELLOW),
        ("3. DBMS Engine", "SQLite / PostgreSQL", "Parser, Query Optimizer & Buffer Cache", PURPLE),
        ("4. Disk Storage", "B-Tree Tables & WAL", "Persistent binary pages on disk drive", GREEN),
    ]
    
    bx = 510
    by = 185
    b_w = 640
    b_h = 75
    
    for idx, (b_title, b_tech, b_desc, b_col) in enumerate(blocks):
        active = idx <= int(t * 4.5)
        bg = (24, 34, 56) if active else (15, 21, 35)
        border = b_col if active else (30, 42, 65)
        draw_rounded_rect(draw, (bx, by, bx + b_w, by + b_h), 10, fill=bg, outline=border, width=2 if active else 1)
        
        # Icon / Badge
        draw_rounded_rect(draw, (bx + 15, by + 15, bx + 150, by + 40), 6, fill=(15, 23, 42), outline=border, width=1)
        draw.text((bx + 25, by + 19), b_title, font=font_badge, fill=b_col if active else TEXT_DIM)
        draw.text((bx + 165, by + 19), f"({b_tech})", font=font_badge, fill=TEXT_MUTED if active else TEXT_DIM)
        draw.text((bx + 25, by + 48), b_desc, font=font_body, fill=TEXT_WHITE if active else TEXT_DIM)
        
        if idx < len(blocks) - 1:
            arrow_y = by + b_h + 3
            draw.text((bx + 310, arrow_y), "▼", font=font_badge, fill=CYAN if active else TEXT_DIM)
        
        by += b_h + 16
        
    draw_footer_progress(draw, i, 220, "Architecture Overview")
    frames.append(img)

# ==========================================
# SCENE 2: CREATE TABLE Schema Blueprint (Frames: 45 to 85 -> 2.6 seconds)
# ==========================================
scene_frames_2 = 40
for i in range(scene_frames_2):
    img, draw = create_base_canvas()
    draw_header(draw, "Step 1: CREATE TABLE EMPLOYEE", "Defining the table schema, column definitions, and primary key constraint", 2)
    
    # Left Card: SQL Code Editor
    draw_rounded_rect(draw, (40, 115, 520, HEIGHT - 75), 14, fill=PANEL_BG, outline=PANEL_BORDER, width=2)
    
    # Code editor top bar
    draw_rounded_rect(draw, (40, 115, 520, 160), 14, fill=(15, 23, 42), outline=PANEL_BORDER, width=1)
    draw.ellipse((58, 133, 70, 145), fill=(239, 68, 68))
    draw.ellipse((76, 133, 88, 145), fill=(245, 158, 11))
    draw.ellipse((94, 133, 106, 145), fill=(16, 185, 129))
    draw.text((130, 130), "schema.sql — SQLite Engine", font=font_badge, fill=TEXT_MUTED)
    
    sql_lines = [
        ("CREATE TABLE", CYAN, " EMPLOYEE (", TEXT_WHITE),
        ("  empId ", TEXT_WHITE, "INTEGER PRIMARY KEY,", YELLOW),
        ("  name  ", TEXT_WHITE, "TEXT NOT NULL,", YELLOW),
        ("  dept  ", TEXT_WHITE, "TEXT NOT NULL", YELLOW),
        (");", TEXT_WHITE, "", TEXT_WHITE)
    ]
    
    code_y = 190
    for l_idx, (p1, c1, p2, c2) in enumerate(sql_lines):
        draw.text((65, code_y), str(l_idx + 1), font=font_code, fill=TEXT_DIM)
        draw.text((100, code_y), p1, font=font_code, fill=c1)
        w1 = draw.textlength(p1, font=font_code)
        draw.text((100 + w1, code_y), p2, font=font_code, fill=c2)
        code_y += 36
        
    # Explanation notes inside left panel
    draw_rounded_rect(draw, (65, 385, 495, HEIGHT - 95), 10, fill=(15, 23, 42), outline=(30, 41, 59), width=1)
    draw.text((80, 400), "Schema Blueprint Explanation:", font=font_bold, fill=CYAN)
    draw.text((80, 430), "• empId: Unique identifier (PRIMARY KEY)", font=font_body, fill=TEXT_WHITE)
    draw.text((80, 458), "• name: Employee's text name (Required)", font=font_body, fill=TEXT_WHITE)
    draw.text((80, 486), "• dept: Department name (Required)", font=font_body, fill=TEXT_WHITE)

    # Right Card: Visual Table Creation Animation
    draw_rounded_rect(draw, (545, 115, WIDTH - 40, HEIGHT - 75), 14, fill=PANEL_BG, outline=PANEL_BORDER, width=2)
    draw.text((575, 140), "Database Table Construction in RAM/Disk", font=font_bold, fill=GREEN)
    
    # Animated Blueprint Columns
    progress = min(1.0, (i + 5) / 25.0)
    col_w = int(180 * progress)
    
    cols = [
        ("empId", "INTEGER", "PRIMARY KEY [PK]", CYAN, 575),
        ("name", "TEXT", "NOT NULL", YELLOW, 775),
        ("dept", "TEXT", "NOT NULL", PURPLE, 975)
    ]
    
    for c_name, c_type, c_const, col_color, cx in cols:
        draw_rounded_rect(draw, (cx, 185, cx + col_w, 420), 10, fill=(24, 34, 56), outline=col_color, width=2)
        if progress > 0.6:
            draw_rounded_rect(draw, (cx + 10, 200, cx + col_w - 10, 240), 6, fill=(15, 23, 42), outline=col_color, width=1)
            draw.text((cx + 20, 210), c_name, font=font_bold, fill=TEXT_WHITE)
            draw.text((cx + 20, 260), f"Type: {c_type}", font=font_badge, fill=col_color)
            draw.text((cx + 20, 300), f"Constraint:", font=font_badge, fill=TEXT_MUTED)
            draw.text((cx + 20, 325), c_const, font=font_badge, fill=GREEN if "PK" in c_const else YELLOW)
            draw.text((cx + 20, 375), "EMPTY TABLE", font=font_badge, fill=TEXT_DIM)
            
    # Status alert
    if i > 20:
        draw_rounded_rect(draw, (575, 450, WIDTH - 65, 520), 10, fill=(16, 185, 129, 40), outline=GREEN, width=2)
        draw.text((600, 472), "✔ Table 'EMPLOYEE' created successfully with 0 rows", font=font_bold, fill=GREEN)
        
    draw_footer_progress(draw, 45 + i, 220, "CREATE TABLE Blueprint")
    frames.append(img)

# ==========================================
# SCENE 3: INSERT INTO (Storing Data) (Frames: 85 to 145 -> 4 seconds)
# ==========================================
scene_frames_3 = 60
for i in range(scene_frames_3):
    img, draw = create_base_canvas()
    draw_header(draw, "Step 2: Storing Data (INSERT INTO)", "Writing new employee records into table storage pages", 3)
    
    # Left: SQL Insert Statements
    draw_rounded_rect(draw, (40, 115, 500, HEIGHT - 75), 14, fill=PANEL_BG, outline=PANEL_BORDER, width=2)
    draw_rounded_rect(draw, (40, 115, 500, 160), 14, fill=(15, 23, 42), outline=PANEL_BORDER, width=1)
    draw.text((65, 130), "insert_statements.sql", font=font_badge, fill=TEXT_MUTED)
    
    inserts = [
        ("INSERT INTO EMPLOYEE VALUES", (1, "Clark", "Sales"), 15),
        ("INSERT INTO EMPLOYEE VALUES", (2, "Dave", "Accounting"), 30),
        ("INSERT INTO EMPLOYEE VALUES", (3, "Ava", "Sales"), 45)
    ]
    
    ins_y = 185
    for idx, (sql_cmd, row_data, trigger_frame) in enumerate(inserts):
        is_current = trigger_frame - 15 <= i < trigger_frame + 5
        has_executed = i >= trigger_frame
        
        bg_card = (24, 34, 56) if is_current else ((15, 23, 42) if has_executed else (13, 18, 30))
        border_card = CYAN if is_current else (GREEN if has_executed else (30, 41, 59))
        
        draw_rounded_rect(draw, (55, ins_y, 485, ins_y + 80), 8, fill=bg_card, outline=border_card, width=2 if is_current else 1)
        draw.text((70, ins_y + 12), f"-- Record #{idx + 1}", font=font_badge, fill=TEXT_DIM)
        draw.text((70, ins_y + 32), f"INSERT INTO EMPLOYEE VALUES", font=font_code, fill=CYAN)
        draw.text((70, ins_y + 54), f"  ({row_data[0]:04d}, '{row_data[1]}', '{row_data[2]}');", font=font_code, fill=YELLOW)
        
        if has_executed:
            draw.text((430, ins_y + 30), "✔", font=font_bold_lg, fill=GREEN)
            
        ins_y += 95

    # Right: Live Table Storing Data
    draw_rounded_rect(draw, (525, 115, WIDTH - 40, HEIGHT - 75), 14, fill=PANEL_BG, outline=PANEL_BORDER, width=2)
    draw.text((555, 135), "EMPLOYEE Table (Live Storage in DB)", font=font_bold, fill=TEXT_WHITE)
    
    # Table Header
    tx = 555
    ty = 175
    draw_rounded_rect(draw, (tx, ty, WIDTH - 65, ty + 40), 6, fill=(30, 41, 59), outline=CYAN, width=1)
    draw.text((tx + 30, ty + 12), "empId (PK)", font=font_bold, fill=CYAN)
    draw.text((tx + 220, ty + 12), "name (TEXT)", font=font_bold, fill=YELLOW)
    draw.text((tx + 420, ty + 12), "dept (TEXT)", font=font_bold, fill=PURPLE)
    
    # Rows
    rows_data = [
        (1, "Clark", "Sales", 15),
        (2, "Dave", "Accounting", 30),
        (3, "Ava", "Sales", 45)
    ]
    
    row_y = ty + 50
    for r_id, r_name, r_dept, r_frame in rows_data:
        if i >= r_frame:
            # Active animated drop-in
            is_just_added = i < r_frame + 8
            row_bg = (20, 83, 45) if is_just_added else (24, 34, 56)
            row_border = GREEN if is_just_added else PANEL_BORDER
            
            draw_rounded_rect(draw, (tx, row_y, WIDTH - 65, row_y + 50), 6, fill=row_bg, outline=row_border, width=2 if is_just_added else 1)
            draw.text((tx + 40, row_y + 15), f"{r_id:04d}", font=font_code, fill=TEXT_WHITE)
            draw.text((tx + 230, row_y + 15), r_name, font=font_bold, fill=TEXT_WHITE)
            
            dept_badge_bg = (30, 58, 138) if r_dept == "Sales" else (76, 29, 149)
            draw_rounded_rect(draw, (tx + 420, row_y + 10, tx + 560, row_y + 40), 6, fill=dept_badge_bg, outline=CYAN if r_dept == "Sales" else PURPLE, width=1)
            draw.text((tx + 440, row_y + 16), r_dept, font=font_bold, fill=TEXT_WHITE)
        else:
            # Placeholder dashed slot
            draw_rounded_rect(draw, (tx, row_y, WIDTH - 65, row_y + 50), 6, fill=(15, 23, 42), outline=(30, 41, 59), width=1)
            draw.text((tx + 220, row_y + 17), "• Waiting for INSERT statement •", font=font_badge, fill=TEXT_DIM)
            
        row_y += 65
        
    # Bottom disk status
    draw_rounded_rect(draw, (tx, 450, WIDTH - 65, 520), 8, fill=(15, 23, 42), outline=(30, 41, 59), width=1)
    draw.text((tx + 20, 465), "Disk Status: B-Tree Index updated with 3 records.", font=font_body, fill=GREEN)
    draw.text((tx + 20, 490), "Transaction Log (WAL): Committed & Synced to Storage.", font=font_badge, fill=TEXT_MUTED)

    draw_footer_progress(draw, 85 + i, 220, "INSERT INTO Execution")
    frames.append(img)

# ==========================================
# SCENE 4: SELECT WHERE dept = 'Sales' (Query & Filter) (Frames: 145 to 195 -> 3.3 seconds)
# ==========================================
scene_frames_4 = 50
for i in range(scene_frames_4):
    img, draw = create_base_canvas()
    draw_header(draw, "Step 3: Querying & Filtering (SELECT)", "Fetching rows where department matches 'Sales'", 4)
    
    # Left Panel: Query Scanner & Logic
    draw_rounded_rect(draw, (40, 115, 480, HEIGHT - 75), 14, fill=PANEL_BG, outline=PANEL_BORDER, width=2)
    draw_rounded_rect(draw, (40, 115, 480, 160), 14, fill=(15, 23, 42), outline=PANEL_BORDER, width=1)
    draw.text((65, 130), "query.sql — Execution Plan", font=font_badge, fill=TEXT_MUTED)
    
    # SQL Query Highlighted
    draw_rounded_rect(draw, (55, 175, 465, 260), 8, fill=(15, 23, 42), outline=CYAN, width=2)
    draw.text((70, 190), "SELECT * FROM EMPLOYEE", font=font_code, fill=CYAN)
    draw.text((70, 220), "WHERE dept = 'Sales';", font=font_code, fill=YELLOW)
    
    # Evaluation Logic
    draw.text((65, 280), "Query Engine Row-by-Row Scan:", font=font_bold, fill=TEXT_WHITE)
    
    scan_states = [
        ("Row 1: Clark (Sales)", "dept == 'Sales' -> TRUE (Match)", GREEN, 5),
        ("Row 2: Dave (Accounting)", "dept == 'Sales' -> FALSE (Discard)", RED, 18),
        ("Row 3: Ava (Sales)", "dept == 'Sales' -> TRUE (Match)", GREEN, 32)
    ]
    
    eval_y = 315
    for r_text, r_res, r_col, r_start in scan_states:
        is_scanned = i >= r_start
        is_active = r_start <= i < r_start + 12
        
        bg = (24, 34, 56) if is_scanned else (15, 21, 35)
        border = r_col if is_scanned else (30, 42, 65)
        draw_rounded_rect(draw, (55, eval_y, 465, eval_y + 55), 6, fill=bg, outline=border, width=2 if is_active else 1)
        draw.text((70, eval_y + 8), r_text, font=font_bold, fill=TEXT_WHITE if is_scanned else TEXT_DIM)
        draw.text((70, eval_y + 30), r_res if is_scanned else "Pending scan...", font=font_badge, fill=r_col if is_scanned else TEXT_DIM)
        eval_y += 68

    # Right Panel: Table Scan Beam & Highlight
    draw_rounded_rect(draw, (505, 115, WIDTH - 40, HEIGHT - 75), 14, fill=PANEL_BG, outline=PANEL_BORDER, width=2)
    draw.text((535, 135), "Full Table Scan & Filtering", font=font_bold, fill=TEXT_WHITE)
    
    tx = 535
    ty = 175
    draw_rounded_rect(draw, (tx, ty, WIDTH - 65, ty + 40), 6, fill=(30, 41, 59), outline=CYAN, width=1)
    draw.text((tx + 30, ty + 12), "empId", font=font_bold, fill=CYAN)
    draw.text((tx + 200, ty + 12), "name", font=font_bold, fill=YELLOW)
    draw.text((tx + 380, ty + 12), "dept", font=font_bold, fill=PURPLE)
    draw.text((tx + 510, ty + 12), "Filter Result", font=font_bold, fill=TEXT_WHITE)
    
    # 3 Rows with Scanner Evaluation
    row_eval = [
        (1, "Clark", "Sales", True, 5),
        (2, "Dave", "Accounting", False, 18),
        (3, "Ava", "Sales", True, 32)
    ]
    
    row_y = ty + 50
    for r_id, r_name, r_dept, matches, r_start in row_eval:
        is_scanned = i >= r_start
        is_active = r_start <= i < r_start + 12
        
        if not is_scanned:
            row_bg = (24, 34, 56)
            row_border = PANEL_BORDER
            status_text = "Waiting..."
            status_col = TEXT_DIM
        elif matches:
            row_bg = (6, 78, 59) if is_active else (20, 83, 45)
            row_border = GREEN
            status_text = "✔ MATCH (KEEP)"
            status_col = GREEN
        else:
            row_bg = (127, 29, 29) if is_active else (30, 20, 25)
            row_border = RED
            status_text = "✖ FILTERED OUT"
            status_col = RED
            
        draw_rounded_rect(draw, (tx, row_y, WIDTH - 65, row_y + 50), 6, fill=row_bg, outline=row_border, width=2 if is_active else 1)
        draw.text((tx + 35, row_y + 15), f"{r_id:04d}", font=font_code, fill=TEXT_WHITE if is_scanned else TEXT_DIM)
        draw.text((tx + 205, row_y + 15), r_name, font=font_bold, fill=TEXT_WHITE if is_scanned else TEXT_DIM)
        draw.text((tx + 385, row_y + 15), r_dept, font=font_bold, fill=TEXT_WHITE if is_scanned else TEXT_DIM)
        draw.text((tx + 515, row_y + 17), status_text, font=font_badge, fill=status_col)
        
        row_y += 65
        
    # Result set summary
    draw_rounded_rect(draw, (tx, 450, WIDTH - 65, 520), 8, fill=(15, 23, 42), outline=GREEN if i >= 40 else (30, 41, 59), width=2 if i >= 40 else 1)
    if i >= 40:
        draw.text((tx + 20, 465), "Query Execution Complete: 2 rows returned (Clark, Ava).", font=font_bold, fill=GREEN)
        draw.text((tx + 20, 492), "1 row excluded (Dave) because dept != 'Sales'. Execution time: 0.12 ms.", font=font_badge, fill=TEXT_MUTED)
    else:
        draw.text((tx + 20, 475), "Query scanner evaluating rows...", font=font_body, fill=YELLOW)

    draw_footer_progress(draw, 145 + i, 220, "SELECT WHERE Filtering")
    frames.append(img)

# ==========================================
# SCENE 5: FINAL RESULT SET & SUMMARY (Frames: 195 to 220 -> 1.7 seconds)
# ==========================================
scene_frames_5 = 25
for i in range(scene_frames_5):
    img, draw = create_base_canvas()
    draw_header(draw, "Result Set Returned to Application", "The final queried data formatted and transmitted back to the client", 5)
    
    # Left Card: Summary of Core Database Concepts
    draw_rounded_rect(draw, (40, 115, 500, HEIGHT - 75), 14, fill=PANEL_BG, outline=PANEL_BORDER, width=2)
    draw.text((65, 140), "Summary: How Databases Work", font=font_bold, fill=CYAN)
    
    summary_items = [
        ("1. Tables & Schemas", "Provide rigid structure and data consistency."),
        ("2. PRIMARY KEY", "Guarantees every record is distinct (empId)."),
        ("3. SQL Queries", "Declarative language: you ask WHAT, DBMS optimizes HOW."),
        ("4. Filtering (WHERE)", "Fast conditional logic discards unwanted rows."),
        ("5. Application Sync", "Client receives structured JSON from DB tuples.")
    ]
    
    sy = 185
    for stitle, sdesc in summary_items:
        draw_rounded_rect(draw, (60, sy, 480, sy + 56), 8, fill=(15, 23, 42), outline=(30, 41, 59), width=1)
        draw.text((75, sy + 10), stitle, font=font_bold, fill=TEXT_WHITE)
        draw.text((75, sy + 32), sdesc, font=font_badge, fill=TEXT_MUTED)
        sy += 66

    # Right Card: Final Output Table (JSON / Rows)
    draw_rounded_rect(draw, (525, 115, WIDTH - 40, HEIGHT - 75), 14, fill=PANEL_BG, outline=GREEN, width=2)
    draw.text((555, 140), "Final Query Output: SELECT * WHERE dept = 'Sales'", font=font_bold, fill=GREEN)
    
    # Final Result Table
    fx = 555
    fy = 185
    draw_rounded_rect(draw, (fx, fy, WIDTH - 65, fy + 40), 6, fill=(30, 41, 59), outline=GREEN, width=1)
    draw.text((fx + 40, fy + 12), "empId", font=font_bold, fill=CYAN)
    draw.text((fx + 220, fy + 12), "name", font=font_bold, fill=YELLOW)
    draw.text((fx + 420, fy + 12), "dept", font=font_bold, fill=PURPLE)
    
    final_rows = [
        (1, "Clark", "Sales"),
        (3, "Ava", "Sales")
    ]
    
    fry = fy + 50
    for fid, fname, fdept in final_rows:
        draw_rounded_rect(draw, (fx, fry, WIDTH - 65, fry + 55), 6, fill=(20, 83, 45), outline=GREEN, width=2)
        draw.text((fx + 45, fry + 18), f"{fid:04d}", font=font_code_lg, fill=TEXT_WHITE)
        draw.text((fx + 225, fry + 18), fname, font=font_bold_lg, fill=TEXT_WHITE)
        
        draw_rounded_rect(draw, (fx + 420, fry + 12, fx + 560, fry + 44), 6, fill=(30, 58, 138), outline=CYAN, width=1)
        draw.text((fx + 445, fry + 19), fdept, font=font_bold, fill=TEXT_WHITE)
        fry += 70

    # JSON representation below
    draw_rounded_rect(draw, (fx, 395, WIDTH - 65, HEIGHT - 95), 8, fill=(15, 23, 42), outline=(30, 41, 59), width=1)
    draw.text((fx + 20, 410), "// Transmitted to Frontend App as JSON:", font=font_badge, fill=TEXT_MUTED)
    draw.text((fx + 20, 435), '[ {"empId": 1, "name": "Clark", "dept": "Sales"},', font=font_code, fill=CYAN)
    draw.text((fx + 20, 465), '  {"empId": 3, "name": "Ava",   "dept": "Sales"} ]', font=font_code, fill=CYAN)
    draw.text((fx + 20, 498), "✔ Application successfully displays 2 Sales employees in UI!", font=font_bold, fill=GREEN)

    draw_footer_progress(draw, 195 + i, 220, "Result Set Delivered")
    frames.append(img)

print(f"Total frames generated: {len(frames)}")

# Save to WebP video & GIF
webp_path_ws = os.path.join(WORKSPACE_DIR, "database_tutorial.webp")
gif_path_ws = os.path.join(WORKSPACE_DIR, "database_tutorial.gif")

webp_path_art = os.path.join(ARTIFACT_DIR, "database_tutorial.webp")
gif_path_art = os.path.join(ARTIFACT_DIR, "database_tutorial.gif")

print(f"Saving high quality animated WebP: {webp_path_ws}")
# duration is in milliseconds per frame (1000 / FPS)
duration_ms = int(1000 / FPS)
frames[0].save(
    webp_path_ws,
    save_all=True,
    append_images=frames[1:],
    duration=duration_ms,
    loop=0,
    quality=85,
    method=4
)

# Also copy to artifact directory
import shutil
shutil.copyfile(webp_path_ws, webp_path_art)

print(f"Saving animated GIF: {gif_path_ws}")
# Downscale slightly for GIF to keep it very fast and responsive
small_frames = [f.resize((800, 450), Image.Resampling.LANCZOS) for f in frames[::2]]
small_frames[0].save(
    gif_path_ws,
    save_all=True,
    append_images=small_frames[1:],
    duration=duration_ms * 2,
    loop=0,
    optimize=True
)
shutil.copyfile(gif_path_ws, gif_path_art)

print("Video generation successfully completed!")
