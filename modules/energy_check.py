from codecarbon import EmissionsTracker
from codecarbon import track_emissions
import os

@track_emissions(save_to_file=True, output_file="aaaaa.txt")
def calc_energy(tracker):
    for i in range(0, 10):
        os.system("dir")


def get_tracker(path):
    tracker = EmissionsTracker(output_file=path)

    return tracker