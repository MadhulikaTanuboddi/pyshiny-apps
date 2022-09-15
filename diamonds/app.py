import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from shiny import App, render, ui

diamonds = sns.load_dataset('diamonds')

app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_text("x", "Text input", placeholder="Enter text"),
            ui.input_slider("sampleSize", "Sample Size", min=1, max=len(diamonds), 
                            value=min(1000, len(diamonds)), step=500),
            ui.input_checkbox("jitter", "Jitter", value = True),
            ui.input_checkbox("smooth", "Smooth", value = True),
            ui.input_select("x", "X", list(diamonds)),
            ui.input_select("y", "Y", choices = list(diamonds), selected = list(diamonds)[1]),
            ui.input_select("color", "Color", list(diamonds), selected=None),

            ui.input_select("facet_row", 'Facet Row', list(diamonds.select_dtypes(include='category')), selected=None),
            ui.input_select("facet_row", 'Facet Row', list(diamonds.select_dtypes(include='category')), selected=None)
        ),
        ui.panel_main(
            ui.output_text_verbatim("txt"),
            ui.output_plot("myPlot1")
            ),
    )  
)

def server(input, output, session):
    @output
    @render.text
    def txt():
        return f'x: "{input.x()}"'

    @output
    @render.plot
    def myPlot1(alt="A histogram"):
        np.random.seed(19680801)
        x = 100 + 15 * np.random.randn(437)

        fig, ax = plt.subplots()
        ax.hist(x, input.sampleSize(), density=True)
        return fig


app = App(app_ui, server, debug=True)

