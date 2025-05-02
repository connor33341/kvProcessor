# TODO

### Documentation:
 - Create a doc/wiki with mkdocs
 - Update `README.md` to have basic examples for 0.2.x versions of the API

### Testing:
 - Update test.py to test for most usecases with the 0.2.x API
 - Use pytest aswell
 - Create a GHAction to makesure that all tests are passed.

### API:
 - Migrate to `kvprocessor.errors` for custom errors
 - Update cli to support 0.2.x verions of the API
 - Expand `kvprocessor.kvtypemap` to support more types.
 - Update `kvprocessor.kvmanifestloader` to be more feature rich
 - Fix the style, so it will lint correctly