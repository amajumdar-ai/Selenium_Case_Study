run the test cases using: mvn clean test -Dsurefire.suiteXmlFiles=testng.xml
run the python test cases using : python -m pytest -v --html=report.html --self-contained-html
Reports can be find under:
    1. selenium report: target>surefire-reports>index.html
    2. Python report: SeleniumProject>index.html
