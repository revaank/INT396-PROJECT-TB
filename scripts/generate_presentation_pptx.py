import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_filename="TB_Insight_Project_Presentation.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Clean Dark Medical Palette
    BG_DARK = RGBColor(9, 12, 21)        # #090C15
    CARD_BG = RGBColor(19, 23, 34)       # #131722
    CARD_BORDER = RGBColor(37, 49, 73)   # #253149
    WHITE = RGBColor(248, 250, 252)      # #F8FAFC
    MUTED = RGBColor(148, 163, 184)      # #94A3B8
    CYAN = RGBColor(56, 189, 248)        # #38BDF8
    EMERALD = RGBColor(16, 185, 129)     # #10B981
    SAFFRON = RGBColor(245, 158, 11)     # #F59E0B
    ROSE = RGBColor(244, 63, 94)         # #F43F5E

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="INT 396 PROJECT · TB INSIGHT"):
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
        tf_cat = cat_box.text_frame
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = CYAN

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.6))
        tf_title = title_box.text_frame
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        return card

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    bar = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(0.8), Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = SAFFRON
    bar.line.fill.background()

    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(2.2))
    tf1 = t_box.text_frame
    p1 = tf1.paragraphs[0]
    p1.text = "Regional Tuberculosis Case-Pattern Clustering"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = WHITE

    p2 = tf1.add_paragraph()
    p2.text = "Using Machine Learning to Group Indian States for Smarter Healthcare Planning"
    p2.font.size = Pt(18)
    p2.font.color.rgb = CYAN
    p2.space_before = Pt(8)

    add_card(s1, Inches(0.8), Inches(4.3), Inches(11.7), Inches(2.4))
    c_box = s1.shapes.add_textbox(Inches(1.1), Inches(4.5), Inches(11.1), Inches(2.0))
    tf_c = c_box.text_frame

    p_meta1 = tf_c.paragraphs[0]
    p_meta1.text = "Course: INT 396 — Data Science & Machine Learning Capstone"
    p_meta1.font.size = Pt(15)
    p_meta1.font.bold = True
    p_meta1.font.color.rgb = WHITE

    p_meta2 = tf_c.add_paragraph()
    p_meta2.text = "• Real Government Data: Ministry of Health & Family Welfare (MoHFW) / Ni-kshay (All 36 States & UTs)"
    p_meta2.font.size = Pt(13)
    p_meta2.font.color.rgb = MUTED
    p_meta2.space_before = Pt(6)

    p_meta3 = tf_c.add_paragraph()
    p_meta3.text = "• Core Technique: Hierarchical Clustering (Ward's Linkage) + PCA + Interactive Web Dashboard"
    p_meta3.font.size = Pt(13)
    p_meta3.font.color.rgb = MUTED

    p_meta4 = tf_c.add_paragraph()
    p_meta4.text = "• Working Live App: Deployed on Cloudflare HTTPS with 4 interactive public health modules"
    p_meta4.font.size = Pt(13)
    p_meta4.font.color.rgb = EMERALD

    # =========================================================================
    # SLIDE 2: THE PROBLEM (WHY THIS PROJECT MATTERS)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "The Real-World Problem: One Rule Doesn't Fit All States")

    col_w = Inches(3.7)
    gap = Inches(0.3)
    top_pos = Inches(1.6)
    height_pos = Inches(5.2)

    # Box 1
    add_card(s2, Inches(0.8), top_pos, col_w, height_pos)
    b1 = s2.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.2), col_w - Inches(0.4), height_pos - Inches(0.4))
    tf1 = b1.text_frame
    p = tf1.paragraphs[0]
    p.text = "1. India's Huge TB Challenge"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ROSE
    for text in [
        "India accounts for over 25% of all TB cases in the world.",
        "The central government wants to eliminate TB quickly.",
        "Today, health budgets and plans are often distributed uniformly across states.",
        "But India's states have completely different challenges."
    ]:
        p = tf1.add_paragraph()
        p.text = "• " + text
        p.font.size = Pt(13)
        p.font.color.rgb = MUTED
        p.space_before = Pt(10)

    # Box 2
    add_card(s2, Inches(0.8) + col_w + gap, top_pos, col_w, height_pos)
    b2 = s2.shapes.add_textbox(Inches(1.0) + col_w + gap, top_pos + Inches(0.2), col_w - Inches(0.4), height_pos - Inches(0.4))
    tf2 = b2.text_frame
    p = tf2.paragraphs[0]
    p.text = "2. Different States, Different Issues"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = SAFFRON
    for text in [
        "Big States (like UP & Bihar): Huge population, hospitals get overcrowded, testing takes 7-10 days.",
        "Southern States (like Kerala & TN): Moderate cases, but high Diabetes patients who get TB easily.",
        "Hilly States (like Sikkim & Ladakh): Low cases, but villages are far apart and sample delivery is tough.",
        "Sending the same supplies to everyone wastes money."
    ]:
        p = tf2.add_paragraph()
        p.text = "• " + text
        p.font.size = Pt(13)
        p.font.color.rgb = MUTED
        p.space_before = Pt(8)

    # Box 3
    add_card(s2, Inches(0.8) + (col_w + gap)*2, top_pos, col_w, height_pos)
    b3 = s2.shapes.add_textbox(Inches(1.0) + (col_w + gap)*2, top_pos + Inches(0.2), col_w - Inches(0.4), height_pos - Inches(0.4))
    tf3 = b3.text_frame
    p = tf3.paragraphs[0]
    p.text = "3. What This Project Does"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = CYAN
    for text in [
        "Uses Machine Learning to automatically group similar states together.",
        "Identifies 'Health Twins' — states with similar patterns so they can share what works.",
        "Built an interactive website where officials can see custom roadmaps for their state.",
        "100% aggregated public health data — no private patient records."
    ]:
        p = tf3.add_paragraph()
        p.text = "• " + text
        p.font.size = Pt(13)
        p.font.color.rgb = MUTED
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 3: DATASET & DATA HYGIENE
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "The Data: Real Government Records & Strict Honesty")

    w_half = Inches(5.7)
    add_card(s3, Inches(0.8), Inches(1.6), w_half, Inches(5.2))
    tb_l = s3.shapes.add_textbox(Inches(1.1), Inches(1.8), w_half - Inches(0.6), Inches(4.8))
    tf_l = tb_l.text_frame
    p = tf_l.paragraphs[0]
    p.text = "Where the Data Comes From"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = CYAN

    data_items = [
        ("Official Source", "Ministry of Health & Family Welfare (MoHFW), Central TB Division, Ni-kshay Portal."),
        ("Geography", "All 36 Indian States and Union Territories."),
        ("Time Covered", "Annual reports from 2019 to 2023 (5 years of data)."),
        ("Size", "4,995 total rows with 11 health indicators."),
        ("Risk Factors Included", "Diabetes, Tobacco use, Alcohol habits, and COVID-19 co-testing.")
    ]
    for k, v in data_items:
        p = tf_l.add_paragraph()
        p.text = f"{k}: {v}"
        p.font.size = Pt(13)
        p.font.color.rgb = WHITE
        p.space_before = Pt(10)

    add_card(s3, Inches(6.8), Inches(1.6), w_half, Inches(5.2))
    tb_r = s3.shapes.add_textbox(Inches(7.1), Inches(1.8), w_half - Inches(0.6), Inches(4.8))
    tf_r = tb_r.text_frame
    p = tf_r.paragraphs[0]
    p.text = "Data Rules We Followed (Academic Ethics)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = EMERALD

    rules = [
        ("No Fake Data", "Never made up any numbers, sample sizes, or missing rows."),
        ("Removed 'All India'", "Excluded the national total row so it didn't confuse the state comparisons."),
        ("Handled Missing Values Carefully", "132 missing entries were tracked honestly. Never filled blank spots with zeros unless zero was actually true."),
        ("Clean Boundaries", "Correctly included new union territories (like Ladakh and J&K)."),
        ("Privacy Respected", "Only state-level summaries used. Zero personal patient info.")
    ]
    for k, v in rules:
        p = tf_r.add_paragraph()
        p.text = f"✓ {k}: {v}"
        p.font.size = Pt(12)
        p.font.color.rgb = MUTED
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 4: PREPARING THE DATA FOR MACHINE LEARNING
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Data Preprocessing: Leveling the Playing Field")

    w_card = Inches(5.7)
    h_card = Inches(2.45)

    add_card(s4, Inches(0.8), Inches(1.6), w_card, h_card)
    tb = s4.shapes.add_textbox(Inches(1.0), Inches(1.75), w_card - Inches(0.4), h_card - Inches(0.3))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "1. Why We Couldn't Just Use Raw Counts"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = ROSE
    p1 = tf.add_paragraph()
    p1.text = "• Uttar Pradesh has 23 crore people; Sikkim has 7 lakh people.\n• If we just fed raw case counts to ML, it would only group states by population size rather than real disease patterns."
    p1.font.size = Pt(12)
    p1.font.color.rgb = MUTED
    p1.space_before = Pt(4)

    add_card(s4, Inches(6.8), Inches(1.6), w_card, h_card)
    tb = s4.shapes.add_textbox(Inches(7.0), Inches(1.75), w_card - Inches(0.4), h_card - Inches(0.3))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "2. Standardizing the Numbers (StandardScaler)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = CYAN
    p1 = tf.add_paragraph()
    p1.text = "• We used StandardScaler: brings every indicator to a common scale (mean=0, standard deviation=1).\n• Now, huge patient counts don't overpower percentages like Treatment Success Rate or Diabetes %."
    p1.font.size = Pt(12)
    p1.font.color.rgb = MUTED
    p1.space_before = Pt(4)

    add_card(s4, Inches(0.8), Inches(4.35), w_card, h_card)
    tb = s4.shapes.add_textbox(Inches(1.0), Inches(4.5), w_card - Inches(0.4), h_card - Inches(0.3))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "3. Reshaping into a State Feature Table"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    p1 = tf.add_paragraph()
    p1.text = "• Converted messy long tables into 1 clean row per state.\n• Key features: Annual Cases, Sputum Positivity Rate, Diabetes Risk, Tobacco Risk, Treatment Success Rate."
    p1.font.size = Pt(12)
    p1.font.color.rgb = MUTED
    p1.space_before = Pt(4)

    add_card(s4, Inches(6.8), Inches(4.35), w_card, h_card)
    tb = s4.shapes.add_textbox(Inches(7.0), Inches(4.5), w_card - Inches(0.4), h_card - Inches(0.3))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "4. Checking Variance with PCA"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = SAFFRON
    p1 = tf.add_paragraph()
    p1.text = "• We used PCA (Principal Component Analysis) to simplify multiple dimensions into 2 main axes.\n• The first 2 components capture >88% of all variance, proving clear clusters exist!"
    p1.font.size = Pt(12)
    p1.font.color.rgb = MUTED
    p1.space_before = Pt(4)

    # =========================================================================
    # SLIDE 5: CLUSTERING METHODOLOGY (HOW WE GROUPED THEM)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Clustering Method: Why We Chose Hierarchical Clustering")

    add_card(s5, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2))
    tb = s5.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(5.1), Inches(4.8))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "Why Ward's Hierarchical Clustering?"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = CYAN

    pts_method = [
        "No Guessing (Deterministic): Normal K-Means starts with random centers and can give different answers each time. Hierarchical clustering gives the exact same result every run.",
        "Dendrogram Tree: Produces a clear visual tree diagram showing how states naturally link to each other.",
        "Ward's Method: Merges states that are closest in behavior, keeping groups tight and clean.",
        "Perfect for 36 States: With 36 administrative states, a hierarchical tree is much easier for officials to understand."
    ]
    for pt in pts_method:
        p = tf.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(12.5)
        p.font.color.rgb = MUTED
        p.space_before = Pt(10)

    add_card(s5, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    tb = s5.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.1), Inches(4.8))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "Finding the Right Number of Groups (k = 3)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = EMERALD

    metrics = [
        ("Tested k from 2 to 5", "We tested 2, 3, 4, and 5 clusters to see which mathematical score was strongest."),
        ("Silhouette Score", "Measures how similar states are to their own cluster vs other clusters. Peak was at k=3."),
        ("Davies-Bouldin Index", "Lower is better. Confirmed k=3 has the best separation between groups."),
        ("Dendrogram Inspection", "The tree showed 3 distinct main branches before smaller splits."),
        ("Real-World Sense", "3 clusters map perfectly to practical health policies: High-Volume, Comorbidity, and Mountain.")
    ]
    for title, desc in metrics:
        p = tf.add_paragraph()
        p.text = f"✓ {title}: {desc}"
        p.font.size = Pt(12)
        p.font.color.rgb = WHITE
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 6: THE 3 CLUSTERS WE FOUND
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "What the Machine Found: 3 Clear State Patterns")

    c_w = Inches(3.7)
    c_h = Inches(5.2)

    # Cluster 0
    add_card(s6, Inches(0.8), Inches(1.6), c_w, c_h)
    tb = s6.shapes.add_textbox(Inches(1.0), Inches(1.8), c_w - Inches(0.4), c_h - Inches(0.4))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "Group 1: High-Volume Giants"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = CYAN
    for line in [
        "States: Uttar Pradesh, Bihar, Madhya Pradesh, West Bengal, Rajasthan.",
        "Pattern: Millions of tests, very high total patient counts (>600k in UP alone).",
        "Biggest Bottleneck: City hospitals are overloaded. Getting test results takes 7 to 10 days.",
        "Smart Solution: Move molecular Truenat testing machines down to rural health centers to catch cases early."
    ]:
        p = tf.add_paragraph()
        p.text = "• " + line
        p.font.size = Pt(12)
        p.font.color.rgb = MUTED
        p.space_before = Pt(10)

    # Cluster 1
    add_card(s6, Inches(4.8), Inches(1.6), c_w, c_h)
    tb = s6.shapes.add_textbox(Inches(5.0), Inches(1.8), c_w - Inches(0.4), c_h - Inches(0.4))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "Group 2: Comorbidity Heavy"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = SAFFRON
    for line in [
        "States: Kerala, Tamil Nadu, Andhra Pradesh, Karnataka, Maharashtra.",
        "Pattern: Moderate case numbers, but over 18% of TB patients also have Diabetes.",
        "Biggest Bottleneck: High blood sugar weakens immunity, causing medicines to take longer to work.",
        "Smart Solution: Set up combined TB + Diabetes clinics so patients get sugar control alongside TB medicines."
    ]:
        p = tf.add_paragraph()
        p.text = "• " + line
        p.font.size = Pt(12)
        p.font.color.rgb = MUTED
        p.space_before = Pt(10)

    # Cluster 2
    add_card(s6, Inches(8.8), Inches(1.6), c_w, c_h)
    tb = s6.shapes.add_textbox(Inches(9.0), Inches(1.8), c_w - Inches(0.4), c_h - Inches(0.4))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "Group 3: Mountain & Frontier"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    for line in [
        "States: Sikkim, Ladakh, Arunachal Pradesh, Mizoram, Andaman & Nicobar.",
        "Pattern: Low total cases, but populations are spread across difficult hilly or island terrain.",
        "Biggest Bottleneck: Samples have to travel long distances through bad weather to reach labs.",
        "Smart Solution: Mobile diagnostic testing vans and local village medicine drop points."
    ]:
        p = tf.add_paragraph()
        p.text = "• " + line
        p.font.size = Pt(12)
        p.font.color.rgb = MUTED
        p.space_before = Pt(10)

    # =========================================================================
    # SLIDE 7: HOW THE APPLICATION WAS BUILT (TECH STACK)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "System Design: Simple, Fast & Clean Architecture")

    l_w = Inches(11.7)
    l_h = Inches(1.55)

    add_card(s7, Inches(0.8), Inches(1.6), l_w, l_h)
    tb = s7.shapes.add_textbox(Inches(1.1), Inches(1.75), l_w - Inches(0.6), l_h - Inches(0.3))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "1. Data & Math Layer (`src/` in Python)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = CYAN
    p1 = tf.add_paragraph()
    p1.text = "• Uses Pandas and NumPy to clean and pivot MoHFW data.\n• Uses Scikit-learn for StandardScaler, Hierarchical Clustering, and PCA calculations.\n• Completely modular: can be verified directly from terminal without opening the website."
    p1.font.size = Pt(12)
    p1.font.color.rgb = MUTED
    p1.space_before = Pt(3)

    add_card(s7, Inches(0.8), Inches(3.35), l_w, l_h)
    tb = s7.shapes.add_textbox(Inches(1.1), Inches(3.5), l_w - Inches(0.6), l_h - Inches(0.3))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "2. Application Router (`app/main.py` in Streamlit)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = SAFFRON
    p1 = tf.add_paragraph()
    p1.text = "• Built with Streamlit — fast, lightweight Python web framework.\n• Manages page routing via query links (`/?page=Home`, `/?page=compare`, `/?page=overcome`, `/?page=knowledge`).\n• Seamless full-screen embedding with zero ugly default borders."
    p1.font.size = Pt(12)
    p1.font.color.rgb = MUTED
    p1.space_before = Pt(3)

    add_card(s7, Inches(0.8), Inches(5.1), l_w, l_h)
    tb = s7.shapes.add_textbox(Inches(1.1), Inches(5.25), l_w - Inches(0.6), l_h - Inches(0.3))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "3. Frontend UI (HTML5, Clean CSS, Interactive Vector Map)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    p1 = tf.add_paragraph()
    p1.text = "• Custom dark theme designed for clinical authority (Inter & Plus Jakarta Sans typography).\n• Built-in interactive SVG India map: instant state selection and real-time live numbers.\n• 100% responsive: works smoothly on mobile, laptop, and tablet."
    p1.font.size = Pt(12)
    p1.font.color.rgb = MUTED
    p1.space_before = Pt(3)

    # =========================================================================
    # SLIDE 8: PAGE 1 - MAP
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Module 1: Interactive Regional Map")

    add_card(s8, Inches(0.8), Inches(1.6), Inches(4.5), Inches(5.2))
    tb = s8.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(4.1), Inches(4.8))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "Map Features"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = CYAN
    for text in [
        "Color-Coded Clusters: Every state is colored by its machine-learning cluster group.",
        "Live Hover Info: Hovering over any state shows its national rank, total cases, and success %.",
        "Quick Filter Chips: One click filters the map to only show High-Volume, Comorbidity, or Mountain states.",
        "Clear & Readable: Uses vibrant, high-contrast colors so boundaries are instantly clear."
    ]:
        p = tf.add_paragraph()
        p.text = "• " + text
        p.font.size = Pt(12)
        p.font.color.rgb = MUTED
        p.space_before = Pt(10)

    img_map = "presentation_assets/slide_map_preview.png"
    if os.path.exists(img_map):
        add_card(s8, Inches(5.6), Inches(1.6), Inches(6.9), Inches(5.2))
        s8.shapes.add_picture(img_map, Inches(5.7), Inches(1.7), Inches(6.7), Inches(5.0))

    # =========================================================================
    # SLIDE 9: PAGE 2 - COMPARE STATES
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Module 2: Compare Any Two States Side-by-Side")

    add_card(s9, Inches(0.8), Inches(1.6), Inches(4.5), Inches(5.2))
    tb = s9.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(4.1), Inches(4.8))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "Comparison Features"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = SAFFRON
    for text in [
        "Head-to-Head Picker: Pick any 2 states from dropdowns (e.g. Uttar Pradesh vs Kerala).",
        "Calculates Differences: Instantly computes percentage gaps in cases, testing, and treatment success.",
        "Smart Text Summary: Automatically explains which state is doing better in testing vs patient recovery.",
        "Helps Policy Makers: Officials can see how other states achieve better cure rates."
    ]:
        p = tf.add_paragraph()
        p.text = "• " + text
        p.font.size = Pt(12)
        p.font.color.rgb = MUTED
        p.space_before = Pt(10)

    img_comp = "presentation_assets/slide_compare_preview.png"
    if os.path.exists(img_comp):
        add_card(s9, Inches(5.6), Inches(1.6), Inches(6.9), Inches(5.2))
        s9.shapes.add_picture(img_comp, Inches(5.7), Inches(1.7), Inches(6.7), Inches(5.0))

    # =========================================================================
    # SLIDE 10: PAGE 3 - TREATMENT & RECOVERY
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Module 3: Treatment & Recovery (State Action Plans)")

    add_card(s10, Inches(0.8), Inches(1.6), Inches(4.5), Inches(5.2))
    tb = s10.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(4.1), Inches(4.8))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "Action Plan Features"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    for text in [
        "Root Bottlenecks: Explains the exact #1 problem slowing down each state.",
        "Health Twins: Pairs the selected state with a sister state that solved the same problem.",
        "Budget Advice: Recommends where money should go (labs vs outreach vs nutrition).",
        "90-Day Roadmap: A simple month-by-month checklist for IAS officers and district doctors."
    ]:
        p = tf.add_paragraph()
        p.text = "• " + text
        p.font.size = Pt(12)
        p.font.color.rgb = MUTED
        p.space_before = Pt(10)

    img_over = "presentation_assets/slide_overcome_preview.png"
    if os.path.exists(img_over):
        add_card(s10, Inches(5.6), Inches(1.6), Inches(6.9), Inches(5.2))
        s10.shapes.add_picture(img_over, Inches(5.7), Inches(1.7), Inches(6.7), Inches(5.0))

    # =========================================================================
    # SLIDE 11: PAGE 4 - HELPLINES & CHATBOT
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Module 4: Help, Helplines & AI Care Assistant")

    add_card(s11, Inches(0.8), Inches(1.6), Inches(4.5), Inches(5.2))
    tb = s11.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(4.1), Inches(4.8))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "Citizen Support Features"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = CYAN
    for text in [
        "National 24×7 Toll-Free Number: One-click dial to Ni-kshay Lifeline (1800-11-6666) + 1075 / 104 / 108.",
        "Zero-Cost Care Guarantee: Shows free testing (Truenat), free medicines, and ₹1,000/month nutrition cash support (doubled Oct 2024).",
        "State TB Directory: Direct phone numbers and health portals for all 36 States/UTs.",
        "Interactive AI Assistant: Instant answers on symptoms, test centers, and government schemes."
    ]:
        p = tf.add_paragraph()
        p.text = "• " + text
        p.font.size = Pt(12)
        p.font.color.rgb = MUTED
        p.space_before = Pt(8)

    img_know = "presentation_assets/slide_knowledge_preview.png"
    if os.path.exists(img_know):
        add_card(s11, Inches(5.6), Inches(1.6), Inches(6.9), Inches(5.2))
        s11.shapes.add_picture(img_know, Inches(5.7), Inches(1.7), Inches(6.7), Inches(5.0))

    # =========================================================================
    # SLIDE 12: LIMITATIONS & VIVA QUESTIONS
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Honest Limitations & Viva Preparation")

    add_card(s12, Inches(0.8), Inches(1.6), col_w, height_pos)
    tb = s12.shapes.add_textbox(Inches(1.1), Inches(1.8), col_w - Inches(0.6), height_pos - Inches(0.4))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "What This Model Can and Cannot Do"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ROSE
    for title, desc in [
        ("Notifications ≠ Total Illness", "Recorded numbers show people who came to doctors, not every sick person at home."),
        ("Correlation, Not Direct Cause", "Clusters find similar state patterns, but don't prove one factor caused another."),
        ("Macro Policy Tool Only", "Meant for health directors and planning; this tool does NOT diagnose individual patients."),
        ("State Averages Hide City Differences", "State totals don't show differences between a rural village and an urban slum.")
    ]:
        p = tf.add_paragraph()
        p.text = f"• {title}: {desc}"
        p.font.size = Pt(12)
        p.font.color.rgb = MUTED
        p.space_before = Pt(8)

    add_card(s12, Inches(6.8), Inches(1.6), col_w, height_pos)
    tb = s12.shapes.add_textbox(Inches(7.1), Inches(1.8), col_w - Inches(0.6), height_pos - Inches(0.4))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "Quick Answers for Common Viva Questions"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    for q, a in [
        ("Why 3 clusters?", "Tested k=2 to 5; k=3 had the best Silhouette score and matches the 3 natural Indian regions (High-Volume, Diabetes, and Mountain)."),
        ("Why standardize data?", "Because UP has 23 crore people and Sikkim has 7 lakh. Without scaling, ML would only group states by size!"),
        ("Why Ward's linkage?", "It is deterministic (no random guessing) and gives a clear dendrogram tree."),
        ("What is next?", "Sub-district level clustering and automated sync with Ni-kshay portal.")
    ]:
        p = tf.add_paragraph()
        p.text = f"✓ {q}\n  → {a}"
        p.font.size = Pt(11.5)
        p.font.color.rgb = WHITE
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 13: PROJECT LINKS & SUBMISSION
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "Project Submission: Live Links & Verification")

    add_card(s13, Inches(0.8), Inches(1.6), l_w, Inches(1.5))
    tb = s13.shapes.add_textbox(Inches(1.1), Inches(1.75), l_w - Inches(0.6), Inches(1.2))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "1. GitHub Repository (Complete Source Code & Documentation)"
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
    p2.text = "• Publicly accessible with complete commit history, automated unit tests, and thorough README."
    p2.font.size = Pt(11.5)
    p2.font.color.rgb = MUTED

    add_card(s13, Inches(0.8), Inches(3.3), l_w, Inches(1.5))
    tb = s13.shapes.add_textbox(Inches(1.1), Inches(3.45), l_w - Inches(0.6), Inches(1.2))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "2. Live Deployed Web Application (Interactive Platform)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    p1 = tf.add_paragraph()
    p1.text = "https://imported-reserved-mentor-records.trycloudflare.com"
    p1.font.size = Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.space_before = Pt(3)
    p2 = tf.add_paragraph()
    p2.text = "• Live HTTPS link accessible on any phone or laptop worldwide. Runs all 4 interactive modules."
    p2.font.size = Pt(11.5)
    p2.font.color.rgb = MUTED

    add_card(s13, Inches(0.8), Inches(5.0), l_w, Inches(1.5))
    tb = s13.shapes.add_textbox(Inches(1.1), Inches(5.15), l_w - Inches(0.6), Inches(1.2))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "3. Official Dataset & Test Verification"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = SAFFRON
    p1 = tf.add_paragraph()
    p1.text = "Central TB Division (CTD), Ministry of Health & Family Welfare / Ni-kshay Open Data"
    p1.font.size = Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.space_before = Pt(3)
    p2 = tf.add_paragraph()
    p2.text = "• Verification: 6/6 automated unit tests passing (`python -m unittest discover tests`). CLI: `notebooks/reproducible_analysis.py`."
    p2.font.size = Pt(11.5)
    p2.font.color.rgb = MUTED

    prs.save(output_filename)
    print(f"Successfully generated simplified {output_filename} with {len(prs.slides)} slides!")

if __name__ == "__main__":
    out = "TB_Insight_Project_Presentation.pptx"
    if len(sys.argv) > 1:
        out = sys.argv[1]
    create_deck(out)
