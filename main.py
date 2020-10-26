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

	@set_ev_cls(@set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER), MAIN_DISPATCHER)
	def event_FeaturesRequest(self, ev):
		msg = ev.msg
		datapath = msg.datapath
		parser = datapath.ofproto_parser
		datapath.send_msg(parser.OFPFlowMod(datapath=datapath, match = parser.OFPMatch(), priority = 0, ))

	@set_ev_cls(@set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER), MAIN_DISPATCHER)
	def event_PacketIn(self, ev):
		msg = ev.msg
		datapath = msg.datapath
		pkt = packet.Packet(msg.data)
		eth = pkt.get_protocols(ethernet.ethernet)[0]
		self.mac_to_port[datapath.id][eth.src] = msg.match['in_port']
		parser = datapath.ofproto_parser
		if eth.dst in self.mac_to_port[datapath.id]:
			out_port = self.mac_to_port[datapath.id][eth.dst]
		else:
			ofproto = datapath.ofproto
			out_port = ofproto.OFPP_FLOOD
		if out_port != ofproto.OFPP_FLOOD:
			datapath.send_msg(parser.OFPFlowMod(datapath=datapath, match = parser.OFPMatch(in_port = msg.match['in_port'], eth_dst = eth.dst, ), priority = 1, ))
		if ofproto.OFP_NO_BUFFER == msg.buffer_id:
			data = msg.data
		datapath.send_msg(parser.OFPPacketOut(datapath=datapath, buffer_id = msg.buffer_id, match = parser.OFPMatch(in_port = msg.match['in_port'], ), actions = [parser.OFPActionOutput(out_port),], data = data, ))


		datapath.send_msg(parser.OFPPacketOut(datapath=datapath, buffer_id = msg.buffer_id, match = parser.OFPMatch(in_port = msg.match['in_port'], ), actions = [parser.OFPActionOutput(out_port),], data = data, ))

