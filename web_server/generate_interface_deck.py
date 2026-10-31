import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_interface_deck(output_path="Presentasi_REINVENT4_Interface_Style.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ─────────────────────────────────────────────────────────────────────────
    # Slidesgo "Interface Style Website Design" Palette & Tokens
    # ─────────────────────────────────────────────────────────────────────────
    BG_CANVAS = RGBColor(250, 247, 242)      # #FAF7F2 Warm off-white
    WINDOW_BG = RGBColor(255, 255, 255)      # Pure white window surface
    BORDER_DARK = RGBColor(46, 58, 47)       # #2E3A2F Retro dark olive-charcoal outline
    
    # Traffic Light Buttons
    BTN_RED = RGBColor(229, 89, 76)          # #E5594C
    BTN_ORANGE = RGBColor(246, 165, 98)      # #F6A562
    BTN_BLUE = RGBColor(148, 194, 209)       # #94C2D1
    
    # Typography Colors
    TEXT_HEADING = RGBColor(31, 58, 36)      # #1F3A24 Dark forest green
    TEXT_BODY = RGBColor(66, 77, 67)         # #424D43 Muted charcoal
    TEXT_MUTED = RGBColor(115, 128, 116)     # #738074 Soft grey-green
    
    # Pastel Accent Badges (Interface Style)
    PASTEL_PINK = RGBColor(250, 210, 207)    # #FAD2CF
    PASTEL_BLUE = RGBColor(182, 216, 228)    # #B6D8E4
    PASTEL_ORANGE = RGBColor(249, 193, 139)  # #F9C18B
    PASTEL_GREEN = RGBColor(197, 222, 201)   # #C5DEC9
    PASTEL_YELLOW = RGBColor(249, 240, 217)  # #F9F0D9
    
    PLUS_COLOR = RGBColor(179, 206, 205)     # #B3CECD Subtle mint plus signs

    def draw_plus_grid(slide):
        # Background canvas fill
        bg_rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg_rect.fill.solid()
        bg_rect.fill.fore_color.rgb = BG_CANVAS
        bg_rect.line.fill.background()

        # Perimeter plus signs (+ + + +)
        # Top row
        for x in range(1, 13):
            tb = slide.shapes.add_textbox(Inches(x), Inches(0.04), Inches(0.3), Inches(0.3))
            p = tb.text_frame.paragraphs[0]
            p.text = "+"
            p.font.size = Pt(12)
            p.font.color.rgb = PLUS_COLOR
        # Bottom row
        for x in range(1, 13):
            tb = slide.shapes.add_textbox(Inches(x), Inches(7.18), Inches(0.3), Inches(0.3))
            p = tb.text_frame.paragraphs[0]
            p.text = "+"
            p.font.size = Pt(12)
            p.font.color.rgb = PLUS_COLOR
        # Left and Right edges
        for y in range(1, 7):
            tb_l = slide.shapes.add_textbox(Inches(0.06), Inches(y), Inches(0.3), Inches(0.3))
            p_l = tb_l.text_frame.paragraphs[0]
            p_l.text = "+"
            p_l.font.size = Pt(12)
            p_l.font.color.rgb = PLUS_COLOR

            tb_r = slide.shapes.add_textbox(Inches(13.0), Inches(y), Inches(0.3), Inches(0.3))
            p_r = tb_r.text_frame.paragraphs[0]
            p_r.text = "+"
            p_r.font.size = Pt(12)
            p_r.font.color.rgb = PLUS_COLOR

    def draw_window_frame(slide, url_path="proto-reinvent4.streamlit.app"):
        draw_plus_grid(slide)

        # Main window container (rounded rectangle)
        win = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.38), Inches(0.36), Inches(12.57), Inches(6.78))
        win.fill.solid()
        win.fill.fore_color.rgb = WINDOW_BG
        win.line.color.rgb = BORDER_DARK
        win.line.width = Pt(1.5)

        # Window Header Divider line
        div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.38), Inches(1.05), Inches(12.57), Inches(0.015))
        div.fill.solid()
        div.fill.fore_color.rgb = BORDER_DARK
        div.line.fill.background()

        # Traffic light buttons (Red, Orange, Blue)
        btn_y = Inches(0.55)
        for i, color in enumerate([BTN_RED, BTN_ORANGE, BTN_BLUE]):
            btn = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.68 + i * 0.40), btn_y, Inches(0.28), Inches(0.28))
            btn.fill.solid()
            btn.fill.fore_color.rgb = color
            btn.line.color.rgb = BORDER_DARK
            btn.line.width = Pt(1.2)

        # URL / Search bar mockup in center of title bar
        url_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.2), Inches(0.50), Inches(8.9), Inches(0.38))
        url_box.fill.solid()
        url_box.fill.fore_color.rgb = BG_CANVAS
        url_box.line.color.rgb = BORDER_DARK
        url_box.line.width = Pt(1.0)

        tf = url_box.text_frame
        tf.word_wrap = True
        tf.margin_top = Inches(0.04)
        p = tf.paragraphs[0]
        p.text = f"https://reinvent4.local/{url_path}"
        p.font.size = Pt(11)
        p.font.name = "Consolas"
        p.font.color.rgb = TEXT_MUTED
        p.alignment = PP_ALIGN.CENTER

        return win

    def add_p(tf, text, size=12, bold=False, color=TEXT_BODY, after=6, align=None, name="Segoe UI"):
        if len(tf.paragraphs) == 1 and tf.paragraphs[0].text == "":
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = text
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = color
        p.font.name = name
        p.space_after = Pt(after)
        if align:
            p.alignment = align
        return p

    def draw_badge(slide, left, top, width, height, text, bg_color):
        b = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        b.fill.solid()
        b.fill.fore_color.rgb = bg_color
        b.line.color.rgb = BORDER_DARK
        b.line.width = Pt(1.2)
        tf = b.text_frame
        tf.margin_top = Inches(0.02)
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_HEADING
        p.font.name = "Segoe UI"
        p.alignment = PP_ALIGN.CENTER
        return b

    def draw_ui_card(slide, left, top, width, height, bg_color=WINDOW_BG):
        c = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        c.fill.solid()
        c.fill.fore_color.rgb = bg_color
        c.line.color.rgb = BORDER_DARK
        c.line.width = Pt(1.2)
        return c

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 1: Cover / Homepage Mockup
    # ═════════════════════════════════════════════════════════════════════════
    s1 = prs.slides.add_slide(blank_layout)
    draw_window_frame(s1, "home")

    # Folder icons on the left (retro aesthetic matching Slidesgo thumbnail)
    folder_tags = [
        ("Pre-processing", PASTEL_PINK),
        ("Transfer Learning", PASTEL_BLUE),
        ("Staged Learning (RL)", PASTEL_ORANGE),
        ("Sampling & Metrik", PASTEL_GREEN)
    ]
    for idx, (lbl, col) in enumerate(folder_tags):
        fy = Inches(1.8 + idx * 1.1)
        draw_badge(s1, Inches(0.9), fy, Inches(2.2), Inches(0.55), lbl, col)

    # Center Hero Title
    hero_box = s1.shapes.add_textbox(Inches(3.4), Inches(1.8), Inches(8.8), Inches(3.2))
    tf1 = hero_box.text_frame
    tf1.word_wrap = True

    add_p(tf1, "REINVENT 4 WEB INTERFACE", 14, True, BTN_ORANGE, after=10)
    add_p(tf1, "Generative Drug Design\nMade Practical.", 38, True, TEXT_HEADING, after=16)
    add_p(tf1, "Mengubah software AI penemuan obat berbasis CLI & TOML yang rumit\nmenjadi aplikasi web interaktif, visual, dan ramah pengguna.", 15, False, TEXT_BODY, after=24)

    # Search Bar Mockup / Sub-box
    sub_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.4), Inches(4.5), Inches(8.8), Inches(0.65))
    sub_box.fill.solid()
    sub_box.fill.fore_color.rgb = BG_CANVAS
    sub_box.line.color.rgb = BORDER_DARK
    sub_box.line.width = Pt(1.2)
    tf_sub = sub_box.text_frame
    tf_sub.margin_top = Inches(0.12)
    add_p(tf_sub, "Input: Dataset SMILES  ➔  AI Pipeline (TL/RL)  ➔  Output: Kandidat Molekul Obat Baru", 12.5, False, TEXT_BODY, align=PP_ALIGN.CENTER)

    # Action Button on bottom right (matching "Start" button in Slidesgo template)
    start_btn = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.3), Inches(5.8), Inches(2.0), Inches(0.7))
    start_btn.fill.solid()
    start_btn.fill.fore_color.rgb = PASTEL_YELLOW
    start_btn.line.color.rgb = BORDER_DARK
    start_btn.line.width = Pt(1.4)
    tf_btn = start_btn.text_frame
    tf_btn.margin_top = Inches(0.14)
    add_p(tf_btn, "Mulai  ➔", 15, True, TEXT_HEADING, align=PP_ALIGN.CENTER)

    # Presenter info
    info_box = s1.shapes.add_textbox(Inches(3.4), Inches(5.9), Inches(6.5), Inches(0.6))
    tf_info = info_box.text_frame
    add_p(tf_info, "Oleh: [Nama Anda]  ·  NIM: [NIM Anda]  ·  S2 Farmasi Komputasi 2026", 11.5, False, TEXT_MUTED)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 2: Table of Contents (6 Pastel Badges matching Slide 2 of template)
    # ═════════════════════════════════════════════════════════════════════════
    s2 = prs.slides.add_slide(blank_layout)
    draw_window_frame(s2, "menu")

    title_box = s2.shapes.add_textbox(Inches(0.9), Inches(1.3), Inches(11.5), Inches(0.7))
    tf2 = title_box.text_frame
    add_p(tf2, "Menu Presentasi", 26, True, TEXT_HEADING, align=PP_ALIGN.CENTER)

    sections = [
        ("01", "Kenapa Dibuat?", "Masalah nyata CLI vs solusi web app yang kami bangun.", PASTEL_PINK),
        ("02", "Tech Stack & Arsitektur", "Desain decoupled: Streamlit, FastAPI, REINVENT core.", PASTEL_BLUE),
        ("03", "4-Stage Pipeline", "Workflow utuh: Preprocessing, TL, RL, hingga Sampling.", PASTEL_ORANGE),
        ("04", "Fitur: Data & Training", "Otomasi sanitasi data & finetuning model prior.", PASTEL_GREEN),
        ("05", "Fitur: RL & Evaluasi", "Dual-model setup (Prior + Agent) & kalkulasi RDKit.", PASTEL_YELLOW),
        ("06", "UX, Demo & Stabilitas", "Bilingual, job tracker, live background execution.", PASTEL_PINK)
    ]

    for idx, (num, heading, desc, col) in enumerate(sections):
        row = idx // 3
        col_idx = idx % 3
        card_x = Inches(0.95 + col_idx * 3.95)
        card_y = Inches(2.2 + row * 2.3)

        # Card container
        draw_ui_card(s2, card_x, card_y, Inches(3.65), Inches(2.05), WINDOW_BG)

        # Number Badge on top left of card
        draw_badge(s2, card_x + Inches(0.2), card_y + Inches(0.2), Inches(0.9), Inches(0.42), num, col)

        # Text inside card
        tb = s2.shapes.add_textbox(card_x + Inches(0.2), card_y + Inches(0.75), Inches(3.25), Inches(1.15))
        tf = tb.text_frame
        tf.word_wrap = True
        add_p(tf, heading, 15, True, TEXT_HEADING, after=4)
        add_p(tf, desc, 11, False, TEXT_BODY, after=0)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 3: Problem & Solution (Kenapa Dibuat?)
    # ═════════════════════════════════════════════════════════════════════════
    s3 = prs.slides.add_slide(blank_layout)
    draw_window_frame(s3, "why-this-app")

    tb = s3.shapes.add_textbox(Inches(0.9), Inches(1.2), Inches(11.5), Inches(0.6))
    add_p(tb.text_frame, "Kenapa Web App Ini Dibuat?", 24, True, TEXT_HEADING)

    # Left: The Problem Card
    draw_ui_card(s3, Inches(0.9), Inches(1.85), Inches(5.6), Inches(4.9), BG_CANVAS)
    draw_badge(s3, Inches(1.15), Inches(2.05), Inches(1.6), Inches(0.4), "MASALAH", PASTEL_PINK)
    tb = s3.shapes.add_textbox(Inches(1.15), Inches(2.6), Inches(5.1), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    add_p(tf, "REINVENT 4 itu hebat, tapi...", 17, True, TEXT_HEADING, after=12)
    bullets = [
        "100% berbasis Terminal (CLI) — harus mengetik sintaks panjang.",
        "Konfigurasi file TOML sangat ketat — salah spasi atau salah tipe data, komputasi langsung gagal.",
        "Output berupa CSV teks mentah — tidak ada visual struktur molekul langsung.",
        "Tidak ada job tracker bawaan — peneliti harus memeriksa log konsol secara manual.",
        "Hasilnya: Kurva belajar sangat tinggi untuk peneliti kimia/farmasi non-programmer."
    ]
    for b in bullets:
        add_p(tf, "•  " + b, 12, False, TEXT_BODY, after=8)

    # Right: The Solution Card
    draw_ui_card(s3, Inches(6.8), Inches(1.85), Inches(5.6), Inches(4.9), WINDOW_BG)
    draw_badge(s3, Inches(7.05), Inches(2.05), Inches(1.6), Inches(0.4), "SOLUSI", PASTEL_GREEN)
    tb = s3.shapes.add_textbox(Inches(7.05), Inches(2.6), Inches(5.1), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    add_p(tf, "Bungkus Menjadi Web GUI Interaktif", 17, True, TEXT_HEADING, after=12)
    bullets = [
        "Zero-CLI: Upload file, atur slider/dropdown, dan klik 'Mulai'.",
        "TOML Builder Otomatis: Menyusun parameter valid tanpa risiko human-error.",
        "Visualisasi Kimia Instan: RDKit menggambar struktur 2D molekul langsung di layar.",
        "Asynchronous Background Jobs: Server tidak freeze saat neural network dilatih.",
        "Job History & File Management: Semua hasil (.prior, .csv) tersimpan rapi dan dapat diunduh kapan saja."
    ]
    for b in bullets:
        add_p(tf, "•  " + b, 12, False, TEXT_BODY, after=8)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 4: Tech Stack & Decoupled Architecture
    # ═════════════════════════════════════════════════════════════════════════
    s4 = prs.slides.add_slide(blank_layout)
    draw_window_frame(s4, "architecture")

    tb = s4.shapes.add_textbox(Inches(0.9), Inches(1.2), Inches(11.5), Inches(0.6))
    add_p(tb.text_frame, "Arsitektur Sistem: Full-Stack Terpisah", 24, True, TEXT_HEADING)

    layers = [
        ("FRONTEND", "Streamlit UI", "Port 8501", PASTEL_BLUE, [
            "Tampilan interaktif dan responsif.",
            "Bilingual (ID/EN) switch kapan saja.",
            "Render struktur molekul 2D (RDKit).",
            "Sidebar live status & scrollable job history."
        ]),
        ("BACKEND API", "FastAPI Server", "Port 8000", PASTEL_PINK, [
            "REST API endpoints terstruktur.",
            "BackgroundTasks (non-blocking).",
            "TOML builder dinamis.",
            "Auto-detect kolom CSV (SMILES/Smiles).",
            "File streaming untuk download artefak."
        ]),
        ("ENGINE", "REINVENT 4 Core", "Python 3.11", PASTEL_ORANGE, [
            "Dieksekusi via Subprocess terisolasi.",
            "Modul datapipeline untuk sanitasi.",
            "Generative model (RNN) & DAP optimizer.",
            "Stabil di CPU mesin laptop biasa."
        ]),
        ("STORAGE", "Job Persistence", "/jobs/{uuid}", PASTEL_YELLOW, [
            "Folder terisolasi dengan UUID unik.",
            "status.json (QUEUED, RUNNING, COMPLETED).",
            "run.log untuk audit dan debugging.",
            "Data tidak hilang saat browser di-refresh."
        ])
    ]

    for idx, (tag, name, port, col, points) in enumerate(layers):
        lx = Inches(0.9 + idx * 2.95)
        draw_ui_card(s4, lx, Inches(1.85), Inches(2.78), Inches(4.9), WINDOW_BG)
        draw_badge(s4, lx + Inches(0.2), Inches(2.05), Inches(2.38), Inches(0.38), tag, col)

        tb = s4.shapes.add_textbox(lx + Inches(0.2), Inches(2.55), Inches(2.38), Inches(4.0))
        tf = tb.text_frame
        tf.word_wrap = True
        add_p(tf, name, 15, True, TEXT_HEADING, after=2)
        add_p(tf, port, 11, False, TEXT_MUTED, after=12, name="Consolas")
        for pt in points:
            add_p(tf, "• " + pt, 11, False, TEXT_BODY, after=6)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 5: 4-Stage End-to-End Pipeline
    # ═════════════════════════════════════════════════════════════════════════
    s5 = prs.slides.add_slide(blank_layout)
    draw_window_frame(s5, "pipeline")

    tb = s5.shapes.add_textbox(Inches(0.9), Inches(1.2), Inches(11.5), Inches(0.6))
    add_p(tb.text_frame, "Alur Kerja: 4 Tahap Desain Molekul Lengkap", 24, True, TEXT_HEADING)

    stages = [
        ("01", "Pre-processing", "Pembersihan Data", PASTEL_PINK, [
            "Input: Dataset CSV mentah (misal: ChEMBL).",
            "Filter: Heavy atoms, berat molekul, muatan.",
            "Output: File .smi bersih terstandardisasi.",
            "Tujuan: Menghilangkan noise sebelum AI dilatih."
        ]),
        ("02", "Transfer Learning", "Fokuskan Model", PASTEL_BLUE, [
            "Input: Base Prior + Dataset target (.csv).",
            "Finetuning bobot jaringan syaraf tiruan.",
            "Fitur: Validation split otomatis (slider 5-50%).",
            "Output: Checkpoint model baru (.prior)."
        ]),
        ("03", "Staged Learning (RL)", "Optimasi Profil Obat", PASTEL_ORANGE, [
            "Input: Dual-Model (Prior Base + Agent TL).",
            "Reinforcement Learning terpandu fungsi reward.",
            "Target: Bobot QED & rentang berat molekul.",
            "Output: Model teroptimasi menuju profil obat."
        ]),
        ("04", "Sampling & Evaluasi", "Panen Kandidat", PASTEL_GREEN, [
            "Input: Model prior akhir (Base / TL / RL).",
            "Generate ratusan struktur molekul baru.",
            "Kalkulasi Validity %, Uniqueness %, Tanimoto.",
            "Output: Tabel CSV & galeri visual 2D."
        ])
    ]

    for idx, (num, title, sub, col, points) in enumerate(stages):
        lx = Inches(0.9 + idx * 2.95)
        draw_ui_card(s5, lx, Inches(1.85), Inches(2.78), Inches(4.9), WINDOW_BG)
        draw_badge(s5, lx + Inches(0.2), Inches(2.05), Inches(0.8), Inches(0.38), num, col)

        tb = s5.shapes.add_textbox(lx + Inches(0.2), Inches(2.55), Inches(2.38), Inches(4.0))
        tf = tb.text_frame
        tf.word_wrap = True
        add_p(tf, title, 15, True, TEXT_HEADING, after=2)
        add_p(tf, sub, 11, False, TEXT_MUTED, after=12)
        for pt in points:
            add_p(tf, "• " + pt, 11, False, TEXT_BODY, after=6)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 6: Fitur 1 - Data Pre-processing
    # ═════════════════════════════════════════════════════════════════════════
    s6 = prs.slides.add_slide(blank_layout)
    draw_window_frame(s6, "features/preprocessing")

    tb = s6.shapes.add_textbox(Inches(0.9), Inches(1.2), Inches(11.5), Inches(0.6))
    add_p(tb.text_frame, "Fitur 1: Data Pre-processing Pipeline", 24, True, TEXT_HEADING)

    draw_ui_card(s6, Inches(0.9), Inches(1.85), Inches(5.6), Inches(4.9), WINDOW_BG)
    draw_badge(s6, Inches(1.15), Inches(2.05), Inches(2.2), Inches(0.4), "PARAMETER FILTER", PASTEL_PINK)
    tb = s6.shapes.add_textbox(Inches(1.15), Inches(2.6), Inches(5.1), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    add_p(tf, "Filter & Normalisasi Dataset SMILES", 16, True, TEXT_HEADING, after=10)
    items = [
        "Powered by reinvent.datapipeline resmi di backend.",
        "Rentang Heavy Atoms: Batasi ukuran molekul (min 2, max 90 atom).",
        "Max Molecular Weight: Menyingkirkan senyawa polimer/makro (default 1200 Da).",
        "Uncharge (Netralisasi Muatan): Otomatis menetralkan ion garam.",
        "Keep Stereochemistry: Mempertahankan konfigurasi kiral (R/S)."
    ]
    for it in items:
        add_p(tf, "• " + it, 12, False, TEXT_BODY, after=8)

    draw_ui_card(s6, Inches(6.8), Inches(1.85), Inches(5.6), Inches(4.9), BG_CANVAS)
    draw_badge(s6, Inches(7.05), Inches(2.05), Inches(2.4), Inches(0.4), "DEVELOPER HIGHLIGHT", PASTEL_YELLOW)
    tb = s6.shapes.add_textbox(Inches(7.05), Inches(2.6), Inches(5.1), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    add_p(tf, "Smart Column Auto-Detection", 16, True, TEXT_HEADING, after=10)
    items = [
        "Solusi bug Polars: REINVENT default mencari kolom case-sensitive 'SMILES'.",
        "Sistem kami otomatis membaca header CSV: mau 'SMILES', 'Smiles', atau 'smiles', semuanya lolos validasi tanpa error.",
        "SMILES Counter Otomatis: Langsung menghitung total senyawa yang lolos filter.",
        "Preview 20 Baris Pertama: Peneliti dapat memverifikasi struktur sebelum diproses.",
        "One-Click Download: Unduh processed.smi langsung untuk tahap Transfer Learning."
    ]
    for it in items:
        add_p(tf, "• " + it, 12, False, TEXT_BODY, after=8)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 7: Fitur 2 - Transfer Learning & Dynamic Split
    # ═════════════════════════════════════════════════════════════════════════
    s7 = prs.slides.add_slide(blank_layout)
    draw_window_frame(s7, "features/transfer-learning")

    tb = s7.shapes.add_textbox(Inches(0.9), Inches(1.2), Inches(11.5), Inches(0.6))
    add_p(tb.text_frame, "Fitur 2: Transfer Learning (Finetuning Prior)", 24, True, TEXT_HEADING)

    draw_ui_card(s7, Inches(0.9), Inches(1.85), Inches(5.6), Inches(4.9), WINDOW_BG)
    draw_badge(s7, Inches(1.15), Inches(2.05), Inches(2.0), Inches(0.4), "CARA KERJA", PASTEL_BLUE)
    tb = s7.shapes.add_textbox(Inches(1.15), Inches(2.6), Inches(5.1), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    add_p(tf, "Mengarahkan Model ke Senyawa Target", 16, True, TEXT_HEADING, after=10)
    items = [
        "Pilih Base Prior: Built-in (reinvent.prior, libinvent, linkinvent) atau upload custom.",
        "Upload dataset target dalam format CSV atau SMILES.",
        "Pengaturan interaktif: Jumlah Epochs dan Batch Size.",
        "Tombol 'Muat Data Contoh': Menyediakan 30 molekul drug-like siap pakai untuk quick testing tanpa upload manual.",
        "Output: Model checkpoint baru (.prior) berukuran ~23 MB."
    ]
    for it in items:
        add_p(tf, "• " + it, 12, False, TEXT_BODY, after=8)

    draw_ui_card(s7, Inches(6.8), Inches(1.85), Inches(5.6), Inches(4.9), BG_CANVAS)
    draw_badge(s7, Inches(7.05), Inches(2.05), Inches(2.5), Inches(0.4), "FITUR UNGGULAN", PASTEL_GREEN)
    tb = s7.shapes.add_textbox(Inches(7.05), Inches(2.6), Inches(5.1), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    add_p(tf, "Dynamic Validation Split Otomatis", 16, True, TEXT_HEADING, after=10)
    items = [
        "Cukup upload 1 file CSV tunggal: Backend otomatis mengacak dan membaginya menjadi dataset training dan validasi.",
        "Slider Proporsi: Fleksibel antara 5% hingga 50% (default: 20% validasi).",
        "Opsi Non-Split via Toggle: Berguna saat menggunakan model yang tidak mensyaratkan data validasi (misal LibInvent).",
        "Menghilangkan proses split manual yang merepotkan peneliti di luar aplikasi."
    ]
    for it in items:
        add_p(tf, "• " + it, 12, False, TEXT_BODY, after=8)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 8: Fitur 3 - Staged Learning (Dual-Model RL)
    # ═════════════════════════════════════════════════════════════════════════
    s8 = prs.slides.add_slide(blank_layout)
    draw_window_frame(s8, "features/staged-learning")

    tb = s8.shapes.add_textbox(Inches(0.9), Inches(1.2), Inches(11.5), Inches(0.6))
    add_p(tb.text_frame, "Fitur 3: Staged Learning (Reinforcement Learning)", 24, True, TEXT_HEADING)

    draw_ui_card(s8, Inches(0.9), Inches(1.85), Inches(5.6), Inches(4.9), WINDOW_BG)
    draw_badge(s8, Inches(1.15), Inches(2.05), Inches(2.2), Inches(0.4), "DUAL-MODEL SETUP", PASTEL_ORANGE)
    tb = s8.shapes.add_textbox(Inches(1.15), Inches(2.6), Inches(5.1), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    add_p(tf, "Arsitektur Prior vs Agent yang Tepat", 16, True, TEXT_HEADING, after=10)
    items = [
        "Sisi Kiri (Prior Base): Model acuan bawaan — bertindak sebagai 'pagar pengawas' agar struktur tetap mematuhi aturan kimia.",
        "Sisi Kanan (Agent TL): Model hasil Transfer Learning — agen yang aktif dieksplorasi dan dioptimasi.",
        "Kedua sisi mendukung dropdown model bawaan atau upload file .prior kustom.",
        "Sesuai dengan arsitektur native REINVENT 4 — tidak disederhanakan secara keliru."
    ]
    for it in items:
        add_p(tf, "• " + it, 12, False, TEXT_BODY, after=8)

    draw_ui_card(s8, Inches(6.8), Inches(1.85), Inches(5.6), Inches(4.9), BG_CANVAS)
    draw_badge(s8, Inches(7.05), Inches(2.05), Inches(2.4), Inches(0.4), "REWARD & PARAMETER", PASTEL_YELLOW)
    tb = s8.shapes.add_textbox(Inches(7.05), Inches(2.6), Inches(5.1), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    add_p(tf, "Multi-Component Scoring Function", 16, True, TEXT_HEADING, after=10)
    items = [
        "QED Weight (0.0 - 10.0): Mengatur bobot kelayakan obat (drug-likeness).",
        "Min & Max MW: Membatasi rentang berat molekul yang diincar peneliti.",
        "Max Steps: Menentukan iterasi siklus optimasi RL.",
        "Strategi DAP (Diversity-Aware Penalization): Mencegah terjadinya mode collapse.",
        "Output: Checkpoint stage1.chkpt & log performa bertahap CSV."
    ]
    for it in items:
        add_p(tf, "• " + it, 12, False, TEXT_BODY, after=8)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 9: Fitur 4 - Sampling & Evaluasi Molekul
    # ═════════════════════════════════════════════════════════════════════════
    s9 = prs.slides.add_slide(blank_layout)
    draw_window_frame(s9, "features/sampling")

    tb = s9.shapes.add_textbox(Inches(0.9), Inches(1.2), Inches(11.5), Inches(0.6))
    add_p(tb.text_frame, "Fitur 4: Sampling & Evaluasi Molekul Baru", 24, True, TEXT_HEADING)

    draw_ui_card(s9, Inches(0.9), Inches(1.85), Inches(5.6), Inches(4.9), WINDOW_BG)
    draw_badge(s9, Inches(1.15), Inches(2.05), Inches(2.2), Inches(0.4), "GENERASI MOLEKUL", PASTEL_GREEN)
    tb = s9.shapes.add_textbox(Inches(1.15), Inches(2.6), Inches(5.1), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    add_p(tf, "De Novo Chemical Space Exploration", 16, True, TEXT_HEADING, after=10)
    items = [
        "Pilih model prior (Base / hasil TL / hasil RL).",
        "Tentukan jumlah molekul yang ingin digenerasi (N smiles).",
        "Tanimoto Similarity Index: Masukkan SMILES molekul referensi untuk membandingkan kemiripan struktur kimia secara otomatis (Morgan Fingerprints).",
        "Ekspor tabel data lengkap dalam format CSV untuk analisis downstream (docking, dll)."
    ]
    for it in items:
        add_p(tf, "• " + it, 12, False, TEXT_BODY, after=8)

    draw_ui_card(s9, Inches(6.8), Inches(1.85), Inches(5.6), Inches(4.9), BG_CANVAS)
    draw_badge(s9, Inches(7.05), Inches(2.05), Inches(2.2), Inches(0.4), "METRIK KIMIAWI", PASTEL_PINK)
    tb = s9.shapes.add_textbox(Inches(7.05), Inches(2.6), Inches(5.1), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    add_p(tf, "Dashboard Evaluasi Otomatis (RDKit)", 16, True, TEXT_HEADING, after=10)
    items = [
        "Validity Rate (%): Menguji apakah struktur mematuhi aturan valensi kimia nyata.",
        "Uniqueness Rate (%): Mengukur keragaman populasi molekul (mendeteksi redundansi).",
        "Visualisasi Grid 2D RDKit: Menggambar struktur molekul 2D langsung di halaman web tanpa software eksternal.",
        "Instant Feedback: Peneliti langsung tahu apakah model bekerja dengan baik."
    ]
    for it in items:
        add_p(tf, "• " + it, 12, False, TEXT_BODY, after=8)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 10: UX, Job Tracking & Developer Experience
    # ═════════════════════════════════════════════════════════════════════════
    s10 = prs.slides.add_slide(blank_layout)
    draw_window_frame(s10, "system-ux")

    tb = s10.shapes.add_textbox(Inches(0.9), Inches(1.2), Inches(11.5), Inches(0.6))
    add_p(tb.text_frame, "UX & Keandalan Sistem", 24, True, TEXT_HEADING)

    cards_info = [
        ("Bilingual System", PASTEL_BLUE, [
            "Welcome/Landing Page elegan dengan opsi bahasa.",
            "Dynamic Switcher: Bahasa Indonesia & English.",
            "Kamus translasi modular (translations.py) memudahkan lokalisasi bahasa lain."
        ]),
        ("Live Job Tracker", PASTEL_ORANGE, [
            "Status live di sidebar: QUEUED, RUNNING, COMPLETED, FAILED.",
            "Riwayat job tersimpan dalam container scrollable.",
            "Buka dan tutup hasil kapan saja tanpa mengotori halaman kerja."
        ]),
        ("One-Click Launch", PASTEL_GREEN, [
            "start_all.bat menyalakan API & UI secara otomatis.",
            "Subprocess isolation menjamin web tidak macet saat neural network dilatih.",
            "Error handling jelas yang memandu pemecahan masalah."
        ])
    ]

    for idx, (title, col, points) in enumerate(cards_info):
        lx = Inches(0.9 + idx * 3.95)
        draw_ui_card(s10, lx, Inches(1.85), Inches(3.65), Inches(4.9), WINDOW_BG)
        draw_badge(s10, lx + Inches(0.2), Inches(2.05), Inches(2.5), Inches(0.4), title, col)

        tb = s10.shapes.add_textbox(lx + Inches(0.2), Inches(2.65), Inches(3.25), Inches(3.9))
        tf = tb.text_frame
        tf.word_wrap = True
        for pt in points:
            add_p(tf, "• " + pt, 12, False, TEXT_BODY, after=10)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 11: Demo / Screenshot Frame
    # ═════════════════════════════════════════════════════════════════════════
    s11 = prs.slides.add_slide(blank_layout)
    draw_window_frame(s11, "live-demo")

    tb = s11.shapes.add_textbox(Inches(0.9), Inches(1.2), Inches(11.5), Inches(0.6))
    add_p(tb.text_frame, "Tampilan Antarmuka Web (Demo)", 24, True, TEXT_HEADING)

    # 3 screenshot placeholder cards
    screens = [
        ("Landing Page & Bahasa", PASTEL_PINK),
        ("Pre-processing & TL", PASTEL_BLUE),
        ("Sampling & Hasil 2D RDKit", PASTEL_GREEN)
    ]
    for idx, (lbl, col) in enumerate(screens):
        lx = Inches(0.9 + idx * 3.95)
        draw_ui_card(s11, lx, Inches(1.85), Inches(3.65), Inches(4.9), BG_CANVAS)
        draw_badge(s11, lx + Inches(0.2), Inches(2.05), Inches(3.25), Inches(0.4), lbl, col)

        # Placeholder box
        inner = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, lx + Inches(0.2), Inches(2.65), Inches(3.25), Inches(3.85))
        inner.fill.solid()
        inner.fill.fore_color.rgb = WINDOW_BG
        inner.line.color.rgb = BORDER_DARK
        inner.line.width = Pt(1.0)

        tf = inner.text_frame
        tf.margin_top = Inches(1.6)
        add_p(tf, f"[Tempelkan Screenshot\n{lbl}\ndi sini]", 12.5, False, TEXT_MUTED, align=PP_ALIGN.CENTER)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 12: Penutup / Q&A
    # ═════════════════════════════════════════════════════════════════════════
    s12 = prs.slides.add_slide(blank_layout)
    draw_window_frame(s12, "finish")

    hero_box = s12.shapes.add_textbox(Inches(2.0), Inches(2.0), Inches(9.33), Inches(3.0))
    tf12 = hero_box.text_frame
    tf12.word_wrap = True

    add_p(tf12, "SYSTEM READY & OPERATIONAL", 14, True, BTN_ORANGE, after=12, align=PP_ALIGN.CENTER)
    add_p(tf12, "Terima Kasih", 44, True, TEXT_HEADING, after=16, align=PP_ALIGN.CENTER)
    add_p(tf12, "Sesi Tanya Jawab (Q & A) & Demonstrasi Sistem Secara Langsung", 17, False, TEXT_BODY, after=28, align=PP_ALIGN.CENTER)

    # 2 Action buttons at bottom
    btn_l = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.1), Inches(5.2), Inches(2.4), Inches(0.65))
    btn_l.fill.solid()
    btn_l.fill.fore_color.rgb = PASTEL_YELLOW
    btn_l.line.color.rgb = BORDER_DARK
    btn_l.line.width = Pt(1.2)
    tf_bl = btn_l.text_frame
    tf_bl.margin_top = Inches(0.12)
    add_p(tf_bl, "UI: proto-reinvent4.streamlit.app", 12, True, TEXT_HEADING, align=PP_ALIGN.CENTER, name="Consolas")

    btn_r = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(5.2), Inches(2.4), Inches(0.65))
    btn_r.fill.solid()
    btn_r.fill.fore_color.rgb = PASTEL_GREEN
    btn_r.line.color.rgb = BORDER_DARK
    btn_r.line.width = Pt(1.2)
    tf_br = btn_r.text_frame
    tf_br.margin_top = Inches(0.12)
    add_p(tf_br, "API: localhost:8000/docs", 12, True, TEXT_HEADING, align=PP_ALIGN.CENTER, name="Consolas")

    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    create_interface_deck("d:/S2/REINVENT/web_server/Presentasi_REINVENT4_Interface_Style.pptx")

