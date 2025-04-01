import streamlit as st
import json
import pandas as pd
import io
import xlsxwriter
import altair as alt
import plotly.graph_objects as go  # For the UI radar chart

###############################################################################
# 1. Constants & Configuration
###############################################################################

PHASES = ["Plan & Design", "Implement", "Operate & Improve"]

# Maturity level details with descriptions
MATURITY_LEVELS_DETAILS = {
    "1": [
        "AI implementation is experimental with no structured approach.",
        "AI models are built in isolation with no integration.",
        "AI processes are inconsistent and lack standardization.",
        "Processes are seen as unpredictable, poorly controlled, and reactive.",
        "Capability limited to a few individuals.",
        "Success is based on individual competence."
    ],
    "2": [
        "Some AI processes are repeatable but vary across teams.",
        "AI is used in specific functions with minimal cross-discipline collaboration.",
        "Limited AI governance and standardization exist.",
        "Teams establish the processes. Little cross-discipline activity.",
        "Processes are characterized by projects and are frequently reactive.",
        "Limited but growing capabilities.",
        "Capabilities developed and adopted but limited to a project."
    ],
    "3": [
        "AI strategies and governance frameworks are well-documented.",
        "AI adoption is organization-wide with standard AI best practices.",
        "AI models are consistently optimized and monitored.",
        "Process defined and documented, and consistently followed across the organization.",
        "Defined goals and standardized processes and tools.",
        "Capabilities developed and adopted.",
        "Capabilities used to deliver service.",
        "Synergy amongst disciplines is leveraged."
    ],
    "4": [
        "AI is integrated into business processes with measurable KPIs.",
        "AI-driven automation improves operational efficiency.",
        "Ethical AI frameworks and compliance measures are in place.",
        "Capabilities are well developed and practiced with appropriate governance.",
        "Methodologies, tools, and templates are readily available.",
        "Processes are measured and controlled with KPIs.",
        "Core skillsets and dedicated teams available.",
        "Organization uses quantitative data for service development."
    ],
    "5": [
        "AI is a key driver of business innovation and growth.",
        "AI models are continuously improved with real-time feedback.",
        "AI governance ensures ethical, fair, and explainable AI.",
        "Improvement methodologies are implemented.",
        "Metrics and KPIs are regularly monitored.",
        "New value propositions developed based on competitive landscape.",
        "Anticipates technology and industry trends.",
        "Creative and collaborative culture.",
        "Processes are stable and flexible."
    ]
}

# Maturity level names
MATURITY_LEVEL_NAMES = {
    "1": "Adhoc",
    "2": "Repeatable",
    "3": "Defined",
    "4": "Optimized",
    "5": "Innovative"
}

# Categories and domains
CATEGORIES = {
    "Business": [
        "AI Discovery & Use Case Development",
        "AI Strategy & Governance",
        "Cost Management and Workload Optimization"
    ],
    "Process": [
        "AI Infrastructure & Compute",
        "AI Model Development & Experimentation",
        "AI Deployment & MLOps",
        "AI Governance & Compliance",
        "AI Bias Detection & Ethical AI"
    ],
    "Tools": [
        "AI Performance Optimization",
        "AI Automation and Monitoring"
    ]
}

# Color mapping for maturity levels
MATURITY_COLORS = {
    1: '#F08080',  # Adhoc (Light Red)
    2: '#F4A460',  # Repeatable (Sandy Brown)
    3: '#FFFF99',  # Defined (Light Yellow)
    4: '#90EE90',  # Optimized (Light Green)
    5: '#98FB98'   # Innovative (Pale Green)
}

###############################################################################
# 2. Session State & Setup
###############################################################################

def init_session_state():
    """Initialize session state variables."""
    if "current_domain_index" not in st.session_state:
        st.session_state.current_domain_index = 0
    if "results" not in st.session_state:
        st.session_state.results = []
    if "show_results" not in st.session_state:
        st.session_state.show_results = False
    if "assessment_data" not in st.session_state:
        st.session_state.assessment_data = {}
    if "partner_name" not in st.session_state:
        st.session_state.partner_name = ""
    if "domain_states" not in st.session_state:
        st.session_state.domain_states = {}

def load_config():
    """Load configuration from JSON file."""
    with open('ai_maturity_framework_final.json', 'r') as f:
        return json.load(f)

