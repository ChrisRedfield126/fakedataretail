# Frescopa Retail Demo Data for Adobe Campaign Classic

**Business:** Coffee capsules & machines (Nespresso-style)  
**Generated:** January 15, 2026  
**Timeline:** 3 years (Jan 2023 - Jan 2026)  
**Total Rows:** 215,620

---

## 📁 File Structure

```
fakedataretail/
├── data-sample/          # Original data (8 products, ~20K recipients)
├── data-augmented/       # ✅ Production-ready augmented data
│   ├── brands.csv        # 2 brands
│   ├── products.csv      # 20 products (13 capsules + 2 machines + 4 accessories)
│   ├── recipients.csv    # 19,933 customers with demographics
│   ├── purchases.csv     # 161,742 order lines (78,188 orders)
│   ├── wishlist.csv      # 3,990 wishlist items
│   ├── abandoned.csv     # 10,000 abandoned cart items
│   └── segments.csv      # 19,933 customer analytics
├── generate_augmented_data.py   # Main generation script
├── verify_data.py               # Data verification & sample queries
├── DATA_SUMMARY.md              # Complete documentation
└── README.md                    # This file
```

---

## 🚀 Quick Start

### 1. Generate the Data

```bash
python3 generate_augmented_data.py
```

**Output:** 7 CSV files in `data-augmented/` folder (ready for ACC import)

### 2. Verify Data Quality

```bash
python3 verify_data.py
```

**Output:** Statistics, sample queries, and validation results

### 3. Import to Adobe Campaign

**Order matters!** Import in this sequence (respects FK dependencies):

1. `brands.csv`
2. `products.csv`
3. `recipients.csv`
4. `purchases.csv`
5. `wishlist.csv`
6. `abandoned.csv`
7. `segments.csv`

**Encoding:** Latin-1 (handles special characters)  
**Separator:** Semicolon (`;`)

---

## 📊 Dataset Highlights

| Metric | Value | Details |
|--------|-------|---------|
| **Customers** | 19,933 | 78.7% purchased, 21.3% prospects |
| **Orders** | 78,188 | 3 years of history |
| **Products** | 20 | Capsules + machines + accessories |
| **Countries** | 4 | US (40%), UK (25%), FR (20%), DE (15%) |
| **Segments** | 6 | Active high/medium, occasional, one-time, lapsed, prospect |
| **Abandoned Carts** | 10,000 | Last 90 days (actionable) |
| **Wishlist Items** | 3,990 | 2,990 customers |

---

## 🎯 Demo Scenarios Enabled

### Segmentation
- ✅ RFM analysis (recency, frequency, monetary)
- ✅ Customer lifecycle (prospect → active → lapsed)
- ✅ VIP tiers (6 levels: invalid to platinum)
- ✅ Churn risk scores (4 levels)
- ✅ Geographic targeting (4 countries, 4 languages)
- ✅ Product affinity (machine owners, capsule preferences)

### Automated Campaigns
- ✅ Abandoned cart recovery (10K recent carts)
- ✅ Replenishment reminders (predictable reorder cycles)
- ✅ Win-back campaigns (2,988 lapsed customers)
- ✅ Birthday campaigns (19,933 birthdates)
- ✅ Wishlist alerts (price drops, stock availability)

### Advanced Queries
- ✅ Machine owners without capsule purchase
- ✅ High-value customers with declining frequency
- ✅ Multi-brand preferences
- ✅ Cross-sell/upsell opportunities
- ✅ Seasonal purchase patterns

---

## 🔗 Data Model

```
brands (PK: name)
  ├─→ products.brand (FK)
  └─→ recipients.brand (FK)

products (PK: code)
  ├─→ purchases.product (FK)
  ├─→ wishlist.product (FK)
  └─→ abandoned.product (FK)

recipients (PK: crmid)
  ├─→ purchases.customer (FK)
  ├─→ wishlist.customer (FK)
  ├─→ abandoned.customer (FK)
  └─→ segments.customer (FK, 1:1)
```

**Validation:** ✅ 100% FK integrity verified

---

## 📈 Key Statistics

### Customer Segments
- **Active High (15%):** 8-12 orders/year, 95% machine ownership
- **Active Medium (20%):** 6-9 orders/year, 90% machine ownership
- **Occasional (25%):** 2-4 orders/year, 70% machine ownership
- **One-time (15%):** 1-2 purchases total, 40% machine ownership
- **Lapsed (15%):** No purchase >6 months, 80% machine ownership
- **Prospect (10%):** Never purchased, 0% machine ownership

### VIP Distribution
- **Platinum (2.3%):** >€3,000 spent
- **Gold (25.6%):** €1,500-€3,000
- **Silver (36.7%):** €500-€1,500
- **Bronze (11.9%):** €100-€500
- **Standard (2.2%):** <€100
- **Invalid (21.3%):** Prospects/blacklisted

