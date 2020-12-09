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

rt = ofproto.OFPP_FLOOD
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