def setup_page():
    """Configure page settings and styling."""
    st.set_page_config(
        page_title="AI Maturity Assessment",
        page_icon="ISSI_logo.png",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    apply_custom_styling()
    st.image("ISSI_logo.png", width=180)
    st.title("🚀 AI Maturity Assessment and Gap Analysis")

def apply_custom_styling():
    """Apply custom CSS styling."""
    st.markdown("""
        <style>
            :root {
                --primary-color: #003366;
                --secondary-color: #0066cc;
                --background-color: #f5f7fa;
                --text-color: #333333;
                --card-background: #ffffff;
            }
            
            .stApp {
                background-color: var(--background-color) !important;
            }
            
            .block-container { 
                padding: 2rem; 
                max-width: 1200px; 
                margin: auto; 
            }
            
            h1, h2, h3 { 
                color: var(--primary-color); 
                margin-bottom: 1.5rem; 
            }
            
            .stButton>button {
                background-color: var(--primary-color);
                color: white;
                font-weight: bold;
                padding: 0.5rem 2rem;
                border-radius: 5px;
                border: none;
                transition: background-color 0.3s;
                width: 100%;
            }
            
            .stButton>button:hover { 
                background-color: var(--secondary-color); 
            }
            
            .stTextInput>div>div>input { 
                border-radius: 5px;
                border: 1px solid #e0e0e0;
            }
            
            .stSelectbox>div>div>div { 
                border-radius: 5px;
                border: 1px solid #e0e0e0;
            }
            
            .custom-info-box {
                padding: 1rem;
                border-radius: 5px;
                background-color: var(--card-background);
                border-left: 5px solid var(--primary-color);
                margin: 1rem 0;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            }
            
            .partner-details {
                background-color: var(--card-background);
                padding: 1rem;
                border-radius: 5px;
                margin-top: 0.5rem;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            }
            
            /* Assessment form styling */
            .assessment-card {
                background-color: var(--card-background);
                padding: 2rem;
                border-radius: 8px;
                margin-bottom: 2rem;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            }
            
            .phase-card {
                background-color: var(--card-background);
                padding: 1.5rem;
                border-radius: 8px;
                height: 100%;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            }
            
            /* Chart container styling */
            .element-container {
                background-color: var(--card-background);
                padding: 1.5rem;
                border-radius: 8px;
                margin-bottom: 1rem;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            }
            
            /* Tab styling */
            .stTabs [data-baseweb="tab-list"] {
                gap: 2px;
                background-color: var(--background-color);
                padding: 0.5rem;
                border-radius: 4px;
            }
            
            .stTabs [data-baseweb="tab"] {
                height: 40px;
                background-color: var(--card-background);
                border: none;
                color: var(--text-color);
                font-weight: 500;
                padding: 8px 16px;
                transition: all 0.2s ease;
                border-radius: 4px;
            }
            
            .stTabs [aria-selected="true"] {
                background-color: var(--primary-color);
                color: white;
            }
            
            /* Table styling */
            .dataframe {
                background-color: var(--card-background);
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            }
            
            .dataframe thead th {
                background-color: var(--primary-color);
                color: white;
                padding: 0.75rem;
            }
            
            .dataframe tbody td {
                padding: 0.75rem;
                border-top: 1px solid #e0e0e0;
            }
            
            /* Expander styling */
            .streamlit-expanderHeader {
                background-color: var(--card-background);
                border-radius: 4px;
            }
        </style>
    """, unsafe_allow_html=True)

###############################################################################
# 3. Excel Generation Functions
###############################################################################

def sanitize_sheet_name(name: str) -> str:
    """Sanitize partner name to a valid Excel sheet name (max 31 chars)."""
    invalid_chars = [':', '\\', '/', '?', '*', '[', ']']
    for c in invalid_chars:
        name = name.replace(c, '')
    # Truncate to 25, then we'll add a short prefix
    name = name[:25]
    return name

def get_rating_color(rating):
    """Get color for a rating value, handling float values."""
    if isinstance(rating, (int, float)):
        # Round float values to nearest integer for color mapping
        rating_int = int(round(rating))
        return MATURITY_COLORS.get(rating_int, '#FFFFFF')
    return '#FFFFFF'

def create_excel_workbook(results, framework, partner_name):
    """Generate Excel report with all sheets."""
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            workbook = writer.book
            
            # Create Partner Details sheet
            create_partner_details_sheet(workbook, writer, partner_name)
            
            # Create other sheets without partner name
            create_ratings_sheet(workbook, writer, results, framework, "Ratings")
            create_heatmap_sheet(workbook, results, "Heatmap")
            create_comments_sheet(workbook, writer, results, "Comments")
            create_definitions_sheet(workbook, writer, "Definitions")
            create_charts_sheet(workbook, writer, results, "Charts")
        
        output.seek(0)
        return output
    except Exception as e:
        st.error(f"Error creating Excel workbook: {str(e)}")
        return None

def create_partner_details_sheet(workbook, writer, partner_name):
    """Create a sheet with partner assessment details."""
    ws = writer.book.add_worksheet("Partner Details")
    
    # Set column width
    ws.set_column('A:B', 30)
    
    # Create formats
    header_format = workbook.add_format({
        'bold': True,
        'font_size': 12,
        'align': 'left',
        'valign': 'vcenter',
        'font_color': '#003366'
    })
    
    value_format = workbook.add_format({
        'font_size': 11,
        'align': 'left',
        'valign': 'vcenter'
    })
    
    # Add assessment details with formatted date and time
    current = pd.Timestamp.now()
    date_str = current.strftime("%d-%m-%Y")
    time_str = current.strftime("%I:%M %p %Z")  # 12-hour format with AM/PM and timezone
    
    details = [
        ["Partner Name", partner_name],
        ["Assessment Date", date_str],
        ["Assessment Time", time_str],
        ["Assessed By", "Meet Shah"]
    ]
    
    for row, (label, value) in enumerate(details):
        ws.write(row, 0, label, header_format)
        ws.write(row, 1, value, value_format)

def create_ratings_sheet(workbook, writer, results, framework, sheet_name):
    """Create the Ratings sheet with color coding."""
    ratings_rows = []
    for cat, domains in CATEGORIES.items():
        for res in results:
            domain = res.get("Domain") if isinstance(res, pd.Series) else res["Domain"]
            if domain in domains:
                for phase in PHASES:
                    if isinstance(res, pd.Series):
                        rating = res.get((phase, "rating"))
                    else:
                        rating = res[phase]["rating"]
                    summary = framework["maturity_levels"][str(rating)]["name"]
                    ratings_rows.append({
                        "Category": cat,
                        "Domain": domain,
                        "Phase": phase,
                        "Rating": rating,
                        "Summary": summary
                    })
    
    df = pd.DataFrame(ratings_rows)
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    format_ratings_sheet(workbook, writer.sheets[sheet_name], df)

def format_ratings_sheet(workbook, worksheet, df):
    """Apply formatting to the Ratings sheet (color code Rating and Summary)."""
    header_format = workbook.add_format({
        'bg_color': '#003366',
        'font_color': 'white',
        'bold': True,
        'align': 'center',
        'valign': 'vcenter',
        'border': 1,
        'text_wrap': True
    })
    
    cell_format = workbook.add_format({
        'border': 1,
        'text_wrap': True,
        'align': 'center',
        'valign': 'vcenter'
    })

    # Write headers
    for col, val in enumerate(df.columns):
        worksheet.write(0, col, val, header_format)
        worksheet.set_column(col, col, 25)

    # Write data with color coding
    for row_num, row_data in enumerate(df.itertuples(index=False), start=1):
        for col_num, col_name in enumerate(df.columns):
            value = getattr(row_data, col_name)
            if col_name == "Rating":
                color = get_rating_color(value)
                fmt = workbook.add_format({
                    'bg_color': color,
                    'border': 1,
                    'align': 'center',
                    'valign': 'vcenter'
                })
                worksheet.write(row_num, col_num, value, fmt)
            elif col_name == "Summary":
                # Color code the Summary with the same color as the rating
                rating_val = getattr(row_data, "Rating")
                color = get_rating_color(rating_val)
                fmt = workbook.add_format({
                    'bg_color': color,
                    'border': 1,
                    'align': 'center',
                    'valign': 'vcenter'
                })
                worksheet.write(row_num, col_num, value, fmt)
            else:
                worksheet.write(row_num, col_num, value, cell_format)

def create_heatmap_sheet(workbook, results, sheet_name):
    """Create heatmap sheet with domain and category level data."""
    worksheet = workbook.add_worksheet(sheet_name)
    
    # Set column widths
    worksheet.set_column('A:A', 30)  # Domain/Category column
    worksheet.set_column('B:D', 15)  # Phase columns
    
    # Create formats
    header_format = workbook.add_format({
        'bold': True,
        'font_size': 11,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': '#D9D9D9'
    })
    
    # Write domain-level headers
    headers = ['Domain', 'Plan & Design', 'Implement', 'Operate & Improve']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, header_format)
    
    # Process domain-level data
    domain_data = []
    row = 1
    for res in results:
        if isinstance(res, pd.Series):
            domain_row = [
                res.get("Domain"),
                res.get(("Plan & Design", "rating"), 0),
                res.get(("Implement", "rating"), 0),
                res.get(("Operate & Improve", "rating"), 0)
            ]
        else:
            domain_row = [
                res["Domain"],
                res["Plan & Design"]["rating"],
                res["Implement"]["rating"],
                res["Operate & Improve"]["rating"]
            ]
        domain_data.append(domain_row)
        for col, value in enumerate(domain_row):
            cell_format = workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'font_size': 10
            })
            if col > 0:  # For rating columns
                cell_format.set_bg_color(get_rating_color(value))
            worksheet.write(row, col, value, cell_format)
        row += 1
    
    domain_end_row = row
    
    # Add domain-level chart (positioned after domain table)
    domain_chart_row = domain_end_row + 2
    add_domain_chart(workbook, worksheet, pd.DataFrame(domain_data, columns=headers), 0, sheet_name, domain_chart_row)
    
    # Add spacing between tables (after domain chart)
    category_start_row = domain_chart_row + 22  # Enough space for the chart
    
    # Write category-level headers
    for col, header in enumerate(headers):
        worksheet.write(category_start_row, col, header.replace('Domain', 'Category'), header_format)
    
    # Process category-level data
    category_data = []
    categories_seen = set()
    row = category_start_row + 1
    
    for res in results:
        domain = res["Domain"] if isinstance(res, dict) else res.get("Domain")
        category = get_category_for_domain(domain)
        
        if category not in categories_seen:
            categories_seen.add(category)
            category_ratings = {"Category": category}
            category_count = 0
            category_sums = {phase: 0 for phase in PHASES}
            
            # Calculate average ratings for the category
            for inner_res in results:
                inner_domain = inner_res["Domain"] if isinstance(inner_res, dict) else inner_res.get("Domain")
                if get_category_for_domain(inner_domain) == category:
                    category_count += 1
                    for phase in PHASES:
                        if isinstance(inner_res, pd.Series):
                            rating = inner_res.get((phase, "rating"), 0)
                        else:
                            rating = inner_res[phase]["rating"]
                        category_sums[phase] += rating
            
            # Calculate averages
            for phase in PHASES:
                category_ratings[phase] = round(category_sums[phase] / category_count, 2) if category_count > 0 else 0
            
            category_row = [
                category_ratings["Category"],
                category_ratings["Plan & Design"],
                category_ratings["Implement"],
                category_ratings["Operate & Improve"]
            ]
            category_data.append(category_row)
            
            for col, value in enumerate(category_row):
                cell_format = workbook.add_format({
                    'align': 'center',
                    'valign': 'vcenter',
                    'font_size': 10
                })
                if col > 0:  # For rating columns
                    cell_format.set_bg_color(get_rating_color(value))
                worksheet.write(row, col, value, cell_format)
            row += 1
    
    # Add category-level chart (positioned after category table)
    if category_data:
        category_chart_row = row + 2
        add_category_chart(workbook, worksheet, pd.DataFrame(category_data, columns=headers), category_start_row, sheet_name, category_chart_row)

