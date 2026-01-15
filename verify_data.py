#!/usr/bin/env python3
"""
Quick verification and sample queries for the augmented data
"""

import pandas as pd
from pathlib import Path

DATA_DIR = Path("data-augmented")

print("="*80)
print("📊 FRESCOPA DATA VERIFICATION & SAMPLE QUERIES")
print("="*80)

# Load data
recipients_df = pd.read_csv(DATA_DIR / "recipients.csv", sep=';', encoding='latin-1')
purchases_df = pd.read_csv(DATA_DIR / "purchases.csv", sep=';', encoding='latin-1')
segments_df = pd.read_csv(DATA_DIR / "segments.csv", sep=';', encoding='latin-1')
abandoned_df = pd.read_csv(DATA_DIR / "abandoned.csv", sep=';', encoding='latin-1')
wishlist_df = pd.read_csv(DATA_DIR / "wishlist.csv", sep=';', encoding='latin-1')

# Convert dates
purchases_df['date'] = pd.to_datetime(purchases_df['date'], format='%d/%m/%Y %H:%M')
abandoned_df['date'] = pd.to_datetime(abandoned_df['date'], format='%d/%m/%Y %H:%M')

print("\n1️⃣  RECIPIENT DATA")
print("-" * 80)
print(f"   Total recipients:    {len(recipients_df):>8,}")
print(f"   Columns: {', '.join(recipients_df.columns)}")
print(f"   Note: Demographics (segment, country, etc.) tracked in segments table")

print("\n2️⃣  PURCHASE ANALYSIS")
print("-" * 80)
print(f"   Total orders:        {purchases_df['orderref'].nunique():>8,}")
print(f"   Total order lines:   {len(purchases_df):>8,}")
print(f"   Unique customers:    {purchases_df['customer'].nunique():>8,}")
print(f"   Avg lines per order: {len(purchases_df) / purchases_df['orderref'].nunique():>8.2f}")

# Top products
print("\n   Top 5 Products by Order Lines:")
top_products = purchases_df['product'].value_counts().head(5)
for product, count in top_products.items():
    print(f"      {product:20} {count:>6,} lines")

print("\n3️⃣  VIP TIER DISTRIBUTION")
print("-" * 80)
vip_counts = segments_df['vip'].value_counts().sort_index()
vip_labels = {-1: 'Invalid/Prospect', 0: 'Standard', 1: 'Bronze', 2: 'Silver', 3: 'Gold', 4: 'Platinum'}
for tier, count in vip_counts.items():
    pct = count / len(segments_df) * 100
    label = vip_labels.get(tier, f'Tier {tier}')
    print(f"   {label:15} {count:>6,} ({pct:>5.1f}%)")

print("\n4️⃣  CHURN RISK DISTRIBUTION")
print("-" * 80)
churn_counts = segments_df['churnprop'].value_counts().sort_index()
churn_labels = {0: 'Low', 1: 'Medium', 2: 'High', 3: 'Very High'}
for risk, count in churn_counts.items():
    pct = count / len(segments_df) * 100
    label = churn_labels.get(risk, f'Risk {risk}')
    print(f"   {label:15} {count:>6,} ({pct:>5.1f}%)")

print("\n5️⃣  SAMPLE DEMO QUERIES")
print("-" * 80)

# Query 1: Get segment info from segments table
active_high_segments = segments_df[segments_df['vip'] >= 3]  # Gold/Platinum as proxy for "active high value"
print(f"\n   Query 1: High-value customers (Gold/Platinum VIP)")
print(f"   Result: {len(active_high_segments):,} customers")
print(f"   Use case: Premium capsule bundle offers")

# Query 2: Lapsed customers from segments (high churn risk)
lapsed_segments = segments_df[segments_df['churnprop'] == 3]
print(f"\n   Query 2: Very high churn risk (no purchase >6 months)")
print(f"   Result: {len(lapsed_segments):,} customers")
print(f"   Use case: Win-back campaign with 20% discount")

