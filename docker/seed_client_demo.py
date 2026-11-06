"""Sample data for a client walkthrough video. Local development only.

Every person, company and number here is made up. Safe to re-run: records that
already exist are skipped.

Run from the host:
  docker exec -w /home/frappe/frappe-bench/sites lms-frappe-1 \
    bash -lc '../env/bin/python /workspace/seed_client_demo.py'

Test logins it sets:
  priya.sharma@example.com / Demo-Instructor-123   (Course Creator only)
"""

import json
import random

import frappe
from frappe.utils import add_days, add_to_date, now_datetime, nowdate
from frappe.utils.password import update_password

SITE = "lms.localhost"
CURRENCY = "INR"
TIMEZONE = "Asia/Kolkata"
INSTRUCTOR_PASSWORD = "Demo-Instructor-123"

INSTRUCTORS = {
	"priya.sharma@example.com": ("Priya", "Sharma"),
	"rahul.verma@example.com": ("Rahul", "Verma"),
	"ananya.iyer@example.com": ("Ananya", "Iyer"),
	"vikram.singh@example.com": ("Vikram", "Singh"),
}

STUDENTS = {
	"aarav.mehta@example.com": ("Aarav", "Mehta"),
	"diya.kapoor@example.com": ("Diya", "Kapoor"),
	"kabir.nair@example.com": ("Kabir", "Nair"),
	"meera.joshi@example.com": ("Meera", "Joshi"),
	"rohan.gupta@example.com": ("Rohan", "Gupta"),
	"sara.khan@example.com": ("Sara", "Khan"),
	"arjun.reddy@example.com": ("Arjun", "Reddy"),
	"neha.patil@example.com": ("Neha", "Patil"),
	"ishaan.das@example.com": ("Ishaan", "Das"),
	"tanya.bose@example.com": ("Tanya", "Bose"),
	"dev.malhotra@example.com": ("Dev", "Malhotra"),
	"pooja.menon@example.com": ("Pooja", "Menon"),
}

# The student shown on camera. Created by the stock demo data.
MAIN_STUDENT = "john.doe@example.com"

