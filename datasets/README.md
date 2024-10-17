This directory contains multiple plugins that can obtain data
associated with a zipcode.  A plugin is a file named
`load_SOMETHING.py` that contains a function named `_run()` that
has zero non-optional arguments.  Meta-loaders generate synthetic
features from (multiple) loaded ones.  They are named like
`make_SOMETHING.py` and should run after cached files are
available.

Plugins are exposed as functions named after their filename,
minus the extension.  For example, placing the mentioned file 
here would allow users to run this:

    >>> import datasets
    >>> datasets.load_SOMETHING()
    [... progress shown ...]

In general, a loader will perform several tasks:

  1. Download some data from a publicly available source.
  2. Massage the data to extract just the relevant features
     associated with a zipcode.  Ideally, most or all US 
     zipcodes will be available from a data source, but
     incomplete data is still useful.
  3. Usually intermediate data is stored in the `cache/`
     directory to avoid the need for downloading every time a
     loader is run.
  4. Transform the data file(s) obtained to extract single
     features.  A feature file is in CSV format with the headers:
     `ZIPCODE,Feature1[,Feature2[,...]]`.  The file should be named 
     `features/FEATURE_TYPE.csv` (for some reasonable
     description of the type of features obtained.
  5. One loader may derive multiple features. Depending on what
     these are and how they are derived, either one or multiple
     feature files may be created.  In particular, if a 
     categorical feature is obtained, it may make sense to 
     one-hot encode it within the loader.
