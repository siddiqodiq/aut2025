import unittest
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor

class AutTest(unittest.TestCase):
    def setUp(self):
        # Daftar browser yang akan diuji
        self.browsers = {
            'firefox': webdriver.FirefoxOptions(),
            'chrome': webdriver.ChromeOptions(),
            'edge': webdriver.EdgeOptions()
        }
        # Konfigurasi opsi untuk setiap browser
        for options in self.browsers.values():
            options.add_argument('--ignore-ssl-errors=yes')
            options.add_argument('--ignore-certificate-errors')
        self.server = 'http://localhost:4444'

    def test_homepage(self, browser_name):
        # Mengambil opsi browser yang sesuai
        options = self.browsers[browser_name]
        # Membuat instance browser remote
        browser = webdriver.Remote(command_executor=self.server, options=options)
        self.addCleanup(browser.quit)

        # Membuka URL
        if len(sys.argv) > 1:
            url = sys.argv[1]
        else:
            url = "http://localhost"
        browser.get(url)

        # Mengambil screenshot
        browser.save_screenshot(f'screenshot_{browser_name}.png')

        # Memeriksa teks yang diharapkan
        expected_result = "Welcome back, Guest!"
        actual_result = browser.find_element(By.TAG_NAME, 'p')
        self.assertIn(expected_result, actual_result.text)

    def test_parallel(self):
        # Menjalankan tes secara paralel untuk setiap browser
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(self.test_homepage, browser_name) for browser_name in self.browsers.keys()]
            for future in futures:
                future.result()

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], verbosity=2, warnings='ignore')
