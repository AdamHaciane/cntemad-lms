"""
API endpoints for quiz operations.

Quiz submission and EC validation.

Usage:
    GET  /api/method/cntemad_lms.api.quiz.get_quiz
    POST /api/method/cntemad_lms.api.quiz.submit_quiz
"""

import frappe
from frappe import _
from frappe.utils import now_datetime, cint
import json


@frappe.whitelist()
def get_quiz(ec_id: str) -> dict:
    """
    Get quiz data for an EC.

    Args:
        ec_id: EC identifier

    Returns:
        dict: {
            ec: EC details,
            quiz: Quiz settings,
            questions: List of questions (without correct answers)
        }
    """
    # Verify EC exists
    if not frappe.db.exists("CNTEMAD EC", ec_id):
        frappe.throw(_("EC non trouvé"), frappe.DoesNotExistError)

    ec = frappe.get_doc("CNTEMAD EC", ec_id)

    # Check if student has paid
    student_id = frappe.db.get_value(
        "CNTEMAD Student", {"user": frappe.session.user}, "name"
    )

    is_paid = False
    if student_id:
        is_paid = frappe.db.exists(
            "CNTEMAD Enrollment",
            {"student": student_id, "ec": ec_id, "status": ["in", ["Paid", "In Progress", "Validated"]]}
        )

    ec_data = {
        "name": ec.name,
        "title": ec.title,
        "is_paid": is_paid,
    }

    if not is_paid:
        return {"ec": ec_data, "quiz": None, "questions": []}

    # Get quiz from LMS or custom doctype
    quiz_data = get_quiz_for_ec(ec)

    if not quiz_data:
        return {"ec": ec_data, "quiz": None, "questions": []}

    # Get questions (without correct answers for security)
    questions = get_quiz_questions(quiz_data.get("name"))

    return {
        "ec": ec_data,
        "quiz": {
            "name": quiz_data.get("name"),
            "title": quiz_data.get("title") or f"Quiz - {ec.title}",
            "passing_score": quiz_data.get("passing_score", 70),
            "time_limit": quiz_data.get("time_limit", 0),  # in minutes
            "max_attempts": quiz_data.get("max_attempts", 3),
            "show_immediate_feedback": quiz_data.get("show_immediate_feedback", False),
        },
        "questions": questions,
    }


def get_quiz_for_ec(ec) -> dict:
    """Get quiz configuration for an EC."""
    # Try to get LMS Quiz linked to EC
    quiz_id = ec.get("quiz") or ec.get("quiz_id")

    if quiz_id and frappe.db.exists("LMS Quiz", quiz_id):
        quiz = frappe.get_doc("LMS Quiz", quiz_id)
        return {
            "name": quiz.name,
            "title": quiz.title,
            "passing_score": quiz.passing_percentage or 70,
            "time_limit": quiz.max_time or 0,
            "max_attempts": quiz.max_attempts or 3,
            "show_immediate_feedback": quiz.show_answers_after_submission or False,
        }

    # Fallback: Create default quiz settings
    return {
        "name": f"quiz-{ec.name}",
        "title": f"Quiz - {ec.title}",
        "passing_score": 70,
        "time_limit": 30,  # 30 minutes default
        "max_attempts": 3,
        "show_immediate_feedback": False,
    }


def get_quiz_questions(quiz_id: str) -> list:
    """
    Get quiz questions without exposing correct answers.

    Returns list of questions with options.
    """
    questions = []

    # Try LMS Quiz questions
    if frappe.db.exists("LMS Quiz", quiz_id):
        quiz_questions = frappe.get_all(
            "LMS Quiz Question",
            filters={"parent": quiz_id},
            fields=["name", "question", "type", "options", "idx"],
            order_by="idx",
        )

        for q in quiz_questions:
            options = []
            if q.options:
                # Parse options (stored as JSON or newline-separated)
                try:
                    options = json.loads(q.options)
                except:
                    options = [opt.strip() for opt in q.options.split("\n") if opt.strip()]

            questions.append({
                "id": q.name,
                "text": q.question,
                "type": "multiple" if q.type == "Multiple Choice" else "single",
                "options": options,
            })

    # Fallback: Sample questions for demo
    if not questions:
        questions = [
            {
                "id": "q1",
                "text": "Question exemple 1 - Sélectionnez la bonne réponse",
                "type": "single",
                "options": ["Option A", "Option B", "Option C", "Option D"],
            },
            {
                "id": "q2",
                "text": "Question exemple 2 - Plusieurs réponses possibles",
                "type": "multiple",
                "options": ["Réponse 1", "Réponse 2", "Réponse 3", "Réponse 4"],
            },
        ]

    return questions


