from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile
from companies.models import Company
from internships.models import Internship
from applications.models import Application
from datetime import datetime, timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = 'Seed the database with mock data'

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        # ── Students ──
        students_data = [
            {"username": "ram_sharma", "email": "ram@example.com", "password": "student123", "bio": "BSc CSIT student passionate about web development.", "skills": "Python, Django, HTML, CSS, JavaScript", "education": "BSc CSIT, TU"},
            {"username": "sita_poudel", "email": "sita@example.com", "password": "student123", "bio": "Final year IT student looking for internship opportunities.", "skills": "Java, Spring Boot, MySQL, React", "education": "BE IT, PU"},
            {"username": "hari_gurung", "email": "hari@example.com", "password": "student123", "bio": "Self-taught developer with experience in building web apps.", "skills": "JavaScript, Node.js, MongoDB, Express", "education": "BCA, KU"},
            {"username": "gita_adhikari", "email": "gita@example.com", "password": "student123", "bio": "Aspiring data scientist with strong analytical skills.", "skills": "Python, Pandas, NumPy, Machine Learning", "education": "MSc Data Science, KU"},
            {"username": "anil_thapa", "email": "anil@example.com", "password": "student123", "bio": "Frontend enthusiast with an eye for design.", "skills": "HTML, CSS, Bootstrap, React, Figma", "education": "BIM, TU"},
        ]
        students = []
        for s in students_data:
            user, created = User.objects.get_or_create(username=s["username"], defaults={"email": s["email"]})
            user.set_password(s["password"])
            user.save()
            Profile.objects.get_or_create(user=user, defaults={"bio": s["bio"], "skills": s["skills"], "education": s["education"]})
            students.append(user)
            if created:
                self.stdout.write(f"  Created student: {s['username']}")

        # ── Companies ──
        companies_data = [
            {"username": "deerwalk", "email": "info@deerwalk.com", "password": "company123", "company_name": "DeerWalk", "description": "A leading IT company in Nepal specializing in software development, data analytics, and healthcare IT solutions."},
            {"username": "f1soft", "email": "info@f1soft.com", "password": "company123", "company_name": "F1Soft", "description": "Nepal's premier fintech company providing digital payment solutions and banking software."},
            {"username": "leapfrog", "email": "info@leapfrog.com", "password": "company123", "company_name": "Leapfrog", "description": "A global software engineering company with offices in Nepal, delivering high-quality products."},
            {"username": "cotiviti", "email": "info@cotiviti.com", "password": "company123", "company_name": "Cotiviti Nepal", "description": "A healthcare analytics company that uses data to improve healthcare quality and reduce costs."},
            {"username": "verisk", "email": "info@verisk.com", "password": "company123", "company_name": "Verisk Nepal", "description": "A data analytics provider serving insurance, healthcare, and financial markets worldwide."},
        ]
        companies = []
        for c in companies_data:
            user, created = User.objects.get_or_create(username=c["username"], defaults={"email": c["email"]})
            if created:
                user.set_password(c["password"])
                user.save()
                company = Company.objects.create(user=user, company_name=c["company_name"], description=c["description"], is_approved=True)
                companies.append(company)
                self.stdout.write(f"  Created company: {c['company_name']}")
            else:
                companies.append(Company.objects.get(user=user))

        # ── Internships ──
        internships_data = [
            {"company": 0, "title": "Python Django Developer Intern", "description": "Work on real-world projects using Django REST framework. You will build APIs, integrate databases, and collaborate with our backend team on production applications.", "location": "Kathmandu"},
            {"company": 0, "title": "React Frontend Intern", "description": "Join our frontend team to build responsive and performant web applications using React, Redux, and Tailwind CSS.", "location": "Lalitpur"},
            {"company": 1, "title": "Fintech Software Intern", "description": "Work on Nepal's leading payment gateway. Learn about secure transactions, banking APIs, and financial software development.", "location": "Kathmandu"},
            {"company": 1, "title": "Mobile App Developer Intern", "description": "Develop cross-platform mobile applications using Flutter. Work on apps used by millions of users across Nepal.", "location": "Kathmandu"},
            {"company": 2, "title": "Software Engineering Intern", "description": "Join our engineering team to build scalable microservices. Work with Go, Node.js, and cloud infrastructure.", "location": "Pokhara"},
            {"company": 2, "title": "Quality Assurance Intern", "description": "Learn test automation with Selenium and Cypress. Ensure product quality through manual and automated testing.", "location": "Pokhara"},
            {"company": 3, "title": "Data Science Intern", "description": "Analyze healthcare data, build predictive models, and derive insights using Python, SQL, and machine learning frameworks.", "location": "Kathmandu"},
            {"company": 3, "title": "Business Analyst Intern", "description": "Work with stakeholders to gather requirements, document processes, and help bridge the gap between business and technology.", "location": "Lalitpur"},
            {"company": 4, "title": "Full Stack Developer Intern", "description": "Build and maintain web applications using .NET and React. Work in an agile environment with experienced mentors.", "location": "Kathmandu"},
            {"company": 4, "title": "DevOps Engineer Intern", "description": "Learn CI/CD pipelines, Docker, Kubernetes, and cloud deployment. Help automate and streamline our infrastructure.", "location": "Kathmandu"},
        ]
        internships = []
        for i, data in enumerate(internships_data):
            days_ago = 30 - i * 2
            created_at = timezone.now() - timedelta(days=days_ago)
            internship = Internship.objects.create(
                company=companies[data["company"]],
                title=data["title"],
                description=data["description"],
                location=data["location"],
            )
            internship.created_at = created_at
            internship.save()
            internships.append(internship)
            self.stdout.write(f"  Created internship: {data['title']}")

        # ── Applications (some students apply to some internships) ──
        applications_data = [
            {"student": 0, "internship": 0, "status": "Accepted"},
            {"student": 0, "internship": 2, "status": "Pending"},
            {"student": 1, "internship": 1, "status": "Pending"},
            {"student": 1, "internship": 4, "status": "Rejected"},
            {"student": 2, "internship": 3, "status": "Accepted"},
            {"student": 2, "internship": 5, "status": "Pending"},
            {"student": 3, "internship": 6, "status": "Pending"},
            {"student": 3, "internship": 7, "status": "Pending"},
            {"student": 4, "internship": 8, "status": "Accepted"},
            {"student": 4, "internship": 9, "status": "Pending"},
            {"student": 0, "internship": 8, "status": "Pending"},
            {"student": 1, "internship": 6, "status": "Accepted"},
        ]
        for a in applications_data:
            app, created = Application.objects.get_or_create(
                student=students[a["student"]],
                internship=internships[a["internship"]],
                defaults={"status": a["status"]}
            )
            if created:
                self.stdout.write(f"  Created application: {students[a['student']].username} -> {internships[a['internship']].title}")

        self.stdout.write(self.style.SUCCESS(f"\nDone! Seeded:"))
        self.stdout.write(f"  - {len(students)} students")
        self.stdout.write(f"  - {len(companies)} companies (all pre-approved)")
        self.stdout.write(f"  - {len(internships)} internships")
        self.stdout.write(f"  - {Application.objects.count()} applications")
        self.stdout.write(f"\nStudent passwords: student123")
        self.stdout.write(f"Company passwords: company123")
        self.stdout.write(f"Admin password: admin123")
