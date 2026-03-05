import re
import unicodedata


class SlugGenerator:
    def __init__(self, separator='-', lowercase=True, max_length=None):
        self.separator = separator
        self.lowercase = lowercase
        self.max_length = max_length
    
    def generate(self, text):
        """Generate a slug from the given text."""
        if not text:
            return ''
        
        # Normalize unicode characters
        text = unicodedata.normalize('NFKD', text)
        text = text.encode('ascii', 'ignore').decode('ascii')
        
        # Convert to lowercase if needed
        if self.lowercase:
            text = text.lower()
        
        # Replace spaces and special characters with separator
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', self.separator, text)
        
        # Remove separator from start and end
        text = text.strip(self.separator)
        
        # Apply max length if specified
        if self.max_length:
            text = text[:self.max_length].rstrip(self.separator)
        
        return text
    
    def __call__(self, text):
        """Allow the instance to be called directly."""
        return self.generate(text)


# Usage examples
if __name__ == '__main__':
    slug = SlugGenerator()
    
    print(slug.generate("Hello World!"))  # hello-world
    print(slug.generate("Python 3.11 Release"))  # python-311-release
    print(slug.generate("Café & Restaurant"))  # cafe-restaurant
    print(slug("Multiple   Spaces"))  # multiple-spaces
    
    # Custom separator
    slug_underscore = SlugGenerator(separator='_')
    print(slug_underscore.generate("Hello World"))  # hello_world
    
    # With max length
    slug_short = SlugGenerator(max_length=10)
    print(slug_short.generate("This is a very long title"))  # this-is-a