import pandas as pd


def merge_fielding_stats(*dfs):
    """
    Merge multiple fielding DataFrames and calculate cumulative statistics.

    Parameters:
        *dfs: Two or more pandas DataFrames with similar structure (fielding stats).

    Returns:
        A merged and cleaned DataFrame with combined fielding stats.
    """
    if len(dfs) < 2:
        raise ValueError("You must provide at least 2 dataframes.")

    # --- Step 1: Normalize column names ---
    rename_map = {
        'team_name': 'team',
        'total_match': 'matches',
        'caught_behind': 'caught_behind',
        'run_outs': 'run_outs',
        'assist_run_outs': 'assist_run_outs',
        'stumpings': 'stumpings',
        'caught_and_bowl': 'caught_and_bowled',
        'total_catches': 'total_catches',
        'total_dismissal': 'total_dismissals'
    }

    def normalize_cols(df):
        df = df.rename(columns=lambda c: c.strip().replace(" ", "_").lower())
        df = df.rename(columns=rename_map)
        if 'name' in df.columns:
            df['name'] = df['name'].astype(str).str.strip().str.replace(r'\s+', ' ', regex=True)
        return df

    dfs = [normalize_cols(df.copy()) for df in dfs]

    # --- Step 2: Merge using player_id if present, else fallback to name ---
    merged = dfs[0]
    for i in range(1, len(dfs)):
        common_keys = [k for k in ['player_id', 'name'] if k in merged.columns and k in dfs[i].columns]
        merged = pd.merge(merged, dfs[i], on=common_keys, how='outer', suffixes=('', f'_{i}'))

    # --- Step 3: Numeric columns to sum cumulatively ---
    numeric_cols = [
        "matches", "catches", "caught_behind", "run_outs", "assist_run_outs",
        "stumpings", "caught_and_bowled", "total_catches", "total_dismissals"
    ]

    for col in numeric_cols:
        col_variants = [c for c in merged.columns if c.startswith(col)]
        if col_variants:
            merged[col] = merged[col_variants].apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1)

    # --- Step 4: Metadata (team) ---
    if "team" in merged.columns:
        merged["team"] = merged[[c for c in merged.columns if c.startswith("team")]].bfill(axis=1).iloc[:, 0].fillna('-')

    # --- Step 5: Derived metrics ---
    merged["catches_per_match"] = merged.apply(
        lambda x: round(x["total_catches"] / x["matches"], 2) if x["matches"] > 0 else 0.0, axis=1
    )

    merged["dismissals_per_match"] = merged.apply(
        lambda x: round(x["total_dismissals"] / x["matches"], 2) if x["matches"] > 0 else 0.0, axis=1
    )

    # --- Step 6: Clean & reorder final columns ---
    final_cols = [
        "player_id", "name", "team", "matches", "catches", "caught_behind", "run_outs",
        "assist_run_outs", "stumpings", "caught_and_bowled", "total_catches", "total_dismissals",
        "catches_per_match", "dismissals_per_match"
    ]

    existing_cols = [c for c in final_cols if c in merged.columns]
    final_df = merged[existing_cols].copy()

    # --- Step 7: Type cleanup ---
    int_cols = ["matches", "catches", "caught_behind", "run_outs", "assist_run_outs",
                "stumpings", "caught_and_bowled", "total_catches", "total_dismissals"]
    for col in int_cols:
        if col in final_df.columns:
            final_df[col] = final_df[col].fillna(0).astype(int)

    # --- Step 8: Sort & return ---
    final_df = final_df.sort_values(
        by=["total_dismissals", "total_catches"], ascending=[False, False]
    ).reset_index(drop=True)

    final_df.columns = [
        "Player ID", "Player Name", "Team", "Matches", "Catches", "Caught Behind",
        "Run Outs", "Assist Run Outs", "Stumpings", "Caught & Bowled",
        "Total Catches", "Total Dismissals", "Catches/Match", "Dismissals/Match"
    ]

    return final_df


if __name__ == '__main__':
    beer_cup = pd.read_csv("Data/Beer_Cup/1397502_fielding_leaderboard.csv")
    beer_cup.drop(['team_id'], axis=1, inplace=True)
    df1 = beer_cup[beer_cup["team_name"] == "SPVGG Dragons"]

    challengers_cup = pd.read_csv("Data/Challengers_Cup/1423920_fielding_leaderboard.csv")
    challengers_cup.drop(['team_id'], axis=1, inplace=True)
    df2 = challengers_cup[challengers_cup["team_name"] == "SPVGG Dragons"]

    t20 = pd.read_csv("Data/T20/1563884_fielding_leaderboard.csv")
    t20.drop(['team_id'], axis=1, inplace=True)
    df3 = t20[t20["team_name"] == "SPVGG Dragons"]

    the_hundred = pd.read_csv("Data/The_Hunderd/fielding_theHundred.csv")
    the_hundred.drop(['team_id'], axis=1, inplace=True)
    df4 = the_hundred[the_hundred["team_name"] == "SPVGG Dragons"]

    trebur_cup = pd.read_csv("Data/Trebur_Cup/1397148_fielding_leaderboard.csv")
    trebur_cup.drop(['team_id'], axis=1, inplace=True)
    df5 = trebur_cup[trebur_cup["team_name"] == "SPVGG Dragons"]

    result = merge_fielding_stats(df1, df2, df3, df4, df5)
    result.to_csv("final_fielding_data.csv", index=False, encoding="utf-8")
    print(result.to_string())
