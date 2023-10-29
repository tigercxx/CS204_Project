# CS204_Project

This uses http3
```
sudo docker run -p 2016:2016 -p 2016:2016/udp --rm --name server server

sudo docker run --network="host" -it --rm ymuski/curl-http3 curl -vs -D/dev/stdout -o/dev/null --http3 -k https://localhost:2016
```

```
sudo docker run --network="host" --name client --rm -d client
```

```
sudo docker run -it --rm ymuski/curl-http3 curl -vs -D/dev/stdout -o/dev/null --http3 https://any.marshmaillow.com:2016
```

`DISPLAY=:20 /opt/google/chrome/google-chrome --enable-quic --origin-to-force-quic-on=localhost:2016`

# THIS ONE CAN GET h3 in VM
DISPLAY=:20 /opt/google/chrome/google-chrome --enable-quic --origin-to-force-quic-on=any.marshmaillow.`com:2016,sites.google.com:443`

--origin-to-force-quic-on=
--enable-quic


# Linux
## http 1.1
DISPLAY=:20 /opt/google/chrome/google-chrome --disable-quic --disable-http2 `--origin-to-force-quic-on=any.marshmaillow.com:2016`

## http 2
DISPLAY=:20 /opt/google/chrome/google-chrome --disable-quic --origin-to-force-quic-on=any.`marshmaillow.com:2016 --user-data-dir=./new2`

## http 3
DISPLAY=:20 /opt/google/chrome/google-chrome --enable-quic --origin-to-force-quic-on=any.marshmaillow.`com:2016 --user-data-dir=./new`

# MacOS
## http 1.1
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --disable-quic --disable-http2 `--origin-to-force-quic-on=any.marshmaillow.com:2016 --user-data-dir=./new3`

## http 2
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --disable-quic `--origin-to-force-quic-on=any.marshmaillow.com:2016 --user-data-dir=./new2`

## http 3
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --enable-quic `--origin-to-force-quic-on=any.marshmaillow.com:2016 --user-data-dir=./new`

`sudo tc qdisc add dev docker0 root netem loss 20%`
`sudo tc qdisc del dev docker0 root netem`
`sudo tc qdisc add dev docker0 root tbf rate 1mbit burst 32kbit limit 125000`
`sudo tc qdisc del dev docker0 root`

# Client

Once you run build.sh in the client folder, exec into the container and run this command:
`python3 client.py 10 https://any.marshmaillow.com:2016`

The given requirements.txt in the client folder is for the docker container.
To run visualisation.py, you need the following packages, I recommend creating a virtual environment and installing them there:
- matplotlib
- pandas
- scipy
