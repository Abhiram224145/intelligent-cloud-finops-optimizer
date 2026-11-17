import pandas as pd


def simulate_optimization(
    resource_id,
    action,
    csv_path="cloud_resources.csv"
):
    df = pd.read_csv(csv_path)

    resource = df[
        df["resource_id"].astype(str) == str(resource_id)
    ]

    if resource.empty:
        return None

    row = resource.iloc[0]

    cpu = float(row["cpu_usage"])
    memory = float(row["memory_usage"])
    cost = float(row["monthly_cost"])

    if action == "Stop resource":
        if cpu >= 10 or memory >= 15:
            print("Stopping not recommended: utilization is too high.")
            return None
        saving_rate = 0.70
        risk = "High"

    elif action == "Right-size resource":
        if cpu >= 70 or memory >= 70:
            print("Right-sizing not recommended.")
            return None
        saving_rate = 0.20
        risk = "Medium"

    elif action == "Storage optimization":
        saving_rate = 0.15
        risk = "Low to Medium"

    else:
        print("Invalid action.")
        return None

    savings = cost * saving_rate

    return {
        "Resource": resource_id,
        "Action": action,
        "Current Monthly Cost": cost,
        "Estimated Monthly Savings": savings,
        "Projected Monthly Cost": cost - savings,
        "Estimated Annual Savings": savings * 12,
        "Risk": risk
    }


if __name__ == "__main__":

    result = simulate_optimization(
        "VM-05",
        "Stop resource"
    )

    if result:
        print("\nWHAT-IF CLOUD COST SIMULATOR")
        print("=" * 40)

        for key, value in result.items():
            print(f"{key}: {value}")