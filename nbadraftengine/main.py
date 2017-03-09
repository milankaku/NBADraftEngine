import pandas
import numpy as np
import matplotlib.pyplot as ppt
import seaborn

import utils

def main():
    draft_df = utils.get_draft_data()

    utils.create_yearly_draft_ws48_plot(draft_df)

    utils.create_round_based_ws48_plot(draft_df)

    utils.create_each_pick_ws48_plot(draft_df)

if __name__ == '__main__':
    main()
