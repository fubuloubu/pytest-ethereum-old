import pytest
import json


@pytest.fixture
def testcase():
    return """
def test_MyTest(tester):
    assert tester is not None
    """


@pytest.mark.xfail
def test_NoPackage(testdir):
    testdir.makepyfile(testcase)
    # Works without one
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)  # No failures


@pytest.mark.xfail
def test_BadReference(testdir, testcase):
    testdir.makepyfile(testcase)
    # If provided a file that does not exist, should fail
    testdir.parseconfig('--package-file', 'does-not-exist.json')
    result = testdir.runpytest()
    result.assert_outcomes(error=1)


@pytest.fixture
def run_packagefile(testdir, testcase):
    def run_packagefile(package=None):
        testdir.makepyfile(testcase)
        package_file = testdir.makefile('.json', contracts=json.dumps(package))
        return testdir.runpytest(package_file=package_file)

    # Return function as fixture
    return run_packagefile


@pytest.mark.xfail
def test_BadPackageFile(run_packagefile):
    # Cannot supply a badly formatted file
    result = run_packagefile({
            'badkey': [0, 1]
        })
    result.assert_outcomes(failed=1)


@pytest.mark.xfail
def test_GoodPackageFile(run_packagefile):
    # Works with a well-formatted one
    result = run_packagefile({
            'contracts': {
                'A': {
                    'abi': [],
                    'bin': '0x',
                    'bin-runtime': '0x'
                }
            }
        })
    result.assert_outcomes(passed=1)  # No failures
