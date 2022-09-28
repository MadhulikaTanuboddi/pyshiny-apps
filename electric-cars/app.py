from shiny import App, render, ui
import pandas as pd
import seaborn as sns

from pathlib import Path

sns.set_theme()

ev_list = pd.read_csv(Path(__file__).parent / "ev.csv")

# Split to create Make and Model columns
ev_list[['Make','Model']] = ev_list['Name'].str.split(' ', n=1, expand=True)

# Clean Price column data
ev_list['PriceinUK'] = ev_list['PriceinUK'].str.replace('£', '')
ev_list['PriceinUK'] = ev_list['PriceinUK'].str.replace(',', '')
ev_list['PriceinUK'] = ev_list['PriceinUK'].astype('float')

# Clean Range column data
ev_list['Range'] = ev_list['Range'].str.replace("( ).*", '')
ev_list['Range'] = ev_list['Range'].astype('float')
ev_list['Range'] = ev_list['Range'].astype('int')

# Clean TopSpeed column data
ev_list['TopSpeed'] = ev_list['TopSpeed'].str.replace("( ).*", '')
ev_list['TopSpeed'] = ev_list['TopSpeed'].astype('int')


ev_make = ev_list["Make"].unique().tolist()

app_ui = ui.page_fluid(
    ui.input_selectize("make", "Make", ev_make, selected = "Tesla", multiple=True),
    ui.input_slider("range", "Range km", 100, 700, value=(150, 700)) ,
    ui.input_slider("speed", "Speed kmph", 100, 300, value=(100, 300)),
    ui.output_plot("barchart")
)


def server(input, output, session):
    @output
    @render.plot
    def barchart():
        indx_make = ev_list["Make"].isin(input.make())
        indx_range = ev_list["Range"].isin(range(input.range()[0],input.range()[1]))
        indx_speed = ev_list["TopSpeed"].isin(range(input.speed()[0],input.speed()[1]))

        sub_df = ev_list[indx_make & indx_range & indx_speed]

        #print(sub_df)
        #plot data
        g = sns.catplot(
            data=sub_df,
            kind="bar",
            y="PriceinUK",
            x="Model",
        )

        #format axis labels
        g.set_xticklabels(rotation=90)
        g.set_xlabels("")
        g.set_ylabels("Price")
        
        return g


app = App(app_ui, server)