### Churn Risk
- **Low (34.7%):** Last purchase <60 days
- **Medium (5.6%):** 60-120 days
- **High (3.9%):** 120-180 days
- **Very High (55.8%):** >180 days (includes lapsed + prospects)

---

## 💡 Sample Demo Queries

### Query 1: Replenishment Reminder
**Target:** Machine owners without capsule purchase in last 60 days  
**Result:** 1,495 customers  
**Campaign:** "Time to restock your favorite blends!"

### Query 2: Cart Recovery
**Target:** Abandoned carts in last 48 hours where `tosend=0`  
**Result:** ~2,000 items  
**Campaign:** "You left something behind! Complete your order."

### Query 3: Win-Back
**Target:** Lapsed customers (segment='lapsed')  
**Result:** 2,988 customers  
**Campaign:** "We miss you! Here's 20% off your next order."

### Query 4: VIP Multi-Country
**Target:** Gold/Platinum customers by country  
**Result:** 5,549 customers (US: 2,196 | UK: 1,391 | FR: 1,144 | DE: 818)  
**Campaign:** Language-personalized exclusive offers

### Query 5: Wishlist Alert
**Target:** Customers with machines in wishlist  
**Result:** 1,298 customers  
**Campaign:** "Your BrewMaster is now 15% off!"

---

## 📅 Temporal Features

**Current Date (in dataset):** January 15, 2026  
**Business History:** January 2023 - January 2026 (3 years)

**Recency Windows:**
- Abandoned carts: Last 90 days (Oct 17, 2025 - Jan 15, 2026)
- Wishlists: Last 6 months (Jul 15, 2025 - Jan 15, 2026)
- Lapsed definition: No purchase since Jul 15, 2025 (6+ months)

**Seasonal Patterns:**
- ☕ Peak season: Sept-Feb (fall/winter)
- 🌞 Low season: June-Aug (summer)
- 🎄 Holiday spike: December-January

---

## 🛠️ Technical Details

### Generation Script
- **Language:** Python 3.12+
- **Libraries:** pandas, numpy
- **Runtime:** ~2-3 minutes on standard laptop
- **Reproducible:** Fixed random seed (42)

### Data Quality
- ✅ No orphaned records
- ✅ No invalid FK references
- ✅ No future dates
- ✅ Realistic temporal sequences
- ✅ Business rule compliance
- ✅ 1:1 relationship validation (segments ↔ recipients)

### Encoding
- **Format:** CSV with semicolon separator (`;`)
- **Encoding:** Latin-1 (handles accents: Anaïs, café)
- **Compatible with:** Adobe Campaign Classic, Excel, SQL imports

---

## 📖 Documentation

- **DATA_SUMMARY.md:** Complete documentation with all demo scenarios
- **verify_data.py:** Sample queries and statistics
- **This README:** Quick reference

---

## 🎓 Use Cases for Adobe Campaign Demos

### Beginner Level
1. Simple recipient list export
2. Email to all customers in France
3. Birthday campaign (this month)

### Intermediate Level
4. Segmentation: Active vs Lapsed customers
5. Product affinity: Machine owners
6. Geographic targeting with language personalization

### Advanced Level
7. RFM segmentation (recency, frequency, monetary)
8. Abandoned cart automation with escalation
9. Churn prediction targeting
10. Multi-touch win-back journey
11. Cross-sell workflows (machines → capsules → accessories)
12. VIP tier-based personalization

### Expert Level
13. Predictive replenishment based on purchase patterns
14. Multi-brand preference analysis
15. Cohort analysis (acquisition month)
16. Customer lifetime value optimization
17. Dynamic product recommendations
18. Journey orchestration (prospect → VIP)

---

## ✅ Validation Checklist

Before importing to Adobe Campaign, verify:

- [ ] All 7 CSV files present in `data-augmented/`
- [ ] Files open correctly (encoding=latin-1, sep=';')
- [ ] Run `verify_data.py` - all checks pass
- [ ] Import order: brands → products → recipients → purchases → wishlist → abandoned → segments
- [ ] FK constraints mapped in ACC schemas
- [ ] Date fields properly formatted (dd/mm/yyyy HH:MM)

---

## 🤝 Support

**Questions?** See `DATA_SUMMARY.md` for detailed documentation.

**Issues?** Re-run `generate_augmented_data.py` (deterministic output)

**Customization?** Edit script parameters:
- `TARGET_PRODUCTS` - Number of products
- `TARGET_PURCHASES_ORDERS` - Number of orders
- `RANDOM_SEED` - Change for different data

---

## 📜 Version History

**v1.0 (Jan 15, 2026)**
- Initial release
- 215,620 total rows
- 6 customer segments
- 20 products
- 100% FK integrity

---

**Generated by:** Frescopa Data Generator  
**Business Model:** Coffee capsules & machines (Nespresso-style)  
**Ready for:** Adobe Campaign Classic import & demos 🚀
