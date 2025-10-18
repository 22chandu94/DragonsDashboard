import pandas as pd

def merge_cricket_stats(*dfs):
    """
    Merge any number of cricket stats DataFrames and sum relevant stats.

    Parameters:
        *dfs: Two or more pandas DataFrames with similar structure (cricket stats).

    Returns:
        A merged and cleaned DataFrame with combined stats.
    """
    if len(dfs) < 2:
        raise ValueError("You must provide at least 2 dataframes.")

    # Step 1: Generate suffixes dynamically
    suffixes = [''] + [f'_{i}' for i in range(1, len(dfs))]

    # Step 2: Merge all DataFrames using outer join on 'player_id'
    merged = dfs[0].copy()
    for i in range(1, len(dfs)):
        merged = pd.merge(
            merged, dfs[i], on='player_id', how='outer',
            suffixes=('', suffixes[i])
        )

    # Step 3: Prepare numeric columns to sum
    numeric_cols = ['total_match', 'innings', 'total_runs', 'not_out',
                    'ball_faced', '4s', '6s', '50s', '100s']

    for col in numeric_cols:
        col_variants = [f"{col}{suffix}" for suffix in suffixes if f"{col}{suffix}" in merged.columns]
        merged[col] = merged[col_variants].fillna(0).sum(axis=1)

    # Step 4: highest_run — take max across columns
    highest_run_cols = [f"highest_run{suffix}" for suffix in suffixes if f"highest_run{suffix}" in merged.columns]
    merged['highest_run'] = merged[highest_run_cols].fillna(0).max(axis=1)

    # Step 5: Recalculate average and strike rate
    dismissals = (merged['innings'] - merged['not_out']).replace(0, 1)
    merged['average'] = (merged['total_runs'] / dismissals).round(2)
    merged['strike_rate'] = (merged['total_runs'] / merged['ball_faced'].replace(0, 1) * 100).round(2)

    # Step 6: Combine metadata (name, team_name, batting_hand)
    metadata_cols = ['name', 'team_name', 'batting_hand']
    for col in metadata_cols:
        col_variants = [f"{col}{suffix}" for suffix in suffixes if f"{col}{suffix}" in merged.columns]
        merged[col] = merged[col_variants[0]]
        for other_col in col_variants[1:]:
            merged[col] = merged[col].combine_first(merged[other_col])

    # Step 7: Final column selection
    final_cols = ['player_id', 'name', 'team_name', 'total_match', 'innings', 'total_runs',
                  'highest_run', 'average', 'not_out', 'strike_rate', 'ball_faced', 'batting_hand',
                  '4s', '6s', '50s', '100s']

    final_df = merged[final_cols].copy()

    # Ensure strike_rate and average are rounded
    final_df['strike_rate'] = final_df['strike_rate'].round(2)
    final_df['average'] = final_df['average'].round(2)

    # Convert all other numeric columns to integers where applicable
    exclude_cols = ['strike_rate', 'average']
    for col in final_df.columns:
        if col not in exclude_cols:
            try:
                if pd.api.types.is_numeric_dtype(final_df[col]):
                    final_df[col] = final_df[col].fillna(0).astype('Int64')  # Nullable integer type
            except Exception as e:
                print(f"Error converting column {col} to integer: {e}")

    # Step 8: Sort and reset index
    final_df = final_df.sort_values(by='total_runs', ascending=False).reset_index(drop=True)

    return final_df


if __name__ == '__main__':
    the_hundred = pd.read_csv("Data/The_Hunderd/batting_theHundred.csv")
    the_hundred.drop(['team_id'], axis=1, inplace=True)
    df1 = the_hundred[the_hundred["team_name"] == "SPVGG Dragons"].reset_index()

    beer_cup = pd.read_csv("Data/Beer_Cup/1397502_batting_leaderboard.csv")
    beer_cup.drop(['team_id'], axis=1, inplace=True)
    df2 = beer_cup[beer_cup["team_name"] == "SPVGG Dragons"].reset_index()

    t20 = pd.read_csv("Data/T20/1563884_batting_leaderboard.csv")
    t20.drop(['team_id'], axis=1, inplace=True)
    df3 = t20[t20["team_name"] == "SPVGG Dragons"].reset_index()

    trebur_cup = pd.read_csv("Data/Trebur_Cup/1397148_batting_leaderboard.csv")
    trebur_cup.drop(['team_id'], axis=1, inplace=True)
    df4 = trebur_cup[trebur_cup["team_name"] == "SPVGG Dragons"].reset_index()

    challengers_cup = pd.read_csv("Data/Challengers_Cup/1423920_batting_leaderboard.csv")
    challengers_cup.drop(['team_id'], axis=1, inplace=True)
    df5 = challengers_cup[challengers_cup["team_name"] == "SPVGG Dragons"].reset_index()

    liga = pd.read_csv("Data/Liga/batting_liga.csv")
    df6 = liga[liga["team_name"] == "SPVGG Dragons"].reset_index()

    rs_cup = pd.read_csv("Data/RS_Cup/batting_rs_cup.csv")
    df7 = liga[liga["team_name"] == "SPVGG Dragons"].reset_index()

    result = merge_cricket_stats(df1, df2, df3, df4, df5, df6, df7)
    result.drop(['player_id'], axis=1, inplace=True)
    result.columns = ["Name", "Team", "Matches", "Innings", "Runs", "Highest", "Average", "Not Outs", "Strike Rate",
                      "Balls Faced", "Batting Hand", "4s", "6s", "50s", "100s"]
    result.to_csv("final_batting_data.csv", index=False, encoding="utf-8")
    print(result.to_string())