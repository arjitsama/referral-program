# Import libraries
import pandas as pd
import os

def profile_table(df, table_name):
    """Profile dataframe: null counts + distinct counts."""
    profile = pd.DataFrame({
        "column": df.columns,
        "null_count": df.isnull().sum().values,
        "distinct_count": [df[col].nunique() for col in df.columns]
    })
    profile.insert(0, "table", table_name)
    return profile


if __name__ == "__main__":
    # Paths
    data_path = "data"
    output_path = "output/final_report.csv"
    profiling_path = "profiling/profiling_report.csv"

    # Load Data
    user_referrals = pd.read_csv(os.path.join(data_path, "user_referrals.csv"))
    user_referral_logs = pd.read_csv(os.path.join(data_path, "user_referral_logs.csv"))
    user_logs = pd.read_csv(os.path.join(data_path, "user_logs.csv"))
    user_referral_statuses = pd.read_csv(os.path.join(data_path, "user_referral_statuses.csv"))
    referral_rewards = pd.read_csv(os.path.join(data_path, "referral_rewards.csv"))
    paid_transactions = pd.read_csv(os.path.join(data_path, "paid_transactions.csv"))
    lead_logs = pd.read_csv(os.path.join(data_path, "lead_log.csv"))

    # Data Profiling
    profiling_results = pd.concat([
        profile_table(user_referrals, "user_referrals"),
        profile_table(user_referral_logs, "user_referral_logs"),
        profile_table(user_logs, "user_logs"),
        profile_table(user_referral_statuses, "user_referral_statuses"),
        profile_table(referral_rewards, "referral_rewards"),
        profile_table(paid_transactions, "paid_transactions"),
        profile_table(lead_logs, "lead_logs"),
    ])
    os.makedirs("profiling", exist_ok=True)
    profiling_results.to_csv(profiling_path, index=False)

    # Data Cleaning
    user_logs["name"] = user_logs["name"].str.title()
    user_referrals = user_referrals.dropna(subset=["referral_id"])

    # Data Processing
    df = (
        user_referrals
        .merge(user_referral_logs, left_on="referral_id", right_on="user_referral_id", how="left")
        .merge(user_logs, left_on="referrer_id", right_on="user_id", how="left", suffixes=("", "_referrer"))
        .merge(user_referral_statuses, left_on="user_referral_status_id", right_on="id", how="left")
        .merge(referral_rewards, left_on="referral_reward_id", right_on="id", how="left", suffixes=("", "_reward"))
        .merge(paid_transactions, on="transaction_id", how="left")
        .merge(lead_logs, left_on="referee_id", right_on="lead_id", how="left", suffixes=("", "_lead"))
    )
    df["referral_source_category"] = df["referral_source"].map({
        "User Sign Up": "Online",
        "Draft Transaction": "Offline",
        "Lead": None
    })
    df.loc[df["referral_source"] == "Lead", "referral_source_category"] = df["source_category"]

    # Basic business logic implementation to detect fraud
    df["reward_value"] = pd.to_numeric(df["reward_value"], errors="coerce").fillna(0)

    conditions_valid = (
        (df["reward_value"] > 0) &
        (df["description"] == "Berhasil") &
        (df["transaction_status"].str.upper() == "PAID") &
        (df["transaction_type"].str.upper() == "NEW")
    )

    conditions_pending_failed = (
        df["description"].isin(["Menunggu", "Tidak Berhasil"]) &
        (df["reward_value"] == 0)
    )

    df["is_business_logic_valid"] = conditions_valid | conditions_pending_failed

    # Output
    report = df[[
        "referral_id", "referral_source", "referral_source_category", "referral_at",
        "referrer_id", "name", "phone_number", "transaction_id", "transaction_status",
        "transaction_type", "is_business_logic_valid"
    ]]

    os.makedirs("output", exist_ok=True)
    report.to_csv(output_path, index=False)

    print(f"Final report saved to {output_path}")
    print(f"Profiling report saved to {profiling_path}")
