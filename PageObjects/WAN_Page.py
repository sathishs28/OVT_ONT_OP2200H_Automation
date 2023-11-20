from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


class WAN_Page:
    # Page Navigation Elements
    CLICK_WAN_MAINMENU_XPATH = "//*[text()='WAN']"  # "//a[@href='javascript:void(0)' and contains(@rel, '4')]"
    CLICK_PON_WAN_SUBMENU_XPATH = "//*[text()='PON WAN']"

    # Switching WAN Page inner frame of Html document
    SWITCH_WAN_INNER_NAME = "contentIframe"

    # New link or Available WAN Dropdown Element
    LIST_WAN_XPATH = "//select[@name='lkname']"

    # Below Elements for New WAN Profile Creation....
    CLICK_ENABLE_VLAN_XPATH = "//input[@name='vlan']"
    SEND_VLAN_ID_XPATH = "//input[@name='vid']"
    LIST_SELECT_CHANNEL_MODE_XPATH = "//select[@name='adslConnectionMode']"
    LIST_SELECT_WAN_CONNECTION_TYPE_XPATH = "//select[@name='ctype']"
    LIST_SELECT_WAN_CONNECTION_TYPE_XPATH_FOR_BDG = "//select[@name='ctypeForBridge']"

    # Fill the WAN Details
    # IP WAN Details Will update soon
    SELECT_IPOE_TYPE_DHCP_XPATH = "//input[@name='ipMode'][2]"
    # PPP WAN Credentials Elements
    SEND_PPP_USERNAME_NAME_XPATH = "//input[@name='pppUserName']"
    SEND_PPP_PASSWORD_XPATH = "//input[@name='pppPassword']"
    SEND_PPP_AC_NAME_XPATH = "//input[@name='acName']"
    SEND_PPP_SERVICE_XPATH = "//input[@name='serviceName']"

    # PORT Mapping Elements
    SELECT_ALL_PORT_MAPPING_XPATH = "//input[@name='chkpt']"
    SELECT_LAN_1_XPATH = "//td[normalize-space()='LAN_1']//input[@name='chkpt']"
    SELECT_LAN_2_XPATH = "//td[normalize-space()='LAN_2']"
    SELECT_WLAN0_XPATH = "//td[normalize-space()='WLAN0']//input[@name='chkpt']"
    SELECT_WLAN1_XPATH = "//td[normalize-space()='WLAN1']//input[@name='chkpt']"

    # APPLY & DELETE Element
    CLICK_WAN_APPLY_BTN_XPATH = "//input[@name='apply']"
    CLICK_WAN_DELETE_BTN_XPATH = "//input[@name='delete']"

    # Verify the Applied configuration
    VERIFY_APPLY_XPATH = "//h4[normalize-space()='Change setting successfully!']"
    VERIFY_APPLY_TAG = "h4"
    CLICK_OK_BTN_XPATH = "//input[@type='button']"

    def __init__(self, driver):
        self.driver = driver

    def click_wan_mainmenu(self):
        self.driver.find_element(By.XPATH, self.CLICK_WAN_MAINMENU_XPATH).click()

    def click_pon_wan_submenu(self):
        self.driver.find_element(By.XPATH, self.CLICK_PON_WAN_SUBMENU_XPATH).click()

    def switch_iframe(self):
        iframe = self.driver.find_element(By.NAME, self.SWITCH_WAN_INNER_NAME)
        self.driver.switch_to.frame(iframe)

    def get_wan_list(self):
        return Select(self.driver.find_element(By.XPATH, self.LIST_WAN_XPATH)).options

    def select_wan(self, wan_interface):
        wan_list = Select(self.driver.find_element(By.XPATH, self.LIST_WAN_XPATH))
        wan_list.select_by_visible_text(wan_interface)

    def enable_vlan(self):
        self.driver.find_element(By.XPATH, self.CLICK_ENABLE_VLAN_XPATH).click()

    def send_vlan_id(self, vlan_id):
        self.driver.find_element(By.XPATH, self.SEND_VLAN_ID_XPATH).clear()
        self.driver.find_element(By.XPATH, self.SEND_VLAN_ID_XPATH).send_keys(vlan_id)

    def select_wan_channel_mode(self, channel_mode):
        list_channel_mode = Select(self.driver.find_element(By.XPATH, self.LIST_SELECT_CHANNEL_MODE_XPATH))
        list_channel_mode.select_by_visible_text(channel_mode)

    # For WAN - Bridge Mode
    def select_connection_type_bg(self, connection_type):
        list_connection_type = Select(self.driver.find_element(By.XPATH,
                                                               self.LIST_SELECT_WAN_CONNECTION_TYPE_XPATH_FOR_BDG))
        list_connection_type.select_by_visible_text(connection_type)

    """ IPoE WAN Elements """

    def list_connection_type(self):
        return Select(self.driver.find_element(By.XPATH, self.LIST_SELECT_WAN_CONNECTION_TYPE_XPATH)).options

    def select_connection_type(self, connection_type):
        list_connection_type = Select(self.driver.find_element(By.XPATH, self.LIST_SELECT_WAN_CONNECTION_TYPE_XPATH))
        list_connection_type.select_by_visible_text(connection_type)

    """ DHCP Elements """
    def select_ipoe_type_dhcp(self):
        self.driver.find_element(By.XPATH, self.SELECT_IPOE_TYPE_DHCP_XPATH).click()

    """ Static Type Elements will update soon """

    """ PPPoE WAN Elements """
    def send_ppp_username_name(self, ppp_username):
        self.driver.find_element(By.XPATH, self.SEND_PPP_USERNAME_NAME_XPATH).clear()
        self.driver.find_element(By.XPATH, self.SEND_PPP_USERNAME_NAME_XPATH).send_keys(ppp_username)

    def send_ppp_password(self, ppp_password):
        self.driver.find_element(By.XPATH, self.SEND_PPP_PASSWORD_XPATH).clear()
        self.driver.find_element(By.XPATH, self.SEND_PPP_PASSWORD_XPATH).send_keys(ppp_password)

    def send_ppp_ac_name(self, ppp_ac_name):
        self.driver.find_element(By.XPATH, self.SEND_PPP_AC_NAME_XPATH).clear()
        self.driver.find_element(By.XPATH, self.SEND_PPP_AC_NAME_XPATH).send_keys(ppp_ac_name)

    def send_ppp_service_name(self, ppp_provider):
        self.driver.find_element(By.XPATH, self.SEND_PPP_SERVICE_XPATH).clear()
        self.driver.find_element(By.XPATH, self.SEND_PPP_SERVICE_XPATH).send_keys(ppp_provider)

    # PORT Mapping defines
    def port_mapping(self):
        port_checkboxes = self.driver.find_elements(By.XPATH, self.SELECT_ALL_PORT_MAPPING_XPATH)
        return port_checkboxes

    """ WAN Apply Elements """
    def click_wan_apply(self):
        self.driver.find_element(By.XPATH, self.CLICK_WAN_APPLY_BTN_XPATH).click()

    def click_wan_delete(self):
        self.driver.find_element(By.XPATH, self.CLICK_WAN_DELETE_BTN_XPATH).click()

    def verify_apply_ele(self):
        return self.driver.find_element(By.XPATH, self.VERIFY_APPLY_XPATH)

    def verify_apply_status(self):
        return self.driver.find_element(By.TAG_NAME, self.VERIFY_APPLY_TAG).text

    def click_ok_btn(self):
        self.driver.find_element(By.XPATH, self.CLICK_OK_BTN_XPATH).click()
    """
    def get_wan_list(self):
        elements = self.driver.find_elements(By.XPATH, self.GET_WAN_LIST_XPATH)
        ele_list = []
        for ele in elements:
            element = ele.text
            ele_list.append(element)
        return ele_list
    """
