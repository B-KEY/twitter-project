# -*- coding: utf-8 -*-
import uiautomator2 as u
import time
import random
import sys
import re
import io

# Fix Windows encoding issues and enable line buffering for real-time output
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)
else:
    # For non-Windows platforms, ensure unbuffered output
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)

# ====== YOUR USERNAMES (exact) ======
USERNAMES = [
    "XoDave11348",
    "humbled99",
    "ghostagain567",
    "New_nepali_",
    "NixonDave192913",
    "Thapabikey57613",
]

# ====== TIMING ======
MIN_DELAY = 3
MAX_DELAY = 7

# ====== RETRIES ======
DRAWER_OPEN_RETRIES = 4
SHEET_OPEN_RETRIES = 6
ROW_SCROLL_ATTEMPTS = 15

# ====== WIFI FALLBACK (optional) ======
# Set your phone's IP:port if you want WiFi fallback when USB not connected
# Example: WIFI_IP = "192.168.1.100:5555"
WIFI_IP = "192.168.0.105:35587"  # Set to None to disable WiFi fallback

# ====== DEVICE PIN (for auto-unlock) ======
import os
DEVICE_PIN = os.getenv("ANDROID_PIN", "2055")  # Set ANDROID_PIN env var to override

if len(sys.argv) < 2:
    print("Usage: python \"import uiautomator2 as u.py\" <tweet_url>")
    sys.exit(1)

TWEET_URL = sys.argv[1]

def connect_device():
    """Try USB first, fallback to WiFi if configured."""
    try:
        print("Attempting USB connection...")
        d = u.connect()
        print("[OK] Connected via USB")
        return d
    except Exception as e:
        if WIFI_IP:
            print(f"USB failed, trying WiFi at {WIFI_IP}...")
            try:
                d = u.connect(WIFI_IP)
                print("[OK] Connected via WiFi")
                return d
            except Exception as e2:
                print(f"[!] WiFi connection failed: {e2}")
        print(f"[!] USB connection failed: {e}")
        sys.exit(1)

d = connect_device()

def wait(t: float):
    time.sleep(t)

def is_screen_locked() -> bool:
    """Check if the device screen is locked."""
    try:
        # Method 1: Check screen state via info
        info = d.info
        if not info.get("screenOn", True):
            return True
        
        # Method 2: Check via dumpsys (more reliable for lock state)
        result = d.shell("dumpsys window | grep 'mDreamingLockscreen'").output.strip()
        if "mDreamingLockscreen=true" in result:
            return True
        
        # Method 3: Check if keyguard (lock screen) is showing
        result = d.shell("dumpsys window | grep 'mShowingLockscreen'").output.strip()
        if "mShowingLockscreen=true" in result:
            return True
            
        return False
    except Exception as e:
        print(f"[!] Could not check lock state: {e}")
        return False

def unlock_device():
    """Wake screen and unlock with PIN if locked."""
    try:
        print("Checking screen lock status...")
        
        if not is_screen_locked():
            print("[OK] Screen already unlocked")
            return True
        
        print("Screen is locked, unlocking...")
        
        # Wake the screen
        d.screen_on()
        wait(0.5)
        
        # Swipe up to reveal PIN pad (adjust coordinates if needed)
        d.swipe(360, 1400, 360, 600, 0.3)
        wait(1)
        
        # Enter PIN
        d.shell(f"input text {DEVICE_PIN}")
        wait(0.5)
        
        # Press Enter to confirm
        d.press("enter")
        wait(1.5)
        
        # Verify unlock succeeded
        if is_screen_locked():
            print("[!] Unlock failed - device still locked")
            return False
        
        print("[OK] Device unlocked successfully")
        return True
        
    except Exception as e:
        print(f"[!] Error during unlock: {e}")
        return False

def human_wait():
    time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))

def center(bounds):
    x1, y1, x2, y2 = bounds
    return (x1 + x2) // 2, (y1 + y2) // 2

def parse_bounds(b: str):
    m = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", b or "")
    if not m:
        return None
    return tuple(map(int, m.groups()))

def contains(b1, b2):
    x1, y1, x2, y2 = b1
    a1, b1y, a2, b2y = b2
    return x1 <= a1 and y1 <= b1y and x2 >= a2 and y2 >= b2y

def open_x_home():
    d.app_start("com.twitter.android")
    wait(4)

def get_dump():
    return d.dump_hierarchy(compressed=False)

# (debug helpers removed for a clean runtime)

