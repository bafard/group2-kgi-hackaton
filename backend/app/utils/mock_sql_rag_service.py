"""
Mock RAG Service for demonstration purposes.
This provides the same interface as the full RAG service but uses mock data.
"""

import json
import logging
from typing import Dict, Any, List
from datetime import datetime
from ..utils.sql_server_connection import sql_server

logger = logging.getLogger(__name__)

class MockSQLRAGService:
    """
    Mock SQL-based RAG Service that simulates vector search with simple text matching
    """
    
    def __init__(self):
        self.machine_data = []
        self.lifetime_data = []
        self.inspection_data = []
        self.last_refresh = None
        
    def refresh_data_and_vectors(self) -> Dict[str, Any]:
        """
        Mock refresh that loads data without creating actual vectors
        """
        try:
            logger.info("🔄 Starting mock RAG data refresh from SQL Server...")
            
            # Fetch real data but use simple text search instead of vectors
            machine_query = """
            SELECT TOP 20
                ID as Machine_ID,
                Serial,
                Machine_Location as Location,
                SMR_Hours as Operating_Hours,
                Model,
                Type,
                Delivery_Date_EQP_Care,
                Latitude,
                Longitude,
                GPS_Time,
                Last_Communication_Date
            FROM Machine_Tracking 
            ORDER BY SMR_Hours DESC
            """
            logger.info(f"🔍 Machine query: {machine_query}")
            
            lifetime_query = """
            SELECT TOP 20
                ID as UC_ID,
                Model,
                General_Sand,
                Soil,
                Marsh,
                Coal,
                Hard_Rock,
                Brittle_Rock,
                Pure_Sand_Middle_East,
                Component
            FROM UC_Life_Time 
            ORDER BY ID
            """
            
            inspection_query = """
            SELECT TOP 20
                ID,
                Serial_No,
                Inspection_Date,
                Machine_Type,
                Model_Code,
                SMR,
                Inspected_By,
                Branch_Name,
                Job_Site,
                Comments,
                UnderfootConditions_Terrain,
                Application_Ground,
                LinkPitch_PercentWorn_LHS,
                LinkPitch_PercentWorn_RHS,
                Bushings_PercentWorn_LHS
            FROM InspectionData 
            ORDER BY ID DESC
            """
            
            try:
                conn = sql_server.get_connection()
                cursor = conn.cursor()
                
                # Get Machine data
                logger.info("🔍 Executing machine query...")
                cursor.execute(machine_query)
                machine_rows = cursor.fetchall()
                machine_columns = [column[0] for column in cursor.description]
                logger.info(f"🔍 Machine query successful: {len(machine_rows)} rows, columns: {machine_columns}")
                
                self.machine_data = []
                for row in machine_rows:
                    row_dict = dict(zip(machine_columns, row))
                    text_content = f"Machine {row_dict.get('Machine_ID', '')} Serial {row_dict.get('Serial', '')} Model {row_dict.get('Model', '')} at {row_dict.get('Location', '')} Type {row_dict.get('Type', '')} with {row_dict.get('Operating_Hours', 0)} SMR hours"
                    
                    self.machine_data.append({
                        'id': f"machine_{row_dict.get('Machine_ID', '')}",
                        'text': text_content,
                        'metadata': {
                            'type': 'machine_tracking',
                            'machine_id': row_dict.get('Machine_ID', ''),
                            'serial_number': row_dict.get('Serial', ''),
                            'model': row_dict.get('Model', ''),
                            'location': row_dict.get('Location', ''),
                            'machine_type': row_dict.get('Machine_Type', ''),
                            'operating_hours': float(row_dict.get('Operating_Hours', 0)) if row_dict.get('Operating_Hours') else 0,
                            'latitude': row_dict.get('Latitude', ''),
                            'longitude': row_dict.get('Longitude', '')
                        }
                    })
                
                # Get UC Lifetime data
                logger.info("🔍 Executing UC lifetime query...")
                cursor.execute(lifetime_query)
                lifetime_rows = cursor.fetchall()
                lifetime_columns = [column[0] for column in cursor.description]
                logger.info(f"🔍 UC query successful: {len(lifetime_rows)} rows, columns: {lifetime_columns}")
                
                self.lifetime_data = []
                for row in lifetime_rows:
                    row_dict = dict(zip(lifetime_columns, row))
                    text_content = f"UC component {row_dict.get('UC_ID', '')} Model {row_dict.get('Model', '')} Component {row_dict.get('Component', '')} General Sand life {row_dict.get('General_Sand', 0)} hours Hard Rock life {row_dict.get('Hard_Rock', 0)} hours"
                    
                    self.lifetime_data.append({
                        'id': f"uc_{row_dict.get('UC_ID', '')}",
                        'text': text_content,
                        'metadata': {
                            'type': 'uc_lifetime',
                            'uc_id': row_dict.get('UC_ID', ''),
                            'model': row_dict.get('Model', ''),
                            'component': row_dict.get('Component', ''),
                            'general_sand': float(row_dict.get('General_Sand', 0)) if row_dict.get('General_Sand') else 0,
                            'soil': float(row_dict.get('Soil', 0)) if row_dict.get('Soil') else 0,
                            'marsh': float(row_dict.get('Marsh', 0)) if row_dict.get('Marsh') else 0,
                            'coal': float(row_dict.get('Coal', 0)) if row_dict.get('Coal') else 0,
                            'hard_rock': float(row_dict.get('Hard_Rock', 0)) if row_dict.get('Hard_Rock') else 0,
                            'brittle_rock': float(row_dict.get('Brittle_Rock', 0)) if row_dict.get('Brittle_Rock') else 0
                        }
                    })

                # Get Inspection Data
                logger.info("🔍 Executing inspection data query...")
                cursor.execute(inspection_query)
                inspection_rows = cursor.fetchall()
                inspection_columns = [column[0] for column in cursor.description]
                logger.info(f"🔍 Inspection query successful: {len(inspection_rows)} rows, columns: {inspection_columns}")
                
                self.inspection_data = []
                for row in inspection_rows:
                    row_dict = dict(zip(inspection_columns, row))
                    inspection_date = row_dict.get('Inspection_Date', '')
                    if inspection_date:
                        inspection_date_str = inspection_date.strftime('%Y-%m-%d') if hasattr(inspection_date, 'strftime') else str(inspection_date)
                    else:
                        inspection_date_str = ''
                    
                    text_content = f"Inspection {row_dict.get('ID', '')} Machine {row_dict.get('Serial_No', '')} on {inspection_date_str} Type {row_dict.get('Machine_Type', '')} Model {row_dict.get('Model_Code', '')} SMR {row_dict.get('SMR', 0)} hours Inspector {row_dict.get('Inspected_By', '')} Site {row_dict.get('Job_Site', '')} Terrain {row_dict.get('UnderfootConditions_Terrain', '')} Link Worn L/R {row_dict.get('LinkPitch_PercentWorn_LHS', 0)}/{row_dict.get('LinkPitch_PercentWorn_RHS', 0)}%"
                    
                    self.inspection_data.append({
                        'id': f"inspection_{row_dict.get('ID', '')}",
                        'text': text_content,
                        'metadata': {
                            'type': 'inspection_data',
                            'inspection_id': row_dict.get('ID', ''),
                            'serial_no': row_dict.get('Serial_No', ''),
                            'inspection_date': inspection_date_str,
                            'machine_type': row_dict.get('Machine_Type', ''),
                            'model_code': row_dict.get('Model_Code', ''),
                            'smr_hours': float(row_dict.get('SMR', 0)) if row_dict.get('SMR') else 0,
                            'inspected_by': row_dict.get('Inspected_By', ''),
                            'branch_name': row_dict.get('Branch_Name', ''),
                            'job_site': row_dict.get('Job_Site', ''),
                            'comments': row_dict.get('Comments', ''),
                            'underfoot_terrain': row_dict.get('UnderfootConditions_Terrain', ''),
                            'application_ground': row_dict.get('Application_Ground', ''),
                            'link_worn_lhs': float(row_dict.get('LinkPitch_PercentWorn_LHS', 0)) if row_dict.get('LinkPitch_PercentWorn_LHS') else 0,
                            'link_worn_rhs': float(row_dict.get('LinkPitch_PercentWorn_RHS', 0)) if row_dict.get('LinkPitch_PercentWorn_RHS') else 0,
                            'bushing_worn_lhs': float(row_dict.get('Bushings_PercentWorn_LHS', 0)) if row_dict.get('Bushings_PercentWorn_LHS') else 0
                        }
                    })
                
                conn.close()
                logger.info(f"📊 Loaded {len(self.machine_data)} machine records, {len(self.lifetime_data)} UC records, and {len(self.inspection_data)} inspection records")
                
            except Exception as e:
                logger.warning(f"⚠️ Could not load real data, using mock data: {str(e)}")
                self._create_mock_data()
            
            self.last_refresh = datetime.now()
            
            return {
                'success': True,
                'machine_records': len(self.machine_data),
                'lifetime_records': len(self.lifetime_data),
                'inspection_records': len(self.inspection_data),
                'last_refresh': self.last_refresh.isoformat(),
                'message': 'Mock RAG data refreshed successfully'
            }
            
        except Exception as e:
            logger.error(f"❌ Error in mock RAG refresh: {str(e)}")
            self._create_mock_data()
            return {
                'success': False,
                'machine_records': len(self.machine_data),
                'lifetime_records': len(self.lifetime_data),
                'inspection_records': len(self.inspection_data),
                'last_refresh': datetime.now().isoformat(),
                'message': f'Using fallback mock data: {str(e)}'
            }
    
    def _create_mock_data(self):
        """Create mock data for demonstration"""
        self.machine_data = [
            {
                'id': 'machine_EX001',
                'text': 'Machine EX001 Serial ABC123 Excavator Model PC210 at Mining Site North status Active operated by John Smith in Operations department with 2500 hours',
                'metadata': {
                    'type': 'machine_tracking',
                    'machine_id': 'EX001',
                    'serial_number': 'ABC123',
                    'model': 'PC210',
                    'location': 'Mining Site North',
                    'machine_type': 'Excavator',
                    'operating_hours': 2500,
                    'latitude': '',
                    'longitude': ''
                }
            },
            {
                'id': 'machine_BD002',
                'text': 'Machine BD002 Serial DEF456 Bulldozer Model D155 at Construction Site East status Maintenance Required operated by Mike Johnson in Construction department with 3200 hours',
                'metadata': {
                    'type': 'machine_tracking',
                    'machine_id': 'BD002',
                    'serial_number': 'DEF456',
                    'model': 'D155',
                    'location': 'Construction Site East',
                    'machine_type': 'Bulldozer',
                    'operating_hours': 3200,
                    'latitude': '',
                    'longitude': ''
                }
            }
        ]
        
        self.lifetime_data = [
            {
                'id': 'uc_001',
                'text': 'UC component 001 type Track Chain on machine EX001 has 25% life remaining condition Worn replacement cost $15000',
                'metadata': {
                    'type': 'uc_lifetime',
                    'uc_id': 'UC001',
                    'machine_id': 'EX001',
                    'component_type': 'Track Chain',
                    'current_hours': 2500,
                    'expected_life_hours': 3000,
                    'remaining_life_percentage': 25,
                    'condition_status': 'Worn',
                    'replacement_cost': 15000
                }
            },
            {
                'id': 'uc_002',
                'text': 'UC component 002 type Track Shoe on machine BD002 has 60% life remaining condition Good replacement cost $8000',
                'metadata': {
                    'type': 'uc_lifetime',
                    'uc_id': 'UC002',
                    'machine_id': 'BD002',
                    'component_type': 'Track Shoe',
                    'current_hours': 1200,
                    'expected_life_hours': 2000,
                    'remaining_life_percentage': 60,
                    'condition_status': 'Good',
                    'replacement_cost': 8000
                }
            }
        ]

        self.inspection_data = [
            {
                'id': 'inspection_001',
                'text': 'Inspection 001 Machine EX001 on 2024-01-15 Type Excavator Model PC210 SMR 2500 hours Inspector John Doe Site Mining Site North Terrain Rocky Link Worn L/R 75/80%',
                'metadata': {
                    'type': 'inspection_data',
                    'inspection_id': '001',
                    'serial_no': 'EX001',
                    'inspection_date': '2024-01-15',
                    'machine_type': 'Excavator',
                    'model_code': 'PC210',
                    'smr_hours': 2500,
                    'inspected_by': 'John Doe',
                    'branch_name': 'Jakarta Branch',
                    'job_site': 'Mining Site North',
                    'comments': 'Undercarriage showing excessive wear, replacement needed',
                    'underfoot_terrain': 'Rocky',
                    'application_ground': 'Hard rock mining',
                    'link_worn_lhs': 75.5,
                    'link_worn_rhs': 80.2,
                    'bushing_worn_lhs': 65.0
                }
            },
            {
                'id': 'inspection_002',
                'text': 'Inspection 002 Machine BD002 on 2024-01-10 Type Bulldozer Model D155 SMR 3200 hours Inspector Jane Smith Site Construction Site East Terrain Muddy Link Worn L/R 45/50%',
                'metadata': {
                    'type': 'inspection_data',
                    'inspection_id': '002',
                    'serial_no': 'BD002',
                    'inspection_date': '2024-01-10',
                    'machine_type': 'Bulldozer',
                    'model_code': 'D155',
                    'smr_hours': 3200,
                    'inspected_by': 'Jane Smith',
                    'branch_name': 'Surabaya Branch',
                    'job_site': 'Construction Site East',
                    'comments': 'Normal wear pattern, continue monitoring',
                    'underfoot_terrain': 'Muddy',
                    'application_ground': 'General construction',
                    'link_worn_lhs': 45.0,
                    'link_worn_rhs': 50.0,
                    'bushing_worn_lhs': 40.0
                }
            }
        ]
    
    def search_relevant_context(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Mock search using simple text matching
        """
        try:
            if not self.machine_data and not self.lifetime_data and not self.inspection_data:
                self.refresh_data_and_vectors()
            
            query_lower = query.lower()
            
            results = {
                'machine_results': [],
                'lifetime_results': [],
                'inspection_results': [],
                'combined_context': '',
                'query': query
            }
            
            # Simple text matching for machine data
            for item in self.machine_data:
                if any(word in item['text'].lower() for word in query_lower.split()):
                    score = len([word for word in query_lower.split() if word in item['text'].lower()]) / len(query_lower.split())
                    results['machine_results'].append({
                        'score': score,
                        'data': item,
                        'relevance': 'high' if score > 0.5 else 'medium' if score > 0.2 else 'low'
                    })
            
            # Simple text matching for UC data
            for item in self.lifetime_data:
                if any(word in item['text'].lower() for word in query_lower.split()):
                    score = len([word for word in query_lower.split() if word in item['text'].lower()]) / len(query_lower.split())
                    results['lifetime_results'].append({
                        'score': score,
                        'data': item,
                        'relevance': 'high' if score > 0.5 else 'medium' if score > 0.2 else 'low'
                    })

            # Simple text matching for Inspection data
            for item in self.inspection_data:
                if any(word in item['text'].lower() for word in query_lower.split()):
                    score = len([word for word in query_lower.split() if word in item['text'].lower()]) / len(query_lower.split())
                    results['inspection_results'].append({
                        'score': score,
                        'data': item,
                        'relevance': 'high' if score > 0.5 else 'medium' if score > 0.2 else 'low'
                    })
            
            # Sort by score and limit results
            results['machine_results'] = sorted(results['machine_results'], key=lambda x: x['score'], reverse=True)[:top_k]
            results['lifetime_results'] = sorted(results['lifetime_results'], key=lambda x: x['score'], reverse=True)[:top_k]
            results['inspection_results'] = sorted(results['inspection_results'], key=lambda x: x['score'], reverse=True)[:top_k]
            
            # Format context
            results['combined_context'] = self._format_context_for_llm(results)
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Error in mock search: {str(e)}")
            return {
                'machine_results': [],
                'lifetime_results': [],
                'inspection_results': [],
                'combined_context': '',
                'query': query
            }
    
    def _format_context_for_llm(self, results: Dict) -> str:
        """Format search results as context for LLM"""
        context_parts = []
        
        if results['machine_results']:
            context_parts.append("=== MACHINE TRACKING DATA ===")
            for result in results['machine_results'][:2]:
                metadata = result['data']['metadata']
                context_parts.append(f"""
Machine {metadata['machine_id']} ({metadata['serial_number']}):
- Model: {metadata['model']}
- Location: {metadata['location']}
- Type: {metadata.get('machine_type', 'Unknown')}
- SMR Hours: {metadata['operating_hours']}
- Latitude: {metadata.get('latitude', '')}
- Longitude: {metadata.get('longitude', '')}
                """.strip())
        
        if results['lifetime_results']:
            context_parts.append("\n=== UNDERCARRIAGE LIFETIME DATA ===")
            for result in results['lifetime_results'][:2]:
                metadata = result['data']['metadata']
                context_parts.append(f"""
UC Component {metadata['uc_id']}:
- Model: {metadata['model']}
- Component: {metadata['component']}
- General Sand Life: {metadata['general_sand']} hours
- Soil Life: {metadata['soil']} hours  
- Hard Rock Life: {metadata['hard_rock']} hours
- Marsh Life: {metadata['marsh']} hours
                """.strip())

        if results['inspection_results']:
            context_parts.append("\n=== INSPECTION DATA ===")
            for result in results['inspection_results'][:2]:
                metadata = result['data']['metadata']
                context_parts.append(f"""
Inspection {metadata['inspection_id']} - Machine {metadata['serial_no']}:
- Date: {metadata['inspection_date']}
- Machine Type: {metadata.get('machine_type', 'Unknown')}
- Model: {metadata.get('model_code', '')}
- SMR Hours: {metadata['smr_hours']}
- Inspector: {metadata.get('inspected_by', '')}
- Job Site: {metadata.get('job_site', '')}
- Branch: {metadata.get('branch_name', '')}
- Terrain: {metadata.get('underfoot_terrain', '')}
- Application: {metadata.get('application_ground', '')}
- Link Wear L/R: {metadata.get('link_worn_lhs', 0)}/{metadata.get('link_worn_rhs', 0)}%
- Bushing Wear L: {metadata.get('bushing_worn_lhs', 0)}%
- Comments: {metadata.get('comments', '')}
                """.strip())
        
        return "\n".join(context_parts)
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get current system statistics"""
        return {
            'machine_records': len(self.machine_data),
            'lifetime_records': len(self.lifetime_data),
            'inspection_records': len(self.inspection_data),
            'has_machine_index': len(self.machine_data) > 0,
            'has_lifetime_index': len(self.lifetime_data) > 0,
            'has_inspection_index': len(self.inspection_data) > 0,
            'last_refresh': self.last_refresh.isoformat() if self.last_refresh else None,
            'embedding_model': 'mock-text-search',
            'embedding_dimension': 'N/A (mock)'
        }

# Global mock instance
sql_rag_service = MockSQLRAGService()