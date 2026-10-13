
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


# =========================================================
# 1. CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="IPL Analytics & Winner Prediction",
    page_icon="🏏",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "ipl_winner_model.pkl"
MATCHES_PATH = BASE_DIR / "matches.csv"
BALL_PATH = BASE_DIR / "IPL_ball_by_ball_cleaned.csv"
HISTORY_PATH = BASE_DIR / "ipl_match_level.csv"


# =========================================================
# 2. LOAD DATA
# =========================================================

@st.cache_data
def load_matches(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()

    if "id" not in df.columns:
        raise ValueError("matches.csv mein 'id' column nahi mila.")

    if "season" not in df.columns:
        raise ValueError("matches.csv mein 'season' column nahi mila.")

    df["season"] = df["season"].astype(str).str.strip()

    return df


@st.cache_data
def load_balls(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()

    required = [
        "match_id",
        "runs_off_bat",
        "extras",
        "batting_team",
    ]

    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(
            f"Ball-by-ball CSV mein ye columns missing hain: {missing}"
        )

    df["match_id"] = pd.to_numeric(
        df["match_id"], errors="coerce"
    )

    df["runs_off_bat"] = pd.to_numeric(
        df["runs_off_bat"], errors="coerce"
    ).fillna(0)

    df["extras"] = pd.to_numeric(
        df["extras"], errors="coerce"
    ).fillna(0)

    return df


@st.cache_resource
def load_model(path):
    return joblib.load(path)


@st.cache_data
def load_history(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    return df


# Load files and display helpful errors if anything is missing.
try:
    matches = load_matches(MATCHES_PATH)
    balls = load_balls(BALL_PATH)

except Exception as e:
    st.error(f"Dataset load karne mein problem: {e}")
    st.info(
        "Check karo ki matches.csv aur "
        "IPL_ball_by_ball_cleaned.csv sahi folder mein hain."
    )
    st.stop()


# =========================================================
# 3. PREPARE MATCH DATA
# =========================================================

matches["id"] = pd.to_numeric(matches["id"], errors="coerce")

if "date" in matches.columns:
    matches["date"] = pd.to_datetime(
        matches["date"], errors="coerce"
    )

if "winner" in matches.columns:
    matches["winner"] = matches["winner"].fillna("Unknown").astype(str)

if "venue" not in matches.columns:
    matches["venue"] = "Unknown"

if "team1" not in matches.columns or "team2" not in matches.columns:
    st.error("matches.csv mein team1 ya team2 column missing hai.")
    st.stop()

matches["venue"] = matches["venue"].fillna("Unknown").astype(str)

# Exclude matches without a valid winner from winner statistics.
valid_matches = matches[
    matches["winner"].notna()
    & (matches["winner"].str.strip() != "")
    & (matches["winner"].str.lower() != "unknown")
    & (matches["winner"].str.lower() != "nan")
    & (matches["winner"].str.lower() != "no result")
].copy()


# =========================================================
# 4. SIDEBAR AND FILTERS
# =========================================================

st.sidebar.title("🏏 IPL Analytics")

page = st.sidebar.radio(
    "Choose a page",
    ["Analytics Dashboard", "Winner Prediction"],
)

st.sidebar.markdown("---")
st.sidebar.subheader("Historical IPL data analysis")

available_seasons = sorted(
    matches["season"].dropna().astype(str).unique(),
    reverse=True,
)

available_teams = sorted(
    set(matches["team1"].dropna().astype(str))
    | set(matches["team2"].dropna().astype(str))
)

available_venues = sorted(
    matches["venue"].dropna().astype(str).unique()
)

selected_seasons = st.sidebar.multiselect(
    "Filter by season",
    options=available_seasons,
    default=available_seasons,
)

selected_teams = st.sidebar.multiselect(
    "Filter by team",
    options=available_teams,
)

selected_venues = st.sidebar.multiselect(
    "Filter by venue",
    options=available_venues,
)


# Apply dashboard filters.
filtered = matches[
    matches["season"].astype(str).isin(selected_seasons)
].copy()

if selected_teams:
    filtered = filtered[
        filtered["team1"].isin(selected_teams)
        | filtered["team2"].isin(selected_teams)
    ]

if selected_venues:
    filtered = filtered[
        filtered["venue"].isin(selected_venues)
    ]


# =========================================================
# 5. ANALYTICS DASHBOARD
# =========================================================

if page == "Analytics Dashboard":

    st.title("🏏 IPL Analytics Dashboard")
    st.write(
        "Explore historical IPL matches, team performance, "
        "scoring patterns and venue statistics."
    )

    if filtered.empty:
        st.warning("Selected filters ke liye koi match nahi mila.")
        st.stop()

    # -----------------------------------------------------
    # KPI METRICS
    # -----------------------------------------------------

    total_matches = len(filtered)
    total_seasons = filtered["season"].nunique()

    total_teams = len(
        set(filtered["team1"].dropna().astype(str))
        | set(filtered["team2"].dropna().astype(str))
    )

    # Calculate runs for the selected matches.
    filtered_ids = set(
        filtered["id"].dropna().astype(int).tolist()
    )

    filtered_balls = balls[
        balls["match_id"].isin(filtered_ids)
    ].copy()

    filtered_balls["total_runs"] = (
        filtered_balls["runs_off_bat"]
        + filtered_balls["extras"]
    )

    total_runs = int(filtered_balls["total_runs"].sum())

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Matches", f"{total_matches:,}")
    col2.metric("Seasons", f"{total_seasons:,}")
    col3.metric("Teams", f"{total_teams:,}")
    col4.metric("Total Runs", f"{total_runs:,}")

    st.divider()

    # -----------------------------------------------------
    # MATCHES PLAYED BY SEASON
    # -----------------------------------------------------

    st.subheader("📈 Matches Played by Season")

    matches_by_season = (
        filtered.groupby("season")
        .size()
        .sort_index()
    )

    st.bar_chart(matches_by_season)

    # -----------------------------------------------------
    # TEAM WINS COMPARISON
    # -----------------------------------------------------

    st.subheader("🏆 Team Wins Comparison")

    filtered_winners = valid_matches[
        valid_matches["id"].isin(filtered["id"])
    ]

    if not filtered_winners.empty:
        team_wins = (
            filtered_winners["winner"]
            .value_counts()
            .rename_axis("Team")
            .to_frame("Wins")
        )

        st.bar_chart(team_wins)
    else:
        st.info("Selected filters ke liye winner data available nahi hai.")

    # -----------------------------------------------------
    # TOP VENUES
    # -----------------------------------------------------

    st.subheader("🏟️ Top Venues by Match Count")

    venue_counts = (
        filtered["venue"]
        .value_counts()
        .head(10)
        .sort_values()
    )

    st.bar_chart(venue_counts)

    # -----------------------------------------------------
    # TOTAL RUNS BY SEASON — FIXED
    # -----------------------------------------------------

    st.subheader("🏏 Total Runs by Season")

    # IMPORTANT:
    # The ball-by-ball file may already contain a season column.
    # Avoid merging another season column and creating season_x/season_y.

    if "season" in filtered_balls.columns:
        ball_season = filtered_balls.copy()

        ball_season["season"] = (
            ball_season["season"].astype(str).str.strip()
        )

    else:
        season_map = (
            matches[["id", "season"]]
            .dropna(subset=["id"])
            .drop_duplicates(subset=["id"])
            .rename(columns={"id": "match_id"})
        )

        # Remove duplicate season information if present.
        ball_season = filtered_balls.merge(
            season_map,
            on="match_id",
            how="left",
        )

    if not ball_season.empty and "season" in ball_season.columns:

        ball_season["total_runs"] = (
            pd.to_numeric(
                ball_season["runs_off_bat"], errors="coerce"
            ).fillna(0)
            +
            pd.to_numeric(
                ball_season["extras"], errors="coerce"
            ).fillna(0)
        )

        ball_season = ball_season[
            ball_season["season"].astype(str).isin(selected_seasons)
        ]

        # If a team filter is selected, show runs scored by
        # the selected batting team(s).
        if selected_teams:
            ball_season = ball_season[
                ball_season["batting_team"].isin(selected_teams)
            ]

        runs_by_season = (
            ball_season.dropna(subset=["season"])
            .groupby("season")["total_runs"]
            .sum()
            .sort_index()
        )

        if not runs_by_season.empty:
            st.line_chart(runs_by_season)
        else:
            st.info("Selected filters ke liye run data available nahi hai.")

    else:
        st.warning(
            "Season column match nahi hua. "
            "CSV files ke match_id aur season columns check karo."
        )

    # -----------------------------------------------------
    # TOSS DECISION ANALYSIS
    # -----------------------------------------------------

    st.subheader("🪙 Toss Decision Analysis")

    if "toss_decision" in filtered.columns:
        toss_counts = filtered["toss_decision"].fillna(
            "Unknown"
        ).value_counts()

        st.bar_chart(toss_counts)
    else:
        st.info("toss_decision column available nahi hai.")

    # -----------------------------------------------------
    # MATCH DATA TABLE
    # -----------------------------------------------------

    st.subheader("📋 Match Details")

    display_columns = [
        col for col in [
            "id",
            "season",
            "date",
            "team1",
            "team2",
            "venue",
            "toss_winner",
            "toss_decision",
            "winner",
            "result",
            "result_margin",
        ]
        if col in filtered.columns
    ]

    st.dataframe(
        filtered[display_columns].sort_values(
            by="season", ascending=False
        ),
        use_container_width=True,
        hide_index=True,
    )

    # Download filtered match data.
    csv_data = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Filtered Match Data",
        data=csv_data,
        file_name="ipl_filtered_matches.csv",
        mime="text/csv",
    )


# =========================================================
# 6. WINNER PREDICTION
# =========================================================

elif page == "Winner Prediction":

    st.title("🔮 IPL Winner Prediction")
    st.write(
        "Choose the two teams, venue and toss details "
        "to generate an experimental prediction."
    )

    try:
        if not MODEL_PATH.exists():
            st.error(f"Model file nahi mili: {MODEL_PATH}")
            st.stop()

        if not HISTORY_PATH.exists():
            st.error(f"History file nahi mili: {HISTORY_PATH}")
            st.stop()

        model = load_model(str(MODEL_PATH))
        history = load_history(str(HISTORY_PATH))

    except Exception as e:
        st.error(f"Model/history load karne mein problem: {e}")
        st.stop()

    required_features = [
        "team_1",
        "team_2",
        "venue",
        "toss_winner_is_team1",
        "toss_decision",
        "team1_h2h_rate",
        "team2_h2h_rate",
        "team1_recent_form",
        "team2_recent_form",
        "team1_venue_win_rate",
        "team2_venue_win_rate",
    ]

    missing_features = [
        col for col in required_features
        if col not in history.columns
    ]

    if missing_features:
        st.error(
            "History CSV mein required columns missing hain: "
            + ", ".join(missing_features)
        )
        st.stop()

    prediction_teams = sorted(
        set(history["team_1"].dropna().astype(str))
        | set(history["team_2"].dropna().astype(str))
    )

    prediction_venues = sorted(
        history["venue"].dropna().astype(str).unique()
    )

    col1, col2 = st.columns(2)

    with col1:
        team_1 = st.selectbox(
            "Select Team 1",
            prediction_teams,
            index=0,
        )

    with col2:
        team_2_options = [
            team for team in prediction_teams if team != team_1
        ]

        team_2 = st.selectbox(
            "Select Team 2",
            team_2_options,
        )

    venue = st.selectbox(
        "Select Venue",
        prediction_venues,
    )

    toss_winner = st.selectbox(
        "Toss Winner",
        [team_1, team_2],
    )

    toss_decision = st.radio(
        "Toss Decision",
        ["bat", "field"],
        horizontal=True,
    )

    if st.button("🚀 Predict Match Winner", type="primary"):

        # Use average historical feature values as a baseline.
        # These are not exact pre-match, team-specific calculations.
        numeric_features = [
            "team1_h2h_rate",
            "team2_h2h_rate",
            "team1_recent_form",
            "team2_recent_form",
            "team1_venue_win_rate",
            "team2_venue_win_rate",
        ]

        averages = history[numeric_features].apply(
            pd.to_numeric, errors="coerce"
        ).mean()

        toss_winner_is_team1 = int(toss_winner == team_1)

        input_data = pd.DataFrame([{
            "team_1": team_1,
            "team_2": team_2,
            "venue": venue,
            "toss_winner_is_team1": toss_winner_is_team1,
            "toss_decision": toss_decision,
            "team1_h2h_rate": averages["team1_h2h_rate"],
            "team2_h2h_rate": averages["team2_h2h_rate"],
            "team1_recent_form": averages["team1_recent_form"],
            "team2_recent_form": averages["team2_recent_form"],
            "team1_venue_win_rate": averages["team1_venue_win_rate"],
            "team2_venue_win_rate": averages["team2_venue_win_rate"],
        }], columns=required_features)

        try:
            prediction = model.predict(input_data)[0]

            st.divider()
            st.subheader("📊 Prediction Result")

            if int(prediction) == 1:
                st.success(f"Predicted Winner: {team_1}")
            else:
                st.success(f"Predicted Winner: {team_2}")

            if hasattr(model, "predict_proba"):
                probabilities = model.predict_proba(input_data)[0]

                st.caption(
                    "Experimental model probabilities — "
                    "not a guarantee of the actual result."
                )

                classes = list(model.classes_)

                prob_team_1 = (
                    float(probabilities[classes.index(1)]) * 100
                    if 1 in classes else 0.0
                )

                prob_team_2 = (
                    float(probabilities[classes.index(0)]) * 100
                    if 0 in classes else 0.0
                )

                pcol1, pcol2 = st.columns(2)

                pcol1.metric(
                    f"{team_1} Win Probability",
                    f"{prob_team_1:.1f}%",
                )

                pcol2.metric(
                    f"{team_2} Win Probability",
                    f"{prob_team_2:.1f}%",
                )

                st.caption(
                    "Historical feature values use dataset averages. "
                    "This is a prototype, not a reliable betting forecast."
                )

        except Exception as e:
            st.error(f"Prediction generate nahi hui: {e}")