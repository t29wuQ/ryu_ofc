from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_5
from ryu.lib.packet import udp
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet

class Switch(app_manager.RyuApp):
	OFP_VERSIONS = [ofproto_v1_5.OFP_VERSION]
	def __init__(self, *args, **kwargs):
		super(Switch, self).__init__(*args, **kwargs)
		self.mac_to_port = {}

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
		u = pkt.get_protocols(udp.udp)
		datapath = msg.datapath
		parser = datapath.ofproto_parser
		eth = pkt.get_protocols(ethernet.ethernet)[0]
		if u.dst_port == 68:
			datapath.send_msg(parser.OFPPacketOut(datapath=datapath, buffer_id = msg.buffer_id, match = parser.OFPMatch(in_port = msg.match['in_port'], ), actions = [parser.OFPActionOutput(self.mac_to_port[eth.dst]),], ))
		else:
			permit = []

datapath.ofproto_parser
		ofproto = datapath.ofproto
		datapath.send_msg(parser.OFPFlowMod(datapath=datapath, match = parser.OFPMatch(), priority = 0, instructions = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER),]),], ))

path=datapath, match = parser.OFPMatch(ipv4_src = v4.src, tcp_dst = 443, ), instructions = permit, ))
			else:
				datapath.send_msg(parser.OFPPacketOut(datapath=datapath, buffer_id = msg.buffer_id, match = parser.OFPMatch(in_port = msg.match['in_port'], ), actions = [parser.OFPActionOutput(3),], ))

	@set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
	def event_FeaturesRequest(self, ev):
		msg = ev.msg
		datapath = msg.datapath
		parser = datapath.ofproto_parser
		ofproto = datapath.ofproto
		datapath.send_msg(parser.OFPFlowMod(datapath=datapath, match = parser.OFPMatch(), priority = 0, instructions = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER),]),], ))

