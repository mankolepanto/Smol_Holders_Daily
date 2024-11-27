
binary_location = '/usr/bin/chromium'

from seleniumbase import Driver
from seleniumbase import SB

with SB (uc=True, demo=True, headless=False) as sb:
    url = ('https://arbiscan.io/exportData?type=tokenholders&contract=0x9e64d3b9e8ec387a9a58ced80b71ed815f8d82b5&decimal=18')
    sb.uc_open_with_reconnect (url,4)
    sb.uc_gui_click_captcha()
    # Encuentra el elemento que quieres hacer clic
    sb.click ('#ContentPlaceHolder1_btnSubmit')
    #sb.click_link ("Download")

    sb.sleep(10)












































