### TODO

-------------------

• Bugfix Test of method AssociationRepository.save_payment

-------------------

• Take request.user from Pastaporto middleware
• Admin APIs
• Create Subscription without passing user_email (duplicated Customer on Stripe) or user_id (user_email becomes our PK, and so if it changes, the subscription will be lost)
• Handle subscriptions ad honorem for founders (no payments, add field `is_associated_forever`)
• Handle subscriptions for organizers (no payments, add field `manual_expiration_date`)
• Webhook Tests
• Test Repository methods proxy of Stripe ones
