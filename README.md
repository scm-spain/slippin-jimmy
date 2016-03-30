# Oozie workflow tools AKA Slippin Jimmy
Generating Oozie workflows can be a tedious task, coding XML is not awesome, so you can generate them from Jinja templates using the process_templates.py script.

## Installing the module
````
# make install
````
For user wide installation run
````
$ make install-user
````

## Running the script
The arguments not provided and mandatory are asked for during script execution:
````
jimmy -h
````

## Running the tests
Remember to remove the package before running the tests or the installed version will be used to run them
````
$ make test
````

## Components of the module
Slippin Jimmy is composed by the above components:
* Scribe: It creates the documentation and basic configuration from the Source database
* Valet: It provisions the cluster with the needed software
* Tlacuilo: It compiles the XML workflows from the YAML configuration
* Anabasii: It uploads the code to the cluster
* Cooper: Once the code has been uploaded it run the workflows
* Hersir: Execute compilation, upload and once is uploaded the code to the cluster run the workflows

![alt tag](http://i.imgur.com/zeLOD2s.jpg?1)