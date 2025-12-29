from playwright.sync_api import sync_playwright, expect
import time

def verify_modal_and_cart(page):
    print("Navigating to localhost:8000")
    page.goto("http://localhost:8000")

    # Wait for products to load
    print("Waiting for products...")
    page.wait_for_selector("#product-grid > div.bg-white", timeout=10000)

    # 1. Open Modal
    print("Clicking first product...")
    first_product = page.locator("#product-grid > div.bg-white").first
    first_product.click()

    # Wait for modal visibility
    modal = page.locator("#product-modal")
    expect(modal).to_be_visible()

    # Screenshot Modal
    print("Screenshotting Modal...")
    page.screenshot(path="/home/jules/verification/1_modal.png")

    # 2. Test Image Navigation in Modal
    print("Testing Image Navigation...")
    next_btn = page.locator("#modal-next-btn")
    if next_btn.is_visible():
        next_btn.click()
        page.wait_for_timeout(500) # Wait for fade
        page.screenshot(path="/home/jules/verification/2_modal_image_changed.png")

    # 3. Add to Cart from Modal
    print("Adding to Cart from Modal...")
    # Find button with 'Agregar' text
    add_btn = page.locator("#modal-controls button").filter(has_text="Agregar")
    if not add_btn.is_visible():
         print("Add button not found or visible (Maybe already added?)")
    else:
         add_btn.click()
         # Check if controls changed to [-] 1 [+]
         # Use a more specific selector to avoid strict mode violation
         controls_container = page.locator("#modal-controls > div.rounded-xl")
         expect(controls_container).to_be_visible()
         page.screenshot(path="/home/jules/verification/3_modal_added.png")

    # 4. Close Modal
    print("Closing Modal...")
    # Close button is the absolute positioned X
    close_btn = page.locator("#product-modal > div > div > button")
    close_btn.click()
    expect(modal).to_be_hidden()

    # 5. Check Grid Button
    print("Checking Grid Button...")
    # The first product card should now have [-] 1 [+]
    # The grid control has a span with the quantity
    grid_qty = first_product.locator("span.text-center").filter(has_text="1")
    expect(grid_qty).to_be_visible()
    page.screenshot(path="/home/jules/verification/4_grid_controls.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            verify_modal_and_cart(page)
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
            page.screenshot(path="/home/jules/verification/error.png")
        finally:
            browser.close()
