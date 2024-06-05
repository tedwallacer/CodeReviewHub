import unittest
from unittest.mock import patch
from code_manager import CodeSubmission, CodeReview
import os


class TestCodeManager(unittest.TestCase):

    def setUp(self):
        os.environ['PYTHON_ENV'] = 'test'
        self.python_submission = CodeSubmission(language='Python', code='print("Hello, World!")')
        self.good_review = CodeReview(submission_id=1, reviewer_id=2, comments='Looks good.')

    def test_python_submission_attributes(self):
        self.assertEqual(self.python_submission.language, 'Python')
        self.assertEqual(self.python_submission.code, 'print("Hello, World!")')

    def test_submission_language_support(self):
        with self.assertRaises(ValueError):
            CodeSubmission(language='Brainfuck', code='+[-->-[>>+>-----<<]')

    @patch('code_manager.CodeSubmission.submit')
    def test_python_submission_submit(self, mock_submit):
        self.python_submission.submit()
        mock_submit.assert_called_once()

    def test_good_review_attributes(self):
        self.assertEqual(self.good_review.submission_id, 1)
        self.assertEqual(self.good_review.reviewer_id, 2)
        self.assertEqual(self.good_review.comments, 'Looks good.')

    @patch('code_manager.CodeReview.submit_review')
    def test_review_submit_method(self, mock_submit_review):
        self.good_review.submit_review()
        mock_submit_review.assert_called_once()

    def test_review_assignment(self):
        with patch('code_manager.CodeSubmission.assign_reviewer') as mock_assign:
            reviewer_id = 100
            self.python_submission.assign_reviewer(reviewer_id)
            mock_assign.assert_called_with(reviewer_id)

    def tearDown(self):
        os.environ.pop('PYTHON_ENV', None)


if __name__ == '__main__':
    unittest.main()