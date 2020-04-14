# https://github.com/aviddiviner/til/blob/master/devops/write-to-stdin-of-a-background-process.md

mkfifo /tmp/mcfifo
cat > /tmp/mcfifo &
echo $! > /tmp/catpid

#cat /tmp/mcfifo | myapp &
# or
#myapp < /tmp/mcfifo &
