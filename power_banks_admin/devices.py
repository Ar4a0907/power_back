from flask import Blueprint, jsonify
from .db import DeviceInfo

bp = Blueprint('devices', __name__)

@bp.route('/devices', methods=['GET'])
def getProfile():

    devices = DeviceInfo.query.all()
    arr = []
    for i in devices:
    	arr.append({
      		"id" : i.id,
            "createdTime" : i.createdTime,
            "deviceNo" : i.deviceNo,
            "deviceName" : i.deviceName,
            "cloudId" : i.cloudId,
            "iccId" : i.iccId,
            "deviceKey" : i.deviceKey,
            "sn" : i.sn,
            "deviceState" : i.deviceState,
            "trace" : i.trace,
            "spaceNu" : i.spaceNu,
            "machineNu" : i.machineNu,
            "deviceUuid" : i.deviceUuid,
            "softVersion" : i.softVersion,
            "hardVersion" : i.hardVersion,
            "agreementVersion" : i.agreementVersion,
            "url" : i.url,
            "deviceModel" : i.deviceModel,
            "deviceSignal" : i.deviceSignal,
            "networkType" : i.networkType,
            "networkOperator" : i.networkOperator,
            "deviceIp" : i.deviceIp,
            "soleUid" : i.soleUid,
            "placeUid" : i.placeUid,
            "agentUid" : i.agentUid
        })

    devicesData = {
        'devicesArray' : arr
    }

    return jsonify(devicesData)
