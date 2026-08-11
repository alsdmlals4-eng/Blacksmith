# BS-CONTENT-20260811-06 Regression Repair Receipt

- Decision: `BS-CONTENT-20260811-06`
- Previous current-state regression failure: prior-content tests still asserted current `5/10` / Decision05 after Decision06 became current.
- Repaired head: `b3cdb0d02b26316d01c7f48ff105c560705d8586`
- Scope of repair: current-state assertions only in Toren, Marek, Ersa, and Cassia contracts. Historical Decision IDs, individual approval slots, and protected content contracts were not rewritten.
- Router whitespace repair remains included from `794e28632c35ec884e5979c47b3507952e37e99e`.
- Health evidence hash repair remains included from `974c6ae2bb21aa01592dee23341c058b5e597680`.
- Required verdict: exact-head full PR GREEN before merge.
