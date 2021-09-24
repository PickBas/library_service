pylint $(python ./ci_tools/pylint/pylint_getting_files.py) --load-plugins pylint_django --disable=F0401,R0901,E5142,R1710,E5110,C0209 | tee ./ci_tools/pylint/file.txt
python ./ci_tools/pylint/pylint_get_score.py

exit $?
