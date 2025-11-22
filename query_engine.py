"""
Query engine for filtering flight data
Handles query execution and filtering logic
"""

import json
from datetime import datetime


class QueryEngine:
    """Execute queries on flight database"""
    
    def __init__(self, flights):
        """
        Initialize query engine with flight data
        
        Args:
            flights (list): List of flight dictionaries to query
        """
        self.flights = flights
        self.datetime_format = '%Y-%m-%d %H:%M'
    
    def execute_query(self, query):
        """
        Execute a single query and return matching flights
        
        Query filtering rules:
        - flight_id, origin, destination: exact match
        - departure_datetime: flights departing >= this value
        - arrival_datetime: flights arriving <= this value
        - price: flights with price <= this value
        
        Args:
            query (dict): Dictionary containing query criteria
            
        Returns:
            list: List of flights matching all query criteria
        """
        matches = []
        
        for flight in self.flights:
            if self._flight_matches_query(flight, query):
                matches.append(flight)
        
        return matches
    
    def _flight_matches_query(self, flight, query):
        """
        Check if a flight matches all query criteria
        
        Args:
            flight (dict): Flight data to check
            query (dict): Query criteria to match against
            
        Returns:
            bool: True if flight matches all criteria, False otherwise
        """
        
        # Exact match fields: flight_id, origin, destination
        exact_match_fields = ['flight_id', 'origin', 'destination']
        for field in exact_match_fields:
            if field in query:
                if flight.get(field) != query[field]:
                    return False
        
        # departure_datetime: include flights departing >= query value
        if 'departure_datetime' in query:
            try:
                query_dt = datetime.strptime(query['departure_datetime'], 
                                            self.datetime_format)
                flight_dt = datetime.strptime(flight['departure_datetime'], 
                                             self.datetime_format)
                if flight_dt < query_dt:
                    return False
            except (ValueError, KeyError):
                return False
        
        # arrival_datetime: include flights arriving <= query value
        if 'arrival_datetime' in query:
            try:
                query_dt = datetime.strptime(query['arrival_datetime'], 
                                            self.datetime_format)
                flight_dt = datetime.strptime(flight['arrival_datetime'], 
                                             self.datetime_format)
                if flight_dt > query_dt:
                    return False
            except (ValueError, KeyError):
                return False
        
        # price: include flights with price <= query value
        if 'price' in query:
            try:
                query_price = float(query['price'])
                flight_price = float(flight['price'])
                if flight_price > query_price:
                    return False
            except (ValueError, KeyError):
                return False
        
        # If all criteria passed, flight matches
        return True
    
    def execute_queries_from_file(self, query_file):
        """
        Load queries from JSON file and execute them
        
        Args:
            query_file (str): Path to JSON file containing queries
            
        Returns:
            list: Array of query result objects, each containing:
                - query: The original query
                - matches: List of matching flights
                
        Raises:
            ValueError: If query file format is invalid
        """
        # Load query file
        with open(query_file, 'r', encoding='utf-8') as f:
            queries = json.load(f)
        
        # Handle single query object or array of queries
        if isinstance(queries, dict):
            queries = [queries]
        elif not isinstance(queries, list):
            raise ValueError("Query file must contain an object or array of query objects")
        
        # Execute each query and collect results
        results = []
        for query in queries:
            matches = self.execute_query(query)
            results.append({
                'query': query,
                'matches': matches
            })
        
        return results