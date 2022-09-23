from shiny import App, ui, render
import plotnine as p9
from plotnine.data import diamonds
import pandas as pd

from shiny import App, reactive, render, ui

app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_slider("sampleSize", "Sample Size", min=1, max=len(diamonds), 
                            value=min(1000, len(diamonds)), step=500),
            ui.input_checkbox("jitter", "Jitter", value = True),
            ui.input_checkbox("smooth", "Smooth", value = True),
            ui.input_select("x", "X", list(diamonds)),
            ui.input_select("y", "Y", choices = list(diamonds), selected = list(diamonds)[1]),
            ui.input_select("color", "Color", list(diamonds), selected=None),

            ui.input_select("facet_row", 'Facet Row', list(diamonds.select_dtypes(include='category')), selected=None),
            ui.input_select("facet_column", 'Facet Column', list(diamonds.select_dtypes(include='category')), selected=None)
        ),
        ui.panel_main(
            ui.output_text_verbatim("txt1"),
            ui.output_text_verbatim("txt2"),
            ui.output_plot("myPlot1"),
            ),
    )  
)

def server(input, output, session):
    @reactive.Calc
    def filtered_dataset():
        data = diamonds.sample(input.sampleSize())
        return data


    @output
    @render.text
    def txt1():
        return f'x: {input.x()}'

    @output
    @render.text
    def txt2():
        return f'y: {input.y()}'
    
    # using matplotlib
    @output
    @render.plot
    def myPlot1():
        df = filtered_dataset()

        plot = (
          p9.ggplot(df, p9.aes(x = df[input.x()], y=df[input.y()], color= df[input.color()])) + 
          p9.geom_point()
        )
      
        return plot.draw()

app = App(app_ui, server, debug=True)

