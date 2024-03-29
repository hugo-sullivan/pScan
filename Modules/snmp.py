from pysnmp import hlapi
from scanInterface import ScannerForm

class scanner(ScannerForm):

    def scan(self):
        """
        parameters = {
            "SNMP_bulk": <boolean>,
            "OID": ""(OID trying to investigate),
            "bulk_non_repeaters": int(),
            "bulk_max_repeaters": int()
        }
        """
        targets = self.scan_param["ip-address"]
        for ip in targets:
            self.scan_target(ip)
        
    
    def get_name():
        return "snmp"

    def scan_target(self, target):
        parameters = self.scan_param["packets"]["parameters"]
        if (not parameters["SNMP_bulk"]):
            try:
                print(get(target, [parameters["OID"]], hlapi.CommunityData('public')))
            except:
                "No RESPONSE"
        elif(parameters["SNMP_bulk"]):
            try:
                print(get_bulk(target, [parameters["OID"]], hlapi.CommunityData('public'), parameters["bulk_max_repeaters"], parameters["bulk_non_repeaters"]))
            except:
                "NO RESPONSE"

def get_bulk(target, oids, credentials, count, start_from=0, port=161,
             engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.bulkCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context,
        start_from, count,
        *construct_object_types(oids)
    )
    return fetch(handler, count)

def get(target, oids, credentials, port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.getCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context,
        #hlapi.ObjectType(hlapi.ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0))
        *construct_object_types(oids)
    )
    return fetch(handler, 1)[0]
    
def construct_object_types(list_of_oids):
    object_types = []
    for oid in list_of_oids:
        object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
    return object_types

def cast(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        try:
            return float(value)
        except (ValueError, TypeError):
            try:
                return str(value)
            except (ValueError, TypeError):
                pass
    return value

def fetch(handler, count):
    result = []
    for i in range(count):
        try:
            error_indication, error_status, error_index, var_binds = next(handler)
            if not error_indication and not error_status:
                items = {}
                for var_bind in var_binds:
                    items[str(var_bind[0])] = cast(var_bind[1])
                result.append(items)
            else:
                raise RuntimeError('Got SNMP error: {0}'.format(error_indication))
        except StopIteration:
            break
    return result


