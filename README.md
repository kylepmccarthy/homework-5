# Homework 5 — RDS &amp; Flask App

## Details

* **Optional** but graded
* Will be good practice for final project skills and you'll get feedback
* **Due Dec 3rd** at 11:59pm ET
* Get started here: <https://classroom.github.com/g/YuHo6Min>

## Objectives

Create an HTML application off of a Philadelphia dataset you're interested in by _modifying_ the Vacant Building application we built. All code should be in [GitHub classroom repo](https://classroom.github.com/g/YuHo6Min) like we've done for all past homeworks.

1. Setup a PostgreSQL database and share credentials as a JSON file
2. Load the neighborhoods dataset and other dataset you chose into the database
3. Modify the week 11 app.py to do the following:
   * For `/`
     * Add additional information summarizing the dataset
       * Dataset name
       * Number of rows
     * Modify the dropdown to fill in the dataset categories for the dataset you chose
     * Change the button to direct to new endpoint (e.g., `/bikelane_viewer` or whatever dataset we're looking at)
   * Add a new API endpoint `/bikelane_viewer`
     * Visualize bike lanes or whatever your new dataset is
     * Fill in table with appropriate information
4. Commit all code to a GitHub classroom repo