COURSES = [
	{
		"title": "Python Programming for Beginners",
		"category": "Web Development",
		"instructor": "priya.sharma@example.com",
		"gradient": "Blue",
		"tags": "Python, Programming, Beginner",
		"featured": 1,
		"certificate": 1,
		"intro": "Write your first real programs in Python, with no coding experience needed.",
		"about": "Start from zero and learn to think like a programmer. By the end you will be able to read and write simple Python programs, work with data, and automate small everyday tasks.",
		"chapters": [
			(
				"Getting started",
				[
					(
						"Why learn Python?",
						"Python reads almost like plain English, which makes it one of the easiest languages to start with. It is used for websites, data analysis, automation and machine learning.",
						["Simple, readable syntax", "A huge library of free packages", "Strong demand from employers"],
					),
					(
						"Your first program",
						"Every programmer starts by making the computer say something. In Python, one line is enough: print('Hello, world!'). Run it and you have written your first program.",
						["Install Python from the official website", "Open a code editor", "Save your file with a .py extension"],
					),
				],
			),
			(
				"Core concepts",
				[
					(
						"Variables and data types",
						"A variable is a labelled box that holds a value. Python works out the type for you, whether that value is text, a whole number or a decimal.",
						["Strings hold text", "Integers hold whole numbers", "Booleans hold True or False"],
					),
					(
						"Decisions and loops",
						"Programs become useful when they can make choices and repeat work. Use if statements to decide what happens next, and for loops to repeat a step for every item in a list.",
						["if, elif and else choose a path", "for repeats over a list", "while repeats until a condition changes"],
					),
				],
			),
		],
		"quiz": {
			"title": "Python Basics Check",
			"questions": [
				("Which function displays text on the screen?", ["print()", "show()", "echo()", "write()"], 0),
				("What type of value is 'Hello'?", ["Integer", "Boolean", "String", "Float"], 2),
				("Which keyword repeats over a list?", ["if", "for", "def", "else"], 1),
				("What file extension do Python files use?", [".txt", ".java", ".py", ".html"], 2),
			],
		},
		"assignment": {
			"title": "Build a Tip Calculator",
			"question": "Write a short Python program that takes a bill amount and a tip percentage, then prints the total to pay. Paste your code below.",
			"answer": "bill = 1200\ntip = 10\nprint(bill + bill * tip / 100)",
		},
		"reviews": [
			(1.0, "Clear explanations. I wrote my first script within an hour."),
			(0.8, "Great pace for a complete beginner, and the assignment really helped."),
			(1.0, "Priya makes programming feel approachable."),
		],
	},
	{
		"title": "Digital Marketing Fundamentals",
		"category": "Business",
		"instructor": "rahul.verma@example.com",
		"gradient": "Orange",
		"tags": "Marketing, SEO, Social Media",
		"featured": 1,
		"price": 1999,
		"intro": "Plan, launch and measure marketing campaigns that bring in real customers.",
		"about": "A practical introduction to how businesses find customers online. You will learn how search, social media and email fit together, and how to tell which of your efforts are actually working.",
		"chapters": [
			(
				"Marketing foundations",
				[
					(
						"Know your customer",
						"Good marketing starts with one clear picture of who you are talking to. Describe your ideal customer, the problem they have, and where they spend time online.",
						["Age, location and occupation", "Goals and frustrations", "Favourite platforms"],
					),
					(
						"The marketing funnel",
						"Customers rarely buy the first time they hear about you. The funnel describes their journey from first noticing you to buying and recommending you to others.",
						["Awareness", "Consideration", "Purchase", "Loyalty"],
					),
				],
			),
			(
				"Reaching your audience",
				[
					(
						"Search engine optimisation",
						"SEO helps people find you when they are already looking for what you offer. Focus on useful content, the words your customers actually use, and a fast website.",
						["Research keywords", "Write helpful pages", "Earn links from trusted sites"],
					),
					(
						"Social media that works",
						"You do not need to be everywhere. Pick the one or two platforms your customers use most, post consistently, and reply to people who engage with you.",
						["Choose platforms carefully", "Plan a weekly calendar", "Track what gets a response"],
					),
				],
			),
		],
		"quiz": {
			"title": "Marketing Essentials Quiz",
			"questions": [
				("What does SEO stand for?", ["Search Engine Optimisation", "Social Engagement Online", "Sales Enablement Office", "Site Editing Options"], 0),
				("Which stage comes first in the funnel?", ["Purchase", "Loyalty", "Awareness", "Consideration"], 2),
				("How many social platforms should a small business start with?", ["All of them", "One or two", "At least ten", "None"], 1),
			],
		},
		"reviews": [
			(1.0, "Practical and to the point. I used the funnel with my own shop straight away."),
			(0.8, "Good overview of the essentials, especially the SEO lesson."),
		],
	},
	{
		"title": "UI/UX Design Essentials",
		"category": "Design",
		"instructor": "ananya.iyer@example.com",
		"gradient": "Violet",
		"tags": "Design, UX, Figma",
		"price": 2499,
		"intro": "Design simple, attractive screens that people find easy to use.",
		"about": "Learn how designers turn an idea into a screen people enjoy using. This course covers user research, layout, colour and typography, and how to test your designs before anything gets built.",
		"chapters": [
			(
				"Thinking like a designer",
				[
					(
						"UI versus UX",
						"UX is how a product works and feels. UI is how it looks. A beautiful screen that confuses people has failed, and so has a logical one that nobody wants to look at.",
						["UX covers journeys and structure", "UI covers visual detail", "Great products need both"],
					),
					(
						"Understanding users",
						"Designers make fewer mistakes when they talk to real people. Five short conversations usually reveal the biggest problems with a product.",
						["Ask open questions", "Watch what people do", "Write down what surprises you"],
					),
				],
			),
			(
				"Visual design basics",
				[
					(
						"Layout and hierarchy",
						"Hierarchy tells people what to look at first. Use size, spacing and contrast to make the most important thing on each screen obvious.",
						["One main action per screen", "Consistent spacing", "Group related items"],
					),
					(
						"Colour and typography",
						"Keep it simple: one or two typefaces and a small colour palette. Always check that your text has enough contrast to be read comfortably.",
						["Limit your palette", "Use at most two typefaces", "Check text contrast"],
					),
				],
			),
		],
		"quiz": {
			"title": "Design Principles Quiz",
			"questions": [
				("What does UX mainly describe?", ["Screen colours", "How a product works and feels", "Programming languages", "Server speed"], 1),
				("How many typefaces are usually enough?", ["One or two", "Five", "Eight", "Ten"], 0),
				("What does visual hierarchy do?", ["Compresses images", "Shows what to look at first", "Adds animation", "Stores user data"], 1),
			],
		},
		"assignment": {
			"title": "Redesign a Login Screen",
			"question": "Pick a login screen from an app you use. Describe three problems with it and how you would improve each one.",
			"answer": "The error message is hard to notice, so I would place it next to the field. The button has low contrast, so I would use a stronger colour. The forgot password link is too small, so I would make it larger.",
		},
		"reviews": [
			(1.0, "I finally understand why some apps just feel right."),
			(0.8, "Lovely examples, and the login redesign assignment was fun."),
		],
	},
	{
		"title": "Personal Finance Made Simple",
		"category": "Finance",
		"instructor": "vikram.singh@example.com",
		"gradient": "Green",
		"tags": "Money, Budgeting, Savings",
		"certificate": 1,
		"intro": "Take control of your money with a simple budget and clear saving habits.",
		"about": "Build confidence with everyday money decisions. You will create a budget that you can stick to, start an emergency fund, and learn the basic ideas behind saving for the long term. General education only, not financial advice.",
		"chapters": [
			(
				"Managing your money",
				[
					(
						"Building a budget",
						"A budget is simply a plan for your money. One popular starting point is the 50/30/20 rule, which splits your income between needs, wants and savings.",
						["50% for needs", "30% for wants", "20% for savings"],
					),
					(
						"Your emergency fund",
						"An emergency fund stops an unexpected bill from turning into debt. A common goal is to set aside three to six months of essential expenses.",
						["Start small and build up", "Keep it easy to access", "Use it for real emergencies only"],
					),
				],
			),
			(
				"Planning ahead",
				[
					(
						"Good debt and bad debt",
						"Not all borrowing is equal. Understand the interest you pay, and clear expensive debts such as unpaid credit card balances first.",
						["Compare interest rates", "Pay more than the minimum", "Avoid borrowing for wants"],
					),
					(
						"The power of compounding",
						"When your savings earn returns, those returns can earn returns too. This is why starting early matters more than starting with a large amount.",
						["Start as early as you can", "Save regularly", "Give your money time to grow"],
					),
				],
			),
		],
		"quiz": {
			"title": "Money Basics Quiz",
			"questions": [
				("In the 50/30/20 rule, what is the 20% for?", ["Rent", "Savings", "Entertainment", "Food"], 1),
				("What is a common emergency fund goal?", ["One week of expenses", "3 to 6 months of expenses", "Five years of income", "No savings at all"], 1),
				("What makes compounding more powerful?", ["Time", "Spending more", "Skipping months", "Higher fees"], 0),
			],
		},
		"reviews": [
			(1.0, "Simple and free of jargon. I set up my first budget the same day."),
			(1.0, "This should be taught in every school."),
			(0.8, "Very useful, particularly the part on emergency funds."),
		],
	},
	{
		"title": "Communication Skills for the Workplace",
		"category": "Personal Development",
		"instructor": "ananya.iyer@example.com",
		"gradient": "Pink",
		"tags": "Communication, Soft Skills, Career",
		"certificate": 1,
		"intro": "Speak, write and listen with confidence at work.",
		"about": "Clear communication helps at every stage of a career. Practise writing better emails, giving useful feedback, and presenting your ideas without nerves getting in the way.",
		"chapters": [
			(
				"Everyday communication",
				[
					(
						"Active listening",
						"Listening well is a skill you can practise. Give the speaker your full attention, ask questions, and repeat back what you heard to confirm you understood.",
						["Put away distractions", "Ask follow-up questions", "Summarise what you heard"],
					),
					(
						"Emails people actually read",
						"Lead with what you need and by when. Keep paragraphs short, use a clear subject line, and read the email once more before pressing send.",
						["A specific subject line", "The request comes first", "One topic per email"],
					),
				],
			),
			(
				"Speaking with confidence",
				[
					(
						"Giving useful feedback",
						"Good feedback is specific and focused on the work rather than the person. Describe what you saw, the effect it had, and what you suggest instead.",
						["Be specific", "Explain the impact", "Offer a next step"],
					),
					(
						"Presenting your ideas",
						"Structure beats charisma. Tell your audience what matters, give them your evidence, and end by saying exactly what you want them to do.",
						["Open with the main point", "Use fewer slides", "Close with a clear ask"],
					),
				],
			),
		],
		"quiz": {
			"title": "Communication Skills Quiz",
			"questions": [
				("What should come first in a work email?", ["Your job history", "What you need and by when", "A long greeting", "A joke"], 1),
				("Good feedback focuses on what?", ["The person's character", "The work and its impact", "Past mistakes", "Rumours"], 1),
				("What is a good habit for active listening?", ["Interrupting early", "Checking your phone", "Summarising what you heard", "Planning your reply"], 2),
			],
		},
		"reviews": [
			(0.8, "Short, useful lessons that I could apply at work the next day."),
			(1.0, "The feedback framework made a difficult conversation much easier."),
		],
	},
	{
		"title": "Full Stack Web Development Bootcamp",
		"category": "Web Development",
		"instructor": "priya.sharma@example.com",
		"gradient": "Teal",
		"tags": "JavaScript, Web, Career",
		"upcoming": 1,
		"price": 4999,
		"intro": "Coming soon: build and launch complete web applications from scratch.",
		"about": "A hands-on bootcamp that takes you from your first web page to a working application with a database and user accounts. Register your interest to hear when enrolment opens.",
		"chapters": [],
		"reviews": [],
	},
]

