import pandas as pd

def merge_bowling_stats(*dfs):
    """
    Merge multiple bowling DataFrames and calculate cumulative statistics.

    Parameters:
        *dfs: Two or more pandas DataFrames with similar structure (bowling stats).

    Returns:
        A merged and cleaned DataFrame with combined bowling stats.
    """
    if len(dfs) < 2:
        raise ValueError("You must provide at least 2 dataframes.")

    # --- Step 1: Normalize column names ---
    rename_map = {
        'team_name': 'team',
        'total_match': 'matches',
        'total_wickets': 'wickets',
        'balls': 'balls_bowled',
        'runs': 'runs_conceded',
        'maidens': 'maiden_overs',
        'overs': 'overs_bowled',
        'highest_wicket': 'highest_wickets'
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
        "matches", "innings", "wickets", "balls_bowled", "runs_conceded",
        "maiden_overs", "dot_balls", "overs_bowled"
    ]

    for col in numeric_cols:
        col_variants = [c for c in merged.columns if c.startswith(col)]
        if col_variants:
            merged[col] = merged[col_variants].apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1)

    # --- Step 4: Highest wickets → max across tournaments ---
    high_cols = [c for c in merged.columns if c.startswith("highest_wickets")]
    if high_cols:
        merged["highest_wickets"] = merged[high_cols].apply(pd.to_numeric, errors='coerce').fillna(0).max(axis=1)

    # --- Step 5: Metadata (team, bowling_style) ---
    for meta_col in ["team", "bowling_style"]:
        col_variants = [c for c in merged.columns if c.startswith(meta_col)]
        if col_variants:
            merged[meta_col] = merged[col_variants].bfill(axis=1).iloc[:, 0].fillna('-')

    # --- Step 6: Derived metrics ---
    merged["economy"] = merged.apply(
        lambda x: round(x["runs_conceded"] / x["overs_bowled"], 2)
        if x["overs_bowled"] > 0 else 0.0, axis=1)

    merged["average"] = merged.apply(
        lambda x: round(x["runs_conceded"] / x["wickets"], 2)
        if x["wickets"] > 0 else 0.0, axis=1)

    merged["strike_rate"] = merged.apply(
        lambda x: round(x["balls_bowled"] / x["wickets"], 2)
        if x["wickets"] > 0 else 0.0, axis=1)

    # --- Step 7: Clean & reorder final columns ---
    final_cols = [
        "player_id", "name", "team", "matches", "innings", "wickets", "highest_wickets",
        "runs_conceded", "balls_bowled", "overs_bowled", "maiden_overs", "dot_balls",
        "economy", "average", "strike_rate", "bowling_style"
    ]

    existing_cols = [c for c in final_cols if c in merged.columns]
    final_df = merged[existing_cols].copy()

    # --- Step 8: Data cleanup ---
    int_cols = ["matches", "innings", "wickets", "highest_wickets", "balls_bowled",
                "maiden_overs", "dot_balls", "runs_conceded"]
    for col in int_cols:
        if col in final_df.columns:
            final_df[col] = final_df[col].fillna(0).astype(int)

    if "overs_bowled" in final_df.columns:
        final_df["overs_bowled"] = final_df["overs_bowled"].fillna(0).round(1)

    # --- Step 9: Sort & return ---
    final_df = final_df.sort_values(by=["wickets", "economy"], ascending=[False, True]).reset_index(drop=True)

    # --- Step 10: Remove players who have not bowled ---
    final_df = final_df[final_df["balls_bowled"] > 0].reset_index(drop=True)
    final_df.columns = [
        "Player ID", "Player Name", "Team", "Matches", "Innings", "Wickets",
        "Best Bowling", "Runs Conceded", "Balls Bowled", "Overs Bowled",
        "Maidens", "Dot Balls", "Economy", "Average", "Strike Rate", "Bowling Style"
    ]
    #final_df.drop(["Player ID"], axis=1, inplace=True)

    return final_df



# === EXAMPLE USAGE ===
if __name__ == "__main__":
    # Load CSVs
    beer_cup = pd.read_csv("Data/Beer_Cup/1397502_bowling_leaderboard.csv")
    beer_cup.drop(['team_id'], axis=1, inplace=True)
    df1 = beer_cup[beer_cup["team_name"] == "SPVGG Dragons"]

    challengers_cup = pd.read_csv("Data/Challengers_Cup/1423920_bowling_leaderboard.csv")
    challengers_cup.drop(['team_id'], axis=1, inplace=True)
    df2 = challengers_cup[challengers_cup["team_name"] == "SPVGG Dragons"]

    t20 = pd.read_csv("Data/T20/1563884_bowling_leaderboard.csv")
    t20.drop(['team_id'], axis=1, inplace=True)
    df3 = t20[t20["team_name"] == "SPVGG Dragons"]

    the_hundred = pd.read_csv("Data/T20/1563884_bowling_leaderboard.csv")
    the_hundred.drop(['team_id'], axis=1, inplace=True)
    df4 = the_hundred[the_hundred["team_name"] == "SPVGG Dragons"]

    trebur_cup = pd.read_csv("Data/T20/1563884_bowling_leaderboard.csv")
    trebur_cup.drop(['team_id'], axis=1, inplace=True)
    df5 = trebur_cup[trebur_cup["team_name"] == "SPVGG Dragons"]

    liga = pd.read_csv("Data/Liga/bowling_liga.csv")
    df6 = liga[liga["team_name"] == "SPVGG Dragons"]

    rs_cup = pd.read_csv("Data/RS_Cup/bowling_rs_cup.csv")
    df7 = rs_cup[rs_cup["team_name"] == "SPVGG Dragons"]

    # Merge
    result = merge_bowling_stats(df1, df2, df3, df4, df5, df6, df7)

    # Save
    #result.to_csv("final_bowling_data.csv", index=False, encoding="utf-8")
    print(result.to_string())
