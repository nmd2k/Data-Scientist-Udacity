## Preparation
Create a Python 3.9 virtual environment and activate it:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies via `pip`:

```bash
pip install -r requirements.txt
```

The dataset contains 3 files, located in the `./data` folder:
- `data/calendar.csv`
- `data/listings.csv`
- `data/reviews.csv`

## Project Motivation

I was interested in conducting exploratory data analysis using an Airbnb Seattle dataset containing listings, reviews, and calendar data to better understand:

-	What is the general vibe of each Seattle neighborhood based on listing descriptions?
-	When are the busiest times of the year to visit Seattle, and how much do prices increase during these periods?
-	Are there price differences across neighborhoods, and which areas tend to be more expensive?
-	How do reviews and sentiment vary across different neighborhoods and property types?

I wanted the opportunity to explore the data and communicate my findings in an engaging way, providing insights into these key questions.

## File Descriptions
There is one exploratory notebook available here to showcase my work related to the questions posed. Markdown cells were used throughout to explain the process taken.

## Blog Post
The main findings of the code can be found at my Medium blog post available [here](https://nmd2k.medium.com/exploring-seattles-airbnb-scene-through-data-147ce465f153).

## Acknowledgement
This dataset is part of Airbnb Inside, and the original source can be found [here](http://insideairbnb.com/get-the-data.html).