def add_domain_chart(workbook, worksheet, df, startrow, sheet_name, chart_row):
    """Add enhanced chart for domain-level data."""
    if df.empty:
        return
        
    chart = workbook.add_chart({'type': 'column'})
    if not chart:
        return
    
    # Add series for each phase with custom colors
    colors = ['#4472C4', '#ED7D31', '#A5A5A5']  # Blue, Orange, Gray
    for i, (phase, color) in enumerate(zip(PHASES, colors), start=1):
        chart.add_series({
            'name':       [sheet_name, startrow, i],
            'categories': [sheet_name, startrow + 1, 0, startrow + len(df), 0],
            'values':     [sheet_name, startrow + 1, i, startrow + len(df), i],
            'fill':       {'color': color},
            'border':     {'color': color},
        })
    
    chart.set_title({'name': 'Domain Level Maturity Ratings', 'font': {'size': 12, 'bold': True}})
    chart.set_x_axis({
        'name': 'Domains',
        'font': {'size': 10},
        'num_font': {'size': 9},
        'label_position': 'low',
        'num_format': '@'  # Treat as text to show full domain names
    })
    chart.set_y_axis({
        'name': 'Rating',
        'min': 0,
        'max': 5,
        'major_unit': 1,
        'font': {'size': 10},
        'num_font': {'size': 9},
    })
    chart.set_style(2)
    chart.set_size({'width': 720, 'height': 400})
    chart.set_legend({'position': 'bottom'})
    
    worksheet.insert_chart(chart_row, 0, chart)

