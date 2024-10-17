# Usage

`zipcodelib` present a simple API.  Plugins that obtain and process data from
various source live in the `datasets/` subdirectory.  The `README.md` file
inside that directory describes the structure of a plugin, and the existing
examples should provide good templates to write additional ones.

Using the library consists simply of (optionally) refreshing the available
data, then using the `lookup()` function to generate additional features
associated with a zip code.  Note that since this data is, by definition,
aggregate--albeit across a small population--any particular traits of the zip
code population may or may not be relevant to the individual person or other
observation made within that zip code.

The pipeline utilizing `zipcodelib` may decide which generated features to
utilize.  All such features are present in the generated DataFrame, but the
usual Pandas APIs may be used to select only some columns of relevant to the
purpose at hand.  Because plugins may dynamically add features, consult the
results as run in your particular installation to see what columns (features)
are made available to you.

## zipcodelib-API example

```python
# We may want to refresh the available features using any
# plugins available under zipcodelib.datasets.  These can
# be loaded individually if preferred with datasets.load_FOO()
from zipcodelib import datasets
datasets.load_all()

# Example of results.  Any sequence of zipcodes is fine.  In
# most cases these will be a column from a Pandas DataFrame
# that contains zip codes for each customer order
zips = ['04930', '91024', '04930', '80303', '11436', '11213']

# The return value is a DataFrame with various columns (or a
# Series if only a single string is passed in).  Users can
# utilize whatever columns they wish.  More are added as plugins
# are written and added to directory
from zipcodelib import lookup
print(lookup(zips))
```
