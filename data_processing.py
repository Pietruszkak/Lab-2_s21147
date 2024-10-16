import pandas as pd


df=pd.read_csv('data_student_21147.csv')
origin_df_len=len(df)

threshold = len(df.columns) / 2
df = df.dropna(thresh=threshold)

rows_deleted=origin_df_len-len(df)

wiek_filled=df['Wiek'].isna().sum()
mean_age = df['Wiek'].mean()
df['Wiek'] = df['Wiek'].fillna(mean_age)

zarobki_filled=df['Średnie Zarobki'].isna().sum()
mean_earnings = df['Średnie Zarobki'].mean()
df['Średnie Zarobki'] = df['Średnie Zarobki'].fillna(mean_age)

df_time=df   #df_time is df without missing time periods
df_time['Czas Początkowy Podróży'] = pd.to_datetime(df_time['Czas Początkowy Podróży'], format='%H:%M', errors='coerce')
df_time['Czas Końcowy Podróży'] = pd.to_datetime(df_time['Czas Końcowy Podróży'], format='%H:%M', errors='coerce')
df_time=df_time.dropna(subset=['Czas Początkowy Podróży'])
df_time=df_time.dropna(subset=['Czas Końcowy Podróży'])
df_time.loc[df_time['Czas Końcowy Podróży'] < df_time['Czas Początkowy Podróży'], 'Czas Końcowy Podróży'] += pd.Timedelta(days=1)
df_time['Czas Podróży'] = df_time['Czas Końcowy Podróży'] - df_time['Czas Początkowy Podróży']
mean_duration = df_time['Czas Podróży'].mean()
mean_duration=mean_duration.round('min')

temp_df_len=len(df)
df = df.dropna(subset=['Czas Początkowy Podróży', 'Czas Końcowy Podróży'], how='all')
times_missing_len=temp_df_len-len(df)

df.loc[df['Czas Końcowy Podróży'] < df['Czas Początkowy Podróży'], 'Czas Końcowy Podróży'] += pd.Timedelta(days=1)
poczatek_filled=df['Czas Początkowy Podróży'].isna().sum()
koncowy_filled=df['Czas Końcowy Podróży'].isna().sum()
df['Czas Początkowy Podróży'] = df['Czas Początkowy Podróży'].fillna(df['Czas Końcowy Podróży'] - mean_duration)
df['Czas Końcowy Podróży'] = df['Czas Końcowy Podróży'].fillna(mean_duration + df['Czas Początkowy Podróży'])

plec_filled=df['Płeć'].isna().sum()
df['Płeć'] = df['Płeć'].fillna("Brak")

wyksztalcenie_filled=df['Wykształcenie'].isna().sum()
df['Wykształcenie'] = df['Wykształcenie'].fillna("Brak")

cel_filled=df['Cel Podróży'].isna().sum()
df['Cel Podróży'] = df['Cel Podróży'].fillna("Inne")

df['Płeć'] = df['Płeć'].astype(str)
df['Wiek'] = df['Wiek'].astype(int)
df['Wykształcenie'] = df['Wykształcenie'].astype(str)
df['Średnie Zarobki'] = df['Średnie Zarobki'].astype(float)
df['Czas Początkowy Podróży'] = pd.to_datetime(df['Czas Początkowy Podróży'], format='%H:%M')
df['Czas Końcowy Podróży'] = pd.to_datetime(df['Czas Końcowy Podróży'], format='%H:%M')
df['Cel Podróży'] = df['Cel Podróży'].astype(str)


