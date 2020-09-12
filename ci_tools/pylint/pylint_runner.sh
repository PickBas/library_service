pylint $(python ./ci_tools/pylint/pylint_getting_files.py) --load-plugins pylint_django --disable=F0401,R0901 | tee ./ci_tools/pylint/file.txt
python ./ci_tools/pylint/pylint_get_score.py

exit $?