def sheet_visible() -> bool:
    """Robust check that the Accounts bottom sheet is visible."""
    try:
        # Fast paths via uiautomator2
        if d(resourceId="com.twitter.android:id/design_bottom_sheet").exists:
            if d(text="Accounts").exists or d(textContains="Accounts").exists:
                return True
            # Fallback: check for common actions within the sheet
            if d(textContains="Add an existing account").exists or d(textContains="Create a new account").exists:
                return True
        # Fallback via raw dump parsing
        sb = get_sheet_bounds()
        if sb:
            # If we can find the header or action texts in the dump, treat as visible
            xml = get_dump()
            if ("text=\"Accounts\"" in xml) or ("Add an existing account" in xml) or ("Create a new account" in xml):
                return True
    except Exception:
        pass
    return False

def find_bounds_by(selector_type: str, value: str):
    xml = get_dump()
    if selector_type == "desc":
        patt = rf'content-desc="{re.escape(value)}"'
    elif selector_type == "id":
        patt = rf'resource-id="{re.escape(value)}"'
    elif selector_type == "text":
        patt = rf'text="{re.escape(value)}"'
    else:
        return None
    for m in re.finditer(r"<node[^>]+>", xml):
        node = m.group(0)
        if patt not in node:
            continue
        b = re.search(r'bounds="(\[[0-9,]+\]\[[0-9,]+\])"', node)
        if not b:
            continue
        cb = parse_bounds(b.group(1))
        if cb:
            return cb
    return None

def get_sheet_bounds():
    return find_bounds_by("id", "com.twitter.android:id/design_bottom_sheet")

def is_subscribe_screen():
    return d(text="Subscribe").exists and not d(text="Accounts").exists

def open_navigation_drawer():
    """Open the navigation drawer with a few gentle retries."""
    for attempt in range(DRAWER_OPEN_RETRIES):
        if d(resourceId="com.twitter.android:id/drawer").exists or bool(find_bounds_by("id", "com.twitter.android:id/drawer")):
            return True
        if d(description="Show navigation drawer").exists:
            d(description="Show navigation drawer").click()
            wait(1.0)
            if d(resourceId="com.twitter.android:id/drawer").exists or bool(find_bounds_by("id", "com.twitter.android:id/drawer")):
                return True
        # Fallback: left-edge swipe to open drawer
        d.swipe(5, 600, 500, 600, 0.25)
        wait(0.8)
        if d(resourceId="com.twitter.android:id/drawer").exists or bool(find_bounds_by("id", "com.twitter.android:id/drawer")):
            return True
    return d(resourceId="com.twitter.android:id/drawer").exists or bool(find_bounds_by("id", "com.twitter.android:id/drawer"))

def click_switch_accounts() -> bool:
    """Safely click the 'Switch accounts' control via multiple selector strategies."""
    # Prefer explicit descriptor
    if d(description="Switch accounts").exists:
        d(description="Switch accounts").click()
        return True
    # Then exact text
    if d(text="Switch accounts").exists:
        d(text="Switch accounts").click()
        return True
    # Text contains (localization or minor variants)
    if d(textContains="Switch accounts").exists:
        d(textContains="Switch accounts").click()
        return True
    # Fallback via parsed bounds
    b = find_bounds_by("desc", "Switch accounts") or find_bounds_by("text", "Switch accounts")
    if b:
        x, y = center(b)
        d.click(x, y)
        return True
    return False

def open_full_accounts_list():
    """Open Accounts sheet reliably, with retries and backoff."""
    # Try drawer path first; if it fails, open profile panel as alternate path
    if not open_navigation_drawer():
        d.click(100, 150)  # avatar area to open profile panel
        wait(1.0)

    # Avoid coordinate taps; use robust click for Switch accounts
    for attempt in range(3):
        if click_switch_accounts():
            # Short settling window, then verify sheet with backoff
            wait(0.8)
            for i in range(SHEET_OPEN_RETRIES):
                if sheet_visible():
                    return True
                if is_subscribe_screen():
                    d.press("back")
                    wait(1)
                wait(0.6)
        else:
            # If not found on first try, nudge via a gentle left-edge swipe to re-open drawer state
            d.swipe(5, 600, 500, 600, 0.25)
            wait(0.6)
    return sheet_visible()

