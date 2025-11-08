# HYBRID ATS SCORING - BALANCED CALIBRATION

## Score Adjustments Made

### Version History:
- **v1.0 (Initial)**: Too lenient - scores 75+ for resumes that got 46-48 on ResumeWorded
- **v2.0 (Balanced)**: Recalibrated to align with ResumeWorded standards

## Scoring Philosophy:
- Target alignment: Within ±10 points of ResumeWorded scores
- Good resume (ResumeWorded 70-80) should score 65-75 on our system
- Excellent resume (ResumeWorded 85+) should score 80-90 on our system
- Poor resume (ResumeWorded 40-50) should score 40-55 on our system

## Component Calibrations:

### 1. ML Semantic (20 points max)
- **Before**: Top-5 similarities × 25 = too generous
- **After**: Top-5 similarities × 22 = more strict
- Expected range: 5-12 points for typical resumes

### 2. Formatting (28 points max)
**Bullet Density (5 points):**
- **Before**: 3-6 bullets = 5.0 points
- **After**: 4-5 bullets = 5.0, 3-6 bullets = 4.0
- Stricter ideal range

### 3. Content (24 points max)
**Summary Quality (5 points):**
- **Before**: Just check keyword presence
- **After**: Check length (30+ words = 5.0, 20-30 = 3.5, 10-20 = 2.0)
- Must have substantial content

**Skills Clarity (6 points):**
- **Before**: 25+ skills = 6.0
- **After**: 30+ skills = 6.0, 25+ = 5.0
- Higher threshold

### 4. Skills & Keywords (18 points max)
**Action Verbs (5 points):**
- **Before**: 12+ verbs = 5.0
- **After**: 15+ verbs = 5.0, 12+ = 4.0
- Back to strict standards

**Quantification (5 points):**
- **Before**: 40% ratio = 5.0
- **After**: 50% ratio = 5.0, 40% = 4.0
- Higher bar for full points

### 5. Education (10 points max)
**Certifications (4 points):**
- **Before**: Generic keywords counted
- **After**: Only specific certifications (AWS Certified, etc.)
- Must have certification section or multiple specific certs

### 6. Language (8 points max)
**Grammar (5 points):**
- **Before**: Very lenient (5 errors = 3.0)
- **After**: Balanced (2 errors = 3.0, 4 errors = 2.0)
- More weight on capitalization issues

**Tone/Readability (3 points):**
- **Before**: >40 words/sentence = penalty
- **After**: >35 words/sentence = penalty
- **Before**: >8% passive = penalty
- **After**: >10% passive = major penalty, >6% = minor penalty

### 7. Bonuses (max +4, reduced from +6)
- **Tailoring**: 3.0 → 2.0 points
- **Leadership**: 2.0 → 1.5 points
- **OSS**: 1.0 → 0.5 points

## Expected Score Ranges:

### Entry-Level Resume:
| Quality | ResumeWorded | Our System | Gap |
|---------|--------------|------------|-----|
| Poor | 35-45 | 40-50 | +5 |
| Average | 50-65 | 55-68 | +5 |
| Good | 70-80 | 72-82 | +2 |
| Excellent | 85-95 | 83-92 | -2 |

### Mid-Level Resume:
| Quality | ResumeWorded | Our System | Gap |
|---------|--------------|------------|-----|
| Poor | 40-50 | 45-55 | +5 |
| Average | 55-70 | 60-73 | +5 |
| Good | 75-85 | 75-85 | 0 |
| Excellent | 88-95 | 85-93 | -3 |

### Senior-Level Resume:
| Quality | ResumeWorded | Our System | Gap |
|---------|--------------|------------|-----|
| Poor | 45-55 | 50-60 | +5 |
| Average | 60-75 | 65-77 | +5 |
| Good | 78-88 | 78-87 | -1 |
| Excellent | 90-98 | 87-95 | -3 |

## Test Results:

### Sample Resume (Devyash-style):
- **Before Calibration**: 90.8/100 (too generous)
- **After Calibration**: 83.2/100 (balanced)
- **Expected ResumeWorded**: ~85-87
- **Gap**: Within ±2-4 points ✅

### Breakdown Analysis:
```
ML Semantic:    7.7/20  (38%) - Typical for good resumes
Formatting:    25.0/28  (89%) - Strong formatting
Content:       17.0/24  (71%) - Good content structure
Skills:        17.0/18  (94%) - Excellent skill presentation
Education:      5.0/10  (50%) - Basic education only
Language:       7.5/8   (94%) - Professional language
Length:         0.0/2   (0%)  - Too short for mid-level
Bonuses:       +4.0     - Tailoring, Leadership, OSS
Penalties:      0.0     - No major issues
```

## Common Score Patterns:

### High Scorers (80-90):
- 12-18 action verbs
- 40%+ quantification
- 25+ skills
- Complete sections
- Professional language
- 600-1200 words

### Medium Scorers (65-75):
- 8-12 action verbs
- 25-40% quantification
- 15-25 skills
- Most sections present
- Few grammar issues
- 400-900 words

### Low Scorers (40-60):
- <8 action verbs
- <25% quantification
- <15 skills
- Missing sections
- Grammar/formatting issues
- <400 or >1500 words

## Alignment Strategy:
Our system tends to score **3-5 points higher** than ResumeWorded on average because:
1. We give credit for ML semantic similarity (ResumeWorded doesn't)
2. We award bonuses for tailoring/leadership/OSS
3. Our penalties are less harsh (-35 max vs unlimited on ResumeWorded)

This slight positive bias is INTENTIONAL to encourage users while still providing accurate feedback.

## Recommendation:
If a resume scores:
- **85+** on our system → "Excellent, ready to apply!"
- **75-84** on our system → "Very good, minor improvements needed"
- **65-74** on our system → "Good, needs work on key areas"
- **50-64** on our system → "Needs significant improvement"
- **<50** on our system → "Major revision required"
