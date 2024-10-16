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
logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_formatter = logging.Formatter('%(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

logging.info("Reading data.\n")
df=pd.read_csv('data_student_21147.csv')
origin_df_len=len(df)

logging.info("Deleting rows with more than half values missing.")
threshold = len(df.columns) / 2
df = df.dropna(thresh=threshold)

rows_deleted=origin_df_len-len(df)
logger.info(f"Deleted rows: {rows_deleted}\n")

logging.info("Filling Wiek and Średnie Zarobki columns with mean.")
wiek_filled=df['Wiek'].isna().sum()
mean_age = df['Wiek'].mean()
df['Wiek'] = df['Wiek'].fillna(mean_age)
logger.info(f"Number of filled 'Wiek' values: {wiek_filled}")

zarobki_filled=df['Średnie Zarobki'].isna().sum()
mean_earnings = df['Średnie Zarobki'].mean()
df['Średnie Zarobki'] = df['Średnie Zarobki'].fillna(mean_age)
logger.info(f"Number of filled 'Średnie Zarobki' values: {zarobki_filled}\n")


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
logger.info(f"Mean of travel duration : {mean_duration}")

logging.info("Dropping rows with both times missing.")
temp_df_len=len(df)
df = df.dropna(subset=['Czas Początkowy Podróży', 'Czas Końcowy Podróży'], how='all')
times_missing_len=temp_df_len-len(df)
logger.info(f"Dropped rows with both missing times: {times_missing_len}\n")

logging.info("Filling times based on mean travel duration.")
df.loc[df['Czas Końcowy Podróży'] < df['Czas Początkowy Podróży'], 'Czas Końcowy Podróży'] += pd.Timedelta(days=1)
poczatek_filled=df['Czas Początkowy Podróży'].isna().sum()
koncowy_filled=df['Czas Końcowy Podróży'].isna().sum()
df['Czas Początkowy Podróży'] = df['Czas Początkowy Podróży'].fillna(df['Czas Końcowy Podróży'] - mean_duration)
logger.info(f"Filled 'Czas Początkowy Podróży' values: {poczatek_filled}")
df['Czas Końcowy Podróży'] = df['Czas Końcowy Podróży'].fillna(mean_duration + df['Czas Początkowy Podróży'])
logger.info(f"Filled 'Czas Końcowy Podróży' values: {koncowy_filled}\n")


logging.info("Filling Płeć and Wykształcenie with 'Brak' and Cel Podróży with 'Inne'.")
plec_filled=df['Płeć'].isna().sum()
df['Płeć'] = df['Płeć'].fillna("Brak")
logger.info(f"Filled 'Płeć' values: {plec_filled}")

wyksztalcenie_filled=df['Wykształcenie'].isna().sum()
df['Wykształcenie'] = df['Wykształcenie'].fillna("Brak")
logger.info(f"Filled 'Wykształcenie' values: {wyksztalcenie_filled}")

cel_filled=df['Cel Podróży'].isna().sum()
df['Cel Podróży'] = df['Cel Podróży'].fillna("Inne")
logger.info(f"Filled 'Cel Podróży' values: {cel_filled}\n")

logging.info("Data standardisation.")
df['Płeć'] = df['Płeć'].astype(str)
df['Wiek'] = df['Wiek'].astype(int)
df['Wykształcenie'] = df['Wykształcenie'].astype(str)
df['Średnie Zarobki'] = df['Średnie Zarobki'].astype(float)
df['Czas Początkowy Podróży'] = pd.to_datetime(df['Czas Początkowy Podróży'], format='%H:%M')
df['Czas Końcowy Podróży'] = pd.to_datetime(df['Czas Końcowy Podróży'], format='%H:%M')
df['Cel Podróży'] = df['Cel Podróży'].astype(str)

logging.info("Data processing ended.")

with open('report.txt', 'w') as file:
    file.write(f"Deleted rows: {(rows_deleted+times_missing_len)/origin_df_len*100}%\nFilled values: {(wiek_filled+zarobki_filled+poczatek_filled+koncowy_filled+plec_filled+wyksztalcenie_filled+cel_filled)/origin_df_len*100}%")