def add_category_chart(workbook, worksheet, df, startrow, sheet_name, chart_row):
    """Add enhanced chart for category-level data."""
    if df.empty:
        return
        
    chart = workbook.add_chart({'type': 'column'})
    if not chart:
        return
    
    # Add series for each phase with custom colors
    colors = ['#4472C4', '#ED7D31', '#A5A5A5']  # Blue, Orange, Gray
    for i, (phase, color) in enumerate(zip(PHASES, colors), start=1):
        chart.add_series({
            'name':       [sheet_name, startrow, i],
            'categories': [sheet_name, startrow + 1, 0, startrow + len(df), 0],
            'values':     [sheet_name, startrow + 1, i, startrow + len(df), i],
            'fill':       {'color': color},
            'border':     {'color': color},
        })
    
    chart.set_title({'name': 'Category Level Maturity Ratings', 'font': {'size': 12, 'bold': True}})
    chart.set_x_axis({
        'name': 'Categories',
        'font': {'size': 10},
        'num_font': {'size': 9},
        'label_position': 'low',
        'num_format': '@'
    })
    chart.set_y_axis({
        'name': 'Rating',
        'min': 0,
        'max': 5,
        'major_unit': 1,
        'font': {'size': 10},
        'num_font': {'size': 9},
    })
    chart.set_style(2)
    chart.set_size({'width': 720, 'height': 400})
    chart.set_legend({'position': 'bottom'})
    
    worksheet.insert_chart(chart_row, 0, chart)

