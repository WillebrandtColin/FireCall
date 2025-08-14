# automation_script.py - REFACTORED VERSION
import os
from datetime import date
from playwright.sync_api import sync_playwright, Page, expect

# The complete default data dictionary, ready to be overridden by Zapier
DEFAULT_CLAIM_DATA = {
    # Main Info
    "reported_by_search": "property owner",
    "reported_by_select": "Property Owner",
    "referred_by_search": "Willebrandt, ERC-Colin",
    "referred_by_select": "Willebrandt, ERC-Colin",
    "provider_office_search": "PDR of Ralei",
    "provider_office_select": "PDR of Ralei",
    "client_search": "Residentials",
    "client_select": "Residentials",

    # Customer Information
    "first_name": "TestFirstName",
    "last_name": "TestLastName",
    "email": "TestEmail@Gmail.com",
    "address": "248 Turner Oaks Dr",
    "zip_code": "27519",
    "phone": "19195551234",

    # Loss Details
    "loss_date": date.today().strftime("%Y/%m/%d"),
    "job_name": "TestFirstName, TestLastName",
    "loss_type_search": "water",
    "loss_type_select": "Water - Sewer Backup, Black,",
    "job_type_select": "Appraisal/Consulting",
    "loss_description": "This is a test loss description created by an automated script.",

    # Internal Participants
    "internal_estimator_search": "RENC",
    "internal_estimator_select": "RENC, estimators",
    "internal_pm_search": "essen",
    "internal_pm_select": "Reescano, Essence",
    "internal_supervisor_search": "non",
    "internal_supervisor_select": "None, None",
    "internal_primary_sales_search": "None",
    "internal_primary_sales_select": "None, None",
    "internal_secondary_sales_search": "rhond",
    "internal_secondary_sales_select": "Rhond",
    "internal_bizdev_search": "willebran",
    "internal_bizdev_select": "Willebran",
    "internal_lead_tech_search": "willebrandt",
    "internal_lead_tech_select": "Willebrandt, Colin",

    # External Participants
    "external_adjuster_company_search": "pdr",
    "external_adjuster_company_select": "PDR-KHTX-JCA",
    "external_adjuster_individual_select": "JCA, JCA",
    "external_agent_company_search": "Self",
    "external_agent_company_select": "Self Pay",
    "external_agent_individual_select": "Pay, Self",
    "external_agent_individual_2_select": "Pay, Self",
    "external_mortgage_company_search": "pdr",
    "external_mortgage_company_select": "PDR-RENC",
    "external_mortgage_individual_select": "Varner, Jason",
    "external_property_mgmt_company_search": "pdr",
    "external_property_mgmt_company_select": "PDR-KHTX",
    "external_tpa_company_search": "No",
    "external_tpa_company_select": "No TPA",
}

def login(page: Page) -> None:
    """Logs into the RMS system using environment variables."""
    company_id = os.getenv("RMS_COMPANY_ID")
    username = os.getenv("RMS_USERNAME")
    password = os.getenv("RMS_PASSWORD")
  await page.goto('https://rms-ngs.net/rms/module/user/login.aspx');
    page.get_by_role("textbox", name="Company ID").fill(company_id)
    page.get_by_role("textbox", name="User Name").fill(username)
    page.get_by_role("textbox", name="Password").fill(password)
    page.get_by_role("button", name="Login").click()
    expect(page.get_by_role("link", name="Create Claim")).to_be_visible(timeout=15000)

