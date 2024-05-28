import os
from dotenv import load_dotenv
from collections import defaultdict
import subprocess
import json

load_dotenv()

class CodeManager:
    def __init__(self):
        self.submissions = {}
        self.reviews = defaultdict(list)
        self.comments = defaultdict(list)

    def add_submission(self, submission_id, code_snippet):
        self.submissions[submission_id] = code_snippet

    def add_comment(self, submission_id, comment):
        if submission_id in self.submissions:
            self.comments[submission_id].append(comment)
        else:
            # Logging or handling this error could be here if needed
            raise ValueError("Invalid submission ID")

    def get_comments(self, submission_id):
        return self.comments.get(submission_id, [])

    def initiate_review(self, submission_id, reviewer):
        if submission_id in self.submissions:
            self.reviews[submission_id].append(reviewer)
        else:
            # Logging or handling this error could be here if needed
            raise ValueError("Invalid submission ID")

    def get_reviewers(self, submission_id):
        return self.reviews.get(submission_id, [])

class CodeQualityManager(CodeManager):
    def __init__(self):
        super().__init__()
        self.quality_checks = {}

    def add_quality_check(self, submission_id, check_command):
        self.quality_checks[submission_id] = check_command

    def run_quality_checks(self, submission_id):
        if submission_id not in self.quality_checks:
            raise ValueError("No quality check command found for this submission ID")
        check_command = self.quality_checks[submission_id]
        try:
            result = subprocess.run(check_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return {"passed": True, "output": result.stdout, "error": result.stderr}
        except subprocess.CalledProcessError as e:
            return {"passed": False, "output": e.stdout, "error": e.stderr}
        except Exception as ex:
            # This captures any other unforeseen error during the subprocess execution
            return {"passed": False, "output": "", "error": str(ex)}

if __name__ == "__main__":
    cm = CodeQualityManager()
    try:
        cm.add_submission('123', 'print("Hello, world!")')
        cm.add_comment('123', 'Looks good!')
        cm.add_quality_check('123', 'python -m flake8 submission_123.py')
        print("Comments for 123:", cm.get_comments('123'))
        print("Running quality checks for 123...")
        result = cm.run_quality_checks('123')
        print(json.dumps(result, indent=2))
    except ValueError as ve:
        print("An error occurred:", ve)
    except Exception as e:
        print("An unexpected error occurred:", str(e))