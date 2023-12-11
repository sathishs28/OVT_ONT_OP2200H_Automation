# import time
import pytest
from Utilities.ReadProperties import ReadConfig
from PageObjects.Login_Page import LoginPage
from PageObjects.WAN_Page import WAN_Page

snap_path = "./ScreenShots/"


class Test_003_New_WAN:
    device_URL = ReadConfig.get_device_url()
    username = ReadConfig.get_username()
    password = ReadConfig.get_password()

    @pytest.mark.Sanity
    @pytest.mark.Smoke
    @pytest.mark.Regression
    def test_add_bridge_wan_1(self, setup, logger):
        self.driver = setup
        self.driver.get(self.device_URL)
        try:
            logger.info("********************* Test_003_New_WAN :: 1-test_add_bridge_wan *********************")
            logger.info("******* test_add_bridge_wan Test case is started & Verifying *******")
            # Login Device
            self.lp = LoginPage(self.driver)
            self.lp.login(self.username, self.password)

            # Navigate to WAN Page
            self.wp = WAN_Page(self.driver)
            self.wp.click_wan_mainmenu()
            self.wp.click_pon_wan_submenu()
            self.wp.switch_iframe()  # Switch to Inner frame of another HTML document

            # Configure Bridge WAN
            bf_wan_list = self.wp.get_wan_list()
            self.wp.select_wan("new link")  # Create New WAN Profile
            self.wp.enable_vlan()
            # time.sleep(3)
            vlan_id = 1000
            self.wp.send_vlan_id(vlan_id)
            self.wp.select_wan_channel_mode("Bridged")
            self.wp.select_connection_type_bg("Other")

            # self.wp.port_mapping()
            # Apply configuration
            self.wp.click_wan_apply()
            # time.sleep(6)
            # self.wp.switch_iframe()     # Switch to Inner frame of another HTML document
            # wait = WebDriverWait(setup, 10)
            # Verify the applied configuration
            status = "Change setting successfully!"
            # status = self.wp.verify_apply_ele()
            # status = wait.until(EC.visibility_of_element_located((By.XPATH, WAN_Page.VERIFY_APPLY_XPATH)))
            """ Print Log
            if status.is_displayed():
                print("Status Element is found")
                self.driver.switch_to.default_content()
                self.lp.click_logout()
                self.driver.close()
            else:
                print("Status Element is not found")
                self.driver.switch_to.default_content()
                self.lp.click_logout()
                self.driver.close()
            """
            # if status.is_displayed():
            if status == self.wp.verify_apply_status():
                # Verify the added WAN is showing or not and print the added WAN interface Name
                self.wp.click_ok_btn()
                # Get current WAN List
                af_wan_list = self.wp.get_wan_list()
                if bf_wan_list != af_wan_list:
                    # print("Newly added WAN is there...")
                    new_wan_index = len(af_wan_list) - 2
                    print("Newly added WAN Interface Name - " + af_wan_list[new_wan_index].text)
                    logger.info("******* test_add_bridge_wan Test case is completed *******")
                    logger.info("******* Newly added WAN Interface Name - " + af_wan_list[new_wan_index].text +
                                '*******')
                    logger.info("******* test_add_bridge_wan Test case is success *******")
                    assert True
                else:
                    # print("Newly added WAN is not there")
                    self.driver.save_screenshot(snap_path + "test_add_bridge_wan_error.png")
                    logger.error("************** Newly added WAN is not added **************")
                    logger.error("************** test_add_bridge_wan Test case is failed **************")
                    assert False
                self.driver.switch_to.default_content()
                self.lp.click_logout()
                self.driver.close()
                return
            else:
                self.driver.save_screenshot(snap_path + "test_add_bridge_wan_error.png")
                logger.error("************** Status -" + self.wp.verify_apply_status() + "**************")
                logger.error("************** test_add_bridge_wan Test case is failed **************")
                self.driver.switch_to.default_content()
                self.lp.click_logout()
                self.driver.close()
                assert False
        except Exception as e1:
            self.driver.save_screenshot(snap_path + "test_add_bridge_wan_issue.png")
            logger.error("************** test_add_bridge_wan Test case is stopped - Webpage is not loaded ("
                         "Refer belo logs**************")
            logger.error(f"Page load failed: {str(e1)}")
            self.driver.switch_to.default_content()
            self.lp.click_logout()
            self.driver.close()
            assert False

    """
        # Below this condition for if above all cases are failed... Try to log out the webpage
        try:
            if self.lp.get_logout_element().is_displayed():
                self.driver.switch_to.default_content()
                self.lp.click_logout()
                self.driver.close()
                return
            else:
                self.lp.click_logout()
                self.driver.close()
                return
        except Exception as e2:
            print(f"Page load failed: {str(e2)}")
    """

    @pytest.mark.Sanity
    @pytest.mark.Smoke
    @pytest.mark.Regression
    def test_add_ipoe_wan_2(self, setup, logger):
        self.driver = setup
        self.driver.get(self.device_URL)
        try:
            logger.info("********************* Test_003_New_WAN :: 2-test_add_ipoe_wan *********************")
            logger.info("******* test_add_ipoe_wan Test case is started & Verifying *******")
            # Login Device
            self.lp = LoginPage(self.driver)
            self.lp.login(self.username, self.password)

            # Navigate to WAN Page
            self.wp = WAN_Page(self.driver)
            self.wp.click_wan_mainmenu()
            self.wp.click_pon_wan_submenu()
            self.wp.switch_iframe()  # Switch to Inner frame of another HTML document

            # Configure IPoE WAN
            bf_wan_list = self.wp.get_wan_list()
            self.wp.select_wan("new link")  # Create New WAN Profile
            self.wp.enable_vlan()
            # time.sleep(3)
            vlan_id = 50
            self.wp.send_vlan_id(vlan_id)
            self.wp.select_wan_channel_mode("IPoE")
            self.wp.select_connection_type("INTERNET_TR069")
            # Configure WAN IP Settings
            self.wp.select_ipoe_type_dhcp()  # WAN IP Mode is DHCP

            # self.wp.port_mapping()
            """ Update will soon """
            # Apply configuration
            self.wp.click_wan_apply()
            status = "Change setting successfully!"

            # if status.is_displayed():
            if status == self.wp.verify_apply_status():
                # Verify the added WAN is showing or not and print the added WAN interface Name
                self.wp.click_ok_btn()
                # Get current WAN List
                af_wan_list = self.wp.get_wan_list()
                if bf_wan_list != af_wan_list:
                    new_wan_index = len(af_wan_list) - 2
                    print("Newly added WAN Interface Name - " + af_wan_list[new_wan_index].text)
                    logger.info("******* test_add_ipoe_wan Test case is completed *******")
                    logger.info("******* Newly added WAN Interface Name - " + af_wan_list[new_wan_index].text +
                                '*******')
                    logger.info("******* test_add_ipoe_wan Test case is success *******")
                    assert True
                else:
                    self.driver.save_screenshot(snap_path + "test_add_ipoe_wan_error.png")
                    logger.error("************** Newly added WAN is not added **************")
                    logger.error("************** test_add_ipoe_wan Test case is failed **************")
                    assert False
                self.driver.switch_to.default_content()
                self.lp.click_logout()
                self.driver.close()
                return
            else:
                self.driver.save_screenshot(snap_path + "test_add_ipoe_wan_error.png")
                logger.error("************** Status -" + self.wp.verify_apply_status() + "**************")
                logger.error("************** test_add_ipoe_wan Test case is failed **************")
                self.driver.switch_to.default_content()
                self.lp.click_logout()
                self.driver.close()
                assert False
        except Exception as e1:
            self.driver.save_screenshot(snap_path + "test_add_ipoe_wan_issue.png")
            logger.error("************** test_add_ipoe_wan Test case is stopped - Webpage is not loaded ("
                         "Refer belo logs**************")
            logger.error(f"Page load failed: {str(e1)}")
            self.driver.switch_to.default_content()
            self.lp.click_logout()
            self.driver.close()
            assert False

    @pytest.mark.Sanity
    @pytest.mark.Smoke
    @pytest.mark.Regression
    def test_add_pppoe_wan_3(self, setup, logger):
        self.driver = setup
        self.driver.get(self.device_URL)
        try:
            logger.info("********************* Test_003_New_WAN :: 3-test_add_pppoe_wan *********************")
            logger.info("******* test_add_pppoe_wan Test case is started & Verifying *******")
            # Login Device
            self.lp = LoginPage(self.driver)
            self.lp.login(self.username, self.password)

            # Navigate to WAN Page
            self.wp = WAN_Page(self.driver)
            self.wp.click_wan_mainmenu()
            self.wp.click_pon_wan_submenu()
            self.wp.switch_iframe()  # Switch to Inner frame of another HTML document

            # Configure IPoE WAN
            bf_wan_list = self.wp.get_wan_list()
            self.wp.select_wan("new link")  # Create New WAN Profile
            self.wp.enable_vlan()
            # time.sleep(3)
            vlan_id = 200
            self.wp.send_vlan_id(vlan_id)
            self.wp.select_wan_channel_mode("PPPoE")
            self.wp.select_connection_type("INTERNET_TR069")
            # Configure PPP Settings
            self.wp.send_ppp_username_name("automation@vlan200")
            self.wp.send_ppp_password("password")
            # self.wp.send_ppp_ac_name("LAB")
            # self.wp.send_ppp_service_name("OVT")

            # self.wp.port_mapping()
            """ Update will soon """
            # Apply configuration
            self.wp.click_wan_apply()
            status = "Change setting successfully!"

            # if status.is_displayed():
            if status == self.wp.verify_apply_status():
                # Verify the added WAN is showing or not and print the added WAN interface Name
                self.wp.click_ok_btn()
                # Get current WAN List
                af_wan_list = self.wp.get_wan_list()
                if bf_wan_list != af_wan_list:
                    new_wan_index = len(af_wan_list) - 2
                    # print("Newly added WAN Interface Name - " + af_wan_list[new_wan_index].text)
                    logger.info("******* test_add_pppoe_wan Test case is completed *******")
                    logger.info("******* Newly added WAN Interface Name - " + af_wan_list[new_wan_index].text +
                                '*******')
                    logger.info("******* test_add_pppoe_wan Test case is success *******")
                    assert True
                else:
                    self.driver.save_screenshot(snap_path + "test_add_pppoe_wan_error.png")
                    logger.error("************** Newly added WAN-pppoe is not added **************")
                    logger.error("************** test_add_pppoe_wan Test case is failed **************")
                    assert False
                self.driver.switch_to.default_content()
                self.lp.click_logout()
                self.driver.close()
                return
            else:
                self.driver.save_screenshot(snap_path + "test_add_pppoe_wan_error.png")
                logger.error("************** Status -" + self.wp.verify_apply_status() + "**************")
                logger.error("************** test_add_pppoe_wan Test case is failed **************")
                self.driver.switch_to.default_content()
                self.lp.click_logout()
                self.driver.close()
                assert False
        except Exception as e1:
            self.driver.save_screenshot(snap_path + "test_add_pppoe_wan_issue.png")
            logger.error("************** test_add_pppoe_wan Test case is stopped - Webpage is not loaded, "
                         "Refer belo logs**************")
            logger.error(f"Page load failed: {str(e1)}")
            self.driver.switch_to.default_content()
            self.lp.click_logout()
            self.driver.close()
            assert False


"""
    # Below test is for internet testing and debugging purpose only
    def test_workout(self, setup, logger):

        self.driver = setup
        self.driver.get(self.device_URL)
        # try:
        # Login Device
        self.lp = LoginPage(self.driver)
        self.lp.login(self.username, self.password)

        # Navigate to WAN Page
        self.wp = WAN_Page(self.driver)
        self.wp.click_wan_mainmenu()
        self.wp.click_pon_wan_submenu()
        self.wp.switch_iframe()  # Switch to Inner frame of another HTML document

        # Get WAN List
        
        # options = self.wp.get_wan_list()
        # print(len(options))
        # for option in options:
        #     print(option.text)
        # print("Printing the last added WAN " + options[2].text)
        
        logger.info("Testing Sample log generated")
        self.driver.switch_to.default_content()
        self.lp.click_logout()
        self.driver.close()
        
"""