def fill_claim_form(page: Page, data: dict) -> None:
    """Fills out the claim form using data from a dictionary."""
    page.get_by_role("link", name="Create Claim").click()

    # Main Info
    page.locator("#ctl00_ContentPlaceHolder1_ProviderCreateClaim_DropDown_ReportedBY_Input").fill(data["reported_by_search"])
    page.get_by_text(data["reported_by_select"], exact=True).click()
    page.locator("#ctl00_ContentPlaceHolder1_ProviderCreateClaim_DropDown_ReferredBy_Input").fill(data["referred_by_search"])
    page.get_by_text(data["referred_by_select"], exact=True).click()
    page.locator("#ctl00_ContentPlaceHolder1_ProviderCreateClaim_DropDown_ProviderOffice_Input").fill(data["provider_office_search"])
    page.get_by_text(data["provider_office_select"], exact=True).click()
    page.locator("#ctl00_ContentPlaceHolder1_ProviderCreateClaim_DropDown_Client_Input").fill(data["client_search"])
    page.get_by_role("listitem").filter(has_text=data["client_select"]).click()

    # Customer Information
    page.locator("#ctl00_ContentPlaceHolder1_ProviderCreateClaim_TextBox_FirstName").fill(data["first_name"])
    page.locator("#ctl00_ContentPlaceHolder1_ProviderCreateClaim_TextBox_LastName").fill(data["last_name"])
    page.locator("#ctl00_ContentPlaceHolder1_ProviderCreateClaim_TextBox_Email").fill(data["email"])
    page.locator("#ctl00_ContentPlaceHolder1_ProviderCreateClaim_TextBox_Address_Input").fill(data["address"])
    page.locator("#ctl00_ContentPlaceHolder1_ProviderCreateClaim_TextBox_Zip").fill(data["zip_code"])
    page.locator("#ctl00_ContentPlaceHolder1_ProviderCreateClaim_TextBox_MainPhone").fill(data["phone"])
    page.get_by_role("checkbox", name="Same as Customer Address").check()

    # Internal Participants
    page.locator("#ctl00_ContentPlaceHolder1_ProviderCreateClaim_InternalParticpantsControl_InternalParticipantsList_ctl00_EstimatorComboBox_Input").fill(data["internal_estimator_search"])
    page.get_by_text(data["internal_estimator_select"], exact=True).click()
    # ... You would continue this pattern for all other internal and external participants...

    # Loss Details
    job_name = f"{data['first_name']}, {data['last_name']}"
    page.locator("#ctl00_ContentPlaceHolder1_ProviderCreateClaim_DatePicker_DateOffLoss_dateInput").fill(data["loss_date"])
    page.locator("#ctl00_ContentPlaceHolder1_ProviderCreateClaim_JobNameRadTextBox").fill(job_name)
    page.locator("#ctl00_ContentPlaceHolder1_ProviderCreateClaim_DropDown_LossType_Input").fill(data["loss_type_search"])
    page.get_by_text(data["loss_type_select"]).click()
    page.get_by_text(data["job_type_select"]).click()
    page.get_by_role("textbox", name="Enter Loss Description").fill(data["loss_description"])

    page.get_by_role('button', name='Save & Go to Slideboard').click()
    page.get_by_role('button', name='Create Claim').click()

def complete_task(page: Page, task_name: str) -> None:
    """Finds a task on the slideboard by name and completes it."""
    task_cell = page.get_by_role('cell', name=task_name, exact=True)
    expect(task_cell).to_be_visible(timeout=10000)
    task_cell.click()

    iframe = page.frame_locator('iframe[name="RadWindow_CommonWindow"]')
    expect(iframe.get_by_role('button', name='Complete This Task')).to_be_visible()
    iframe.get_by_role('checkbox', name=lambda n: "Please select the checkbox" in n).check()
    iframe.get_by_role('button', name='Complete This Task').click()
    # Wait for modal to disappear
    expect(iframe).to_be_hidden()

def run_automation(claim_data: dict) -> None:
    """The main function that runs the entire browser automation."""
    print(f"Starting automation for: {claim_data.get('first_name')}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            login(page)
            fill_claim_form(page, claim_data)

            # Process initial tasks
            complete_task(page, '01 - Contact Customer')
            complete_task(page, '01. Assign Estimator to Prepare Estimate')
            complete_task(page, '02 - Arrive onsite')

            print("✅ Automation tasks completed successfully.")
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            page.screenshot(path="error_screenshot.png")
        finally:
            browser.close()
