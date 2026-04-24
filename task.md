The task is to *produce a Python program* that executes the following task:

1. Read a file containing tax data for one or more persons
2. Perform table-based calculation based on wage income for a taxpayer in Eastern Norway. The rules for the table-based
   calculation can be found in the file [tax.md](tax.md)
3. Produce a file with calculated tax per year

The program should written from scratch as a stand-alone project, in the output directory given by the `$FILE_DIR`
environment variable.

The program should accept a single input file as an argument and produce the answer on stdout.

The project directory should contain a `README.md` file with instructions on how to run the program. For evaluation
purposes, the README file should contain a section saying when the project was initiated, and when it was completed. The
timestamps should be in a resolution of seconds.

Example input file, with two taxpayers where name, age, and income are provided:

```
Roger Rud
50 years
125 000 NOK

Per Høneeier
42 years
7 000 000 NOK
```

Example result output, where the taxpayers are listed with tax owed:

```
Roger Rud
20 000 NOK

Per Hønseeier
1 000 000
```
