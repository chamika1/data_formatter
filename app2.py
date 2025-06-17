import re
import csv
import os
import google.generativeai as genai
from typing import List, Tuple, Optional

class DataPatternFormatter:
    def __init__(self, api_key: str):
        """Initialize with Gemini API key"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
    def read_file(self, file_path: str) -> List[str]:
        """Read data from txt or csv file"""
        data = []
        file_ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_ext == '.txt':
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = [line.strip() for line in file.readlines() if line.strip()]
            elif file_ext == '.csv':
                with open(file_path, 'r', encoding='utf-8') as file:
                    csv_reader = csv.reader(file)
                    data = [','.join(row) for row in csv_reader if any(row)]
            else:
                raise ValueError("Unsupported file format. Please use .txt or .csv files.")
                
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            raise Exception(f"Error reading file: {str(e)}")
            
        return data
    
    def get_regex_pattern_from_gemini(self, sample_data: List[str], expected_format: str) -> str:
        """Get regex pattern from Gemini API based on sample data and expected format"""
        
        # Show sample data to user for verification
        print(f"\nSample data (first 5 lines):")
        for i, line in enumerate(sample_data[:5]):
            print(f"{i+1}: {line}")
        
        # Improved dynamic prompt
        prompt = f"""
Analyze the following data pattern and create a precise regex pattern to extract the required fields.

SAMPLE DATA:
{chr(10).join(sample_data[:10])}

EXPECTED OUTPUT FORMAT: {expected_format}

INSTRUCTIONS:
1. Study the data structure carefully - identify separators, delimiters, and patterns
2. Count how many fields need to be extracted based on the expected format
3. Create a regex pattern with appropriate capture groups for each field
4. Consider different data types (numbers, text, special characters, etc.)
5. Handle edge cases like empty fields or varying lengths

REQUIREMENTS:
- Provide ONLY the regex pattern (no explanations, no code blocks)
- Use capture groups () for each field to extract
- Make sure the pattern matches the data structure shown
- Test mentally with the sample data provided

