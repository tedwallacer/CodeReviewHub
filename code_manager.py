import os
import subprocess
import json
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()

class CodeManager:
    def __init__(self):
        self.submissions = {}
        self.reviews = defaultdict(list)
        self.comments = defaultdict(list)

    def add_submission(self, submission_id, code_snippet):
        """Add a new code snippet submission."""
        self.submissions[submission_id] = code_snippet

    def add_comment(self, submission_id, comment):
        """Add a comment to a submission."""
        if submission_id in self.submissions:
            self.comments[submission_id].append(comment)
        else:
            raise ValueError(f"Invalid submission ID: {submission_id}")

    def get_comments(self, submission_id):
        """Get all comments for a submission."""
        return self.comments.get(submission_id, [])

    def initiate_review(self, submission_id, reviewer):
        """Initiate a review by adding a reviewer."""
        if submission_id in self.submissions:
            self.reviews[submission_id].append(reviewer)
        else:
            raise ValueError(f"Invalid submission ID: {submission_id}")

    def get_reviewers(self, submission_id):
        """Get all reviewers for a submission."""
        return self.reviews.get(submission_id, [])

    def list_all_submissions(self):
        """List all submissions with review status."""
        return [{"id": id, "code_snippet": snippet, "has_review": id in self.reviews} for id, snippet in self.submissions.items()]

class CodeQualityManager(CodeManager):
    def __init__(self):
        super().__init__()
        self.quality_checks = {}
        self.quality_check_logs = defaultdict(list)

    def add_quality_check(self, submission_id, check_command):
        """Assign a quality check command to a submission."""
        self.quality_checks[submission_id] = check_command

    def run_quality_checks(self, submission_id):
        """Run assigned quality checks for a submission."""
        if submission_id not in self.quality_checks:
            raise ValueError("No quality check command found for this submission ID")
        
        check_command = self.quality_checks[submission_id]
        try:
            result = subprocess.run(check_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.log_quality_check(submission_id, True, result.stdout, result.stderr)
            return {"passed": True, "output": result.stdout, "error": result.stderr}
        except subprocess.CalledProcessError as e:
            self.log_quality_check(submission_id, False, e.stdout, e.stderr)
            return {"passed": False, "output": e.stdout, "error": e.stderr}
        except Exception as ex:
            self.log_quality_check(submission_id, False, "", str(ex))
            return {"passed": False, "output": "", "error": str(ex)}

    def log_quality_check(self, submission_id, passed, output, error):
        """Log the result of a quality check."""
        self.quality_check_logs[submission_id].append({
            "passed": passed,
            "output": output,
            "error": error
        })

    def get_quality_check_logs(self, submission_id):
        """Get all quality check logs for a submission."""
        return self.quality_check_logs.get(submission_id, [])

if __name__ == "__main__":
    code_quality_manager = CodeQualityManager()
    try:
        code_quality_manager.add_submission('123', 'print("Hello, world!")')
        code_quality_manager.add_comment('123', 'Looks good!')
        code_quality_manager.add_quality_check('123', 'python -m flake8 submission_123.py')
        print("Comments for 123:", code_quality_manager.get_comments('123'))
        print("Running quality checks for 123...")
        result = code_quality_manager.run_quality_checks('123')
        print(json.dumps(result, indent=2))
        print("All submissions:", code_quality_manager.list_all_submissions())
        print("Quality check logs for 123:", code_quality_manager.get_quality_check_logs('123'))
    except ValueError as ve:
        print(f"An error occurred: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")