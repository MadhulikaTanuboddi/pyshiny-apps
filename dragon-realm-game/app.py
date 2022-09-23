from shiny import *
import random

app_ui = ui.page_fluid(
    ui.h1("Intro"),
    ui.p(
        """
        You are in a land full of dragons. In front of you, you see two caves.
        In one cave, the dragon is friendly and will share his treasure with you. 
        The other dragon is greedy and hungry, and will eat you on sight
        """
    ),

    ui.input_action_button("intro_continue", "Continue"),
    
    ui.h1("Question"),
    ui.p("Which cave you want to go into? (1 or 2)"),
    ui.input_action_button("cave_01", "Cave 1"),
    ui.input_action_button("cave_02", "Cave 2"),

    ui.h1("Consequences"),
    #ui.p("win text or lose text"),
    ui.output_text("consequence_text"),

    ui.h1("play again??"),

    ui.input_action_button("play_again", "Play again!"),
    ui.input_action_button("end_game", "No, thank you"),

    ui.input_text("txt", "Enter the text to display below:")

)


def server(input, output, session):

    @reactive.Effect
    @reactive.event(input.intro_continue)
    def _():
        print("Intro continue button is pressed")

    cave_number = reactive.Value(1)
    
    @reactive.Effect
    @reactive.event(input.cave_01)
    def _():
        print("Cave 1 button is pressed")
        cave_number.set(1)

    @reactive.Effect
    @reactive.event(input.cave_02)
    def _():
        print("Cave 2 button is pressed")
        cave_number.set(2)

    
    @output
    @render.text
    def consequence_text():
        #return "cave_number is.. " + str(cave_number())
        return consequences(cave_number())



    @reactive.Effect
    @reactive.event(input.play_again)
    def _():
        print("Play again button is pressed")

    @reactive.Effect
    @reactive.event(input.end_game)
    def _():
        print("No: thank you button is pressed")

    @output
    @render.text
    def text():
        return input.txt()

def consequences(cave_number):
    # friendly dragon == match with cave_number
    options = [1, 2]
    friendly = random.sample(options, 1)
    if cave_number == friendly:
        return "Congratulations, you have a dragon friend!"
    else:
        return "Womp womp you've been eaten by a hungry dragon"

    


app = App(app_ui, server)

#' Flowchart
#'  Start (mash with intro text for round 1)
#'  Introductory text
#'  Player chooses a cave
#'  Check for a hungry dragon or a friendly dragon
#'    - player wins
#'    - player loses
#'  Ask to play again
#'    - if yes, go to start
#'    - else:
#'      -- End
