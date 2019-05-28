from harc.harc_cli import main
import unittest


class TestPropertyRepository(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # def test_git_branches(self):
    #     main(['git:branches', '-u', 'jan.ripke'])

    def test_git_branches(self):
        main(['git:branches'])


if __name__ == '__main__':
    unittest.main()