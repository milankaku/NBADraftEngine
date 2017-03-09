import nbadraftengine.utils as utils


def main():
    """
    This module plots average career Win Share per 48 minutes
    based on Draft Year and Draft Pick
    """
    draft_df = utils.get_draft_data()

    utils.create_yearly_draft_ws48_plot(draft_df)

    utils.create_round_based_ws48_plot(draft_df)

    utils.create_each_pick_ws48_plot(draft_df)


if __name__ == '__main__':
    main()
