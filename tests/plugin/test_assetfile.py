import pytest
import json


@pytest.fixture
def testcase():
    return """
def test_MyTest(tester):
    assert tester is not None
    """


@pytest.mark.xfail
def test_NoAssets(testdir):
    testdir.makepyfile(testcase)
    # Works without one
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)  # No failures


@pytest.mark.xfail
def test_BadReference(testdir, testcase):
    testdir.makepyfile(testcase)
    # If provided a file that does not exist, should fail
    testdir.parseconfig('--assets-file', 'does-not-exist.json')
    result = testdir.runpytest()
    result.assert_outcomes(error=1)


@pytest.fixture
def run_assetsfile(testdir, testcase):
    def run_assetsfile(assets=None):
        testdir.makepyfile(testcase)
        assets_file = testdir.makefile('.json', contracts=json.dumps(assets))
        return testdir.runpytest(assets_file=assets_file)

    # Return function as fixture
    return run_assetsfile


@pytest.mark.xfail
def test_BadAssetsFile(run_assetsfile):
    # Cannot supply a badly formatted file
    result = run_assetsfile({
            'badkey': [0, 1]
        })
    result.assert_outcomes(failed=1)


@pytest.mark.xfail
def test_GoodAssetsFile(run_assetsfile):
    # Works with a well-formatted one
    result = run_assetsfile({
            'contracts': {
                'A': {
                    'abi': [],
                    'bin': '0x',
                    'bin-runtime': '0x'
                }
            }
        })
    result.assert_outcomes(passed=1)  # No failures
