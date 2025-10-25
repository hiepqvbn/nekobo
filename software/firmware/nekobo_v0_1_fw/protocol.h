#ifndef NEKOBO_PROTOCOL_H
#define NEKOBO_PROTOCOL_H

// Generated protocol header - do not edit by hand. Run tools/sync_protocol.py

// Protocol version
#define PROTOCOL_VERSION "1"

#define MSG_MOVE 0x01
#define MSG_STOP 0x02
#define MSG_SET_LED 0x03
#define MSG_SENSOR_REPORT 0x81
#define MSG_HEARTBEAT_REQ 0x10
#define MSG_HEARTBEAT_RESP 0x82

// Error codes
#define ERR_MISSING_ARGS 0x01

#endif // NEKOBO_PROTOCOL_H
