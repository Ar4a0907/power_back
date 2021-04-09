from flask import Blueprint, jsonify
from .db import DeviceInfo

bp = Blueprint('devices', __name__)

@bp.route('/devices', methods=['GET'])
def getProfile():

    devices = DeviceInfo.query.all()
    arr = []
    for device in devices:
    	arr.append({
			"id" : device.id,
			"createdTime" : device.createdTime,
			"deviceNo" : device.deviceNo,
			"deviceName" : device.deviceName,
			"cloudId" : device.cloudId,
			"iccId" : device.iccId,
			"deviceKey" : device.deviceKey,
			"sn" : device.sn,
			"deviceState" : device.deviceState,
			"trace" : device.trace,
			"spaceNu" : device.spaceNu,
			"machineNu" : device.machineNu,
			"deviceUuid" : device.deviceUuid,
			"softVersion" : device.softVersion,
			"hardVersion" : device.hardVersion,
			"agreementVersion" : device.agreementVersion,
			"url" : device.url,
			"deviceModel" : device.deviceModel,
			"deviceSignal" : device.deviceSignal,
			"networkType" : device.networkType,
			"networkOperator" : device.networkOperator,
			"deviceIp" : device.deviceIp,
			"soleUid" : device.soleUid,
			"placeUid" : device.placeUid,
			"agentUid" : device.agentUid
        })

    devicesData = {
        'devices' : arr
    }

    return jsonify(devicesData)
