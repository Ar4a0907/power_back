from flask import Blueprint, jsonify
from .db import DeviceInfo, dbSession
from .config import ITEMS_PER_PAGE
from flask import request

bp = Blueprint('devices', __name__)

@bp.route('/devices', methods=['GET'])
def getProfile():

    page = request.args.get('page', default=1, type=int)
    if page < 1:
    	page = 1
    devices = DeviceInfo.query.paginate(page, ITEMS_PER_PAGE, False)
    total = len(dbSession.query(DeviceInfo.id).all())
    arr = []
    for device in devices.items:
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
    	"data" : arr,
    	"total" : total
    }
    

    return jsonify(devicesData)
