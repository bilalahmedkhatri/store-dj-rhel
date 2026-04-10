import re
import os

def fix_models(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix CompositePrimaryKey fields to lowercase
    content = re.sub(r"pk = models\.CompositePrimaryKey\('(.*?)', '(.*?)'\)", 
                     lambda m: f"pk = models.CompositePrimaryKey('{m.group(1).lower()}', '{m.group(2).lower()}')", 
                     content)

    # Convert model references in FK from Class to 'Class'
    # Correcting the regex to be more precise
    def stringify_fk(match):
        full_field_type = match.group(1) # e.g. models.ForeignKey
        model_name = match.group(3).strip()
        
        # If model_name is already a string, don't wrap it
        if model_name.startswith("'") or model_name.startswith('"'):
             return match.group(0)
        
        # If it's 'self', 'User', etc.
        if model_name == 'self':
             return f"{full_field_type}('self',"
        
        return f"{full_field_type}('{model_name}',"

    # Match models.ForeignKey(ModelName, 
    content = re.sub(r"(models\.(ForeignKey|OneToOneField|ManyToManyField))\(([^,\s\)]+),", 
                     stringify_fk, 
                     content)

    # Remove duplicated UserRolesRole classes
    pattern = r"class UserRolesRole\(models\.Model\):.*?(?=(class |$))"
    matches = list(re.finditer(pattern, content, re.DOTALL))
    if len(matches) > 1:
        print(f"Found {len(matches)} occurrences of UserRolesRole. Removing extra ones.")
        # We find the start of the 2nd one and remove everything from there for those classes
        # Actually replace the whole match with empty string for matches[1:]
        for match in matches[1:]:
             content = content.replace(match.group(0), "")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    fix_models('app/models.py')
