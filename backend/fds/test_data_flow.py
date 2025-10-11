#!/usr/bin/env python3
"""
Test script to verify that real GOES-R requirements flow from database to FDS data engine
"""

import asyncio
import requests
import time
import subprocess
import sys
from database_requirements_service import requirements_service

class DataFlowTester:
    """Test the complete data flow from database to FDS endpoints"""
    
    def __init__(self):
        self.fds_url = "http://localhost:8001"
        self.server_process = None
    
    def start_fds_server(self):
        """Start the FDS server in background"""
        print("🚀 Starting FDS server in background...")
        try:
            self.server_process = subprocess.Popen([
                sys.executable, "start_fds.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait a bit for server to start
            time.sleep(5)
            
            # Test if server is running
            try:
                response = requests.get(f"{self.fds_url}/health", timeout=5)
                if response.status_code == 200:
                    print("✅ FDS server started successfully")
                    return True
            except:
                pass
            
            print("❌ Failed to start FDS server")
            return False
            
        except Exception as e:
            print(f"❌ Error starting server: {e}")
            return False
    
    def stop_fds_server(self):
        """Stop the FDS server"""
        if self.server_process:
            print("🛑 Stopping FDS server...")
            self.server_process.terminate()
            self.server_process = None
    
    async def test_database_requirements(self):
        """Test database requirements are available"""
        print("\n📊 Testing database requirements...")
        
        # Get requirements from database
        requirements = await requirements_service.get_requirements(limit=10)
        print(f"✅ Database has {len(requirements)} requirements")
        
        if requirements:
            sample_req = requirements[0]
            print(f"   Sample: {sample_req['requirement_id']}: {sample_req['title'][:50]}...")
            return True
        else:
            print("❌ No requirements found in database")
            return False
    
    def test_fds_health(self):
        """Test FDS server health"""
        print("\n🏥 Testing FDS server health...")
        
        try:
            response = requests.get(f"{self.fds_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ FDS server healthy: {data}")
                return True
            else:
                print(f"❌ FDS server unhealthy: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Cannot connect to FDS server: {e}")
            return False
    
    def test_regenerate_from_database(self):
        """Test regenerating data from database requirements"""
        print("\n🔄 Testing data regeneration from database...")
        
        try:
            response = requests.post(f"{self.fds_url}/mock/admin/seed", timeout=30)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Data regeneration successful:")
                print(f"   Status: {data.get('status')}")
                print(f"   Source: {data.get('source', 'unknown')}")
                print(f"   Message: {data.get('message')}")
                
                if data.get('source') == 'database_requirements':
                    print(f"   🎉 Successfully using database requirements!")
                    if 'generated' in data:
                        gen = data['generated']
                        print(f"   📊 Generated from real GOES-R requirements:")
                        for key, value in gen.items():
                            print(f"      {key}: {value}")
                    return True
                else:
                    print(f"   ⚠️ Using fallback synthetic data")
                    return False
            else:
                print(f"❌ Regeneration failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error during regeneration: {e}")
            return False
    
    def test_jama_requirements(self):
        """Test Jama requirements endpoint with real data"""
        print("\n📋 Testing Jama requirements endpoint...")
        
        try:
            response = requests.get(f"{self.fds_url}/mock/jama/items?type=requirement&size=5", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Retrieved {len(data)} Jama requirements")
                
                for item in data[:3]:
                    print(f"   • {item['global_id']}: {item['name'][:60]}...")
                    if 'fields' in item and 'source_document' in item['fields']:
                        print(f"     Source: {item['fields']['source_document']}")
                
                # Check if any items have real GOES-R content
                goes_r_items = [item for item in data if 'GOES' in str(item) or 'MRD' in str(item)]
                if goes_r_items:
                    print(f"   🎯 Found {len(goes_r_items)} items with GOES-R content!")
                    return True
                else:
                    print(f"   ⚠️ No obvious GOES-R content detected")
                    return False
            else:
                print(f"❌ Failed to get Jama items: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error getting Jama items: {e}")
            return False
    
    def test_requirements_api(self):
        """Test the requirements management API"""
        print("\n🔧 Testing requirements management API...")
        
        try:
            # Test documents endpoint
            response = requests.get(f"{self.fds_url}/mock/admin/documents", timeout=10)
            if response.status_code == 200:
                data = response.json()
                docs = data.get('documents', [])
                print(f"✅ Found {len(docs)} documents in system")
                
                for doc in docs:
                    print(f"   📄 {doc['original_filename']} ({doc['document_type']})")
                    print(f"      Mission: {doc['mission']}, Requirements: {doc['requirements_extracted']}")
                
                return len(docs) > 0
            else:
                print(f"❌ Failed to get documents: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error getting documents: {e}")
            return False
    
    async def run_complete_test(self):
        """Run complete data flow test"""
        print("🧪 GOES-R Data Flow Test")
        print("=" * 50)
        
        results = []
        
        # Test 1: Database requirements
        results.append(await self.test_database_requirements())
        
        # Test 2: Start FDS server
        results.append(self.start_fds_server())
        
        if not results[-1]:
            print("❌ Cannot proceed without FDS server")
            return
        
        try:
            # Test 3: FDS health
            results.append(self.test_fds_health())
            
            # Test 4: Regenerate from database
            results.append(self.test_regenerate_from_database())
            
            # Test 5: Test Jama endpoint
            results.append(self.test_jama_requirements())
            
            # Test 6: Test admin API
            results.append(self.test_requirements_api())
            
        finally:
            # Always stop the server
            self.stop_fds_server()
        
        # Summary
        print(f"\n📈 TEST RESULTS:")
        print("=" * 30)
        passed = sum(results)
        total = len(results)
        
        test_names = [
            "Database Requirements",
            "FDS Server Start",
            "FDS Health Check", 
            "Data Regeneration",
            "Jama Endpoint",
            "Admin API"
        ]
        
        for i, (test, result) in enumerate(zip(test_names, results)):
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {test}: {status}")
        
        print(f"\n🎯 Overall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 SUCCESS: Real GOES-R requirements are flowing to the data engine!")
        elif passed >= total - 1:
            print("⚠️ MOSTLY WORKING: Minor issues but data flow is functional")
        else:
            print("❌ ISSUES: Data flow needs attention")
        
        print("\n" + "=" * 50)

async def main():
    tester = DataFlowTester()
    await tester.run_complete_test()

if __name__ == "__main__":
    asyncio.run(main())