BATCHES = [
	{
		"title": "Python Live Cohort: January",
		"course": "Python Programming for Beginners",
		"instructor": "priya.sharma@example.com",
		"starts_in": 21,
		"weeks": 6,
		"time": ("18:00:00", "19:30:00"),
		"seats": 30,
		"intro": "Learn Python together over six weeks of live evening classes.",
		"details": "<p>Join a small group and learn Python with a live instructor. Includes weekly classes, assignments with feedback, and a certificate on completion.</p>",
		"members": 6,
	},
	{
		"title": "Digital Marketing Weekend Workshop",
		"course": "Digital Marketing Fundamentals",
		"instructor": "rahul.verma@example.com",
		"starts_in": 10,
		"weeks": 2,
		"time": ("10:00:00", "13:00:00"),
		"seats": 20,
		"price": 3499,
		"intro": "Two intensive weekends to build a marketing plan for your own business.",
		"details": "<p>Bring your business idea and leave with a complete marketing plan, reviewed by your instructor and your fellow participants.</p>",
		"members": 4,
	},
	{
		"title": "UI/UX Design Studio",
		"course": "UI/UX Design Essentials",
		"instructor": "ananya.iyer@example.com",
		"starts_in": -14,
		"weeks": 8,
		"time": ("17:00:00", "18:30:00"),
		"seats": 15,
		"intro": "A running studio where you design a real product with weekly critiques.",
		"details": "<p>Work on a real product brief with weekly design critiques from your instructor and peers. This batch is already under way.</p>",
		"members": 5,
	},
]

