Setup
-----

Create the conda environment and use it:
```
conda create -n componentsDB --file requirements.txt
conda activate componentsDB
```

Testing
-------
Testing uses `unittest` module, should be already available.

`python testing.py`

Tests are run and if everything is ok no errors is issued.

If you want to see how the code is transformed to SQL calls,
change the `VERBOSITY` flag in `dbclasses.py` file.

Understanding the code
----------------------
The file `dbclasses.py` defines a set of components objects
that are stored in the database. There are two components 
type each with one parameter (a number): `Quadrupole` and 
`Crystal`.

Components can be grouped together to form a compound object.

To see an example of how to fill and query the database, 
check the `testing.py` file. In particular check the methods:
`test1_add*` to see how to add components to the database 
starting from python instances of objects and `test2_read*` 
functions to see how to query the database.

The database is of type `sqlite3` and is in memory, modify
the funciton `dbclasses.initialize` to store the database
in a single file.

Single table vs multiple tables
-------------------------------
When objects are persistified in the database from python
two possible approaches are possible:
 1. Store every data in a single giant table that will 
    contain all data from all possible components type in 
    separate columns (as it is now the AD database)
 2. Store each component type in a separate table.

 According to blog posts the former should be more efficient
 in terms of CPU speed, but the latter is much better for DB 
 design and makes everything readable. However switching
 between the two is a very simple matter, change the value 
 of the variable `USE_SEPARATE_TABLES` in `dblcasses.py` 
 file.

