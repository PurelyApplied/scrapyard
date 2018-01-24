FlakyDefinitionCommit=

flakyTest() {
  grep '@Category(FlakyTest.class)' ${1}
  outcome=$?
  if [ outcome -eq 1 ] ; then
    return 1;
  else # Grep not found or file not exists is "good"
    return 0;
}

getFlakyAge() {

}

getFlakyFiles() {

}

for thisFile in getFlakyFile() ; do
    getFlakyAge ${thisFile}
done
