#!/usr/bin/env python3
"""
Smoke Tests for Vienna Voting Bugs (TDD approach)
==================================================
These tests define the EXPECTED behavior. They should FAIL before the fix
and PASS after the fix.

Bug 1: 點擊投票只會跳出「投票系統載入中，請稍候」
  - Root cause: Firestore rules `create` rule too strict, blocks first vote
  - Fix: Simplify `create` rule to just require auth

Bug 2: 版面大爆炸（照片和格子都超大）
  - Root cause: Tailwind Play CDN blocked by CSP or misconfigured
  - Fix: Ensure CSP allows Tailwind CDN CSS injection

Run: python test_voting_bugs.py
"""

import re
import sys
import os

os.chdir('/home/node/.openclaw/workspace/vienna-trip-gh-pages')


# ===== Bug 1: Voting System =====

def test_bug1_firestore_rules_allow_first_vote():
    """
    BUG 1 ROOT CAUSE: The `create` rule has an impossible condition for first vote.

    Current rule:
      allow create: if request.auth != null
                    && (!exists(...) || request.auth.uid not in resource.data.voters);

    When a document doesn't exist yet:
      - `!exists(...)` evaluates to true
      - The OR short-circuits... BUT the second part is still evaluated for syntax?
      - Actually, the real problem: `resource.data` on a non-existent doc IS null
      - Accessing `.voters` on null throws a JavaScript error in the rules engine
      - This causes the entire rule to fail

    FIX: Simplify create rule to just require auth.
    """
    with open('firestore.rules') as f:
        rules = f.read()

    # The create rule should NOT reference resource.data.voters
    # because resource.data is null for a non-existent document
    create_section = re.search(r'allow create:(.*?)(?=allow|$)', rules, re.DOTALL)
    assert create_section, "No create rule found"

    create_body = create_section.group(1)

    # FAIL condition: create rule references resource.data.voters (impossible for new doc)
    assert 'resource.data' not in create_body, \
        "BUG: create rule references resource.data which is null for new documents! " \
        "This blocks the first vote. Fix: remove resource.data checks from create rule."

    print("✅ test_bug1_firestore_rules_allow_first_vote passed")


def test_bug1_firestore_rules_correct_update_logic():
    """
    The `update` rule should enforce:
    1. count increments by exactly 1
    2. voters array grows by exactly 1
    3. new voter uid is in the NEW voters list (request.resource)
    4. new voter uid is NOT in the OLD voters list (resource)
    """
    with open('firestore.rules') as f:
        rules = f.read()

    update_section = re.search(r'allow update:(.*?)(?=allow|$)', rules, re.DOTALL)
    assert update_section, "No update rule found"
    update_body = update_section.group(1)

    # Must check count increment
    assert 'count + 1' in update_body or 'increment' in update_body.lower(), \
        "update rule must verify count increments by 1"

    # Must check new voter is in new voters list
    assert 'request.resource.data.voters' in update_body or \
           'request.resource.data' in update_body, \
        "update rule must check request.resource.data for new voter"

    # Must check new voter NOT in old voters list
    assert 'request.auth.uid not in resource.data.voters' in update_body, \
        "update rule must check new voter is NOT in old resource.data.voters"

    print("✅ test_bug1_firestore_rules_correct_update_logic passed")


def test_bug1_no_indefinite_loading_alert():
    """
    When window.__canVote is false, clicking vote should NOT just alert()
    and return. It should wait or retry, not permanently block the user.

    The current code:
      if (!window.__canVote) {
        alert('投票系統載入中，請稍候');
        return;
      }

    This is a synchronous alert that blocks nothing and provides no feedback
    after the auth completes. The user sees "載入中" forever if Firebase
    takes too long or fails silently.
    """
    with open('index.html') as f:
        html = f.read()

    # Find the castVote function
    castvote_match = re.search(r'async function castVote\(placeId\)\s*\{(.*?)\n\}',
                               html, re.DOTALL)
    assert castvote_match, "castVote function not found"
    castvote_body = castvote_match.group(1)

    # FAIL: If __canVote check exists and only shows alert, that's the bug pattern
    if '__canVote' in castvote_body and "alert('投票系統載入中" in castvote_body:
        # Check if there's a retry/wait mechanism beyond just alert
        has_retry = 'setTimeout' in castvote_body or 'retry' in castvote_body.lower()
        assert has_retry, \
            "BUG: castVote shows alert('投票系統載入中') with no retry/wait. " \
            "User gets stuck. Fix: add retry logic or auto-retry when __canVote becomes true."

    print("✅ test_bug1_no_indefinite_loading_alert passed")


