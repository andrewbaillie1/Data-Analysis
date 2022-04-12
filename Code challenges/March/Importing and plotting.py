import pandas as pd
from IPython.display import display
from pathlib import Path
from scipy import signal
import plotly.express as px
input_folder = Path(r'C:\Projects\DSP Committee\Drop in challenges\9 March')
all_top_ten_peaks = []
all_peaks = []
for csv in input_folder.glob('*.csv'):
    df = pd.read_csv(csv)
    time_series = df.set_index('Time (s)')
    time_series = time_series['Reading']
    peak_indexes = signal.argrelmax(time_series.to_numpy(), order=15)[0]
    peaks = time_series.iloc[peak_indexes]
    print(f'95% quantile for {csv.name} = {peaks.quantile(0.95)}')
    for idx, peak in peaks.iteritems():
        all_peaks.append([idx, peak, csv.name])
    top_ten_peaks = peaks.sort_values(ascending=False).iloc[:10]
    for idx, peak in top_ten_peaks.iteritems():
        all_top_ten_peaks.append([idx, peak, csv.name])
all_top_ten_peaks_df = pd.DataFrame(
    all_top_ten_peaks, columns=['time', 'peak', 'source'])
all_peaks_df = pd.DataFrame(all_peaks, columns=['time', 'peak', 'source'])
overall_top_ten_peaks = all_peaks_df.sort_values(
    by='peak', ascending=False)[:10]
print('Overall top 10 peaks: ')
display(overall_top_ten_peaks)
fig = px.scatter(all_top_ten_peaks_df, x='time', y='peak', color='source')
fig.add_scatter(x=overall_top_ten_peaks['time'], y=overall_top_ten_peaks['peak'], mode='markers', marker=dict(
    symbol='circle-open',
    size=20,
    line=dict(
        color='red',
        width=2
    )))
display(fig)
print(
    f'95% quantile across ALL gauges = {all_peaks_df["peak"].quantile(0.95)}')
