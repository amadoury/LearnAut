
both:
	python3 examples.py && mvn clean compile exec:java -Dexec.args="data.txt"
 
java:
	mvn clean compile exec:java -Dexec.args="data.txt"
py:
	python3 example.py