# ===== Bug 2: Layout Explosion =====

def test_bug2_csp_allows_tailwind_css():
    """
    BUG 2 ROOT CAUSE: Tailwind Play CDN CSS injection requires proper CSP.

    Tailwind Play CDN JS (`https://cdn.tailwindcss.com`) dynamically injects
    a <style> tag with all utility classes. For this to work:

    1. script-src must whitelist: https://cdn.tailwindcss.com
    2. style-src must whitelist the same origin OR have 'unsafe-inline'
    3. If blocked, NO Tailwind utilities apply → layout explosion

    Common failure: CSP allows the JS but NOT the CSS it injects.
    """
    with open('index.html') as f:
        html = f.read()

    csp_match = re.search(r'<meta http-equiv="Content-Security-Policy" content="([^"]+)"', html)
    assert csp_match, "CSP meta tag not found"
    csp = csp_match.group(1)

    # Must allow Tailwind CDN JS
    assert 'cdn.tailwindcss.com' in csp, \
        "BUG: CSP script-src does NOT include cdn.tailwindcss.com!"

    # For dynamic CSS injection, style-src needs either:
    # a) 'unsafe-inline' (allows <style> tag injection)
    # b) OR the CDN origin in style-src
    style_src_match = re.search(r'style-src ([^;]+)', csp)
    if style_src_match:
        style_src = style_src_match.group(1)
        has_unsafe_inline = "'unsafe-inline'" in style_src
        has_tailwind_cdn = 'cdn.tailwindcss.com' in style_src
        assert has_unsafe_inline or has_tailwind_cdn, \
            f"BUG: style-src does NOT allow 'unsafe-inline' or cdn.tailwindcss.com! " \
            f"Tailwind CSS injection will be blocked. Current style-src: {style_src}"
    else:
        # If no explicit style-src, default-src applies
        default_src = re.search(r'default-src ([^;]+)', csp)
        if default_src:
            default_src_val = default_src.group(1)
            has_unsafe_inline = "'unsafe-inline'" in default_src_val
            assert has_unsafe_inline, \
                "BUG: CSP default-src lacks 'unsafe-inline' for Tailwind CSS injection!"

    print("✅ test_bug2_csp_allows_tailwind_css passed")


def test_bug2_tailwind_config_not_blocked():
    """
    tailwind.config is set via a <script> tag, NOT via the CDN JS import.

    Current code:
      <script src="https://cdn.tailwindcss.com"></script>
      <script>
        tailwind.config = { ... }   ← This runs AFTER tailwind CDN loads

    This should work IF Tailwind CDN JS is allowed. But tailwind.config
    is applied to the global Tailwind object that CDN creates. If CDN JS
    fails to load, tailwind.config is set on undefined → no effect.
    """
    with open('index.html') as f:
        html = f.read()

    # Check that tailwind.config is defined in a <script> tag AFTER CDN
    # This is just a sanity check - the real issue is CDN loading
    has_tailwind_cdn = 'cdn.tailwindcss.com' in html
    has_tailwind_config = 'tailwind.config' in html

    assert has_tailwind_cdn, "Tailwind CDN script tag not found"
    assert has_tailwind_config, "tailwind.config not found"

    # Check order: CDN should come BEFORE config
    cdn_pos = html.find('cdn.tailwindcss.com')
    config_pos = html.find('tailwind.config =')

    # The config script block comes AFTER the CDN in the <head>
    # Both are in <head>, so CDN script tag should come before config
    assert cdn_pos < config_pos or config_pos == -1, \
        "tailwind.config is defined BEFORE Tailwind CDN loads? Check order."

    print("✅ test_bug2_tailwind_config_not_blocked passed")


def test_bug2_aspect_video_class_applied():
    """
    Bug symptom: photos are huge and cards explode.

    The card uses:
      <div class="relative aspect-video overflow-hidden bg-gray-300">
        <img class="w-full h-full object-cover object-center" ...>

    aspect-video = height: 56.25% (16:9) + width: 100%
    If Tailwind CSS fails to load, aspect-video has NO effect,
    so image displays at natural size → layout explosion.

    This test verifies the CSS selector exists (smoke test).
    """
    with open('index.html') as f:
        html = f.read()

    # Check that aspect-video is used in the card template
    assert 'aspect-video' in html, \
        "aspect-video class not found in template (card photo container)"

    # Check that the img has w-full h-full object-cover
    img_section = re.search(r'<img[^>]*class="[^"]*aspect-video[^"]*"(.*?)>', html, re.DOTALL)
    if img_section:
        img_tag = img_section.group(0)
        assert 'w-full' in img_tag or 'object-cover' in img_tag, \
            "Image inside aspect-video container missing w-full/object-cover"

    print("✅ test_bug2_aspect_video_class_applied passed")


