import pandas as pd
import datapane as dp
from themed_components import styled_title, styled_image, styled_metric, styled_table

# Load the dataset
file_path = 'simulated_hotel_income.csv'
df = pd.read_csv(file_path)

# Preview the data
print(df.head())

# Calculate key metrics
income_2022 = df["2022"].sum()
income_2021 = df["2021"].sum()
income_diff = income_2022 - income_2021
is_upward = income_diff > 0

print(f"Income in 2022 : {income_2022:.2f}")
print(f"Income in 2021 : {income_2021:.2f}")
print(f"Income diff: {income_diff:.2f}")

# Styled components
title = styled_title("Hotel Income Report", "Analysis of Annual Income for 2022")
logo = styled_image("hotel_logo.png", width="200px")
metric_1 = styled_metric("Total Income for 2022", income_2022, change=income_diff, is_upward_change=is_upward)
metric_2 = styled_metric("Total Income for 2021", income_2021)
table = styled_table(df)

# CSV Attachment
data_attachment = dp.Attachment(file=file_path)

# Create the report
report = dp.Report(
    dp.Group(
        title,
        logo,
    ),
    dp.HTML("<h2>Key Metrics</h2>"),
    dp.Group(
        metric_1,
        metric_2,
        columns=2,
    ),
    dp.Group(
        dp.HTML("<h2>Detailed Data</h2>"),
        table,
    ),
    dp.Group(
        dp.HTML("<h2>Download Data</h2>"),
        data_attachment,
    )
)

# Save the report
report.save("hotel_income_report.html", open=True)
