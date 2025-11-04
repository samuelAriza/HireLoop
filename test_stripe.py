#!/usr/bin/env python
"""Test script to verify Stripe configuration"""
import os
import django
from dotenv import load_dotenv

load_dotenv()

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hireloop.settings')
django.setup()

import stripe
from django.conf import settings

print("=" * 60)
print("STRIPE CONFIGURATION TEST")
print("=" * 60)

# Check if keys are loaded
print(f"\n1. STRIPE_SECRET_KEY loaded: {bool(settings.STRIPE_SECRET_KEY)}")
print(f"   Length: {len(settings.STRIPE_SECRET_KEY)}")
print(f"   Starts with: {settings.STRIPE_SECRET_KEY[:15]}...")

print(f"\n2. STRIPE_PUBLIC_KEY loaded: {bool(settings.STRIPE_PUBLIC_KEY)}")
print(f"   Length: {len(settings.STRIPE_PUBLIC_KEY)}")
print(f"   Starts with: {settings.STRIPE_PUBLIC_KEY[:15]}...")

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

print("\n3. Testing Stripe API connection...")
try:
    # Test API with a simple call
    balance = stripe.Balance.retrieve()
    print(f"   ✓ Connection successful!")
    print(f"   Available balance: {balance.available}")
except stripe.error.AuthenticationError as e:
    print(f"   ✗ Authentication failed: {e}")
except stripe.error.StripeError as e:
    print(f"   ✗ Stripe error: {e}")
except Exception as e:
    print(f"   ✗ Unexpected error: {e}")

print("\n4. Testing Checkout Session creation...")
try:
    # Create a test checkout session
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "unit_amount": 1000,  # $10.00
                "product_data": {
                    "name": "Test Product",
                },
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
    )
    print(f"   ✓ Session created successfully!")
    print(f"   Session ID: {session.id}")
    print(f"   Session URL: {session.url}")
except stripe.error.InvalidRequestError as e:
    print(f"   ✗ Invalid request: {e}")
except stripe.error.StripeError as e:
    print(f"   ✗ Stripe error: {e}")
except Exception as e:
    print(f"   ✗ Unexpected error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
