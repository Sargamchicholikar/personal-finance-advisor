"""Lightweight deep-learning-style forecasting using NumPy MLP."""

from typing import Any, Dict

import numpy as np
import pandas as pd


def _make_windows(series: np.ndarray, window: int) -> tuple[np.ndarray, np.ndarray]:
    x, y = [], []
    for i in range(window, len(series)):
        x.append(series[i - window : i])
        y.append(series[i])
    return np.array(x, dtype=float), np.array(y, dtype=float).reshape(-1, 1)


def run_deep_learning_forecast(monthly_trend_df: pd.DataFrame, window: int = 3) -> Dict[str, Any]:
    """
    Train a tiny MLP and forecast next value.
    This keeps the project lightweight while still demonstrating neural-network learning.
    """
    if monthly_trend_df is None or len(monthly_trend_df) < 8:
        return {"error": "Need at least 8 months of data for DL forecast."}

    values = monthly_trend_df["Amount"].astype(float).values
    x, y = _make_windows(values, window)
    if len(x) < 4:
        return {"error": "Not enough sequence windows for training."}

    # Normalize for stable training
    mean_x = x.mean()
    std_x = x.std() + 1e-8
    mean_y = y.mean()
    std_y = y.std() + 1e-8
    x_n = (x - mean_x) / std_x
    y_n = (y - mean_y) / std_y

    split = max(2, int(len(x_n) * 0.8))
    x_train, y_train = x_n[:split], y_n[:split]
    x_test, y_test = x_n[split:], y_n[split:]

    # Tiny MLP: window -> 8 hidden -> 1
    rng = np.random.default_rng(42)
    w1 = rng.normal(0, 0.2, size=(window, 8))
    b1 = np.zeros((1, 8))
    w2 = rng.normal(0, 0.2, size=(8, 1))
    b2 = np.zeros((1, 1))

    lr = 0.03
    epochs = 350
    losses = []

    for _ in range(epochs):
        z1 = x_train @ w1 + b1
        a1 = np.tanh(z1)
        y_hat = a1 @ w2 + b2

        err = y_hat - y_train
        loss = float(np.mean(err**2))
        losses.append(loss)

        # Backprop
        d_y = 2 * err / len(x_train)
        d_w2 = a1.T @ d_y
        d_b2 = np.sum(d_y, axis=0, keepdims=True)
        d_a1 = d_y @ w2.T
        d_z1 = d_a1 * (1 - np.tanh(z1) ** 2)
        d_w1 = x_train.T @ d_z1
        d_b1 = np.sum(d_z1, axis=0, keepdims=True)

        w2 -= lr * d_w2
        b2 -= lr * d_b2
        w1 -= lr * d_w1
        b1 -= lr * d_b1

    # Evaluate test
    if len(x_test) > 0:
        test_pred_n = np.tanh(x_test @ w1 + b1) @ w2 + b2
        test_pred = (test_pred_n * std_y) + mean_y
        test_actual = (y_test * std_y) + mean_y
        dl_mae = float(np.mean(np.abs(test_pred - test_actual)))
    else:
        test_pred = np.array([]).reshape(-1, 1)
        test_actual = np.array([]).reshape(-1, 1)
        dl_mae = 0.0

    # Baseline MAE: persistence (previous month = prediction)
    if len(x_test) > 0:
        baseline_pred = (x_test[:, -1].reshape(-1, 1) * std_x) + mean_x
        baseline_mae = float(np.mean(np.abs(baseline_pred - test_actual)))
    else:
        baseline_mae = 0.0

    # Next month forecast
    last_window = values[-window:]
    last_window_n = ((last_window - mean_x) / std_x).reshape(1, -1)
    next_pred_n = np.tanh(last_window_n @ w1 + b1) @ w2 + b2
    next_pred = float((next_pred_n[0, 0] * std_y) + mean_y)

    compare_df = pd.DataFrame()
    if len(x_test) > 0:
        compare_df = pd.DataFrame(
            {
                "Index": list(range(len(test_actual))),
                "Actual": test_actual.flatten(),
                "DL_Prediction": test_pred.flatten(),
            }
        )

    return {
        "predicted_next": max(0.0, next_pred),
        "dl_mae": dl_mae,
        "baseline_mae": baseline_mae,
        "loss_curve": losses,
        "comparison_df": compare_df,
        "window": window,
        "epochs": epochs,
    }

