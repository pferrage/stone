#!/usr/bin/env bash

# Use este script para testar se um host/porta TCP está disponível
#
# Exemplo de uso: ./wait-for-it.sh google.com:80 -- echo "Google está no ar"

cmdname=$(basename $0)

echoerr() { if [[ $QUIET -ne 1 ]]; then echo "$@" 1>&2; fi }

usage()
{
    cat << USAGE >&2
Usage:
    $cmdname host:port [-t timeout] [-- command args]
    -q | --quiet                        Não exibir mensagens de status
    -t TIMEOUT | --timeout=timeout      Timeout em segundos, zero para sem timeout
    -- COMMAND ARGS                     Executar comando com args após o teste
USAGE
    exit 1
}

wait_for()
{
    if [[ $TIMEOUT -gt 0 ]]; then
        echoerr "$cmdname: esperando $TIMEOUT segundos por $HOST:$PORT"
    else
        echoerr "$cmdname: esperando por $HOST:$PORT sem timeout"
    fi
    start_ts=$(date +%s)
    while :
    do
        if [[ $ISBUSY -eq 1 ]]; then
            nc -z $HOST $PORT
            result=$?
        else
            (echo > /dev/tcp/$HOST/$PORT) >/dev/null 2>&1
            result=$?
        fi
        if [[ $result -eq 0 ]]; then
            end_ts=$(date +%s)
            echoerr "$cmdname: $HOST:$PORT está disponível após $((end_ts - start_ts)) segundos"
            break
        fi
        sleep 1
    done
    return $result
}

wait_for_wrapper()
{
    # Para suportar SIGINT durante o timeout: https://unix.stackexchange.com/a/57692
    if [[ $QUIET -eq 1 ]]; then
        timeout $TIMEOUT $0 -q -t 0 -- "$HOST:$PORT" &
    else
        timeout $TIMEOUT $0 -t 0 -- "$HOST:$PORT" &
    fi
    WAITFORPID=$!
    trap "kill -INT -$WAITFORPID" INT
    wait $WAITFORPID
    WAITFORRESULT=$?
    trap - INT
    return $WAITFORRESULT
}

check_cmd_exists()
{
    local CMD=$1
    command -v $CMD >/dev/null 2>&1
}

check_host_port_format()
{
    local HP=$1
    if [[ $HP != *:* ]]; then
        echoerr "$cmdname: formato inválido de host:porta"
        usage
    fi
    HOST=$(echo $HP | cut -d : -f 1)
    PORT=$(echo $HP | cut -d : -f 2)
    if [[ -z "$HOST" || -z "$PORT" ]]; then
        echoerr "$cmdname: formato inválido de host:porta"
        usage
    fi
}

if [[ $# -lt 1 ]]; then
    usage
fi

QUIET=0
TIMEOUT=15
ISBUSY=0

while [[ $# -gt 0 ]]
do
    case "$1" in
        *:* )
        check_host_port_format $1
        shift 1
        ;;
        -q | --quiet)
        QUIET=1
        shift 1
        ;;
        -t)
        TIMEOUT="$2"
        if [[ $TIMEOUT == "" ]]; then break; fi
        shift 2
        ;;
        --timeout=*)
        TIMEOUT="${1#*=}"
        shift 1
        ;;
        --)
        shift
        break
        ;;
        -h | --help)
        usage
        ;;
        *)
        echoerr "Argumento desconhecido: $1"
        usage
        ;;
    esac
done

if ! check_cmd_exists timeout; then
    echoerr "$cmdname: comando 'timeout' ausente"
    exit 1
fi

if ! check_cmd_exists nc; then
    ISBUSY=1
fi

if [[ $TIMEOUT -gt 0 ]]; then
    wait_for_wrapper
else
    wait_for
fi

shift $((OPTIND-1))

if [[ $# -gt 0 ]]; then
    exec "$@"
else
    exit 0
fi
