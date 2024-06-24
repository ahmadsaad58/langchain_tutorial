from typing import List
import pandas as pd


def read_codes(file_path: str, drop_items: List[str]) -> pd.DataFrame:
	codes = pd.read_csv(file_path)
	return codes.drop(columns=drop_items)

def description_to_code(df: pd.DataFrame) -> pd.DataFrame:
	df['description_to_code'] = df['Description'] + ":" + df['Diagnosis Code']
	return df

def code_to_description(df: pd.DataFrame) -> pd.DataFrame:
	df['code_to_description'] = df['Diagnosis Code'] + ':' +  df['Description']
	return df

def main():
	# file to read
	HCC_CODES = 'data/HCC.csv'
	drop = ['2020 CMS-HCC Model Category (V24)', '2024 Proposed CMS-HCC Model Category (V24)', '2020 CMS-HCC Model Category (V24) for 2024 Payment Year', '2024 Proposed CMS-HCC Model Category (V24) for 2024 Payment Year']

	# read file and clean up
	codes = read_codes(HCC_CODES, drop_items=drop)

	# create mappings
	description_to_code(codes)
	code_to_description(codes)

	# print codes
	print(codes.head())


if __name__ == '__main__':
	main()

