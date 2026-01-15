# Frescopa Demo Data - Summary Report

**Generated:** January 15, 2026  
**Business Period:** January 2023 - January 2026 (3 years)

---

## 📊 Dataset Overview

| Table | Rows | Description |
|-------|------|-------------|
| **brands** | 2 | Coffee brands (Coffee Works, Java Junction) |
| **products** | 20 | 13 capsules + 2 machines + 1 discount + 4 accessories |
| **recipients** | 19,933 | Customer master data with demographics |
| **purchases** | 161,742 | Order lines (78,188 orders) |
| **wishlist** | 3,990 | Aspirational products (2,990 customers) |
| **abandoned** | 10,000 | Recent cart abandonments (5,744 customers) |
| **segments** | 19,933 | Customer analytics (1:1 with recipients) |
| **TOTAL** | **215,620** | **Total rows across all tables** |

---

## 🔗 Data Model & Relationships

### Foreign Key Integrity (100% Validated)

```
brands (name)
  ↓ 1:N
  ├─→ products (brand)
  └─→ recipients (brand)
  
recipients (crmid)
  ↓ 1:N
  ├─→ purchases (customer)
  ├─→ wishlist (customer)
  ├─→ abandoned (customer)
  └─→ segments (customer) [1:1]
  
products (code)
  ↓ 1:N
  ├─→ purchases (product)
  ├─→ wishlist (product)
  └─→ abandoned (product)
```

---

## 👥 Customer Segmentation

| Segment | Count | % | Purchase Behavior | Machine Ownership |
|---------|-------|---|-------------------|-------------------|
| **Active High** | 3,003 | 15% | 8-12 orders/year (25-35 days) | 95% |
| **Active Medium** | 3,955 | 20% | 6-9 orders/year (40-60 days) | 90% |
| **Occasional** | 5,057 | 25% | 2-4 orders/year (80-120 days) | 70% |
| **One-time** | 2,954 | 15% | 1-2 purchases total | 40% |
| **Lapsed** | 2,988 | 15% | No purchase >6 months | 80% |
| **Prospect** | 1,976 | 10% | Never purchased | 0% |

**Purchased Customers:** 15,681 (78.7%)  
**Non-Purchasers:** 4,252 (21.3% - prospects + inactive)

---

## 🌍 Geographic Distribution

| Country | Customers | Language | Distribution |
|---------|-----------|----------|--------------|
| **United States** | ~7,973 | English | 40% |
| **United Kingdom** | ~4,983 | English | 25% |
| **France** | ~3,987 | French | 20% |
| **Germany** | ~2,990 | German | 15% |

**Gender Distribution:**
- Male: 48%
- Female: 48%
- Other: 4%

---

## ☕ Product Catalog

### Capsules (Category 1) - 13 varieties

**Coffee Works Brand (8 capsules):**
- VanillaVelvet, MorningBoost, MochaMadness, EspressoEnergy, CaramelCream
- RomaRoast, MilanoMagic, CapriCappuccino, AmericanoBliss, DecafDelight

**Java Junction Brand (3 capsules):**
- HazelnutHeaven, ChocolateCharm, IntenseIndulgence

**Price Range:** €9.00 - €14.00 per sleeve

### Machines (Category 2) - 2 models

- **BrewMaster** - €199.00
- **CaffeineQueen** - €399.00

### Accessories (Category 4) - 4 items

- **DescaleKit** - €19.00
- **CapsuleHolder** - €29.00
- **MilkFrother** - €89.00
- **TravelMug** - €24.00

### Special (Category 3)

- **discount** - Variable discount application

---

## 📈 Purchase Patterns

**Total Orders:** 78,188  
**Total Order Lines:** 161,742  
**Average Lines per Order:** 2.07  
**Date Range:** January 2023 - January 15, 2026

**Temporal Distribution:**
- Peak Season (Sept-Feb): Higher frequency, holiday spikes
- Low Season (June-Aug): Reduced frequency
- Time of Day: 60% orders between 12pm-10pm

