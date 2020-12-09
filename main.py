from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_5
from .functions import is_auth
from ryu.lib.packet import ipv4
from ryu.lib.packet import packet

class Switch(app_manager.RyuApp):
	OFP_VERSIONS = [ofproto_v1_5.OFP_VERSION]
	def __init__(self, *args, **kwargs):
		super(Switch, self).__init__(*args, **kwargs)
		msg = ev.msg
		datapath = msg.datapath
		parser = datapath.ofproto_parser
		permit = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, [parser.OFPActionOutput(1),]),]
		datapath.send_msg(parser.OFPFlowMod(datapath=datapath, match = parser.OFPMatch(udp_src = 67, ), instructions = permit, ))
		self.mac_to_port = {}

	@set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
	def event_PacketIn(self, ev):
		msg = ev.msg
		pkt = packet.Packet(msg.data)
		v4 = pkt.get_protocols(ipv4.ipv4)
		datapath = msg.datapath
		parser = datapath.ofproto_parser
		if is_auth(ip_address = v4.src, ):
			permit = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, [parser.OFPActionOutput(2),]),]
			datapath.send_msg(parser.OFPFlowMod(datapath=datapath, match = parser.OFPMatch(ipv4_src = v4.src, tcp_dst = 80, ), instructions = permit, ))
			datapath.send_msg(parser.OFPFlowMod(datapath=datapath, match = parser.OFPMatch(ipv4_src = v4.src, tcp_dst = 443, ), instructions = permit, ))

er.OFPMatch(in_port = msg.match['in_port'], ), actions = [parser.OFPActionOutput(out_port),], data = data, ))

	@set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
	def event_FeaturesRequest(self, ev):
		msg = ev.msg
		datapath = msg.datapath
		parser = datapath.ofproto_parser
		ofproto = datapath.ofproto
		datapath.send_msg(parser.OFPFlowMod(datapath=datapath, match = parser.OFPMatch(), priority = 0, instructions = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER),]),], ))



