import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats

COLUMNS = ['changedFiles','hours_spent', 'body', 'comments']

df = pd.read_csv('out/pullRequests.csv')
df_merged = df[df['state'] == 'MERGED']
df_closed = df[df['state'] == 'CLOSED']
reviews = df['reviews']
for col in COLUMNS:
    print('Working on:',  col)
    # A
    closed = df_closed[col].to_list()
    merged = df_merged[col].to_list()

    fig, ax = plt.subplots()
    data = [closed, merged]
    ax.boxplot(data, labels=['closed', 'merged'], showfliers=False, whis=1.5)
    ax.set_title(col)
    plt.savefig('out/A_' + col + '.png')
    plt.close()
    
    # B
    fig, ax = plt.subplots()
    x = df[col]
    y = reviews
    spearman = stats.spearmanr(x, y)
    title = 'Spearman: ' + str(round(spearman[0],2))
    ax.scatter(x, y, alpha=0.5)
    ax.set(
        xlabel=col,
        ylabel='reviews',
        title=title
    )
    plt.savefig('out/B_' + col + '.png')
    plt.close()


