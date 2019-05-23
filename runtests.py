import os
import unittest
import coverage
import sys


def runTests():
    tests = unittest.TestLoader().discover('bin/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    return result

def mainOnlyTest():

    try:
        result = runTests()
        print("Test Results: {}".format(result), file=sys.stderr)
    except Exception:
        return 1

    if result.wasSuccessful():
        return 0
    else:

        return 1

def mainTestWithCoverage():
    """Runs the unit tests with coverage."""

    COV = coverage.coverage(
        branch=False,
        include='bin/*',
        omit=[
            'bin/tests/*',
            'bin/__init__.py'
        ]
    )

    COV.start()

    try:
        
        result = runTests()
        print("Coverage Test Results: {}".format(result.wasSuccessful(), file=sys.stderr))

        if result.wasSuccessful():

            COV.stop()
            COV.save()
            print('Coverage Summary:',file=sys.stderr)
            COV.report()

            basedir = os.path.abspath(os.path.dirname(__file__))
            covdir = os.path.join(basedir, 'tmp/coverage')
            COV.html_report(directory=covdir)
            print('HTML version: file://%s/index.html' % covdir, file=sys.stderr)
            COV.erase()
            return 0
        
        else:

            return 1

    except Exception:

        return 1

    

if __name__ == '__main__':

    if len(sys.argv) > 1:
        sys.exit(mainOnlyTest())
        
    else:
        sys.exit(mainTestWithCoverage())