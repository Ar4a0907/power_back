from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from .config import ADMIN_ROLE, ADMIN_STATUS

db = SQLAlchemy()
dbSession = db.session


class Admin(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)

    # Admin Authentication fields
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    loginAttempts = db.Column(db.SmallInteger, default=0)

    # Admin fields
    name = db.Column(db.String(50), nullable=True)
    surname = db.Column(db.String(50), nullable=True)

    status = db.Column(db.SmallInteger, default=ADMIN_STATUS['created'])
    role = db.Column(db.SmallInteger, default=ADMIN_ROLE['admin'])
    created = db.Column(db.DateTime, default=datetime.utcnow)


class DeviceInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)

    createdTime = db.Column(db.DateTime, default=None)
    deviceNo = db.Column(db.String(255), nullable=False)
    deviceName = db.Column(db.String(100), default=None)
    cloudId = db.Column(db.String(100), default=None)
    iccId = db.Column(db.String(200), default=None)
    deviceKey = db.Column(db.String(200), default=None)
    sn = db.Column(db.String(200), default=None)
    deviceState = db.Column(db.Integer(10), nullable=False, default=2)
    trace = db.Column(db.BigInteger(20), default=0)
    spaceNu = db.Column(db.Integer(8), default=None)
    machineNu = db.Column(db.Integer(8), default=None)
    deviceUuid = db.Column(db.String(100), default=None)

    softVersion = db.Column(db.String(100), default=None)
    hardVersion = db.Column(db.String(20), default=None)
    agreementVersion = db.Column(db.String(20), default=None)

    url = db.Column(db.String(255), default=None)
    deviceModel = db.Column(db.String(20), default=None)
    deviceSignal = db.Column(db.String(20), default=None)
    networkType = db.Column(db.String(20), default=None)
    networkOperator = db.Column(db.String(20), default=None)
    deviceIp = db.Column(db.String(20), default=None)
    soleUid = db.Column(db.String(30), default=None)
    placeUid = db.Column(db.String(30), default=None)
    agentUid = db.Column(db.String(30), default=None)


class FindbackLog(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)

    deviceUuid = db.Column(db.String(20), default=None)
    machineUuid = db.Column(db.Text)
    event = db.Column(db.String(10), collation="utf8mb4_unicode_ci", default=None)
    bid = db.Column(db.Integer, default=None)
    createdTime = db.Column(db.DateTime, default=None)


class MPlaceInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)

    createTime = db.Column(db.DateTime, default=None)
    updateTime = db.Column(db.DateTime, default=None)
    chargeNo = db.Column(db.String(50), default=None)
    placeUid = db.Column(db.Integer, default=None)
    placeName = db.Column(db.String(20), default=None)
    placeRemark = db.Column(db.String(50), default=None)
    placeNo = db.Column(db.String(50), default=None)
    lon = db.Column(db.Float(10.6), default=None)
    lat = db.Column(db.Float(10.6), default=None)
    pictureUrl = db.Column(db.String(255), default=None)
    openTime = db.Column(db.String(255), default=None)
    state = db.Column(db.Integer, nullable=False, default=0)
    type = db.Column(db.Integer, nullable=False, default=0)


class OrderPay(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)

    orderType = db.Column(db.Integer, nullable=False, default=0)
    payState = db.Column(db.Integer, nullable=False, default=0)
    payCount = db.Column(db.String(50), collation="utf8mb4_unicode_ci", nullable=False, default=None)
    payMoney = db.Column(db.Integer, nullable=False)
    realMoney = db.Column(db.Integer, default=None)
    outTradeNo = db.Column(db.String(50), collation="utf8mb4_unicode_ci", nullable=False)
    wxOutTradeNo = db.Column(db.String(255), collation="utf8mb4_unicode_ci", default=None)
    prepayId = db.Column(db.String(255), collation="utf8mb4_unicode_ci", default=None)
    expiresIn = db.Column(db.Integer, default=None)
    tradeType = db.Column(db.String(255), collation="utf8mb4_unicode_ci", default=None)
    createdTime = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    payTime = db.Column(db.DateTime, default=None)
    applyRefundTime = db.Column(db.DateTime, default=None)
    refundMoney = db.Column(db.Integer, default=0)
    refundTime = db.Column(db.DateTime, default=None)
    payType = db.Column(db.Integer, nullable=False, default=0)


