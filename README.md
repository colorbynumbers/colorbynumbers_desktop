# Color by numbers

## A project from two students from the university of applied sciences(HTWG) in constance.

This program computes a painting-by-numbers template from pictures your choice.

## Installation

For now there is no installer yet.
So here are the steps to get the application running.

First of all you need to download the repository and unzip it.
Then you need to have anaconda installed on your machine. [Anaconda Download Page](https://www.anaconda.com/distribution/)

### GNU/Linux or MacOS

Open up a shell and navigate to the root of the repository and run the command ```./run.sh```.
This shell-script sets everything up for you and starts the application.

### Windows

#### 1. Environment Setup

    These steps only have to be taken once.

1. Press the windows key and search for ```Anaconda Prompt``` and execute it.
1. Use the command ```conda init``` to make the command ```conda``` available in the Command Prompt.
1. Change the directory to your root of the downloaded application.
1. Use the command ```conda env list``` to list all virtual environments and check if there is the environment ```cbn``` installed.
1. If the environment ```cbn``` is not installed, use the command ```conda env create -f environment.yml``` to setup everything the application needs.

#### 2. Start application

1. Open up ```Command Prompt``` or ```Anaconda Prompt```.
1. Change the directory to the folder ```src/``` that is located in the root of the downloaded repository.
1. Run ```conda activate cbn``` to activate the virtual environment.
1. Start the application with ```python ColorByNumber.py```.

## How to use

1. Start the program.
2. Browse a picture or photo of your choice.
3. Makes some configurations and press start.
    :sparkles:magic:sparkles:
4. Press export and print it.
5. Color your photo and enjoy! :smile:

## Contributors

[Lionel Kornberger](https://github.com/SpurNut "GitHub Account")

[Samantha Isted](https://github.com/sammyCatlady42 "GitHub Account")