JOBS = [
	("Junior Python Developer", "Bengaluru", "Full Time", "Hybrid", "BrightPath Software", "Build and maintain internal tools with a small, supportive engineering team. A good first role for recent learners."),
	("Digital Marketing Executive", "Mumbai", "Full Time", "On-site", "Nimbus Retail", "Run social media and email campaigns for a growing retail brand, and report on the results every month."),
	("UI/UX Design Intern", "Remote", "Part Time", "Remote", "Pixel Lane Studio", "Help designers with research, wireframes and prototypes in a six-month paid internship."),
	("Freelance Content Writer", "Pune", "Freelance", "Remote", "Wordsmith Media", "Write clear, well-researched articles on personal finance and careers for an online publication."),
]

PROGRAM = {
	"title": "Career Starter Program",
	"courses": ["Python Programming for Beginners", "Communication Skills for the Workplace", "Personal Finance Made Simple"],
	"author": "priya.sharma@example.com",
}


def main():
	# Keeps made-up activity out of product telemetry and stops any emails going out.
	frappe.flags.in_lms_demo = True
	frappe.flags.mute_emails = True
	random.seed(42)

	ensure_country_and_currency()
	make_users()
	courses = {spec["title"]: make_course(spec) for spec in COURSES}
	enroll_learners(courses)
	make_batches(courses)
	make_program()
	make_jobs()
	backdate_activity()

	from lms.lms.doctype.lms_course.lms_course import update_course_statistics

	update_course_statistics()
	frappe.db.commit()
	print_summary()


