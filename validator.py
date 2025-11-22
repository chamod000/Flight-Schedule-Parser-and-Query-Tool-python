"""
Flight data validation module
Handles all validation rules for flight records
"""

import re
from datetime import datetime


class FlightValidator:
    """Validates flight data according to specification"""
    
    # Valid airport codes (3-letter IATA codes)
    # You can expand this list with more airports
    VALID_AIRPORTS = {
        'LHR', 'JFK', 'FRA', 'RIX', 'OSL', 'HEL', 'ARN', 'CDG', 'DXB',
        'DOH', 'SYD', 'AMS', 'LAX', 'BRU', 'ORD', 'ATL', 'DFW', 'DEN',
        'SFO', 'SEA', 'MIA', 'MCO', 'LAS', 'PHX', 'IAH', 'EWR', 'IST',
        'CLT', 'MSP', 'DTW', 'PHL', 'LGA', 'BOS', 'SLC', 'BWI', 'TPA',
        'SAN', 'PDX', 'STL', 'HNL', 'SVO', 'LON'
    }
    
    def __init__(self):
        """Initialize validator with datetime format"""
        self.datetime_format = '%m/%d/%Y %H:%M'
    
    def validate_flight(self, flight_data):
        """
        Validate a flight record against all rules
        
        Args:
            flight_data (dict): Dictionary containing flight information
            
        Returns:
            tuple: (is_valid, error_messages)
                - is_valid (bool): True if all validations pass
                - error_messages (list): List of validation error messages
        """
        errors = []
        
        # Check for required fields
        required_fields = ['flight_id', 'origin', 'destination', 
                          'departure_datetime', 'arrival_datetime', 'price']
        
        for field in required_fields:
            if field not in flight_data or flight_data[field] == '':
                errors.append(f"missing {field} field")
        
        # If fields are missing, return early
        if errors:
            return False, errors
        
        # Validate flight_id (2-8 alphanumeric characters)
        if not self._validate_flight_id(flight_data['flight_id']):
            errors.append(f"invalid flight_id (must be 2-8 alphanumeric characters)")
        
        # Validate origin (3 uppercase letters, valid airport code)
        if not self._validate_airport_code(flight_data['origin']):
            errors.append(f"invalid origin code")
        
        # Validate destination (3 uppercase letters, valid airport code)
        if not self._validate_airport_code(flight_data['destination']):
            errors.append(f"invalid destination code")
        
        # Validate datetimes and compare them
        departure_dt = None
        arrival_dt = None
        
        try:
            departure_dt = datetime.strptime(flight_data['departure_datetime'], 
                                            self.datetime_format)
        except (ValueError, TypeError):
            errors.append("invalid departure datetime")
        
        try:
            arrival_dt = datetime.strptime(flight_data['arrival_datetime'], 
                                          self.datetime_format)
        except (ValueError, TypeError):
            errors.append("invalid arrival datetime")
        
        # Check that arrival is after departure
        if departure_dt and arrival_dt:
            if arrival_dt <= departure_dt:
                errors.append("arrival before departure")
        
        # Validate price (positive float)
        try:
            price = float(flight_data['price'])
            if price <= 0:
                errors.append("negative price value")
        except (ValueError, TypeError):
            errors.append("invalid price format")
        
        # Return validation result
        return len(errors) == 0, errors
    
    def _validate_flight_id(self, flight_id):
        """
        Validate flight ID: 2-8 alphanumeric characters
        
        Args:
            flight_id (str): Flight ID to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not flight_id:
            return False
        if len(flight_id) < 2 or len(flight_id) > 8:
            return False
        return flight_id.isalnum()
    
    def _validate_airport_code(self, code):
        """
        Validate airport code: 3 uppercase letters
        
        Args:
            code (str): Airport code to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not code:
            return False
        if len(code) != 3:
            return False
        if not code.isupper() or not code.isalpha():
            return False
        
        # Check against known airport codes
        # Comment out the next line if you want to accept any 3-letter code
        return code in self.VALID_AIRPORTS
    
    def convert_to_typed_flight(self, flight_data):
        """
        Convert validated flight data to proper types
        
        Args:
            flight_data (dict): Dictionary with string values
            
        Returns:
            dict: Dictionary with properly typed values
        """
        return {
            'flight_id': flight_data['flight_id'],
            'origin': flight_data['origin'],
            'destination': flight_data['destination'],
            'departure_datetime': flight_data['departure_datetime'],
            'arrival_datetime': flight_data['arrival_datetime'],
            'price': float(flight_data['price'])
        }