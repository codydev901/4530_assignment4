import pandas as pd
import plotly.express as px

"""
Cody Whitt
pkz325
CPSC 4530 Spring 2023
Assignment 4

For Dataset 1 - Tree Based (Used Treemap to visualize relationship between bombs dropped between theater/aircraft)

https://plotly.com/python/treemaps/
"""


def parse_data():
    """
    Parse step for DataSet 1
    """

    # Load in raw data, do basic check
    raw_df = pd.read_csv("raw_data/operations.csv")
    print(raw_df.head())
    print(raw_df.info())

    # Drop attributes we are not interested in
    keep_attributes = ["Mission ID", "Theater of Operations", "Aircraft Series", "High Explosives Weight (Tons)"]
    raw_df = raw_df[keep_attributes]
    raw_df.dropna(inplace=True)
    print(raw_df.head())
    print(raw_df.info())

    # Rename attributes
    raw_df = raw_df.rename(columns={"Mission ID": "mission_id", "Theater of Operations": "theater",
                                    "Aircraft Series": "aircraft", "High Explosives Weight (Tons)": "bomb_tonnage"})
    print(raw_df.head())
    print(raw_df.info())

    # Quick Check Theater/Tonnage
    print(raw_df.groupby(by=["theater"])["bomb_tonnage"].sum())

    # Drop EAST AFRICA -- we'll just look at the highest 4 theaters (may end up dropping CBI later)
    raw_df = raw_df[~raw_df["theater"].isin(["EAST AFRICA"])]
    print(raw_df.head())
    print(raw_df.info())
    print(raw_df.groupby(by=["theater"])["bomb_tonnage"].sum())

    # Create DF for plotting (Only include aircraft > 0.05% use in each theater)
    parsed_df = [["theater", "aircraft", "bomb_tonnage", "bomb_tonnage_theater_percent",
                  "bomb_tonnage_overall_percent"]]

    sum_tonnage = raw_df["bomb_tonnage"].sum()  # Percent showing that theater/aircraft pair to overall war
    t_a_threshold = 0.005  # Threshold to include

    # Group by theater/aircraft
    for theater in list(raw_df["theater"].unique()):
        theater_df = raw_df[raw_df["theater"] == theater]
        total_tonnage = theater_df["bomb_tonnage"].sum()
        print(theater)
        for aircraft in list(theater_df["aircraft"].unique()):
            theater_aircraft_df = theater_df[theater_df["aircraft"] == aircraft]
            theater_aircraft_tonnage = theater_aircraft_df["bomb_tonnage"].sum()
            t_a_ratio = theater_aircraft_tonnage / total_tonnage
            sum_tonnage_ratio = theater_aircraft_tonnage / sum_tonnage
            if t_a_ratio > t_a_threshold:
                print(aircraft, t_a_ratio, sum_tonnage_ratio)
                parsed_df.append([theater, aircraft, theater_aircraft_tonnage, t_a_ratio, sum_tonnage_ratio])

    # Write to Parsed
    parsed_df = pd.DataFrame(data=parsed_df[1:], columns=parsed_df[0])
    parsed_df.to_csv("parsed_data/ww2_bomb_parsed.csv", index=False)

    print("Parsed/Wrote WW2")


def plot_data():
    """
    Plot step for DataSet 1
    """

    # Read DF
    df = pd.read_csv("parsed_data/ww2_bomb_parsed.csv")
    print(df.head())

    # Plot Treemap
    fig = px.treemap(df, path=[px.Constant("Theater"), 'theater', 'aircraft'], values='bomb_tonnage',
                     title="WW2 Allied Bomb Tonnage By Theater/Aircraft")
    fig.update_traces(root_color="lightgrey")
    fig.show()


def main():

    parse_data()

    plot_data()


if __name__ == "__main__":

    main()

