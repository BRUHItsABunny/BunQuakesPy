###########################################################
# Author: BRUHItsABunny                                   #
# Bunnystyle version of github.com/maximilionis/muwa      #
###########################################################
import numpy as np
import matplotlib.pyplot as plt


def get_date(date_str: str):
    if "/" in date_str:
        # 2/22/75
        str_split = date_str.split("/")
        day = int(str_split[1])
        month = int(str_split[0])
        year = int(str_split[2])
    else:
        # 1975-02-23T02:58:41.000Z (earthquakes.txt:3379)
        str_split = date_str.split("-")
        day = int(str_split[2].split("T")[0])
        month = int(str_split[1])
        year = int(str_split[0][-2:].join(""))
    return day, month, year


def main():

    filename = "earthquakes.txt"
    full_array = np.genfromtxt(filename, delimiter=",", dtype=str)
    fast_lookup = {}

    for quake in full_array:
        _,  month, year = get_date(str(quake[0]))
        if year <= 70:
            if year not in fast_lookup:
                fast_lookup[year] = {}
            if month not in fast_lookup[year]:
                fast_lookup[year][month] = np.empty(shape=(0, 7), dtype=str)
            fast_lookup[year][month] = np.append(arr=fast_lookup[year][month], values=[quake], axis=0)
        else:
            break

    del full_array
    plot_number = 1
    np_months = np.array([
        "\nJan", "Feb", "\nMar", "Apr",
        "\nMay", "Jun", "\nJul", "Aug",
        "\nSep", "Oct", "\nNov", "Dec"
    ])

    fig = plt.figure()
    fig.set_size_inches(8, 10, forward=True)
    for year in fast_lookup.keys():
        averages = np.empty(shape=1, dtype=float)
        for month in range(1, 12):
            month_count = float(len(fast_lookup[year][month]))
            month_magnitude = 0.0
            for quake in fast_lookup[year][month]:
                month_magnitude += float(quake[6])
            # print("Dividing %f by %f" % (month_magnitude, month_count))
            averages = np.append(arr=averages, values=[(month_magnitude / month_count)], axis=0)
        plt.subplot(3, 2, plot_number)
        plt.yticks(np.arange(0, 8, 1))
        plt.plot(np_months, averages, "ro")
        plt.title("Average Magnitude 19%i" % year)
        plot_number += 1
    plt.show()


if __name__ == '__main__':
    main()
