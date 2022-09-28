from re import L
from shiny import App, render, ui
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

sns.set_theme()

# Data source: https://www.kaggle.com/code/kevinmorgado/us-monthly-generation-eda/data
# Kept only CA data to reduce csv file size
power_list = pd.read_csv(Path(__file__).parent / "ca_gen.csv")

# Create date column
power_list["Date"] = pd.to_datetime(dict(year=power_list["YEAR"],month=power_list["MONTH"],day=1))
power_list=power_list.set_index("Date")

# Remove columns not needed
power_list.drop(columns=["YEAR","MONTH", "STATE", "TYPE OF PRODUCER"],inplace=True)

# Add power per month by energy source
total_power = power_list.groupby(by=["Date","ENERGY SOURCE"]).sum().reset_index()
total_power = total_power[total_power["ENERGY SOURCE"].str.contains("Total") == False]
total_power["ENERGY SOURCE"] = total_power["ENERGY SOURCE"].str.replace("Hydroelectric Conventional", "Hydroelectric")
total_power["ENERGY SOURCE"] = total_power["ENERGY SOURCE"].str.replace("Solar Thermal and Photovoltaic", "Solar")
total_power["ENERGY SOURCE"] = total_power["ENERGY SOURCE"].str.replace("Wood and Wood Derived Fuels", "Wood")

df = pd.DataFrame(total_power)

# Create lists for UI
energy_source = total_power["ENERGY SOURCE"].unique().tolist()
print(energy_source)


app_ui = ui.page_fluid(
     ui.input_checkbox_group(
        "source", 
        "Energy Source:", 
        {
            "Coal": "Coal",
            "Hydroelectric": "Hydroelectric",
            "Natural Gas": "Natural Gas",
            "Nuclear": "Nuclear",
            "Petroleum": "Petroleum",
            "Solar": "Solar",
            "Wind": "Wind",
            "Geothermal": "Geothermal",
            "Other Gases": "Other Gases",
            "Other": "Other",
        },
        selected = "Natural Gas",
    ),
     ui.output_plot("lineplot"),
)

def server(input, output, session):
     @output
     @render.plot
     def lineplot():

        sub_df = df[(df["ENERGY SOURCE"].isin(input.source()))]

        for src in input.source():
            sub_df_tmp = sub_df[(sub_df["ENERGY SOURCE"] == src)]      
            g = sns.lineplot(
                data = sub_df_tmp,
                x = "Date",
                y = "GENERATION (Megawatthours)",
            )
        return g

app = App(app_ui, server)