def ensure_country_and_currency():
	if not frappe.db.exists("Currency", CURRENCY) or not frappe.db.exists("Country", "India"):
		from frappe.utils.install import import_country_and_currency

		import_country_and_currency()
	frappe.db.set_value("Currency", CURRENCY, "enabled", 1)


def make_users():
	from lms.lms.utils import create_user

	for email, (first, last) in INSTRUCTORS.items():
		create_user(email, first, last, f"{first} {last}", roles=["Course Creator"], ignore_permissions=True)
	for email, (first, last) in STUDENTS.items():
		create_user(email, first, last, f"{first} {last}", ignore_permissions=True)
	update_password("priya.sharma@example.com", INSTRUCTOR_PASSWORD)


def blocks_for(text, points):
	return json.dumps(
		{
			"time": 1770118649591,
			"blocks": [
				{"id": frappe.generate_hash(length=10), "type": "paragraph", "data": {"text": text}},
				{
					"id": frappe.generate_hash(length=10),
					"type": "list",
					"data": {
						"style": "unordered",
						"items": [{"content": point, "items": []} for point in points],
					},
				},
			],
			"version": "2.29.0",
		}
	)


def block_for(block_type, field, value):
	return json.dumps(
		{
			"time": 1770118649591,
			"blocks": [
				{"id": frappe.generate_hash(length=10), "type": block_type, "data": {field: value}}
			],
			"version": "2.29.0",
		}
	)


def make_course(spec):
	from lms.demo.demo_data import create_lesson, get_chapter, prepare_chapter

	existing = frappe.db.exists("LMS Course", {"title": spec["title"]})
	if existing:
		return frappe.get_doc("LMS Course", existing)

	course = frappe.new_doc("LMS Course")
	course.update(
		{
			"title": spec["title"],
			"category": spec["category"],
			"tags": spec["tags"],
			"short_introduction": spec["intro"],
			"description": f"<p>{spec['about']}</p>",
			"card_gradient": spec["gradient"],
			"instructors": [{"instructor": spec["instructor"]}],
			"published": 1,
			"published_on": add_days(nowdate(), -90),
			"featured": spec.get("featured", 0),
			"upcoming": spec.get("upcoming", 0),
			"enable_certification": spec.get("certificate", 0),
		}
	)
	if spec.get("price"):
		course.update({"paid_course": 1, "course_price": spec["price"], "currency": CURRENCY})
	course.save()

	for chapter_title, lessons in spec["chapters"]:
		prepare_chapter(course, chapter_title)
		chapter = get_chapter(course, chapter_title)
		for title, text, points in lessons:
			create_lesson(course, chapter, title, blocks_for(text, points))

	if spec.get("quiz") or spec.get("assignment"):
		prepare_chapter(course, "Test your knowledge")
		chapter = get_chapter(course, "Test your knowledge")
		if spec.get("quiz"):
			quiz = make_quiz(spec["quiz"])
			create_lesson(course, chapter, "Final quiz", block_for("quiz", "quiz", quiz.name))
		if spec.get("assignment"):
			assignment = make_assignment(spec["assignment"])
			create_lesson(
				course, chapter, "Practical assignment", block_for("assignment", "assignment", assignment.name)
			)
	course.reload()
	return course


