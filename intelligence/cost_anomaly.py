import pandas as pd


def detect_resource_waste(csv_path="cloud_resources.csv"):
    """
    Detect potentially underutilized cloud resources.
    Uses CPU and memory utilization together.
    """

    try:
        df = pd.read_csv(csv_path)

        required_columns = [
            "resource_id",
            "resource_type",
            "cpu_usage",
            "memory_usage",
            "monthly_cost"
        ]

        missing = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing:
            return None, f"Missing columns: {missing}"

        # Convert numeric columns safely
        for column in [
            "cpu_usage",
            "memory_usage",
            "monthly_cost"
        ]:
            df[column] = pd.to_numeric(
                df[column], errors="coerce"
            )

        df = df.dropna(subset=required_columns)

        # Calculate average utilization
        df["average_utilization"] = (
            df["cpu_usage"] + df["memory_usage"]
        ) / 2

        # Classify resource utilization
        def classify(row):

            if (
                row["cpu_usage"] < 10
                and row["memory_usage"] < 15
            ):
                return "High Waste Risk"

            elif (
                row["cpu_usage"] < 20
                and row["memory_usage"] < 25
            ):
                return "Potential Waste"

            return "Healthy"

        df["waste_status"] = df.apply(
            classify, axis=1
        )

        # Estimate potentially avoidable cost.
        # This is an investigation estimate, not verified savings.
        df["estimated_waste_cost"] = df.apply(
            lambda row: (
                row["monthly_cost"] * 0.5
                if row["waste_status"] == "High Waste Risk"
                else row["monthly_cost"] * 0.2
                if row["waste_status"] == "Potential Waste"
                else 0
            ),
            axis=1
        )

        return df, None

    except FileNotFoundError:
        return None, f"CSV file not found: {csv_path}"

    except Exception as error:
        return None, str(error)


if __name__ == "__main__":

    results, error = detect_resource_waste()

    if error:
        print("ERROR:", error)

    else:
        print("\nCLOUD RESOURCE WASTE ANALYSIS")
        print("=" * 45)

        print(
            results[
                [
                    "resource_id",
                    "cpu_usage",
                    "memory_usage",
                    "monthly_cost",
                    "waste_status",
                    "estimated_waste_cost"
                ]
            ].to_string(index=False)
        )

        print("\nAnalysis completed.")