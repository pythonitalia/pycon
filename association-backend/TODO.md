### TODO

-------------------

• Bugfix Test of method AssociationRepository.save_payment

• Refactoring of Mutation test to mock stripe repository methods instead of the service

-------------------

• Take request.user from Pastaporto middleware

• Admin APIs

• Handle subscriptions ad honorem for founders (no payments, add field `is_associated_forever`)

• Handle subscriptions for organizers (no payments, add field `manual_expiration_date`)

• Webhook Tests (Very Expensive)

• Test Repository methods proxy of Stripe ones
