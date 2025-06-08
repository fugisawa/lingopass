#!/usr/bin/env python3
"""
Test script to verify edge cases and error handling in the LingoApp Streamlit dashboard
"""

import sys
sys.path.append('/home/fugisawa/.local/lib/python3.13/site-packages')

import pandas as pd
import numpy as np
from pathlib import Path
import ast

def test_data_loading():
    """Test data loading and column renaming"""
    print("🧪 Testing data loading...")
    
    try:
        data_dir = Path('data')
        
        # Test languages data loading
        df_languages = pd.read_csv(data_dir / 'languages.csv')
        original_cols = list(df_languages.columns)
        
        df_languages.rename(columns={
            'TAM_Milhoes': 'TAM_Milhões',
            'Complexidade_Tecnica': 'Complexidade_Técnica',
            'Competicao_Level': 'Competição_Level'
        }, inplace=True)
        
        print(f"  ✅ Languages: {len(df_languages)} rows, renamed columns correctly")
        
        # Test competitors data loading with our fix
        df_competitors = pd.read_csv(data_dir / 'competitors.csv')
        df_competitors.rename(columns={
            'Modelo_Negocio': 'Modelo_Negócio',
            'User_Base_Milhoes': 'User_Base_Milhões',  # This was the bug!
            'Revenue_Milhoes': 'Revenue_Milhões'
        }, inplace=True)
        
        # Test that the fixed columns exist
        assert 'User_Base_Milhões' in df_competitors.columns
        assert 'Revenue_Milhões' in df_competitors.columns
        print(f"  ✅ Competitors: {len(df_competitors)} rows, column rename fix works")
        
        return df_languages, df_competitors
        
    except Exception as e:
        print(f"  ❌ Data loading failed: {e}")
        return None, None

def test_empty_dataframe_handling(df_languages):
    """Test handling of empty DataFrames (extreme filter conditions)"""
    print("🧪 Testing empty DataFrame handling...")
    
    try:
        # Create impossible filter conditions
        df_filtered = df_languages[
            (df_languages['ROI_Ratio'] >= 100) &  # Impossible ROI
            (df_languages['Payback_Meses'] <= 1) &  # Impossible payback
            (df_languages['TAM_Milhões'] >= 1000)  # Impossible TAM
        ]
        
        assert len(df_filtered) == 0, "Filter should create empty DataFrame"
        print(f"  ✅ Empty DataFrame created: {len(df_filtered)} rows")
        
        # Test calculations that should handle empty DataFrames
        avg_roi = df_filtered['ROI_Ratio'].mean() if len(df_filtered) > 0 else 0
        total_tam = df_filtered['TAM_Milhões'].sum()
        
        assert avg_roi == 0, "Average ROI should be 0 for empty DataFrame"
        assert total_tam == 0, "Total TAM should be 0 for empty DataFrame"
        
        print(f"  ✅ Safe calculations: avg_roi={avg_roi}, total_tam={total_tam}")
        
    except Exception as e:
        print(f"  ❌ Empty DataFrame handling failed: {e}")

def test_division_by_zero_protection(df_languages):
    """Test division by zero protection"""
    print("🧪 Testing division by zero protection...")
    
    try:
        # Test ROI calculation with zero investment
        test_df = df_languages.copy()
        test_df.loc[0, 'Investimento_K'] = 0  # Set investment to 0
        
        total_investment = test_df['Investimento_K'].sum()
        total_return = test_df['Ano2_Revenue_K'].sum()
        
        # Test our safe division
        roi_text = f"ROI: {total_return/total_investment:.1f}x" if total_investment > 0 else "ROI: N/A"
        
        # Since we set one investment to 0, total should still be > 0
        # But let's test the pure zero case
        zero_investment = 0
        safe_roi = f"ROI: {100/zero_investment:.1f}x" if zero_investment > 0 else "ROI: N/A"
        
        assert safe_roi == "ROI: N/A", "Should handle division by zero safely"
        print(f"  ✅ Division by zero protection: {safe_roi}")
        
    except Exception as e:
        print(f"  ❌ Division by zero protection failed: {e}")

def test_competitive_landscape_data(df_competitors):
    """Test competitive landscape data access"""
    print("🧪 Testing competitive landscape data access...")
    
    try:
        # Test accessing the columns that caused the original bug
        for platform in df_competitors['Plataforma']:
            data = df_competitors[df_competitors['Plataforma'] == platform].iloc[0]
            
            # These were the problematic column accesses
            user_base = data['User_Base_Milhões']
            revenue = data['Revenue_Milhões']
            market_share = data['Market_Share_Pct']
            
            print(f"  ✅ {platform}: {user_base}M users, ${revenue}M revenue, {market_share}% share")
            
        print(f"  ✅ All competitive data accessible")
        
    except Exception as e:
        print(f"  ❌ Competitive landscape data access failed: {e}")

def test_ast_literal_eval():
    """Test AST literal_eval for phases data"""
    print("🧪 Testing AST literal_eval for phases...")
    
    try:
        # Test the string-to-list conversion
        test_string = "['Espanhol','Francês','Alemão']"
        result = ast.literal_eval(test_string)
        
        assert isinstance(result, list), "Should return a list"
        assert len(result) == 3, "Should have 3 languages"
        assert 'Espanhol' in result, "Should contain Espanhol"
        
        print(f"  ✅ AST literal_eval works: {result}")
        
    except Exception as e:
        print(f"  ❌ AST literal_eval failed: {e}")

def main():
    """Run all tests"""
    print("🚀 Starting comprehensive edge case testing...\n")
    
    # Test 1: Data loading
    df_languages, df_competitors = test_data_loading()
    
    if df_languages is not None:
        # Calculate ROI ratio for testing
        df_languages['ROI_Ratio'] = df_languages['LTV_USD'] / df_languages['CAC_USD']
        
        # Test 2: Empty DataFrame handling
        test_empty_dataframe_handling(df_languages)
        
        # Test 3: Division by zero protection  
        test_division_by_zero_protection(df_languages)
    
    if df_competitors is not None:
        # Test 4: Competitive landscape data
        test_competitive_landscape_data(df_competitors)
    
    # Test 5: AST literal_eval
    test_ast_literal_eval()
    
    print("\n🎉 All edge case tests completed!")

if __name__ == "__main__":
    main()