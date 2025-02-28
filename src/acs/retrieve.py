import requests
import pandas as pd
from typing import List, Dict


state_fips = {
            'ALABAMA': '01',
            'ALASKA': '02',
            'ARIZONA': '04',
            'ARKANSAS': '05',
            'CALIFORNIA': '06',
            'COLORADO': '08',
            'CONNECTICUT': '09',
            'DELAWARE': '10',
            'DISTRICT OF COLUMBIA': '11',
            'FLORIDA': '12',
            'GEORGIA': '13',
            'HAWAII': '15',
            'IDAHO': '16',
            'ILLINOIS': '17',
            'INDIANA': '18',
            'IOWA': '19',
            'KANSAS': '20',
            'KENTUCKY': '21',
            'LOUISIANA': '22',
            'MAINE': '23',
            'MARYLAND': '24',
            'MASSACHUSETTS': '25',
            'MICHIGAN': '26',
            'MINNESOTA': '27',
            'MISSISSIPPI': '28',
            'MISSOURI': '29',
            'MONTANA': '30',
            'NEBRASKA': '31',
            'NEVADA': '32',
            'NEW HAMPSHIRE': '33',
            'NEW JERSEY': '34',
            'NEW MEXICO': '35',
            'NEW YORK': '36',
            'NORTH CAROLINA': '37',
            'NORTH DAKOTA': '38',
            'OHIO': '39',
            'OKLAHOMA': '40',
            'OREGON': '41',
            'PENNSYLVANIA': '42',
            'RHODE ISLAND': '44',
            'SOUTH CAROLINA': '45',
            'SOUTH DAKOTA': '46',
            'TENNESSEE': '47',
            'TEXAS': '48',
            'UTAH': '49',
            'VERMONT': '50',
            'VIRGINIA': '51',
            'WASHINGTON': '53',
            'WEST VIRGINIA': '54',
            'WISCONSIN': '55',
            'WYOMING': '56',
            'PUERTO RICO': '72'
        }

class CensusDataRetriever:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.census.gov/data"
        self.year = "2022"  # Most recent ACS 5-year estimates
        self.dataset = "acs/acs5"
        
    def get_variable_groups(self) -> Dict:
        """Retrieve available variable groups for reference"""
        url = f"{self.base_url}/{self.year}/{self.dataset}/groups.json"
        response = requests.get(url)
        return response.json()
    
    def get_place_data(self, state_fips: str, variables: List[str]) -> pd.DataFrame:
        """
        Retrieve data for all places (cities) in a state
        
        Parameters:
        state_fips: Two-digit state FIPS code
        variables: List of Census variable codes
        """
        # Construct variable string
        var_str = ",".join(variables)
        
        # Build API URL
        url = f"{self.base_url}/{self.year}/{self.dataset}"
        
        # Parameters for the request
        params = {
            "get": f"NAME,{var_str}",
            "for": "place:*",
            "in": f"state:{state_fips}",
            "key": self.api_key
        }
        
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"API request failed: {response.text}")
            
        # Convert response to DataFrame
        data = response.json()
        df = pd.DataFrame(data[1:], columns=data[0])
        return df

def main():
    # Replace with your Census API key
    API_KEY = "185f22854b5fff8e12d4d135d81adabd7ede4310"
    
    # Initialize retriever
    retriever = CensusDataRetriever(API_KEY)
    
    # Example variables for different demographics
    # You can find more variables at: https://api.census.gov/data/2022/acs/acs5/variables.html
    variables = [
        # Total population
        
        # Age and Sex (examples)

        'B01001_001E', 
        'B01001H_025E', 
        'B01001D_025E',
        'B01001D_010E',
        'B01001H_010E',
        'B01001H_011E',
        'B01001D_011E',
    ]
    
    # Example: Get data for California (FIPS: 06)
    ca_data = retriever.get_place_data("06", variables)
    
    # Clean and process the data
    # ca_data = ca_data.apply()
    
    # Add descriptive column names
    column_map = {
        'B01001_001E': 'total_population',
        'B01001H_025E': 'female_white_alone_30_34',
        'B01001D_025E': 'female_asian_alone_30_34',
        'B01001D_010E': 'male_asian_alone_30_34',
        'B01001H_010E': 'male_white_alone_30_34',
        'B01001H_011E': 'male_white_alone_35_39',
        'B01001D_011E': 'male_asian_alone_35_39',
    }
    ca_data = ca_data.rename(columns=column_map)
    
    # Save to CSV
    ca_data.to_csv('california_demographics.csv', index=False)
    print("Data successfully retrieved and saved to california_demographics.csv")

if __name__ == "__main__":
    main()