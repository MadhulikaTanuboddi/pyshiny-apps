import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import plotnine as p9
from plotnine.data import diamonds

from shiny import App, reactive, render, ui

# Notes while working on this app: https://gist.github.com/MadhulikaTanuboddi/6d78bc74d5295fc7b1ee5938973cf52d

diamonds = sns.load_dataset('diamonds')

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
            ui.output_plot("myPlot2")
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

        # Few options to fetch the x and y values from the data frame to render scatter plot
        if input.color() != 'None':
            p = plt.scatter(df[input.x()], df[input.y()], c = df[input.color()])
        # plt.scatter(getattr(df, input.x()), getattr(df, input.y()))
        # df.plot.scatter(x=input.x(), y=input.y(), s=60, c='green')
        
        #TODO: How to make facets works with matplotlib
        # facets = df[input.x()] + '~' + df[input.x()]
    

app = App(app_ui, server, debug=True)

