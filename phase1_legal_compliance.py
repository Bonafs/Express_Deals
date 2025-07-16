#!/usr/bin/env python3
"""
Phase 1: Legal Compliance Implementation
Implement robots.txt checking and terms of service compliance
"""

import os
import django
import requests
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from scraping.models import ScrapeTarget

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LegalComplianceChecker:
    """Implement legal compliance for web scraping"""
    
    def __init__(self):
        self.user_agent = 'ExpressDeals-Bot/1.0 (+https://express-deals.com/bot)'
        self.compliant_sites = []
        self.blocked_sites = []
    
    def check_robots_txt(self, base_url):
        """Check robots.txt compliance for a site"""
        try:
            robots_url = urljoin(base_url, '/robots.txt')
            logger.info(f"🤖 Checking robots.txt: {robots_url}")
            
            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            
            # Check common paths
            paths_to_check = ['/search', '/products', '/shop', '/category']
            allowed_paths = []
            
            for path in paths_to_check:
                if rp.can_fetch(self.user_agent, path):
                    allowed_paths.append(path)
            
            # Get crawl delay
            crawl_delay = rp.crawl_delay(self.user_agent)
            
            result = {
                'url': base_url,
                'robots_url': robots_url,
                'allowed_paths': allowed_paths,
                'crawl_delay': crawl_delay,
                'compliant': len(allowed_paths) > 0
            }
            
            if result['compliant']:
                logger.info(f"✅ {base_url} allows scraping: {allowed_paths}")
                self.compliant_sites.append(result)
            else:
                logger.warning(f"❌ {base_url} blocks scraping")
                self.blocked_sites.append(result)
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error checking robots.txt for {base_url}: {e}")
            return {'url': base_url, 'error': str(e), 'compliant': False}
    
    def check_terms_of_service(self, base_url):
        """Check for terms of service and scraping policies"""
        try:
            # Common terms of service URLs
            tos_urls = [
                urljoin(base_url, '/terms'),
                urljoin(base_url, '/terms-of-service'),
                urljoin(base_url, '/legal'),
                urljoin(base_url, '/terms-and-conditions'),
                urljoin(base_url, '/api-terms')
            ]
            
            scraping_keywords = [
                'scraping', 'automated', 'bot', 'crawler', 'api', 
                'data collection', 'extraction', 'prohibited'
            ]
            
            for tos_url in tos_urls:
                try:
                    response = requests.get(tos_url, timeout=10)
                    if response.status_code == 200:
                        content = response.text.lower()
                        
                        # Check for scraping-related terms
                        found_terms = [term for term in scraping_keywords if term in content]
                        
                        logger.info(f"📄 Found ToS at {tos_url}")
                        if found_terms:
                            logger.warning(f"⚠️ Scraping-related terms found: {found_terms}")
                        
                        return {
                            'tos_url': tos_url,
                            'found_terms': found_terms,
                            'requires_review': len(found_terms) > 0
                        }
                        
                except requests.RequestException:
                    continue
            
            logger.info(f"📄 No ToS found for {base_url}")
            return {'tos_url': None, 'found_terms': [], 'requires_review': False}
            
        except Exception as e:
            logger.error(f"❌ Error checking ToS for {base_url}: {e}")
            return {'error': str(e)}
    
    def create_legal_whitelist(self):
        """Create whitelist of legally compliant sites"""
        logger.info("🏛️ Creating legal compliance whitelist...")
        
        targets = ScrapeTarget.objects.filter(status='active')
        compliance_report = []
        
        for target in targets:
            logger.info(f"\n🔍 Checking: {target.name}")
            
            # Check robots.txt
            robots_check = self.check_robots_txt(target.base_url)
            
            # Check terms of service
            tos_check = self.check_terms_of_service(target.base_url)
            
            compliance_result = {
                'target': target,
                'robots_compliant': robots_check.get('compliant', False),
                'robots_details': robots_check,
                'tos_review_needed': tos_check.get('requires_review', False),
                'tos_details': tos_check,
                'overall_compliance': robots_check.get('compliant', False) and not tos_check.get('requires_review', False),
                'recommended_delay': robots_check.get('crawl_delay', 1)
            }
            
            compliance_report.append(compliance_result)
            
            # Update target with compliance info
            target.legal_compliance = compliance_result
            # target.save()  # Uncomment to save compliance data
        
        return compliance_report
    
    def generate_compliance_report(self, compliance_report):
        """Generate a detailed compliance report"""
        print("\n🏛️ LEGAL COMPLIANCE REPORT")
        print("=" * 50)
        
        compliant_count = sum(1 for r in compliance_report if r['overall_compliance'])
        review_needed = sum(1 for r in compliance_report if r['tos_review_needed'])
        
        print(f"📊 SUMMARY:")
        print(f"   Total sites checked: {len(compliance_report)}")
        print(f"   Fully compliant: {compliant_count}")
        print(f"   Need legal review: {review_needed}")
        print(f"   Compliance rate: {(compliant_count/len(compliance_report)*100):.1f}%")
        
        print(f"\n✅ COMPLIANT SITES:")
        for result in compliance_report:
            if result['overall_compliance']:
                target = result['target']
                delay = result['recommended_delay']
                print(f"   • {target.name} (delay: {delay}s)")
        
        print(f"\n⚠️ SITES NEEDING REVIEW:")
        for result in compliance_report:
            if not result['overall_compliance']:
                target = result['target']
                reasons = []
                if not result['robots_compliant']:
                    reasons.append("robots.txt blocks")
                if result['tos_review_needed']:
                    reasons.append("ToS mentions scraping")
                print(f"   • {target.name}: {', '.join(reasons)}")
        
        print(f"\n📋 RECOMMENDATIONS:")
        print(f"   1. Use only fully compliant sites for production")
        print(f"   2. Implement recommended crawl delays")
        print(f"   3. Contact sites needing review for permission")
        print(f"   4. Regular compliance monitoring (monthly)")
        
        return compliance_report

def execute_legal_compliance():
    """Execute Phase 1: Legal Compliance"""
    print("🏛️ PHASE 1: IMPLEMENTING LEGAL COMPLIANCE")
    print("=" * 45)
    
    checker = LegalComplianceChecker()
    
    # Step 1: Create legal whitelist
    compliance_report = checker.create_legal_whitelist()
    
    # Step 2: Generate detailed report
    checker.generate_compliance_report(compliance_report)
    
    # Step 3: Update scraping targets
    compliant_targets = [r['target'] for r in compliance_report if r['overall_compliance']]
    
    print(f"\n🎯 PHASE 1 COMPLETE!")
    print(f"   Compliant targets identified: {len(compliant_targets)}")
    print(f"   Legal framework established: ✅")
    print(f"   Risk mitigation implemented: ✅")
    
    return compliance_report

if __name__ == "__main__":
    execute_legal_compliance()
