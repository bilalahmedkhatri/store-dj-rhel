import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from app.models import ProductOptionGroup, ProductOption, ProductOptionGroupTranslation, ProductOptionTranslation

def check_options():
    groups = ProductOptionGroup.objects.all()
    print(f"Option Groups: {groups.count()}")
    for g in groups:
        trans = ProductOptionGroupTranslation.objects.filter(baseid=g, languagecode='en').first()
        name = trans.name if trans else g.code
        print(f"Group: {name} (ID: {g.id}, Code: {g.code})")
        options = ProductOption.objects.filter(groupid=g)
        for o in options:
            o_trans = ProductOptionTranslation.objects.filter(baseid=o, languagecode='en').first()
            o_name = o_trans.name if o_trans else o.code
            print(f"  Option: {o_name} (ID: {o.id}, Code: {o.code})")

if __name__ == "__main__":
    check_options()
