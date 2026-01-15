#!/usr/bin/env python3
"""
Frescopa Demo Data Generator
Generates augmented retail data for Adobe Campaign Classic demos
MAINTAINS EXACT SAME STRUCTURE AS ORIGINAL - Only adds volume!

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

# Target volumes
TARGET_PRODUCTS = 20
TARGET_PURCHASES_ORDERS = 90000
TARGET_WISHLIST = 4500
TARGET_ABANDONED = 10000

# Random seed for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

print("="*80)
print("🚀 FRESCOPA DATA GENERATOR")
print("="*80)
print(f"Current Date: {CURRENT_DATE.strftime('%B %d, %Y')}")
print(f"Business Period: {BUSINESS_START.strftime('%Y')} - {CURRENT_DATE.strftime('%Y')}")
print(f"⚠️  MAINTAINS EXACT SAME STRUCTURE - Only adds volume!")
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
    """Add realistic hour/minute to date"""
    rand = random.random()
    if rand < 0.25:
        hour = random.randint(6, 11)
    elif rand < 0.60:
        hour = random.randint(12, 17)
    elif rand < 0.90:
        hour = random.randint(18, 21)
    else:
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
    """Apply seasonal patterns"""
    month = base_date.month
    if month in [9, 10, 11, 12, 1, 2]:
        if random.random() < 0.25:
            base_date = base_date - timedelta(days=random.randint(5, 10))
        if month in [12, 1] and random.random() < 0.15:
            base_date = base_date - timedelta(days=random.randint(3, 7))
    elif month in [6, 7, 8]:
        if random.random() < 0.20:
            base_date = base_date + timedelta(days=random.randint(5, 15))
    return base_date

# ============================================================================
# STEP 1: LOAD EXISTING DATA
# ============================================================================

print("\n📂 STEP 1: Loading existing data...")

brands_df = pd.read_csv(DATA_SAMPLE_DIR / "brands.csv", sep=';', encoding='latin-1')
brand_names = brands_df['name'].tolist()
print(f"   ✓ brands.csv: {len(brands_df)} rows - {list(brands_df.columns)}")

products_df = pd.read_csv(DATA_SAMPLE_DIR / "products.csv", sep=';', encoding='latin-1')
print(f"   ✓ products.csv: {len(products_df)} rows - {list(products_df.columns)}")

recipients_df = pd.read_csv(DATA_SAMPLE_DIR / "recipients.csv", sep=';', encoding='latin-1')
print(f"   ✓ recipients.csv: {len(recipients_df)} rows - {list(recipients_df.columns)}")

# Cache for FK validation
recipient_crmids = recipients_df['crmid'].tolist()

# ============================================================================
# STEP 2: GENERATE NEW PRODUCTS (Same structure!)
# ============================================================================

print("\n☕ STEP 2: Generating new products (same structure)...")

# EXACT COLUMNS: code, priceref, category, description, brand, imageurl
new_products = [
    {'code': 'RomaRoast', 'priceref': 11.50, 'category': 1, 'description': 'Roma Roast (9/10)', 'brand': 'coffeeworks', 'imageurl': ''},
    {'code': 'MilanoMagic', 'priceref': 12.00, 'category': 1, 'description': 'Milano Magic (8/10)', 'brand': 'coffeeworks', 'imageurl': ''},
    {'code': 'CapriCappuccino', 'priceref': 11.00, 'category': 1, 'description': 'Capri Cappuccino (6/10)', 'brand': 'coffeeworks', 'imageurl': ''},
    {'code': 'AmericanoBliss', 'priceref': 10.50, 'category': 1, 'description': 'Americano Bliss (7/10)', 'brand': 'coffeeworks', 'imageurl': ''},
    {'code': 'DecafDelight', 'priceref': 11.00, 'category': 1, 'description': 'Decaf Delight (5/10)', 'brand': 'coffeeworks', 'imageurl': ''},
    {'code': 'HazelnutHeaven', 'priceref': 12.50, 'category': 1, 'description': 'Hazelnut Heaven (7/10)', 'brand': 'javajunction', 'imageurl': ''},
    {'code': 'ChocolateCharm', 'priceref': 13.00, 'category': 1, 'description': 'Chocolate Charm (8/10)', 'brand': 'javajunction', 'imageurl': ''},
    {'code': 'IntenseIndulgence', 'priceref': 14.00, 'category': 1, 'description': 'Intense Indulgence (13/13)', 'brand': 'javajunction', 'imageurl': ''},
    {'code': 'DescaleKit', 'priceref': 19.00, 'category': 4, 'description': 'Descaling Kit', 'brand': 'coffeeworks', 'imageurl': ''},
    {'code': 'CapsuleHolder', 'priceref': 29.00, 'category': 4, 'description': 'Rotating Capsule Holder', 'brand': 'coffeeworks', 'imageurl': ''},
    {'code': 'MilkFrother', 'priceref': 89.00, 'category': 4, 'description': 'Milk Frother', 'brand': 'javajunction', 'imageurl': ''},
    {'code': 'TravelMug', 'priceref': 24.00, 'category': 4, 'description': 'Insulated Travel Mug', 'brand': 'javajunction', 'imageurl': ''},
]

new_products_df = pd.DataFrame(new_products)
products_df = pd.concat([products_df, new_products_df], ignore_index=True)
product_codes = products_df['code'].tolist()

print(f"   ✓ Added {len(new_products)} new products")
print(f"   ✓ Total products: {len(products_df)}")

# ============================================================================
# STEP 3: INTERNAL CUSTOMER SEGMENTATION (for logic, not exported!)
# ============================================================================

print("\n👥 STEP 3: Assigning internal segments (for purchase logic)...")

# Internal fields - NOT exported to recipients.csv!
segment_distribution = {
    'active_high': 0.15,
    'active_medium': 0.20,
    'occasional': 0.25,
    'one_time': 0.15,
    'lapsed': 0.15,
    'prospect': 0.10
}

recipients_df['_internal_segment'] = np.random.choice(
    list(segment_distribution.keys()),
    size=len(recipients_df),
    p=list(segment_distribution.values())
)

# Assign acquisition dates (internal)
def assign_acquisition_date(segment):
    if segment == 'lapsed':
        return random_date(datetime(2023, 1, 1), datetime(2024, 6, 30))
    elif segment in ['active_high', 'active_medium']:
        return random_date(datetime(2023, 1, 1), datetime(2025, 10, 31))
    elif segment == 'prospect':
        return random_date(datetime(2025, 10, 15), datetime(2026, 1, 15))
    elif segment == 'occasional':
        return random_date(datetime(2023, 3, 1), datetime(2025, 11, 30))
    else:
        return random_date(datetime(2023, 1, 1), datetime(2025, 12, 31))

recipients_df['_internal_acquisition'] = recipients_df['_internal_segment'].apply(assign_acquisition_date)

# Machine ownership (internal)
def assign_machine_ownership(segment):
    prob = {'active_high': 0.95, 'active_medium': 0.90, 'occasional': 0.70,
            'one_time': 0.40, 'lapsed': 0.80, 'prospect': 0.00}
    return random.random() < prob.get(segment, 0.50)

recipients_df['_internal_owns_machine'] = recipients_df['_internal_segment'].apply(assign_machine_ownership)

print(f"   ✓ Internal segments assigned (not exported to CSV)")

# ============================================================================
# STEP 4: GENERATE PURCHASES (Same structure!)
# ============================================================================

print("\n🛒 STEP 4: Generating purchases (same structure)...")
print("   (This may take a few minutes...)")

# EXACT COLUMNS: date, orderref, orderline, product, price, quantity, customer
purchases = []
order_id_counter = 1

capsules = products_df[products_df['category'] == 1]['code'].tolist()
machines = products_df[products_df['category'] == 2]['code'].tolist()
accessories = products_df[products_df['category'] == 4]['code'].tolist()

for idx, customer in recipients_df.iterrows():
    if idx % 2000 == 0:
        print(f"   Processing customer {idx}/{len(recipients_df)}...")
    
    crmid = customer['crmid']
    segment = customer['_internal_segment']
    acquisition_date = customer['_internal_acquisition']
    owns_machine = customer['_internal_owns_machine']
    
    if segment == 'prospect':
        continue
    
    order_counts = {
        'active_high': (8, 12),
        'active_medium': (6, 9),
        'occasional': (2, 4),
        'one_time': (1, 2),
        'lapsed': (3, 6)
    }
    
    min_orders, max_orders = order_counts.get(segment, (2, 4))
    num_orders = random.randint(min_orders, max_orders)
    
    reorder_intervals = {
        'active_high': (25, 35),
        'active_medium': (40, 60),
        'occasional': (80, 120),
        'one_time': (180, 365),
        'lapsed': (30, 60)
    }
    
    min_interval, max_interval = reorder_intervals[segment]
    current_date = acquisition_date
    
    for order_num in range(num_orders):
        if order_num == 0:
            current_date = acquisition_date + timedelta(days=random.randint(0, 14))
        else:
            interval = random.randint(min_interval, max_interval)
            current_date = current_date + timedelta(days=interval)
            current_date = apply_seasonality(current_date)
        
        if segment == 'lapsed':
            last_purchase_cutoff = CURRENT_DATE - timedelta(days=random.randint(180, 540))
            if current_date > last_purchase_cutoff:
                break
        
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
        
        # Add capsules
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
        
        # Maybe add accessories
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
        
        # Maybe add discount
        if random.random() < 0.20 and line_num > 1:
            order_total = sum(p['price'] * p['quantity'] for p in purchases if p['orderref'] == order_ref)
            discount_amount = round(order_total * random.uniform(0.05, 0.15), 2)
            purchases.append({
                'date': format_date(current_date),
                'orderref': order_ref,
                'orderline': line_num,
                'product': 'discount',
                'price': -discount_amount,
                'quantity': 1,
                'customer': crmid
            })

purchases_df = pd.DataFrame(purchases)
print(f"   ✓ Generated {len(purchases_df)} purchase lines")
print(f"   ✓ Structure: {list(purchases_df.columns)}")

# ============================================================================
# STEP 5: GENERATE WISHLIST (Same structure!)
# ============================================================================

print("\n💝 STEP 5: Generating wishlist (allows overlap with purchases for conversion tracking)...")

# EXACT COLUMNS: wishListId, wishListName, lastUpdate, creationDate, product, customer
wishlist = []
wishlist_id = 1

wishlist_candidates = recipients_df.sample(frac=0.15)

for idx, customer in wishlist_candidates.iterrows():
    crmid = customer['crmid']
    customer_purchases = purchases_df[purchases_df['customer'] == crmid]
    
    # Get all machines and accessories (don't filter out purchased items!)
    # This allows tracking wishlist → purchase conversion
    available = machines + accessories
    
    if len(available) > 0:
        num_items = random.choice([1, 1, 2])
        selected = random.sample(available, min(num_items, len(available)))
        
        for product in selected:
            # Wishlist creation date logic:
            # - If customer bought this product, wishlist was added BEFORE first purchase (aspirational)
            # - If not bought yet, wishlist is recent (ongoing aspiration)
            
            product_purchases = customer_purchases[customer_purchases['product'] == product]
            
            if len(product_purchases) > 0:
                # Product was purchased! Wishlist must be BEFORE first purchase
                first_purchase_date = pd.to_datetime(product_purchases['date'], format='%d/%m/%Y %H:%M').min()
                first_purchase_date = first_purchase_date.to_pydatetime()
                
                # Wishlist created 7-90 days before first purchase
                days_before = random.randint(7, 90)
                creation_date = first_purchase_date - timedelta(days=days_before)
                
                # Make sure it's after acquisition
                creation_date = max(creation_date, customer['_internal_acquisition'])
            else:
                # Product not purchased yet - recent wishlist (last 6 months)
                creation_date = random_date(
                    max(customer['_internal_acquisition'], CURRENT_DATE - timedelta(days=180)),
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
print(f"   ✓ Structure: {list(wishlist_df.columns)}")

# ============================================================================
# STEP 6: GENERATE ABANDONED CARTS (Same structure!)
# ============================================================================

print("\n🛒 STEP 6: Generating abandoned carts (with cartnum)...")

# COLUMNS: date, cartid, cartnum, product, quantity, tosend, customer
abandoned = []
cart_id_counter = 1  # Sequential cart ID to avoid duplicates

active_customers = recipients_df[
    recipients_df['_internal_segment'].isin(['active_high', 'active_medium', 'occasional'])
]

num_carts_needed = TARGET_ABANDONED
carts_per_customer = max(1, num_carts_needed // len(active_customers))

for idx, customer in active_customers.iterrows():
    crmid = customer['crmid']
    num_carts = random.randint(1, min(carts_per_customer, 3))
    
    for _ in range(num_carts):
        cart_id = f'CART{str(cart_id_counter).zfill(6)}'  # Sequential, unique cart ID
        cart_id_counter += 1
        
        days_ago = int(np.random.exponential(scale=30))
        days_ago = min(days_ago, 90)
        cart_date = CURRENT_DATE - timedelta(days=days_ago)
        
        num_products = random.choice([1, 1, 2, 3])
        cart_products = random.sample(capsules + machines, num_products)
        
        # Add cartnum (line number within cart)
        cart_line = 1
        for product in cart_products:
            abandoned.append({
                'date': format_date(cart_date),
                'cartid': cart_id,
                'cartnum': cart_line,
                'product': product,
                'quantity': random.choice([1, 5, 10, 15, 20]),
                'tosend': 0,
                'customer': crmid
            })
            cart_line += 1
        
        if len(abandoned) >= TARGET_ABANDONED:
            break
    
    if len(abandoned) >= TARGET_ABANDONED:
        break

abandoned_df = pd.DataFrame(abandoned[:TARGET_ABANDONED])
print(f"   ✓ Generated {len(abandoned_df)} abandoned cart items")
print(f"   ✓ Structure: {list(abandoned_df.columns)}")

# ============================================================================
# STEP 7: GENERATE SEGMENTS (Same structure!)
# ============================================================================

print("\n📊 STEP 7: Calculating segments (same structure)...")

# EXACT COLUMNS: customer, churnprop, churndate, nps, npsdate, reactscore, reactdate, vip, vipdate
segments = []

for idx, customer in recipients_df.iterrows():
    crmid = customer['crmid']
    customer_orders = purchases_df[purchases_df['customer'] == crmid]
    
    if len(customer_orders) > 0:
        order_dates = pd.to_datetime(customer_orders['date'], format='%d/%m/%Y %H:%M')
        last_purchase = order_dates.max()
        days_since = (CURRENT_DATE - last_purchase).days
        purchase_count = customer_orders['orderref'].nunique()
        total_spent = customer_orders.apply(lambda x: x['price'] * x['quantity'], axis=1).sum()
        
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
        
        # NPS
        if purchase_count >= 10:
            nps = random.choice([8, 9, 9, 9])
        elif purchase_count >= 5:
            nps = random.choice([7, 8, 8, 9])
        else:
            nps = random.choice([6, 7, 8])
        
        reactscore = min(10, purchase_count)
    else:
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
print(f"   ✓ Generated {len(segments_df)} segment records")
print(f"   ✓ Structure: {list(segments_df.columns)}")

# ============================================================================
# STEP 8: VALIDATE FK INTEGRITY
# ============================================================================

print("\n🔍 STEP 8: Validating FK integrity...")

errors = []

# Validate all FKs
product_brands = set(products_df['brand'])
brand_names_set = set(brand_names)
if not product_brands.issubset(brand_names_set):
    errors.append(f"Invalid brands in products")
else:
    print(f"   ✓ products.brand → brands.name: OK")

recipient_brands = set(recipients_df['brand'])
if not recipient_brands.issubset(brand_names_set):
    errors.append(f"Invalid brands in recipients")
else:
    print(f"   ✓ recipients.brand → brands.name: OK")

purchase_customers = set(purchases_df['customer'].unique())
recipient_crmids_set = set(recipient_crmids)
if not purchase_customers.issubset(recipient_crmids_set):
    errors.append(f"Invalid customers in purchases")
else:
    print(f"   ✓ purchases.customer → recipients.crmid: OK")

purchase_products = set(purchases_df['product'].unique())
product_codes_set = set(product_codes)
if not purchase_products.issubset(product_codes_set):
    errors.append(f"Invalid products in purchases")
else:
    print(f"   ✓ purchases.product → products.code: OK")

wishlist_customers = set(wishlist_df['customer'].unique())
if not wishlist_customers.issubset(recipient_crmids_set):
    errors.append(f"Invalid customers in wishlist")
else:
    print(f"   ✓ wishlist.customer → recipients.crmid: OK")

wishlist_products = set(wishlist_df['product'].unique())
if not wishlist_products.issubset(product_codes_set):
    errors.append(f"Invalid products in wishlist")
else:
    print(f"   ✓ wishlist.product → products.code: OK")

abandoned_customers = set(abandoned_df['customer'].unique())
if not abandoned_customers.issubset(recipient_crmids_set):
    errors.append(f"Invalid customers in abandoned")
else:
    print(f"   ✓ abandoned.customer → recipients.crmid: OK")

abandoned_products = set(abandoned_df['product'].unique())
if not abandoned_products.issubset(product_codes_set):
    errors.append(f"Invalid products in abandoned")
else:
    print(f"   ✓ abandoned.product → products.code: OK")

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
# STEP 9: WRITE OUTPUT FILES (EXACT SAME STRUCTURE!)
# ============================================================================

print("\n💾 STEP 9: Writing output files (same structure as originals)...")

DATA_AUGMENTED_DIR.mkdir(exist_ok=True)

# Write brands (unchanged)
brands_df.to_csv(DATA_AUGMENTED_DIR / "brands.csv", sep=';', index=False, encoding='latin-1')
print(f"   ✓ brands.csv ({len(brands_df)} rows) - {list(brands_df.columns)}")

# Write products (new products added)
products_df.to_csv(DATA_AUGMENTED_DIR / "products.csv", sep=';', index=False, encoding='latin-1')
print(f"   ✓ products.csv ({len(products_df)} rows) - {list(products_df.columns)}")

# Write recipients - ONLY ORIGINAL COLUMNS!
recipients_export = recipients_df[['crmid', 'firstname', 'lastname', 'email', 'brand', 'birthdate', 'folder']]
recipients_export.to_csv(DATA_AUGMENTED_DIR / "recipients.csv", sep=';', index=False, encoding='latin-1')
print(f"   ✓ recipients.csv ({len(recipients_export)} rows) - {list(recipients_export.columns)}")

# Write purchases
purchases_df.to_csv(DATA_AUGMENTED_DIR / "purchases.csv", sep=';', index=False, encoding='latin-1')
print(f"   ✓ purchases.csv ({len(purchases_df)} rows) - {list(purchases_df.columns)}")

# Write wishlist
wishlist_df.to_csv(DATA_AUGMENTED_DIR / "wishlist.csv", sep=';', index=False, encoding='latin-1')
print(f"   ✓ wishlist.csv ({len(wishlist_df)} rows) - {list(wishlist_df.columns)}")

# Write abandoned
abandoned_df.to_csv(DATA_AUGMENTED_DIR / "abandoned.csv", sep=';', index=False, encoding='latin-1')
print(f"   ✓ abandoned.csv ({len(abandoned_df)} rows) - {list(abandoned_df.columns)}")

# Write segments
segments_df.to_csv(DATA_AUGMENTED_DIR / "segments.csv", sep=';', index=False, encoding='latin-1')
print(f"   ✓ segments.csv ({len(segments_df)} rows) - {list(segments_df.columns)}")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("✅ DATA GENERATION COMPLETE")
print("="*80)
print(f"\n📊 SUMMARY:")
print(f"   Brands:          {len(brands_df):>8,}")
print(f"   Products:        {len(products_df):>8,}")
print(f"   Recipients:      {len(recipients_export):>8,}")
print(f"   Purchases:       {len(purchases_df):>8,} lines ({purchases_df['orderref'].nunique():,} orders)")
print(f"   Wishlist:        {len(wishlist_df):>8,}")
print(f"   Abandoned:       {len(abandoned_df):>8,}")
print(f"   Segments:        {len(segments_df):>8,}")

print(f"\n✅ ALL FILES MAINTAIN EXACT SAME STRUCTURE AS ORIGINALS")
print(f"📁 Files written to: {DATA_AUGMENTED_DIR}/")
print(f"🎯 Ready for Adobe Campaign Classic import!")
print("="*80)
