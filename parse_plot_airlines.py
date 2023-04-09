import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx

"""
Cody Whitt
pkz325
CPSC 4530 Spring 2023
Assignment 4

For Dataset 2 - Network (used node-edge to show airline connections and average flight delay)
"""


def parse_data():
    """
    Parse step for Dataset 2
    """

    # Load in raw data, do basic check
    raw_df = pd.read_csv("raw_data/flights.csv")
    print(raw_df.head())
    print(raw_df.info())

    # Filter to just Delta
    raw_df = raw_df[raw_df["AIRLINE"] == "DL"]
    print(raw_df.head())
    print(raw_df.info())

    # Filter to relevant attributes
    raw_df = raw_df[["AIRLINE", "ORIGIN_AIRPORT", "DESTINATION_AIRPORT", "DEPARTURE_DELAY", "ARRIVAL_DELAY"]]
    raw_df.dropna(inplace=True)
    print(raw_df.head())
    print(raw_df.info())

    parsed_df = [["origin_airport", "destination_airport", "num_flights", "average_delay"]]

    # Group by edge's, filter out pairs with < daily flights. Calc average delay
    for origin_airport in list(raw_df["ORIGIN_AIRPORT"].unique()):
        origin_df = raw_df[raw_df["ORIGIN_AIRPORT"] == origin_airport]
        for destination_airport in list(origin_df["DESTINATION_AIRPORT"].unique()):
            origin_destination_df = origin_df[(origin_df["ORIGIN_AIRPORT"] == origin_airport) &
                                              (origin_df["DESTINATION_AIRPORT"] == destination_airport)]
            num_flights = len(origin_destination_df)
            if num_flights >= 365:
                average_delay = (origin_destination_df["DEPARTURE_DELAY"].mean() + origin_destination_df["ARRIVAL_DELAY"].mean()) / 2.0
                parsed_df.append([origin_airport, destination_airport, num_flights, average_delay])

    # Spot check above transformation
    parsed_df = pd.DataFrame(data=parsed_df[1:], columns=parsed_df[0])
    print(parsed_df.head())
    print(parsed_df.info())

    # Check Average Delay
    parsed_df.sort_values(by=["average_delay"], inplace=True)
    print(parsed_df.head())

    # Get List of VALID airports
    valid_airport_df = pd.read_csv("raw_data/airports.csv")
    valid_airports = list(valid_airport_df["IATA_CODE"].unique())
    print(valid_airports)

    # Filter out potentially invalid origin/destination airports
    parsed_df = parsed_df[(parsed_df["origin_airport"].isin(valid_airports)) &
                          (parsed_df["destination_airport"].isin(valid_airports))]
    print(parsed_df.head())
    print(parsed_df.info())

    # Re-Check Average Delay
    parsed_df.sort_values(by=["average_delay"], inplace=True)
    print(parsed_df.head())

    parsed_df.to_csv("parsed_data/flights_parsed.csv", index=False)
    print("Wrote Parsed Flights")


def plot_data():
    """
    Plot step for dataset 2

    Some links I found helpful for this, since don't typically use networkx
    https://stackoverflow.com/questions/17632151/coloring-networkx-edges-based-on-weight
    https://networkx.org/documentation/stable/reference/classes/multidigraph.html
    https://stackoverflow.com/questions/17051589/parsing-through-edges-in-networkx-graph
    """

    # Read DF
    df = pd.read_csv("parsed_data/flights_parsed.csv")

    # Convert delay to RGBA color using colorscale
    c_map = plt.get_cmap('bwr')
    c_norm = colors.Normalize(vmin=df["average_delay"].min(), vmax=df["average_delay"].max())
    scalar_map = cmx.ScalarMappable(norm=c_norm, cmap=c_map)
    df["average_delay_color"] = df["average_delay"].apply(lambda x: scalar_map.to_rgba(x))

    # Since edge were not in order, make a lookup.. (that was fun to debug)
    edge_color_dict = {}
    for i, row in df.iterrows():
        try:
            edge_color_dict[row["origin_airport"]][row["destination_airport"]] = row["average_delay_color"]
        except KeyError:
            edge_color_dict[row["origin_airport"]] = {}
            edge_color_dict[row["origin_airport"]][row["destination_airport"]] = row["average_delay_color"]

    # Plot Construction
    G = nx.from_pandas_edgelist(df, 'origin_airport', 'destination_airport', create_using=nx.MultiDiGraph())
    plt.title("Delta Airlines Flight Connections and Average Delay")

    # Edge colormap in correct order...
    edge_colors = []
    for e in G.edges():
        edge_colors.append(edge_color_dict[e[0]][e[1]])

    nx.draw_spring(G, with_labels=True, node_color='skyblue', node_size=150, width=1.0,
                   font_size=6, edge_color=edge_colors)
    plt.show()


def main():

    # parse_data()

    plot_data()


if __name__ == "__main__":

    main()