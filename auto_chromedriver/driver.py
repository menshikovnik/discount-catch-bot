from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc


class Driver(uc.Chrome):
    def __init__(self, options: uc.ChromeOptions = None) -> None:
        self.options = options
        self.manager = ChromeDriverManager()
        super().__init__(use_subprocess=True, options=options)

    def __del__(self):
        try:
            super().__del__()
        except OSError:
            pass