Regex Pattern:
        """
        
        try:
            print("Sending request to Gemini API...")
            
            # Configure generation settings for better reliability
            generation_config = {
                "temperature": 0.1,
                "max_output_tokens": 150,
            }
            
            response = self.model.generate_content(
                prompt, 
                generation_config=generation_config
            )
            
            print("Received response from API...")
            
            if not response or not response.text:
                raise Exception("Empty response from Gemini API")
            
            regex_pattern = response.text.strip()
            print(f"Raw API response: {regex_pattern}")
            
            # Clean up the response to get only the regex pattern
            if '```' in regex_pattern:
                lines = regex_pattern.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('```') and not line.startswith('#'):
                        regex_pattern = line
                        break
            
            # Remove common prefixes and labels
            prefixes_to_remove = [
                'regex:', 'pattern:', 'Regex:', 'Pattern:', 
                'Regex Pattern:', 'regex pattern:', 'Pattern:',
                'Answer:', 'answer:', 'Result:', 'result:'
            ]
            for prefix in prefixes_to_remove:
                if regex_pattern.startswith(prefix):
                    regex_pattern = regex_pattern[len(prefix):].strip()
            
            # Remove any trailing explanations
            if '\n' in regex_pattern:
                regex_pattern = regex_pattern.split('\n')[0].strip()
            
            print(f"Cleaned regex pattern: {regex_pattern}")
            return regex_pattern
            
        except Exception as e:
            print(f"Gemini API Error: {str(e)}")
            # Dynamic fallback pattern generation
            fallback_pattern = self.generate_fallback_pattern(sample_data, expected_format)
            print(f"Using fallback pattern: {fallback_pattern}")
            return fallback_pattern
    
    def generate_fallback_pattern(self, sample_data: List[str], expected_format: str) -> str:
        """Generate a fallback regex pattern based on basic analysis"""
        if not sample_data:
            return r'(.*)'
        
        first_line = sample_data[0]
        
        # Count expected fields from format
        field_count = expected_format.count('|') + 1 if '|' in expected_format else 1
        
        # Detect common separators
        if '|' in first_line:
            separator = '|'
        elif ',' in first_line:
            separator = ','
        elif '\t' in first_line:
            separator = '\t'
        elif ';' in first_line:
            separator = ';'
        else:
            # Default to whitespace
            separator = r'\s+'
        
        # Generate pattern
        if separator == '|':
            pattern = r'([^|]+)' + (r'\|([^|]+)' * (field_count - 1))
        elif separator == ',':
            pattern = r'([^,]+)' + (r',([^,]+)' * (field_count - 1))
        elif separator == '\t':
            pattern = r'([^\t]+)' + (r'\t([^\t]+)' * (field_count - 1))
        elif separator == ';':
            pattern = r'([^;]+)' + (r';([^;]+)' * (field_count - 1))
        else:
            pattern = r'(\S+)' + (r'\s+(\S+)' * (field_count - 1))
        
        return pattern
    
    def apply_regex_pattern(self, data: List[str], regex_pattern: str) -> List[str]:
        """Apply regex pattern to extract and format data"""
        formatted_data = []
        
        try:
            pattern = re.compile(regex_pattern)
            
            for line in data:
                match = pattern.search(line)
                if match:
                    # Join all captured groups with |
                    formatted_line = '|'.join(match.groups())
                    formatted_data.append(formatted_line)
                    
        except re.error as e:
            raise Exception(f"Invalid regex pattern: {str(e)}")
        except Exception as e:
            raise Exception(f"Error applying regex pattern: {str(e)}")
            
        return formatted_data
    
    def save_output(self, data: List[str], output_path: str):
        """Save formatted data to txt or csv file"""
        file_ext = os.path.splitext(output_path)[1].lower()
        
        try:
            if file_ext == '.txt':
                with open(output_path, 'w', encoding='utf-8') as file:
                    for line in data:
                        file.write(line + '\n')
            elif file_ext == '.csv':
                with open(output_path, 'w', newline='', encoding='utf-8') as file:
                    csv_writer = csv.writer(file)
                    for line in data:
                        csv_writer.writerow(line.split('|'))
            else:
                raise ValueError("Unsupported output format. Please use .txt or .csv extension.")
                
            print(f"Output saved successfully to: {output_path}")
            
        except Exception as e:
            raise Exception(f"Error saving output: {str(e)}")

def main():
    # Initialize with your Gemini API key
    API_KEY = "API_KEY-GEMINI"
    
    print("=== Universal Data Pattern Identifier and Formatter ===\n")
    print("Initializing Gemini API...")
    
    try:
        formatter = DataPatternFormatter(API_KEY)
        print("✓ Gemini API initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize Gemini API: {str(e)}")
        print("Option 1 (Pattern Recognition) will not work without API.")
        formatter = DataPatternFormatter(API_KEY)
    
    while True:
        print("\n" + "="*50)
        print("Select an option:")
        print("1. Get Regex Pattern (Analyze any data and identify pattern using Gemini AI)")
        print("2. Format Data (Apply your regex pattern to format entire file)")
        print("3. Exit")
        print("="*50)
        
        choice = input("\nEnter your choice (1/2/3): ").strip()
        
        if choice == '1':
            print("\n🔍 PATTERN RECOGNITION MODE")
            print("This will analyze your data and suggest a regex pattern using Gemini AI")
            try:
                # Get input file
                input_file = input("\nEnter the path to your input file (txt or csv): ").strip()
                if not os.path.exists(input_file):
                    print("❌ File not found. Please check the path.")
                    continue
                
                # Read data
                print("📖 Reading data...")
                data = formatter.read_file(input_file)
                print(f"✅ Read {len(data)} lines from file.")
                
                if not data:
                    print("❌ No data found in file.")
                    continue
                
                # Get expected output format - more flexible
                print("\n📝 Specify your desired output format:")
                print("Examples:")
                print("  - [field1]|[field2]|[field3]|[field4]    (for 4 fields)")
                print("  - [name]|[email]|[phone]                (for 3 fields)")
                print("  - [id]|[data]                           (for 2 fields)")
                print("  - [username]|[password]|[email]|[age]    (for 4 fields)")
                expected_format = input("Enter expected output format: ").strip()
                
                if not expected_format:
                    print("❌ No output format specified.")
                    continue
                
                # Get regex pattern from Gemini
                print("\n🤖 Analyzing data with Gemini AI...")
                regex_pattern = formatter.get_regex_pattern_from_gemini(data, expected_format)
                
                print(f"\n✅ SUGGESTED REGEX PATTERN:")
                print(f"📋 {regex_pattern}")
                print("\n📝 Copy this pattern to use in Option 2 for formatting your data!")
                
                # Optional: Test the pattern
                test_choice = input("\n🧪 Test this pattern with sample data? (y/n): ").strip().lower()
                if test_choice == 'y':
                    try:
                        test_results = formatter.apply_regex_pattern(data[:5], regex_pattern)
                        if test_results:
                            print("\n✅ Pattern test results:")
                            for i, result in enumerate(test_results[:3]):
                                print(f"   {i+1}: {result}")
                        else:
                            print("❌ Pattern didn't match sample data. May need adjustment.")
                    except Exception as e:
                        print(f"❌ Error testing pattern: {str(e)}")
                
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                
        elif choice == '2':
            print("\n⚙️ DATA FORMATTING MODE")
            print("This will format your entire file using your regex pattern")
            try:
                # Get input file
                input_file = input("\nEnter the path to your input file (txt or csv): ").strip()
                if not os.path.exists(input_file):
                    print("❌ File not found. Please check the path.")
                    continue
                
                # Read ALL data from file
                print("📖 Reading entire file...")
                data = formatter.read_file(input_file)
                print(f"✅ Read {len(data)} lines from file.")
                
                if not data:
                    print("❌ No data found in file.")
                    continue
                
                # Show sample data for verification
                print(f"\n📋 Sample data (first 5 lines):")
                for i, line in enumerate(data[:5]):
                    print(f"   {i+1}: {line}")
                
                # Get regex pattern
                print("\n🎯 Enter your regex pattern:")
                print("Examples:")
                print("  - ([^|]+)\\|([^|]+)\\|([^|]+)\\|([^|]+)  (4 pipe-separated fields)")
                print("  - ([^,]+),([^,]+),([^,]+)               (3 comma-separated fields)")
                print("  - (\\w+)\\s+(\\w+)\\s+(\\d+)              (word word number)")
                regex_pattern = input("Regex pattern: ").strip()
                
                if not regex_pattern:
                    print("❌ No pattern provided.")
                    continue
                
                # Apply pattern to ALL data
                print(f"\n⚙️ Processing all {len(data)} lines...")
                formatted_data = formatter.apply_regex_pattern(data, regex_pattern)
                
                if not formatted_data:
                    print("❌ No matches found with the provided pattern.")
                    print("💡 Check your regex pattern and try again.")
                    continue
                
                print(f"✅ Successfully formatted {len(formatted_data)} lines out of {len(data)} total lines.")
                
                # Show preview
                print(f"\n📋 Preview (showing first 10 of {len(formatted_data)} formatted lines):")
                for i, line in enumerate(formatted_data[:10]):
                    print(f"   {i+1}: {line}")
                
                if len(formatted_data) > 10:
                    print(f"   ... and {len(formatted_data) - 10} more lines")
                
                # Get output file path
                output_file = input(f"\n💾 Enter output file path to save all {len(formatted_data)} formatted lines: ").strip()
                
                if not output_file:
                    print("❌ No output file specified.")
                    continue
                
                # Add extension if not provided
                if not output_file.endswith(('.txt', '.csv')):
                    output_file += '.txt'
                    print(f"📝 Added .txt extension: {output_file}")
                
                # Save ALL formatted data
                formatter.save_output(formatted_data, output_file)
                print(f"✅ SUCCESS! All {len(formatted_data)} formatted lines saved to: {output_file}")
                
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                
        elif choice == '3':
            print("\n👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()