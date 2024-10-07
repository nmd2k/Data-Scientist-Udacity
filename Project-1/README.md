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

-	What kinds of properties are most common in Seattle, and which neighborhoods have the highest concentration of listings?
-	What is the price distribution of Airbnb listings in Seattle, and what are typical prices?
-	How does room type affect pricing, and which room types are most common in Seattle?
-	When is the best time to visit Seattle based on availability and review activity?

I wanted the opportunity to explore the data and communicate my findings in an engaging way, providing insights into these key questions.

## File Descriptions
There is one exploratory notebook available here to showcase my work related to the questions posed. Markdown cells were used throughout to explain the process taken.

## Blog Post
The main findings of the code can be found at my Medium blog post available [here](https://nmd2k.medium.com/exploring-seattles-airbnb-scene-through-data-147ce465f153).

## Acknowledgement
This dataset is part of Airbnb Inside, and the original source can be found [here](http://insideairbnb.com/get-the-data.html).