
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math

# Quick plotting funcs
def _plot_box(df, column, figsize=(6,4)):
    plt.figure(figsize=figsize)
    sns.boxplot(x=df[column])
    plt.title(f'Box Plot of {column}')
    plt.xlabel(column)
    plt.show()

def _plot_scatter(df, x_column, y_column, z_column=None, figsize=(6, 4)):
    if z_column:
        plt.figure(figsize=figsize)
        sns.scatterplot(x=df[x_column], y=df[y_column], hue=df[z_column])
        plt.title(f'Scatter Plot of {x_column} vs. {y_column} colored by {z_column}')
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.legend(title=z_column)
        plt.show()
    else:
        plt.figure(figsize=figsize)
        sns.scatterplot(x=df[x_column], y=df[y_column])
        plt.title(f'Scatter Plot of {x_column} vs. {y_column}')
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.show()

def _plot_countbar(df, column, hue=None, stat="count", figsize=(6, 4)):
    plt.figure(figsize=figsize)
    plt.title(f'Bar Plot of {column}')
    plt.xlabel(column)
    if hue:
        sns.countplot(data=df, x=column, hue=hue, stat=stat)
        plt.legend(title=f'{hue}', loc='upper right')
        plt.show()
    else:
        sns.countplot(x=df[column], stat=stat)
        plt.show()

def _plot_hist(df, column, bins=10, use_kde=True, figsize=(6, 4)):
    plt.figure(figsize=figsize)
    col = df[column].dropna()
    sns.histplot(col, bins=bins, kde=use_kde)
    plt.xlabel(f'{column}')
    plt.title(f'Histogram of {column} w {bins} bins')
    plt.show()

# Multi plotting
def _plot_hist_subplot(ax, x, fieldname, bins=10, use_kde=True):
    sns.histplot(x, bins=bins, kde=use_kde, ax=ax)
    ax.set_xlabel(f'{fieldname} bins tickers')
    ax.set_ylabel(f'Count obs in {fieldname} each bin')
    ax.set_title(f'Histogram of {fieldname} w {bins} bins')

def _plot_barchart_subplot(ax, x, fieldname):
    df_summary = x.value_counts(dropna=False)
    y_values = df_summary.values
    x_index = df_summary.index
    sns.barplot(x=x_index, y=y_values, order=x_index, ax=ax)
    for label, p in zip(y_values, ax.patches):
        ax.annotate(label, (p.get_x() + p.get_width() / 4, p.get_height() + 0.15))
    ax.set_xlabel(f'Group of {fieldname}')
    ax.set_ylabel(f'Count obs in {fieldname}')
    ax.set_title(f'Barchart of {fieldname}')
    ax.tick_params(axis='x', rotation=45)

def _plot_auto_grid(df, columns=None, bins=10, use_kde=True):
    if columns is None:
        columns = df.columns.tolist()

    valid_columns = []
    plot_types = []

    for col in columns:
        series = df[col]
        dtype = series.dtype

        if pd.api.types.is_numeric_dtype(dtype):
            valid_columns.append(col)
            plot_types.append('hist')

        elif pd.api.types.is_object_dtype(dtype) or pd.api.types.is_categorical_dtype(dtype):
            n_unique = series.nunique(dropna=False)
            if n_unique <= 10:
                valid_columns.append(col)
                plot_types.append('bar')
            else:
                print(f"Skipping column '{col}': too many groups ({n_unique})")

        else:
            print(f"Skipping column '{col}': unsupported data type ({dtype})")

    n_plots = len(valid_columns)
    if n_plots == 0:
        print("No valid columns to plot.")
        return

    n_cols = 4
    n_rows = math.ceil(n_plots / n_cols)

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4 * n_rows))
    axes = axes.flatten()

    for idx, (col, ptype) in enumerate(zip(valid_columns, plot_types)):
        ax = axes[idx]
        series = df[col]

        if ptype == 'hist':
            _plot_hist_subplot(ax, series, col, bins=bins, use_kde=use_kde)
        elif ptype == 'bar':
            _plot_barchart_subplot(ax, series, col)

    # Xóa subplot thừa nếu có
    for j in range(idx + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()