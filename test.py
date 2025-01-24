from DrissionPage import ChromiumPage, ChromiumOptions
from RecaptchaSolver import RecaptchaSolver
import time

options = ChromiumOptions()
driver = ChromiumPage(options)
recaptchaSolver = RecaptchaSolver(driver)

# driver.get("https://www.google.com/recaptcha/api2/demo")

driver.get('http://localhost')

t0 = time.time()
try: # TODO: fix waiting when simple clicking works
    recaptchaSolver.solve_captcha()
    print(f"Time to solve the captcha: {time.time()-t0:.2f} seconds")
except:
    print("Captcha not solved")


response = driver.run_js('grecaptcha.getResponse()', as_expr=True)
print(f"Response: {response}")

#driver.ele("#recaptcha-demo-submit").click()

#driver.close()