def create_comments_sheet(workbook, writer, results, sheet_name):
    """Create the Detailed Comments sheet."""
    comments_rows = []
    for res in results:
        domain = res.get("Domain") if isinstance(res, pd.Series) else res["Domain"]
        for phase in PHASES:
            if isinstance(res, pd.Series):
                rating = res.get((phase, "rating"))
                comments = res.get((phase, "comments"))
                partner_details = res.get((phase, "partner_details"), "")
            else:
                rating = res[phase]["rating"]
                comments = res[phase]["comments"]
                partner_details = res[phase].get("partner_details", "")
                
            comments_rows.append({
                "Domain": domain,
                "Phase": phase,
                "Rating": rating,
                "Selected Points": comments,
                "Partner Specific Details": partner_details
            })

    df = pd.DataFrame(comments_rows)
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    format_comments_sheet(workbook, writer.sheets[sheet_name], df)

def format_comments_sheet(workbook, worksheet, df):
    """Apply formatting to the Detailed Comments sheet."""
    header_format = workbook.add_format({
        'bg_color': '#003366',
        'font_color': 'white',
        'bold': True,
        'align': 'center',
        'border': 1
    })
    cell_format = workbook.add_format({'border': 1, 'align': 'center'})
    
    # Write header row
    for col, col_name in enumerate(df.columns):
        worksheet.write(0, col, col_name, header_format)
        worksheet.set_column(col, col, 30)
    
    # Write data rows using index-based access
    for row_num, row_data in enumerate(df.itertuples(index=False), start=1):
        for col_num, _ in enumerate(df.columns):
            value = row_data[col_num]
            worksheet.write(row_num, col_num, value, cell_format)

def create_definitions_sheet(workbook, writer, sheet_name):
    """
    Create the Ratings Definition sheet in Excel using the local
    MATURITY_LEVELS_DETAILS + MATURITY_LEVEL_NAMES, with color-coded headers.
    """
    ws = workbook.add_worksheet(sheet_name)
    cell_format = workbook.add_format({'border': 1, 'text_wrap': True})

    sorted_levels = sorted(MATURITY_LEVELS_DETAILS.keys(), key=int)
    for i, level in enumerate(sorted_levels):
        level_title = f"{level} = {MATURITY_LEVEL_NAMES[level]}"
        color = get_rating_color(int(level))
        level_format = workbook.add_format({
            'bg_color': color,
            'font_color': 'black',
            'bold': True,
            'align': 'center',
            'border': 1,
            'text_wrap': True
        })
        ws.write(0, i, level_title, level_format)

        bullet_points = MATURITY_LEVELS_DETAILS[level]
        for row_index, bullet in enumerate(bullet_points, start=1):
            ws.write(row_index, i, bullet, cell_format)
        ws.set_column(i, i, 40)

def create_charts_sheet(workbook, writer, results, sheet_name):
    """Create enhanced charts sheet with color coding."""
    if not results:
        return

    ws = workbook.add_worksheet(sheet_name)
    
    # Prepare data
    data_rows = []
    for res in results:
        if isinstance(res, pd.Series):
            domain = res.get("Domain")
            row = {
                "Domain": domain,
                "Plan & Design": res.get(("Plan & Design", "rating"), 0),
                "Implement": res.get(("Implement", "rating"), 0),
                "Operate & Improve": res.get(("Operate & Improve", "rating"), 0)
            }
        else:
            row = {
                "Domain": res["Domain"],
                "Plan & Design": res["Plan & Design"]["rating"],
                "Implement": res["Implement"]["rating"],
                "Operate & Improve": res["Operate & Improve"]["rating"]
            }
        data_rows.append(row)

    if not data_rows:
        return

    # Write color-coded table
    headers = ["Domain"] + PHASES
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#4472C4',
        'font_color': 'white',
        'align': 'center',
        'border': 1
    })

    for col, header in enumerate(headers):
        ws.write(0, col, header, header_format)
        ws.set_column(col, col, 15)

    for row, data in enumerate(data_rows, start=1):
        ws.write(row, 0, data["Domain"])
        for col, phase in enumerate(PHASES, start=1):
            value = data[phase]
            color = get_rating_color(value)
            fmt = workbook.add_format({
                'bg_color': color,
                'align': 'center',
                'border': 1
            })
            ws.write(row, col, value, fmt)

    last_row = len(data_rows)

    # Create Radar Chart
    radar_chart = workbook.add_chart({'type': 'radar'})
    if radar_chart:
        for i, (phase, color) in enumerate(zip(PHASES, ['#4472C4', '#ED7D31', '#A5A5A5']), start=1):
            radar_chart.add_series({
                'name': phase,
                'categories': [sheet_name, 1, 0, last_row, 0],
                'values': [sheet_name, 1, i, last_row, i],
                'marker': {'type': 'automatic'},
                'line': {'width': 2.25, 'color': color}
            })

        radar_chart.set_title({'name': 'Capability Rating by Domain', 'font': {'size': 12, 'bold': True}})
        radar_chart.set_size({'width': 500, 'height': 300})
        radar_chart.set_style(2)
        ws.insert_chart('F2', radar_chart)

    # Create Scatter Chart instead of Bubble Chart
    scatter_chart = workbook.add_chart({'type': 'scatter'})
    if scatter_chart:
        scatter_chart.add_series({
            'name': 'Domains',
            'categories': [sheet_name, 1, 1, last_row, 1],  # Plan & Design
            'values': [sheet_name, 1, 2, last_row, 2],      # Implement
            'marker': {
                'type': 'circle',
                'size': 10,
                'fill': {'color': '#4472C4'},
                'border': {'color': '#2F528F'}
            }
        })

        scatter_chart.set_title({
            'name': 'Plan & Design vs Implement',
            'font': {'size': 12, 'bold': True}
        })
        scatter_chart.set_x_axis({
            'name': 'Plan & Design',
            'min': 0,
            'max': 5,
            'major_gridlines': {'visible': True}
        })
        scatter_chart.set_y_axis({
            'name': 'Implement',
            'min': 0,
            'max': 5,
            'major_gridlines': {'visible': True}
        })
        scatter_chart.set_size({'width': 500, 'height': 300})
        scatter_chart.set_style(2)
        ws.insert_chart('F20', scatter_chart)

