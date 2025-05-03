from django.core.management.base import BaseCommand
from django.urls import get_resolver, reverse, URLPattern, URLResolver
from django.conf import settings

class Command(BaseCommand):
    help = "List all registered URLs in the project with their full URLs"

    def handle(self, *args, **kwargs):
        # Base domain (ensure this is configured in settings.py)
        base_url = getattr(settings, "DEFAULT_DOMAIN", "http://localhost")
        
        self.stdout.write("Registered Full URLs:")
        self.stdout.write("======================")
        
        # Recursively process URL patterns
        def process_patterns(patterns, parent_pattern=""):
            for pattern in patterns:
                if isinstance(pattern, URLPattern):  # Handle individual URL patterns
                    try:
                        if pattern.name:  # Only process named URLs
                            full_path = reverse(pattern.name)
                            full_url = f"{base_url}{full_path}"
                            self.stdout.write(f"- {pattern.name}: {full_url}")
                        else:
                            self.stdout.write(f"- [Unnamed Pattern]: {parent_pattern}{pattern.pattern}")
                    except Exception as e:
                        self.stdout.write(f"- [Error with {pattern.pattern}]: {e}")
                elif isinstance(pattern, URLResolver):  # Handle nested patterns
                    self.stdout.write(f"Processing included patterns: {parent_pattern}{pattern.pattern}")
                    process_patterns(pattern.url_patterns, parent_pattern=f"{parent_pattern}{pattern.pattern}/")
        
        # Start processing from the root resolver
        root_resolver = get_resolver()
        process_patterns(root_resolver.url_patterns)