# Query 3: Recent cart abandoners
recent_carts = abandoned_df[abandoned_df['tosend'] == 0]
cart_customers = recent_carts['customer'].nunique()
print(f"\n   Query 3: Customers with abandoned carts (reminder not sent)")
print(f"   Result: {cart_customers:,} customers ({len(recent_carts):,} items)")
print(f"   Use case: 24h automated reminder emails")

# Query 4: Wishlist with high-value items
wishlist_machines = wishlist_df[wishlist_df['product'].isin(['BrewMaster', 'CaffeineQueen'])]
print(f"\n   Query 4: Customers with machines in wishlist")
print(f"   Result: {wishlist_machines['customer'].nunique():,} customers")
print(f"   Use case: Machine promotion alerts")

# Query 5: Machine owners without recent capsule purchase
# Get machine buyers
machine_purchases = purchases_df[purchases_df['product'].isin(['BrewMaster', 'CaffeineQueen'])]
machine_owners = set(machine_purchases['customer'].unique())

# Get recent capsule buyers (last 60 days)
capsule_products = ['VanillaVelvet', 'MorningBoost', 'MochaMadness', 'EspressoEnergy', 
                    'CaramelCream', 'RomaRoast', 'MilanoMagic', 'CapriCappuccino', 
                    'AmericanoBliss', 'DecafDelight', 'HazelnutHeaven', 'ChocolateCharm', 
                    'IntenseIndulgence']
recent_date = pd.Timestamp('2025-11-15')  # 60 days before Jan 15, 2026
recent_capsules = purchases_df[
    (purchases_df['product'].isin(capsule_products)) & 
    (purchases_df['date'] >= recent_date)
]
recent_capsule_buyers = set(recent_capsules['customer'].unique())

# Machine owners without recent capsule purchase
needs_replenishment = machine_owners - recent_capsule_buyers
print(f"\n   Query 5: Machine owners without capsule purchase in last 60 days")
print(f"   Result: {len(needs_replenishment):,} customers")
print(f"   Use case: Capsule replenishment reminder")

# Query 6: Multi-tier VIP customers
vip_segments = segments_df[segments_df['vip'] >= 3]
print(f"\n   Query 6: Gold/Platinum VIP customers")
print(f"   Result: {len(vip_segments):,} customers")
print(f"   Use case: Exclusive VIP offers")
print(f"   Note: Use recipients table join for country/language targeting")

print("\n6️⃣  TEMPORAL PATTERNS")
print("-" * 80)

# Orders by month (last 6 months)
purchases_df['month'] = purchases_df['date'].dt.to_period('M')
recent_months = purchases_df[purchases_df['date'] >= '2025-07-01']
monthly_orders = recent_months.groupby('month')['orderref'].nunique()

print(f"\n   Orders by month (Jul 2025 - Jan 2026):")
for month, count in monthly_orders.items():
    print(f"      {month}: {count:>5,} orders")

print("\n7️⃣  ABANDONED CART RECENCY")
print("-" * 80)
from datetime import datetime, timedelta
current_date = pd.Timestamp('2026-01-15')

abandoned_df['days_ago'] = (current_date - abandoned_df['date']).dt.days
recency_bins = [0, 7, 14, 30, 60, 90]
recency_labels = ['<7 days', '7-14 days', '14-30 days', '30-60 days', '60-90 days']
abandoned_df['recency'] = pd.cut(abandoned_df['days_ago'], bins=recency_bins, labels=recency_labels)

print(f"\n   Abandoned cart recency distribution:")
recency_counts = abandoned_df['recency'].value_counts().sort_index()
for period, count in recency_counts.items():
    pct = count / len(abandoned_df) * 100
    print(f"      {period:12} {count:>5,} items ({pct:>5.1f}%)")

print("\n" + "="*80)
print("✅ VERIFICATION COMPLETE - Data ready for Adobe Campaign!")
print("="*80)
print(f"\nSee DATA_SUMMARY.md for complete documentation")
