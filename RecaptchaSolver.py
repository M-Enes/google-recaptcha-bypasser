import os,urllib,random,pydub,speech_recognition,time
from DrissionPage.common import Keys
from DrissionPage import ChromiumPage
from CaptchaImageSolver import CaptchaImageSolver

class RecaptchaSolver:
    def __init__(self, driver:ChromiumPage):
        self.driver = driver
    
    def solve_image_captcha(self, solver : CaptchaImageSolver, grid_size=0):

        iframe = self.getiframe()
        iframe('#rc-imageselect', timeout=3).get_screenshot(name=f"captcha.png")

        # Solve the image captcha
        result, grid_size_response = solver.solve_captcha_image(f"captcha.png")

        if grid_size == 0:
            grid_size = grid_size_response
    
        if result == "no":
            print("debug: end of captcha")
            self.click_verify()
            time.sleep(0.3)
            if self.is_solved():
                return True
            
            if iframe("@class=rc-imageselect-incorrect-response"):
                # Try again to solve
                return self.solve_image_captcha(solver, grid_size)
            
            print("captcha failed")
            return False

        print("debug:",result, ":::")
        result = result.replace("(","").replace(")","").replace("'","").replace(" ","").replace(",", "")
        print("debug:",result)
        print("debug: grid_size: ", grid_size)

        for i in range(0, len(result) - 1, 2):
            row_index = int(result[i])
            column_index = int(result[i + 1])
        
            if row_index == grid_size or column_index == grid_size:
                # Error: Invalid result
                # print("Invalid result")
                # return


                # Just act as upper bound
                if row_index == grid_size:
                    row_index = grid_size - 1
                if column_index == grid_size:
                    column_index = grid_size - 1

    
            tabindex = 4 + (row_index * grid_size) + column_index
            iframe(f"@tabindex={tabindex}").click()
            time.sleep(0.4)


        one_time = False
        if iframe("@class=rc-imageselect-tile rc-imageselect-tileselected"):
            one_time = True

        if not one_time:
            time.sleep(.7)
            return self.solve_image_captcha(solver, grid_size)

        # Submit the captcha
        self.click_verify()

        if self.is_solved():
            return True
        





    def solve_captcha(self):
        iframe = self.getiframe()
        self.click_checkbox()
        if self.is_solved():
            return

        # Click on the audio button
        time.sleep(.4)
        iframe('#recaptcha-audio-button',timeout=1).drag(3,5)
        time.sleep(.4)


        if (self.check_try_again(iframe)):
            self.driver.refresh()
            self.click_checkbox()
            time.sleep(.3)
            solver = CaptchaImageSolver()
            is_successful = self.solve_image_captcha(solver)

            while not is_successful:
                self.solve_image_captcha(solver)

            

        # Get the audio source
        src = iframe('#audio-source').attrs['src']
        
        # Download the audio to the temp folder
        path_to_mp3 = os.path.normpath(os.path.join((os.getenv("TEMP") if os.name=="nt" else "/tmp/")+ str(random.randrange(1,1000))+".mp3"))
        path_to_wav = os.path.normpath(os.path.join((os.getenv("TEMP") if os.name=="nt" else "/tmp/")+ str(random.randrange(1,1000))+".wav"))
        
        urllib.request.urlretrieve(src, path_to_mp3)

        # Convert mp3 to wav
        sound = pydub.AudioSegment.from_mp3(path_to_mp3)
        sound.export(path_to_wav, format="wav")
        sample_audio = speech_recognition.AudioFile(path_to_wav)
        r = speech_recognition.Recognizer()
        with sample_audio as source:
            audio = r.record(source)
        
        # Recognize the audio
        key = r.recognize_google(audio)
        
        # Input the key
        iframe('#audio-response').input(key.lower(), by_js=True)
        time.sleep(0.4)
        
        # Submit the key
        iframe('#audio-response').input(Keys.ENTER)
        time.sleep(.2)

        self.click_verify()
        
        time.sleep(.7)

        # Check if the captcha is solved
        if self.is_solved():
            return
        else:
            raise Exception("Failed to solve the captcha")


    def click_checkbox(self):
        iframe_inner = self.driver("@title=reCAPTCHA")
        time.sleep(0.3)
        # Click on the recaptcha
        iframe_inner('.rc-anchor-content',timeout=1).drag(5, 7)
        self.driver.wait.ele_displayed("xpath://iframe[contains(@title, 'recaptcha')]",timeout=3)


    def click_verify(self):
        iframe = self.getiframe()
        iframe("#recaptcha-verify-button").click()

    def getiframe(self):
        iframe = self.driver("xpath://iframe[contains(@title, 'recaptcha')]")
        return iframe

    def is_solved(self):
        try:
            return "style" in self.driver.ele(".recaptcha-checkbox-checkmark",timeout=1).attrs
        except:
            return False
        
    def check_try_again(self, iframe):
        # check for try again text
        return iframe.wait.ele_displayed(".rc-doscaptcha-header",timeout=0.5)