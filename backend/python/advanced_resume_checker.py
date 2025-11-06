"""
Advanced Resume Checker - Comprehensive analysis like ResumeWorded
Checks: Grammar, Spelling, Buzzwords, Formatting, Structure, and more
"""

import re
from typing import Dict, List, Tuple, Set
from datetime import datetime


class AdvancedResumeChecker:
    """Comprehensive resume analysis with multiple quality checks"""
    
    def __init__(self):
        # Ineffective buzzwords/clichés to flag
        self.buzzwords = {
            'team player', 'hard worker', 'detail-oriented', 'results-driven',
            'self-starter', 'go-getter', 'think outside the box', 'synergy',
            'passionate', 'dynamic', 'innovative thinker', 'excellent communication',
            'hard-working', 'motivated', 'dedicated', 'responsible for',
            'duties included', 'strategic thinker', 'proven track record',
            'best of breed', 'go-to person', 'proactive', 'team-oriented',
            'highly motivated', 'fast-paced environment', 'self-motivated',
            'goal-oriented', 'results oriented', 'strong work ethic'
        }
        
        # Weak/passive phrases to avoid
        self.weak_phrases = {
            'helped with', 'assisted in', 'worked on', 'participated in',
            'responsible for', 'duties included', 'was involved in',
            'tried to', 'attempted to', 'tasked with'
        }
        
        # Filler words that add no value
        self.filler_words = {
            'very', 'really', 'quite', 'rather', 'somewhat', 'fairly',
            'pretty', 'just', 'actually', 'basically', 'literally'
        }
        
        # Outdated/unnecessary sections
        self.outdated_sections = {
            'references', 'references available upon request',
            'objective', 'hobbies', 'interests', 'personal information',
            'marital status', 'age', 'photo', 'nationality'
        }
        
        # Common spelling errors in resumes
        self.common_errors = {
            'recieve': 'receive', 'acheive': 'achieve', 'occured': 'occurred',
            'managment': 'management', 'seperate': 'separate', 'definately': 'definitely',
            'accomodate': 'accommodate', 'embarass': 'embarrass', 'concensus': 'consensus',
            'existance': 'existence', 'maintainance': 'maintenance', 'occassion': 'occasion',
            'neccessary': 'necessary', 'publically': 'publicly', 'sucessful': 'successful'
        }
        
        # Personal pronouns to avoid
        self.personal_pronouns = {'i', 'me', 'my', 'we', 'us', 'our'}
        
    def analyze_comprehensive(self, text: str, info: Dict) -> Dict:
        """
        Comprehensive analysis returning multiple quality scores
        
        Returns:
            Dictionary with individual scores for each category
        """
        text_lower = text.lower()
        
        results = {
            # Core structure checks
            'structure_score': self._check_structure(text, info),
            'formatting_score': self._check_formatting(text, info),
            
            # Content quality checks
            'buzzword_score': self._check_buzzwords(text_lower),
            'weak_phrases_score': self._check_weak_phrases(text_lower),
            'grammar_score': self._check_grammar(text, info),
            'spelling_score': self._check_spelling(text_lower),
            
            # Professional checks
            'pronoun_score': self._check_pronouns(text_lower),
            'date_format_score': self._check_date_formatting(text),
            'outdated_sections_score': self._check_outdated_sections(text_lower),
            
            # Quantification & impact
            'impact_score': self._check_impact(text, info),
            'quantification_score': self._check_quantification(info),
            
            # Length & density
            'length_score': self._check_length(info),
            'density_score': self._check_content_density(text, info),
            
            # Details for feedback
            'issues_found': [],
            'warnings': [],
            'strengths': []
        }
        
        # Collect specific issues
        results['issues_found'] = self._collect_issues(text, text_lower, info)
        results['warnings'] = self._collect_warnings(text, info, results)
        results['strengths'] = self._collect_strengths(info, results)
        
        # Calculate overall score (weighted)
        results['overall_score'] = self._calculate_overall_score(results)
        
        return results
    
    def _check_structure(self, text: str, info: Dict) -> float:
        """Check resume structure and organization (15 points)"""
        score = 0
        
        # Core sections present (10 points)
        required_sections = {'experience', 'education', 'skills'}
        recommended_sections = {'summary', 'projects', 'certifications'}
        
        found_sections = set(s.lower() for s in info.get('sections', []))
        
        # Must have all required
        if required_sections.issubset(found_sections):
            score += 10
        else:
            missing = required_sections - found_sections
            score += 10 * (len(required_sections - missing) / len(required_sections))
        
        # Bonus for recommended sections (5 points)
        recommended_found = len(found_sections & recommended_sections)
        score += (recommended_found / len(recommended_sections)) * 5
        
        return score
    
    def _check_formatting(self, text: str, info: Dict) -> float:
        """Check formatting consistency (10 points)"""
        score = 10
        lines = text.split('\n')
        
        # Check bullet point consistency
        bullet_types = set()
        for line in lines:
            match = re.match(r'^\s*([•\-\*◦▪○●])\s+', line)
            if match:
                bullet_types.add(match.group(1))
        
        # Penalty for mixed bullet styles
        if len(bullet_types) > 2:
            score -= 3
        
        # Check for consistent spacing
        blank_line_counts = []
        prev_blank = False
        count = 0
        for line in lines:
            if line.strip() == '':
                if not prev_blank:
                    count = 1
                else:
                    count += 1
                prev_blank = True
            else:
                if prev_blank and count > 0:
                    blank_line_counts.append(count)
                prev_blank = False
                count = 0
        
        # Penalty for inconsistent spacing
        if blank_line_counts and len(set(blank_line_counts)) > 2:
            score -= 2
        
        return max(0, score)
    
    def _check_buzzwords(self, text_lower: str) -> float:
        """Check for ineffective buzzwords (10 points)"""
        found_buzzwords = []
        for buzzword in self.buzzwords:
            if buzzword in text_lower:
                found_buzzwords.append(buzzword)
        
        # Deduct points for each buzzword
        penalty = len(found_buzzwords) * 2
        score = max(0, 10 - penalty)
        
        return score
    
    def _check_weak_phrases(self, text_lower: str) -> float:
        """Check for weak/passive phrases (10 points)"""
        found_weak = []
        for phrase in self.weak_phrases:
            if phrase in text_lower:
                found_weak.append(phrase)
        
        # Deduct points for each weak phrase
        penalty = len(found_weak) * 2.5
        score = max(0, 10 - penalty)
        
        return score
    
    def _check_grammar(self, text: str, info: Dict) -> float:
        """Basic grammar checks (10 points)"""
        score = 10
        
        # Check for basic grammar issues
        # Double spaces
        if '  ' in text:
            score -= 1
        
        # Check for sentences starting with lowercase (after periods)
        sentences = re.split(r'[.!?]\s+', text)
        lowercase_starts = sum(1 for s in sentences if s and s[0].islower())
        if lowercase_starts > 2:
            score -= 2
        
        # Check for missing periods at end of bullets
        lines = text.split('\n')
        bullets_without_period = 0
        for line in lines:
            if re.match(r'^\s*[•\-\*◦▪]\s+', line):
                # If bullet is long enough, should end with period
                if len(line.strip()) > 50 and not line.strip().endswith(('.', '!', '?')):
                    bullets_without_period += 1
        
        if bullets_without_period > 5:
            score -= 2
        
        return max(0, score)
    
    def _check_spelling(self, text_lower: str) -> float:
        """Check for common spelling errors (10 points)"""
        words = re.findall(r'\b\w+\b', text_lower)
        
        errors_found = []
        for word in words:
            if word in self.common_errors:
                errors_found.append(word)
        
        # Deduct 2 points per error
        penalty = len(set(errors_found)) * 2
        score = max(0, 10 - penalty)
        
        return score
    
    def _check_pronouns(self, text_lower: str) -> float:
        """Check for personal pronouns (should be avoided) (5 points)"""
        words = re.findall(r'\b\w+\b', text_lower)
        
        pronoun_count = sum(1 for word in words if word in self.personal_pronouns)
        
        # Allow a few (like in summary), penalize excessive use
        if pronoun_count <= 2:
            score = 5
        elif pronoun_count <= 5:
            score = 3
        else:
            score = max(0, 5 - (pronoun_count - 5) * 0.5)
        
        return score
    
    def _check_date_formatting(self, text: str) -> float:
        """Check date formatting consistency (10 points)"""
        # Find all date patterns
        date_patterns = [
            r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}\b',  # Jan 2020
            r'\b\d{1,2}/\d{4}\b',  # 01/2020
            r'\b\d{4}\b',  # 2020
            r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b'  # January 2020
        ]
        
        formats_found = set()
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                formats_found.add(pattern)
        
        # Score based on consistency
        if len(formats_found) == 0:
            return 5  # No dates found (might be okay for fresh grads)
        elif len(formats_found) == 1:
            return 10  # Consistent formatting
        elif len(formats_found) == 2:
            return 7   # Mostly consistent
        else:
            return 3   # Inconsistent
    
    def _check_outdated_sections(self, text_lower: str) -> float:
        """Check for outdated/unnecessary sections (10 points)"""
        found_outdated = []
        for section in self.outdated_sections:
            if section in text_lower:
                found_outdated.append(section)
        
        # Major penalty for outdated sections
        penalty = len(found_outdated) * 5
        score = max(0, 10 - penalty)
        
        return score
    
    def _check_impact(self, text: str, info: Dict) -> float:
        """Check for impact/achievement-oriented language (10 points)"""
        # Strong action verbs indicating impact
        impact_verbs = {
            'increased', 'decreased', 'reduced', 'improved', 'enhanced',
            'generated', 'delivered', 'achieved', 'exceeded', 'transformed',
            'launched', 'pioneered', 'spearheaded', 'accelerated', 'optimized',
            'streamlined', 'doubled', 'tripled', 'boosted', 'elevated'
        }
        
        text_lower = text.lower()
        impact_count = sum(1 for verb in impact_verbs if verb in text_lower)
        
        # Score based on number of impact verbs
        if impact_count >= 8:
            return 10
        elif impact_count >= 5:
            return 8
        elif impact_count >= 3:
            return 6
        else:
            return max(0, impact_count * 2)
    
    def _check_quantification(self, info: Dict) -> float:
        """Check quantification ratio (15 points)"""
        total_bullets = info.get('total_bullets', 0)
        quantified_bullets = info.get('quantified_bullets', 0)
        
        if total_bullets == 0:
            return 10  # No bullets, neutral score
        
        ratio = quantified_bullets / total_bullets
        
        # ResumeWorded wants 50%+ quantified
        if ratio >= 0.7:
            return 15
        elif ratio >= 0.5:
            return 13
        elif ratio >= 0.35:
            return 10
        elif ratio >= 0.2:
            return 7
        else:
            return 4
    
    def _check_length(self, info: Dict) -> float:
        """Check resume length appropriateness (10 points)"""
        word_count = info.get('word_count', 0)
        
        # Ideal: 400-800 words (1-2 pages)
        if 400 <= word_count <= 800:
            return 10
        elif 350 <= word_count < 400:
            return 8
        elif 300 <= word_count < 350:
            return 6
        elif 800 < word_count <= 1000:
            return 8
        elif 1000 < word_count <= 1200:
            return 6
        elif word_count < 300:
            return 3
        else:
            return 4
    
    def _check_content_density(self, text: str, info: Dict) -> float:
        """Check content density and white space (5 points)"""
        lines = text.split('\n')
        non_empty_lines = [l for l in lines if l.strip()]
        
        if not lines:
            return 0
        
        # Good density: 60-80% non-empty lines
        density = len(non_empty_lines) / len(lines)
        
        if 0.6 <= density <= 0.8:
            return 5
        elif 0.5 <= density < 0.6 or 0.8 < density <= 0.85:
            return 4
        elif density > 0.9:
            return 2  # Too dense, no white space
        else:
            return 3
    
    def _collect_issues(self, text: str, text_lower: str, info: Dict) -> List[Dict]:
        """Collect specific issues found"""
        issues = []
        
        # Buzzwords
        found_buzzwords = [bw for bw in self.buzzwords if bw in text_lower]
        if found_buzzwords:
            issues.append({
                'category': 'Buzzwords & Clichés',
                'severity': 'medium',
                'count': len(found_buzzwords),
                'examples': found_buzzwords[:3],
                'message': f'Found {len(found_buzzwords)} vague buzzwords that add little value'
            })
        
        # Weak phrases
        found_weak = [wp for wp in self.weak_phrases if wp in text_lower]
        if found_weak:
            issues.append({
                'category': 'Weak Phrases',
                'severity': 'medium',
                'count': len(found_weak),
                'examples': found_weak[:3],
                'message': f'Found {len(found_weak)} weak/passive phrases - use strong action verbs'
            })
        
        # Spelling errors
        words = re.findall(r'\b\w+\b', text_lower)
        spelling_errors = [w for w in words if w in self.common_errors]
        if spelling_errors:
            issues.append({
                'category': 'Spelling',
                'severity': 'high',
                'count': len(set(spelling_errors)),
                'examples': list(set(spelling_errors))[:3],
                'message': f'Found {len(set(spelling_errors))} spelling errors'
            })
        
        # Personal pronouns
        pronoun_count = sum(1 for word in words if word in self.personal_pronouns)
        if pronoun_count > 5:
            issues.append({
                'category': 'Personal Pronouns',
                'severity': 'low',
                'count': pronoun_count,
                'message': f'Used {pronoun_count} personal pronouns (I, me, my) - avoid in resumes'
            })
        
        # Repetitive action verbs
        repetitive = info.get('repetitive_verbs', {})
        if repetitive:
            for verb, count in repetitive.items():
                issues.append({
                    'category': 'Repetition',
                    'severity': 'medium',
                    'verb': verb,
                    'count': count,
                    'message': f'Action verb "{verb.title()}" used {count} times (max 2 recommended)'
                })
        
        # Outdated sections
        found_outdated = [s for s in self.outdated_sections if s in text_lower]
        if found_outdated:
            issues.append({
                'category': 'Unnecessary Sections',
                'severity': 'high',
                'examples': found_outdated,
                'message': f'Found outdated sections: {", ".join(found_outdated)}'
            })
        
        return issues
    
    def _collect_warnings(self, text: str, info: Dict, results: Dict) -> List[str]:
        """Collect warnings based on scores"""
        warnings = []
        
        if results['quantification_score'] < 10:
            ratio = info.get('quantified_bullets', 0) / max(info.get('total_bullets', 1), 1)
            warnings.append(f'Only {int(ratio*100)}% of bullets are quantified - aim for 50%+')
        
        if results['length_score'] < 6:
            wc = info.get('word_count', 0)
            if wc < 300:
                warnings.append(f'Resume too short ({wc} words) - aim for 400-800 words')
            else:
                warnings.append(f'Resume too long ({wc} words) - aim for 400-800 words')
        
        if results['structure_score'] < 10:
            warnings.append('Missing key resume sections (Experience, Education, Skills)')
        
        if results['date_format_score'] < 7:
            warnings.append('Inconsistent date formatting throughout resume')
        
        return warnings
    
    def _collect_strengths(self, info: Dict, results: Dict) -> List[str]:
        """Collect strengths based on scores"""
        strengths = []
        
        if results['buzzword_score'] >= 9:
            strengths.append('No ineffective buzzwords or clichés found')
        
        if results['spelling_score'] >= 9:
            strengths.append('No spelling errors detected')
        
        if results['outdated_sections_score'] >= 9:
            strengths.append('No outdated or unnecessary sections')
        
        if results['date_format_score'] >= 9:
            strengths.append('Consistent date formatting throughout')
        
        if results['quantification_score'] >= 13:
            strengths.append('Excellent quantification of achievements')
        
        if results['impact_score'] >= 8:
            strengths.append('Strong use of impact-oriented language')
        
        if len(info.get('sections', [])) >= 5:
            strengths.append('Well-structured with comprehensive sections')
        
        return strengths
    
    def _calculate_overall_score(self, results: Dict) -> float:
        """Calculate weighted overall score"""
        weights = {
            'structure_score': 1.2,
            'formatting_score': 0.8,
            'buzzword_score': 1.0,
            'weak_phrases_score': 1.0,
            'grammar_score': 1.0,
            'spelling_score': 1.5,  # Higher weight
            'pronoun_score': 0.5,
            'date_format_score': 1.0,
            'outdated_sections_score': 1.2,
            'impact_score': 1.3,  # Higher weight
            'quantification_score': 1.5,  # Highest weight
            'length_score': 0.8,
            'density_score': 0.5
        }
        
        total_score = 0
        total_weight = 0
        
        for key, weight in weights.items():
            if key in results:
                total_score += results[key] * weight
                total_weight += weight * 10  # Each score is out of 10-15 points
        
        # Normalize to 100
        normalized_score = (total_score / total_weight) * 100
        
        return round(normalized_score, 1)
