#!/usr/bin/env python3
"""Smoke tests for Vienna voting feature"""
import re
import sys

def test_csp_updated():
    with open('index.html') as f:
        html = f.read()
    assert 'firebaseio.com' in html, "CSP should allow Firebase CDN"
    assert 'googleapis.com' in html, "CSP should allow Google APIs"
    assert 'gstatic.com' in html, "CSP should allow Gstatic"
    print("✅ CSP updated correctly")

def test_firebase_sdk_imported():
    with open('index.html') as f:
        html = f.read()
    assert 'firebase-app.js' in html
    assert 'firebase-auth.js' in html
    assert 'firebase-firestore.js' in html
    assert "type=\"module\"" in html
    print("✅ Firebase SDK imported")

def test_anonymous_auth():
    with open('index.html') as f:
        html = f.read()
    assert 'signInAnonymously' in html
    assert 'onAuthStateChanged' in html
    assert 'voted_places' in html
    print("✅ Anonymous auth implemented")

def test_vote_handler():
    with open('index.html') as f:
        html = f.read()
    assert 'castVote' in html
    assert 'increment(1)' in html
    assert 'arrayUnion(currentUid)' in html
    assert 'votedPlaces' in html
    print("✅ Vote handler implemented")

def test_vote_ui():
    with open('index.html') as f:
        html = f.read()
    assert 'vote-btn' in html
    assert '👍' in html
    assert 'vote-check' in html
    print("✅ Vote UI implemented")

def test_firestore_rules():
    with open('firestore.rules') as f:
        rules = f.read()
    assert 'allow read: if true' in rules
    assert 'allow create: if request.auth != null' in rules
    assert 'allow delete: if false' in rules
    assert 'request.auth.uid not in resource.data.voters' in rules
    print("✅ Firestore rules valid")

def test_no_votes_in_places_json():
    import json
    with open('places.json') as f:
        data = json.load(f)
    for p in data.get('places', []):
        assert 'votes' not in p, f"places.json should not have votes field for {p.get('id')}"
    print("✅ places.json unchanged (no votes field)")

if __name__ == '__main__':
    import os
    os.chdir('/home/node/.openclaw/workspace/vienna-trip-gh-pages')
    tests = [
        test_csp_updated,
        test_firebase_sdk_imported,
        test_anonymous_auth,
        test_vote_handler,
        test_vote_ui,
        test_firestore_rules,
        test_no_votes_in_places_json,
    ]
    failed = 0
    for t in tests:
        try:
            t()
        except AssertionError as e:
            print(f"❌ {t.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {t.__name__}: {e}")
            failed += 1
    print(f"\n{'✅ All tests passed!' if failed == 0 else f'❌ {failed} test(s) failed'}")
    sys.exit(failed)