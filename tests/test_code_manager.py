import unittest
from unittest.mock import patch
from code_manager import CodeSubmission, CodeReview
import os

class TestCodeManager(unittest.TestCase):

    def setUp(self):
        os.environ['PYTHON_ENV'] = 'test'
        self.submission = CodeSubmission(language='Python', code='print("Hello, World!")')
        self.review = CodeReview(submission_id=1, reviewer_id=2, comments='Looks good.')

    def test_submission_creation(self):
        self.assertEqual(self.submission.language, 'Python')
        self.assertEqual(self.submission.code, 'print("Hello, World!")')

    def test_submission_language_support(self):
        with self.assertRaises(ValueError):
            CodeSubmission(language='Brainfuck', code='+[-->-[>>+>-----<<]')

    @patch('code_manager.CodeSubmission.submit')
    def test_submission_submit_method(self, mock_submit):
        self.submission.submit()
        mock_submit.assert_called_once()

    def test_review_creation(self):
        self.assertEqual(self.review.submission_id, 1)
        self.assertEqual(self.review.reviewer_id, 2)
        self.assertEqual(self.review.comments, 'Looks good.')

    @patch('code_manager.CodeReview.submit_review')
    def test_review_submit_method(self, mock_submit_review):
        self.review.submit_review()
        mock_submit_review.assert_called_once()

    def test_review_assignment_logic(self):
        with patch('code_dir_you_have.CodeSubmission.assign_reviewer') as mock_assign:
            reviewer_id = 100  
            self.submission.assign_reviewer(reviewer_id)
            mock_assign.assert_called_with(reviewer_id)

    def tearDown(self):
        os.environ.pop('PYTHON_ENV', None)


if __name__ == '__main__':
    unittest.main()