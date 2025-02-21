import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 日本語フォントを指定（Windows用）
plt.rcParams['font.family'] = 'MS Gothic'  # Windows標準のフォント

def summarize_trial_counts_with_ratio(trial_counts, bin_size, max_value):
    bins = np.arange(1, max_value + bin_size, bin_size)
    hist, bin_edges = np.histogram(trial_counts, bins=bins)

    df_summary = pd.DataFrame({
        "範囲": [f"{int(bin_edges[i])} - {int(bin_edges[i+1]-1)}" for i in range(len(bin_edges)-1)],
        "試行回数の頻度": hist,
    })
    return df_summary

# Streamlit UI
st.title("試行回数のシミュレーション")

# ユーザーがパラメータを設定
NUM_SIMULATIONS = st.number_input("シミュレーション回数", value=1000000, step=100000, format="%d")
X = st.number_input("必要な当選回数", value=5, step=1, format="%d")
P = st.number_input("1回の試行で当選する確率 (0.01 = 1/100)", value=0.01, step=0.001, format="%.3f")
BIN_SIZE = st.slider("ヒストグラムの区分サイズ", min_value=100, max_value=2000, value=500, step=100)
MAX_VALUE = st.slider("ヒストグラムの最大値", min_value=5000, max_value=50000, value=20000, step=5000)

# シミュレーションの実行
trial_counts = np.random.negative_binomial(X, P, NUM_SIMULATIONS) + X

# ヒストグラムの作成
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(trial_counts, bins=50, density=True, alpha=0.6, color='blue', edgecolor='black')
ax.set_xlabel('Trials')
ax.set_ylabel('Probability')
ax.set_title(f'Distribution of Trials Needed to Win {X} Times in a 1/{round(1/P, 1)} Lottery')
ax.set_xlim(X, np.percentile(trial_counts, 100))

st.pyplot(fig)

# 平均・中央値・標準偏差を表示
mean_trials = np.mean(trial_counts)
median_trials = np.median(trial_counts)
std_trials = np.std(trial_counts)

st.write(f"**平均試行回数:** {mean_trials:.2f}")
st.write(f"**中央値:** {median_trials:.2f}")
st.write(f"**標準偏差:** {std_trials:.2f}")

# ヒストグラム集計データを取得
df_summary = summarize_trial_counts_with_ratio(trial_counts, BIN_SIZE, MAX_VALUE)

# データフレームを表示
st.dataframe(df_summary)

# データのダウンロードリンクを作成
csv = df_summary.to_csv(index=False).encode("utf-8-sig")
st.download_button("CSVをダウンロード", data=csv, file_name="simulation_results.csv", mime="text/csv")
