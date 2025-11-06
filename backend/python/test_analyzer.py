#!/usr/bin/env python3
"""
Test Resume Analyzer - Shows detailed breakdown of scoring
"""

import json
from resume_analyzer_ml import get_analyzer

# Sample resume text (you can replace with your actual resume)
sample_resume = """
John Doe
Email: john.doe@email.com | Phone: (123) 456-7890 | LinkedIn: linkedin.com/in/johndoe

PROFESSIONAL SUMMARY
Results-driven Software Engineer with 5+ years of experience developing scalable web applications.
Proven track record of improving system performance by 40% and reducing deployment time by 60%.

EXPERIENCE

Senior Software Engineer | Tech Corp | Jan 2020 - Present
• Developed and deployed microservices architecture serving 100K+ daily active users
• Improved application performance by 45% through code optimization and caching strategies
• Led team of 5 developers in agile environment, increasing sprint velocity by 30%
• Automated CI/CD pipeline reducing deployment time from 2 hours to 20 minutes
• Implemented comprehensive testing suite achieving 95% code coverage

Software Developer | StartupXYZ | Jun 2018 - Dec 2019
• Built REST APIs using Node.js and Express handling 10K requests per second
• Integrated payment processing system increasing revenue by $500K annually
• Collaborated with cross-functional teams to launch 3 major product features
• Reduced bug count by 60% through implementation of automated testing

EDUCATION
Bachelor of Science in Computer Science | University of Technology | 2018
GPA: 3.8/4.0 | Dean's List 2016-2018

TECHNICAL SKILLS
Languages: Python, JavaScript, TypeScript, Java, SQL
Frameworks: React, Node.js, Django, Flask, Spring Boot
Cloud & DevOps: AWS, Docker, Kubernetes, Jenkins, Git, CI/CD
Databases: PostgreSQL, MongoDB, Redis, MySQL
Tools: JIRA, Agile, Scrum, Unit Testing, REST APIs

CERTIFICATIONS
• AWS Certified Solutions Architect - Associate
• Certified Kubernetes Administrator (CKA)
"""

def test_analyzer():
    print("=" * 70)
    print("RESUME ANALYZER TEST")
    print("=" * 70)
    print()
    
    analyzer = get_analyzer()
    
    # Analyze the resume
    result = analyzer.analyze_resume(sample_resume)
    
    if result['success']:
        print(f"✅ ATS SCORE: {result['score']}%")
        print(f"📊 Status: {result['status'].upper()} - {result['statusMessage']}")
        print()
        
        # Show metrics breakdown
        print("📈 METRICS BREAKDOWN:")
        print("-" * 70)
        metrics = result['metrics']
        print(f"  • Word Count: {metrics['wordCount']}")
        print(f"  • Sections Found: {metrics['sectionsFound']}")
        print(f"  • Skills Found: {metrics['skillsFound']}")
        print(f"  • Action Verbs: {metrics['actionVerbs']}")
        print(f"  • Quantifiable Metrics: {metrics['quantifiableMetrics']}")
        print(f"  • Contact Info: {'✅ Complete' if metrics['contactInfoPresent'] else '❌ Missing'}")
        print()
        
        # Show insights
        if result['insights']:
            print("💡 WHAT'S GOOD:")
            print("-" * 70)
            for insight in result['insights']:
                print(f"  ✓ {insight}")
            print()
        
        # Show recommendations
        if result['recommendations']:
            print("🎯 RECOMMENDATIONS TO IMPROVE:")
            print("-" * 70)
            for i, rec in enumerate(result['recommendations'], 1):
                print(f"  {i}. {rec}")
            print()
        
        # Show extracted info
        if 'extractedInfo' in result:
            info = result['extractedInfo']
            if info.get('skills'):
                print("🔧 DETECTED SKILLS:")
                print("-" * 70)
                skills_str = ", ".join(info['skills'])
                print(f"  {skills_str}")
                print()
        
        print("=" * 70)
        print(f"FINAL SCORE: {result['score']}% - {result['status'].upper()}")
        print("=" * 70)
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    test_analyzer()
