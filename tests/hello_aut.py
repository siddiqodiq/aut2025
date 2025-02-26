import unittest, sys
from selenium import webdriver
from selenium.webdriver.common.by import By

class AutTest(unittest.TestCase):
    def setUp(self):
        browser_type = sys.argv[1] if len(sys.argv) > 1 else 'firefox'
        
        options = None
        if browser_type == 'firefox':
            options = webdriver.FirefoxOptions()
        elif browser_type == 'chrome':
            options = webdriver.ChromeOptions()
        elif browser_type == 'edge':
            options = webdriver.EdgeOptions()

        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        
        server = f'http://localhost:444{["4", "5", "6"].index(browser_type)}'
        self.browser = webdriver.Remote(command_executor=server, options=options)
        self.addCleanup(self.browser.quit)

    def test_homepage(self):
        if len(sys.argv) > 2:
            url = sys.argv[2]
        else:
            url = "http://localhost"
        self.browser.get(url)
        self.browser.save_screenshot(f'screenshot_{sys.argv[1]}.png')
        expected_result = "Welcome back, Guest!"
        actual_result = self.browser.find_element(By.TAG_NAME, 'p')
        self.assertIn(expected_result, actual_result.text)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], verbosity=2, warnings='ignore')
