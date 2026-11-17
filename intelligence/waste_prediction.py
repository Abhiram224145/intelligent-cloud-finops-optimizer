import pandas as pd
from sklearn.linear_model import LinearRegression


def predict_resource_waste(
    csv_path="intelligence/resource_history.csv",
    forecast_days=7
):
    try:
        df = pd.read_csv(csv_path)

        required = [
            "timestamp",
            "resource_id",
            "cpu_usage",
            "memory_usage",
            "monthly_cost"
        ]

        if not all(col in df.columns for col in required):
            return None, "Required columns are missing."

        df["timestamp"] = pd.to_datetime(
            df["timestamp"], errors="coerce"
        )

        for col in ["cpu_usage", "memory_usage", "monthly_cost"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna(subset=required)

        predictions = []

        for resource_id, group in df.groupby("resource_id"):

            group = group.sort_values("timestamp").copy()

            if len(group) < 3:
                continue

            group["day_number"] = (
                group["timestamp"] - group["timestamp"].min()
            ).dt.total_seconds() / 86400

            X = group[["day_number"]]

            for metric in ["cpu_usage", "memory_usage"]:

                model = LinearRegression()
                model.fit(X, group[metric])

                future_day = group["day_number"].max() + forecast_days

                predicted_value = model.predict(
                    pd.DataFrame({
                        "day_number": [future_day]
                    })
                )[0]

                predictions.append({
                    "resource_id": resource_id,
                    "metric": metric,
                    "current_value": round(
                        group[metric].iloc[-1], 2
                    ),
                    "predicted_value": round(
                        max(0, min(100, predicted_value)), 2
                    ),
                    "forecast_days": forecast_days
                })

        if not predictions:
            return None, "Insufficient historical data."

        result = pd.DataFrame(predictions)

        return result, None

    except FileNotFoundError:
        return None, "Historical CSV file not found."

    except Exception as error:
        return None, str(error)


if __name__ == "__main__":

    result, error = predict_resource_waste()

    if error:
        print("ERROR:", error)

    else:
        print("\n7-DAY RESOURCE UTILIZATION FORECAST")
        print("=" * 55)
        print(result.to_string(index=False))