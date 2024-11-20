import datapane as dp
from io import BytesIO
import matplotlib.pyplot as plt
import base64


def styled_title(title: str, subtitle: str = ""):
    """
    Generate a styled title section with a main title and an optional subtitle.
    """
    return dp.HTML(f"""
    <div style="background-color: #007bff; color: white; text-align: center; padding: 20px; border-radius: 8px;">
        <h1 style="margin: 0; font-family: Arial, sans-serif;">{title}</h1>
        <p style="margin: 0; font-family: Arial, sans-serif; font-size: 16px;">{subtitle}</p>
    </div>
    """)


def styled_image(image_path: str, width: str = "200px"):
    """
    Embed an image with custom styling and size.
    """
    with open(image_path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")
    return dp.HTML(f"""
    <div style="text-align: center; margin-top: 10px;">
        <img src="data:image/png;base64,{image_base64}" alt="Image" style="width: {width}; height: auto; border-radius: 8px;">
    </div>
    """)


def styled_graph(fig):
    """
    Convert a Matplotlib figure to a styled Base64 HTML image.
    """
    buffer = BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    graph_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    buffer.close()
    return dp.HTML(f"""
    <div style="text-align: center; margin-top: 20px;">
        <img src="data:image/png;base64,{graph_base64}" alt="Graph" style="width: 100%; max-width: 800px; height: auto; border: 1px solid #ddd; border-radius: 8px;">
    </div>
    """)


def styled_metric(heading: str, value, change=None, is_upward_change=True):
    """
    Create a styled BigNumber component.
    """
    return dp.BigNumber(
        heading=heading,
        value=value,
        change=change,
        is_upward_change=is_upward_change,
    )


def styled_table(dataframe):
    """
    Create a styled interactive table.
    """
    return dp.DataTable(dataframe)


def placeholder_message(message: str, icon: str = "ℹ️"):
    """
    Generate a placeholder styled section for missing data or upcoming features.
    """
    return dp.HTML(f"""
    <div style="text-align: center; background-color: #f8f9fa; color: #6c757d; padding: 20px; border: 1px dashed #6c757d; border-radius: 8px;">
        <h3 style="margin: 0; font-family: Arial, sans-serif;">{icon} {message}</h3>
    </div>
    """)


# Example reusable theme
THEME_COLORS = {
    "primary": "#007bff",
    "secondary": "#6c757d",
    "light": "#f8f9fa",
    "dark": "#343a40",
}
