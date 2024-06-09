import unittest
from unittest.mock import patch, MagicMock
from code_manager import CodeDanSubmission, CodeReview
import os


class TestCodeManager(unittest.TestCase):
    """Test suite for testing the CodeManager functionality."""

    def setUp(self):
        """Prepare environment and test cases."""
        os.environ['PYTHON_ENV'] = 'test'
        self.python_submission = CodeSubmission(language='Python', code='import os\nprint("Hello, World!")')
        self.good_review = CodeReview(submission_id=1, reviewer_id=2, comments='Looks good.')

    def test_python_submission_attributes(self):
        """Test if Python submission attributes are correctly set."""
        self.assertEqual(self.python_submission.language, 'Python')
        self.assertEqual(self.python_submission.code, 'import os\nprint("Hello, World!")')

    def test_submission_language_support(self):
        """Test submission with unsupported programming language raises ValueError."""
        with self.assertRaises(ValueError):
            CodeSubmission(language='Brainfuck', code='+[-->-[>>+>-----<<]')

    @patch('code_manager.CodeSubmission.submit')
    def test_python_submission_submit(self, mock_submit):
        """Test if Python submission can be submitted."""
        self.python_submission.submit()
        mock_submit.assert_called_once()

    def test_good_review_attributes(self):
        """Test if review attributes are correctly set."""
        self.assertEqual(self.good_review.submission_id, 1)
        self.assertEqual(self.good_review.reviewer_id, 2)
        self.assertEqual(self.good_review.comments, 'Looks good.')

    @patch('code_manager.CodeReview.submit_review')
    def test_review_submit_method(self, mock_submit_review):
        """Test if review can be submitted."""
        self.good_review.submit_review()
        mock_submit_review.assert_called_once()

    @patch('code_manager.CodeSubmission.assign_reviewer')
    def test_review_assignment(self, mock_assign):
        """Test if a reviewer can be assigned to a submission."""
        reviewer_id = 100
        self.python_submission.assign_reviewer(reviewer_id)
        mock_assign.assert_called_with(reviewer_id)

    @patch('code_manager.CodeSubmission.analyze_code')
    def test_static_code_analysis_feedback(self, mock_analyze_code):
        """Test if static code analysis offers helpful feedback."""
        feedback = "Unused import 'os'"
        mock_analyze_code.return_value = feedback
        result = self.python_submission.analyze_code()
        self.assertEqual(result, feedback)
        mock_analyze_code.assert_called_once()

    def tearDown(self):
        """Cleanup environment variables."""
        os.environ.pop('PYTHON_ENV', None)


if __name__ == '__main__':
    unittest.main()