# GBL Sample Comparison

## Key Data Points Extracted

| Field | Sample 1 | Sample 2 | Sample 3 |
|-------|----------|----------|----------|
| **B/L Number** | LKNQ0540823 ✓ | HBAT0163600 ✓ | JEAT0598732 ✓ |
| **SCAC Code** | SDDA | MCHO | DORD |
| **Service Code** | D | D | D |
| **Shipment No** | 1 | 1 | 3 |
| **Date B/L Printed** | 20251212 | 20251212 | 20251126 |
| **Property Owner** | BLYTHE, NICHOLAS | La Rosa, Angelica | Higgins, Charlotte |
| **SSN (Redacted)** | XXX-XX-XXXX | XXX-XX-XXXX | XXX-XX-7835 |
| **Rank/Grade** | TSG/E-6 | SPC/E-4 | PO2/E-5 |
| **Service Branch** | USAF | USA | USN |
| **Authority** | AA8HNT ARPC | 0024968989 FORT BLISS TX | 0995 BUPERS |
| **Date of Order** | 20230320 | 20251113 | 20250409 |
| **Transportation Company** | Suddath Relocation Systems of Atlanta, Inc. | Alaska Seavan, Inc. (SUDDATH RELOCATION SYSTEMS OF TEXAS, INC) | Door to Door Moving & Storage (MITCHELL MOVING AND STORAGE CO) |
| **Origin** | 1550 Central Ave.- Apt. 27, RIVERSIDE, CA 92507 | 11345 Bullseye St, EL PASO, TX 79934 | NTSR - 18800 Southcenter Parkway Lot# 25-015, TUKWILA, WA 98188 |
| **Destination** | BLYTHE, NICHOLAS TSG/E-6 McChord AFB, WA, MCCHORD AFB, WA 98438 | IGNACIO, DAVID , J Agent, JBLM LEWIS, JOINT BASE LEWIS MCCHORD, WA 98433 | Higgins, Charlotte PO2/E-5 NSA/CSS / DENVER, CO, 6000 S Fraser Stapt 08-302, CENTENNIAL, CO 80016 |
| **GBLOC Codes** | JEAT, LKNQ | JEAT, HBAT | KKFA, JEAT |
| **Issuing Officer** | James M. Bode - Director | MEGAN JOSEPH - TRANSPORTATION OFFICER | Ms. Dawn M. Nesiba - Transportation Officer |
| **SDN** | PR08163005NHNT | - | - |
| **AIN** | 387700 | - | - |
| **DI** | 57 | 21 | 17 |
| **TAC** | FIUL | CAE6 | NAD5 |
| **SAC** | 733700 503 6262 73116 5AIR77 46200 01 59398F 387700 | LAR8348PB93172 | 1751453.2258 210 00022 050120 2D D74200 02225CTEQQ5Y |
| **MDC** | NONE | 3AE6 | - |

## Pattern Observations

### B/L Number Format
All follow the pattern: **4 letters + 7 digits** ✓ Working perfectly

### Customer Name Variations
- All caps with comma: `BLYTHE, NICHOLAS`
- Title case with comma: `La Rosa, Angelica`, `Higgins, Charlotte`
- Pattern: `[Last], [First]` followed by rank/grade

### SCAC Codes
- Format: 2-4 uppercase letters
- Present in all samples: SDDA, MCHO, DORD

### Date Format
- Consistent: YYYYMMDD (8 digits)
- Examples: 20251212, 20251126, 20230320

## Extraction Improvements Needed

1. ✓ **B/L Number** - Working perfectly
2. **SCAC Code** - Need to improve extraction (currently returning None for some)
3. **Date B/L Printed** - Need to improve extraction
4. **Property Owner Name** - Handle both UPPER and Title case
5. **Transportation Company** - Better pattern matching
6. **Administrative Codes** - More robust extraction for SDN, AIN when present
