import api

def main():
    """
    This module plots average career Win Share per 48 minutes
    based on Draft Year and Draft Pick
    """
    draft_dataframe = api.Drafts()

    draft_dataframe.create_yearly_draft_ws48_plot()

    draft_dataframe.create_round_based_ws48_plot()

    draft_dataframe.create_each_pick_ws48_plot()


if __name__ == '__main__':
    main()