###############################################################################
# 4. Assessment Form Functions
###############################################################################

def get_domain_state_key(domain, phase):
    """Generate a consistent key for storing domain state."""
    return f"{domain}_{phase}"

def save_domain_state(domain, phase_results):
    """Save the current domain's state to session state."""
    if domain not in st.session_state.domain_states:
        st.session_state.domain_states[domain] = {}
    
    for phase, data in phase_results.items():
        key = get_domain_state_key(domain, phase)
        st.session_state.domain_states[domain][phase] = {
            "rating": data["rating"],
            "partner_details": data.get("partner_details", ""),
            "comments": data.get("comments", "")
        }

def load_domain_state(domain):
    """Load a domain's saved state from session state."""
    return st.session_state.domain_states.get(domain, {})

def collect_phase_assessment(phase, current_domain, framework):
    """Collect assessment data for a single phase with state preservation."""
    # Generate consistent keys for session state
    rating_key = get_domain_state_key(current_domain, f"{phase}_rating")
    details_key = get_domain_state_key(current_domain, f"{phase}_details")
    
    # Load saved state if available
    saved_state = load_domain_state(current_domain)
    saved_phase_data = saved_state.get(phase, {})
    
    # Initialize or load saved values in session state
    if rating_key not in st.session_state:
        st.session_state[rating_key] = str(saved_phase_data.get("rating", "1"))
    if details_key not in st.session_state:
        st.session_state[details_key] = saved_phase_data.get("partner_details", "")

    # Display the form with saved values
    maturity_rating = st.selectbox(
        f"Maturity level for {phase}",
        options=["1", "2", "3", "4", "5"],
        index=int(st.session_state[rating_key]) - 1,  # Convert to 0-based index
        format_func=lambda x: f"{x} - {framework['maturity_levels'][x]['name']}",
        key=rating_key
    )

    bullet_points = MATURITY_LEVELS_DETAILS[maturity_rating]
    st.markdown("\n".join([f"- {bp}" for bp in bullet_points]), unsafe_allow_html=True)
    
    with st.expander("Add Partner Specific Details"):
        partner_details = st.text_area(
            "Partner Details (optional):",
            value=st.session_state[details_key],
            key=details_key,
            help="Add specific observations about the partner's capabilities"
        )

    # Return the assessment data
    return {
        "rating": int(maturity_rating),
        "comments": "\n- ".join([""] + bullet_points),
        "partner_details": partner_details,
        "color": framework["maturity_levels"][maturity_rating]["color"]
    }

def display_assessment_form(framework, current_domain):
    """Display the assessment form for the current domain."""
    st.markdown(f"""
        <div class="assessment-card">
            <h2 style='color: var(--primary-color); margin-bottom: 1.5rem;'>{current_domain}</h2>
        </div>
    """, unsafe_allow_html=True)

    phase_results = {}
    cols = st.columns(3)

    for i, phase in enumerate(PHASES):
        with cols[i]:
            st.markdown(f"""
                <div class="phase-card">
                    <h3 style='color: var(--primary-color); margin-bottom: 1rem;'>{phase}</h3>
                </div>
            """, unsafe_allow_html=True)
            phase_results[phase] = collect_phase_assessment(
                phase, current_domain, framework
            )

    display_navigation_buttons(current_domain, phase_results)

