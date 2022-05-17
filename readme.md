# IRS Code Challenge

My solution to creating two utility functions for searching IRS tax forms

## Assumptions

1. For both utility functions, the company only wants to keep track of the english versions of each Tax Form
1. The company would like the return object of the first utility function in a separate file for the option to parse later

## Solution formulation

Steps I thought of and executed for implementing both utility functions:

1. Use a global variable: `recoded_forms` to aid first function in updating recorded tax forms accordingly

2. Create a main() function that:
   1. uses pagination principle to query IRS website, getting max 200 forms a time
   2. call both utility functions, passing in 200 rows of tax forms a time
3. For first utility function `get_form_info` :
   1. loop through each form given to the argument and check if form is an english version
   2. add english form to `recorded_forms` variable
   3. if english form has already been added, update the `max_year` and `min_year` accordingly
   4. for faster lookup, each form is being recorded in `recorded_forms` variable with the following format:
      - {Publ 1: {
        "form_number": "Publ 1",
        "form_title": "Your Rights As A Taxpayer",
        "min_year": 1996,
        "max_year": 2017
        }, ...} : with this format, we only need to search for the form name instead of looping through an array of tax form information
4. For second utility function `save_form_pdf` :
   1. loop through each form pdf and check for english versions
   2. accommodate for large pdf files by using `iter_content()` method to write 1024 bits a time

## Libraries/Tools used

- Written with `Python` version 3.10.0
- `loguru` version 0.5.3
- `lxml` version 4.6.4 (parser)
- `beautifulsoup4` version 4.10.0
- `requests` version 2.26.0

## How to setup

Run the following commands to set up, given `python3` is installed and on project directory:

1. cd { local directory }/"Pinwheel Code Challenge"
2. pip3 install -r requirements.txt
3. python3 main.py
4. Loading message will appear if script successfully starts
5. Script make take a couple of minutes to finish running

![Code Coverage](https://user-images.githubusercontent.com/55603364/140648392-a6368bcb-61b8-4d74-afe7-e3e13154f254.jpeg)

## Decisions

1. Inputs for both utility functions is: `rows` parameter, which can have a max number of 200 html tax form objects stored
2. Output for first utility function is stored in FormData_Results folder in data.json file
3. Output for second utility function is stored under Downloaded_PDFs folder
4. VENV python folder
   - Virtual Environment should be used whenever you work on any Python based project