**Typical Order Composition:**
- Capsules: 80-85% of orders (5-20 sleeves)
- Machines: 15% of orders (first-time or upgrades)
- Accessories: 5% of orders
- Discounts: 20% of orders (5-15% off)

---

## 💝 Wishlist Analysis

**Total Items:** 3,990  
**Customers with Wishlist:** 2,990 (15% of total)  
**Average Items per Customer:** 1.3

**Wishlist Content:**
- 80% Machines (aspiration for premium models)
- 15% Accessories
- 5% Premium capsule bundles

**Creation Window:** Last 6 months (July 2025 - January 2026)

---

## 🛒 Abandoned Cart Analysis

**Total Items:** 10,000  
**Customers with Abandoned Carts:** 5,744  
**Date Range:** Last 90 days (October 17, 2025 - January 15, 2026)

**Recency Distribution:**
- Last 2 weeks: 40%
- Last month: 25%
- 1-2 months ago: 20%
- 2-3 months ago: 15%

**Field `tosend`:** All set to 0 (ready for remarketing triggers)

---

## 📊 Customer Analytics (Segments Table)

### Churn Propensity

| Level | Score | Days Since Purchase | Customers |
|-------|-------|---------------------|-----------|
| Low | 0 | <60 days | ~45% |
| Medium | 1 | 60-120 days | ~20% |
| High | 2 | 120-180 days | ~15% |
| Very High | 3 | >180 days | ~20% |

### VIP Tiers (Based on Total Spend)

| Tier | Score | Spend Range | Distribution |
|------|-------|-------------|--------------|
| Invalid/Blacklist | -1 | Prospects | 10% |
| Standard | 0 | <€100 | 30% |
| Bronze | 1 | €100-€500 | 35% |
| Silver | 2 | €500-€1,500 | 15% |
| Gold | 3 | €1,500-€3,000 | 7% |
| Platinum | 4 | >€3,000 | 3% |

### Net Promoter Score (NPS)

- Range: 6-9
- Distribution: Bell curve around 7-8
- Correlated with purchase frequency

### Engagement Score (reactscore)

- Range: 0-10
- Based on purchase count
- Updated: January 10, 2026

---

## 🎯 Adobe Campaign Demo Scenarios

### 1. **Segmentation Queries**

#### RFM Analysis
```
- Active buyers (last 60 days)
- At-risk customers (60-120 days)
- Lapsed customers (120+ days)
- High-value customers (VIP tier ≥3)
```

#### Product Affinity
```
- Machine owners without recent capsule purchase
- Capsule subscribers (regular reorder pattern)
- Premium buyers (VIP + machines)
- Accessories cross-sell candidates
```

#### Geographic Targeting
```
- Multi-country campaigns (US, UK, FR, DE)
- Language-specific personalization
- Regional product preferences
```

---

### 2. **Automated Campaigns**

#### Abandoned Cart Recovery
- **10,000 recent abandonments** ready for testing
- Trigger: 24h, 48h, 72h reminders
- Offer progression: reminder → 5% off → 10% off

#### Replenishment Reminders
- **Active buyers** with predictable reorder cycles
- Trigger: 25-30 days after last capsule order
- "Time to restock your favorite blends!"

#### Win-Back Campaigns
- **2,988 lapsed customers** (no purchase >6 months)
- Multi-touch sequences
- Special reactivation offers

#### Birthday Campaigns
- **19,933 customers** with birthdates
- Monthly cohorts ready
- "Celebrate with 15% off!"

---

### 3. **Advanced Segmentation**

#### Wishlist Conversion
- **3,990 wishlist items** for remarketing
- "Your BrewMaster is on sale!"
- Cross-reference with purchase history

#### Churn Prevention
- **High churn risk** (score 2-3): targeted retention
- Predictive: customers showing declining frequency
- Early intervention offers

#### Upsell/Cross-sell
```sql
-- Machine buyers without accessories
-- One-time buyers → subscription conversion
-- Standard tier → VIP progression
```

#### Multi-Brand Strategy
- Coffee Works vs Java Junction preferences
- Brand-specific campaigns
- Cross-brand offers

---

### 4. **Journey Orchestration**

