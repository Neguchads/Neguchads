# NAVI pilot — public profile

Complementary Python unittest gate covering profile rendering, public status
privacy and local Git publication fixtures. Does not publish anything or invoke
the real remote publisher. The existing daily build and Pages workflows remain
unchanged and authoritative. The token is read-only. No inherited secrets.
Core pin: e9fa2e4c825615ddc6f0a24b65d7139ec38fc477.
Merge only after CI, restore-tested backup and rollout review. Revert the
integration commit for rollback. No required checks or rulesets changed.


Validated release candidate: NAVI Core v0.2.0rc1. Complementary gate only; original CI and branch governance unchanged.
