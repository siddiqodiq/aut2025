import unittest, sys
from selenium import webdriver
from selenium.webdriver.common.by import By

class AutTest(unittest.TestCase):
    def setUp(self):
        browser = sys.argv[2] if len(sys.argv) > 2 else "firefox"
        options = None
        port = None

        if browser == "firefox":
            options = webdriver.FirefoxOptions()
            port = 4444
        elif browser == "chrome":
            options = webdriver.ChromeOptions()
            port = 4445
        elif browser == "edge":
            options = webdriver.EdgeOptions()
            port = 4446

        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        server = f'http://localhost:{port}'
        self.browser = webdriver.Remote(command_executor=server, options=options)
        self.addCleanup(self.browser.quit)

    def test_homepage(self):
        if len(sys.argv) > 1:
            url = sys.argv[1]
        else:
            url = "http://localhost"
        self.browser.get(url)
        self.browser.save_screenshot(f'screenshot_{sys.argv[2]}.png')
        expected_result = "Welcome back, Guest!"
        actual_result = self.browser.find_element(By.TAG_NAME, 'p')
        self.assertIn(expected_result, actual_result.text)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], verbosity=2, warnings='ignore')