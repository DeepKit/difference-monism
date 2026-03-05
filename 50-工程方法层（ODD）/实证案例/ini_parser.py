import re
from typing import Dict, Any, Optional
from collections import OrderedDict


class INIParser:
    def __init__(self, case_sensitive: bool = False):
        self.case_sensitive = case_sensitive
        self.data: Dict[str, Dict[str, str]] = OrderedDict()
        self.comments: Dict[str, list] = {}
        
    def parse(self, content: str) -> None:
        """Parse INI content from string"""
        self.data.clear()
        self.comments.clear()
        
        current_section = None
        section_comments = []
        
        for line in content.splitlines():
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
                
            # Handle comments
            if line.startswith(';') or line.startswith('#'):
                section_comments.append(line)
                continue
            
            # Handle sections
            section_match = re.match(r'^\[([^\]]+)\]', line)
            if section_match:
                current_section = section_match.group(1).strip()
                if not self.case_sensitive:
                    current_section = current_section.lower()
                    
                if current_section not in self.data:
                    self.data[current_section] = OrderedDict()
                    
                if section_comments:
                    self.comments[current_section] = section_comments
                    section_comments = []
                continue
            
            # Handle key-value pairs
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # Remove inline comments
                for comment_char in [';', '#']:
                    if comment_char in value:
                        value = value.split(comment_char)[0].strip()
                
                if not self.case_sensitive:
                    key = key.lower()
                
                if current_section is None:
                    current_section = 'DEFAULT'
                    if current_section not in self.data:
                        self.data[current_section] = OrderedDict()
                
                self.data[current_section][key] = value
    
    def load(self, filepath: str, encoding: str = 'utf-8') -> None:
        """Load and parse INI file"""
        with open(filepath, 'r', encoding=encoding) as f:
            content = f.read()
        self.parse(content)
    
    def save(self, filepath: str, encoding: str = 'utf-8') -> None:
        """Save INI data to file"""
        content = self.to_string()
        with open(filepath, 'w', encoding=encoding) as f:
            f.write(content)
    
    def to_string(self) -> str:
        """Convert INI data to string"""
        lines = []
        
        for section, items in self.data.items():
            # Add section comments
            if section in self.comments:
                lines.extend(self.comments[section])
            
            # Add section header
            if section != 'DEFAULT':
                lines.append(f'[{section}]')
            
            # Add key-value pairs
            for key, value in items.items():
                lines.append(f'{key} = {value}')
            
            lines.append('')  # Empty line between sections
        
        return '\n'.join(lines)
    
    def get(self, section: str, key: str, default: Any = None) -> Optional[str]:
        """Get value from section"""
        if not self.case_sensitive:
            section = section.lower()
            key = key.lower()
        
        return self.data.get(section, {}).get(key, default)
    
    def set(self, section: str, key: str, value: str) -> None:
        """Set value in section"""
        if not self.case_sensitive:
            section = section.lower()
            key = key.lower()
        
        if section not in self.data:
            self.data[section] = OrderedDict()
        
        self.data[section][key] = str(value)
    
    def has_section(self, section: str) -> bool:
        """Check if section exists"""
        if not self.case_sensitive:
            section = section.lower()
        return section in self.data
    
    def has_option(self, section: str, key: str) -> bool:
        """Check if option exists in section"""
        if not self.case_sensitive:
            section = section.lower()
            key = key.lower()
        return section in self.data and key in self.data[section]
    
    def sections(self) -> list:
        """Get all section names"""
        return list(self.data.keys())
    
    def options(self, section: str) -> list:
        """Get all option names in section"""
        if not self.case_sensitive:
            section = section.lower()
        return list(self.data.get(section, {}).keys())
    
    def items(self, section: str) -> list:
        """Get all items in section as list of tuples"""
        if not self.case_sensitive:
            section = section.lower()
        return list(self.data.get(section, {}).items())
    
    def remove_section(self, section: str) -> bool:
        """Remove a section"""
        if not self.case_sensitive:
            section = section.lower()
        
        if section in self.data:
            del self.data[section]
            if section in self.comments:
                del self.comments[section]
            return True
        return False
    
    def remove_option(self, section: str, key: str) -> bool:
        """Remove an option from section"""
        if not self.case_sensitive:
            section = section.lower()
            key = key.lower()
        
        if section in self.data and key in self.data[section]:
            del self.data[section][key]
            return True
        return False


# Usage example
if __name__ == '__main__':
    # Create parser
    parser = INIParser()
    
    # Parse from string
    ini_content = """
    ; Database configuration
    [database]
    host = localhost
    port = 5432
    user = admin
    password = secret
    
    # Application settings
    [app]
    debug = true
    log_level = info
    """
    
    parser.parse(ini_content)
    
    # Read values
    print(parser.get('database', 'host'))  # localhost
    print(parser.get('app', 'debug'))      # true
    
    # Set values
    parser.set('database', 'port', '3306')
    parser.set('app', 'timeout', '30')
    
    # Save to file
    parser.save('config.ini')
    
    # Load from file
    parser2 = INIParser()
    parser2.load('config.ini')