def display_navigation_buttons(current_domain, phase_results):
    """Display and handle navigation buttons with state preservation."""
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⬅️ Previous"):
            # Save current state before navigating back
            save_domain_state(current_domain, phase_results)
            
            if st.session_state.current_domain_index > 0:
                st.session_state.current_domain_index -= 1
                st.rerun()
            elif st.session_state.current_domain_index == 0:
                st.session_state.partner_name = ""
                st.rerun()
                
    with col2:
        if st.button("Save & Continue ➡️"):
            save_and_continue(current_domain, phase_results)

def save_and_continue(current_domain, phase_results):
    """Save current assessment and move to next domain."""
    # Save the current domain state
    save_domain_state(current_domain, phase_results)
    
    # Update results while preserving other domains
    st.session_state.results = [r for r in st.session_state.results 
                              if r["Domain"] != current_domain]
    st.session_state.results.append({
        "Domain": current_domain,
        **{phase: data for phase, data in phase_results.items()}
    })

    all_domains = [domain for domains in CATEGORIES.values() for domain in domains]
    if st.session_state.current_domain_index < len(all_domains) - 1:
        st.session_state.current_domain_index += 1
    else:
        st.session_state.show_results = True
    st.rerun()

###############################################################################
# 5. Results Page Functions
###############################################################################

def display_results_page(framework, partner_name):
    """Display the results page with all visualizations."""
    st.header("Assessment Results")
    tab1, tab2, tab3 = st.tabs(["Summary", "Detailed Ratings", "Charts"])
    
    with tab1:
        display_summary_tab()
    with tab2:
        display_detailed_ratings_tab()
    with tab3:
        display_charts_tab()
    
    display_download_button(framework, partner_name)

def get_category_for_domain(domain):
    """Helper to find the category for a given domain."""
    for cat, domains in CATEGORIES.items():
        if domain in domains:
            return cat
    return "Unknown"

def display_summary_tab():
    """Display summary tab with color-coded ratings."""
    if not st.session_state.results:
        st.write("No results to display.")
        return

    summary_data = []
    for res in st.session_state.results:
        if isinstance(res, pd.Series):
            summary_data.append({
                "Category": get_category_for_domain(res.get("Domain")),
                "Domain": res.get("Domain"),
                "Plan & Design": res.get(("Plan & Design", "rating")),
                "Implement": res.get(("Implement", "rating")),
                "Operate & Improve": res.get(("Operate & Improve", "rating"))
            })
        else:
            summary_data.append({
                "Category": get_category_for_domain(res["Domain"]),
                "Domain": res["Domain"],
                "Plan & Design": res["Plan & Design"]["rating"],
                "Implement": res["Implement"]["rating"],
                "Operate & Improve": res["Operate & Improve"]["rating"]
            })
    
    df = pd.DataFrame(summary_data)
    
    # Color code the numeric columns
    def color_rating(val):
        if isinstance(val, (int, float)):
            color = get_rating_color(val)
            return f'background-color: {color}'
        return ''
    
    styled_df = df.style.applymap(
        color_rating,
        subset=PHASES
    )
    
    st.write(styled_df.to_html(escape=False), unsafe_allow_html=True)

def display_detailed_ratings_tab():
    """Display detailed ratings with comments."""
    if not st.session_state.results:
        st.write("No detailed results to display.")
        return

    for res in st.session_state.results:
        if isinstance(res, pd.Series):
            domain = res.get("Domain")
            with st.expander(f"{domain} ({get_category_for_domain(domain)})"):
                for phase in PHASES:
                    rating = res.get((phase, "rating"))
                    comments = res.get((phase, "comments"))
                    partner_details = res.get((phase, "partner_details"))
                    
                    st.markdown(f"**{phase}:** Level {rating}")
                    if comments:
                        st.markdown(comments)
                    if partner_details:
                        st.markdown(f"*Partner Details:* {partner_details}")
        else:
            with st.expander(f"{res['Domain']} ({get_category_for_domain(res['Domain'])})"):
                for phase in PHASES:
                    st.markdown(f"**{phase}:** Level {res[phase]['rating']}")
                    st.markdown(res[phase]["comments"])
                    if res[phase].get("partner_details"):
                        st.markdown(f"*Partner Details:* {res[phase]['partner_details']}")

