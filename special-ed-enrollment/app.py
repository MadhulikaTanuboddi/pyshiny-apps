from dis import dis
from re import sub
from shiny import App, render, ui
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
from pathlib import Path

sns.set_theme()

enroll_list = pd.read_csv(Path(__file__).parent / "scc_enrollment.csv")

# DATA CLEANING: Extract Year from Date
enroll_list["Date"] = enroll_list["Date"].astype('datetime64[ns]')
enroll_list["Year"] = enroll_list["Date"].dt.year

# DATA CLEANING: Remove unavailable data label "*"
enroll_list = enroll_list.replace({'\*' : '0'}, regex = True )

# Create input lists
age = enroll_list["Age"].unique().tolist()
disability = enroll_list.columns.values.tolist()
disability.remove("Date")
disability.remove("Age")
disability.remove("Year")
disability.sort()


app_ui = ui.page_fluid(
    ui.input_selectize("disability", "Disability", disability, selected = "Autism", multiple=False),
    ui.input_selectize("age", "Age", age, selected = 6, multiple=False),
    ui.output_plot("lineplot"),
)

def server(input, output, session):
    @output
    @render.plot
    def lineplot():
        # Filter data by age selection
        sub_df = enroll_list[(enroll_list["Age"] == pd.to_numeric(input.age()))]

        # Keep only columns with disability selection
        dis = input.disability()
        target_list = ['Age', 'Year', dis]
        sub_df = sub_df.filter(regex="|".join(target_list), axis=1)

        sub_df[dis]=sub_df[dis].astype('int64')
       # enroll_list["Date"] = enroll_list["Date"].astype('datetime64[ns]')

        # Plot data
        g = sns.lineplot(
            data=sub_df,
            y= dis,
            x="Year",
            marker="o",
            label=dis,
        )

        # Format axis labels
        g.set_ylabel("Number Of Enrolled Students")

        return g

app = App(app_ui, server)

#TODO:
# Implement Shiny modules
# Have dropdown of disability
#For each age value:
 #Have value boxes of max count / average count
 #Have plot output
 #(This “value boxes + plot output” should be written as a shiny module)