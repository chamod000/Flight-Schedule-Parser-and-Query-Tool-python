"""
CSV and JSON parsing modules
Handles reading and parsing of flight data files
"""

import csv
import json
from pathlib import Path


class CSVParser:
    """Parse CSV flight data files"""
    
    def __init__(self, validator):
        """
        Initialize CSV parser with a validator
        
        Args:
            validator (FlightValidator): Validator instance for flight data
        """
        self.validator = validator
    
    def parse_file(self, filepath):
        """
        Parse a single CSV file
        
        Args:
            filepath (str): Path to the CSV file
            
        Returns:
            tuple: (valid_flights, errors)
                - valid_flights (list): List of valid flight dictionaries
                - errors (list): List of error dictionaries
        """
        valid_flights = []
        errors = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                # Read all lines to track line numbers
                lines = f.readlines()
            
            # Use csv.DictReader for parsing
            reader = csv.DictReader(lines, skipinitialspace=True)
            
            # Track line number (accounting for header)
            line_num = 1  # Header is line 1
            
            for raw_line, row in zip(lines[1:], reader):  # Skip header in lines
                line_num += 1
                
                # Skip empty lines
                if not raw_line.strip():
                    continue
                
                # Skip comment lines (starting with #)
                if raw_line.strip().startswith('#'):
                    errors.append({
                        'line_number': line_num,
                        'content': raw_line.strip(),
                        'reason': 'comment line, ignored for data parsing'
                    })
                    continue
                
                # Clean the row data (strip whitespace from keys and values)
                flight_data = {k.strip(): v.strip() if v else '' 
                              for k, v in row.items() if k}
                
                # Validate the flight data
                is_valid, error_messages = self.validator.validate_flight(flight_data)
                
                if is_valid:
                    # Convert to proper types and add to valid flights
                    typed_flight = self.validator.convert_to_typed_flight(flight_data)
                    valid_flights.append(typed_flight)
                else:
                    # Record error with line number and reason
                    errors.append({
                        'line_number': line_num,
                        'content': raw_line.strip(),
                        'reason': ', '.join(error_messages)
                    })
        
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {filepath}")
        except Exception as e:
            raise Exception(f"Error parsing CSV: {e}")
        
        return valid_flights, errors
    
    def parse_directory(self, directory):
        """
        Parse all CSV files in a directory
        
        Args:
            directory (str): Path to directory containing CSV files
            
        Returns:
            tuple: (combined_valid_flights, combined_errors)
                - combined_valid_flights (list): All valid flights from all files
                - combined_errors (list): All errors from all files
        """
        dir_path = Path(directory)
        
        if not dir_path.exists() or not dir_path.is_dir():
            raise ValueError(f"Invalid directory: {directory}")
        
        all_valid_flights = []
        all_errors = []
        
        # Find all CSV files in the directory
        csv_files = sorted(dir_path.glob('*.csv'))
        
        if not csv_files:
            print(f"Warning: No CSV files found in {directory}")
            return all_valid_flights, all_errors
        
        # Parse each file
        for csv_file in csv_files:
            print(f"  Processing: {csv_file.name}")
            valid_flights, errors = self.parse_file(str(csv_file))
            
            # Add filename context to errors for better tracking
            for error in errors:
                error['filename'] = csv_file.name
            
            all_valid_flights.extend(valid_flights)
            all_errors.extend(errors)
        
        return all_valid_flights, all_errors


class JSONParser:
    """Parse and load JSON flight databases"""
    
    def load(self, filepath):
        """
        Load flights from JSON file
        
        Args:
            filepath (str): Path to JSON file
            
        Returns:
            list: List of flight dictionaries
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If JSON is invalid or not an array
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate that it's a list
            if not isinstance(data, list):
                raise ValueError("JSON file must contain an array of flight objects")
            
            return data
        
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON file not found: {filepath}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")