from django.core.management import execute_from_command_line
import os
import sys

def main():
    
    settings_module = 'videoshare.deployment' if 'WEBSITE_HOSTNAME' in os.environ else 'videoshare.settings'
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Ar you sure its installed and "
            "available on your PYTHONPATH environmnt variable Did you "
            "forget to activate a virtual environmnt?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