def make_quiz(spec):
	existing = frappe.db.exists("LMS Quiz", {"title": spec["title"]})
	if existing:
		return frappe.get_doc("LMS Quiz", existing)

	marks = 5
	quiz = frappe.new_doc("LMS Quiz")
	quiz.update(
		{
			"title": spec["title"],
			"passing_percentage": 60,
			"total_marks": marks * len(spec["questions"]),
			"show_answers": 1,
		}
	)
	for text, options, correct in spec["questions"]:
		question = frappe.new_doc("LMS Question")
		question.update({"question": text, "type": "Choices"})
		for index, option in enumerate(options, start=1):
			question.set(f"option_{index}", option)
			question.set(f"is_correct_{index}", int(index - 1 == correct))
		question.save()
		quiz.append("questions", {"question": question.name, "marks": marks})
	quiz.save()
	return quiz


def make_assignment(spec):
	existing = frappe.db.exists("LMS Assignment", {"title": spec["title"]})
	if existing:
		return frappe.get_doc("LMS Assignment", existing)

	assignment = frappe.new_doc("LMS Assignment")
	assignment.update(
		{
			"title": spec["title"],
			"question": f"<p>{spec['question']}</p>",
			"type": "Text",
		}
	)
	assignment.save()
	return assignment


def enroll(member, course, paid=False):
	filters = {"member": member, "course": course.name}
	if frappe.db.exists("LMS Enrollment", filters):
		return

	enrollment = frappe.new_doc("LMS Enrollment")
	enrollment.update({"member": member, "course": course.name})
	if paid:
		enrollment.payment = record_payment(member, "LMS Course", course.name, course.course_price)
	enrollment.save()


def record_payment(member, doctype, docname, amount):
	"""A sample payment marked as received. No money or gateway is involved."""
	payment = frappe.get_doc(
		{
			"doctype": "LMS Payment",
			"member": member,
			"billing_name": frappe.db.get_value("User", member, "full_name"),
			"amount": amount,
			"currency": CURRENCY,
			"payment_for_document_type": doctype,
			"payment_for_document": docname,
			"payment_received": 1,
		}
	)
	payment.flags.recorded_by_staff = True
	payment.insert(ignore_permissions=True)
	return payment.name


def enroll_learners(courses):
	from lms.demo.demo_data import create_progress

	students = list(STUDENTS)
	for spec in COURSES:
		if not spec["chapters"]:
			continue

		course = courses[spec["title"]]
		total = frappe.db.count("Course Lesson", {"course": course.name})
		learners = random.sample(students, k=random.randint(6, len(students)))
		for index, member in enumerate(learners):
			enroll(member, course, paid=bool(spec.get("price")))
			# A spread of progress, with the first learners finishing the course.
			lessons = total if index < 3 else random.randint(0, total - 1)
			if lessons:
				create_progress(course, frappe._dict(name=member), lessons)
			if lessons == total:
				issue_certificate(member, course)
				submit_work(member, spec, course)
			elif lessons:
				submit_work(member, spec, course, passed=index % 2 == 0)

		add_reviews(spec, course, learners)

	# The student on camera: finished one course, midway through two, one paid.
	journey = [
		("Python Programming for Beginners", None),
		("Personal Finance Made Simple", 3),
		("Digital Marketing Fundamentals", 2),
	]
	for title, lessons in journey:
		spec = next(item for item in COURSES if item["title"] == title)
		course = courses[title]
		enroll(MAIN_STUDENT, course, paid=bool(spec.get("price")))
		create_progress(course, frappe._dict(name=MAIN_STUDENT), lessons)
		if lessons is None:
			issue_certificate(MAIN_STUDENT, course)
			submit_work(MAIN_STUDENT, spec, course)


