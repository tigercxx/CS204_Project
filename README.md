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
