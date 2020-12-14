import traceback

class TestCase:
    def __init__(self, name):
      self.name = name

    def setUp(self):
      pass

    def tearDown(self):
      pass

    def run(self, result):
      result.testStarted()
      try:
        self.setUp()
      except:
        result.setUpFailed()
      try:
        method = getattr(self, self.name)
        method()
      except:
        result.testFailed()
      self.tearDown()
      return result

class TestSuite:
  def __init__(self):
    self.tests= []

  def add(self, test):
    self.tests.append(test)

  def run(self, result):
    for test in self.tests:
      test.run(result)

class TestResult:
    def __init__(self):
      self.runCount= 0
      self.errorCount= 0
      self.errorLog= ""
      self.listeners= []
      self.setUpFailure= None

    def traceback(func):
        def inner(self):
          self.traceback = traceback.format_exc()
          func(self)
        return inner

    @traceback
    def setUpFailed(self):
      self.setUpFailure= self.traceback

    def testStarted(self):
      self.runCount= self.runCount + 1
      for listener in self.listeners:
        listener.startTest()

    @traceback
    def testFailed(self):
      self.errorCount= self.errorCount + 1
      self.errorLog= self.errorLog + self.traceback

    def summary(self):
      if self.setUpFailure:
        return "%sNo tests were run, setUp() failed" % self.setUpFailure
      else:
        return "%s%d run, %d failed" % (self.errorLog, self.runCount, self.errorCount)

    def addListener(self, newListener):
     self.listeners.append(newListener)

class WasRun(TestCase):
  def __init__(self, name):
      TestCase.__init__(self, name)

  def setUp(self):
      self.wasRun = None
      self.log = "setUp "

  def testMethod(self):
      self.log= self.log + "testMethod "

  def testBrokenMethod(self):
      raise Exception

  def tearDown(self):
      self.log= self.log + "tearDown "

class BrokenSetUp(TestCase):
  def setUp(self):
      raise Exception