@frappe.whitelist()
def submit_quiz(ec_id: str, quiz_id: str = None, answers: str = None, time_spent: int = None) -> dict:
    """
    Submit quiz answers and calculate score.

    Args:
        ec_id: EC identifier
        quiz_id: Quiz identifier
        answers: JSON string of answers [{question_id, answer}]
        time_spent: Time spent in seconds

    Returns:
        dict: {
            score: Number of correct answers,
            total: Total questions,
            percent: Score percentage,
            passed: Whether passed,
            can_retry: Can retry quiz,
            attempts_remaining: Remaining attempts
        }
    """
    # Verify student
    student_id = frappe.db.get_value(
        "CNTEMAD Student", {"user": frappe.session.user}, "name"
    )

    if not student_id:
        frappe.throw(_("Profil étudiant non trouvé"))

    # Verify EC
    if not frappe.db.exists("CNTEMAD EC", ec_id):
        frappe.throw(_("EC non trouvé"))

    # Verify enrollment
    enrollment = frappe.db.get_value(
        "CNTEMAD Enrollment",
        {"student": student_id, "ec": ec_id},
        ["name", "status", "quiz_attempts"],
        as_dict=True
    )

    if not enrollment:
        frappe.throw(_("Vous n'êtes pas inscrit à cet EC"))

    if enrollment.status == "Validated":
        frappe.throw(_("Cet EC est déjà validé"))

    # Check max attempts
    max_attempts = 3
    current_attempts = enrollment.quiz_attempts or 0

    if current_attempts >= max_attempts:
        frappe.throw(_("Vous avez atteint le nombre maximum de tentatives"))

    # Parse answers
    try:
        answer_list = json.loads(answers) if answers else []
    except:
        answer_list = []

    # Calculate score
    score, total, details = calculate_quiz_score(ec_id, quiz_id, answer_list)

    percent = round((score / total) * 100) if total > 0 else 0
    passing_score = 70  # Default, could come from quiz settings

    if quiz_id and frappe.db.exists("LMS Quiz", quiz_id):
        passing_score = frappe.db.get_value("LMS Quiz", quiz_id, "passing_percentage") or 70

    passed = percent >= passing_score

    # Update enrollment
    new_attempts = current_attempts + 1

    if passed:
        frappe.db.set_value("CNTEMAD Enrollment", enrollment.name, {
            "status": "Validated",
            "validation_date": now_datetime(),
            "quiz_score": percent,
            "quiz_attempts": new_attempts,
        })
    else:
        frappe.db.set_value("CNTEMAD Enrollment", enrollment.name, {
            "status": "In Progress",
            "quiz_score": max(enrollment.get("quiz_score") or 0, percent),
            "quiz_attempts": new_attempts,
        })

    frappe.db.commit()

    # Log the attempt
    log_quiz_attempt(student_id, ec_id, quiz_id, score, total, percent, passed, time_spent)

    return {
        "score": score,
        "total": total,
        "percent": percent,
        "passed": passed,
        "can_retry": not passed and new_attempts < max_attempts,
        "attempts_remaining": max_attempts - new_attempts if not passed else 0,
        "correct_answers": details if passed else None,  # Only show if passed
    }


def calculate_quiz_score(ec_id: str, quiz_id: str, answers: list) -> tuple:
    """
    Calculate quiz score by comparing answers with correct ones.

    Returns: (score, total, details)
    """
    correct_count = 0
    total = 0
    details = []

    # Get correct answers from quiz
    correct_answers = get_correct_answers(quiz_id)

    for answer_item in answers:
        question_id = answer_item.get("question_id")
        user_answer = answer_item.get("answer", [])

        if not isinstance(user_answer, list):
            user_answer = [user_answer]

        correct = correct_answers.get(question_id, [])

        if not isinstance(correct, list):
            correct = [correct]

        total += 1

        # Check if answers match
        is_correct = (
            len(user_answer) == len(correct) and
            all(a in correct for a in user_answer)
        )

        if is_correct:
            correct_count += 1

        details.append({
            "question_id": question_id,
            "user_answer": user_answer,
            "correct_answer": correct,
            "is_correct": is_correct,
        })

    # If no answers submitted, use total questions count
    if total == 0:
        total = len(correct_answers) or 1

    return correct_count, total, details


def get_correct_answers(quiz_id: str) -> dict:
    """
    Get correct answers for a quiz.

    Returns dict of {question_id: correct_answer_index(es)}
    """
    correct = {}

    if quiz_id and frappe.db.exists("LMS Quiz", quiz_id):
        questions = frappe.get_all(
            "LMS Quiz Question",
            filters={"parent": quiz_id},
            fields=["name", "type", "options", "correct_options"],
        )

        for q in questions:
            if q.correct_options:
                try:
                    # correct_options stored as JSON array of indices
                    correct[q.name] = json.loads(q.correct_options)
                except:
                    # Or as comma-separated indices
                    correct[q.name] = [int(i.strip()) for i in q.correct_options.split(",") if i.strip().isdigit()]
            else:
                # Default: first option is correct (for demo)
                correct[q.name] = [0]

    # Fallback for demo questions
    if not correct:
        correct = {
            "q1": [0],  # First option correct
            "q2": [0, 2],  # First and third options correct
        }

    return correct


def log_quiz_attempt(
    student_id: str,
    ec_id: str,
    quiz_id: str,
    score: int,
    total: int,
    percent: int,
    passed: bool,
    time_spent: int = None
):
    """Log quiz attempt for analytics."""
    try:
        frappe.get_doc({
            "doctype": "Comment",
            "comment_type": "Info",
            "reference_doctype": "CNTEMAD Enrollment",
            "reference_name": f"{student_id}-{ec_id}",
            "content": f"Quiz attempt: {score}/{total} ({percent}%) - {'Passed' if passed else 'Failed'}",
        }).insert(ignore_permissions=True)
    except:
        pass


@frappe.whitelist()
def get_quiz_history(ec_id: str) -> dict:
    """
    Get quiz attempt history for an EC.

    Returns:
        dict: { attempts: [], best_score: int }
    """
    student_id = frappe.db.get_value(
        "CNTEMAD Student", {"user": frappe.session.user}, "name"
    )

    if not student_id:
        return {"attempts": [], "best_score": 0}

    enrollment = frappe.db.get_value(
        "CNTEMAD Enrollment",
        {"student": student_id, "ec": ec_id},
        ["quiz_score", "quiz_attempts", "status", "validation_date"],
        as_dict=True
    )

    if not enrollment:
        return {"attempts": [], "best_score": 0}

    return {
        "attempts": enrollment.quiz_attempts or 0,
        "best_score": enrollment.quiz_score or 0,
        "status": enrollment.status,
        "validated_at": str(enrollment.validation_date) if enrollment.validation_date else None,
    }
