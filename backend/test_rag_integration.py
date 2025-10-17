"""
Test script untuk verifikasi integrasi InspectionData ke SQL RAG system
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.utils.mock_sql_rag_service import sql_rag_service
import asyncio
import json

async def test_rag_integration():
    print("🔧 Testing RAG Integration with InspectionData...")
    
    # Test refresh data
    print("\n1. Testing data refresh...")
    refresh_result = sql_rag_service.refresh_data_and_vectors()
    print(f"✅ Refresh result: {json.dumps(refresh_result, indent=2)}")
    
    # Test system stats
    print("\n2. Testing system stats...")
    stats = sql_rag_service.get_system_stats()
    print(f"📊 System stats: {json.dumps(stats, indent=2)}")
    
    # Test search with inspection-related query
    print("\n3. Testing search with inspection query...")
    search_result = sql_rag_service.search_relevant_context("inspection maintenance repair", top_k=3)
    print(f"🔍 Search results for 'inspection maintenance repair':")
    print(f"- Machine results: {len(search_result['machine_results'])}")
    print(f"- Lifetime results: {len(search_result['lifetime_results'])}")  
    print(f"- Inspection results: {len(search_result['inspection_results'])}")
    
    if search_result['inspection_results']:
        print("\n📝 Inspection results details:")
        for i, result in enumerate(search_result['inspection_results'][:2], 1):
            metadata = result['data']['metadata']
            print(f"  {i}. Inspection {metadata['inspection_id']} - Score: {result['score']:.2f}")
            print(f"     Machine: {metadata['machine_id']}, Date: {metadata['inspection_date']}")
            print(f"     Condition: {metadata['overall_condition']}, Actions: {metadata['recommended_actions']}")
    
    # Test search with machine-specific query
    print("\n4. Testing search with machine query...")
    machine_search = sql_rag_service.search_relevant_context("EX001 machine tracking", top_k=2)
    print(f"🔍 Search results for 'EX001 machine tracking':")
    print(f"- Machine results: {len(machine_search['machine_results'])}")
    print(f"- Inspection results: {len(machine_search['inspection_results'])}")
    
    # Display combined context
    print("\n5. Combined context for LLM:")
    if search_result['combined_context']:
        print(search_result['combined_context'][:500] + "..." if len(search_result['combined_context']) > 500 else search_result['combined_context'])
    
    print("\n✅ RAG Integration test completed!")

if __name__ == "__main__":
    asyncio.run(test_rag_integration())