#!/bin/sh

# Subcommand architecture credit to https://gist.github.com/waylan/4080362
ProgName=$(basename $0)

# should be in server directory
SERVER_PATH="server.jar"
FIFO_PATH="mcfifo"
LOG_PATH="logs/latest.log"
PID_PATH="server.pid"

COMMAND="java -Xms1G -Xmx1G -jar $SERVER_PATH nogui"


sub_init() {
  rm $FIFO_PATH
  mkfifo $FIFO_PATH
  java -jar $SERVER_PATH --initSettings
  echo "Now change the eula"
}

sub_help() {
  echo "Usage: $ProgName <subcommand> [options]\n"
  echo "Subcommands:"
  echo "    start   start the server"
  echo "    stop    stop the server"
  echo "    attach  connect to the stdin and stdout of the server"
  echo "    init    setup the fifo and add the eula server.properties"
  echo ""
  echo "For help with each subcommand run:"
  echo "$ProgName <subcommand> -h|--help"
  echo ""
}

sub_start() {
  echo "Starting..."
  tail -f $FIFO_PATH | $COMMAND 1>/dev/null 2>&1 &
  echo $! > $PID_PATH 
}

sub_stop() {
  echo "Stopping..."
  kill `cat $PID_PATH`
}

sub_attach() {
  echo "Attaching..."
  trap 'kill %1' EXIT
  tail -f $LOG_PATH &
  cat /dev/stdin > $FIFO_PATH
}

sub_ps() {
  ps `cat $PID_PATH`
}

#run_server
subcommand=$1
case $subcommand in
    "" | "-h" | "--help")
        sub_help
        ;;
    *)
        shift
        sub_${subcommand} $@
        if [ $? = 127 ]; then
            echo "Error: '$subcommand' is not a known subcommand." >&2
            echo "       Run '$ProgName --help' for a list of known subcommands." >&2
            exit 1
        fi
        ;;
esac
