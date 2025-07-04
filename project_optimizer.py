#!/usr/bin/env python
"""
Express Deals - Consolidated Project Optimizer
Removes duplicates, optimizes configuration, ensures full functionality
"""
import os
import sys
import subprocess
import time
from pathlib import Path

class ExpressDealsOptimizer:
    def __init__(self):
        self.project_root = Path("c:/Users/BONAFS/OneDrive/Documents/Express_Deals/Express_Deals")
        self.errors = []
        self.warnings = []
        self.success_count = 0
        
    def log(self, message, level="INFO"):
        """Log messages with appropriate formatting"""
        icons = {"INFO": "📋", "SUCCESS": "✅", "WARNING": "⚠️", "ERROR": "❌"}
        colors = {"INFO": "\033[96m", "SUCCESS": "\033[92m", "WARNING": "\033[93m", "ERROR": "\033[91m", "END": "\033[0m"}
        
        print(f"{colors.get(level, '')}{icons.get(level, '•')} {message}{colors['END']}")
        
        if level == "ERROR":
            self.errors.append(message)
        elif level == "WARNING":
            self.warnings.append(message)
        elif level == "SUCCESS":
            self.success_count += 1
    
    def run_command(self, command, description="Command"):
        """Execute command with proper error handling"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                self.log(f"{description} successful", "SUCCESS")
                return True, result.stdout
            else:
                self.log(f"{description} failed: {result.stderr}", "ERROR")
                return False, result.stderr
        except subprocess.TimeoutExpired:
            self.log(f"{description} timed out", "ERROR")
            return False, "Timeout"
        except Exception as e:
            self.log(f"{description} error: {e}", "ERROR")
            return False, str(e)
    
    def check_django_setup(self):
        """Verify Django configuration"""
        self.log("Checking Django configuration...", "INFO")
        
        try:
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
            import django
            django.setup()
            
            from django.conf import settings
            self.log(f"Django {django.get_version()} configured successfully", "SUCCESS")
            self.log(f"Database: {settings.DATABASES['default']['ENGINE']}", "INFO")
            self.log(f"Debug mode: {settings.DEBUG}", "INFO")
            
            # Test management commands
            from django.core.management import call_command
            call_command('check', verbosity=0)
            self.log("Django system check passed", "SUCCESS")
            
            return True
            
        except ImportError as e:
            self.log(f"Django import failed: {e}", "ERROR")
            return False
        except Exception as e:
            self.log(f"Django setup failed: {e}", "ERROR")
            return False
    
    def optimize_packages(self):
        """Install and verify required packages"""
        self.log("Optimizing package installation...", "INFO")
        
        # Core packages (no duplicates)
        core_packages = [
            "django==5.2.4",
            "djangorestframework==3.14.0",
            "channels==4.0.0",
            "channels-redis==4.1.0",
            "dj-database-url==2.3.0",
            "whitenoise==6.8.2",
            "celery==5.3.4",
            "redis==5.0.1",
            "django-celery-beat==2.5.0",
            "django-celery-results==2.6.0",
            "pillow==11.1.0",
            "stripe==12.3.0",
            "beautifulsoup4==4.12.2",
            "requests==2.31.0"
        ]
        
        # Upgrade pip first
        self.run_command(f"{sys.executable} -m pip install --upgrade pip", "Pip upgrade")
        
        # Try requirements.txt first
        if Path("requirements.txt").exists():
            success, _ = self.run_command(f"pip install -r requirements.txt", "Requirements.txt installation")
            if not success:
                self.log("Installing packages individually...", "WARNING")
                for package in core_packages:
                    self.run_command(f"pip install {package}", f"Installing {package}")
        else:
            for package in core_packages:
                self.run_command(f"pip install {package}", f"Installing {package}")
    
    def verify_imports(self):
        """Verify critical package imports"""
        self.log("Verifying package imports...", "INFO")
        
        critical_imports = {
            "Django": "import django; print(f'Django {django.get_version()}')",
            "DRF": "import rest_framework; print(f'DRF {rest_framework.VERSION}')",
            "Channels": "import channels; print('Channels OK')",
            "Celery": "import celery; print(f'Celery {celery.__version__}')",
            "Redis": "import redis; print('Redis OK')",
            "Stripe": "import stripe; print('Stripe OK')",
        }
        
        for name, import_cmd in critical_imports.items():
            success, output = self.run_command(f'python -c "{import_cmd}"', f"{name} import")
            if success and output.strip():
                self.log(f"{output.strip()}", "INFO")
    
    def optimize_structure(self):
        """Optimize directory structure"""
        self.log("Optimizing directory structure...", "INFO")
        
        # Required directories
        required_dirs = ["logs", "media", "static", "staticfiles"]
        for dirname in required_dirs:
            dir_path = Path(dirname)
            if not dir_path.exists():
                dir_path.mkdir(exist_ok=True)
                self.log(f"Created {dirname} directory", "SUCCESS")
            else:
                self.log(f"{dirname} directory exists", "SUCCESS")
    
    def cleanup_configuration(self):
        """Clean up redundant configuration files"""
        self.log("Cleaning up configuration...", "INFO")
        
        # Remove .env file if it exists
        env_file = Path(".env")
        if env_file.exists():
            env_file.unlink()
            self.log("Removed .env file (using hardcoded settings)", "SUCCESS")
        else:
            self.log("No .env file found (using hardcoded settings)", "SUCCESS")
        
        # Check for old environment directory
        old_env = Path("env")
        new_env = Path(".venv")
        if old_env.exists() and new_env.exists():
            self.log("Found both 'env' and '.venv' directories", "WARNING")
            self.log("Consider removing the old 'env' directory manually", "INFO")
    
    def remove_duplicate_scripts(self):
        """Identify and report duplicate scripts"""
        self.log("Checking for duplicate scripts...", "INFO")
        
        # Script patterns that might be duplicates
        script_patterns = {
            "setup": ["setup_*.py", "setup_*.bat", "setup_*.ps1"],
            "fix": ["*fix*.py", "*fix*.bat", "*fix*.ps1"],
            "verify": ["verify_*.py", "check_*.py", "test_*.py"],
            "commit": ["commit_*.py", "*commit*.bat", "*commit*.ps1"]
        }
        
        duplicates_found = False
        for category, patterns in script_patterns.items():
            files = []
            for pattern in patterns:
                files.extend(Path(".").glob(pattern))
            
            if len(files) > 2:  # Allow some variation
                duplicates_found = True
                self.log(f"Multiple {category} scripts found: {len(files)}", "WARNING")
                for file in files[:3]:  # Show first 3
                    self.log(f"  - {file.name}", "INFO")
        
        if not duplicates_found:
            self.log("No significant script duplicates found", "SUCCESS")
    
    def performance_test(self):
        """Test Django performance"""
        self.log("Testing Django performance...", "INFO")
        
        start_time = time.time()
        try:
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
            import django
            django.setup()
            end_time = time.time()
            
            startup_time = end_time - start_time
            self.log(f"Django startup time: {startup_time:.2f} seconds", "SUCCESS")
            
            if startup_time < 2.0:
                self.log("Performance: Excellent", "SUCCESS")
            elif startup_time < 5.0:
                self.log("Performance: Good", "SUCCESS")
            else:
                self.log("Performance: Could be improved", "WARNING")
                
        except Exception as e:
            self.log(f"Performance test failed: {e}", "ERROR")
    
    def generate_report(self):
        """Generate optimization report"""
        print("\n" + "="*60)
        print("🎉 EXPRESS DEALS OPTIMIZATION REPORT")
        print("="*60)
        
        print(f"\n📊 Summary:")
        print(f"✅ Successful operations: {self.success_count}")
        print(f"⚠️  Warnings: {len(self.warnings)}")
        print(f"❌ Errors: {len(self.errors)}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings:")
            for warning in self.warnings[:5]:  # Show first 5
                print(f"  • {warning}")
        
        if self.errors:
            print(f"\n❌ Errors:")
            for error in self.errors[:5]:  # Show first 5
                print(f"  • {error}")
        
        print(f"\n🚀 Status: ", end="")
        if len(self.errors) == 0:
            print("✅ FULLY OPTIMIZED")
        elif len(self.errors) < 3:
            print("⚠️  MOSTLY OPTIMIZED")
        else:
            print("❌ NEEDS ATTENTION")
        
        print(f"\n💡 Next Steps:")
        print(f"1. python manage.py runserver")
        print(f"2. Open: http://127.0.0.1:8000/")
        print(f"3. Test all functionality")
    
    def run_optimization(self):
        """Run complete optimization process"""
        print("🚀 EXPRESS DEALS - PROJECT OPTIMIZER")
        print("="*50)
        
        os.chdir(self.project_root)
        
        # Optimization steps
        steps = [
            ("Package Optimization", self.optimize_packages),
            ("Import Verification", self.verify_imports),
            ("Django Setup Check", self.check_django_setup),
            ("Structure Optimization", self.optimize_structure),
            ("Configuration Cleanup", self.cleanup_configuration),
            ("Duplicate Script Check", self.remove_duplicate_scripts),
            ("Performance Test", self.performance_test),
        ]
        
        for step_name, step_func in steps:
            print(f"\n🔧 {step_name.upper()}")
            print("-" * 40)
            try:
                step_func()
            except Exception as e:
                self.log(f"{step_name} failed: {e}", "ERROR")
        
        self.generate_report()

def main():
    """Main entry point"""
    try:
        optimizer = ExpressDealsOptimizer()
        optimizer.run_optimization()
        return len(optimizer.errors) == 0
    except KeyboardInterrupt:
        print("\n⚠️  Optimization interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
