from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_5
from ryu.lib.packet import ethernet
from ryu.lib.packet import packet

class Switch(app_manager.RyuApp):
	OFP_VERSIONS = [ofproto_v1_5.OFP_VERSION]
	def __init__(self, *args, **kwargs):
		super(Switch, self).__init__(*args, **kwargs)
		self.mac_to_port = {}

	@set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
	def event_PacketIn(self, ev):
		msg = ev.msg
		datapath = msg.datapath
		pkt = packet.Packet(msg.data)
		eth = pkt.get_protocols(ethernet.ethernet)[0]
		ofproto = datapath.ofproto
		parser = datapath.ofproto_parser
		self.mac_to_port.setdefault(datapath.id, {})
		self.mac_to_port[datapath.id][eth.src] = msg.match['in_port']
		if eth.dst in self.mac_to_port[datapath.id]:
			out_port = self.mac_to_port[datapath.id][eth.dst]
		else:
			out_port = ofproto.OFPP_FLOOD
		if out_port != ofproto.OFPP_FLOOD:
			datapath.send_msg(parser.OFPFlowMod(datapath=datapath, match = parser.OFPMatch(in_port = msg.match['in_port'], eth_dst = eth.dst, ), priority = 1, instructions = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, [parser.OFPActionOutput(out_port),]),], ))
		if ofproto.OFP_NO_BUFFER == msg.buffer_id:
			data = msg.data
		datapath.send_msg(parser.OFPPacketOut(datapath=datapath, buffer_id = msg.buffer_id, match = parser.OFPMatch(in_port = msg.match['in_port'], ), actions = [parser.OFPActionOutput(out_port),], data = data, ))

	@set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
	def event_FeaturesRequest(self, ev):
		msg = ev.msg
		datapath = msg.datapath
		parser = datapath.ofproto_parser
		ofproto = datapath.ofproto
		datapath.send_msg(parser.OFPFlowMod(datapath=datapath, match = parser.OFPMatch(), priority = 0, instructions = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER),]),], ))

= msg.match['in_port'], ), actions = [parser.OFPActionSetField(ipv4_dst = get_origin_ip(port_dst = u.dst_port, ), udp_dst = get_origin_port(port_dst = u.dst_port, ), ), parser.OFPActionOutput(self.mac_to_port[eth.dst]),], ))
		else:
			if True != eth.src in self.mac_to_port:
				self.mac_to_port[eth.src] = msg.match['in_port']
			datapath.send_msg(parser.OFPPacketOut(datapath=datapath, buffer_id = msg.buffer_id, match = parser.OFPMatch(in_port = msg.match['in_port'], ), actions = [parser.OFPActionSetField(ipv4_src = "192.168.1.1", tcp_src = new_port(ip_src = v4.src, port_src = t.src_port, ), ), parser.OFPActionOutput(self.mac_to_port[eth.src]),], ))

o = datapath.ofproto
		datapath.send_msg(parser.OFPFlowMod(datapath=datapath, match = parser.OFPMatch(), priority = 0, instructions = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER),]),], ))

