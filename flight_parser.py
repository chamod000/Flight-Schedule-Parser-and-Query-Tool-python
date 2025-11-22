#!/usr/bin/env python3
"""
Flight Schedule Parser and Query Tool
Main entry point for the application
Author: Kodithuwakku Arachchige Chamod Chirantha Dilshan
Student ID: 233AEB022
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
from validator import FlightValidator
from parser import CSVParser, JSONParser
from query_engine import QueryEngine
from utils import save_json, save_errors


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Flight Schedule Parser and Query Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python flight_parser.py -i data/db.csv
  python flight_parser.py -d data/flights/
  python flight_parser.py -j data/db.json -q data/query.json
        """
    )
    
    parser.add_argument('-i', '--input', 
                       help='Parse a single CSV file',
                       type=str)
    
    parser.add_argument('-d', '--directory',
                       help='Parse all CSV files in a folder',
                       type=str)
    
    parser.add_argument('-o', '--output',
                       help='Custom output path for valid flights JSON (default: db.json)',
                       type=str,
                       default='db.json')
    
    parser.add_argument('-j', '--json',
                       help='Load existing JSON database instead of parsing CSVs',
                       type=str)
    
    parser.add_argument('-q', '--query',
                       help='Execute queries defined in a JSON file',
                       type=str)
    
    return parser.parse_args()


def main():
    """Main program logic"""
    args = parse_arguments()
    
    # Initialize components
    validator = FlightValidator()
    valid_flights = []
    errors = []
    
    # Step 1: Load or parse data
    if args.json:
        # Load existing JSON database
        print(f"Loading existing database from: {args.json}")
        try:
            json_parser = JSONParser()
            valid_flights = json_parser.load(args.json)
            print(f"✓ Loaded {len(valid_flights)} flights from database")
        except Exception as e:
            print(f"✗ Error loading JSON: {e}")
            sys.exit(1)
    
    elif args.input:
        # Parse single CSV file
        print(f"Parsing CSV file: {args.input}")
        csv_parser = CSVParser(validator)
        valid_flights, errors = csv_parser.parse_file(args.input)
        print(f"✓ Parsed {len(valid_flights)} valid flights, {len(errors)} errors")
        
        # Save results
        save_json(valid_flights, args.output)
        if errors:
            save_errors(errors, 'errors.txt')
            print(f"✓ Errors saved to: errors.txt")
    
    elif args.directory:
        # Parse all CSV files in directory
        print(f"Parsing all CSV files in directory: {args.directory}")
        csv_parser = CSVParser(validator)
        valid_flights, errors = csv_parser.parse_directory(args.directory)
        print(f"✓ Parsed {len(valid_flights)} valid flights, {len(errors)} errors")
        
        # Save results
        save_json(valid_flights, args.output)
        if errors:
            save_errors(errors, 'errors.txt')
            print(f"✓ Errors saved to: errors.txt")
    
    else:
        print("Error: Must specify either -i, -d, or -j option")
        print("Use -h for help")
        sys.exit(1)
    
    # Step 2: Execute queries if requested
    if args.query:
        if not valid_flights:
            print("✗ No flights loaded to query")
            sys.exit(1)
        
        print(f"\nExecuting queries from: {args.query}")
        try:
            query_engine = QueryEngine(valid_flights)
            results = query_engine.execute_queries_from_file(args.query)
            
            # Generate response filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M')
            # IMPORTANT: Replace with your actual student information
            student_id = "studentid"
            name = "name"
            lastname = "lastname"
            response_file = f"response_{student_id}_{name}_{lastname}_{timestamp}.json"
            
            save_json(results, response_file)
            print(f"✓ Query results saved to: {response_file}")
            print(f"  Executed {len(results)} queries")
            for i, result in enumerate(results, 1):
                print(f"    Query {i}: {len(result['matches'])} matches")
        
        except Exception as e:
            print(f"✗ Error executing queries: {e}")
            sys.exit(1)
    
    print("\n✓ All operations completed successfully")


if __name__ == '__main__':
    main()