#### New Customer Onboarding
- **Prospects** (1,976 never purchased)
- Acquisition source tracking
- First purchase incentives

#### Post-Purchase Follow-up
- Machine buyers → capsule education
- First capsule order → taste profile survey
- Accessory recommendations

#### Lifecycle Campaigns
- Prospect → First Purchase → Regular → VIP → Retention
- Segment transitions tracked
- Automated journey triggers

---

## 📅 Temporal Scenarios (Current Date: Jan 15, 2026)

### Timely Campaigns

**January 2026 (NOW):**
- Post-holiday engagement
- New Year resolution (premium coffee at home)
- Peak season (winter coffee consumption)

**Recent Activity:**
- Abandoned carts: Last 90 days
- Wishlists: Last 6 months
- Churn risk calculated: Jan 10, 2026

**Historical Analysis:**
- 3-year purchase history (2023-2026)
- Seasonal patterns visible
- Cohort analysis ready

---

## ✅ Data Quality & Integrity

### Validated Constraints

✓ **All FK relationships** (9 foreign keys validated)  
✓ **1:1 relationship** (segments ↔ recipients)  
✓ **No orphaned records**  
✓ **No invalid product references**  
✓ **No future dates** (all ≤ Jan 15, 2026)  
✓ **Realistic temporal sequences** (acquisition → purchases → carts)  
✓ **Business rule compliance** (machine owners buy capsules)

### Date Integrity

✓ All purchase dates between customer acquisition and current date  
✓ Lapsed customers: last purchase 180-540 days ago  
✓ Abandoned carts: last 90 days only  
✓ Wishlists: last 6 months  
✓ Seasonal patterns applied  

---

## 🚀 Import Instructions

### File Locations

**Source Data:** `/data-sample/` (original 8 products, 19,933 recipients)  
**Augmented Data:** `/data-augmented/` (all 7 tables, production-ready)

### Encoding

**Format:** CSV with semicolon separator (`;`)  
**Encoding:** Latin-1 (handles special characters like Anaïs, café)

### Import Order (Respect FK Dependencies)

1. `brands.csv` (no dependencies)
2. `products.csv` (depends on brands)
3. `recipients.csv` (depends on brands)
4. `purchases.csv` (depends on recipients + products)
5. `wishlist.csv` (depends on recipients + products)
6. `abandoned.csv` (depends on recipients + products)
7. `segments.csv` (depends on recipients)

---

## 📝 Notes for Adobe Campaign Classic

### Schema Mapping Recommendations

**Recipients Table:**
- Primary Key: `crmid`
- Add custom fields: `segment`, `acquisition_date`, `country`, `gender`, `language`, `owns_machine`
- Folder: Use existing `folder` field

**Purchase Table:**
- Link to recipients: `customer` → `recipients.crmid`
- Link to products: `product` → `products.code`
- Consider creating order header table (group by `orderref`)

**Segments Table:**
- 1:1 extension of recipients
- Import as custom resource or extend recipient schema
- Use for advanced targeting

### Workflow Ideas

1. **Daily Cart Abandonment**: Process carts where `tosend=0` and date >24h
2. **Weekly Churn Risk**: Target `churnprop ≥2` with retention offers
3. **Monthly Replenishment**: Find capsule buyers due for reorder
4. **Wishlist Alerts**: Price drops or stock availability on wishlisted items

---

## 🎓 Demo Value Proposition

This dataset enables demonstrations of:

✅ **Multi-table joins** (recipients ↔ purchases ↔ products)  
✅ **Temporal segmentation** (recency, frequency, lifecycle)  
✅ **Behavioral targeting** (machine owners, capsule preferences)  
✅ **Geographic personalization** (country, language)  
✅ **Churn prediction** (propensity scores)  
✅ **Campaign automation** (cart abandonment, replenishment)  
✅ **Journey orchestration** (prospect → customer → VIP)  
✅ **Cross-sell/upsell** (machines → capsules → accessories)  
✅ **Data quality** (100% referential integrity)  

---

**Generated by:** Frescopa Data Generator v1.0  
**Script:** `generate_augmented_data.py`  
**Validation:** All FK constraints passed ✅
