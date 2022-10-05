from shiny import App, Inputs, Outputs, Session, reactive, render, ui
import pandas as pd
import seaborn as sns

from pathlib import Path

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
    # Title
    ui.h1("Electric cars"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_selectize("make", "Make", ev_make, selected = "Tesla", multiple=True),
            ui.input_slider("range", "Range km", 100, 700, value=(150, 700)) ,
            ui.input_slider("speed", "Speed kmph", 100, 300, value=(100, 300)),
            ui.input_checkbox_group(
                "drive", "Drive type", {"fw": "Front Wheel", "rw": "Rear Wheel", "aw": "All Wheel" }
            ),
            ui.input_action_button("btn", "Update", class_="btn-sm"),
        ),
        ui.panel_main(ui.output_plot("barchart"))
    )
)


def server(input: Inputs, output: Outputs, session: Session):
    @reactive.Calc
    def filtered_df():
        indx_make = ev_list["Make"].isin(input.make())
        indx_range = ev_list["Range"].isin(range(input.range()[0],input.range()[1]))
        indx_speed = ev_list["TopSpeed"].isin(range(input.speed()[0],input.speed()[1]))
        indx_drive = ev_list["Drive"].isin(input.drive())
        
        sub_df = ev_list[indx_make & indx_range & indx_speed]
        return sub_df
        
        
        # sub_df = ev_list[indx_make & indx_range & indx_speed & indx_drive]
        # result = min(sub_df, default="EMPTY")
        # return result


    @output
    @render.plot
    @reactive.event(input.btn)
    def barchart():
        g = sns.catplot(
            data=filtered_df(),
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
