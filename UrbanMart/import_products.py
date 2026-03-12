import os 
import django
import csv
import json
import ast
from decimal import Decimal


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UrbanMart.settings')
django.setup()

from Products.models import Products
from Categories.models import Category

# Defining 4 target categories with keyword for matching
TARGET_CATEGORIES = {
    'fashion' : {
        'keywords' : ['clothing', 'fashion', 'apparel', 'wear', 'shirt', 'jeans', 'dress', 'kurta', 'saree', 'ethnic', 'western', 'shoe', 'footwear', 'sandal', 'boot', 'accessories', 'jewellery', 'watch', 'lingerie', 't-shirt', 'top', 'trouser', 'short'],
        'db_category' : None  # will be set dynamically
    },
    'electronics' : {
        'keywords': ['electronic', 'laptop', 'mobile', 'phone', 'computer', 'gadget', 'camera', 
                     'tv', 'television', 'audio', 'headphone', 'speaker', 'smartphone', 'tablet',
                     'charger', 'cable', 'connector', 'power', 'battery'],
        'db_category': None
    },
    'home_decor': {
        'keywords': ['home', 'decor', 'furniture', 'furnishing', 'curtain', 'light', 'lamp', 
                     'showpiece', 'clock', 'cushion', 'pillow', 'bed', 'sofa', 'table', 'chair',
                     'kitchen', 'bath', 'towel', 'bed sheet', 'diwan'],
        'db_category': None
    },
    'groceries': {
        'keywords': ['grocery', 'food', 'snack', 'beverage', 'drink', 'pet supplies', 'nutrition',
                     'health', 'supplement', 'oil', 'spice', 'tea', 'coffee', 'protein'],
        'db_category': None
    }
}

def get_category_from_tree(category_tree):               # determine which of the 4 target categories the product belongs to. Returns category name or None
    if not category_tree:
        return None
    
    try:
        tree_list = ast.literal_eval(category_tree)
        if not tree_list:
            return None
        
        full_path = tree_list[0].lower()


        # check against each target category's keywords
        for category_name, category_info in TARGET_CATEGORIES.items():
            for keyword in category_info['keywords']:
                if keyword in full_path:
                    return category_name
                
        return None       # if no match found, return None (skips product)
    
    except Exception as e:
        print(f'Error parsing category tree: {e}')
        return None
    

def get_price(row):
    discounted = row.get('discounted_price', '').strip()
    if discounted and discounted.replace('.', '').replace('-', '').isdigit():
        return Decimal(discounted)
    
    retail = row.get('retail_price', '').strip()
    if retail and retail.replace('.', '').replace('-', '').isdigit():
        return Decimal(retail)

    return Decimal('0.00')


def get_description(row):
    parts = []

    if row.get('product_name'):
        parts.append(f'Product Name: {row['product_name']}')

    if row.get('description'):
        desc = str(row.get('description', ''))

        # clean up description
        desc = desc.replace('Price: Rs.', '').strip()
        if desc:
            parts.append(desc)

    if row.get('brand') and row['brand'] != 'No rating available':
        parts.append(f"Brand: {row['brand']}")

    if row.get('product_rating') and row['product_rating'] != 'No rating available':
        parts.append(f"Rating: {row['product_rating']}")

    return '\n\n'.join(parts)


