from testcase import *

class TestCaseTest(TestCase):
  def setUp(self):
    self.result= TestResult()

  def testTemplateMethod(self):
    test= WasRun("testMethod")
    test.run(self.result)
    assert("setUp testMethod tearDown " == test.log)

  def testResult(self):
    test= WasRun("testMethod")
    test.run(self.result)
    assert("1 run, 0 failed" == self.result.summary())

  def testFailedResult(self):
    test= WasRun("testBrokenMethod")
    test.run(self.result)
    assert(
            (
              "Traceback (most recent call last):\n"
              "  File \"/Users/rain/tdd-by-example/testcase.py\", line 21, in run\n"
              "    method()\n"
              "  File \"/Users/rain/tdd-by-example/testcase.py\", line 87, in testBrokenMethod\n"
              "    raise Exception\n"
              "Exception\n"
              "1 run, 1 failed"
            ) == self.result.summary()
          )

  def testFailedResultFormatting(self):
    self.result.testStarted()
    format_exc = traceback.format_exc
    def trace():
        return "Exception, "
    traceback.format_exc = trace
    self.result.testFailed()
    traceback.format_exc = format_exc
    assert("Exception, 1 run, 1 failed" == self.result.summary())

  def testSuite(self):
    suite= TestSuite()
    suite.add(WasRun("testMethod"))
    suite.add(WasRun("testBrokenMethod"))
    suite.run(self.result)
    assert("2 run, 1 failed" == self.result.summary().splitlines()[-1])

  def testNotification(self):
    self.count= 0
    self.result.addListener(self)
    WasRun("testNotification").run(self.result)
    assert(1 == self.count)

  def startTest(self):
    self.count= self.count + 1

  def testFailedSetUp(self):
    test= BrokenSetUp("testMethod")
    test.run(self.result)
    assert(
            (
              "Traceback (most recent call last):\n"
              "  File \"/Users/rain/tdd-by-example/testcase.py\", line 16, in run\n"
              "    self.setUp()\n"
              "  File \"/Users/rain/tdd-by-example/testcase.py\", line 94, in setUp\n"
              "    raise Exception\n"
              "Exception\n"
              "No tests were run, setUp() failed"
            ) == self.result.summary()
          )

  def testFailedSetUpFormatting(self):
    format_exc = traceback.format_exc
    def trace():
        return "Exception, "
    traceback.format_exc = trace
    self.result.setUpFailed()
    traceback.format_exc = format_exc
    assert("Exception, No tests were run, setUp() failed" == self.result.summary())

suite= TestSuite()
suite.add(TestCaseTest("testTemplateMethod"))
suite.add(TestCaseTest("testResult"))
suite.add(TestCaseTest("testFailedResult"))
suite.add(TestCaseTest("testFailedResultFormatting"))
suite.add(TestCaseTest("testSuite"))
suite.add(TestCaseTest("testNotification"))
suite.add(TestCaseTest("testFailedSetUp"))
suite.add(TestCaseTest("testFailedSetUpFormatting"))
result= TestResult()
suite.run(result)
print result.summary()