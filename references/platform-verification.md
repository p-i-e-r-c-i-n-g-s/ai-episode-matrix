# Platform verification

Platform adapters are not permanent API documentation. Before using a named engine, verify its current model/interface, input types, reference syntax, duration/aspect controls, audio behavior, and output limits from the platform's current documentation or UI.

Record `verified_at`, `verified_source`, and `interface_version` in the working prompt pack or take record. If verification is unavailable, keep the control under `UNVERIFIED` and write a model-agnostic prompt. Recheck an adapter when the platform announces a model/interface change or at least once per quarter for active productions.

The repository's tests validate prompt structure offline. They do not spend credits or claim that a vendor generation succeeded.