def display_charts_tab():
    """Display enhanced interactive charts in the UI."""
    try:
        if not st.session_state.results:
            st.write("No charts to display.")
            return

        # Prepare data for charts
        domain_data = []
        for res in st.session_state.results:
            try:
                if isinstance(res, pd.Series):
                    domain = res.get("Domain")
                    category = get_category_for_domain(domain)
                    domain_data.append({
                        "Domain": domain,
                        "Category": category,
                        "Plan & Design": res.get(("Plan & Design", "rating"), 0),
                        "Implement": res.get(("Implement", "rating"), 0),
                        "Operate & Improve": res.get(("Operate & Improve", "rating"), 0)
                    })
                else:
                    domain_data.append({
                        "Domain": res["Domain"],
                        "Category": get_category_for_domain(res["Domain"]),
                        "Plan & Design": res["Plan & Design"]["rating"],
                        "Implement": res["Implement"]["rating"],
                        "Operate & Improve": res["Operate & Improve"]["rating"]
                    })
            except Exception as e:
                st.warning(f"Error processing result: {str(e)}")
                continue

        if not domain_data:
            st.warning("No valid data available for charts.")
            return

        df_domain = pd.DataFrame(domain_data)
        
        # Create Domain Level Maturity Ratings chart
        fig_domain = go.Figure()
        colors = ['#4472C4', '#ED7D31', '#A5A5A5']  # Blue, Orange, Gray
        
        for phase, color in zip(PHASES, colors):
            fig_domain.add_trace(go.Bar(
                name=phase,
                x=df_domain["Domain"],
                y=df_domain[phase],
                marker_color=color
            ))

        fig_domain.update_layout(
            title={
                'text': "Domain Level Maturity Ratings",
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=20, color='#003366')
            },
            barmode='group',
            xaxis_title="Domains",
            yaxis_title="Rating",
            yaxis=dict(range=[0, 5]),
            plot_bgcolor='rgba(240,240,240,0.8)',
            paper_bgcolor='rgba(240,240,240,0.8)',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig_domain, use_container_width=True)

        # Create Category Level Maturity Ratings chart
        df_category = df_domain.groupby('Category')[PHASES].mean().reset_index()
        
        fig_category = go.Figure()
        
        for phase, color in zip(PHASES, colors):
            fig_category.add_trace(go.Bar(
                name=phase,
                x=df_category["Category"],
                y=df_category[phase],
                marker_color=color
            ))
        
        fig_category.update_layout(
            title={
                'text': "Category Level Maturity Ratings",
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=20, color='#003366')
            },
            barmode='group',
            xaxis_title="Categories",
            yaxis_title="Rating",
            yaxis=dict(range=[0, 5]),
            plot_bgcolor='rgba(240,240,240,0.8)',
            paper_bgcolor='rgba(240,240,240,0.8)',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig_category, use_container_width=True)

        # Create enhanced Radar Chart
        fig_radar = go.Figure()
        
        for phase, color in zip(PHASES, colors):
            fig_radar.add_trace(go.Scatterpolar(
                r=df_domain[phase],
                theta=df_domain["Domain"],
                name=phase,
                fill='toself',
                line=dict(color=color, width=2),
                fillcolor=f'rgba{tuple(list(int(color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + [0.2])}'
            ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 5],
                    gridcolor='rgba(0,0,0,0.1)',
                    linecolor='rgba(0,0,0,0.1)'
                ),
                bgcolor='rgba(240,240,240,0.8)',
                angularaxis=dict(gridcolor='rgba(0,0,0,0.1)')
            ),
            showlegend=True,
            title={
                'text': "Domain Maturity Overview",
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=20, color='#003366')
            },
            paper_bgcolor='rgba(240,240,240,0.8)',
            plot_bgcolor='rgba(240,240,240,0.8)'
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)

    except Exception as e:
        st.error(f"Error displaying charts: {str(e)}")

def display_download_button(framework, partner_name):
    """Display Excel download button."""
    if not st.session_state.results:
        st.write("No data available for download.")
        return

    # Sanitize partner name for filename
    sanitized_filename = "".join(c for c in partner_name if c.isalnum() or c in (' ', '-', '_')).strip()
    if not sanitized_filename:
        sanitized_filename = "AI_Maturity_Assessment"
    
    excel_file = create_excel_workbook(
        st.session_state.results,
        framework,
        partner_name
    )
    
    st.download_button(
        "📥 Download Full Assessment Report (Excel)",
        excel_file,
        f"{sanitized_filename}_AI_Maturity_Assessment_Report.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

###############################################################################
# 6. Main Application
###############################################################################

def main():
    """Main application flow."""
    init_session_state()
    setup_page()
    framework = load_config()
    
    # Handle partner name input
    if not st.session_state.partner_name:
        partner_name = st.text_input("Enter Partner Name:", key="partner_name_input")
        if not partner_name:
            st.warning("Please enter partner name to continue")
            st.stop()
        st.session_state.partner_name = partner_name
    
    # Display either results or assessment form
    if st.session_state.show_results:
        display_results_page(framework, st.session_state.partner_name)
    else:
        all_domains = [domain for domains in CATEGORIES.values() for domain in domains]
        current_domain = all_domains[st.session_state.current_domain_index]
        display_assessment_form(framework, current_domain)

if __name__ == "__main__":
    main()