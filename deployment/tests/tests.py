import subprocess
import unittest
from unittest import TestCase

class DeployTest(TestCase):

    def test_deploy_to_local_vm(self):

        output = subprocess.check_output(['python', 'deploy.py', 'local-vm'])

        # TODO: check it setup up okay


if __name__ == '__main__':
    unittest.main()