def issue_certificate(member, course):
	from lms.lms.doctype.lms_certificate.lms_certificate import get_default_certificate_template

	if not course.enable_certification:
		return
	if frappe.db.exists("LMS Certificate", {"member": member, "course": course.name}):
		return

	frappe.get_doc(
		{
			"doctype": "LMS Certificate",
			"member": member,
			"course": course.name,
			"issue_date": add_days(nowdate(), -random.randint(1, 30)),
			"template": get_default_certificate_template(),
			"published": 1,
		}
	).insert(ignore_permissions=True)


def submit_work(member, spec, course, passed=True):
	if spec.get("quiz"):
		submit_quiz(member, spec, course, passed)
	if spec.get("assignment") and passed:
		submit_assignment(member, spec, course)


def submit_quiz(member, spec, course, passed):
	quiz_name = frappe.db.get_value("LMS Quiz", {"title": spec["quiz"]["title"]})
	if frappe.db.exists("LMS Quiz Submission", {"quiz": quiz_name, "member": member}):
		return

	rows = frappe.get_all(
		"LMS Quiz Question", {"parent": quiz_name, "parenttype": "LMS Quiz"}, ["question", "marks"], order_by="idx"
	)
	submission = frappe.new_doc("LMS Quiz Submission")
	submission.update(
		{
			"quiz": quiz_name,
			"member": member,
			"course": course.name,
			"score": 0,
			"score_out_of": sum(row.marks for row in rows),
			"percentage": 0,
			"passing_percentage": 60,
		}
	)
	for index, row in enumerate(rows):
		_text, options, correct = spec["quiz"]["questions"][index]
		right = passed or index == 0
		submission.append(
			"result",
			{
				"question_name": row.question,
				"question": _text,
				"answer": options[correct if right else (correct + 1) % len(options)],
				"is_correct": int(right),
				"marks": row.marks if right else 0,
				"marks_out_of": row.marks,
			},
		)
	submission.insert(ignore_permissions=True)


def submit_assignment(member, spec, course):
	assignment = frappe.db.get_value("LMS Assignment", {"title": spec["assignment"]["title"]})
	if frappe.db.exists("LMS Assignment Submission", {"assignment": assignment, "member": member}):
		return

	lesson = frappe.db.get_value("Course Lesson", {"course": course.name, "title": "Practical assignment"})
	graded = random.random() < 0.6
	frappe.get_doc(
		{
			"doctype": "LMS Assignment Submission",
			"assignment": assignment,
			"member": member,
			"lesson": lesson,
			"course": course.name,
			"answer": f"<p>{spec['assignment']['answer']}</p>",
			"status": "Pass" if graded else "Not Graded",
			"evaluator": spec["instructor"] if graded else None,
			"comments": "<p>Well done, this meets the brief.</p>" if graded else None,
		}
	).insert(ignore_permissions=True)


def add_reviews(spec, course, learners):
	for member, (rating, text) in zip(learners, spec["reviews"], strict=False):
		if frappe.db.exists("LMS Course Review", {"course": course.name, "owner": member}):
			continue
		# The controller ties a review to its owner, so write it as that learner.
		frappe.session.user = member
		try:
			review = frappe.new_doc("LMS Course Review")
			review.update({"course": course.name, "rating": rating, "review": text})
			review.insert(ignore_permissions=True)
		finally:
			frappe.session.user = "Administrator"


