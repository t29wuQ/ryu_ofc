from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_5
from ryu.lib.packet import ipv4
from ryu.lib.packet import packet
from functions.napt import get_origin_ip
from ryu.lib.packet import udp
from functions.napt import get_origin_port
from ryu.lib.packet import ethernet
from functions.napt import new_port
from ryu.lib.packet import tcp

class Switch(app_manager.RyuApp):
	OFP_VERSIONS = [ofproto_v1_5.OFP_VERSION]
	def __init__(self, *args, **kwargs):
		super(Switch, self).__init__(*args, **kwargs)
		self.mac_to_port = 

	@set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
	def event_FeaturesRequest(self, ev):
		msg = ev.msg
		datapath = msg.datapath
		parser = datapath.ofproto_parser
		ofproto = datapath.ofproto
		datapath.send_msg(parser.OFPFlowMod(datapath=datapath, match = parser.OFPMatch(), priority = 0, instructions = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER),]),], ))

	@set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
	def event_PacketIn(self, ev):
		msg = ev.msg
		pkt = packet.Packet(msg.data)
		v4 = pkt.get_protocols(ipv4.ipv4)
		datapath = msg.datapath
		parser = datapath.ofproto_parser
		u = pkt.get_protocols(udp.udp)
		eth = pkt.get_protocols(ethernet.ethernet)[0]
		t = pkt.get_protocols(tcp.tcp)
		if v4.dst == "192.168.1.1":
			if ipv4.proto == 6:
				datapath.send_msg(parser.OFPPacketOut(datapath=datapath, buffer_id = msg.buffer_id, match = parser.OFPMatch(in_port = msg.match['in_port'], ), actions = [parser.OFPActionSetField(ipv4_dst = get_origin_ip(port_dst = u.dst_port, ), tcp_dst = get_origin_port(port_dst = u.dst_port, ), ), parser.OFPActionOutput(self.mac_to_port[eth.dst]),], ))
			elif ipv4.proto == 17:
				datapath.send_msg(parser.OFPPacketOut(datapath=datapath, buffer_id = msg.buffer_id, match = parser.OFPMatch(in_port = msg.match['in_port'], ), actions = [parser.OFPActionSetField(ipv4_dst = get_origin_ip(port_dst = u.dst_port, ), udp_dst = get_origin_port(port_dst = u.dst_port, ), ), parser.OFPActionOutput(self.mac_to_port[eth.dst]),], ))
		else:
			if True != eth.src in self.mac_to_port:
				self.mac_to_port[eth.src] = msg.match['in_port']
			datapath.send_msg(parser.OFPPacketOut(datapath=datapath, buffer_id = msg.buffer_id, match = parser.OFPMatch(in_port = msg.match['in_port'], ), actions = [parser.OFPActionSetField(ipv4_src = "192.168.1.1", tcp_src = new_port(ip_src = v4.src, port_src = t.src_port, ), ), parser.OFPActionOutput(self.mac_to_port[eth.src]),], ))

o = datapath.ofproto
		datapath.send_msg(parser.OFPFlowMod(datapath=datapath, match = parser.OFPMatch(), priority = 0, instructions = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER),]),], ))

