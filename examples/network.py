from quectel import Network
net = Network()
net.init()
net.query_usim()
net.attach()
