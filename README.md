# tflocals

Example usage:
```
# Generate files
./run.sh ../directory/with/tf_files/

# Run terraform console on locals
echo 'keys(local.something)' | terraform -chdir=testlocals/ console
```
