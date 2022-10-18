from shiny import App, Inputs, Outputs, Session, reactive, render, ui
import pandas as pd
import seaborn as sns
import asyncio

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
            ui.input_action_button("btn", "Press Update", class_="btn-sm"),
        ),
        ui.panel_main(
            ui.output_plot("barchart"),
            ui.output_text_verbatim("mytext_1"),
            ui.output_text_verbatim("mytext_2")
            )
    )
)


def server(input: Inputs, output: Outputs, session: Session):
    
    # Exploring reactive.Value concept
    drive_type = reactive.Value("hello")

    @reactive.Calc
    def filtered_df():
        indx_make = ev_list["Make"].isin(input.make())
        indx_range = ev_list["Range"].isin(range(input.range()[0],input.range()[1]))
        indx_speed = ev_list["TopSpeed"].isin(range(input.speed()[0],input.speed()[1]))
        indx_drive = ev_list["Drive"].isin(input.drive())
        
        sub_df = ev_list[indx_make & indx_range & indx_speed]
        return sub_df

    @output
    @render.plot
    # We want to be able to have the function execute first time and render the plot
    # without pressing the button. So, adding ignore_none=False
    @reactive.event(input.btn, ignore_none=False)
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

    
    @reactive.Effect
    async def my_text_value():
        '''Using reactive effect to set a new value to the reactive value variable'''

        input.btn()        # Take a dependency on the button
        await asyncio.sleep(2) # Wait 2 seconds (to simulate a long computation)
        
        # Exploring setting reactive value within isolate
        with reactive.isolate():
            # Inside this block, we can use input.drive() without taking a
            # dependency on it.
            if not input.drive():
                drive_type.set("None selected")
            else:
                drive_type.set("Atleast one drive type is selected")


    @reactive.Calc
    async def my_text_calc():
        '''Using reactive calculation to return a specific string'''
        input.btn()        # Take a dependency on the button
        await asyncio.sleep(2) # Wait 2 seconds (to simulate a long computation)
        
        # Exploring setting reactive value within isolate
        with reactive.isolate():
            # Inside this block, we can use input.drive() without taking a
            # dependency on it.
            if not input.drive():
                return "None selected"
            else:
                return "Atleast one drive type is selected"



    @output
    @render.text
    async def mytext_1():
        return f"Result: {drive_type()}" # Uses reactive effect


    @output
    @render.text
    async def mytext_2():
        return f"Result: {await my_text_calc()}" # Used reactive calculation

app = App(app_ui, server)
