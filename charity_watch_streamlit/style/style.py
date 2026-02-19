#THIS FILE WILL DEFINE THE APP'S STYLING

#defining the app colour palette using a green scale. (see design for reasoning behing palette)
APP_COLOUR_PALETTE = {
    "bg":         "#040907",
    "surface":    "#0f261c",
    "border":     "#4d5c55",
    "border_lit": "#2a5e43",
    "text":       "#e8f0ec",
    "muted":      "#6b8f7e",
    "accent":     "#4ade80",
    "white":      "#ffffff",
}

app_style_design = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800;900&family=DM+Sans:wght@300;400;500;600&display=swap');

    /* HOME PAGE STYLING */
    .stApp{{
        background: {APP_COLOUR_PALETTE['bg']};
        color: {APP_COLOUR_PALETTE['text']};
        font-family: 'DM Sans', sans-serif;
    }}

    /* HIDE SIDEBAR (not needed for app) */
    #MainMenu, header, footer {{ visibility: hidden; }}
    section[data-testid="stSidebar"] {{ display: none; }}
    .block-container {{ padding-top: 20px; padding-bottom: 20px; max-width: 1400px; }}

    /* ── Title ── */
    .cw-title {{
        font-family: 'Playfair Display', serif;
        text-align: center;
    }}

    /* ── Map border ── */
    iframe {{
        border-radius: 14px;
        border: 3px solid {APP_COLOUR_PALETTE["border"]} !important;
    }}

</style>
"""

#https://medium.com/snowflake/style-and-customize-your-streamlit-in-snowflake-apps-4a8495b8e469
statistic_cards_style = """ 
{
    background-color: #0f261c;
    border-radius: 10px;
    box-shadow: -6px 5px 8px 1px #2a5e43;
    width: 100%;
    box-sizing: border-box;
    min-height: 55px;
    display: flex;
    align-items: center;
    padding: 0 25px;
}
"""
statistic_cards_small_style = """ 
{
    background-color: #091711;
    border-radius: 10px;
    box-shadow: -6px 5px 8px 1px #0f261c;
    width: 100%;
    box-sizing: border-box;
    min-height: 40px;
    display: flex;
    align-items: center;
    padding: 0 25px;
}
"""