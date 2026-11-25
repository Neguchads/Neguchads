# NAVI pilot — public profile

Complementary Python unittest gate covering profile rendering, public status
privacy and local Git publication fixtures. Does not publish anything or invoke
the real remote publisher. The existing daily build and Pages workflows remain
unchanged and authoritative. The token is read-only. No inherited secrets.
Core pin: 280e259cade8a1dd6d783c9daebbd57c1b771c8e.
Merge only after CI, restore-tested backup and rollout review. Revert the
integration commit for rollback. No required checks or rulesets changed.
