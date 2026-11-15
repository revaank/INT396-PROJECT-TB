import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_simple_deck(output_filename="TB_Insight_Project_Presentation.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Clean Dark Medical Palette
    BG_DARK = RGBColor(10, 14, 23)        # #0A0E17 Deep Dark Canvas
    CARD_BG = RGBColor(18, 23, 36)        # #121724 Slate Card
    CARD_BORDER = RGBColor(37, 49, 73)    # #253149 Subtle Border
    WHITE = RGBColor(248, 250, 252)       # #F8FAFC Crisp White
    MUTED = RGBColor(156, 171, 192)       # #9CABC0 Easy-to-read Muted Gray
    CYAN = RGBColor(56, 189, 248)         # #38BDF8 Tech Cyan
    EMERALD = RGBColor(16, 185, 129)      # #10B981 Bharat Emerald
    SAFFRON = RGBColor(245, 158, 11)      # #F59E0B Warm Amber
    ROSE = RGBColor(244, 63, 94)          # #F43F5E Rose Accent

    def set_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, eyebrow_text="INT 396 PROJECT · TB INSIGHT"):
        # Eyebrow tag
        eb_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
        tf_eb = eb_box.text_frame
        p_eb = tf_eb.paragraphs[0]
        p_eb.text = eyebrow_text.upper()
        p_eb.font.size = Pt(11)
        p_eb.font.bold = True
        p_eb.font.color.rgb = CYAN

        # Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.6))
        tf_t = t_box.text_frame
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = WHITE

    def add_card(slide, left, top, width, height, bg=CARD_BG, border=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg
        card.line.color.rgb = border
        card.line.width = Pt(1)
        return card

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)

    # Accent line
    bar = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(1.0), Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = SAFFRON
    bar.line.fill.background()

    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(2.2))
    tf1 = t_box.text_frame
    p1 = tf1.paragraphs[0]
    p1.text = "Regional Tuberculosis Clustering in India"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = WHITE

    p2 = tf1.add_paragraph()
    p2.text = "An Interactive Web Platform for State-by-State Healthcare Planning"
    p2.font.size = Pt(19)
    p2.font.color.rgb = CYAN
    p2.space_before = Pt(8)

    add_card(s1, Inches(0.8), Inches(4.3), Inches(11.7), Inches(2.3))
    c_box = s1.shapes.add_textbox(Inches(1.1), Inches(4.5), Inches(11.1), Inches(1.9))
    tf_c = c_box.text_frame

    p_c1 = tf_c.paragraphs[0]
    p_c1.text = "Course Project: INT 396 — Data Science & Machine Learning"
    p_c1.font.size = Pt(15)
    p_c1.font.bold = True
    p_c1.font.color.rgb = WHITE

    bullets_s1 = [
        "What it does: Uses Machine Learning to group Indian states facing similar TB challenges.",
        "What was built: A live, 4-page interactive dashboard with an India map, comparison tool, recovery plans, and helplines.",
        "Live Website: Deployed online with public access for evaluation."
    ]
    for b in bullets_s1:
        p = tf_c.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(13)
        p.font.color.rgb = MUTED
        p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 2: WHY WE BUILT THIS (THE PURPOSE)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_header(s2, "Project Goal: Why Did We Build This?")

    col_w = Inches(3.7)
    gap = Inches(0.3)
    top_pos = Inches(1.6)
    h_pos = Inches(5.2)

    # Box 1
    add_card(s2, Inches(0.8), top_pos, col_w, h_pos)
    tb = s2.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.2), col_w - Inches(0.4), h_pos - Inches(0.4))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "1. The Big Challenge"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ROSE
    for text in [
        "India accounts for over 25% of all TB cases worldwide.",
        "The national government wants to eliminate TB quickly.",
        "However, policies and budgets are often sent out as a single national rule for everyone.",
        "Treating every state the same does not work."
    ]:
        p = tf.add_paragraph()
        p.text = "• " + text
        p.font.size = Pt(13)
        p.font.color.rgb = MUTED
        p.space_before = Pt(10)

    # Box 2
    add_card(s2, Inches(0.8) + col_w + gap, top_pos, col_w, h_pos)
    tb = s2.shapes.add_textbox(Inches(1.0) + col_w + gap, top_pos + Inches(0.2), col_w - Inches(0.4), h_pos - Inches(0.4))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "2. Every State is Different"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = SAFFRON
    for text in [
        "Huge States (like UP): Have millions of patients. Hospitals get overcrowded and testing is delayed.",
        "Southern States (like Kerala): Have high rates of Diabetes + TB co-infection.",
        "Hilly States (like Sikkim): Have fewer cases, but villages are remote and hard to reach.",
        "Sending the same kits to everyone wastes resources."
    ]:
        p = tf.add_paragraph()
        p.text = "• " + text
        p.font.size = Pt(13)
        p.font.color.rgb = MUTED
        p.space_before = Pt(8)

    # Box 3
    add_card(s2, Inches(0.8) + (col_w + gap)*2, top_pos, col_w, h_pos)
    tb = s2.shapes.add_textbox(Inches(1.0) + (col_w + gap)*2, top_pos + Inches(0.2), col_w - Inches(0.4), h_pos - Inches(0.4))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "3. What Our App Does"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    for text in [
        "Uses Machine Learning to automatically group similar states together.",
        "Shows health officers which other states share the exact same problems ('Health Twins').",
        "Gives tailored 90-day action plans and budget advice for each state.",
        "Provides 24/7 helpline access and an AI chatbot for citizens."
    ]:
        p = tf.add_paragraph()
        p.text = "• " + text
        p.font.size = Pt(13)
        p.font.color.rgb = MUTED
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 3: THE DATASET WE USED
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_header(s3, "The Dataset: Official Government Health Data")

    w_half = Inches(5.7)
    add_card(s3, Inches(0.8), Inches(1.6), w_half, Inches(5.2))
    tb_l = s3.shapes.add_textbox(Inches(1.1), Inches(1.8), w_half - Inches(0.6), Inches(4.8))
    tf_l = tb_l.text_frame
    p = tf_l.paragraphs[0]
    p.text = "Dataset Details"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = CYAN

    data_points = [
        ("Source", "Ministry of Health and Family Welfare (MoHFW) / Ni-kshay Portal."),
        ("Geography", "All 36 Indian States and Union Territories."),
        ("Years", "Annual surveillance records from 2019 to 2023."),
        ("Total Rows", "4,995 data rows with 11 health indicators."),
        ("Key Measures", "Annual Cases, Testing Positivity, Treatment Success %, and Diabetes/Tobacco Risk.")
    ]
    for title, val in data_points:
        p = tf_l.add_paragraph()
        p.text = f"{title}: {val}"
        p.font.size = Pt(13)
        p.font.color.rgb = WHITE
        p.space_before = Pt(10)

    add_card(s3, Inches(6.8), Inches(1.6), w_half, Inches(5.2))
    tb_r = s3.shapes.add_textbox(Inches(7.1), Inches(1.8), w_half - Inches(0.6), Inches(4.8))
    tf_r = tb_r.text_frame
    p = tf_r.paragraphs[0]
    p.text = "How We Cleaned and Handled the Data"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = EMERALD

    clean_points = [
        ("No Fake Numbers", "We never made up any missing rows or fake numbers."),
        ("Removed 'All India' Row", "Excluded the national total so it wouldn't skew the state averages."),
        ("Handled Blanks Honestly", "132 missing spots were audited; never filled with zeros unless actually zero."),
        ("Standardized Values", "Used StandardScaler so big population states (like UP) don't overpower small states (like Sikkim)."),
        ("100% Privacy Safe", "Only aggregated state numbers; zero personal medical records.")
    ]
    for title, val in clean_points:
        p = tf_r.add_paragraph()
        p.text = f"✓ {title}: {val}"
        p.font.size = Pt(12.5)
        p.font.color.rgb = MUTED
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 4: HOW WE GROUPED THE STATES (MACHINE LEARNING)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "Machine Learning: Grouping States into 3 Patterns")

    add_card(s4, Inches(0.8), Inches(1.6), w_half, Inches(5.2))
    tb_l = s4.shapes.add_textbox(Inches(1.1), Inches(1.8), w_half - Inches(0.6), Inches(4.8))
    tf_l = tb_l.text_frame
    p = tf_l.paragraphs[0]
    p.text = "Why Hierarchical Clustering?"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = CYAN

    ml_points = [
        "Deterministic (No Random Guessing): Normal K-Means starts randomly and changes answers. Hierarchical clustering gives the exact same result every time.",
        "Ward's Linkage: Merges states that are closest in health behavior, keeping groups tight and clean.",
        "Built-in Tree (Dendrogram): Creates an easy visual tree diagram showing how states link together.",
        "Perfect for 36 States: Clean, stable, and completely understandable for doctors and health officers."
    ]
    for pt in ml_points:
        p = tf_l.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(13)
        p.font.color.rgb = MUTED
        p.space_before = Pt(10)

    add_card(s4, Inches(6.8), Inches(1.6), w_half, Inches(5.2))
    tb_r = s4.shapes.add_textbox(Inches(7.1), Inches(1.8), w_half - Inches(0.6), Inches(4.8))
    tf_r = tb_r.text_frame
    p = tf_r.paragraphs[0]
    p.text = "Why Exactly 3 Groups?"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = SAFFRON

    eval_points = [
        ("Tested 2, 3, 4, and 5 Groups", "We tested different cluster counts to find the mathematical sweet spot."),
        ("Silhouette Score", "Showed highest score at 3 clusters — meaning states are most similar to their own group."),
        ("Davies-Bouldin Score", "Confirmed 3 clusters give the cleanest separation with zero overlap."),
        ("Real-World Sense", "3 clusters cleanly reflect India's actual geography: Big States, Diabetes States, and Hilly States.")
    ]
    for title, val in eval_points:
        p = tf_r.add_paragraph()
        p.text = f"✓ {title}: {val}"
        p.font.size = Pt(12.5)
        p.font.color.rgb = WHITE
        p.space_before = Pt(10)

    # =========================================================================
    # SLIDE 5: THE 3 STATE GROUPS WE FOUND
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "The 3 State Groups Discovered by Machine Learning")

    # 3 Cards
    add_card(s5, Inches(0.8), top_pos, col_w, h_pos)
    tb = s5.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.2), col_w - Inches(0.4), h_pos - Inches(0.4))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "Group 1: High-Volume Giants"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = CYAN
    for line in [
        "States: Uttar Pradesh, Bihar, Madhya Pradesh, West Bengal, Rajasthan.",
        "Problem: Massive patient numbers (>600k in UP).",
        "Bottleneck: Testing takes 7 to 10 days because district labs are jammed.",
        "Recommended Fix: Place Truenat molecular testing machines right in local village clinics."
    ]:
        p = tf.add_paragraph()
        p.text = "• " + line
        p.font.size = Pt(12)
        p.font.color.rgb = MUTED
        p.space_before = Pt(8)

    add_card(s5, Inches(0.8) + col_w + gap, top_pos, col_w, h_pos)
    tb = s5.shapes.add_textbox(Inches(1.0) + col_w + gap, top_pos + Inches(0.2), col_w - Inches(0.4), h_pos - Inches(0.4))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "Group 2: Comorbidity Heavy"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = SAFFRON
    for line in [
        "States: Kerala, Tamil Nadu, Andhra Pradesh, Karnataka, Maharashtra.",
        "Problem: Over 18% of TB patients also have Diabetes.",
        "Bottleneck: High blood sugar delays healing and increases relapse.",
        "Recommended Fix: Combined TB + Diabetes clinics so patients get sugar control alongside TB medicines."
    ]:
        p = tf.add_paragraph()
        p.text = "• " + line
        p.font.size = Pt(12)
        p.font.color.rgb = MUTED
        p.space_before = Pt(8)

    add_card(s5, Inches(0.8) + (col_w + gap)*2, top_pos, col_w, h_pos)
    tb = s5.shapes.add_textbox(Inches(1.0) + (col_w + gap)*2, top_pos + Inches(0.2), col_w - Inches(0.4), h_pos - Inches(0.4))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "Group 3: Mountain & Remote"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    for line in [
        "States: Sikkim, Ladakh, Arunachal Pradesh, Mizoram, A&N Islands.",
        "Problem: Small case numbers, but villages are far apart.",
        "Bottleneck: Transporting test samples over hills takes days.",
        "Recommended Fix: Mobile diagnostic vans and village medicine drop boxes."
    ]:
        p = tf.add_paragraph()
        p.text = "• " + line
        p.font.size = Pt(12)
        p.font.color.rgb = MUTED
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 6: HOW WE BUILT THE APP (TECH STACK)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_header(s6, "Tech Stack: Simple, Fast & Clean")

    l_w = Inches(11.7)
    l_h = Inches(1.55)

    add_card(s6, Inches(0.8), Inches(1.6), l_w, l_h)
    tb = s6.shapes.add_textbox(Inches(1.1), Inches(1.75), l_w - Inches(0.6), l_h - Inches(0.3))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "1. Backend & Data Processing (Python, Pandas, Scikit-learn)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = CYAN
    p1 = tf.add_paragraph()
    p1.text = "• Python: Cleans the government CSV data, removes outliers, and runs the clustering algorithm.\n• Scikit-learn: Runs StandardScaler, Hierarchical Clustering, and PCA."
    p1.font.size = Pt(12.5)
    p1.font.color.rgb = MUTED
    p1.space_before = Pt(3)

    add_card(s6, Inches(0.8), Inches(3.35), l_w, l_h)
    tb = s6.shapes.add_textbox(Inches(1.1), Inches(3.5), l_w - Inches(0.6), l_h - Inches(0.3))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "2. Web Server & Page Routing (Streamlit)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = SAFFRON
    p1 = tf.add_paragraph()
    p1.text = "• Streamlit: Powers the web server and manages links between the 4 pages.\n• Fast, lightweight, and lets anyone open the website directly in their browser."
    p1.font.size = Pt(12.5)
    p1.font.color.rgb = MUTED
    p1.space_before = Pt(3)

    add_card(s6, Inches(0.8), Inches(5.1), l_w, l_h)
    tb = s6.shapes.add_textbox(Inches(1.1), Inches(5.25), l_w - Inches(0.6), l_h - Inches(0.3))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "3. Frontend User Interface (HTML5, Modern CSS, Vector India Map)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    p1 = tf.add_paragraph()
    p1.text = "• Custom Dark Theme: Clean, modern, and easy on the eyes.\n• Interactive Vector Map: Built-in India SVG map that reacts when you click any state."
    p1.font.size = Pt(12.5)
    p1.font.color.rgb = MUTED
    p1.space_before = Pt(3)

    # =========================================================================
    # SLIDE 7: FEATURE 1 - INTERACTIVE INDIA MAP (PHOTO)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_header(s7, "Feature 1: Interactive Regional Map")

    add_card(s7, Inches(0.8), Inches(1.6), Inches(4.5), Inches(5.2))
    tb = s7.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(4.1), Inches(4.8))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "What You Can Do on This Page:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = CYAN

    f1_points = [
        "Visual Map of India: Shows all 36 states colored according to their ML cluster group.",
        "Hover Live Numbers: Move your mouse over any state to see its cases, national rank, and cure rate.",
        "One-Click Filter Buttons: Click 'High-Volume' or 'Comorbidity' to instantly highlight only those states.",
        "Clear & High Contrast: Designed so borders and numbers are instantly visible."
    ]
    for pt in f1_points:
        p = tf.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(12.5)
        p.font.color.rgb = MUTED
        p.space_before = Pt(10)

    # Embedded Screenshot
    img_map = "presentation_assets/slide_map_preview.png"
    if os.path.exists(img_map):
        add_card(s7, Inches(5.6), Inches(1.6), Inches(6.9), Inches(5.2))
        s7.shapes.add_picture(img_map, Inches(5.7), Inches(1.7), Inches(6.7), Inches(5.0))

    # =========================================================================
    # SLIDE 8: FEATURE 2 - STATE COMPARISON TOOL (PHOTO)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8)
    add_header(s8, "Feature 2: State Comparison Tool")

    add_card(s8, Inches(0.8), Inches(1.6), Inches(4.5), Inches(5.2))
    tb = s8.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(4.1), Inches(4.8))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "What You Can Do on This Page:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = SAFFRON

    f2_points = [
        "Pick Any Two States: Select any two states from simple dropdowns (e.g. Uttar Pradesh vs Kerala).",
        "Side-by-Side Cards: Compares their cases, testing percentages, and treatment success rates.",
        "Automatic Difference Calculation: Shows the exact gap between them in simple numbers.",
        "Smart Text Summary: Automatically explains which state is better in testing vs patient recovery."
    ]
    for pt in f2_points:
        p = tf.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(12.5)
        p.font.color.rgb = MUTED
        p.space_before = Pt(10)

    # Embedded Screenshot
    img_comp = "presentation_assets/slide_compare_preview.png"
    if os.path.exists(img_comp):
        add_card(s8, Inches(5.6), Inches(1.6), Inches(6.9), Inches(5.2))
        s8.shapes.add_picture(img_comp, Inches(5.7), Inches(1.7), Inches(6.7), Inches(5.0))

    # =========================================================================
    # SLIDE 9: FEATURE 3 - TREATMENT & RECOVERY PLANS (PHOTO)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9)
    add_header(s9, "Feature 3: Treatment & Recovery Plans")

    add_card(s9, Inches(0.8), Inches(1.6), Inches(4.5), Inches(5.2))
    tb = s9.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(4.1), Inches(4.8))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "What You Can Do on This Page:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = EMERALD

    f3_points = [
        "Finds the Root Problem: Identifies the exact #1 bottleneck holding back the selected state.",
        "Health Twin State: Tells officials which other state had this problem and how they fixed it.",
        "Smart Budget Advice: Suggests where health funds should be spent (labs vs medicines vs nutrition).",
        "90-Day Action Checklist: A simple, month-by-month plan for district officers and doctors."
    ]
    for pt in f3_points:
        p = tf.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(12.5)
        p.font.color.rgb = MUTED
        p.space_before = Pt(10)

    # Embedded Screenshot
    img_over = "presentation_assets/slide_overcome_preview.png"
    if os.path.exists(img_over):
        add_card(s9, Inches(5.6), Inches(1.6), Inches(6.9), Inches(5.2))
        s9.shapes.add_picture(img_over, Inches(5.7), Inches(1.7), Inches(6.7), Inches(5.0))

    # =========================================================================
    # SLIDE 10: FEATURE 4 - HELPLINES & AI ASSISTANT (PHOTO)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_bg(s10)
    add_header(s10, "Feature 4: Helplines & AI Care Assistant")

    add_card(s10, Inches(0.8), Inches(1.6), Inches(4.5), Inches(5.2))
    tb = s10.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(4.1), Inches(4.8))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "What You Can Do on This Page:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = CYAN

    f4_points = [
        "National 24×7 Toll-Free Helpline: One-click call to Ni-kshay Lifeline (1800-11-6666) + 1075 / 104 / 108.",
        "Free Care Guarantee: Shows free diagnosis, free medicines, and the updated ₹1,000/month nutrition cash scheme (doubled in Oct 2024).",
        "State Officer Directory: Direct phone numbers and official health portals for all 36 States/UTs.",
        "Highlighted AI Chatbot: Instant answers to patient questions about symptoms and testing centers."
    ]
    for pt in f4_points:
        p = tf.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(12)
        p.font.color.rgb = MUTED
        p.space_before = Pt(8)

    # Embedded Screenshot
    img_know = "presentation_assets/slide_knowledge_preview.png"
    if os.path.exists(img_know):
        add_card(s10, Inches(5.6), Inches(1.6), Inches(6.9), Inches(5.2))
        s10.shapes.add_picture(img_know, Inches(5.7), Inches(1.7), Inches(6.7), Inches(5.0))

    # =========================================================================
    # SLIDE 11: PROJECT LINKS & SUBMISSION
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_bg(s11)
    add_header(s11, "Project Submission: Live Links & Verification")

    l_w = Inches(11.7)
    add_card(s11, Inches(0.8), Inches(1.6), l_w, Inches(1.5))
    tb = s11.shapes.add_textbox(Inches(1.1), Inches(1.75), l_w - Inches(0.6), Inches(1.2))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "1. GitHub Repository (Complete Source Code)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = CYAN
    p1 = tf.add_paragraph()
    p1.text = "https://github.com/revaank/INT396-PROJECT-TB"
    p1.font.size = Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.space_before = Pt(3)
    p2 = tf.add_paragraph()
    p2.text = "• Fully public repository with complete commit history, modular Python code, unit tests, and thorough README."
    p2.font.size = Pt(11.5)
    p2.font.color.rgb = MUTED

    add_card(s11, Inches(0.8), Inches(3.3), l_w, Inches(1.5))
    tb = s11.shapes.add_textbox(Inches(1.1), Inches(3.45), l_w - Inches(0.6), Inches(1.2))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "2. Live Deployed Web Application (Interactive Platform)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    p1 = tf.add_paragraph()
    p1.text = "https://tb-insight-india.streamlit.app/"
    p1.font.size = Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.space_before = Pt(3)
    p2 = tf.add_paragraph()
    p2.text = "• Live HTTPS link accessible on any phone or laptop worldwide. Runs all 4 interactive pages."
    p2.font.size = Pt(11.5)
    p2.font.color.rgb = MUTED

    add_card(s11, Inches(0.8), Inches(5.0), l_w, Inches(1.5))
    tb = s11.shapes.add_textbox(Inches(1.1), Inches(5.15), l_w - Inches(0.6), Inches(1.2))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "3. Official Dataset & Source Link (Ni-kshay & MoHFW)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = SAFFRON
    p1 = tf.add_paragraph()
    p1.text = "Ni-kshay National TB Surveillance Portal: https://www.nikshay.in"
    p1.font.size = Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.space_before = Pt(3)
    p2 = tf.add_paragraph()
    p2.text = "• Annual State Surveillance Reports: Central TB Division, MoHFW (https://tbcindia.mohfw.gov.in)."
    p2.font.size = Pt(11.5)
    p2.font.color.rgb = MUTED

    prs.save(output_filename)
    print(f"Successfully generated simple {output_filename} with {len(prs.slides)} slides!")

if __name__ == "__main__":
    out = "TB_Insight_Project_Presentation.pptx"
    if len(sys.argv) > 1:
        out = sys.argv[1]
    create_simple_deck(out)