def import_filtered_products(file_path):
    print("=" * 70)
    print("IMPORTING PRODUCTS - 4 TARGET CATEGORIES ONLY")
    print("=" * 70)
    print("Target Categories:")
    print("  • Fashion")
    print("  • Electronics")
    print("  • Home Decor")
    print("  • Groceries")
    print("-" * 70)

    # create or get the 4 categories in database
    for category_name in TARGET_CATEGORIES.keys():
        display_name = category_name.replace('_', '').title()
        category, created = Category.objects.get_or_create(
            name = display_name,
            defaults = {'description' : f'Products in {display_name} category'}
        )
        TARGET_CATEGORIES[category_name]['db_category'] = category
        if created:
            print(f"Created category: {display_name}")
        else:
            print(f"Found category: {display_name}")

    print("=" * 70)


    # import stats
    stats = {
        'fashion' : 0,
        'electronics' : 0,
        'home_decor' : 0,
        'groceries' : 0,
        'skipped' : 0,
        'errors' : 0
    }

    with open(file_path, 'r', encoding = 'utf-8-sig') as file:
        reader = csv.DictReader(file)
        total_rows = 0

        for row_num, row in enumerate(reader, 1):
            try:
                # determine which category product belongs to
                matched_category = get_category_from_tree(row.get('product_category_tree', ''))

                if not matched_category:
                    stats['skipped'] += 1
                    continue

                # get product name
                product_name = row.get('product_name', '').strip()
                if not product_name:
                    stats['skipped'] += 1
                    continue

                # truncate name if too long
                if len(product_name) > 100:
                    product_name = product_name[:97] + '...'

                # get the database category object
                category = TARGET_CATEGORIES[matched_category]['db_category']

                # get price
                price = get_price(row)

                # get description
                description = get_description(row)

                # get image url
                image_url = ''
                if row.get('image_url'):
                    try:
                        image_list = ast.literal_eval(row['image', '[]'])
                        if image_list and len(image_list) > 0:
                            image_url = image_list[0]     # this takes the first image
                    except :
                        pass

                # create or update product
                product, created = Products.objects.update_or_create(
                    name = product_name,
                    defaults={
                            'description': description,
                            'category': category,
                            'price': price,
                            'image_url': image_url
                        }
                )

                if created:
                    stats[matched_category] += 1

                    # progress indicator every 100 products
                    total_imported = sum(stats[c] for c in ['fashion', 'electronics', 'home_decor', 'groceries'])
                    if total_imported % 100 == 0:
                        print(f'Progress: {total_imported} products imported....')

            except Exception as e:
                stats['error'] += 1
                print(f'Error on row {row_num}: {str(e)[:100]}')


    # Print final statistics
    print("\n" + "=" * 70)
    print("IMPORT COMPLETE!")
    print("=" * 70)

    total_imported = sum(stats[c] for c in ['fashion', 'electronics', 'home_decor', 'groceries'])
    print(f"Total products imported: {total_imported}")
    print("-" * 70)
    print(f"Fashion:      {stats['fashion']:5d} products")
    print(f"Electronics:  {stats['electronics']:5d} products")
    print(f"Home Decor:   {stats['home_decor']:5d} products")
    print(f"Groceries:    {stats['groceries']:5d} products")
    print("-" * 70)
    print(f"Skipped:      {stats['skipped']:5d} products (other categories)")
    print(f"Errors:       {stats['errors']:5d}")

    # Show sample from each category
    print("\n" + "=" * 70)
    print("SAMPLE PRODUCTS BY CATEGORY")
    print("=" * 70)

    for cat_name, cat_info in TARGET_CATEGORIES.items():
        category = cat_info['db_category']
        products = Products.objects.filter(category=category)[:3]
        if products:
            display_name = cat_name.replace('_', ' ').title()
            print(f"\n{display_name}:")
            for p in products:
                print(f"  • {p.name[:50]}... - ₹{p.price}")

def quick_check():
    """Quick check of what's in the database"""
    print("\n" + "=" * 70)
    print("DATABASE CHECK")
    print("=" * 70)

    for cat_name in TARGET_CATEGORIES.keys():
        display_name = cat_name.replace('_', ' ').title()
        try:
            category = Category.objects.get(name=display_name)
            count = Products.objects.filter(category=category).count()
            print(f"✓ {display_name}: {count} products")
        except Category.DoesNotExist:
            print(f"✗ {display_name}: Category not found")

if __name__ == '__main__':
    # Run the import
    import_filtered_products('csv_data/data.csv')

    # Final check
    quick_check()