class OrderRentPay(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)

    orderNo = db.Column(db.String(100), collation="utf8mb4_unicode_ci", nullable=False)
    userId = db.Column(db.Integer, nullable=False, default=0)
    powerNo = db.Column(db.String(50), collation="utf8mb4_unicode_ci", nullable=False)
    money = db.Column(db.Integer, nullable=False, default=0)
    memo = db.Column(db.String(255), collation="utf8mb4_unicode_ci", default=None)
    orderType = db.Column(db.Integer, nullable=False, default=0)
    orderState = db.Column(db.Integer, nullable=False, default=0)
    payWay = db.Column(db.Integer, nullable=False, default=0)
    deviceUuid = db.Column(db.String(20), collation="utf8mb4_unicode_ci", default=None)
    createTime = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    updateTime = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    closeTime = db.Column(db.TIMESTAMP, nullable=True, default=None)
    finishTime = db.Column(db.TIMESTAMP, nullable=True, default=None)
    orderPayNo = db.Column(db.String(255), collation="utf8mb4_unicode_ci", default=None)


class Powerbank(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)

    powerNo = db.Column(db.String(20), nullable=False)
    state = db.Column(db.Integer, nullable=False, default=1)
    powerName = db.Column(db.String(255), default=None)
    powerAd = db.Column(db.Integer(20), default=None)
    positionUuid = db.Column(db.String(50), nullable=False)
    machineUuid = db.Column(db.String(20), nullable=False)
    deviceUuid = db.Column(db.String(20), nullable=False)
    createdTime = db.Column(db.DateTime, nullable=False)
    updateTime = db.Column(db.DateTime, default=None)
    backTime = db.Column(db.DateTime, default=None)
    errorState = db.Column(db.Integer, nullable=False, default=0)
    allPositionUuidRow = db.Column(db.Integer, default=None)
    allPositionUuidCol = db.Column(db.Integer, default=None)
    allPositionUuidld = db.Column(db.Integer, default=None)


class PowerbankLog(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)

    posUuid = db.Column(db.String(20), default=None)
    backResult = db.Column(db.String(10), default=None)
    powerAd = db.Column(db.String(20), default=None)
    powerUuid = db.Column(db.String(50), default=None)
    temp = db.Column(db.String(20), default=None)
    powerbankState = db.Column(db.String(20), default=None)
    bid = db.Column(db.Integer, default=None)


class PowerbankPositionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)

    createTime = db.Column(db.DateTime, default=None)
    positionUuid = db.Column(db.String(20), collation="utf8mb4_unicode_ci", default=None)
    powerNo = db.Column(db.String(100), collation="utf8mb4_unicode_ci", default=None)
    state = db.Column(db.Integer, nullable=False, default=0)
    modifyTime = db.Column(db.DateTime, default=None)
    userId = db.Column(db.Integer, default=None)
    deviceUuid = db.Column(db.String(100), collation="utf8mb4_unicode_ci", default=None)
    backTime = db.Column(db.DateTime, default=None)


class WxaUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)

    nickName = db.Column(db.String(225), collation="utf8mb4_unicode_ci", nullable=False)
    headUrl = db.Column(db.String(225), collation="utf8mb4_unicode_ci", nullable=False)
    sex = db.Column(db.Integer, nullable=False, default=0)
    province = db.Column(db.String(225), collation="utf8mb4_unicode_ci", default=None)
    city = db.Column(db.String(225), collation="utf8mb4_unicode_ci", default=None)
    rent = db.Column(db.Integer, nullable=False, default=0)
    userType = db.Column(db.Integer, nullable=False, default=1)
    loanType = db.Column(db.Integer, nullable=False, default=0)
    unionId = db.Column(db.String(225), collation="utf8mb4_unicode_ci", default=None)
    openId = db.Column(db.String(225), collation="utf8mb4_unicode_ci", nullable=False)
    uuid = db.Column(db.String(225), collation="utf8mb4_unicode_ci", nullable=False)
    debug = db.Column(db.Integer, nullable=False, default=0)
    createdTime = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    country = db.Column(db.String(225), collation="utf8mb4_unicode_ci", default=None)
    money = db.Column(db.Integer, nullable=False, default=0)


class WxaUserFormId(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    
    openId = db.Column(db.String(225), collation="utf8mb4_unicode_ci", nullable=False)
    formId = db.Column(db.String(225), collation="utf8mb4_unicode_ci", nullable=False)
    state = db.Column(db.Integer, nullable=False, default=0)
    createdTime = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)