def make_batches(courses):
	students = list(STUDENTS)
	for spec in BATCHES:
		existing = frappe.db.exists("LMS Batch", {"title": spec["title"]})
		if existing:
			continue

		start = add_days(nowdate(), spec["starts_in"])
		batch = frappe.new_doc("LMS Batch")
		batch.update(
			{
				"title": spec["title"],
				"description": spec["intro"],
				"batch_details": spec["details"],
				"start_date": start,
				"end_date": add_days(start, spec["weeks"] * 7),
				"start_time": spec["time"][0],
				"end_time": spec["time"][1],
				"timezone": TIMEZONE,
				"seat_count": spec["seats"],
				"medium": "Online",
				"category": frappe.db.get_value("LMS Course", courses[spec["course"]].name, "category"),
				"published": 1,
				"allow_self_enrollment": 1,
				"instructors": [{"instructor": spec["instructor"]}],
				"courses": [{"course": courses[spec["course"]].name}],
			}
		)
		if spec.get("price"):
			batch.update({"paid_batch": 1, "amount": spec["price"], "currency": CURRENCY})
		batch.save()

		for member in random.sample(students, k=spec["members"]):
			enrollment = frappe.new_doc("LMS Batch Enrollment")
			enrollment.update({"member": member, "batch": batch.name})
			if spec.get("price"):
				enrollment.payment = record_payment(member, "LMS Batch", batch.name, spec["price"])
			enrollment.insert(ignore_permissions=True)


def make_program():
	if frappe.db.exists("LMS Program", PROGRAM["title"]):
		return

	program = frappe.new_doc("LMS Program")
	course_names = [frappe.db.get_value("LMS Course", {"title": title}) for title in PROGRAM["courses"]]
	program.update(
		{
			"title": PROGRAM["title"],
			"published": 1,
			"enforce_course_order": 1,
			"authors": [{"author": PROGRAM["author"]}],
			"program_courses": [{"course": name} for name in course_names],
			"program_members": [{"member": MAIN_STUDENT}]
			+ [{"member": member} for member in list(STUDENTS)[:5]],
		}
	)
	program.save()


def make_jobs():
	for title, location, job_type, mode, company, description in JOBS:
		if frappe.db.exists("Job Opportunity", {"job_title": title, "company_name": company}):
			continue
		frappe.get_doc(
			{
				"doctype": "Job Opportunity",
				"job_title": title,
				"location": location,
				"country": "India",
				"type": job_type,
				"work_mode": mode,
				"status": "Open",
				"company_name": company,
				"company_website": "https://example.com",
				"company_email_address": "careers@example.com",
				"company_logo": "/assets/lms/images/lms-logo.png",
				"description": f"<p>{description}</p>",
			}
		).insert(ignore_permissions=True)


def backdate_activity():
	"""Spread sign-ups and enrolments over 90 days so the Statistics charts have a shape."""
	for doctype, filters in (
		("LMS Enrollment", {"member": ("in", list(STUDENTS) + [MAIN_STUDENT])}),
		("User", {"name": ("in", list(STUDENTS) + list(INSTRUCTORS))}),
	):
		for name in frappe.get_all(doctype, filters=filters, pluck="name"):
			moment = add_to_date(now_datetime(), days=-random.randint(1, 90))
			frappe.db.set_value(doctype, name, "creation", moment, update_modified=False)


def print_summary():
	for doctype in (
		"User",
		"LMS Course",
		"Course Lesson",
		"LMS Enrollment",
		"LMS Course Review",
		"LMS Quiz",
		"LMS Quiz Submission",
		"LMS Assignment",
		"LMS Assignment Submission",
		"LMS Certificate",
		"LMS Batch",
		"LMS Batch Enrollment",
		"LMS Program",
		"LMS Payment",
		"Job Opportunity",
	):
		print(f"{doctype}: {frappe.db.count(doctype)}")
	print("SEED_DONE")


if __name__ == "__main__":
	frappe.init(site=SITE, sites_path=".")
	frappe.connect()
	frappe.set_user("Administrator")
	try:
		main()
	except Exception:
		frappe.db.rollback()
		raise
	finally:
		frappe.destroy()