def find_smallest_clickable_container_for(target_bounds, restrict_region):
    xml = get_dump()
    clickable_nodes = []
    for m in re.finditer(r"<node[^>]+>", xml):
        node = m.group(0)
        if ('clickable="true"' not in node) and ('focusable="true"' not in node):
            continue
        b = re.search(r'bounds="(\[[0-9,]+\]\[[0-9,]+\])"', node)
        if not b:
            continue
        cb = parse_bounds(b.group(1))
        if not cb:
            continue
        if restrict_region and not contains(restrict_region, cb):
            continue
        if not contains(cb, target_bounds):
            continue
        clickable_nodes.append(cb)
    if not clickable_nodes:
        return None
    clickable_nodes.sort(key=lambda b: (b[2]-b[0])*(b[3]-b[1]))
    return clickable_nodes[0]

def container_has_current_account_marker(container_bounds):
    xml = get_dump()
    for m in re.finditer(r"<node[^>]+>", xml):
        node = m.group(0)
        if 'content-desc="current account"' not in node:
            continue
        b = re.search(r'bounds="(\[[0-9,]+\]\[[0-9,]+\])"', node)
        if not b:
            continue
        cb = parse_bounds(b.group(1))
        if not cb:
            continue
        if contains(container_bounds, cb):
            return True
    return False

def swipe_inside_sheet(direction_down: bool = True):
    region = get_sheet_bounds()
    if not region:
        d.swipe(360, 1200, 360, 400, 0.2)
        wait(0.8)
        return
    x1, y1, x2, y2 = region
    mid_x = (x1 + x2) // 2
    start_y = y2 - 80
    end_y = y1 + 120
    if direction_down:
        d.swipe(mid_x, start_y, mid_x, end_y, 0.25)
    else:
        d.swipe(mid_x, end_y, mid_x, start_y, 0.25)
    wait(0.8)

def click_account_row_for(username: str) -> bool:
    target_text = f"@{username}"
    restrict_region = get_sheet_bounds()
    if not restrict_region:
        if sheet_visible():
            restrict_region = get_sheet_bounds()
        else:
            return False
    for attempt in range(ROW_SCROLL_ATTEMPTS):
        if d(text=target_text).exists:
            el = d(text=target_text)
            tb = el.info.get("bounds")
            if not tb:
                el.click()
                wait(3)
                return True
            target_bounds = (tb["left"], tb["top"], tb["right"], tb["bottom"])
            container = find_smallest_clickable_container_for(target_bounds, restrict_region)
            if container:
                if container_has_current_account_marker(container):
                    return True
                x, y = center(container)
                d.click(x, y)
            else:
                el.click()
            wait(4)
            return True
        swipe_inside_sheet(direction_down=True)
    return False

def switch_to_account(username: str) -> bool:
    if not open_full_accounts_list():
        print("[!] Could not open Accounts list")
        return False
    ok = click_account_row_for(username)
    if ok:
        print(f"[+] Switched to @{username}")
        return True
    print(f"[!] Could not find @{username} in accounts list")
    # back out cleanly
    d.press("back")
    wait(1)
    return False

def open_tweet():
    d.shell(f'am start -a android.intent.action.VIEW -d "{TWEET_URL}"')
    wait(4)

def like_if_needed():
    btn = d(resourceId="com.twitter.android:id/inline_like")
    if btn.exists:
        info = btn.info
        if info.get("selected") or info.get("checked"):
            print("    -> Already liked")
        else:
            btn.click()
            print("    [LIKED]")
            wait(1)

def repost_if_needed():
    btn = d(resourceId="com.twitter.android:id/inline_retweet")
    if not btn.exists:
        print("    [!] Repost button not found")
        return

    btn.click()
    wait(1)

    # If already reposted, X shows Undo
    if d(textContains="Undo").exists:
        print("    -> Already reposted")
        d.press("back")
        wait(1)
        return

    for t in ["Repost", "Retweet"]:
        if d(textContains=t).exists:
            d(textContains=t).click()
            print("    [REPOSTED]")
            wait(1)
            return

    print("    [!] Repost option not found")

# ========== RUN ==========
print(f"Starting automation for: {TWEET_URL}")
print(f"Processing {len(USERNAMES)} accounts...\n")

# Check and unlock device if needed
if not unlock_device():
    print("[!] Failed to unlock device - aborting")
    sys.exit(1)

open_x_home()

order = USERNAMES[:]
random.shuffle(order)

for user in order:
    if not switch_to_account(user):
        continue
    open_tweet()
    like_if_needed()
    repost_if_needed()
    human_wait()

print("\nDONE — all accounts processed safely")
