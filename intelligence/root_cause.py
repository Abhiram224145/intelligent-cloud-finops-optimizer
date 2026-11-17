import pandas as pd


def analyze_root_causes(csv_path="cloud_resources.csv"):

    try:
        df = pd.read_csv(csv_path)

        required = [
            "resource_id",
            "resource_type",
            "cpu_usage",
            "memory_usage",
            "monthly_cost"
        ]

        if not all(col in df.columns for col in required):
            return None, "Required columns are missing."

        for col in ["cpu_usage", "memory_usage", "monthly_cost"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna(subset=required)

        results = []

        for _, row in df.iterrows():

            cpu = row["cpu_usage"]
            memory = row["memory_usage"]
            cost = row["monthly_cost"]

            if cpu < 10 and memory < 15:
                status = "High Waste Risk"
                cause = "Both CPU and memory utilization are very low."
                recommendation = (
                    "Investigate whether this resource can be resized "
                    "or safely stopped."
                )

            elif cpu < 20 and memory < 25:
                status = "Potential Waste"
                cause = "CPU and memory utilization are relatively low."
                recommendation = (
                    "Review historical usage and consider rightsizing."
                )

            else:
                status = "Healthy"
                cause = "No low-utilization warning from current thresholds."
                recommendation = (
                    "Continue monitoring resource utilization."
                )

            results.append({
                "Resource ID": row["resource_id"],
                "Resource Type": row["resource_type"],
                "CPU Usage": cpu,
                "Memory Usage": memory,
                "Monthly Cost": cost,
                "Status": status,
                "Root Cause": cause,
                "Recommendation": recommendation
            })

        return pd.DataFrame(results), None

    except FileNotFoundError:
        return None, "Cloud resource CSV file not found."

    except Exception as error:
        return None, str(error)


if __name__ == "__main__":

    results, error = analyze_root_causes()

    if error:
        print("ERROR:", error)

    else:
        print("\nAI ROOT CAUSE ANALYSIS")
        print("=" * 60)

        for _, row in results.iterrows():

            print(f"\nResource: {row['Resource ID']}")
            print(f"Status: {row['Status']}")
            print(f"Root Cause: {row['Root Cause']}")
            print(f"Recommendation: {row['Recommendation']}")
            print(f"Monthly Cost: {row['Monthly Cost']}")

        print("\nRoot cause analysis completed.")