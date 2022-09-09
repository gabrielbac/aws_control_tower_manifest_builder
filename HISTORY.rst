=======
History
=======

0.3.1 (2022-03-03)
------------------

* First release on PyPI.

0.4.0 (2022-03-27)
------------------

* Change to mantain order, comments and support exclamation marks in Cloudformation

0.4.1 (2022-03-27)
------------------

* Fix for the default region option

0.5.0 (2022-03-29)
------------------

* Add argument to set schema version

0.5.1 (2022-03-24)
------------------

* Fix issue when leaving region blank not picking default value

0.5.2 (2022-04-08)
------------------

* Fail if files name or name in metadata dont match regex

0.5.3 (2022-04-09)
------------------

* Fix in logging and update to Readme

0.5.4 (2022-04-18)
------------------

* Exit with error when there is an issue in any manifest file

0.6.0 (2022-05-18)
------------------

* Enforce description in SCP and correct extension

0.7.0 (2022-08-28)
------------------

* Added 2 new options
    --metadata-name -> to customize the name in the metadata
    --enforce-account-number-only ->  Allows to enforce use of 12 digit account numbers
    The input scps folder is not mandatory anymore

0.8.0 (2022-09-08)
------------------

* Added 1 new option
    --enable_stack_set_deletion -> defaults to False. Set to True to enable the CT pipeline to delete stacksets.