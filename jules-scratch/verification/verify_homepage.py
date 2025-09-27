from playwright.sync_api import sync_playwright, expect, TimeoutError

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            print("Navigating to http://localhost:5173/...")
            page.goto("http://localhost:5173/", timeout=30000)

            print("Waiting for page to reach 'load' state...")
            page.wait_for_load_state('load', timeout=15000)
            print("Page has loaded.")

            print("Waiting for Hero title...")
            hero_title = page.get_by_role("heading", name="Quantum Intelligence Quotient Unit")
            expect(hero_title).to_be_visible(timeout=10000) # Reduced timeout slightly
            print("Hero title is visible.")

            screenshot_path = "jules-scratch/verification/qiqu_homepage_styled.png"
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"Screenshot saved to {screenshot_path}")

        except Exception as e:
            print(f"An error occurred: {e}")
            # Capture HTML and screenshot for debugging
            html_content = page.content()
            with open("jules-scratch/verification/error_page.html", "w") as f:
                f.write(html_content)
            page.screenshot(path="jules-scratch/verification/error_screenshot.png")
            print("Saved error_page.html and error_screenshot.png for debugging.")
        finally:
            browser.close()

if __name__ == "__main__":
    run_verification()