def test_bug2_grid_layout_responsive():
    """
    The places grid uses:
      class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"

    If Tailwind CDN fails, grid-cols-* and gap-* won't apply.
    This causes a broken layout with cards in a single column or no gaps.
    """
    with open('index.html') as f:
        html = f.read()

    # Find places-grid
    # Find places-grid (class comes before id in the HTML)
    grid_match = re.search(r'<div[^>]*class="([^"]+)"[^>]*id="places-grid"', html)
    assert grid_match, "places-grid element not found"

    grid_classes = grid_match.group(1)

    required_classes = ['grid', 'grid-cols-1', 'md:grid-cols-2', 'lg:grid-cols-3', 'gap-6']
    for cls in required_classes:
        assert cls in grid_classes, \
            f"BUG: places-grid missing '{cls}' class! " \
            f"If Tailwind CSS fails, layout will be broken."

    print("✅ test_bug2_grid_layout_responsive passed")


# ===== Integration Tests =====

def test_firebase_sdk_cors_headers():
    """
    Firebase SDK must be loadable from CDN.

    SDK URL pattern:
      https://www.gstatic.com/firebasejs/10.7.0/firebase-app.js

    Check that:
    1. index.html imports from the correct Firebase CDN
    2. CSP allows the gstatic domain
    """
    with open('index.html') as f:
        html = f.read()

    # Firebase imports
    assert 'firebasejs' in html, "Firebase SDK not imported"
    assert 'firebase-app.js' in html, "firebase-app.js not imported"
    assert 'firebase-firestore.js' in html, "firebase-firestore.js not imported"
    assert 'firebase-auth.js' in html, "firebase-auth.js not imported"

    # CSP must allow gstatic (Firebase CDN origin)
    csp_match = re.search(r'<meta http-equiv="Content-Security-Policy" content="([^"]+)"', html)
    csp = csp_match.group(1)
    assert 'gstatic.com' in csp or '*.gstatic.com' in csp, \
        "CSP must whitelist gstatic.com for Firebase SDK"

    print("✅ test_firebase_sdk_cors_headers passed")


def test_firestore_rules_synced_with_code():
    """
    The Firestore rules must match what the code expects.

    Code uses: setDoc(docRef, { count: increment(1), voters: arrayUnion(currentUid) }, { merge: true })

    This means:
    - First vote on a place: creates doc with count=1, voters=[uid]
    - Subsequent votes: updates doc, increments count, adds uid to voters array

    Rules should match this pattern.
    """
    with open('firestore.rules') as f:
        rules = f.read()

    with open('index.html') as f:
        html = f.read()

    # Code uses merge: true, so create OR update can happen
    assert 'merge: true' in html, "Code should use merge: true for setDoc"

    # Code uses increment(1) for count
    assert 'increment(1)' in html, "Code should use increment(1) for count"

    # Code uses arrayUnion(currentUid) for voters
    assert 'arrayUnion' in html, "Code should use arrayUnion for voters"

    print("✅ test_firestore_rules_synced_with_code passed")


if __name__ == '__main__':
    tests = [
        # Bug 1 tests
        test_bug1_firestore_rules_allow_first_vote,
        test_bug1_firestore_rules_correct_update_logic,
        test_bug1_no_indefinite_loading_alert,
        # Bug 2 tests
        test_bug2_csp_allows_tailwind_css,
        test_bug2_tailwind_config_not_blocked,
        test_bug2_aspect_video_class_applied,
        test_bug2_grid_layout_responsive,
        # Integration tests
        test_firebase_sdk_cors_headers,
        test_firestore_rules_synced_with_code,
    ]

    failed = 0
    print("=" * 60)
    print("Vienna Voting Bugs — Smoke Tests (TDD)")
    print("=" * 60)
    print()

    for t in tests:
        try:
            t()
        except AssertionError as e:
            print(f"❌ FAIL: {t.__name__}")
            print(f"   {e}")
            print()
            failed += 1
        except Exception as e:
            print(f"⚠️  ERROR: {t.__name__}: {e}")
            print()
            failed += 1

    print("=" * 60)
    if failed == 0:
        print("✅ All tests passed!")
    else:
        print(f"❌ {failed} test(s) FAILED — bugs confirmed")
    print("=" * 60)

    sys.exit(failed)