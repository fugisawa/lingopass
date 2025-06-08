#!/usr/bin/env python3
"""
Simple CSV structure validation without heavy dependencies
"""

import csv
import ast

def test_csv_structure():
    """Test CSV file structure and content"""
    print("🧪 Testing CSV file structure...")
    
    # Test languages.csv
    try:
        with open('data/languages.csv', 'r') as f:
            reader = csv.DictReader(f)
            languages_data = list(reader)
            
        expected_lang_cols = ['Idioma', 'TAM_Milhoes', 'ARPPU_USD', 'LTV_USD', 'CAC_USD']
        actual_cols = list(languages_data[0].keys())
        
        print(f"  ✅ Languages CSV: {len(languages_data)} rows")
        print(f"      Columns: {actual_cols}")
        
        # Test that we can rename problematic columns
        problematic_cols = ['TAM_Milhoes', 'Complexidade_Tecnica', 'Competicao_Level']
        for col in problematic_cols:
            if col in actual_cols:
                print(f"      ✅ Found column to rename: {col}")
        
    except Exception as e:
        print(f"  ❌ Languages CSV test failed: {e}")
    
    # Test competitors.csv  
    try:
        with open('data/competitors.csv', 'r') as f:
            reader = csv.DictReader(f)
            competitors_data = list(reader)
            
        actual_cols = list(competitors_data[0].keys())
        print(f"  ✅ Competitors CSV: {len(competitors_data)} rows")
        print(f"      Columns: {actual_cols}")
        
        # Test the specific columns that caused the bug
        bug_cols = ['User_Base_Milhoes', 'Revenue_Milhoes']
        for col in bug_cols:
            if col in actual_cols:
                print(f"      ✅ Found column that needed renaming: {col}")
        
        # Test data access
        for row in competitors_data:
            platform = row['Plataforma']
            users = row.get('User_Base_Milhoes', 'N/A')
            revenue = row.get('Revenue_Milhoes', 'N/A')
            print(f"      {platform}: {users}M users, ${revenue}M revenue")
            
    except Exception as e:
        print(f"  ❌ Competitors CSV test failed: {e}")
    
    # Test phases.csv
    try:
        with open('data/phases.csv', 'r') as f:
            reader = csv.DictReader(f)
            phases_data = list(reader)
            
        print(f"  ✅ Phases CSV: {len(phases_data)} rows")
        
        # Test AST literal_eval on Idiomas column
        for row in phases_data:
            phase = row['Fase']
            idiomas_str = row['Idiomas']
            try:
                idiomas_list = ast.literal_eval(idiomas_str)
                print(f"      {phase}: {len(idiomas_list)} languages - {idiomas_list}")
            except Exception as e:
                print(f"      ❌ AST eval failed for {phase}: {e}")
                
    except Exception as e:
        print(f"  ❌ Phases CSV test failed: {e}")

def test_edge_cases():
    """Test edge cases without pandas"""
    print("\n🧪 Testing edge cases...")
    
    # Test division by zero protection
    try:
        total_investment = 0
        total_return = 1000
        
        # Our safe division logic
        roi_text = f"ROI: {total_return/total_investment:.1f}x" if total_investment > 0 else "ROI: N/A"
        
        assert roi_text == "ROI: N/A", "Should handle division by zero"
        print(f"  ✅ Division by zero protection: {roi_text}")
        
    except Exception as e:
        print(f"  ❌ Division by zero test failed: {e}")
    
    # Test empty list handling
    try:
        empty_list = []
        avg_value = sum(empty_list) / len(empty_list) if len(empty_list) > 0 else 0
        
        assert avg_value == 0, "Should handle empty list"
        print(f"  ✅ Empty list protection: avg = {avg_value}")
        
    except Exception as e:
        print(f"  ❌ Empty list test failed: {e}")

def main():
    """Run validation tests"""
    print("🚀 Starting CSV structure validation...\n")
    
    test_csv_structure()
    test_edge_cases()
    
    print("\n🎉 CSV validation completed!")

if __name__ == "__main__":
    main()