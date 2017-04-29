
import sys, subprocess, os
 
DATABASE = sys.argv[1]
 
subprocess.call(["mdb-schema", DATABASE, "mysql"])
 
table_names = subprocess.Popen(["mdb-tables", "-1", DATABASE],
                               stdout=subprocess.PIPE).communicate()[0]
tables = table_names.splitlines()
 
print("BEGIN") 
sys.stdout.flush()
for table in tables:
    if table != '':
        subprocess.call(["mdb-export", "-I", "mysql", DATABASE, table])
 
print("COMMIT")
sys.stdout.flush()
