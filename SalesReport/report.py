import base64
import pandas as pd
import matplotlib.pyplot as plt
import datapane as dp

# Load the data
df = pd.read_csv('resources/sales_data.csv')

# Filter data for specific years
df_2021 = df[df['Año'] == 2021]
df_2020 = df[df['Año'] == 2020]

# Calculate income and differences
income_2021 = df_2021['Ventas'].sum()
income_2020 = df_2020['Ventas'].sum()
income_diff = income_2021 - income_2020
percentage = (income_diff / income_2020) * 100 if income_2020 != 0 else 0

# Pivot Table for Bar Chart

pivot_tipoDeProducto_byYear = df_2021.pivot_table(
    index='Tipo de producto',
    columns='Año',
    values='Ventas',
    aggfunc='sum'
)

plt.figure(figsize=(10, 6))
pivot_tipoDeProducto_byYear.plot(kind='bar', color=["#FF5733", "#33FFCE", "#3380FF"])
plt.title('Ventas por Tipo de producto (2021)')
plt.xlabel('Tipo de producto')
plt.ylabel('Ventas')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('TipoProductoVentas.png')
plt.close()

# Pie Chart for Sales by Product Type
sales_by_product_2021 = df_2021.groupby('Tipo de producto')["Ventas"].sum()
plt.figure(figsize=(8, 8))
plt.pie(
    sales_by_product_2021,
    labels=sales_by_product_2021.index,
    autopct='%1.1f%%',
    startangle=140,
    colors=["#FF5733", "#33FFCE", "#3380FF"],
)
plt.title("Distribución de Ventas por Tipo de producto (2021)")
plt.savefig("TipoProducto_PieChart_2021.png")
plt.close()


# Function to Style Images
def styled_image(image_path: str, width: str = "300px"):
    with open(image_path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")
    return dp.HTML(f"""
    <div style="text-align: center; margin-top: 10px;">
        <img src="data:image/png;base64,{image_base64}" alt="Image" style="width: {width}; height: auto; border-radius: 8px;">
    </div>
    """)


# Styled Metrics Section
analysis_numbers = dp.Group(
    dp.BigNumber(
        heading="Income 2021",
        value=f"{income_2021:,.2f} €",
    ),
    dp.BigNumber(
        heading="Income 2020",
        value=f"{income_2020:,.2f} €",
    ),
    columns=2,
)

analysis_numbers_summary = dp.Group(
    dp.BigNumber(
        heading="Difference in Income",
        value=f"{income_diff:,.2f} €",
        change=percentage,
        is_upward_change=income_diff > 0,
    ),
    columns=1,
)

# Pie Chart Section
pie_chart_section = dp.Group(
    styled_image("TipoProducto_PieChart_2021.png", "300px"),
    dp.Text("<h3 style='text-align: center;'>Distribución de Ventas por Tipo de Producto (2021)</h3>"),
)

# Bar Chart Section
bar_chart_section = dp.Group(
    styled_image("TipoProductoVentas.png", "800px"),
    dp.Text("<h3 style='text-align: center;'>Ventas por Tipo de Producto (2021)</h3>"),
)

# Pivot Table Section
pivot_table_section = dp.Group(
    dp.Table(pivot_tipoDeProducto_byYear),
    dp.Text("<h3 style='text-align: center;'>Detalle de Ventas por Tipo de Producto y Año</h3>"),
)

# Create the Report
report = dp.Report(
    dp.Text("# Sales Report 2021"),
    analysis_numbers,
    analysis_numbers_summary,
    pie_chart_section,
    bar_chart_section,
    pivot_table_section,
)

# Save the Report
report.save("sales_report.html", open=True)
