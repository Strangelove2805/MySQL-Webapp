"""Table data processing functions"""

import pandas as pd


def grab_metrics(data: list) -> tuple:
    """Makes the data a bit more useful

    Input Parameters:
    -----------------
    data            Type:   list
                    Use:    Unprocessed in-data from the MySQL server

    Output Parameters:
    -----------------

    metrics         Type:   tuple
                    Use:    Tuple of processed bits of data. Specifically
                            user scores, locations and application status
    """
    scores = []
    lat = []
    lon = []
    status = {"Accepted": 0,
              "Rejected": 0,
              "Withdrawn": 0,
              "Shortlisted": 0}

    for row in data:

        scores.append(row[3])
        lat.append(row[6])
        lon.append(row[7])
        status[row[4]] += 1

    return (scores, lat, lon, status)


def process(data: list, columns: tuple) -> tuple:
    """Puts all the data into nice dataframes to be displayed. Sorted by
       score, highest to lowest

    Input Parameters:
    -----------------
    data            Type:   list
                    Use:    Unprocessed in-data from the MySQL server

    columns         Type:   tuple
                    Use:    Tuple of column names. This isn't used so
                            don't worry about it

    Output Parameters:
    -----------------

    dataframes      Type:   tuple
                    Use:    Tuple of 3 dataframes, one for the score chart,
                            one for the status chart and the last for a map
    """
    data.sort(key=lambda row: row[3], reverse=False)

    metrics = grab_metrics(data)

    dict_scores = {"Scores": metrics[0]}
    dict_latlong = {"latitude": metrics[1], "longitude": metrics[2]}

    df_scores = pd.DataFrame(dict_scores)
    df_map = pd.DataFrame(dict_latlong)
    df_status = pd.DataFrame([metrics[3]])

    return (df_scores, df_map, df_status)
