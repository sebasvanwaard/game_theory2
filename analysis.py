import pandas as pd
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt


def corr_with_pvalues(df):
    cols = df.columns
    n = len(cols)
    
    corr_matrix = pd.DataFrame(np.zeros((n, n)), columns=cols, index=cols)
    pval_matrix = pd.DataFrame(np.zeros((n, n)), columns=cols, index=cols)
    
    for i in range(n):
        for j in range(n):
            if i == j:
                corr_matrix.iloc[i,j] = 1.0
                pval_matrix.iloc[i,j] = 0.0
            else:
                r, p = stats.pearsonr(df.iloc[:,i], df.iloc[:,j])
                corr_matrix.iloc[i,j] = r
                pval_matrix.iloc[i,j] = p
                
    return corr_matrix, pval_matrix

if __name__ == '__main__':
    # Read CSV, skip the first column (the list string)
    df = pd.read_csv("depth3n1000000.txt", header=None, usecols=[1,2], names = ["scores", "strat_sum"])
    df.head()

    corr, pvals = corr_with_pvalues(df)

    print("Correlation matrix:")
    print(corr)

    print("\nP-values:")
    print(pvals)

    grouped_df = df.groupby("strat_sum")["scores"].mean().reset_index()

    x = grouped_df["strat_sum"]
    y = grouped_df["scores"]

    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    line = slope * x + intercept

    plt.scatter(x, y, label="Mean scores")
    plt.plot(x, line, color="green", label=f"Fit line (r={r_value:.2f})")

    plt.xlabel("Strat sum")
    plt.ylabel("Mean score")
    plt.title("Mean score per strat_sum with trend line")
    plt.legend()
    plt.show()