import pandas as pd
import logging

logging.basicConfig(
    filename="log.txt",
    encoding="utf-8",
    filemode="w",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.INFO
)

logging.info("Reading data.")
df=pd.read_csv('data_student_21147.csv')
origin_df_len=len(df)

logging.info("Deleting rows with more than half values missing.")
threshold = len(df.columns) / 2
df = df.dropna(thresh=threshold)

rows_deleted=origin_df_len-len(df)

logging.info("Filling Wiek and Średnie Zarobki columns with mean.")
wiek_filled=df['Wiek'].isna().sum()
mean_age = df['Wiek'].mean()
df['Wiek'] = df['Wiek'].fillna(mean_age)

zarobki_filled=df['Średnie Zarobki'].isna().sum()
mean_earnings = df['Średnie Zarobki'].mean()
df['Średnie Zarobki'] = df['Średnie Zarobki'].fillna(mean_age)

logging.info("Finding mean for travel duration.")
df_time=df   #df_time is df without missing time periods
df_time['Czas Początkowy Podróży'] = pd.to_datetime(df_time['Czas Początkowy Podróży'], format='%H:%M', errors='coerce')
df_time['Czas Końcowy Podróży'] = pd.to_datetime(df_time['Czas Końcowy Podróży'], format='%H:%M', errors='coerce')
df_time=df_time.dropna(subset=['Czas Początkowy Podróży'])
df_time=df_time.dropna(subset=['Czas Końcowy Podróży'])
df_time.loc[df_time['Czas Końcowy Podróży'] < df_time['Czas Początkowy Podróży'], 'Czas Końcowy Podróży'] += pd.Timedelta(days=1)
df_time['Czas Podróży'] = df_time['Czas Końcowy Podróży'] - df_time['Czas Początkowy Podróży']
mean_duration = df_time['Czas Podróży'].mean()
mean_duration=mean_duration.round('min')

logging.info("Dropping rows with both times missing.")
temp_df_len=len(df)
df = df.dropna(subset=['Czas Początkowy Podróży', 'Czas Końcowy Podróży'], how='all')
times_missing_len=temp_df_len-len(df)

logging.info("Filling times based on mean travel duration.")
df.loc[df['Czas Końcowy Podróży'] < df['Czas Początkowy Podróży'], 'Czas Końcowy Podróży'] += pd.Timedelta(days=1)
poczatek_filled=df['Czas Początkowy Podróży'].isna().sum()
koncowy_filled=df['Czas Końcowy Podróży'].isna().sum()
df['Czas Początkowy Podróży'] = df['Czas Początkowy Podróży'].fillna(df['Czas Końcowy Podróży'] - mean_duration)
df['Czas Końcowy Podróży'] = df['Czas Końcowy Podróży'].fillna(mean_duration + df['Czas Początkowy Podróży'])

logging.info("Filling Płeć and Wykształcenie with 'Brak' and Cel Podróży with 'Inne'.")
plec_filled=df['Płeć'].isna().sum()
df['Płeć'] = df['Płeć'].fillna("Brak")

wyksztalcenie_filled=df['Wykształcenie'].isna().sum()
df['Wykształcenie'] = df['Wykształcenie'].fillna("Brak")

cel_filled=df['Cel Podróży'].isna().sum()
df['Cel Podróży'] = df['Cel Podróży'].fillna("Inne")

logging.info("Data standardisation.")
df['Płeć'] = df['Płeć'].astype(str)
df['Wiek'] = df['Wiek'].astype(int)
df['Wykształcenie'] = df['Wykształcenie'].astype(str)
df['Średnie Zarobki'] = df['Średnie Zarobki'].astype(float)
df['Czas Początkowy Podróży'] = pd.to_datetime(df['Czas Początkowy Podróży'], format='%H:%M')
df['Czas Końcowy Podróży'] = pd.to_datetime(df['Czas Końcowy Podróży'], format='%H:%M')
df['Cel Podróży'] = df['Cel Podróży'].astype(str)

logging.info("Data processing ended.")


