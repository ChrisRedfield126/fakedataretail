#!/usr/bin/env python3
"""
Frescopa Demo Data Generator
Generates augmented retail data for Adobe Campaign Classic demos

Current Date: January 15, 2026
Business Timeline: Jan 2023 - Jan 2026 (3 years)
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

# Paths
DATA_SAMPLE_DIR = Path("data-sample")
DATA_AUGMENTED_DIR = Path("data-augmented")

# Timeline
CURRENT_DATE = datetime(2026, 1, 15)
BUSINESS_START = datetime(2023, 1, 1)
TOTAL_DAYS = (CURRENT_DATE - BUSINESS_START).days

# Target volumes
TARGET_PRODUCTS = 20
TARGET_RECIPIENTS = 20000
TARGET_PURCHASES_ORDERS = 90000  # ~250K order lines
TARGET_WISHLIST = 4500
TARGET_ABANDONED = 10000
TARGET_SEGMENTS = 20000  # 1:1 with recipients

# Random seed for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

print("="*80)
print("🚀 FRESCOPA DATA GENERATOR")
print("="*80)
print(f"Current Date: {CURRENT_DATE.strftime('%B %d, %Y')}")
print(f"Business Period: {BUSINESS_START.strftime('%Y')} - {CURRENT_DATE.strftime('%Y')}")
print(f"Reading from: {DATA_SAMPLE_DIR}")
print(f"Writing to: {DATA_AUGMENTED_DIR}")
print("="*80)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def random_date(start_date, end_date):
    """Generate random date between start and end"""
    if start_date >= end_date:
        return start_date
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

def add_realistic_time(date_obj):
    """Add realistic hour/minute to date (order time distribution)"""
    # Order time distribution
    rand = random.random()
    if rand < 0.25:  # 6am-12pm
        hour = random.randint(6, 11)
    elif rand < 0.60:  # 12pm-6pm (35%)
        hour = random.randint(12, 17)
    elif rand < 0.90:  # 6pm-10pm (30%)
        hour = random.randint(18, 21)
    else:  # 10pm-6am (10%)
        hour = random.choice(list(range(22, 24)) + list(range(0, 6)))
    
    minute = random.randint(0, 59)
    return date_obj.replace(hour=hour, minute=minute, second=0)

def format_date(date_obj):
    """Format date in CSV format: dd/mm/yyyy HH:MM"""
    if isinstance(date_obj, str):
        return date_obj
    date_with_time = add_realistic_time(date_obj)
    return date_with_time.strftime('%d/%m/%Y %H:%M')

def apply_seasonality(base_date):
    """Apply seasonal patterns (coffee peak in fall/winter)"""
    month = base_date.month
    
    # High season: Sept-Feb
    if month in [9, 10, 11, 12, 1, 2]:
        if random.random() < 0.25:
            base_date = base_date - timedelta(days=random.randint(5, 10))
        # Holiday boost (Dec-Jan)
        if month in [12, 1] and random.random() < 0.15:
            base_date = base_date - timedelta(days=random.randint(3, 7))
    
    # Low season: June-Aug
    elif month in [6, 7, 8]:
        if random.random() < 0.20:
            base_date = base_date + timedelta(days=random.randint(5, 15))
    
    return base_date

# ============================================================================
# STEP 1: LOAD EXISTING DATA
# ============================================================================

print("\n📂 STEP 1: Loading existing data...")

# Load brands
brands_df = pd.read_csv(DATA_SAMPLE_DIR / "brands.csv", sep=';', encoding='latin-1')
brand_names = brands_df['name'].tolist()
print(f"   ✓ Loaded {len(brands_df)} brands: {brand_names}")

# Load products
products_df = pd.read_csv(DATA_SAMPLE_DIR / "products.csv", sep=';', encoding='latin-1')
print(f"   ✓ Loaded {len(products_df)} existing products")

# Load recipients
recipients_df = pd.read_csv(DATA_SAMPLE_DIR / "recipients.csv", sep=';', encoding='latin-1')
print(f"   ✓ Loaded {len(recipients_df)} recipients")

# Cache existing data
existing_product_codes = set(products_df['code'].tolist())
recipient_crmids = recipients_df['crmid'].tolist()

print(f"\n   Total existing:")
print(f"   - Brands: {len(brands_df)}")
print(f"   - Products: {len(products_df)}")
print(f"   - Recipients: {len(recipients_df)}")

# ============================================================================
# STEP 2: GENERATE NEW PRODUCTS
# ============================================================================

print("\n☕ STEP 2: Generating new products...")

# New capsule varieties (category 1)
new_capsules = [
    {'code': 'RomaRoast', 'priceref': 11.50, 'category': 1, 'description': 'Roma Roast (9/10)', 'brand': 'coffeeworks'},
    {'code': 'MilanoMagic', 'priceref': 12.00, 'category': 1, 'description': 'Milano Magic (8/10)', 'brand': 'coffeeworks'},
    {'code': 'CapriCappuccino', 'priceref': 11.00, 'category': 1, 'description': 'Capri Cappuccino (6/10)', 'brand': 'coffeeworks'},
    {'code': 'AmericanoBliss', 'priceref': 10.50, 'category': 1, 'description': 'Americano Bliss (7/10)', 'brand': 'coffeeworks'},
    {'code': 'DecafDelight', 'priceref': 11.00, 'category': 1, 'description': 'Decaf Delight (5/10)', 'brand': 'coffeeworks'},
    {'code': 'HazelnutHeaven', 'priceref': 12.50, 'category': 1, 'description': 'Hazelnut Heaven (7/10)', 'brand': 'javajunction'},
    {'code': 'ChocolateCharm', 'priceref': 13.00, 'category': 1, 'description': 'Chocolate Charm (8/10)', 'brand': 'javajunction'},
    {'code': 'IntenseIndulgence', 'priceref': 14.00, 'category': 1, 'description': 'Intense Indulgence (13/13)', 'brand': 'javajunction'},
]

# New accessories (category 4)
new_accessories = [
    {'code': 'DescaleKit', 'priceref': 19.00, 'category': 4, 'description': 'Descaling Kit', 'brand': 'coffeeworks'},
    {'code': 'CapsuleHolder', 'priceref': 29.00, 'category': 4, 'description': 'Rotating Capsule Holder (40 pods)', 'brand': 'coffeeworks'},
    {'code': 'MilkFrother', 'priceref': 89.00, 'category': 4, 'description': 'Milk Frother', 'brand': 'javajunction'},
    {'code': 'TravelMug', 'priceref': 24.00, 'category': 4, 'description': 'Insulated Travel Mug', 'brand': 'javajunction'},
]

# Combine all products
new_products_df = pd.DataFrame(new_capsules + new_accessories)
new_products_df['imageurl'] = ''

# Combine with existing
products_df = pd.concat([products_df, new_products_df], ignore_index=True)
product_codes = products_df['code'].tolist()

print(f"   ✓ Added {len(new_products_df)} new products")
print(f"   ✓ Total products: {len(products_df)}")
print(f"   - Capsules (cat 1): {len(products_df[products_df['category']==1])}")
print(f"   - Machines (cat 2): {len(products_df[products_df['category']==2])}")
print(f"   - Discount (cat 3): {len(products_df[products_df['category']==3])}")
print(f"   - Accessories (cat 4): {len(products_df[products_df['category']==4])}")

# ============================================================================
# STEP 3: AUGMENT RECIPIENTS
# ============================================================================

print("\n👥 STEP 3: Augmenting recipients with new fields...")

# Assign customer segments
segment_distribution = {
    'active_high': 0.15,
    'active_medium': 0.20,
    'occasional': 0.25,
    'one_time': 0.15,
    'lapsed': 0.15,
    'prospect': 0.10
}

recipients_df['segment'] = np.random.choice(
    list(segment_distribution.keys()),
    size=len(recipients_df),
    p=list(segment_distribution.values())
)

# Assign acquisition dates based on segment
def assign_acquisition_date(row):
    segment = row['segment']
    if segment == 'lapsed':
        return random_date(datetime(2023, 1, 1), datetime(2024, 6, 30))
    elif segment in ['active_high', 'active_medium']:
        return random_date(datetime(2023, 1, 1), datetime(2025, 10, 31))
    elif segment == 'prospect':
        return random_date(datetime(2025, 10, 15), datetime(2026, 1, 15))
    elif segment == 'occasional':
        return random_date(datetime(2023, 3, 1), datetime(2025, 11, 30))
    else:  # one_time
        return random_date(datetime(2023, 1, 1), datetime(2025, 12, 31))

recipients_df['acquisition_date'] = recipients_df.apply(assign_acquisition_date, axis=1)

# Add geographic data
countries = ['US', 'UK', 'FR', 'DE']
recipients_df['country'] = np.random.choice(countries, size=len(recipients_df), p=[0.40, 0.25, 0.20, 0.15])

# Add demographic data
recipients_df['gender'] = np.random.choice(['M', 'F', 'Other'], size=len(recipients_df), p=[0.48, 0.48, 0.04])

# Add language based on country
language_map = {'US': 'en', 'UK': 'en', 'FR': 'fr', 'DE': 'de'}
recipients_df['language'] = recipients_df['country'].map(language_map)

# Machine ownership (important for capsule purchases)
def assign_machine_ownership(segment):
    probabilities = {
        'active_high': 0.95,
        'active_medium': 0.90,
        'occasional': 0.70,
        'one_time': 0.40,
        'lapsed': 0.80,
        'prospect': 0.00
    }
    return random.random() < probabilities.get(segment, 0.50)

recipients_df['owns_machine'] = recipients_df['segment'].apply(assign_machine_ownership)

print(f"   ✓ Added fields: segment, acquisition_date, country, gender, language, owns_machine")
print(f"   ✓ Segment distribution:")
for seg, pct in segment_distribution.items():
    count = len(recipients_df[recipients_df['segment'] == seg])
    print(f"      - {seg}: {count} ({pct*100:.0f}%)")

# ============================================================================
# STEP 4: GENERATE PURCHASES
# ============================================================================

print("\n🛒 STEP 4: Generating purchase history...")
print("   (This may take a few minutes...)")

purchases = []
order_id_counter = 1

# Get capsules and machines for selection
capsules = products_df[products_df['category'] == 1]['code'].tolist()
machines = products_df[products_df['category'] == 2]['code'].tolist()
accessories = products_df[products_df['category'] == 4]['code'].tolist()
discount_code = 'discount'

for idx, customer in recipients_df.iterrows():
    if idx % 2000 == 0:
        print(f"   Processing customer {idx}/{len(recipients_df)}...")
    
    crmid = customer['crmid']
    segment = customer['segment']
    acquisition_date = customer['acquisition_date']
    owns_machine = customer['owns_machine']
    
    # Skip prospects (no purchases)
    if segment == 'prospect':
        continue
    
    # Determine number of orders
    order_counts = {
        'active_high': (8, 12),
        'active_medium': (6, 9),
        'occasional': (2, 4),
        'one_time': (1, 2),
        'lapsed': (3, 6)
    }
    
    min_orders, max_orders = order_counts.get(segment, (2, 4))
    num_orders = random.randint(min_orders, max_orders)
    
    # Reorder intervals (days between orders)
    reorder_intervals = {
        'active_high': (25, 35),
        'active_medium': (40, 60),
        'occasional': (80, 120),
        'one_time': (180, 365),
        'lapsed': (30, 60)
    }
    
    min_interval, max_interval = reorder_intervals[segment]
    
    # Generate orders
    current_date = acquisition_date
    
    for order_num in range(num_orders):
        # Calculate order date
        if order_num == 0:
            days_delay = random.randint(0, 14)
            current_date = acquisition_date + timedelta(days=days_delay)
        else:
            interval = random.randint(min_interval, max_interval)
            current_date = current_date + timedelta(days=interval)
            current_date = apply_seasonality(current_date)
        
        # Lapsed customers: stop buying 6-18 months ago
        if segment == 'lapsed':
            last_purchase_cutoff = CURRENT_DATE - timedelta(days=random.randint(180, 540))
            if current_date > last_purchase_cutoff:
                break
        
        # Don't exceed current date
        if current_date > CURRENT_DATE:
            break
        
        order_ref = f"ORD{str(order_id_counter).zfill(6)}"
        order_id_counter += 1
        line_num = 1
        
        # First order: maybe buy machine
        if order_num == 0 and not owns_machine and random.random() < 0.40:
            machine = random.choice(machines)
            machine_price = float(products_df[products_df['code'] == machine]['priceref'].iloc[0])
            purchases.append({
                'date': format_date(current_date),
                'orderref': order_ref,
                'orderline': line_num,
                'product': machine,
                'price': machine_price,
                'quantity': 1,
                'customer': crmid
            })
            line_num += 1
            owns_machine = True
        
        # Add capsules (if owns machine)
        if owns_machine:
            num_varieties = random.choice([1, 1, 2, 2, 3])
            selected_capsules = random.sample(capsules, min(num_varieties, len(capsules)))
            
            for capsule in selected_capsules:
                capsule_price = float(products_df[products_df['code'] == capsule]['priceref'].iloc[0])
                quantity = random.choice([5, 10, 10, 15, 20])
                
                purchases.append({
                    'date': format_date(current_date),
                    'orderref': order_ref,
                    'orderline': line_num,
                    'product': capsule,
                    'price': capsule_price,
                    'quantity': quantity,
                    'customer': crmid
                })
                line_num += 1
        
        # Maybe add accessories (5% chance)
        if random.random() < 0.05 and len(accessories) > 0:
            accessory = random.choice(accessories)
            accessory_price = float(products_df[products_df['code'] == accessory]['priceref'].iloc[0])
            purchases.append({
                'date': format_date(current_date),
                'orderref': order_ref,
                'orderline': line_num,
                'product': accessory,
                'price': accessory_price,
                'quantity': 1,
                'customer': crmid
            })
            line_num += 1
        
        # Maybe add discount (20% of orders)
        if random.random() < 0.20 and line_num > 1:
            order_total = sum(p['price'] * p['quantity'] for p in purchases if p['orderref'] == order_ref)
            discount_amount = round(order_total * random.uniform(0.05, 0.15), 2)
            purchases.append({
                'date': format_date(current_date),
                'orderref': order_ref,
                'orderline': line_num,
                'product': discount_code,
                'price': -discount_amount,
                'quantity': 1,
                'customer': crmid
            })

purchases_df = pd.DataFrame(purchases)

print(f"   ✓ Generated {len(purchases_df)} purchase lines")
print(f"   ✓ Total orders: {purchases_df['orderref'].nunique()}")
print(f"   ✓ Customers who purchased: {purchases_df['customer'].nunique()}")

# ============================================================================
# STEP 5: GENERATE WISHLIST
# ============================================================================

print("\n💝 STEP 5: Generating wishlist...")

wishlist = []
wishlist_id = 1

# 15% of customers have wishlist
wishlist_candidates = recipients_df.sample(frac=0.15)

for idx, customer in wishlist_candidates.iterrows():
    crmid = customer['crmid']
    
    # Don't wishlist what they already bought
    customer_purchases = purchases_df[purchases_df['customer'] == crmid]
    bought_products = set(customer_purchases['product'].unique())
    
    # Wishlist = machines/accessories they don't own
    available_machines = [p for p in machines if p not in bought_products]
    available_accessories = [p for p in accessories if p not in bought_products]
    available = available_machines + available_accessories
    
    if len(available) > 0:
        num_items = random.choice([1, 1, 2])
        selected = random.sample(available, min(num_items, len(available)))
        
        for product in selected:
            creation_date = random_date(
                max(customer['acquisition_date'], CURRENT_DATE - timedelta(days=180)),
                CURRENT_DATE
            )
            last_update = creation_date + timedelta(days=random.randint(0, 30))
            last_update = min(last_update, CURRENT_DATE)
            
            wishlist.append({
                'wishListId': f'WISH{str(wishlist_id).zfill(6)}',
                'wishListName': random.randint(0, 5),
                'lastUpdate': format_date(last_update),
                'creationDate': format_date(creation_date),
                'product': product,
                'customer': crmid
            })
            wishlist_id += 1

wishlist_df = pd.DataFrame(wishlist)

print(f"   ✓ Generated {len(wishlist_df)} wishlist items")
print(f"   ✓ Customers with wishlist: {wishlist_df['customer'].nunique()}")

# ============================================================================
# STEP 6: GENERATE ABANDONED CARTS
# ============================================================================

print("\n🛒 STEP 6: Generating abandoned carts...")

abandoned = []
cart_start_date = CURRENT_DATE - timedelta(days=90)

# Active customers abandon carts
active_customers = recipients_df[
    recipients_df['segment'].isin(['active_high', 'active_medium', 'occasional'])
]

# Target 10,000 cart items
num_carts_needed = TARGET_ABANDONED
carts_per_customer = max(1, num_carts_needed // len(active_customers))

for idx, customer in active_customers.iterrows():
    crmid = customer['crmid']
    
    num_carts = random.randint(1, min(carts_per_customer, 3))
    
    for _ in range(num_carts):
        cart_id = f'CART{random.randint(100000, 999999)}'
        
        # Exponential distribution: more recent = more likely
        days_ago = int(np.random.exponential(scale=30))
        days_ago = min(days_ago, 90)
        cart_date = CURRENT_DATE - timedelta(days=days_ago)
        
        # 1-3 products per cart
        num_products = random.choice([1, 1, 2, 3])
        cart_products = random.sample(capsules + machines, num_products)
        
        for product in cart_products:
            quantity = random.choice([1, 5, 10, 15, 20])
            
            abandoned.append({
                'date': format_date(cart_date),
                'cartid': cart_id,
                'product': product,
                'quantity': quantity,
                'tosend': 0,
                'customer': crmid
            })
        
        if len(abandoned) >= TARGET_ABANDONED:
            break
    
    if len(abandoned) >= TARGET_ABANDONED:
        break

abandoned_df = pd.DataFrame(abandoned[:TARGET_ABANDONED])

print(f"   ✓ Generated {len(abandoned_df)} abandoned cart items")
print(f"   ✓ Customers with abandoned carts: {abandoned_df['customer'].nunique()}")

# ============================================================================
# STEP 7: GENERATE SEGMENTS
# ============================================================================

print("\n📊 STEP 7: Calculating customer segments...")

segments = []

for idx, customer in recipients_df.iterrows():
    crmid = customer['crmid']
    
    # Get purchase history
    customer_purchases = purchases_df[purchases_df['customer'] == crmid]
    
    if len(customer_purchases) > 0:
        # Calculate metrics
        order_dates = pd.to_datetime(customer_purchases['date'], format='%d/%m/%Y %H:%M')
        last_purchase = order_dates.max()
        days_since = (CURRENT_DATE - last_purchase).days
        
        purchase_count = customer_purchases['orderref'].nunique()
        total_spent = customer_purchases.apply(lambda x: x['price'] * x['quantity'], axis=1).sum()
        
        # Churn propensity
        if days_since < 60:
            churnprop = 0
        elif days_since < 120:
            churnprop = 1
        elif days_since < 180:
            churnprop = 2
        else:
            churnprop = 3
        
        # VIP tier
        if total_spent < 100:
            vip = 0
        elif total_spent < 500:
            vip = 1
        elif total_spent < 1500:
            vip = 2
        elif total_spent < 3000:
            vip = 3
        else:
            vip = 4
        
        # NPS (correlated with purchase count)
        if purchase_count >= 10:
            nps = random.choice([8, 9, 9, 9])
        elif purchase_count >= 5:
            nps = random.choice([7, 8, 8, 9])
        else:
            nps = random.choice([6, 7, 8])
        
        # React score (engagement)
        reactscore = min(10, purchase_count)
    else:
        # Prospect
        churnprop = 0
        vip = -1
        nps = random.choice([6, 7, 8])
        reactscore = 0
    
    segments.append({
        'customer': crmid,
        'churnprop': churnprop,
        'churndate': '10/01/2026 09:00:00',
        'nps': nps,
        'npsdate': '15/12/2025 10:00:00',
        'reactscore': reactscore,
        'reactdate': '10/01/2026 10:00:00',
        'vip': vip,
        'vipdate': '30/11/2025 12:00:00'
    })

segments_df = pd.DataFrame(segments)

print(f"   ✓ Generated {len(segments_df)} segment records (1:1 with recipients)")

# ============================================================================
# STEP 8: VALIDATE FK INTEGRITY
# ============================================================================

print("\n🔍 STEP 8: Validating FK integrity...")

errors = []

# Products → Brands
product_brands = set(products_df['brand'])
brand_names_set = set(brand_names)
if not product_brands.issubset(brand_names_set):
    errors.append(f"Invalid brands in products: {product_brands - brand_names_set}")
else:
    print(f"   ✓ products.brand → brands.name: OK")

# Recipients → Brands
recipient_brands = set(recipients_df['brand'])
if not recipient_brands.issubset(brand_names_set):
    errors.append(f"Invalid brands in recipients: {recipient_brands - brand_names_set}")
else:
    print(f"   ✓ recipients.brand → brands.name: OK")

# Purchases → Recipients
purchase_customers = set(purchases_df['customer'].unique())
recipient_crmids_set = set(recipient_crmids)
if not purchase_customers.issubset(recipient_crmids_set):
    errors.append(f"Invalid customers in purchases: {len(purchase_customers - recipient_crmids_set)}")
else:
    print(f"   ✓ purchases.customer → recipients.crmid: OK")

# Purchases → Products
purchase_products = set(purchases_df['product'].unique())
product_codes_set = set(product_codes)
if not purchase_products.issubset(product_codes_set):
    errors.append(f"Invalid products in purchases: {purchase_products - product_codes_set}")
else:
    print(f"   ✓ purchases.product → products.code: OK")

# Wishlist → Recipients
wishlist_customers = set(wishlist_df['customer'].unique())
if not wishlist_customers.issubset(recipient_crmids_set):
    errors.append(f"Invalid customers in wishlist: {len(wishlist_customers - recipient_crmids_set)}")
else:
    print(f"   ✓ wishlist.customer → recipients.crmid: OK")

# Wishlist → Products
wishlist_products = set(wishlist_df['product'].unique())
if not wishlist_products.issubset(product_codes_set):
    errors.append(f"Invalid products in wishlist: {wishlist_products - product_codes_set}")
else:
    print(f"   ✓ wishlist.product → products.code: OK")

# Abandoned → Recipients
abandoned_customers = set(abandoned_df['customer'].unique())
if not abandoned_customers.issubset(recipient_crmids_set):
    errors.append(f"Invalid customers in abandoned: {len(abandoned_customers - recipient_crmids_set)}")
else:
    print(f"   ✓ abandoned.customer → recipients.crmid: OK")

# Abandoned → Products
abandoned_products = set(abandoned_df['product'].unique())
if not abandoned_products.issubset(product_codes_set):
    errors.append(f"Invalid products in abandoned: {abandoned_products - product_codes_set}")
else:
    print(f"   ✓ abandoned.product → products.code: OK")

# Segments → Recipients (1:1)
segments_customers = set(segments_df['customer'])
if segments_customers != recipient_crmids_set:
    errors.append(f"Segments not 1:1 with recipients")
else:
    print(f"   ✓ segments.customer ↔ recipients.crmid (1:1): OK")

if errors:
    print("\n❌ VALIDATION FAILED:")
    for error in errors:
        print(f"   • {error}")
    raise ValueError("FK integrity validation failed!")
else:
    print("\n✅ ALL FOREIGN KEY CONSTRAINTS VALID")

# ============================================================================
# STEP 9: WRITE OUTPUT FILES
# ============================================================================

print("\n💾 STEP 9: Writing output files...")

# Create output directory
DATA_AUGMENTED_DIR.mkdir(exist_ok=True)

# Write all CSV files (using latin-1 encoding for compatibility)
brands_df.to_csv(DATA_AUGMENTED_DIR / "brands.csv", sep=';', index=False, encoding='latin-1')
print(f"   ✓ brands.csv ({len(brands_df)} rows)")

products_df.to_csv(DATA_AUGMENTED_DIR / "products.csv", sep=';', index=False, encoding='latin-1')
print(f"   ✓ products.csv ({len(products_df)} rows)")

recipients_df.to_csv(DATA_AUGMENTED_DIR / "recipients.csv", sep=';', index=False, encoding='latin-1')
print(f"   ✓ recipients.csv ({len(recipients_df)} rows)")

purchases_df.to_csv(DATA_AUGMENTED_DIR / "purchases.csv", sep=';', index=False, encoding='latin-1')
print(f"   ✓ purchases.csv ({len(purchases_df)} rows)")

wishlist_df.to_csv(DATA_AUGMENTED_DIR / "wishlist.csv", sep=';', index=False, encoding='latin-1')
print(f"   ✓ wishlist.csv ({len(wishlist_df)} rows)")

abandoned_df.to_csv(DATA_AUGMENTED_DIR / "abandoned.csv", sep=';', index=False, encoding='latin-1')
print(f"   ✓ abandoned.csv ({len(abandoned_df)} rows)")

segments_df.to_csv(DATA_AUGMENTED_DIR / "segments.csv", sep=';', index=False, encoding='latin-1')
print(f"   ✓ segments.csv ({len(segments_df)} rows)")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("✅ DATA GENERATION COMPLETE")
print("="*80)
print(f"\n📊 SUMMARY:")
print(f"   Brands:          {len(brands_df):>8,}")
print(f"   Products:        {len(products_df):>8,}")
print(f"   Recipients:      {len(recipients_df):>8,}")
print(f"   Purchases:       {len(purchases_df):>8,} lines ({purchases_df['orderref'].nunique():,} orders)")
print(f"   Wishlist:        {len(wishlist_df):>8,}")
print(f"   Abandoned:       {len(abandoned_df):>8,}")
print(f"   Segments:        {len(segments_df):>8,}")
print(f"\n   Total rows:      {len(brands_df) + len(products_df) + len(recipients_df) + len(purchases_df) + len(wishlist_df) + len(abandoned_df) + len(segments_df):>8,}")

print(f"\n📁 Files written to: {DATA_AUGMENTED_DIR}/")
print(f"\n🎯 Ready for Adobe Campaign Classic import!")
print("="*80)
