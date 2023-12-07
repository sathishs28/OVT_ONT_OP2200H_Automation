import time
import pytest
from Utilities.ReadProperties import ReadConfig
from PageObjects.Login_Page import LoginPage
from PageObjects.WAN_Page import WAN_Page

snap_path = "./ScreenShots/"


class Test_004_Delete_WAN:
    device_URL = ReadConfig.get_device_url()
    username = ReadConfig.get_username()
    password = ReadConfig.get_password()

    @pytest.mark.Sanity
    @pytest.mark.Smoke
    @pytest.mark.Regression
    def test_delete_wan(self, setup, logger):
        self.driver = setup
        self.driver.get(self.device_URL)
        try:
            logger.info("********************* Test_004_Delete_WAN :: test_delete_wan *********************")
            logger.info("******* test_delete_wan Test case is started & Verifying *******")
            # Login Device
            self.lp = LoginPage(self.driver)
            self.lp.login(self.username, self.password)

            # Navigate to WAN Page
            self.wp = WAN_Page(self.driver)
            self.wp.click_wan_mainmenu()
            self.wp.click_pon_wan_submenu()
            self.wp.switch_iframe()  # Switch to Inner frame of another HTML document
            time.sleep(1)
            options = self.wp.get_wan_list()
            list_options = []  # Defined and Stored all WAN List items
            j = 0
            while j <= (len(options) - 1):
                option = options[j].text
                list_options.append(option)
                j = j + 1
            # print("All my WAN list", list_options)
            i = len(options) - 2  # Get Maximum WAN list index
            t = i + 1
            if i >= 0:
                logger.info("******* Total-{} WAN profile has found, Starting deletion process *******".format(t))
                while i >= 0:
                    option = list_options[i]
                    # print(option)
                    # Selecting WAN and Delete
                    logger.info("******* Deleting WAN - " + option + " *******")
                    # time.sleep(5)
                    self.wp.select_wan(option)
                    self.wp.click_wan_delete()
                    status = "Change setting successfully!"
                    # time.sleep(5)
                    # Verify the status
                    if status == self.wp.verify_apply_status():
                        self.wp.click_ok_btn()
                        # Get current WAN List
                        current_options = self.wp.get_wan_list()
                        # After Deleted, verify the WAN list deleted WAN is removed or not
                        if option not in current_options:
                            logger.info("******* Successfully Deleted WAN Interface Name - " + option +
                                        ' *******')
                        else:
                            logger.error("******* Deleted WAN - " + option + " is not removed in list. Still it's "
                                                                             "there *******")
                            # return
                    else:
                        self.driver.save_screenshot(snap_path + "test_delete_wan(" + option + ")_error.png")
                        logger.error("******* Deleting WAN - " + option + " is not successful *******")
                        # return
                    i = i - 1
            else:
                logger.info("******* WAN profile has not found, Stopped deletion process *******")

            # After completed the deleting process verify the WAN List
            if len(self.wp.get_wan_list()) == 1:
                assert True
                logger.info("******* test_delete_wan Test case is success *******")
                logger.info("******* test_delete_wan Test case is completed *******")
                self.driver.switch_to.default_content()
                self.lp.click_logout()
                self.driver.close()
            else:
                logger.error("******* test_delete_all_wan not completed, something wrong...! *******")
                logger.error("******* test_delete_all_wan Test case is failed *******")
                self.driver.switch_to.default_content()
                self.lp.click_logout()
                self.driver.close()
                assert False
        except Exception as e1:
            self.driver.save_screenshot(snap_path + "test_delete_wan_issue.png")
            logger.error("************** test_delete_wan Test case is stopped - Webpage is not loaded, "
                         "Refer belo logs**************")
            logger.error(f"Page load failed: {str(e1)}")
            self.driver.switch_to.default_content()
            self.lp.click_logout()
            self.driver.close()
            assert False
